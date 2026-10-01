# GT Pulse Unit A pre-production closure — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the Unit A gaps decided on 2026-10-01 (D3, D5, D6, D8, D11, D12), then prove the
whole loop on an isolated local stack and assemble a release packet — production untouched.

**Architecture:** Routing rules stay in `sales_core.tg_lead_event_task` (0362, amended in place:
it has never been applied anywhere, so no new slot). The order-line reply is one small worker
port that writes an event under the existing per-lead advisory lock. Read scope is three SQL
filters in `queries_handler.ts`. Portal changes are two conditionals in tranche 185.

**Tech Stack:** PostgreSQL 17 + pgTAP, Fastify/Kysely (node:test via tsx, Vitest for order-intake),
Next.js 15 + Vitest + Playwright (Chromium), Docker (Supabase Postgres + GoTrue + Mailpit).

**Spec:** `docs/superpowers/specs/2026-10-01-gt-pulse-a-preprod-closure-design.md`.

## Global Constraints

- No production merge, deploy, migration, flag flip, backfill or customer message.
- `stock_ledger` and factory core untouched. `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` stays false.
- No new Hebrew UI string. Existing approved strings only (tranche 185 register).
- `activity_required` stays false.
- No `git add -A` / `git add .`. Push to the existing branches; PRs #329/#239 stay draft.
- Every test count reported N/N on the exact head it ran on.

## File map

| File | Change |
|---|---|
| backend `db/migrations/0362_sales_activity_tasks.sql` | D5 source, D6 one open reply, D8 owner + reassignment |
| backend `db/tests/0362_sales_activity_tasks.test.sql` | expectations for D6/D8, new D5 cases |
| backend `api/src/order-intake/sales/order_line_reply.ts` (new) | D5 port: phone → open leads → note under lock |
| backend `api/src/order-intake/worker.ts` | optional `leadReply` dep, called on the order line |
| backend `api/src/order-intake/sales/__tests__/order_line_reply_db.test.ts` (new) | DB test incl. two-connection race with wake lock |
| backend `api/src/order-intake/__tests__/worker*.test.ts` | worker calls the port only on the order line, never throws |
| backend `api/src/sales/queries_handler.ts` | D3 rep scope on leads, orgs, lead events |
| backend `api/src/sales/mutations_handler.ts` | D8 rep may resolve own contact gap |
| backend `api/test/sales_workspace_tasks.test.ts` | D3/D8 contract tests |
| backend `.github/workflows/gt-pulse-a-branch.yml` | run the new DB test |
| portal `src/app/(sales)/_components/SalesShell.tsx` | D11 |
| portal `src/app/(sales)/_components/TaskCard.tsx` | D8 contact form for the owning rep |
| portal `tests/unit/sales/{sales-shell,leads}.test.tsx`, TaskCard test | D11, D12, D8 |

---

### Task 1: Routing rules D5, D6, D8 in 0362

**Files:** Modify `db/migrations/0362_sales_activity_tasks.sql` (trigger at ~line 102-214),
`db/tests/0362_sales_activity_tasks.test.sql`.

- [ ] **Step 1: failing pgTAP expectations.** In the test file change:
  - line 46 `'repeat contact adds one reply'` → expect `1` and rename `'one open reply per lead'`.
  - line 47-48 total for lead 11: `4` → `3`.
  - line 254 block: the open reply on lead 12 is the earlier `synthetic-wamid` one; assert
    `count(*) where kind='reply' and status='open'` = 1 and that `synthetic-after-wait` created a
    `lead_event` but no task.
  - Add after line 24:
```sql
update sales_core.lead set assignee='rep@example.com' where id='03620000-0000-4000-8000-000000000013';
select is((select owner_email from sales_core.task where lead_id='03620000-0000-4000-8000-000000000013' and kind='contact_resolution'),
 'rep@example.com', 'contact resolution follows the assignee');
update sales_core.lead set assignee=null where id='03620000-0000-4000-8000-000000000013';
```
  - Add a D5 case on lead 12 before it is lost:
