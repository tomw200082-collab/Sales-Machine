# MASTERPROMPT — GT Pulse Unit B: one verified business, its people and its full order history, live in production

**STATUS: LIVE — not yet executed** · canonical copy: `Sales-Machine` `docs/plans/2026-10-01-gt-pulse-b-masterprompt.md` (branch `status/gt-pulse-a-2026-09-30`, then `main` after W0.1)
The executing session's last act is to change this line in that repo file (not in the pasted copy), commit it, to `SHIPPED`, `SUPERSEDED by <path>`, or `ABANDONED — why`, with evidence pointers (D12).

> **Usage:** paste this entire file as the first message of a fresh Claude Code session. Attach these repos: `gt-factory-os`, `gt-factory-os-portal`, `gt-factory-os-production-brain`, `Sales-Machine`, and `gt-site` (gt-site only provides the `taste-skill` files).
>
> It takes GT Pulse from where it is now to where Unit B leaves it.
> - **Now:** the CRM knows leads, and is blind to customers. 17 of 245 orgs are linked to Shopify. No order history is stored anywhere.
> - **After:** every verified B2B customer is one org, with verified contacts and a full, reconciled order history. The org screen carries the business circle, the event river and the contact compass. All of it is live in production.
>
> It halts for Tom only at the points listed in §6.
>
> **Provenance:** written 2026-10-01 by the session that shipped GT Pulse Unit A and D1. It was measured on 2026-10-01 between 13:30 and 14:30 UTC with:
> - read-only production SQL (Supabase project `rvadsozabmxkkrktwgnv`);
> - `git` on each repo's `origin/main` and the branches named below;
> - GitHub open-PR listings;
> - three read-only code surveys.
>
> **Authority, in order:**
> 1. `gt-factory-os-production-brain/CLAUDE.md`
> 2. `EXECUTION_POLICY.md`
> 3. `Sales-Machine/CLAUDE.md`
> 4. the GT Pulse program spec (§2.1)
> 5. `Sales-Machine/CURRENT_STATE.md`
>
> They are cited below, never copied. Where this document disagrees with one of them, the authority wins and this document is wrong.
>
> **Shelf life:** treat §2 as wrong if this is pasted after 2026-10-15. Run §2.5 first. If reality no longer matches §2, adapt and record what changed in your first message to Tom. Halt only if a §8 condition trips.

## 0. How to work

- **Who you are:** one Claude Code session that owns Unit B end to end, through production, with Tom available in chat.
  - You hold the repos above.
  - You hold the Supabase MCP for project `rvadsozabmxkkrktwgnv`. Use read-only SQL; DDL goes only through the deploy workflow.
  - You hold the Vercel and GitHub MCPs and the Shopify Admin read path the backend already uses.
  - **You may decide alone:** engineering choices inside the approved spec.
  - **Tom decides:** product scope, identity rules, Hebrew copy, anything customer-facing, and the production backfill.
- **Read first, in order:**
  1. `gt-factory-os-production-brain/CLAUDE.md` (Boot, Authorization, Watching, Stop conditions).
  2. `gt-factory-os/CLAUDE.md` (Stock truth, Migrations, Checks).
  3. `gt-factory-os-portal/CLAUDE.md`: UI language table (the sales route group is Hebrew-first), Invariants, tranche hook.
  4. `Sales-Machine/CLAUDE.md` (two kinds of truth, the 7 rules, Hard boundaries).
  5. The program spec: `Sales-Machine` branch `design/gt-pulse-crm`, `docs/superpowers/specs/2026-09-29-gt-pulse-crm-program-design.md`. Read §4 (units), §5 (ownership and tasks), §7 (orders, retention, basket), §8 (visual) and §9 (acceptance gates).
  6. The Unit A closure spec: `Sales-Machine` branch `status/gt-pulse-a-2026-09-30`, `docs/superpowers/specs/2026-10-01-gt-pulse-a-preprod-closure-design.md`. Read §2 (glossary) and §3 (D1–D17).
  7. The D1 visual spec: same branch, `docs/superpowers/specs/2026-10-01-gt-pulse-d1-visual-design.md` (V1–V12).
  8. `Sales-Machine/CURRENT_STATE.md` on `status/gt-pulse-a-2026-09-30`: the top five dated sections and the UNRESOLVED list. `main` is stale (§7 L1).
  9. `gt-factory-os-production-brain/docs/decisions/modules/sales-declaration.md`: Amendment A, §5 data model, §15 M-Gates.
  10. The Menu Builder, for constraints only (§3 R5): `gt-factory-os-production-brain` branch `claude/menu-builder-discovery`, `docs/plans/2026-10-01-menu-builder/10-gt-pulse-integration-proposal.md`.
