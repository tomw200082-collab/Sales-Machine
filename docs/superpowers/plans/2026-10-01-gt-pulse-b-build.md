# GT Pulse Unit B — Build Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Execution mode (decided):** inline in this session, because the local PostgreSQL inner loop is session-local; fresh subagents only for the independent review (Task 28). Tom's standing rule applies throughout: no new business, commercial or product-policy decision is taken by the executor; a missing decision stops the work with a recommendation and its main alternative.

**Goal:** Every verified Shopify business customer is exactly one `sales_core` org, with verified contacts and a full, reconciled order history, live in production, per spec `docs/superpowers/specs/2026-10-01-gt-pulse-b-design.md` (v2, approved by Tom 2026-10-01).

**Architecture:** A Railway job pulls Shopify (bulk operations) into stage tables; the SQL function `mirror_promote` runs the whole apply (mirror rows, identity layer, chain memberships, contacts, review tasks) either rolled back (dry-run: report and digest) or committed (apply, on Tom's count-specific go). One SQL function (`link_org_shopify`) is the only writer of the Shopify link. Views and routes are shaped by link status and by a reconciliation publication gate. The portal org screen follows only after Tom approves mockups and the first string batch.

**Tech Stack:** PostgreSQL 17 (Supabase) + pgTAP, Node 22 + Fastify + Kysely + `pg`, Vitest and `tsx --test`, Deno Edge Functions, GitHub Actions, Next.js 15 (portal), Playwright.

## Global Constraints

Copied from the spec and the repositories' rules; every task includes them.

- **Tom decides business, commercial and product policy.** Engineering that implements an approved decision proceeds; every reading of the spec that goes beyond its literal text is listed under "Interpretations" at the end and goes to Tom in the final report.
- `stock_ledger` append-only; the sales module reads factory core only through curated views and writes nothing there (no `private_core`, `order_intake`, `customer_portal` write). `rebuild_verifier() = 0` before and after every production migration and the apply.
- No customer-facing send path; `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` and the frozen Shopify flags are not touched; no write to Shopify, Green Invoice or LionWheel.
- Migrations: additive only; next slot = highest + 1 with a listing of `db/migrations/` immediately before and after each numbered write (FR1/FR2); a new file appearing in between is a HALT (`contract_failure`). Never in a `deploy-production.yml` glob: `0353`, `0354`. Each B migration is wrapped in `begin … commit`, sets `lock_timeout = '5s'`, is idempotent, and is frozen once applied (fixes go forward in a new slot).
- Money is ex-VAT: the sum of line `discountedTotalSet.shopMoney` (`recipes/sales-report.md`, D-012). Buckets in Asia/Jerusalem. Never tax, net or gross columns, `amountSpent` or `currentTotalPriceSet`. Amounts are `numeric(14,2)`; digests use integer agorot.
- Order class precedence: draft, test, cancelled, refunded, completed. Clean = completed or refunded. Verified customer = a clean order in all history, a `client_key` non-blank after trim, and no review tag. Active = a clean order in the last 12 months (a label, not a condition).
- Customer personal data only for verified and review customers; no `id_nomber`, no email, no notes; evidence rows hold salted hashes, never raw values; nothing personal in append-only payloads; customers outside B1 and review are counted and never stored (not even in stage tables).
- Committed files and images in the public repositories (Sales-Machine, the portal, the brain) contain no customer name, id, amount, order or contact: fixtures are synthetic. CI fails on a phone or email pattern in fixtures.
- Shopify: the mirror module pins its own API version, checks the served `X-Shopify-API-Version`, contains no `mutation` (test), and never stores, logs or returns the bulk download URL; `mirror_run.error_detail` holds codes and GIDs only.
- Coded errors are `raise exception 'SALES_<CODE>: …'` and are tested with pgTAP `throws_matching`. After PR-2 no reader treats `shopify_customer_id is not null` as proof of a customer: readers use `sales_core.org_link_is_verified(...)` (views, routes) or `sales_core.org_link_trusted(...)` (the three pre-cutover readers, Task 9).
- Hebrew UI strings only from the register after Tom approves them; the sales route group is Hebrew-first and RTL; every portal change is one bounded tranche with a manifest registered in `docs/portal-os/registry.md`.
- Git: never `git add -A` or `git add .`; branch `claude/new-session-muj7mx` in every repo, reset from fresh `origin/main` after each merge; draft PR; after every `create_pull_request` call `unsubscribe_pr_activity` immediately and again on any `subscription.created` notice; no PR watching, check-ins or Routines unless Tom asks; merge only on green checks.
- Tests: local PostgreSQL 16 through `gtpg.sh` for the inner loop (always under `env -i`; never the production `DATABASE_URL`); GitHub CI on PG17 is the authority. Each SQL and Node task lands red, then green. A pgTAP file's `plan(n)` equals the number of assertions it lists (pgTAP fails the file on a mismatch). Report N/N.

## File Structure

**Backend `/home/user/gt-factory-os`**

| Path | Responsibility |
|---|---|
| `.github/workflows/sales-db.yml` | the gate (extended in PR-1, PR-3) |
| `db/ci/skipped_migrations.txt`, `db/ci/expected_test_failures.txt`, `db/ci/schema_fingerprint.sql`, `db/ci/gen_chain_seed.mjs` | pinned CI baselines, fingerprint query, chain seed generator |
| `db/migrations/<N>…<N+6>` | M1 (additive): order class, org identity, chains, mirror tables, contacts, promote functions, reader functions |
| `db/migrations/<N+7>` | M2 (cutover; applied only in W6 step 5) |
| `db/migrations/<N+8>` | M3 (the refresh `pg_cron` entry; applied only in W6 step 6) |
| `db/tests/<slot>_*.test.sql` | one pgTAP file per migration (several for the promote functions) |
| `api/src/sales/mirror/` | `client.ts`, `bulk.ts`, `parse.ts`, `eligibility.ts`, `stage.ts`, `run.ts`, `refresh.ts`, `reconcile.ts`, `shopifyql.ts`, `chain.ts`, `promote_customer.ts`, `fixtures/`, `__tests__/` |
| `api/src/internal/jobs/sales_shopify_mirror_route.ts` | the job route (202 + run id) |
| `api/src/sales/orgs_handler.ts`, `orgs_routes.ts` | org detail, orders, river, contacts, circle, list, search, identity review, mutations |
| `api/src/sales/queries_handler.ts` | `/tasks` filters out identity tasks |
| `api/test/sales_orgs.test.ts`, `api/test/sales_link_writers.test.ts` | role matrix; repo-level sole-writer test |
| `supabase/functions/sales-leads-poll/`, `supabase/functions/sales-sleeping-radar/` | evidence-only lookup, readers through the SQL predicates, radar bearer check |
| `.claude/skills/customer-setup-shopify-gi/SKILL.md` | §5 records evidence instead of updating the org |

**Portal `/home/user/gt-factory-os-portal`** (only after Tom approves mockups and string round 1): tranches 189+, `src/app/(sales)/sales/orgs/[id]/page.tsx`, `_components/org/*`, `_lib/labels.ts`, proxies under `src/app/api/sales/…`.

**Sales-Machine `/home/user/Sales-Machine`:** this plan, `CURRENT_STATE.md`, `doctrine/decisions.md`, the masterprompt status line.

## Local test harness (used by every task)

`G=/tmp/claude-0/-home-user/9a0fba27-af96-5382-9ff0-2839d814676d/scratchpad/gtpg.sh`: `$G up`, `$G reset`, `$G apply` (the CI apply loop; expect `Applied: 296; skipped: 48` before B), `$G test <file>…`, `$G psql …`. The local cluster listens on `127.0.0.1:55432` with trust auth. CI log retrieval: `get_job_logs` with `return_content=false` returns a pre-signed `logs_url`; download it with `curl` through the proxy and `grep`.

---

## PR-1 — CI scaffolding (backend)

### Task 1: Pin today's skipped migrations and failing tests; fail on anything new

**Files:**
- Create: `db/ci/skipped_migrations.txt` (the 48 names), `db/ci/expected_test_failures.txt` (the 17 failing `db/tests/03*.test.sql` names from the local baseline), `db/ci/schema_fingerprint.sql`
- Modify: `.github/workflows/sales-db.yml`

**Interfaces — produces the CI contract:** a skipped migration not in the pinned list fails the job; a `db/tests/03*.test.sql` failure not in the pinned list fails the job; a pinned failure that now passes fails the job (prune the pin); `# Looks like` fails; a missing test file fails.

- [ ] **Step 1: Write the pinned files from the local baseline**

```bash
G=/tmp/claude-0/-home-user/9a0fba27-af96-5382-9ff0-2839d814676d/scratchpad/gtpg.sh
S=/tmp/claude-0/-home-user/9a0fba27-af96-5382-9ff0-2839d814676d/scratchpad
$G reset && $G apply                           # Applied: 296; skipped: 48
sort $S/skipped.txt > db/ci/skipped_migrations.txt
grep '^FAIL' $S/test-baseline.txt | sed 's/^FAIL //' | sort > db/ci/expected_test_failures.txt
wc -l db/ci/skipped_migrations.txt db/ci/expected_test_failures.txt     # 48 and 17
```

- [ ] **Step 2: Write `db/ci/schema_fingerprint.sql`** (one deterministic row per object class in `sales_core` and `api_read`)

```sql
select 'columns', md5(string_agg(table_schema||'.'||table_name||'|'||column_name||'|'||data_type||'|'||is_nullable||'|'||coalesce(column_default,''), E'\n' order by table_schema, table_name, column_name))
  from information_schema.columns where table_schema in ('sales_core','api_read')
union all select 'constraints', md5(string_agg(conrelid::regclass::text||'|'||conname||'|'||pg_get_constraintdef(oid), E'\n' order by conrelid::regclass::text, conname))
  from pg_constraint where connamespace = 'sales_core'::regnamespace
union all select 'indexes', md5(string_agg(tablename||'|'||indexname||'|'||indexdef, E'\n' order by tablename, indexname))
  from pg_indexes where schemaname = 'sales_core'
union all select 'functions', md5(string_agg(p.oid::regprocedure::text||'|'||pg_get_functiondef(p.oid), E'\n' order by p.oid::regprocedure::text))
  from pg_proc p where p.pronamespace = 'sales_core'::regnamespace and p.prokind = 'f'
union all select 'views', md5(string_agg(schemaname||'.'||viewname||'|'||definition, E'\n' order by schemaname, viewname))
  from pg_views where schemaname in ('sales_core','api_read')
union all select 'triggers', md5(string_agg(tgrelid::regclass::text||'|'||tgname||'|'||pg_get_triggerdef(oid), E'\n' order by tgrelid::regclass::text, tgname))
  from pg_trigger where not tgisinternal and tgrelid::regclass::text like 'sales_core.%';
```

- [ ] **Step 3: Rewrite the apply and test steps of `sales-db.yml`.** The apply loop appends each skipped file name to `/tmp/skipped.txt` and then runs `diff <(sort /tmp/skipped.txt) db/ci/skipped_migrations.txt`. The test step globs:

```bash
failed=()
for file in db/tests/03*.test.sql; do
  [ -f "$file" ] || { echo "MISSING $file"; exit 1; }
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -At -f "$file" > /tmp/gt-pgtap.log 2>&1 || true
  if grep -q -E '^not ok|# Looks like|^psql:.*ERROR' /tmp/gt-pgtap.log; then failed+=("$(basename "$file")"); fi
done
printf '%s\n' "${failed[@]:-}" | sed '/^$/d' | sort > /tmp/failed.txt
diff /tmp/failed.txt db/ci/expected_test_failures.txt     # any difference fails: a new failure, or a pin that can be pruned
```

The path filter gains `supabase/functions/sales-*/**`, `api/src/internal/**`, `.claude/skills/customer-setup-shopify-gi/**` (`db/**` already covers `db/ci/**`). The existing named pgTAP loop (8 files) is removed, because the glob contains them.

- [ ] **Step 4: Add the idempotency step after the apply step:** `psql … -At -f db/ci/schema_fingerprint.sql > /tmp/fp1.txt`; re-apply every migration numbered `0363` and above (`for f in $(ls db/migrations/*.sql | awk -F/ '{split($3,a,"_"); if (a[1] >= "0363") print}')`); `psql … > /tmp/fp2.txt`; `diff /tmp/fp1.txt /tmp/fp2.txt`. With no such migration yet the step passes as a no-op.
- [ ] **Step 5: Prove red, then green.** Locally: add a bogus name to a temporary copy of the pinned skip list and show `diff` fails. In CI: push (must be green), then a throwaway commit that deletes one line from `expected_test_failures.txt` must turn the run red; record both run URLs (download `logs_url`, grep the `diff` output); revert the throwaway.
- [ ] **Step 6: Commit** (`ci(sales): pin skipped migrations and expected test failures, fail on anything new`), open a draft PR, `unsubscribe_pr_activity`, wait for green, mark ready, squash-merge, reset the branch from `origin/main`.

**Evidence:** both run URLs; `Applied: 296; skipped: 48` in the log; the 48- and 17-line pins.

### Task 2: Run every sales API test in CI

**Files:** Modify `.github/workflows/sales-db.yml`; Create `api/test/ci/expected_failures.txt` only if needed.

- [ ] **Step 1:** locally `cd api && npm ci --include=dev && env -i PATH="$PATH" HOME="$HOME" DATABASE_URL=postgresql://postgres@127.0.0.1:55432/gt_test npx tsx --test --test-concurrency=1 test/sales_*.test.ts`; record N/N per file.
- [ ] **Step 2:** replace the three named `tsx --test` steps (`sales_workspace_tasks`, `sales_workspace`, `sales_leads_poll_alerts`) with the glob `npx tsx --test --test-concurrency=1 test/sales_*.test.ts`; pin any failing file in `api/test/ci/expected_failures.txt` with the same `diff` rule as Task 1.
- [ ] **Step 3:** add a root-level step `npx vitest run api/src/sales/mirror --maxWorkers=1 --minWorkers=1` guarded by `ls api/src/sales/mirror/__tests__/*.test.ts 2>/dev/null` so it is a no-op until PR-3.
- [ ] **Step 4:** CI green; commit; merge with Task 1's PR if it is still open.

---

## PR-2 — Schema and SQL logic, M1 (backend)

Every task follows one cycle: write the pgTAP file first (red on the local database), then the migration (green), then the whole local baseline (`31 pass, 17 fail` unchanged) and the idempotency check (apply the migration twice; fingerprints equal). Slots: list `db/migrations/` immediately before writing each numbered file and again after. M1 files in order: `N sales_order_class`, `N+1 sales_org_identity`, `N+2 sales_chain`, `N+3 sales_mirror_tables`, `N+4 sales_contacts`, `N+5 sales_mirror_promote`, `N+6 sales_reader_functions` (N = highest + 1 at write time, 0363 today). Task 14 adds one more M1-numbered file for the reconcile functions.

### Task 3: Order class function

**Files:** Create `db/migrations/<N>_sales_order_class.sql`, `db/tests/<N>_sales_order_class.test.sql`.

**Interfaces — produces:** `sales_core.order_class(p_kind text, p_test boolean, p_cancelled_at timestamptz, p_refund_count integer) returns text` (immutable); `sales_core.is_clean_class(p_class text) returns boolean`.

- [ ] **Step 1: Failing test (the truth table)**

```sql
begin;
create extension if not exists pgtap;
select plan(12);
select is(sales_core.order_class('draft', false, null, 0), 'draft', 'draft stays draft');
select is(sales_core.order_class('draft', true, now(), 2), 'draft', 'draft wins over test, cancelled and refunded');
select is(sales_core.order_class('order', true, now(), 2), 'test', 'test wins over cancelled and refunded');
select is(sales_core.order_class('order', false, now(), 2), 'cancelled', 'cancelled wins over refunded');
select is(sales_core.order_class('order', false, null, 1), 'refunded', 'a refund record makes it refunded');
select is(sales_core.order_class('order', false, null, 0), 'completed', 'a plain order is completed');
select is(sales_core.order_class('order', false, null, null), 'completed', 'a null refund count is zero');
select ok(sales_core.is_clean_class('completed') and sales_core.is_clean_class('refunded'), 'completed and refunded are clean');
select ok(not sales_core.is_clean_class('cancelled') and not sales_core.is_clean_class('test') and not sales_core.is_clean_class('draft'), 'cancelled, test and draft are not clean');
select is(sales_core.is_clean_class(null), false, 'a null class is not clean');
select is((select provolatile::text from pg_proc where oid = 'sales_core.order_class(text,boolean,timestamptz,integer)'::regprocedure), 'i', 'order_class is immutable');
select throws_matching($$select sales_core.order_class('weird', false, null, 0)$$, '^SALES_ORDER_KIND', 'an unknown kind is refused');
select * from finish();
rollback;
```

- [ ] **Step 2: Run red:** `$G test db/tests/<N>_sales_order_class.test.sql` → FAIL (function does not exist).
- [ ] **Step 3: Implement**

```sql
begin;
set local lock_timeout = '5s';

create or replace function sales_core.order_class(
  p_kind text, p_test boolean, p_cancelled_at timestamptz, p_refund_count integer)
returns text language plpgsql immutable as $$
begin
  if coalesce(p_kind, '') not in ('order', 'draft') then
    raise exception 'SALES_ORDER_KIND: unknown order kind %', p_kind;
  end if;
  return case
    when p_kind = 'draft'                then 'draft'
    when coalesce(p_test, false)         then 'test'
    when p_cancelled_at is not null      then 'cancelled'
    when coalesce(p_refund_count, 0) > 0 then 'refunded'
    else 'completed' end;
end $$;

create or replace function sales_core.is_clean_class(p_class text)
returns boolean language sql immutable as $$ select coalesce(p_class in ('completed', 'refunded'), false) $$;

commit;
```

- [ ] **Step 4: Run green; commit** (`db(sales): order_class and is_clean_class`).

### Task 4: Org identity — link writer, evidence, event log, rep scope, link predicates

**Files:** `db/migrations/<N+1>_sales_org_identity.sql`, `db/tests/<N+1>_sales_org_identity.test.sql`.

**Interfaces — produces (exact):**
```
sales_core.org (+ shopify_link_status text check in ('verified','review','disputed','retired'), owner_email text, created_by_run uuid, retired_by_run uuid, merged_into_org_id uuid references sales_core.org)
sales_core.org_event(id uuid pk, org_id uuid not null references sales_core.org, event_type text check in (identity_linked, identity_review, identity_disputed, identity_resolved, identity_reverted, identity_merged, org_retired, owner_assigned, contact_added, contact_verified, contact_rejected, contact_redacted), payload jsonb not null default '{}', actor text not null, run_id uuid, created_at timestamptz not null default now())   -- append-only
sales_core.org_identity_evidence(id uuid pk, org_id uuid not null references sales_core.org, shopify_customer_id text, source text check in ('shopify','lead','customer_portal_access','customer_book','customer_setup','manager'), kind text check in ('shopify_id','phone_exact','manual'), value_hash text not null, source_ref text, source_updated_at timestamptz, run_id uuid, created_at timestamptz not null default now())   -- append-only
sales_core.value_hash(p_value text) returns text                         -- salted sha256; salt = app_setting 'identity_salt'
sales_core.record_org_identity_evidence(p_org uuid, p_customer text, p_source text, p_kind text, p_value text, p_ref text, p_source_updated timestamptz, p_run uuid) returns uuid
sales_core.link_org_shopify(p_org uuid, p_customer text, p_status text, p_evidence jsonb, p_actor text, p_run uuid) returns void
sales_core.unlink_org_shopify(p_org uuid, p_actor text, p_run uuid) returns void     -- clears id and status of a pre-existing org (rollback of a link); writes identity_reverted
sales_core.rep_can_read_org(p_email text, p_org uuid) returns boolean
sales_core.org_link_is_verified(p_customer_id text, p_status text) returns boolean   -- strict: id is not null and status = 'verified'
sales_core.org_link_trusted(p_customer_id text, p_status text) returns boolean       -- M1: id is not null and (status is null or status = 'verified'); M2 redefines it as org_link_is_verified (Task 17)
```
The guard trigger is **not** created here (M2). `link_org_shopify` and `unlink_org_shopify` set `sales.link_writer = 'on'` (transaction-local) around their own `update`, which is what the M2 guard will look for. `p_evidence` is a jsonb array of `{source, kind, value, ref, source_updated_at}` objects; each is passed through `record_org_identity_evidence`, which stores only `value_hash`.

```sql
create or replace function sales_core.value_hash(p_value text) returns text
language sql stable as $$
  select encode(sha256(convert_to(
    (select value->>'v' from sales_core.app_setting where key = 'identity_salt') || ':' || p_value, 'UTF8')), 'hex') $$;

-- salt: inserted once, never rotated (rotation would orphan every stored hash)
insert into sales_core.app_setting(key, value)
select 'identity_salt', jsonb_build_object('v', replace(gen_random_uuid()::text || gen_random_uuid()::text, '-', ''))
 where not exists (select 1 from sales_core.app_setting where key = 'identity_salt');

create or replace function sales_core.link_org_shopify(
  p_org uuid, p_customer text, p_status text, p_evidence jsonb, p_actor text, p_run uuid)
returns void language plpgsql as $$
declare v_old_customer text; v_old_status text; e jsonb;
begin
  if p_status not in ('verified','review','disputed','retired') then
    raise exception 'SALES_LINK_STATUS: bad status %', p_status; end if;
  if p_customer is not null and p_customer not like 'gid://shopify/Customer/%' then
    raise exception 'SALES_LINK_BAD_GID: %', p_customer; end if;
  if p_customer is not null and exists (select 1 from sales_core.org where shopify_customer_id = p_customer and id <> p_org) then
    raise exception 'SALES_LINK_CONFLICT: customer already held by another org'; end if;
  select shopify_customer_id, shopify_link_status into v_old_customer, v_old_status
    from sales_core.org where id = p_org for update;
  if not found then raise exception 'SALES_LINK_NO_ORG: %', p_org; end if;
  perform set_config('sales.link_writer', 'on', true);
  update sales_core.org
     set shopify_customer_id = p_customer, shopify_link_status = p_status,
         retired_by_run = case when p_status = 'retired' then p_run else retired_by_run end,
         updated_at = now()
   where id = p_org;
  perform set_config('sales.link_writer', 'off', true);
  for e in select * from jsonb_array_elements(coalesce(p_evidence, '[]'::jsonb)) loop
    perform sales_core.record_org_identity_evidence(p_org, p_customer, e->>'source', e->>'kind',
      e->>'value', e->>'ref', nullif(e->>'source_updated_at','')::timestamptz, p_run);
  end loop;
  insert into sales_core.org_event(org_id, event_type, payload, actor, run_id)
  values (p_org,
    case p_status when 'verified' then 'identity_linked' when 'review' then 'identity_review'
                  when 'disputed' then 'identity_disputed' else 'org_retired' end,
    jsonb_build_object('from_status', v_old_status, 'to_status', p_status,
                       'customer', coalesce(p_customer, v_old_customer)),
    p_actor, p_run);
end $$;
```

- [ ] **Step 1: Failing tests** (`plan(27)`; each line is one assertion, with its expected result):
  1–2. UPDATE and DELETE on `org_event` raise `…append-only…` (`throws_matching`). 3–4. same for `org_identity_evidence`.
  5. `link_org_shopify(org, 'gid://shopify/Order/1', 'verified', '[]', 't', null)` raises `^SALES_LINK_BAD_GID`. 6. `'123'` raises the same. 7. status `'maybe'` raises `^SALES_LINK_STATUS`.
  8. a valid call writes `shopify_customer_id` and `shopify_link_status = 'verified'`. 9. it writes exactly one `identity_linked` event whose payload has `customer`, `from_status`, `to_status`. 10. it writes one evidence row per element of `p_evidence`.
  11. linking a customer already held by another org raises `^SALES_LINK_CONFLICT` and changes nothing. 12. status `'retired'` with `p_customer = null` clears the id, sets `retired_by_run` and writes `org_retired` whose payload still names the old customer.
  13. `unlink_org_shopify` clears id and status of a linked lead-born org, keeps the org, and writes `identity_reverted` naming the old customer. 14. it raises `^SALES_LINK_NO_ORG` for an unknown org. 15. the evidence rows survive the unlink.
  16. `value_hash('+972501110363')` is 64 hex characters. 17. it is stable across two calls. 18. it differs for `'+972501110364'`. 19. it does not contain the input. 20. `identity_salt` exists once after the migration runs twice.
  21. `rep_can_read_org('rep@x', org)` is true for an org behind a lead with `assignee = 'rep@x'`. 22. true when `owner_email = 'rep@x'`. 23. false for an org behind another assignee's lead. 24. false for an org with no lead and no owner.
  25. `org_link_is_verified('gid://shopify/Customer/1', 'verified')` is true, and false for `'review'`, `'disputed'`, `'retired'` and for `(null, 'verified')` (one `ok` over the five). 26. `org_link_trusted('gid://shopify/Customer/1', 'review')` is false, `(null, 'verified')` is false and `('gid://shopify/Customer/1', 'verified')` is true (stable across M1 and M2; the null-status case is asserted only in Task 17's test). 27. `record_org_identity_evidence` rejects a `kind` outside the check list.
- [ ] **Steps 2–4:** run red; implement (the DDL for the two logs copies the `lead_event` append-only trigger pattern from `0318`/`0320`); run green; run the sales baseline (`$G test db/tests/0318…0362` — unchanged results); commit (`db(sales): org identity layer, link writer, evidence`).

### Task 5: Chains

**Files:** `db/migrations/<N+2>_sales_chain.sql` (tables, functions, and the generated seed), `db/tests/<N+2>_sales_chain.test.sql`, `db/ci/gen_chain_seed.mjs`.

**Interfaces — produces:**
```
sales_core.chain(id uuid pk, key text unique not null, segment text not null, kind text not null check (kind in ('רשת','מפיץ')), note text, roster_badge text, single_record_note text, status text check (status is null or status = 'moved_to_distributor'), moved_to text, moved_on text check (moved_on is null or moved_on ~ '^[0-9]{4}-[0-9]{2}$'), group_key text, serves text[] not null default '{}', source_sha text not null, seeded_at timestamptz not null default now())
sales_core.chain_rule(id uuid pk, chain_id uuid not null references sales_core.chain, kind text check (kind in ('match','exclude')), pattern text not null, unique (chain_id, kind, pattern))
sales_core.chain_branch_group(id uuid pk, chain_id uuid not null references sales_core.chain, entry jsonb not null)      -- display only (the file's branch_merge entries)
sales_core.chain_member(id uuid pk, chain_id uuid not null references sales_core.chain, shopify_customer_id text not null unique check (shopify_customer_id like 'gid://shopify/Customer/%'), basis text not null check (basis in ('map_rule','manual')), approved_run uuid, approved_by text, created_at timestamptz not null default now())
sales_core.chain_flat(p text) returns text                 -- the reference normalisation of scripts/sales-report/build_facts.py::_flat
sales_core.chain_rule_hits(p_display_name text) returns table(chain_id uuid, key text)
```
`chain_flat` must equal the reference `re.sub(r'[\s"\'׳״.\-]+', ' ', s.replace('״','"')).strip()`; PG's `[[:space:]]` depends on the locale, so whitespace is enumerated explicitly:

```sql
create or replace function sales_core.chain_flat(p text) returns text language sql immutable as $$
  select btrim(regexp_replace(replace(coalesce(p, ''), '״', '"'),
    '[ \t\n\r\f\v\x1c-\x1f\x85   -     　"''׳״.-]+', ' ', 'g'), ' ')
$$;
create or replace function sales_core.chain_rule_hits(p_display_name text)
returns table(chain_id uuid, key text) language sql stable as $$
  with f as (select sales_core.chain_flat(p_display_name) as flat)
  select c.id, c.key from sales_core.chain c, f
   where exists (select 1 from sales_core.chain_rule r where r.chain_id = c.id and r.kind = 'match'   and position(r.pattern in f.flat) > 0)
     and not exists (select 1 from sales_core.chain_rule r where r.chain_id = c.id and r.kind = 'exclude' and position(r.pattern in f.flat) > 0)
$$;
```
The seed is generated, never hand-written: `node db/ci/gen_chain_seed.mjs /home/user/gt-factory-os-production-brain/docs/sales/chain_map.json` prints idempotent `insert … on conflict (key) do update` rows for the 48 chains (the file is `{ "_doc": …, "chains": { "<name>": { segment, kind, match[], exclude[]?, note?, roster_badge?, single_record_note?, status?, moved_to?, moved_on?, group?, serves[]?, branch_merge[]? } } }`), their rules and their branch-merge entries, with `source_sha` = the file's git blob SHA (`git hash-object`, equal to the GitHub contents API `sha`; `c5f53793d2286fe9be356d540b5ebc24f845c084` at plan time). The output is appended to the migration file after the DDL.

- [ ] **Step 1: Failing tests** (`plan(16)`): 1–12 `chain_flat` golden table, one `is()` per synthetic input (an NBSP, a gershayim, a geresh, a hyphen run, leading and trailing spaces, a dotted abbreviation, mixed Hebrew and Latin, an empty string, null, and three more), with expected outputs generated once during development by the Python reference (`python3 -c` over the same inputs) and pasted into the test; 13. `chain_rule_hits` returns one row for a synthetic name that contains a `match` pattern of chain A and none of A's `exclude` patterns (a chain inserted inside the test transaction); 14. a name hitting two chains returns two rows (the caller detects the conflict; the function never resolves it); 15. an `exclude` hit returns zero rows; 16. seeded data: `chain` has 48 rows, `chain_member` is empty, every chain has at least one `match` rule and all rows share one `source_sha` (one `is` over the concatenated string `'48|0|0|1'`, where the third field counts chains without a match rule and the fourth counts distinct `source_sha`).
- [ ] **Steps 2–4:** red, implement, green, commit. The commit message records `seed identical to generator output` after re-running the generator and `diff`.

### Task 6: Mirror tables, stage tables, run lease, exceptions

**Files:** `db/migrations/<N+3>_sales_mirror_tables.sql`, `db/tests/<N+3>_sales_mirror_tables.test.sql`.

**Interfaces — produces:**
```
sales_core.mirror_run(id uuid pk default gen_random_uuid(), kind text not null check (kind in ('backfill','refresh','customer_sweep','anti_join','reconcile','promote_customer')), status text not null default 'running' check (status in ('running','staged','applied','failed','pass','fail')), parent_run_id uuid references sales_core.mirror_run, cutoff_t timestamptz, started_at timestamptz not null default now(), heartbeat_at timestamptz not null default now(), finished_at timestamptz, api_version text, bulk_sha256 text, counts jsonb not null default '{}', report jsonb, digest text, expected_count int, expected_digest text, approved_by text, approval_note text, error_code text, error_detail jsonb check (error_detail is null or error_detail::text !~ 'https?://'))
unique index mirror_run_one_running on sales_core.mirror_run ((true)) where status = 'running'
sales_core.mirror_exception(id uuid pk, run_id uuid references sales_core.mirror_run, kind text check in ('cap_exceeded','stale_refresh','chain_map_changed','chain_conflict','b1_fact_mismatch','reconcile_failed','order_gone','customer_unresolved'), detail jsonb not null default '{}', created_at timestamptz not null default now(), resolved_at timestamptz, resolved_by text)
sales_core.shopify_customer(gid text pk, display_name text, client_key text, tags text[] not null default '{}', shopify_created_at timestamptz, shopify_updated_at timestamptz, synced_at timestamptz not null default now(), last_run_id uuid)
sales_core.shopify_customer_phone(customer_gid text references sales_core.shopify_customer on delete cascade, e164 text, field text check (field in ('default','address')), primary key (customer_gid, e164))
sales_core.shopify_order(order_gid text pk, shopify_customer_id text references sales_core.shopify_customer(gid), kind text check (kind in ('order','draft')), order_name text, created_at timestamptz, processed_at timestamptz, cancelled_at timestamptz, closed_at timestamptz, test boolean not null default false, financial_status text, fulfillment_status text, source_name text, tags text[] not null default '{}', refund_count int not null default 0, edited boolean not null default false, subtotal numeric(14,2), current_subtotal numeric(14,2), lines_ex_vat numeric(14,2), currency text, shopify_updated_at timestamptz, draft_status text, deleted_at timestamptz, first_run_id uuid, last_run_id uuid, synced_at timestamptz not null default now())
sales_core.shopify_order_line(order_gid text references sales_core.shopify_order on delete cascade, line_gid text, sku text, title text, quantity int, current_quantity int, original_total numeric(14,2), discounted_total numeric(14,2), product_gid text, variant_gid text, primary key (order_gid, line_gid))
index on shopify_order (shopify_customer_id, created_at desc); index on shopify_order (shopify_updated_at)
sales_core.v_shopify_order  -- shopify_order.* + sales_core.order_class(kind, test, cancelled_at, refund_count) as class + sales_core.is_clean_class(...) as is_clean
sales_core.mirror_stage_customer(run_id uuid references mirror_run on delete cascade, gid text, display_name text, client_key text, tags text[], shopify_created_at timestamptz, shopify_updated_at timestamptz, b1_result text check (b1_result in ('verified','review_tagged','review_active_no_key','manual')), clean_orders int not null, last_clean_order_at timestamptz, primary key (run_id, gid))
sales_core.mirror_stage_customer_phone(run_id, customer_gid, e164, field, primary key (run_id, customer_gid, e164), foreign key (run_id, customer_gid) references mirror_stage_customer on delete cascade)
sales_core.mirror_stage_order(run_id, order_gid, customer_gid, + the shopify_order columns except deleted_at/first_run_id/last_run_id, primary key (run_id, order_gid))
sales_core.mirror_stage_order_line(run_id, order_gid, line_gid, + the shopify_order_line columns, primary key (run_id, order_gid, line_gid), foreign key (run_id, order_gid) references mirror_stage_order on delete cascade)
sales_core.mirror_start_run(p_kind text, p_cutoff timestamptz default null, p_parent uuid default null) returns uuid
sales_core.mirror_heartbeat(p_run uuid) returns void
sales_core.mirror_finish_run(p_run uuid, p_status text, p_counts jsonb default null, p_error_code text default null, p_error_detail jsonb default null) returns void
sales_core.history_published() returns boolean       -- the latest kind='reconcile' row has status 'pass'
api_read.v_sales_org_list  -- see below, shaped from day one with org_link_is_verified and history_published()
```
`mirror_start_run` first fails every `running` row whose `heartbeat_at < now() - interval '15 minutes'` (`error_code = 'lease_expired'`) and then inserts the new `running` row; the partial unique index turns a race into `unique_violation`, which the function re-raises as `SALES_MIRROR_RUNNING`. The composite daily refresh is one parent run holding the lease; its steps write into the parent's `counts.steps`, and reconcile results are separate `kind = 'reconcile'` rows inserted already `pass` or `fail` (never `running`), so they never contend for the lease.

`api_read.v_sales_org_list` (created here, not in M2): one row per non-retired org with `id, display_name, shopify_link_status, owner_email, last_activity_at, has_open_lead` plus the shaped columns `is_active_customer, last_order_at, orders_12m, ex_vat_12m_agorot, chain_name`, each `case when sales_core.org_link_is_verified(o.shopify_customer_id, o.shopify_link_status) and sales_core.history_published() then … end`, aggregated from `v_shopify_order` where `is_clean` and `deleted_at is null` (12 months in Asia/Jerusalem).

- [ ] **Step 1: Failing tests** (`plan(16)`): 1. a second `mirror_start_run` while one is running raises `^SALES_MIRROR_RUNNING`; 2. a run whose `heartbeat_at` is 16 minutes old is failed with `error_code = 'lease_expired'` by the next start and that start succeeds; 3. a run that heartbeated 14 minutes ago is untouched and the second start still raises; 4. `v_shopify_order.class` equals `order_class(...)` on five seeded rows, one per class; 5. `is_clean` is true for exactly two of them; 6. money columns are `numeric(14,2)` (`information_schema`); 7. a stage customer rejects a GID that is not a customer GID; 8. deleting a run cascades its stage rows; 9. `history_published()` is false with no reconcile row; 10. true after a `pass` row; 11. false after a later `fail` row; 12. `v_sales_org_list` returns null shaped columns for an org with status `review`; 13. null for `verified` while `history_published()` is false; 14. real values for `verified` with a `pass` reconcile; 15. `mirror_exception.kind` rejects an unknown kind; 16. `mirror_finish_run('failed', …, error_detail := '{"u":"https://x"}')` is rejected by the URL check.
- [ ] **Steps 2–4:** red, implement, green, commit.

### Task 7: Contacts and access log

**Files:** `db/migrations/<N+4>_sales_contacts.sql`, `db/tests/<N+4>_sales_contacts.test.sql`.

**Interfaces — produces:**
```
sales_core.contact(id uuid pk, org_id uuid not null references sales_core.org, display_name text, phone_e164 text, email text, kind text not null check (kind in ('person','org_channel')), verification text not null default 'unverified' check (verification in ('unverified','verified','rejected')), verified_by text, verified_at timestamptz, verification_basis text, redacted_at timestamptz, created_by_run uuid, created_at timestamptz not null default now(), updated_at timestamptz not null default now())
  unique (org_id, phone_e164) where phone_e164 is not null and redacted_at is null; unique (org_id, lower(email)) where email is not null and redacted_at is null
sales_core.contact_source(id uuid pk, contact_id uuid not null references sales_core.contact, source_system text check (source_system in ('lead','wa_customer_map','customer_portal_access','customer_book','manager')), source_ref text, source_field text, observed_at timestamptz not null default now(), source_updated_at timestamptz, value_hash text not null, run_id uuid)   -- append-only
sales_core.access_log(id uuid pk, actor text not null, org_id uuid, route text not null, at timestamptz not null default now())
sales_core.add_contact(p_org uuid, p_name text, p_phone text, p_email text, p_kind text, p_source_system text, p_source_ref text, p_source_field text, p_source_updated timestamptz, p_run uuid) returns uuid
sales_core.verify_contact(p_contact uuid, p_actor text, p_basis text) returns void
sales_core.reject_contact(p_contact uuid, p_actor text) returns void
sales_core.promote_contact(p_contact uuid, p_name text, p_actor text) returns void     -- org_channel → person, name required; stays unverified
sales_core.redact_contact(p_contact uuid, p_actor text) returns void                   -- nulls name, phone, email; keeps row and sources; writes contact_redacted
```
`add_contact` normalises the phone with `normalize_phone_il`, refuses an implausible one (`SALES_CONTACT_PHONE`), merges into an existing `(org, e164)` contact by adding only a `contact_source` row, and writes a `contact_added` event (payload: ids only). A contact without a source row cannot exist: `add_contact` inserts the contact and its first source row in one function, and a deferred constraint trigger checks it at commit.

- [ ] **Step 1: Failing tests** (`plan(16)`): 1. `add_contact` with `'050-111-0363'` stores `+972501110363`; 2. a phone failing plausibility raises `^SALES_CONTACT_PHONE`; 3. the same phone twice for one org leaves one contact and two source rows; 4. the same phone for two orgs gives two contacts; 5. a bare `insert into sales_core.contact` without a source row fails at commit (`throws_matching` over a deferred check); 6–7. `contact_source` UPDATE and DELETE raise; 8. `verify_contact` sets `verified_by`, `verified_at`, `verification_basis`; 9. it writes `contact_verified`; 10. `reject_contact` writes `contact_rejected`; 11. `promote_contact` on an `org_channel` without a name raises `^SALES_CONTACT_NAME`; 12. with a name it sets `kind = 'person'` and keeps `verification`; 13. `promote_contact` on a `person` raises; 14. `redact_contact` nulls name, phone and email, keeps the row and its sources, sets `redacted_at`; 15. the `contact_redacted` payload contains no raw value (`payload::text !~ '050|972|@'`); 16. a redacted contact's phone can be added again as a new contact.
- [ ] **Steps 2–4:** red, implement, green, commit.

### Task 8: `mirror_promote` — rows, B1 facts, identity, chains, contacts, digest, report, refresh, one-customer promotion, rollback

This is the core. Built as small functions, each with its own test file, then composed. **Files:** `db/migrations/<N+5>_sales_mirror_promote.sql`, `db/tests/<N+5>_sales_mirror_rows.test.sql`, `…_identity.test.sql`, `…_chains_contacts.test.sql`, `…_promote.test.sql`.

**Interfaces — produces:**
```
sales_core.mirror_apply_rows(p_run uuid) returns jsonb          -- stage → shopify_customer/_phone/_order/_order_line by GID; first_run_id on insert, last_run_id always; an order absent from the stage is untouched; replaces the lines of a changed order
sales_core.mirror_check_b1_facts(p_run uuid) returns int         -- count of staged customers whose clean_orders/last_clean_order_at differ from the staged orders recomputed with order_class; must be 0
sales_core.identity_derive(p_run uuid, p_caps boolean default false) returns jsonb   -- the transition table below; p_caps applies the refresh caps
sales_core.chain_propose(p_run uuid, p_attach boolean) returns jsonb               -- backfill attaches map_rule members; refresh turns new hits into review tasks
sales_core.contacts_ingest(p_run uuid) returns jsonb
sales_core.mirror_digest(p_run uuid) returns jsonb               -- {count, digest}
sales_core.mirror_report(p_run uuid) returns jsonb               -- every field in "Report" below
sales_core.mirror_promote(p_run uuid, p_commit boolean default false, p_expected_count int default null, p_expected_digest text default null, p_approver text default null) returns jsonb
sales_core.mirror_promote_refresh(p_run uuid) returns jsonb      -- refuses unless a kind='backfill' run is 'applied'; identity_derive(p_caps := true)
sales_core.mirror_promote_one(p_run uuid, p_actor text) returns jsonb   -- the manual promotion of one staged customer (b1_result 'manual')
sales_core.mirror_rollback(p_run uuid, p_actor text) returns jsonb      -- see "Rollback"
```
`mirror_promote` runs `mirror_apply_rows`, `mirror_check_b1_facts`, `identity_derive`, `chain_propose(true)`, `contacts_ingest`, `mirror_digest`, `mirror_report` inside `begin … exception when sqlstate 'MR001' then null end`; with `p_commit = false` it raises `MR001` after the report is held in a local variable, so every table change rolls back and the report is returned (and stored in `mirror_run.report` by a final update after the block). With `p_commit = true` it requires `p_approver`, `p_expected_count` and `p_expected_digest` non-null, recomputes the digest and raises `SALES_MIRROR_DIGEST_MISMATCH` on any difference, requires `b1_fact_mismatch = 0` and `order_coverage.difference = 0`, deletes the run's stage rows, and sets `status = 'applied'`, `approved_by`, `approval_note`, `expected_*`. It raises `SALES_MIRROR_NOT_STAGED` unless the run is `staged`.

**Identity transition table (the contract of `identity_derive`; each row traces to spec §3.6, T1, T3, T4).** `V` = staged customers with `b1_result = 'verified'`; `R` = `review_tagged` or `review_active_no_key`; `H(C)` = the non-retired org holding `shopify_customer_id = C`; `K(O)` = staged customers whose phones contain org `O`'s `phone_e164`; `multi(C)` = C is a member (or rule hit) of a chain with two or more branches; a lead-born org is a non-retired org with no id and no `created_by_run`.

| # | Condition | Action | Event / task |
|---|---|---|---|
| 1 | `C ∈ V`, `H(C)` exists, status `verified` | none | none |
| 2 | `C ∈ V`, `H(C) = O` exists, status null / `review` / `disputed`, `O.phone ∈ phones(C)`, `\|K(O)\| = 1`, not `multi(C)` | `verified`; evidence `phone_exact` and `shopify_id` | `identity_linked`; close task `system:identity` |
| 3 | as 2 but `\|K(O)\| ≥ 2` | `disputed` | `identity_disputed`; task reason `phone_shared` (payload: both GIDs) |
| 4 | as 2 but `multi(C)` | `disputed` | `identity_disputed`; task reason `chain_branch` |
| 5 | as 2 but `O.phone ∉ phones(C)` (the id is unproven) | `review` | `identity_review`; task reason `id_unproven` |
| 6 | `C ∈ R`, `H(C)` exists | `review` | `identity_review`; task reason `b1_review_tag` or `b1_active_no_client_key` |
| 7 | an org holds an id whose customer is not staged (no clean order, no longer resolves, or lost B1) | `review` | `identity_review`; task reason `customer_not_verified` |
| 8 | `C ∈ V`, no `H(C)`, no lead-born org `O` with `O.phone ∈ phones(C)` | create org (display name from Shopify; `phone_e164`, `email`, `email_domain` null; `created_by_run`), link `verified`, evidence `shopify_id` (source `shopify`) | `identity_linked` |
| 9 | `C ∈ V`, no `H(C)`, exactly one such lead-born `O`, `\|K(O)\| = 1`, not `multi(C)` | link `O` to `C` as `verified`; evidence `phone_exact` | `identity_linked` |
| 10 | `C ∈ V`, no `H(C)`, such `O` with `\|K(O)\| ≥ 2` | `O` becomes `disputed` (no id); `C` still gets an org by row 8 (no placeholder is created for the dispute) | `identity_disputed`; task reason `phone_shared` on `O` |
| 11 | `C ∈ V`, `H(C)` exists (or is created in this run), a lead-born `O` with `O.phone ∈ phones(C)`, `\|K(O)\| = 1`, not `multi(C)` | **merge**: `update sales_core.lead set org_id = H(C)` for `O`'s leads, retire `O` (`merged_into_org_id`) | `identity_merged` on both orgs |
| 12 | `C ∈ R`, no `H(C)` | create org in `review` (same fields as row 8) | `identity_review`; task reason as row 6 |
| 13 | `b1_result = 'manual'` | create org (row 8) or link `verified` to the existing one, evidence `manual` by the actor | `identity_linked` |
| 14 | a task's condition no longer holds | cancel the task, `cancelled_by = 'system:identity'`, reason `condition_cleared` | none |

A rep-visible effect follows only from status `verified`; `review`, `disputed` and `retired` are gate-4 states. Identity tasks: `task.org_id`, kind `other`, `source_kind = 'identity_review'`, `source_id = <customer gid>`, `source_key = 'identity_review:<gid>:<reason>:<md5 of the sorted evidence hashes>'`, `owner_email` null, `due_at = now()`, `created_by = 'system:identity'`; a second reason on the same customer creates a second task. Evidence from `wa_customer_map` counts only when the row was mapped by a person and never when it records several accounts sharing a number. `identity_derive(p_caps := true)` stops after counting: if rows 8/9/12 would create more than 10 orgs, rows 2/9/13 more than 10 links, or `contacts_ingest` more than 20 contacts, the identity step is skipped and one `mirror_exception` (`cap_exceeded`, detail = the three counts) is written; mirror rows have already been applied.

**Rollback (`mirror_rollback`, spec §3.4).** For the run: orgs created by it (`created_by_run`) are retired through `link_org_shopify(…, null, 'retired', …)`; pre-existing orgs it linked go through `unlink_org_shopify`; review tasks it created are cancelled with reason `rollback`; mirror rows with `first_run_id = run` are deleted (lines cascade); chain members it attached are deleted; each change writes `identity_reverted`. Merges are **not** undone (leads are never moved back silently); the return value lists them for a manager.

**Digest lines** (sorted, joined with `\n`, `md5`): orders `O|<order_gid>|<class>|<agorot>|<customer_gid>`; identity `I|<customer_gid>|<action>|<status>|<evidence kinds sorted, comma-joined>`; contacts `C|<customer_gid or org:<existing org uuid>>|<source_system>|<kind>|<value_hash>`; chain members `M|<customer_gid>|<chain key>`. No id generated by the run enters a line, so a dry-run and its apply produce the same digest. `count` is the number of lines.

**Report fields** (jsonb): `orders_by_class`, `orders_by_kind`, `customers_verified`, `customers_review`, `customers_excluded` (from `mirror_run.counts`, split by last-order year as `excluded_no_client_key_by_year`), `orgs_created`, `orgs_linked`, `orgs_merged`, `orgs_disputed`, `orgs_review`, `contacts_added`, `verified_only_by_zero_orders`, `today_card_changes` (`gained_returning_customer`, `lost_returning_customer`; computed from open leads with the old predicate `shopify_customer_id is not null or shopify_snapshot_at is not null` versus the new `status = 'verified'`, restricted to the `returning_customer` branch of `v_sales_today`), `chain_members`, `chain_conflicts` (customers matching two chains), `order_coverage` (`{total, mirrored, no_customer, excluded_customers, difference}`, from the `mirror_run.counts` keys the job writes: `orders_total`, `drafts_total`, `orders_no_customer`, `orders_excluded_customers`, `drafts_excluded_customers`, `oldest_order_at`), `b1_fact_mismatch`, `digest`, `count`.

- [ ] **Step 1: Failing tests, one concern per file** (the descriptions are the assertions):
  - *rows:* apply twice leaves identical row counts; the second run keeps `first_run_id`; a changed order replaces its lines; money columns equal the stage values; an order absent from a later stage is untouched; a customer's phones are replaced as a set; `mirror_check_b1_facts` is 0 for consistent facts; it is 1 when `clean_orders` is wrong; applying rows never touches a table outside `sales_core`; a stage customer with an unknown `b1_result` is impossible (check constraint).
  - *identity:* one test per table row 1–14; plus a rerun creates nothing new; a tagged customer with a clean order and a `client_key` is `review`, not verified; an active customer with a blank-after-trim `client_key` is `review`; the merged org's leads now point at the surviving org and the `lead_event` rows are untouched; a retired org keeps its history; the task key changes when the evidence changes; a task is cancelled by `system:identity` when its condition clears; a customer GID outside `V ∪ R` gets no org; `identity_derive(p_caps := true)` with 11 would-be orgs creates none and writes one `cap_exceeded` exception; with exactly 10 it creates all ten.
  - *chains and contacts:* a customer matching one chain becomes a `map_rule` member in the backfill; in a refresh the same hit creates a review task (`chain_rule_hit`) and no member; `exclude` wins; two chains → no member and one `chain_conflicts` entry; a lead's contact becomes an unverified person; a staff-mapped `wa_customer_map` phone without a name becomes an unverified `org_channel`; a row whose `notes` contain `auto-resolved from Shopify` creates nothing; an approved portal-access row creates an unverified `org_channel`; a `customer_book` contact with `field_sources->>'contact_name' = 'lionwheel'` is ignored; a phone failing plausibility creates nothing; a session phone linked to a completed mirror order of the org (`wa_session.shopify_draft_id`) is `verified` with basis `approved_order`; contacts for an excluded customer are impossible.
  - *promote:* `p_commit = false` leaves `shopify_order`, `org`, `task`, `chain_member`, `contact` row counts unchanged and returns every report field; the same stage yields the same `digest` in two separate sessions; changing one order total by `0.01` changes it; `p_commit = true` with the right count and digest commits and marks the run `applied`; with a wrong digest it raises `^SALES_MIRROR_DIGEST_MISMATCH` and leaves nothing; with a null approver it raises; on a run that is not `staged` it raises `^SALES_MIRROR_NOT_STAGED`; the apply deletes the run's stage rows while the dry-run does not; `order_coverage.difference ≠ 0` makes the apply refuse; `mirror_promote_refresh` raises before any applied backfill and, after one, applies rows and respects the caps; `mirror_promote_one` creates one org for a `manual` customer and nothing else; `today_card_changes` equals the count of `returning_customer` rows in `v_sales_today` before and after on a seeded fixture; the report holds no phone, email or customer name (`report::text` regex against the fixture values); `mirror_rollback` retires created orgs, unlinks linked ones, deletes mirror rows by `first_run_id`, cancels the run's review tasks and lists merges, and the hashes of the non-append-only tables outside `org`, `task`, `chain_member` and `contact` equal their pre-apply values.
- [ ] **Step 2: Run red** for each file as it is written (`$G test db/tests/<N+5>_sales_*.test.sql`).
- [ ] **Step 3: Implement function by function** in the order of the interface list, running the matching test file green before the next. `identity_derive` is set-based (temp tables `tmp_stage`, `tmp_phone_match`, `tmp_plan`), applies through `link_org_shopify`, `unlink_org_shopify` and `add_contact`, and returns counts plus the plan lines used by the digest.
- [ ] **Step 4:** full local baseline (`31 pass, 17 fail` + the new files green), idempotency fingerprints; commit.

### Task 9: Reader functions (additive; flipped atomically by M2)

**Files:** `db/migrations/<N+6>_sales_reader_functions.sql`, `db/tests/<N+6>_sales_reader_functions.test.sql`.

**Interfaces — produces:** `sales_core.radar_org_batch(p_limit integer) returns table(id uuid, shopify_customer_id text)`:

```sql
select o.id, o.shopify_customer_id
  from sales_core.org o
 where o.shopify_customer_id is not null
   and sales_core.org_link_trusted(o.shopify_customer_id, o.shopify_link_status)
   and exists (select 1 from sales_core.lead l where l.org_id = o.id)
 order by o.id
 limit p_limit
```
(Orgs with at least one lead only, today's behaviour; M2 changes `org_link_trusted`, so the same function then requires `verified`.)

- [ ] **Step 1: Failing tests** (`plan(5)`): an org with an id and a lead is returned; an org with an id and no lead is not; an org with no id is not; an org with status `review` and a lead is not; `p_limit` is honoured. (The legacy `status is null` case is not asserted here, because M2 removes it; Task 10 proves it in production by set equality at the moment M1 is applied.)
- [ ] **Steps 2–4:** red, implement, green, commit.

### Task 10: Ship PR-2 and apply M1 to production

- [ ] **Step 1:** push; draft PR; `unsubscribe_pr_activity`; wait for `sales-db` and `typecheck` green (download `logs_url`; confirm `# Looks like` count 0, the pinned diffs empty, the idempotency step green).
- [ ] **Step 2:** a throwaway commit that breaks one new pgTAP assertion must turn `sales-db` red (record the URL), then revert it.
- [ ] **Step 3 (production, additive; spec §3.13 step 2 — from the branch, before the merge):** announce one line; `rebuild_verifier()` through the Supabase connector must be 0; record the production result of `select array_agg(o.id order by o.id) from sales_core.org o where o.shopify_customer_id is not null and exists (select 1 from sales_core.lead l where l.org_id = o.id)` (call it `S0`); dispatch `deploy-production.yml` on the PR branch with `confirm=APPLY`, `skip_deploy=true`, `migrations` = the exact list of the M1 files (never `0353`/`0354`); then check `information_schema`/`pg_proc` for every new object, `rebuild_verifier() = 0` again, and that `select array_agg(id order by id) from sales_core.radar_org_batch(500)` equals `S0` (the readers' behaviour is unchanged).
- [ ] **Step 4:** mark ready, squash-merge, reset the branch from `origin/main`.

**Evidence:** run URLs (red and green), the workflow run URL for M1, both verifier values, the `S0` equality.

---

## PR-3 — Mirror job (backend Node)

### Task 11: Shopify client with paging, cost-aware retry, version check

**Files:** Create `api/src/sales/mirror/client.ts`, `__tests__/client.test.ts`; Modify `api/src/order-intake/shopify/graphql.ts` (return `extensions` additively).

**Interfaces — produces:**
```ts
export const MIRROR_API_VERSION = '2026-07';   // checked against the Shopify docs at write time; the only version constant of the module
export interface MirrorGql {
  query<T>(q: string, vars?: Record<string, unknown>): Promise<{ data: T; cost?: number; servedVersion: string }>;
  pages<T>(q: string, vars: Record<string, unknown>,
    path: (d: any) => { nodes: T[]; pageInfo: { hasNextPage: boolean; endCursor: string | null } }): AsyncGenerator<T>;
}
export function createMirrorGql(cfg: { domain: string; token: string; fetch?: typeof fetch; sleep?: (ms: number) => Promise<void> }): MirrorGql;
```
- [ ] **Step 1: Failing tests (vitest, fake fetch):** a `THROTTLED` response (HTTP 200, `errors[0].extensions.code`, `extensions.cost.throttleStatus.currentlyAvailable = 10`, `restoreRate = 50`, `requestedQueryCost = 200`) makes the client sleep `ceil((200 - 10) / 50 * 1000)` ms and retry, at most 5 tries, then throw `SALES_MIRROR_THROTTLED` — never empty data; HTTP 401 and 403 throw `SALES_MIRROR_AUTH` at once; an `X-Shopify-API-Version` different from `MIRROR_API_VERSION` throws `SALES_MIRROR_VERSION`; `pages` follows cursors across three pages and yields every node; the token is `SALES_MIRROR_SHOPIFY_TOKEN` and falls back to `SHOPIFY_ADMIN_API_TOKEN` (env test); the module source contains no `mutation` (a test reads every file under `api/src/sales/mirror/` except `__tests__` and asserts `!/\bmutation\b/i`).
- [ ] **Steps 2–4:** red, implement (reuse `createShopifyGraphQL`), green; run the order-bot suites (`npx vitest run api/src/order-intake`) to prove the shared client change is additive; commit.

### Task 12: Bulk operations and JSONL parsing

**Files:** `api/src/sales/mirror/bulk.ts`, `parse.ts`, `__tests__/bulk.test.ts`, `__tests__/parse.test.ts`, `fixtures/*.jsonl` (synthetic; a test fails on any phone or email pattern under `fixtures/`).

**Interfaces — produces:**
```ts
export async function runBulk(gql: MirrorGql, bulkQuery: string, opts?: { pollMs?: number; maxPolls?: number;
  download?: (url: string) => Promise<AsyncIterable<string>> }): Promise<{ lines: AsyncIterable<string>; objectCount: number; sha256: Promise<string> }>;
export interface ParsedLine { gid: string; sku: string | null; title: string; quantity: number; currentQuantity: number; originalAgorot: number; discountedAgorot: number; productGid: string | null; variantGid: string | null }
export interface ParsedOrder { gid: string; customerGid: string | null; kind: 'order' | 'draft'; name: string; createdAt: string; processedAt: string | null; cancelledAt: string | null; closedAt: string | null; test: boolean; financialStatus: string | null; fulfillmentStatus: string | null; sourceName: string | null; tags: string[]; refundCount: number; edited: boolean; subtotalAgorot: number; currentSubtotalAgorot: number; linesAgorot: number; currency: string; updatedAt: string; draftStatus: string | null; lines: ParsedLine[] }
export interface ParsedCustomer { gid: string; displayName: string; clientKey: string | null; tags: string[]; createdAt: string; updatedAt: string; phones: Array<{ e164: string; field: 'default' | 'address' }> }
export function parseOrders(jsonl: Iterable<string>): { orders: ParsedOrder[]; orphans: string[] };
export function parseCustomers(jsonl: Iterable<string>): ParsedCustomer[];
```
`runBulk` polls `bulkOperation(id:)` by id (never `currentBulkOperation`), requests ungrouped JSONL, never returns or logs the URL, accepts only hosts ending `.shopifycdn.com` or equal to `storage.googleapis.com`, and hashes the stream with sha256.
- [ ] **Step 1: Failing tests:** children before their parent, and in any order, still join by `__parentId`; an orphan child is reported in `orphans`, never dropped silently; `"845.0"`, `"61.75"`, `"0.00"` become 84500, 6175, 0 agorot; a line without a SKU keeps `sku: null`; a cancelled order with `currentQuantity: 0` lines keeps its full `discountedAgorot`, and `linesAgorot` is the sum of the lines; `refundCount` comes from the refunds list; phones are normalised to E.164 with the same plausibility rule as `normalize_phone_il` (a golden list of 10 synthetic numbers shared with Task 7's test through a JSON fixture); a bulk operation in `FAILED`, `EXPIRED` or "already in progress" throws a coded error; a URL on a foreign host is refused; the returned object contains no URL.
- [ ] **Steps 2–4:** red, implement, green, commit.

### Task 13: Eligibility, staging, run orchestration, refresh, route, manual promotion, chain-map check

**Files:** `api/src/sales/mirror/eligibility.ts`, `stage.ts`, `run.ts`, `refresh.ts`, `chain.ts`, `promote_customer.ts`, `__tests__/*.test.ts`; `api/src/internal/jobs/sales_shopify_mirror_route.ts` (registered in `api/src/server.ts`, using `lead_wake_route.ts` as the template).

**Interfaces — produces:**
```ts
export type B1Result = 'verified' | 'review_tagged' | 'review_active_no_key' | 'manual';
export function classifyCustomers(orders: ParsedOrder[], customers: ParsedCustomer[], now: Date): {
  staged: Array<{ customer: ParsedCustomer; b1: B1Result; cleanOrders: number; lastCleanOrderAt: string | null }>;
  excluded: { count: number; byLastOrderYear: Record<string, number> };
  ordersExcludedCustomers: number; draftsExcludedCustomers: number; ordersNoCustomer: number };
export async function stageRun(db: Db, runId: string, data: { staged: Array<…>; orders: ParsedOrder[]; counts: Record<string, unknown>; sha256: string; apiVersion: string }): Promise<void>;
export async function runMirror(deps: MirrorDeps, req: { mode: 'dry_run' | 'refresh' | 'reconcile' | 'promote_customer'; customerGid?: string }): Promise<{ runId: string }>;
// POST /api/v1/internal/jobs/sales-shopify-mirror  { mode, customer_gid? }  → 202 { ok: true, run_id }   (bearer JOB_RUNNER_TOKEN; 503 when unset; 401 on mismatch; 409 while a run is active; 400 for any other mode)
```
B1 in Node (T1): tag in {`needs-verification`, `whatsapp-bot-test`} → `review_tagged`; else a clean order and a `client_key` non-blank after trim → `verified`; else an active customer (clean order in 12 months, Asia/Jerusalem) without `client_key` → `review_active_no_key`; else excluded (counted by last-order year, never staged). Orders are staged only for staged customers; every Shopify order and draft is accounted for in `counts` (`orders_total`, `drafts_total`, `orders_no_customer`, `orders_excluded_customers`, `drafts_excluded_customers`, `oldest_order_at`).

**Modes.** `dry_run`: `mirror_start_run('backfill', T)` with `T` = 00:00 Asia/Jerusalem of the day; bulk pull of orders (created before `T`) and of customers who ever ordered; classify; stage; `mirror_finish_run('staged')`; then `select sales_core.mirror_promote(run, false)` (the report lands in `mirror_run.report`). `refresh` (the daily composite, one lease): orders by `updated_at` from the watermark minus 10 minutes; open drafts as a set; the customer sweep (nightly: customers who ever ordered, re-evaluating B1; a customer with a non-blank `client_key` who is not in the mirror gets their own orders fetched through `customer.orders` and classified, capped at 50 per run, over the cap → a `mirror_exception`); on Sundays the anti-join of order GIDs (`deleted_at` on a vanished GID; an org whose customer no longer resolves → row 7 of the transition table); the chain-map check (below); then `mirror_promote_refresh`; then reconcile (Task 14) as a separate `kind = 'reconcile'` row. A refresh **refuses with a coded error until a backfill run is `applied`**. `reconcile`: Task 14 only. `promote_customer`: fetches one customer by GID and their orders live, stages them with `b1 = 'manual'`, calls `mirror_promote_one`; it is reachable only from the manager mutation (Task 16), never from the cron entry.

**The job never applies a backfill:** the module's only SQL calls are `mirror_start_run`, `mirror_heartbeat`, `mirror_finish_run`, the stage inserts, `mirror_promote(…, false)`, `mirror_promote_refresh`, `mirror_promote_one`, and the reconcile functions (a test greps the module for `mirror_promote(` and asserts every call passes `false`).

**Chain-map check (`chain.ts`).** `checkChainMap(deps)` fetches `https://api.github.com/repos/tomw200082-collab/gt-factory-os-production-brain/contents/docs/sales/chain_map.json` (override: `SALES_CHAIN_MAP_URL`) and compares the returned blob `sha` with `chain.source_sha`; a difference writes one `mirror_exception` (`chain_map_changed`); a fetch failure is a logged warning, never a run failure (the check is advisory and the file is public).

- [ ] **Step 1: Failing tests:** `classifyCustomers` over a shared JSON truth table `api/src/sales/mirror/fixtures/b1_cases.json` (the same cases are read by a pgTAP helper in Task 8 so the two implementations are held to one table): clean order and `' ck '` → `verified`; blank-after-trim key → not verified; only cancelled, only test, only draft → excluded or review as the table says; refunded-only → `verified`; ₪0 completed → `verified`; tag + key + clean → `review_tagged`; active without key → `review_active_no_key`; dormant without key → excluded; excluded customers' names and phones never reach `stageRun` (spy on the db); `counts` accounts for every order (`orders_total = staged orders + orders_no_customer + orders_excluded_customers`); `runMirror('dry_run')` heartbeats, ends `staged`, and records the sha256, the API version and counts; a failure sets `status = 'failed'` with a code and GIDs only; a second concurrent call gets 409; `refresh` refuses before an applied backfill; the route rejects `mode: 'apply'`, `'rollback'` and anything else with 400; the route answers within one second when the run takes longer (fake timers); `checkChainMap` writes one exception on a different sha, none on an equal one, and does not throw on a fetch error; the customer sweep fetches orders only for newly keyed customers and stops at 50; every `mirror_promote(` call in the module passes `false`.
- [ ] **Steps 2–4:** red, implement, green; the root vitest step now runs these (`npx vitest run api/src/sales/mirror`); commit.

### Task 14: Reconciliation

**Files:** `api/src/sales/mirror/reconcile.ts`, `shopifyql.ts`, `__tests__/reconcile.test.ts`; SQL `sales_core.mirror_reconcile_input() returns jsonb` and `sales_core.mirror_record_reconcile(p_parent uuid, p_result jsonb) returns uuid` in an additional M1-numbered migration file in this PR (`<next>_sales_mirror_reconcile.sql`), applied to production by the workflow that precedes PR-3's merge.

**Interfaces — produces:**
```ts
export async function censusByCustomer(ql: ShopifyQl, sinceIso: string, untilIso: string): Promise<Map<string, { orders: number; totalSales: number }>>;   // FROM sales SHOW orders, total_sales GROUP BY customer_id
export function chooseSample(input: { customers: SampleCustomer[]; seedHex: string }): string[];   // every org with a refunded/test/cancelled/edited/draft order + top 10 by revenue + 20 seeded-random
export function compareSets(mirror: Array<{ gid: string; cls: string; agorot: number }>, live: Array<{ gid: string; cls: string; agorot: number }>): { equal: boolean; onlyMirror: string[]; onlyLive: string[]; differ: string[] };
export async function reconcile(deps: ReconcileDeps): Promise<{ status: 'pass' | 'fail'; census: unknown; sample: unknown; gates: { gate1: unknown; gate2: unknown }; inFlight: number; coverage: { verifiedActive: number; censusActive: number; source: 'shopifyql'; asOf: string } }>;
```
Rules: non-test order count per customer equals exactly; the revenue residual is attributed per order (edit, order-level discount, refund, shipping) and any unexplained residual fails; recipe gate 1 (≤ 0.5% over the window) and gate 2 (exact monthly counts including cancelled, Asia/Jerusalem); the live sample is read to the end and restricted to `created_at < T`, compared as **sets** of `(gid, class, agorot)` with tolerance 0; orders with `updatedAt` after the watermark are in flight and excluded, more than 1% in flight fails; seed = the first 8 hex digits of the apply digest; a throttled live read fails the run. `coverage` (T8) is stored in the reconcile row's `counts` and surfaced to managers.
- [ ] **Step 1: Failing tests:** a mirror that classifies a cancelled order as completed fails on the census even when the live side uses the same function (the census does not depend on `order_class`); `compareSets` flags an off-by-0.01 total, an only-mirror GID and an only-live GID; the sample always includes the refunded and test orgs of a synthetic population and is stable for a fixed seed; an in-flight order is excluded and reported, and 2 of 100 in flight fails; a throttled live read fails the run, never counts as zero; a pass writes a `kind = 'reconcile'`, `status = 'pass'` row and flips `history_published()`; a fail writes `fail` and a `reconcile_failed` exception.
- [ ] **Steps 2–4:** red, implement, green, commit.

### Task 15: CI end-to-end over recorded fixtures, then ship PR-3

**Files:** `.github/workflows/sales-db.yml`, `api/src/sales/mirror/__tests__/e2e.db.test.ts` (runs only when `DATABASE_URL` points at localhost, like `lead_db.test.ts`), `api/src/sales/mirror/fixtures/*`.

- [ ] **Step 1:** the e2e loads the synthetic fixture set through `stageRun`, calls `mirror_promote(run, false)` twice (identical digests), then `true` (counts equal the report), then once more on a fresh stage (no change: table hashes equal); simulates a crash after the first half of the stage (the next `mirror_start_run` after a 16-minute-old heartbeat resumes); `apply` with a stale digest is refused; the rollback test calls `mirror_rollback` and compares hashes of the non-append-only tables with the pre-apply state; the hash of every table outside `sales_core` is unchanged. Required fixture cases: completed; ₪0 line; cancelled with a refund record; refunded in full and in part; edited; order-level discount; line without SKU; no lines; the test order; `taxesIncluded=false`; presentment currency; no customer; customer reassigned; created before `T` and updated after; the 2026-04 mass cancel (a block of 40 cancelled orders); drafts open, invoice-sent, completed and older than a year; customers with no `client_key`, with `needs-verification`, with only cancelled orders, with only drafts; orphan and out-of-order JSONL children; a throttled response; a failed bulk operation.
- [ ] **Step 2:** CI green, with the e2e step visible in the log; the fixture scrub test green.
- [ ] **Step 3 (ship):** draft PR, `unsubscribe_pr_activity`, throwaway red proof on one e2e assertion, revert, merge, reset the branch. The job code deploys to Railway with the merge (its schema dependency, M1 plus the reconcile functions, is already applied). Verify `/health` and that `POST /api/v1/internal/jobs/sales-shopify-mirror` answers 401 without the bearer (a read-only `curl`).

**Evidence:** CI run URLs (green; red proof), the 401 check, N/N counts.

---

## PR-4 — Read API, cutover migration, cron entry (backend)

PR-4 stays **open (ready, unmerged)** until W6 step 5 has applied M2 from its branch; the new routes read only M1 objects, so they do not depend on M2, but the M2 and M3 files ride in this PR and are applied from its head, as the spec orders (§3.13). It merges right after M2 is applied and verified.

### Task 16: Org read routes, mutations, scope and shaping

**Files:** `api/src/sales/orgs_handler.ts`, `orgs_routes.ts`, `api/test/sales_orgs.test.ts` (role matrix, `tsx --test`), `api/src/sales/queries_handler.ts` (the `/tasks` select gains `and t.source_kind <> 'identity_review'`), `api/src/sales/route.ts` (registers `orgs_routes`).

Handlers follow `queries_handler.ts`: `requireSalesAccess(session)`, `session.role === 'sales_rep'` scoping, `AuthError('Not authorised', 403)`, `sql` from Kysely, `ok(body)`; a manager is `planner` or `admin` (a new `requireSalesManager`); ids go through `parseId`; every route reads M1 objects only.

**Interfaces — produces (all under `/api/v1/queries/sales` unless noted):**
```
GET  /orgs/:id                -> { header, chain, moved: {to, on} | null, link_status, counts, active, coverage_line (managers), history_status: 'ok'|'unverified'|'stale', as_of }
GET  /orgs/:id/orders?cursor= -> { rows: [{gid, name, created_at, class, ex_vat_agorot | null, line_count}], next }
GET  /orgs/:id/orders/:gid    -> lines + provenance (source: Shopify, observed_at)
GET  /orgs/:id/river?cursor=&chip=   -> merged stream (orders, org events, lead events the session can read); internal notifications hidden
GET  /orgs/:id/contacts       -> { verified: [...], review: [...] }       -- unverified rows carry no link fields
GET  /orgs/:id/circle         -> { months: [{ym, completed, refunded, cancelled, drafts}], last_order_at, as_of }
GET  /orgs/page?filter=&sort=&cursor=&limit=   -> { rows, next }          -- v_sales_org_list; filter: active | prospect | all | review (managers); sort: last_order | ex_vat_12m | name; pages of 50
GET  /orgs/search?q=          -> [{id, name, phone}]                      -- lean index for the command palette
GET  /identity-review         -> managers: { orgs: [...with candidates, order count and last order labelled as candidate evidence], exceptions: [...unresolved mirror_exception], coverage }
POST /api/v1/mutations/sales/orgs/owner            managers: { org_ids: string[], owner_email }
POST /api/v1/mutations/sales/orgs/:id/identity     managers: { action: 'confirm'|'pick'|'reject', customer_gid? }
POST /api/v1/mutations/sales/orgs/promote-customer managers: { customer_gid }   -> 202 { run_id } (calls runMirror('promote_customer'))
POST /api/v1/mutations/sales/contacts/:id/(verify|reject|promote|redact)   managers
```
The legacy `GET /orgs` stays (shaped by M2) until the portal switches to `/orgs/page` in Task 24; Task 24 removes it with its test.

- [ ] **Step 1: Failing tests (role matrix, one assertion per cell):** rep A gets 403 with an empty body on rep B's org for `detail`, `orders`, `orders/:gid`, `river`, `contacts`, `circle`; a rep reads an org behind own leads and an org with `owner_email`; the river for a rep on a shared org carries no events of another rep's leads; a manager succeeds on every route; `identity-review`, owner, identity, promote-customer and every contact mutation return 403 for a rep; a `review`, `disputed` or `retired` org returns its own leads and lead events and **no** orders, money, circle, chain or Shopify contacts, and a rep gets only a status code (no candidates); `history_status` is `unverified` when the latest reconcile failed or none exists, `stale` when older than 36 hours, `ok` otherwise, and money is null unless `ok`; `/tasks` and Today never return `source_kind = 'identity_review'` tasks; `POST /mutations/sales/tasks/:id/complete` on an identity task returns an error and changes nothing; every success on contacts, orders and river writes one `access_log` row; ids are validated (`parseId`) and a malformed id returns 400; an unverified contact has no `tel`, `wa` or `mailto` field; `owner` assigns in one transaction and writes `owner_assigned`; `identity` `confirm` links, `pick` merges, `reject` retires the link, and each writes its event and cancels its task in one transaction; `/orgs/page` returns 50 rows and a cursor, honours `filter` and `sort`, and applies a rep's scope; the circle counts months in Asia/Jerusalem (a fixture order at 23:30 UTC on 30 June lands in July).
- [ ] **Steps 2–4:** red (`cd api && env -i PATH="$PATH" HOME="$HOME" DATABASE_URL=postgresql://postgres@127.0.0.1:55432/gt_test npx tsx --test --test-concurrency=1 test/sales_orgs.test.ts`), implement, green, commit.

### Task 17: M2 cutover migration (written and tested here, applied only at W6 step 5)

**Files:** `db/migrations/<N+7>_sales_identity_cutover.sql`, `db/tests/<N+7>_sales_identity_cutover.test.sql`; deliberate test edits in the files listed under "Carve-outs".

**Contents:**
1. `create or replace function sales_core.org_link_trusted(...)` redefined as `select sales_core.org_link_is_verified(p_customer_id, p_status)` (this flips the radar batch, the conversion select and the alert flag of Task 20 to verified-only).
2. The guard trigger:
```sql
create or replace function sales_core.org_link_guard() returns trigger language plpgsql as $$
begin
  if coalesce(current_setting('sales.link_writer', true), '') <> 'on' then
    if tg_op = 'INSERT' and (new.shopify_customer_id is not null or new.shopify_link_status is not null) then
      raise exception 'SALES_LINK_GUARD: org insert with a link; use sales_core.link_org_shopify';
    elsif tg_op = 'UPDATE' and (new.shopify_customer_id is distinct from old.shopify_customer_id
                             or new.shopify_link_status is distinct from old.shopify_link_status) then
      raise exception 'SALES_LINK_GUARD: link columns change only through sales_core.link_org_shopify';
    end if;
  end if;
  return new;
end $$;
create trigger org_link_guard before insert or update on sales_core.org for each row execute function sales_core.org_link_guard();
```
3. `ingest_lead` rewritten from the `0361` text: the three places that write `shopify_customer_id` (the new-org insert and the two `update … set shopify_customer_id = coalesce(…)`) stop writing it; when `p_shopify_customer_id` is given the function calls `record_org_identity_evidence(org, p_shopify_customer_id, 'lead', 'shopify_id', p_shopify_customer_id, null, null, null)`; the `matched_existing_customer` lead event is emitted only when `org_link_is_verified(org.shopify_customer_id, org.shopify_link_status)` holds at that moment. Signature, return table and every other behaviour are unchanged.
4. `convert_lead(uuid, text, numeric, text, text, text, timestamptz)` (same signature as `0348`): for `p_evidence_kind = 'shopify_order'` it raises `SALES_CONVERT_UNVERIFIED` unless the lead's org satisfies `org_link_is_verified`; `green_invoice` evidence is unchanged.
5. `create or replace view` (every existing column kept in its position; new columns appended) for `api_read.v_sales_orgs`, `v_sales_leads`, `v_sales_today`, `v_sales_attention`, `v_sales_backlog_triage` and `v_sales_sleeping_radar_latest`: `is_existing_customer` and the `returning_customer` branch become `sales_core.org_link_is_verified(o.shopify_customer_id, o.shopify_link_status)` (the old `or o.shopify_snapshot_at is not null` disappears); `shopify_snapshot` is `null::jsonb`; `v_sales_orgs` appends `shopify_link_status, is_active_customer, last_order_at, orders_12m, ex_vat_12m_agorot, chain_name, owner_email, has_open_lead` from `api_read.v_sales_org_list`; `v_sales_sleeping_radar_latest` joins `sales_core.org` and returns only rows whose org passes `org_link_is_verified`.
6. `sales_core.radar_org_batch` needs no change (it reads `org_link_trusted`).

- [ ] **Step 1: Failing tests (`plan` equals the assertions listed):** for an org in `review`, `disputed` and `retired`: `v_sales_orgs`, `v_sales_today`, `v_sales_leads`, `v_sales_attention`, `v_sales_backlog_triage` return `is_existing_customer = false`, no `returning_customer` item, null mirror columns and null `shopify_snapshot`; for `verified` with `history_published()` false the money columns are null and the flag is true; `org_link_trusted('gid://shopify/Customer/1', null)` is now false (the M1 permissive case, asserted here only); every old column of the six views still exists at the same ordinal position (compare `information_schema.columns` against a pinned list captured from the pre-M2 definitions); a build-failing test lists any view column in `api_read` whose definition mentions `shopify_order`, `v_shopify_order` or `v_sales_org_list` without `org_link_is_verified` (read from `pg_views`); the guard rejects a direct `update … set shopify_customer_id`, a direct `insert` with an id, and a direct status change, and accepts `link_org_shopify`; `ingest_lead` with a Shopify id creates the lead, attaches an existing org by that id, writes one evidence row and never sets the id on a new org, and emits `matched_existing_customer` only for a verified org; `convert_lead(…'shopify_order')` raises for a `review` org and succeeds for a `verified` one; `convert_lead(…'green_invoice')` is unaffected; `radar_org_batch` excludes `review`, `disputed`, `retired` and null-status orgs.
- [ ] **Step 2: Carve-outs.** Run the whole local baseline after M2 applies. Every previously passing `db/tests/03*` file must still pass, except files whose assertions describe the **old derivation** (expected: `0323`, `0341`, and the `matched_existing_customer` and link-write assertions of `0321`, `0332`, `0345`, `0361`; `0346` and `0330` are already pinned failures). For each, change only the assertions about the old meaning and the fixture inserts that set an id directly (add `set local sales.link_writer = 'on';` before the insert and `shopify_link_status` to the column list, so the fixture simulates the one writer), and list every changed assertion (old meaning → new meaning, gate 4 / T2 / T3) in the PR description and in the final report. A changed assertion that is not about the old derivation is a defect.
- [ ] **Steps 3–4:** red, implement, green, baseline, commit.

### Task 18: M3 — the refresh cron entry (written here, applied only at W6 step 6)

**Files:** `db/migrations/<N+8>_sales_mirror_cron.sql`, `db/tests/<N+8>_sales_mirror_cron.test.sql`.

- [ ] **Step 1: Failing test (`plan(5)`):** after the migration, `cron.job` has one row named `sales_shopify_mirror_refresh`; its schedule is `40 0 * * *`; its command contains `/api/v1/internal/jobs/sales-shopify-mirror`, `factory_os_job_runner_token` and `'{"mode":"refresh"}'`; its command contains no literal bearer value (`!~ 'Bearer [A-Za-z0-9._-]{20,}'`); a second run of the file leaves one row.
- [ ] **Step 2: Implement** exactly in the `0330_lionwheel_poll_railway_cron.sql` pattern: `begin; select cron.unschedule('sales_shopify_mirror_refresh') where exists (select 1 from cron.job where jobname = 'sales_shopify_mirror_refresh'); select cron.schedule('sales_shopify_mirror_refresh', '40 0 * * *', $job$ select net.http_post(url := 'https://gt-factory-os-api-production.up.railway.app/api/v1/internal/jobs/sales-shopify-mirror', headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name = 'factory_os_job_runner_token')), body := '{"mode":"refresh"}'::jsonb, timeout_milliseconds := 30000); $job$); commit;`, with a header comment naming the clear slots (`30 1` radar, `0 4` leads job, `17 4` ShopifyQL, `*/5` reconciler, `*/15` shop sync) and the rollback line `select cron.unschedule('sales_shopify_mirror_refresh');`.
- [ ] **Step 3:** green; commit.

### Task 19: PR-4 checks (merge only at W6 step 5)

- [ ] Draft PR, `unsubscribe_pr_activity`; `sales-db` green (the role matrix and cutover tests run in CI); a throwaway red proof on one role-matrix assertion, reverted; mark ready and **leave unmerged**. Evidence: run URLs.

---

## PR-5 — Edge functions, link writers and skill (backend)

### Task 20: Readers through the SQL predicates, evidence-only writers, radar bearer check

**Files:** `supabase/functions/sales-leads-poll/index.ts`, `supabase/functions/sales-leads-poll/_lib/lookup.ts` (new, pure), `supabase/functions/sales-sleeping-radar/index.ts`, `supabase/functions/sales-sleeping-radar/_lib/auth.ts` (new, pure), `.github/workflows/deploy-edge-function.yml`, `.claude/skills/customer-setup-shopify-gi/SKILL.md`, tests `api/test/sales_leads_poll_lookup.test.ts`, `api/test/sales_radar_auth.test.ts`, `api/test/sales_link_writers.test.ts`.

- [ ] **Step 1: Failing tests (`tsx --test`):**
  - `pickSingleCustomer(edges)` returns `null` for two or more customers, the single customer for one, and `null` for none (the lookup no longer takes `edges[0]`).
  - `isServiceRoleBearer(authHeader)` decodes the JWT payload (no signature check: the platform's `verify_jwt` has already verified it) and returns true only for `role === 'service_role'`; false for `anon`, a malformed token and a missing header.
  - `sales_link_writers.test.ts` (repo-level "sole writer" guard): scans `api/src`, `supabase/functions` and `.claude/skills` and fails on any assignment of `shopify_customer_id` to `sales_core.org` (a case-insensitive pattern over statements that mention `sales_core.org`), with an allow-list that is empty.
- [ ] **Step 2: Implement.**
  - **leads-poll:** `lookupShopifyCustomer` uses `pickSingleCustomer`; the daily backfill calls `sales_core.record_org_identity_evidence(org, gid, 'lead', 'shopify_id', gid, null, null, null)` instead of `update sales_core.org set shopify_customer_id, shopify_snapshot, shopify_snapshot_at`, and selects only orgs with no evidence row in the last 30 days (`not exists (select 1 from sales_core.org_identity_evidence e where e.org_id = l.org_id and e.created_at > now() - interval '30 days')`), so it stops re-checking the same 150; it no longer writes `matched_existing_customer`. The conversion select replaces `o.shopify_customer_id is not null` by `sales_core.org_link_trusted(o.shopify_customer_id, o.shopify_link_status)`. The new-lead alert's `is_known_customer` becomes `sales_core.org_link_trusted(o.shopify_customer_id, o.shopify_link_status)`, selected as a boolean column.
  - **radar:** the inline select becomes `select id, shopify_customer_id from sales_core.radar_org_batch($1)`; `routeRun` returns `orgs_truncated: true` when the result length equals the limit; the `run` route first checks `isServiceRoleBearer(req.headers.get('authorization'))` and answers 401 otherwise (`health` stays open, as today).
  - **deploy list:** add `sales-sleeping-radar` to the `options` of `deploy-edge-function.yml`.
  - **skill:** replace §5's `update sales_core.org set shopify_customer_id = …` block with `select sales_core.record_org_identity_evidence('<org_id>'::uuid, '<gid>', 'customer_setup', 'shopify_id', '<gid>', null, null, null);` and one sentence saying the identity layer decides the link at the next run.
- [ ] **Step 3: Green; run `npx tsx --test` over the three new files and the existing `sales_leads_poll_*` tests; commit.**

### Task 21: Ship PR-5 and deploy the edge functions

- [ ] Draft PR, `unsubscribe_pr_activity`, `sales-db` green, throwaway red proof (one `pickSingleCustomer` assertion), merge, reset the branch.
- [ ] **Production (after M1, before the apply):** announce one line; dispatch `deploy-edge-function` for `sales-leads-poll` and `sales-sleeping-radar` from `main`; read the deployed version in each run log; a read-only check that the next scheduled runs write no `errors` (`sales_core.sleeping_radar_run` rows for the next run id; `lead_event` unaffected); a `POST {"route":"run"}` to the radar with the anon key returns 401 (from SQL via `net.http_post` with the anon key from the project settings, never printed).

---

## Mockups and string round 1 (parallel from PR-2 onward; Tom's gate for the portal)

### Task 22: Mockups at 390 and 1280 with synthetic data

**Files (local, not committed to the portal until approved):** standalone HTML under the scratchpad using the real `--s-*` tokens from `sales-tokens.css`; screenshots rendered with the installed Chromium (`/opt/pw-browsers`) at 390 and 1280, light and dark and reduced motion; published to Tom as a private Artifact for phone viewing.

- [ ] **Cases:** 0, 1, 8, 28 and 216 orders; a distributor gap and a branch moved to a distributor; an org in review; a disputed org; an org with no lead; a long Hebrew name (64 characters) and long product titles; the list at 3,000 rows' worth of density; the manager identity-review screen. Every name is synthetic.
- [ ] **Output:** the first-viewport order (header, next action, primary contact with call and WhatsApp, summary, ring), the two-year ring with its month sheet, the merged river with chips, the contacts list with its review area, the gate-4 states, the stale and unverified banners.

### Task 23: String batch round 1

- [ ] Group by category (list chips, badges and empty states; header and summary with the VAT basis and the coverage caveat; ring; river and the `org_event` types; order classes and filters; provenance sheet; contacts; gate-4 states; identity review; owner assignment), each with where it appears and the English meaning; send with the mockups; **stop for Tom's approval** (C and D1 of the checkpoint). Later rounds hold only UX-gate fixes.

---

## PR-6 — Portal (starts only after Tom approves Tasks 22–23)

Each tranche: create the manifest under `docs/portal-os/tranches/`, register it in `docs/portal-os/registry.md`, set `_active.txt`, then edit only listed files. After each: `npx tsc --noEmit`, `npx vitest run`, mocked e2e at 320/390/430/1280, light, dark, reduced motion, long-fixture overflow check.

### Task 24: Tranche 189 — org route, API proxies, list scale, search index

**Files:** `src/app/(sales)/sales/orgs/[id]/page.tsx`, `src/app/(sales)/sales/orgs/page.tsx`, `_components/OrgList.tsx`, `_lib/api.ts`, `_lib/types.ts`, one-file proxies `src/app/api/sales/orgs/**`, `SalesShell.tsx` (the command palette uses `/orgs/search`), tests.

- [ ] Tests first: the list requests `/orgs/page` with `filter`, `sort`, `cursor`, `limit=50` and renders a "show more" button; a filter-aware empty state ("no matches" differs from "no businesses yet"); the palette loads the lean index once; `orgs.test.tsx` is replaced (the assertion on the snapshot word "נטש" is removed: the explicit D8 carve-out); a 403 renders its own state; the legacy `/orgs` call and its backend test are removed in the paired backend commit.
- [ ] Implement; register copy keys with the approved strings only.

### Task 25: Tranche 190 — header, summary, next action, contacts list, order history and river

**Files:** `_components/org/OrgHeader.tsx`, `NextAction.tsx`, `OrgSummary.tsx`, `ContactsList.tsx`, `OrderRiver.tsx`, `SourceSheet.tsx`, `_lib/format.ts` (ex-VAT formatter, one Asia/Jerusalem calendar-day helper), `_lib/labels.ts` (approved strings), tests including the event-label completeness test.

- [ ] Tests first: ex-VAT label on every money value; a banner when `history_status` is `unverified` or `stale`; an unverified contact renders no `tel:`, `wa.me` or `mailto:` link; every node and number opens `SourceSheet` with source and time; text ≥ 12 px measured by glyph box for SVG; a 64-character name, ten contacts and twelve unverified rows, 300 river items without overflow; a test that fails on any `org_event` or river type without a label.
- [ ] Implement.

### Task 26: Tranche 191 — the two-year ring and the manager identity-review screen

**Files:** `_components/org/Ring.tsx`, `IdentityReview.tsx`, `BulkOwner.tsx`, tests.

- [ ] Tests first: month segments are the tap targets (≥ 44 px at 390 px, a 6×4 grid below 360 px); a tap opens the month sheet; the centre shows the last order and "as of" and, for a moved-to-distributor chain, the moved text and no silence count; reduced motion leaves no running animation (`getAnimations().length === 0`); the review screen shows candidates side by side with confirm, pick and reject, the unresolved exceptions and the coverage line; bulk owner assignment needs no date.
- [ ] Implement with the `taste-skill`, `frontend-design`, `ui-ux-pro-max` and `impeccable` skills; no animation library.

### Task 27: UX gate and portal PRs

- [ ] `/ux-release-gate` in the sales profile (both roles through `gt.fakeauth.v1`; 320/390/430/1280; light, dark by user preference, reduced motion; long fixtures; viewport shots) against the rendered app; fix every real P0 and P1 and re-gate; the report goes to brain `docs/phase8/dry-runs/`. Open each tranche's PR as a draft, `unsubscribe_pr_activity`, `portal-pr-guard` green, merge after PR-4 (the proxies need its routes).

---

## Review and simplification

### Task 28: Independent review, then simplify

- [ ] `requesting-code-review` (an independent reviewer subagent per repo) on the final backend and portal diffs, `code-review` at level `high` on each PR, `receiving-code-review` to triage; fix every Critical and Important finding; then `simplify` and `ponytail-review` (delete, merge duplicates; never weaken validation, security, accessibility, error handling or an approved requirement); re-run every affected test; run a fresh red-team pass over the final design only if the review finds a structural issue.

---

## W6 — Ship

### Task 29: Production rollout

- [ ] **Step 1 (pre-flight):** announce one line; `rebuild_verifier() = 0`; M1 is applied and PR-2, PR-3, PR-5 are merged; the read-only Shopify token with `read_orders`, `read_all_orders`, `read_customers`, `read_draft_orders` is in Railway as `SALES_MIRROR_SHOPIFY_TOKEN` (otherwise the fallback token is used and the run records it); the Railway deployment for the merge SHA is verified by inspecting its commit field (if the response carries none, D11 is reported unmet, never claimed); the edge functions are deployed (Task 21).
- [ ] **Step 2 (dry-run):** trigger the job from the database (`select net.http_post(…)` with the vault token resolved inside SQL, so the session never reads it); poll `mirror_run` until `staged`; read `mirror_run.report`; check that `order_coverage.difference = 0` and that the total equals Shopify's all-time order total (13,652 measured on 2026-10-01); check the oldest mirrored order against `oldest_order_at` (a missing `read_all_orders` scope would cut history).
- [ ] **Step 3 (Tom's go):** give Tom the exact counts and the digest in Hebrew, with `excluded_no_client_key_by_year`, `today_card_changes` in both directions, the chain memberships and conflicts, the customers verified only by ₪0 orders, the contacts to add and the disputed and review orgs. **Stop** until he gives a count-specific go (D10).
- [ ] **Step 4 (apply):** `select sales_core.mirror_promote(<run>, true, <count>, '<digest>', 'tom-approved')` through the Supabase connector in one statement; record the `mirror_run` row; `rebuild_verifier() = 0`; trigger `{"mode":"reconcile"}` straight after and require `pass`.
- [ ] **Step 5 (cutover):** announce; apply M2 through `deploy-production.yml` from the PR-4 head (`confirm=APPLY`, exact glob, `skip_deploy=true`); verify the views (no `review` or `disputed` org shows money or a customer flag), that the Today change counts equal the dry-run's, `rebuild_verifier() = 0`, and that `radar_org_batch(500)` returns only verified orgs with a lead; merge PR-4 (Railway deploys the new routes); then merge the portal PRs.
- [ ] **Step 6 (schedule):** announce; apply M3 from the same head.
- [ ] **Step 7 (D11):** the Railway deployment and the Vercel deployment on the merge SHA, `/health`, a new route returns 401 without auth, the post-deploy reconcile output.
- [ ] **Evidence:** the dry-run report, Tom's quoted go, the apply `mirror_run` row, the reconcile result, the workflow run URLs, both `rebuild_verifier()` values around every production DDL and the apply.
- [ ] **Rollback:** before the apply, do not apply. After it: `select sales_core.mirror_rollback(<run>, 'tom')` (Task 8), which retires created orgs, unlinks linked ones, deletes mirror rows by run and cancels review tasks, and lists any merges for a manager; M2 rolls forward only (a new slot restoring the views).

### Task 30: Close

- [ ] D4b: report pending until three scheduled reconciles have passed; Rule R (radar and conversion read the mirror) is its own tranche after D4b, with a preview of the leads that would become `won`.
- [ ] `verification-before-completion` on the exact final heads of every repo after the last change; `CURRENT_STATE.md` gets a dated Unit B section with D1–D12; the masterprompt's status line becomes `SHIPPED`, `SUPERSEDED by <path>` or `ABANDONED — why`, with evidence pointers (D12); the final report to Tom in Hebrew with the eight PASS fields (files changed, tests N/N, contracts referenced, signals emitted, stop conditions tripped, Tom approvals required, rollback plan, next handoff) and the single next action.

---

## Interpretations (engineering readings of the spec; listed in the final report)

1. **Transition table (Task 8).** The spec says "a table of status × B1 result gives the action" without printing it; the table above is derived row by row from §3.6, T1, T3 and T4. A legacy link whose phone does not prove it stays `review` (T3: "an id the identity layer did not set starts as review until B4 re-derives it").
2. **`org_link_trusted` (Tasks 4, 9, 17, 20).** The radar, the conversion select and the new-lead alert keep today's behaviour until the apply and become verified-only at M2; one SQL predicate redefined by M2 flips all three atomically, so the edge functions deploy once.
3. **`mirror_exception` (Task 6).** The spec says a capped or stale refresh "raises an exception"; the sales module may not write `private_core`, so exceptions are a new B table shown on the manager identity-review screen.
4. **Paged list at `/orgs/page` (Task 16).** Keeps the legacy `/orgs` working until the portal switches; the legacy route is then removed.
5. **`promote` on a contact (Task 7).** Read as `org_channel` → `person` with a supplied name; verification stays separate. Tom's T1 "promote a customer by hand" is the separate `promote-customer` action (Tasks 13, 16).
6. **`matched_existing_customer` (Task 17).** Emitted only for a verified org, so the event stays truthful under T3; past events are unchanged.
7. **Test carve-outs (Task 17).** Assertions about the old derivation (`0323`, `0341`, and the link-write assertions of `0321`, `0332`, `0345`, `0361`) change deliberately; each is listed with old and new meaning.
8. **M1 applied from the PR branch before merge, M2 and M3 from the PR-4 head (Tasks 10, 29),** as §3.13 orders; PR-4 merges after M2 is applied.
9. **Customer sweep for newly keyed customers (Task 13)** is capped at 50 per run so a bulk `client_key` edit in Shopify cannot flood the identity step; over the cap it raises a `mirror_exception`.
10. **Rollback leaves merges in place (Task 8):** leads are never moved back silently, so a merged lead-born org stays retired and is listed for a manager.

## Self-review against the spec

- **Spec coverage.** §2.2 T1 → Tasks 8 (rows 6, 12), 13 (classification, counts); T2 → Tasks 6, 17 (shaping, gate 4); T3 → Tasks 4, 17, 20 (sole writer, evidence-only ingest, lookup, skill, guard); T4 → Task 8 (phone-only, multi-branch dispute); T5 → Tasks 16, 22, 23 (labels, no silence count for moved chains); T6 → Task 5 (all fields, SHA, branch-merge display only) and Tasks 8, 13 (rule hits to review in refresh, daily SHA check); T7 → harness; T8 → Task 14 (`coverage`), Task 16 (`coverage_line`); T9 → Tasks 6, 16, 26 (default filter, bulk owner); T10 → Tasks 7, 8 (contact inputs); T11 → Task 29 and Tom's list; T12 → redaction path (Task 7), access log (Tasks 7, 16). §3.2 → Tasks 3–7; §3.3 → Tasks 3, 6, 12; §3.4 → Tasks 11–13, 29 (job, lease, dry-run, apply, refresh, rollback); §3.5 → Tasks 14, 16, 17; §3.6 → Tasks 4, 8, 17, 20; §3.7 → Tasks 7, 8, 16; §3.8 → Tasks 6, 16, 17; §3.9 → Tasks 4, 6, 7, 11, 12, 16, 20 (radar bearer check, no raw values, scope); §3.10 → Tasks 22–27; §3.11 → Tasks 9, 17, 20 and Task 30 (R); §3.12 → Tasks 1, 2, 15 and each task's tests; §3.13 → Tasks 10, 21, 29.
- **Open for Tom, by design:** Task 23 (strings), Task 22 (visual approval), Task 29 step 3 (the go), his security actions, the read-only Shopify token, the Ice Dream fact.
- **Placeholder scan:** no "TBD", "later" or "similar to"; slot numbers are fixed at write time by the FR1/FR2 rule, which is a spec requirement, not a deferred decision.
- **Type consistency:** `order_class`, `link_org_shopify`, `unlink_org_shopify`, `org_link_is_verified`, `org_link_trusted`, `mirror_promote`, `mirror_promote_refresh`, `mirror_promote_one`, `mirror_rollback`, `mirror_start_run`, `ParsedOrder`, `ParsedCustomer` and `B1Result` are defined once above and used with the same names and arities in later tasks.