```sql
insert into sales_core.lead_event(lead_id,event_type,payload,actor) values
 ('03620000-0000-4000-8000-000000000012','note','{"kind":"repeat_contact","source":"whatsapp_order_line","external_id":"synthetic-order-line"}','system:order-line');
select is((select count(*)::int from sales_core.task where lead_id='03620000-0000-4000-8000-000000000012' and kind='reply' and status='open'),1,
 'order-line reply joins the one open reply');
```
  - Add a contactless-created-with-assignee case (new lead `...014`, assignee set at insert,
    `phone_raw` null) asserting owner = assignee. Update `plan(N)` to the new total.
- [ ] **Step 2: run, expect FAIL** —
  `psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f db/tests/0362_sales_activity_tasks.test.sql` on a
  disposable DB built like CI (`.github/workflows/gt-pulse-a-branch.yml:55-97`).
- [ ] **Step 3: implement** in the trigger:
```sql
  elsif new.event_type='note' and new.payload->>'kind'='repeat_contact'
        and new.payload->>'source' in ('whatsapp_ctwa','whatsapp_unattributed','website_form','whatsapp_order_line')
...
  if v_kind='reply' then
    -- cancellations unchanged
    if exists (select 1 from sales_core.task where lead_id=new.lead_id and kind='reply' and status='open') then
      return new;  -- D6: the open reply already represents this work; the event is the evidence
    end if;
  end if;
  v_owner := v_lead.assignee;  -- D8: unowned work alone belongs to the manager queue
```
  and in `tg_lead_task_owner` drop `and kind<>'contact_resolution'`. Update the comments that
  say contact resolution is manager-only (line ~194, ~220).
- [ ] **Step 4: run, expect PASS N/N**, plus 0360/0361 tests unchanged.
- [ ] **Step 5: commit** `fix(sales): one open reply per lead; contact resolution follows owner; order-line replies route`.

### Task 2: Order-line reply port (D5)

**Files:** Create `api/src/order-intake/sales/order_line_reply.ts`,
`api/src/order-intake/sales/__tests__/order_line_reply_db.test.ts`; modify `worker.ts`,
worker unit test, CI workflow.

**Interfaces:** Produces `createOrderLineReply(pool: Pool): (ev: NormalizedMessage) => Promise<number>`
(returns notes written) and `WorkerDeps.leadReply?: (ev: NormalizedMessage) => Promise<unknown>`.

- [ ] **Step 1: failing DB test** (Vitest, local DB only, same guard as `wake_race_db.test.ts`):
  open lead with phone `+972501110777` → call port with `{from:'972501110777', wa_message_id:'w1'}`
  → one `repeat_contact` note (source `whatsapp_order_line`, external_id `w1`) and one open
  `reply` task; same event again → still one note; lost lead / opted-out lead / unknown phone →
  0 notes. Race: connection A holds `pg_advisory_lock(hashtext('sales_core.activity:'||lead))`
  (as `withLeadLock` does); the port call must not commit until A unlocks (assert the note is
  absent while A holds, present after).
- [ ] **Step 2: run, expect FAIL** (module missing).
- [ ] **Step 3: implement**
```ts
// Order-line reply — a lead who answers on the ORDER number (Tom 2026-10-01, D5).
// Writes the same repeat_contact fact the lead line's ingest writes, so routing
// stays in one place (tg_lead_event_task). Never creates a lead (U-025 is out of
// scope) and never sends. Serialised with wake sends by the per-lead lock.
import type { Pool } from 'pg';
import type { NormalizedMessage } from '../types.js';

export function createOrderLineReply(pool: Pool) {
  return async (ev: NormalizedMessage): Promise<number> => {
    const client = await pool.connect();
    try {
      await client.query('begin');
      const leads = await client.query<{ id: string }>(
        `select id from sales_core.lead
          where phone_e164 = '+' || $1 and status in ('new','working') and opt_out_at is null`, [ev.from]);
      let written = 0;
      for (const { id } of leads.rows) {
        await client.query(`select pg_advisory_xact_lock(hashtext('sales_core.activity:' || $1::text))`, [id]);
        const r = await client.query(
          `insert into sales_core.lead_event(lead_id,event_type,payload,actor)
           select $1,'note',jsonb_build_object('kind','repeat_contact','source','whatsapp_order_line','external_id',$2::text),'system:order-line'
            where not exists (select 1 from sales_core.lead_event where lead_id=$1 and event_type='note'
              and payload->>'source'='whatsapp_order_line' and payload->>'external_id'=$2)`, [id, ev.wa_message_id]);
        written += r.rowCount ?? 0;
      }
      await client.query('commit');
      return written;
    } catch (err) {
      await client.query('rollback').catch(() => {});
      throw err;
    } finally {
      client.release();
    }
  };
}
```
  In `worker.ts` after the `leadCapture` block (order line only):