- **Inherited, not restated:**
  - Halt conditions, evidence standard and the 8 PASS fields: brain `CLAUDE.md` §Stop conditions, §Evidence, §Handoff.
  - Git discipline: never `git add -A` or `git add .`; branch from `main`; draft PR.
  - Migration slots and the FR1/FR2 bracket: `gt-factory-os/CLAUDE.md` §Migrations and `EXECUTION_POLICY.md` §FR1→write→FR2.
  - Watching: brain `CLAUDE.md` §Watching. After every `create_pull_request`, call `unsubscribe_pr_activity` immediately. Schedule no check-ins.
  - **Deltas for this work only** are in §8.
- **The standard (Tom, 2026-10-01):** `CRM מושלם גם בפני עצמו` — a perfect CRM on its own. Three bans with observable subjects:
  1. No number on screen without a source and a timestamp a tap away. This is program spec §9 gate 1.
  2. No money, history or signal shown for a disputed business↔customer link. This is §9 gate 4.
  3. No Hebrew string outside the approved register.
- **Language:** this document is English because that is the register you reason best in. Data literals stay in their own script, in backticks, and are never translated.
  - **Output language to Tom: concise Hebrew.** Short sentences. No preamble, no recap, no menus of options. Give one recommendation with a one-line reason. End with at most one action for him.
  - Code, commits, PRs and specs: English, following each repo's conventions.
  - UI copy: Hebrew, from the register only.

### 0.1 Skill orchestration — run each skill at its point, not all at once

Every skill below was verified installed on 2026-10-01. Invoke skills by name; do not open their `SKILL.md` files.
- Most come from `gt-factory-os-production-brain/.claude/skills/`.
- `frontend-design`, `ui-ux-pro-max` and `impeccable` come from `gt-factory-os-portal/.claude/skills/`.
- `/ux-release-gate` is a brain command.
- `simplify` and `code-review` are built-ins.

| Phase | Skills, in order | What the phase must produce | Exit criterion |
|---|---|---|---|
| **P1. Boot and ground truth** | `using-superpowers`, then `caveman` with arg `lite` (for chat with Tom only; never for specs, code or PR bodies) | §2.5 re-run, with the results compared to §2 | Every §2.2 number re-measured; differences listed |
| **P2. Product thinking** | `brainstorming`, then the grill. `/grill-with-docs` exists, but only Tom can invoke it (`disable-model-invocation: true`), so ask him once to type it. If he does not, run `grilling` together with `domain-modeling`, which are the two skills it loads, and keep `CONTEXT.md` and ADRs as it would. **Do not use `ponytail` in P1–P3.** | The B spec: `Sales-Machine/docs/superpowers/specs/<date>-gt-pulse-b-design.md`, with every §6 decision closed | Tom approves the spec in writing |
| **P3. Plan** | `writing-plans`, then `using-git-worktrees`, one isolated worktree per repo, from fresh `origin/main` | A plan with tasks small enough to verify. Every task names its test and its evidence | Plan committed; worktrees clean |
| **P4. Build** | `executing-plans` (or `subagent-driven-development` for independent tasks). `test-driven-development` for every SQL function, migration, API handler and data contract. `systematic-debugging` on any failure, regression or surprise; never patch at random. `ponytail` at level `lite` to reuse what exists (§3 R3) — but it may never remove an approved requirement or UX behaviour | Code plus tests | All tests green on a disposable DB (§7 L6) |
| **P5. UI** | `frontend-design` and `ui-ux-pro-max` *before* drawing a screen, then `impeccable` (critique and polish) while building it. For the signature visuals (circle, river, compass), also apply `taste-skill`. Its local copy is `gt-site/.claude/skills/taste-skill/SKILL.md`; if that is not attached, fetch `https://raw.githubusercontent.com/Leonxlnx/taste-skill/main/skills/taste-skill/SKILL.md`. Keep the GT Pulse language (§2.1): extend the `--s-*` tokens; never add a second design system | Org screen and visuals | Renders at 320/390/430/1280, light and dark, reduced motion, with no overflow |
| **P6. UX gate** | `/ux-release-gate`, in the sales profile (§7 L9), against the rendered app with long realistic fixtures. Fix every real P0 and P1, then re-gate | Gate report in brain `docs/phase8/dry-runs/` | 0 P0; every P1 fixed or decided by Tom |
| **P7. Independent review** | `requesting-code-review` (an independent reviewer subagent), then `code-review` at level `high` on each PR, then `receiving-code-review` to triage the findings. Review for: duplicate business logic, wrong source of truth, broken ownership, races, migration safety, permissions and rep scope, lead_event semantics, data-quality assumptions, and regressions to the live A/D1 flows | Findings fixed or answered | No open Critical or Important finding |
| **P8. Simplify** | Only after P6 and P7: `simplify`, then `ponytail-review`. Delete, merge duplicates, reuse infrastructure. Never weaken validation, security, a11y, error handling or an approved requirement. Then re-run every test affected | Smaller diff | Tests green again |
| **P9. Ship** | `finishing-a-development-branch`, then `/release-check`, then production per §4 W6 | Merged, applied, deployed | D9–D11 observed |
| **P10. Last act** | `verification-before-completion` on the exact final heads, after every fix and simplification. Then stamp the status line (D12) | Final report (§9) | Fresh evidence for each claim |

If a later finding sends you back (for example a P7 bug), loop to the earliest phase it touches and come forward again through P10. Never claim `DONE`, `READY` or `PASS` from evidence older than the last change.

## 1. Mission and definition of done

**One testable sentence:** in production, every Shopify customer that Tom's approved rule calls a verified B2B customer is exactly one `sales_core` org. Each such org shows:
- its verified contacts;
- a full order history that reconciles to Shopify, with drafts, cancellations, tests and refunds told apart;
- the business circle, event river and contact compass, each opening its source and timestamp.

| # | Condition | The observation that would prove it false |
|---|---|---|
| D1 | Ground-truth debt is closed before B code lands. Three things must hold: the GT Pulse docs branches are merged; files for `0353` and `0354` are on `gt-factory-os` `main` and match what production applied; and the backend PR gate runs the sales DB tests | (a) `git merge-base --is-ancestor origin/status/gt-pulse-a-2026-09-30 origin/main` fails in `Sales-Machine`, or the same check for `audit/gt-pulse-a-ux` fails in the brain repo. (b) A disposable DB built from `main`'s `db/migrations` differs from production in `information_schema.columns` (name, type, nullability, default) for `sales_core.customer_book`, `customer_price` or `list_price`, or in their grants (`information_schema.role_table_grants`). (c) There is no URL of a red backend check run on a throwaway draft PR that breaks one sales DB assertion (W0.3) |
| D2 | The B spec is written and Tom has approved it in writing, with every §6 decision recorded and dated | The spec file lacks an approval line quoting Tom, or any §6 item has no recorded answer |
| D3 | Identity is one model. Each verified customer maps to exactly one org. A chain is a parent of branches. No merge happens on name similarity or a public email domain. Disputed links sit in a review queue | A production query finds a `shopify_customer_id` on two orgs, a verified customer with no org, or an org whose screen shows money while its link status is disputed |
| D4 | Full order history is stored (paginated, every order ever), classified completed / draft / cancelled / test / refunded, with ex-VAT line money per `Sales-Machine/recipes/sales-report.md`. Drafts do not come back from the orders query (`recipes/sales-report.md:33`); they are read separately via `draftOrders` | For a random sample of 20 verified orgs taken in production after the backfill, comparing only orders with `created_at < T` (T fixed before the read): the order count per class differs from the Shopify Admin API at all, the ex-VAT total differs by more than 0.01 ILS, or the draft count differs from `draftOrders`. The sample must include the org with the most orders |
| D5 | Contacts: verified contacts are people at the buying business, each with provenance. Unverified ones sit in a separate review area. A café's own customers are never contacts (closure spec §2) | A contact without a provenance field, or an unverified contact rendered in the verified list |
| D6 | The org screen (portal) shows the order history, the business circle, the event river and the contact compass, at 320/390/430/1280, light and dark, and in reduced motion | Any node, line or number that does not open its source and timestamp. Horizontal overflow > 0 at any of those widths. Any text under 12px |
| D7 | Reps see only their own orgs (D3 of the closure spec extends to orgs, contacts and orders); managers see all | A rep session receives a success response carrying data for an org it does not own, or any order or contact row of another owner's org |
| D8 | Unit A and D1 behaviour is unchanged | Any existing sales unit test, mocked e2e, or pgTAP file fails on the final heads (the four known local `tel:` artifacts excepted, see §7 L7) |
| D9 | Production schema is applied through the deploy workflow, with `rebuild_verifier()` = 0 before and after | The workflow run log lacks the verifier lines, or either value ≠ 0 |
| D10 | The production backfill (orgs, contacts, orders) ran only after Tom's count-and-digest go, and it matches the preview | No Tom message approving that exact count and digest, or the applied counts differ from the preview |
| D11 | The API (Railway, deployed from the merge SHA via git, never `railway up`) and the portal (Vercel, READY on the merge SHA) are live, and the D4 reconciliation was re-run in production after deploy | The Railway deployment has no commit SHA, the Vercel deployment is not READY on the merge SHA, or there is no post-deploy reconciliation output |
| D12 | This file's status line is stamped `SHIPPED` with evidence pointers, and `Sales-Machine/CURRENT_STATE.md` has a dated B section | The status line still reads `LIVE`, or there is no B section |

Anything not on this list is out of scope unless Tom asks.

### 1.1 Settled — do not reopen