```ts
  // A lead answering on the order number becomes a reply task (D5). Best effort:
  // the order pipeline below must run whatever happens here.
  await deps.leadReply?.(ev).catch((err) => console.error('order-line reply failed', err));
```
  and wire `leadReply: createOrderLineReply(pool)` in the live deps builder.
- [ ] **Step 4: worker unit test** with fakes: lead-line message → `leadReply` not called;
  order-line message → called once; a throwing `leadReply` → result identical to absent dep.
- [ ] **Step 5: run both, expect PASS**; add the DB test file to the `vitest run` line in
  `.github/workflows/gt-pulse-a-branch.yml:126`.
- [ ] **Step 6: commit** `feat(sales): order-line replies from open leads route a reply task`.

### Task 3: Rep read scope (D3) and own contact gap (D8)

**Files:** `api/src/sales/queries_handler.ts:164-208`, `api/src/sales/mutations_handler.ts:112-124`,
`api/test/sales_workspace_tasks.test.ts`.

- [ ] **Step 1: failing tests** using the existing `fixture`/`rolled` helpers:
```ts
test('a rep reads only own leads, events and orgs', { skip: !db }, async () => {
  await rolled(async (trx) => {
    const f = await fixture(trx);
    const leads = (await handleSalesLeads(trx, rep)).body.rows as Array<{ id: string }>;
    assert.ok(leads.some(r => r.id === f.owned.id));
    assert.ok(!leads.some(r => r.id === f.unowned.id));
    await assert.rejects(handleSalesLeadEvents(trx, rep, f.unowned.id), AuthError);
    assert.ok((await handleSalesLeadEvents(trx, rep, f.owned.id)).body.rows.length > 0);
    assert.ok(((await handleSalesLeads(trx, manager)).body.rows as Array<{ id: string }>).some(r => r.id === f.unowned.id));
    await handleSalesLeadEvents(trx, manager, f.unowned.id);
  });
});
test('a rep resolves the contact gap of an own lead only', { skip: !db }, async () => {
  await rolled(async (trx) => {
    const f = await fixture(trx, true);
    await assert.rejects(handleResolveContactGap(trx, rep, f.unowned.id,
      { phone: '0501111299', provenance: 'synthetic' } as never), AuthError);
    const r = await handleResolveContactGap(trx, rep, f.owned.id,
      { phone: '0501111298', provenance: 'synthetic' } as never);
    assert.equal(r.body.lead_id, f.owned.id);
  });
});
```
  Orgs: assert a rep's org list holds only orgs with a lead assigned to them.
- [ ] **Step 2: run** `cd api && npx tsx --test test/sales_workspace_tasks.test.ts` → FAIL.
- [ ] **Step 3: implement**
```ts
const repOnly = (session: Session) => session.role === 'sales_rep';
// handleSalesLeads
  const scope = repOnly(session) ? sql`where assignee = ${session.email}` : sql``;
  select * from api_read.v_sales_leads ${scope} order by ...
// handleSalesLeadEvents — before the select
  if (repOnly(session)) {
    const own = await sql`select 1 from sales_core.lead where id=${leadId}::uuid and assignee=${session.email}`.execute(db);
    if (own.rows.length === 0) throw new AuthError('Not authorised', 403);
  }
// handleSalesOrgs
  const scope = repOnly(session)
    ? sql`where id in (select org_id from sales_core.lead where assignee = ${session.email})` : sql``;
```
  `handleResolveContactGap`: replace the role throw with
  `return withOwnedLead(db, session, leadId, async (trx) => { ...same select on trx... })`
  and update its doc comment ("the owner or a manager").
- [ ] **Step 4: run** the file and `test/sales_workspace.test.ts` → PASS N/N; `npm run typecheck`.
- [ ] **Step 5: commit** `feat(sales): reps read only own leads; owners resolve own contact gaps`.

### Task 4: Portal D11, D8, D12

**Files:** `src/app/(sales)/_components/SalesShell.tsx:129-140`, `TaskCard.tsx:76`, tests.

- [ ] **Step 1: failing tests**: `sales-shell.test.tsx` — with role `sales_rep`,
  `queryByTestId('sales-switch-factory')` is null; with `planner` it is present.
  TaskCard test — owned `contact_resolution` task with `manager={false}` renders the contact form.
  `leads.test.tsx` — `?lead=<id not in rows>` renders `lead-not-found` (add only if not covered).
- [ ] **Step 2: run** `npx vitest run tests/unit/sales` → FAIL.
- [ ] **Step 3: implement**: wrap the switch `<Link>` in `{session?.role !== "sales_rep" ? … : null}`;
  TaskCard condition `contactGap && task.lead_id && (manager || !task.needs_assignment)`.
- [ ] **Step 4: run** unit tests, `npm run typecheck`, `npm run lint` → PASS.
- [ ] **Step 5: commit** within tranche 185 manifest; if a file is outside it, add it to the
  manifest in the same commit with the D-number as authority.

### Task 5: Push and exact-head CI

- [ ] Push both branches; confirm PR #329 `sales-db`, `staff-mail`, `typecheck` and PR #239 `ci`
  on the new heads. Fix any red before continuing.

### Task 6: Local isolated stack (D1)

- [ ] `docker run` Supabase Postgres 17 (`supabase/postgres:17.4.1.054`), apply
  `db/migrations/*.sql` in order with `-1`, logging every failed file; GoTrue `v2.177.0` with an
  ES256 JWK (`GOTRUE_JWT_KEYS`), SMTP to Mailpit, behind a path proxy exposing
  `/auth/v1/*`. Seed: `app_users` rows for `rep@staging.invalid` (`sales_rep`) and
  `manager@staging.invalid` (`planner`); two synthetic leads (one per owner), reserved numbers only.
- [ ] API: `NODE_ENV=production`, dev shim off, `SUPABASE_URL` = proxy, `DATABASE_URL` = local.
  Portal: `next build && next start` with `NEXT_PUBLIC_SUPABASE_URL`/`ANON_KEY` local,
  `API_BASE` local, dev shim off.
- [ ] Evidence: skipped-migration list, `to_regclass('sales_core.task')`, JWKS `alg=ES256`.

### Task 7: Connected proof (P2, P3)

- [ ] Playwright (Chromium) against the local stack: signed out → magic link from Mailpit →
  `/sales/leads?lead=<rep lead>` → record activity → capture `x-request-id`, query the committed
  `lead_event`/`task` rows; rep request for manager lead events → 403 and absent from list.
- [ ] Draft durability: fill note, abort the request (route intercept timeout), reload → draft
  restored; resubmit with the same `request_id` → one event.
- [ ] Order-line reply + wake race on the local DB (Task 2's test, re-run against the stack).
- [ ] Redacted screenshots to the brain evidence folder.

### Task 8: UX gates (P4)

- [ ] `/frontend-design` + `ui-ux-pro-max` review of the touched surfaces (no new copy).
- [ ] Fixture `/ux-release-gate` (five agents + governor), labelled fixture.
- [ ] Connected five-lens audit on the local stack, rep + manager, 320/390/430/1280, light/dark,
  reduced motion, keyboard. WebKit: HOLD (not installed).
- [ ] Fix verified P0/P1 RED→GREEN; rerun both.

### Task 9: Simplify, review, verify, release packet (P5, P6)

- [ ] `/simplify` on both branch diffs; `/code-review` per repo; fix Important/Critical.
- [ ] `verification-before-completion` on final SHAs: pgTAP, Vitest, tsx tests, typecheck,
  portal unit/lint/build, focused Playwright, PR checks.
- [ ] Release packet in brain `docs/phase8/dry-runs/2026-10-01-gt-pulse-a-release-packet.md`:
  SHAs, 0362 checksum, order (migration → API → portal), flags unchanged, zero-outreach
  invariant, preflight, rollback, unperformed production checks (Resend delivery, Railway SHA,
  backfill count go/no-go), one Tom decision.
- [ ] Update Sales-Machine `CURRENT_STATE.md`, execution index, masterprompt status; tear down
  the local stack.