- **Program spec units, gates, ownership and visual language.** Tom approved them on 2026-09-29 (spec line 3). B's deliverable is spec §4 row B. §9 is the acceptance gate.
- **Unit A, D1, tranche 187 (corridor) and tranche 188 (copy round)** are live and Tom-approved (`CURRENT_STATE.md`, sections 2026-10-01 08:00 through 13:20 UTC). Do not redesign them; extend them.
- **Shopify is the order source.** LionWheel `orders_mirror` is not canonical (spec §7). Money is ex-VAT (Sales-Machine `doctrine/decisions.md` D-012).
- **A lead order stays a Shopify draft** until GT opens the customer (D-029).
- **`SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` stays `true`** (Tom, 2026-10-01). B adds no sending path.
- **The Menu Builder is not integrated in this session** (Tom, 2026-10-01). Read it only for constraints (§3 R5).
- **Sequencing** (Tom asked for this recommendation; see §3): W0 → B (+ the D elements that need only B) → C → the Builder integration. Unit E is deferred.

## 2. Ground truth — measured 2026-10-01; re-verify at boot

### 2.1 What is built and live

- **Backend `main` at `30759a2`** (GT Pulse Unit A, #329). The highest migration on `main` is `0362`.
- **Portal `main` at `89aa411`** (#243). The live production Vercel deployment is `dpl_J6zstx3ZCfrcythvyR4xb9aPA8dL`.
- **Sales corridor** (`gt-factory-os-portal/src/app/(sales)/`):
  - Today, with the journey flow, the petrol band and the mini rail.
  - Leads, Attention, Orgs and Settings, each with a petrol band.
  - The lead card, which has the D1 frame: header with mini rail, panels, history line.
  - The org card (`_components/OrgCard.tsx`), which shows a header, leads and **one lead's** timeline. It shows no orders and no contacts.
- **Tokens and copy:** design tokens live in `sales-tokens.css` (`--s-*`; shape lock V8; motion V6/V11). Copy lives in `_lib/labels.ts`, registered per tranche in `docs/portal-os/tranches/185…188`.
- **`sales_core`** (backend `db/migrations`): `org` (0318), `lead`, `lead_event` (append-only, 0320), `task` and `task_event` (0362), `lead_wait`, `activity_request`, and `sleeping_radar_run` (0346).
  - The identity functions `match_org` (0321) and `ingest_lead` (0361) match on Shopify id, then phone, then exact email, then business domain.
- **Shopify linkage today:**
  - At ingest, `supabase/functions/sales-leads-poll/index.ts` (around line 1001) takes the first hit of an email-or-phone search.
  - A daily backfill also runs (same file, the daily backfill block; read 2026-10-01).
  - Snapshots are built by `_lib/convert.ts` (lines 79–93).
  - Every order reader fetches live and stores nothing: convert (`first:20`), the sleeping radar (`first:15`), the bot (`first:40`), and portal pricing (40, with a 5-minute cache).

### 2.2 The numbers (production, 2026-10-01 ~14:00 UTC, read-only)

```
org 245 · org_with_shopify_cid 17 · org_snapshot_latest 2026-09-08 04:00 UTC
lead 263 · new 148 · working 38 · won 5 · lost 72 · lead_assigned 44
task open 187 · task done 0
lead_event since Unit A went live (2026-10-01 08:00 UTC): 16 total, 5 by humans
sales_core.customer_book 0 · customer_price 0 · list_price 0   (tables exist; see 2.4)
sleeping_radar_run: 29 runs, latest 2026-10-01 01:30 UTC; flags in latest run: insufficient_history 15, silent 1
private_core.orders_mirror 2132 (all LIONWHEEL) · orders_mirror_lines 7271
private_core.shopify_sales_90d 79 items, synced 2026-10-01 10:56 UTC (no customer dimension)
order_intake.wa_customer_map 212 · order_bot.customer 93 · customer_portal.order_submission 4
```

**What these mean:**
- The real customer base is invisible to the CRM.
- Three other customer-identity stores exist (`wa_customer_map`, `order_bot.customer`, `customer_portal.access`), and none of them is linked to `sales_core.org`.
- The radar sees 16 orgs.

### 2.3 What is NOT built

- A stored per-customer order history, and per-customer Shopify line items.
- A contacts model. Production has only two contact columns on `customer_book` (`contact_name`, `contact_phone`, from `0354`); there is no contacts table anywhere.
- A chain/branch map.
- An org-detail API.
- Any org-orders or org-contacts route.
- A curated sales catalogue view.
- Any UI that shows orders, contacts or the radar.
- A spec for B, C or E on any branch (survey of 2026-10-01).

### 2.4 Known-broken, adjacent, out of scope

- **Applied but not on `main`.** Production applied `0353_sales_core_price_book` and `0354_sales_core_customer_contact` on 2026-09-24 (`supabase_migrations.schema_migrations`). Their files exist only on the unmerged `gt-factory-os` PR #283 (branch `claude/shopify-customer-identifier-cwm1j1`, "Ice Dream handoff — price book, customer book, distributor package"). A DB built from `main` lacks `customer_book`, `customer_price` and `list_price`. Despite its name, `0354` creates no table: it adds `contact_name`, `contact_phone` and `served_by` (default `icedream`) to `customer_book`. `customer_book` is keyed by `shopify_customer_id` and carries `chain` and `tax_id`, so it is already an identity store. `0353` grants it to `service_role` only, commenting that customer contacts are PII. This is W0.
- **Snapshot shapes disagree.** The backend writes `orders_count`, `total_spent`, … (`0330`, `_lib/convert.ts:84-92`). The portal's `ShopifySnapshot` expects `status`, `rev12`, `orders`, `days_since_last_order` (`_lib/types.ts:31-40`; `_lib/wa.ts:54-70`). Measured 2026-10-01: all 14 orgs with a `shopify_snapshot` carry only `display_name`, `orders_count`, `total_spent`, `currency`, `snapshot_at`, `matched_by`, `matched_run`, so `CustomerContext` renders nothing for every org. Also 17 orgs have a Shopify id but only 14 have a snapshot. B replaces the snapshot with stored history; fix the contract there, not by patching the type.
- **Docs that are true are not on `main`.** None of these is merged:
  - `Sales-Machine` `design/gt-pulse-crm` (the program spec) and `status/gt-pulse-a-2026-09-30` (all specs and `CURRENT_STATE` since 2026-09-30);
  - brain `audit/gt-pulse-a-ux` (release packet and UX gate reports);
  - brain `claude/menu-builder-discovery`.
- **Backend CI** (`.github/workflows/typecheck.yml`) runs typecheck only. The sales DB tests run nowhere on PRs. `gt-pulse-a-branch.yml` targets a dead branch.
- **Open, unrelated PRs** stay untouched unless this document says otherwise: backend #330 (Menu Builder preview) and #283 apart from the W0 file port; portal #225, #217, #216, #212, #210, #207, #203, #196.
- **Real-device proof is still HOLD** for Unit A: WebKit/iOS keyboard save, a screen reader, the iOS date locale, and `tel:`.

### 2.5 Re-verification block

```sql
-- run read-only via the Supabase MCP, project rvadsozabmxkkrktwgnv; compare with 2.2 (measured 2026-10-01)
select 'org' t, count(*)::text n from sales_core.org union all
select 'org_with_shopify_cid', count(*)::text from sales_core.org where shopify_customer_id is not null union all
select 'org_snapshot_latest', max(shopify_snapshot_at)::text from sales_core.org union all
select 'lead_by_status', string_agg(s||':'||c,' ') from (select status s, count(*) c from sales_core.lead group by 1) x union all
select 'task_by_status', string_agg(s||':'||c,' ') from (select status s, count(*) c from sales_core.task group by 1) x union all
select 'human_events_since_A', count(*)::text from sales_core.lead_event where created_at >= '2026-10-01 08:00+00' and actor not like 'system%' union all
select 'customer_book', count(*)::text from sales_core.customer_book union all
select 'wa_customer_map', count(*)::text from order_intake.wa_customer_map union all
select 'order_bot.customer', count(*)::text from order_bot.customer union all
select 'applied_0353_0354', string_agg(name, ',') from supabase_migrations.schema_migrations where name in ('0353_sales_core_price_book','0354_sales_core_customer_contact');
```
```bash
# git baseline (2026-10-01: backend 30759a2, portal 89aa411; highest migration 0362)
git -C gt-factory-os log --oneline -1 origin/main; git -C gt-factory-os ls-tree --name-only origin/main db/migrations/ | tail -3
git -C gt-factory-os-portal log --oneline -1 origin/main
git -C Sales-Machine merge-base --is-ancestor origin/design/gt-pulse-crm origin/main && echo merged || echo NOT_MERGED
```

## 3. What the hard part actually is

- **R1. B is not "add an orders tab". It is giving the CRM its customers.** The 245 orgs are lead-born. The repeat B2B buyers who make most of GT's revenue live in Shopify, `wa_customer_map`, `order_bot.customer` and `customer_portal.access`, and none of those is linked to an org. B's centre of gravity is one identity model, with a verified-customer rule Tom approves and a review queue for doubt. The screens are downstream of that. Build the identity layer first, prove it on production data read-only, then build history and UI on it.
- **R2. "Full history" reverses a stated design.** `0318`'s header calls `shopify_customer_id` "a REFERENCE … we never mirror it". Spec §4/§7 requires a full paginated, classified, reconciled history, and the event river and Unit C both need it stored. Recommend a stored, idempotent mirror refreshed from Shopify, with reconciliation as a test. Put the reversal to Tom in P2 as an explicit decision, stating the cost of a live-only fetch: no event river, no C, and no reconciliation gate.
- **R3. Four stores already hold half of B.** `customer_book` (0353/0354: one row per Shopify customer with `chain`, `tax_id` and two contact columns; applied, empty, `service_role`-only because of PII), `wa_customer_map`, `customer_portal.access`, `order_bot.customer`, and the `customer-setup-shopify-gi` skill all touch customer identity. B must name one source of truth per fact and read the others as *evidence*. It must not add a fifth store. Ponytail's role in P4 is exactly this.
- **R4. Order of work after W0: B, then C, then the Builder.**
  - C's cadence and basket need B's stored history.
  - D's circle, river and compass need only B, so build them inside B.
  - D's basket map needs C plus a catalogue key, so it ships with C.
  - E (AI drafting) waits until B and C are stable and has separate quality and cost tests (spec §4 row E).
- **R5. The Builder constrains B's keys; it must not shape B's scope.** Builder V1 is leads-only and needs only A (`10-gt-pulse-integration-proposal.md` §3). V1.1 needs B's org identity, through `customer_portal.access` (`wa_phone` ↔ `shopify_customer_id`) and `sales_core.org.shopify_customer_id`. C's basket map should use the Builder's product key (the portal catalogue key; dependency ledger DL-18) and its single pricer (DL-10: "GT Pulse never computes a kit or a price"). So in B: keep `org.id` stable, keep `shopify_customer_id` unique per branch, and make `customer_portal.access` a mapped source, not a rival.

## 4. Workstreams

### W0 — Close ground-truth debt (P1; small, first)
1. **Docs PRs.** Open a draft PR from `Sales-Machine` `status/gt-pulse-a-2026-09-30` into `main`, and one from brain `audit/gt-pulse-a-ux` into `main`. Merge them per brain `CLAUDE.md` §Authorization (docs, checks green). The status branch already carries the program spec byte-identical to `design/gt-pulse-crm`. Do not merge `design/gt-pulse-crm` separately: both branches add `docs/plans/2026-09-29-gt-pulse-a-native-masterprompt.md` with different contents, and the status branch's version wins. Close `design/gt-pulse-crm`'s PR, if any, as superseded. Do not merge `claude/menu-builder-discovery`; leave it for the Builder session.
2. **Port the applied migrations.** Port `db/migrations/0353_sales_core_price_book.sql` and `0354_sales_core_customer_contact.sql`, and their `db/tests` files, **byte-identical** from PR #283 to a new backend branch.
   - This is an approved exception to "next slot = highest + 1": it lands slots production already applied. Still run the FR1/FR2 listing bracket. Never include `0353` or `0354` in a `migrations` glob passed to `deploy-production.yml`.
   - Prove in a disposable PG that `main` plus these files reproduces production's columns for the four tables.
   - Merge them. Do not merge or modify the rest of #283; that is Tom's Ice Dream work (§6 A).
3. **Backend PR gate.** Add a job that runs on every PR touching `db/`, `api/src/sales` or `api/src/order-intake`:
   - Port the postgres service, migration-apply, cron-stub and pgTAP steps from `.github/workflows/gt-pulse-a-branch.yml` (its lines 60–92 as of 2026-10-01), then delete that file.
   - The API DB tests switch on when `DATABASE_URL` points at `localhost` or `127.0.0.1` (`api/src/order-intake/sales/__tests__/lead_db.test.ts:15-17`); run them with `cd api && npm test` (`tsx --test`). Root Vitest runs through the root `test:*` scripts.
   - Prove it: open a throwaway draft PR that breaks one sales assertion, record the URL of the red check run, close the PR, and `unsubscribe_pr_activity`.

**Acceptance:** D1.

### W1 — Spec B (P2)

Write `Sales-Machine/docs/superpowers/specs/<date>-gt-pulse-b-design.md` from the grill. Close every §6 B item in it.
- Before each question to Tom: research it in code, docs and production yourself; think as GT's owner; state your recommendation; then ask only the decision that needs an owner.

**Acceptance:** D2.

### W2 — Identity layer (P3–P4)

- **Org model:** org = the buying branch (one Shopify customer). A chain is a parent grouping (sales-declaration §5 `account_hierarchy`). Match on evidence tiers. A disputed link has a status that blocks money and history.
- **Review queue:** a queue for unmatched and disputed links. Each item is a task with a manager owner, routed through the existing `sales_core.task` machinery. Do not add a new queue type unless the spec says so.
- **Mapped sources:** link `wa_customer_map`, `customer_portal.access` and `customer_book` as evidence. Never write to the first two. `customer_book` is reused or kept as evidence per the B spec (§6 A).
- **Tests:** TDD in pgTAP and Vitest. Cover: one customer → one org; a chain is not merged by name; a public email domain never links; a disputed link hides money.

**Acceptance:** D3, D7.

### W3 — Order history (P4)

- **Mirror and classification:** an idempotent mirror of every order per verified customer: header and lines, paginated to the end. Classify each order as completed, draft, cancelled, test or refunded. Keep line-level ex-VAT money per `recipes/sales-report.md`.
- **Reconciliation:** reconcile against the Shopify Admin API as an automated check you can run in production.
- **One client:** reuse one Shopify client. Replace the `first:15` / `first:20` / `first:40` readers only where the spec says so; never leave two truths.

**Acceptance:** D4.

### W4 — Contacts (P4)

There is no contacts table (§2.4). The B spec decides whether contacts get a new `sales_core` table or extend `customer_book`'s two columns; recommend a new table with provenance and verification state, with `customer_book.contact_*` read as evidence. Contacts are PII: keep `service_role`-only grants on raw tables and expose them only through rep-scoped API routes. Unverified contacts go to the review area.

**Acceptance:** D5.

### W5 — Org screen and D elements on B (P5–P6)

- **Screen and API:** an org detail screen (or the evolved `OrgCard`) with order history, contacts, the **business circle**, the **event river** and the **contact compass** (spec §8). API routes go under `queries/sales/orgs/:id/*`, with rep scope.
- **Mobile:** the visuals collapse to a vertical sequence.
- **Every node opens its source** and timestamp.
- **Tranches and copy:** new portal tranches with manifests (§7 L8). Hebrew copy is proposed to Tom as one batch (§6 C).
- **Visual approval:** show Tom before/after screenshots and a short motion video (§6 D).

**Acceptance:** D6, with the UX gate (P6).

### W6 — Ship (P9)

**The write path is code, not SQL by hand.** The backfill and the recurring mirror refresh run as one idempotent job in the backend (an API job route on Railway, or an Edge Function deployed through `.github/workflows/deploy-edge-function.yml`; the B plan picks one and names it). It has a dry-run mode that writes nothing and emits the preview counts and digest. The preview Tom approves must come from that same code in dry-run. Rollback: every backfilled row carries a `backfill_run` id, so one run can be undone by id without touching others.

Order matters, because Railway auto-deploys `main` on merge:
1. Announce in one line before dispatch (brain `CLAUDE.md` §Authorization).
2. Apply the **additive** migrations first, from the feature branch, through `gt-factory-os` `.github/workflows/deploy-production.yml`: `workflow_dispatch` on that branch with `confirm=APPLY`, the exact `migrations` glob, and `skip_deploy=true`. Its default `skip_deploy=false` runs `railway up` from the dispatched ref, an upload deploy without a git SHA. The workflow runs the `rebuild_verifier` preflight.
3. Merge with checks green. Railway then deploys `main` from git. Verify the Railway deployment the way the Unit A deploy was verified (`CURRENT_STATE.md`, the 2026-10-01 Unit A live section: deployment SUCCESS at the merge SHA, `/health` ok, new route returns 401 without auth). Inspect the real Railway response for the commit field; do not guess its name. If the metadata carries no SHA (a 2026-09-30 deploy in `CURRENT_STATE.md` had none), report that instead of claiming D11. Deploy the portal via Vercel `main`.
4. Run the job in dry-run, and give Tom the counts and digest. Apply only on his count-specific go.
5. Re-run the reconciliation in production.

**Acceptance:** D9–D11.

## 5. Scope

**IN:** everything in §4.

**OUT — do not touch and do not "improve":**
- **Unit C:** retention signals, check tasks and the basket map. Leave C one sentence in the B spec saying what it inherits.
- **Unit E**, and any AI drafting.
- **The Menu Builder:** any integration, route, `lead_event` type, `builder_session`, or merge of #330.
- Any outreach or sending path. Any write to Shopify, Green Invoice or LionWheel.
- The pricing tables' contents: `list_price`, `customer_price` (the Ice Dream work, §6 A).
- Factory core: `stock_ledger`, `items`, `bom_*`, `balance_anchors`, projections (Sales-Machine `CLAUDE.md` §Hard boundaries).
- Lead ingest semantics (`ingest_lead`), apart from what the B spec explicitly changes.
- The open portal PRs listed in §2.4.

## 6. Tom's part — the complete list; everything else is yours

Bring each item in P2 with your researched recommendation, one at a time.
- **A. Ice Dream PR #283.** Confirm that W0 may land only the `0353`/`0354` files on `main`, and that the rest of #283 stays his. Ask whether orders placed through the distributor still land in Shopify (sales-machine U-006). If some do not, B's "full history" needs a second source; the spec must say which. *Why only Tom:* it is his distributor deal and business process.
- **B. The B decisions:**
  1. The "verified B2B customer" rule.
  2. Org = branch, with a chain parent.
  3. The stored mirror versus live-only (R2).
  4. Which identity sources count as evidence.
  5. The contact sources and the verification rule.
  6. The default owner for an existing customer with no lead (spec §5 allows "explicit owner"; recommend a manager queue plus a one-time bulk assignment by Tom).
  7. Which roles see money.

  *Why only Tom:* these are product and ownership rules (spec §1.1, Sales-Machine rule 5).
- **C. Hebrew copy.** Approve one batch of new strings for the register. *Why only Tom:* portal `CLAUDE.md` UI language rules, and the register practice of tranches 185–188.
- **D. Visual.** Before/after screenshots and a motion video before merge (spec §9 gate 7).
- **E. Backfill go.** The exact org, contact and order counts and the digest from the read-only preview (D10).
- **F.** Optional: a real-device check of the org screen on his iPhone. If he declines, it stays HOLD and is reported as such.

## 7. Landmines — do not rediscover these

1. **Reading `main` gives a stale world.** All GT Pulse specs and `CURRENT_STATE` updates since 2026-09-29 are on unmerged branches (§2.4). → Read the branches named in §0, and merge them in W0.
2. **The migration named `customer_contact` creates no contacts table.** `0354_sales_core_customer_contact` only adds two contact columns to `customer_book`. Code surveys of `main` miss even those, because the file is not on `main`. → Check `information_schema` in production before designing; never trust a migration's name. W0 lands the files.
3. **Production credentials sit in the container env** (`DATABASE_URL`, Shopify and Resend keys, `RAILWAY_TOKEN`). DB tests refuse, or worse, hit production. → Run every local command through an env-scrubbed wrapper: `env -i PATH="$PATH" HOME="$HOME" …`.
4. **psql cannot reach the production DB** (no network route). → Use the Supabase MCP `execute_sql` for read-only checks and previews. Apply DDL only through `deploy-production.yml`.
5. **`NODE_ENV=production` in the env** makes `npm ci` skip devDependencies. → Use `npm ci --include=dev`.
6. **Supabase branch replay is broken**: history starts at `0090`, has gaps and duplicates, and contains data rows. → Build a disposable PG17 from `db/migrations` with Docker (image `supabase/postgres:17.4.1.054`), with the CI cron stub. Start `dockerd` as a background command so it survives.
7. **Four mocked sales e2e tests fail locally on Chromium 1194**: `sales-attention.spec.ts:285` and `sales-outcome-integrity.spec.ts:159/180/207`, all of which click a `tel:` link. They pass in CI on 1217.
   - Point Playwright at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` with a local, git-excluded config.
   - `mobile-*.spec.ts` targets WebKit, which is not installed; run them in Chromium at a phone viewport.
8. **The portal tranche hook** blocks any edit outside the active tranche's manifest (`docs/portal-os/tranches/_active.txt`). CI (`portal-pr-guard`) also fails if a new `docs/portal-os/tranches/*.md` is not listed in `docs/portal-os/registry.md`. → Create the tranche file, add it to the registry, and set `_active.txt` before you touch `src/`. Extend the manifest when the scope grows.
9. **The UX gate profile for the sales corridor** differs from the factory gate:
   - Hebrew RTL is checked against the copy register, not against English-first.
   - Test both roles (`planner` and `sales_rep`) through the dev-shim localStorage key `gt.fakeauth.v1`.
   - Test at 320/390/430/1280, in light, dark (the user preference `theme_preference` → `html.dark`, not OS emulation) and reduced motion.
   - Use long realistic fixture values; short fixtures hid a 655px sideways scroll in the lead card.
   - Capture viewport shots, not `fullPage`; fixed bars paint mid-page in fullPage shots.
   - Prior reports and dispositions: brain `audit/gt-pulse-a-ux`, `docs/phase8/dry-runs/2026-10-01-gt-pulse-*`.
10. **Opening a PR subscribes the session server-side**, and the hook cannot see it. → `unsubscribe_pr_activity` right after `create_pull_request`. Expect a later `subscription.created` notification, and unsubscribe again.
11. **The portal `Toast` was under an open drawer** until tranche 187 (fixed with `z-50`). Any new overlay must sit below `z-50` or deliberately above it. → Add an e2e that presses an action raised while an overlay is open.
12. **`sales-shell.test.tsx` prints 36 `ECONNREFUSED` lines.** The noise is pre-existing on `main` and not a failure.
13. **Unit A adoption is real but thin**: 5 human events in its first ~6 hours. → Do not reshape A's flows from usage data this small. Report adoption in the final report.

## 8. Halt conditions (additions to the inherited set)

- A design would merge two orgs or two Shopify customers without an evidence tier the approved spec allows → **STOP**, surface the case.
- Shopify reconciliation (D4) differs for any sampled org after two honest fixes → **STOP**. Report the diff; never widen the tolerance.
- Any write is needed outside `sales_core`, `api_read` views, or new B tables (for example `order_intake.*`, `customer_portal.*`, `private_core.*`) → **STOP**, ask.
- Migration slot drift between your two listings → **STOP**, `contract_failure` (backend `CLAUDE.md` §Migrations).
- `rebuild_verifier()` ≠ 0 at any point → **STOP**.

## 9. Final report (to Tom, in Hebrew; keep the evidence pointers in English)

Use brain `AGENT_TEMPLATE.md` §Output format, with tokens from `VERDICT_GLOSSARY.md`, plus:
1. What Tom can now open in production, and what it shows: one org, end to end.
2. D1–D12, each ✅ or ❌ with its evidence pointer. No partial credit.
3. The numbers: orgs, verified customers, contacts, orders by class, reconciliation diffs (0 expected), and Unit A adoption since 2026-10-01.
4. The artifacts: spec, plan, PRs, gate report, screenshots, video.
5. What is still Tom's, and what is unfinished: C's prerequisites, the Builder's prerequisites, and the real-device HOLDs.
6. The single next action. Expected: the masterprompt for Unit C.

If anything is not ready, say so first and plainly.
