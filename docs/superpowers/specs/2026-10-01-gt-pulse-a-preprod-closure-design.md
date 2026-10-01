# GT Pulse Unit A — pre-production closure design

**Date:** 2026-10-01 · **Status:** approved — Tom accepted every recommendation in the
2026-10-01 grill round (Q1–Q9) and delegated the remaining design decisions in this
document to Claude ("תחשוב לעומק ותמליץ לי ותחליט בשבילי"). New Hebrew copy, paid
resources and anything in production are **not** covered by that delegation.

**Parents:** `design/gt-pulse-crm` → `2026-09-29-gt-pulse-crm-program-design.md` (PG),
`2026-09-29-sales-activity-task-loop-design.md` (TL), plan `2026-09-29-gt-pulse-a-sales-task-loop.md`.
This document amends TL where stated and adds the closure work. It does not rebuild the nine
completed tasks.

## 1. Facts this design rests on (2026-10-01 05:07–05:30 UTC)

- Review heads unchanged: backend `ff69e3c` (PR #329, checks green), portal `1ba2c98`
  (PR #239, `ci` green). Both branches are 0 behind their `main`.
- Production: `sales_core.task` absent, 261 leads. Active sales-capable users: 2 `admin`,
  4 `planner`, **0 `sales_rep`**. Everyone working leads today is a manager by the code's rule.
- Supabase branching cannot rebuild this schema: the managed migration history starts at
  `0090` (0001–0089 were applied with psql and never recorded), has gaps, duplicates and
  data-write rows. `private_core.supplier_items` exists in `db/migrations/0002_masters.sql:239`;
  the branch failed because 0002 was never in the history it replays.
- Docker runs in the session container; `supabase/postgres:17.4.1.054` and
  `supabase/gotrue:v2.177.0` pull. Playwright has Chromium only (no WebKit).
- Inbound on the **lead line** reaches `ingest_lead`, which writes a `repeat_contact` note, which
  routes a `reply` task. Inbound on the **order line** from a lead's phone only flips the wake
  guard's `replied` (`wake.ts:263-269`); no event, no task.

## 2. Glossary (canonical terms)

- **Lead** — one enquiry/opportunity from a business; status `new | working | won | lost`.
- **Org** — the business; the lasting relationship behind one or more leads.
- **Contact** — a person at the buying business. A café's own customers are never contacts.
- **Lead event** — an append-only fact that already happened on a lead. Corrections are new events.
- **Task** — work still to be done, routed from a lead event; `open | done | cancelled`, always dated.
- **Owner** — the lead's `assignee`; a task's owner follows it.
- **Rep** — a user with role `sales_rep`. Sees and acts on own leads only.
- **Manager** — a user with role `planner` or `admin`. Sees all leads, owns the unassigned queue,
  assigns. No separate manager role exists or is added.
- **Manager queue** — open tasks with no owner (unassigned lead) or an inactive owner.
- **Waiting** — a dated pause chosen by a human (`lead_wait`); stops wake sends, never sends by itself.
- **Reply** — an identified inbound message from the lead (either WhatsApp line, or form); creates
  at most one open `reply` task per lead.
- **Conversion (won)** — a Shopify order or a Green Invoice document number recorded by a person.
  A draft order is never a conversion.
- **Lead line / order line** — `054-758-8132` (leads) and `054-398-2444` (existing customers'
  orders). Distinguished only by `phone_number_id`.

## 3. Decisions

| # | Decision | Reason |
|---|---|---|
| D1 | Staging = local isolated stack in the session container (§5). No Supabase branch, no new project. | $0, real GoTrue, zero production contact; branch replay is structurally broken. |
| D2 | Manager = `planner` or `admin`. No new role. | Matches code and every current user. |
| D3 | Reps read only their own leads: lead list, lead events, orgs (only orgs behind own leads), lead detail. Unassigned leads appear only to managers. Aggregate week stats stay global (counts, no rows). | Least privilege; gives the falsifiable cross-owner denial P2 requires. |
| D4 | A rep may record WhatsApp `answered_progressing` on their own word. TL:21/TL:71 amended: the event's actor is the provenance; identified inbound is not required. | The lead line has never delivered inbound (U-050); enforcement would block real work. |
| D5 | Order-line inbound from the phone of an open, not-opted-out lead writes a `repeat_contact` note (source `whatsapp_order_line`, external id = wamid). That routes a `reply` task like the lead line does. | Closes the silent-reply gap without creating leads from the order line (U-025 stays out of scope). |
| D6 | At most one open `reply` task per lead, on every source. Later replies while one is open add events only. | Ten messages must not mean ten tasks. |
| D7 | No first-contact SLA escalation. `contact_first` stays due `now()`; overdue shows in Today/Attention. | YAGNI; overdue already surfaces. Revisit if leads go stale. |
| D8 | Contactless lead with an assignee: the `contact_resolution` task goes to the assignee. Without one, it goes to the manager queue. Reassignment moves **all** open tasks, including `contact_resolution`. | The owner can research the contact; the manager only handles unowned work. |
| D9 | Quick-result default follow-ups stay (1 business day no-answer, 2 for WhatsApp/email), prefilled and editable. TL "the date chosen" amended accordingly. | Faster entry; the rep still chooses. |
| D10 | Conversion rule unchanged (Shopify order or rep-entered Green Invoice number, actor recorded). | Auditable after the fact; no new integration. |
| D11 | Sales shell hides "switch to factory" for `sales_rep`. | Reps have no factory surface; the link is a dead end. |
| D12 | Staff alert recipients unchanged. A rep opening a deep link to a lead that is not theirs gets the portal's existing not-found/denied state; if no approved string fits, that state is a copy HOLD, not invented copy. | No production email behaviour change; no unapproved copy. |
| D13 | Scope = Unit A + D3, D5, D6, D8, D11 + proofs. Out: org tasks, org owner after conversion, Units B–E, lead creation from the order line, SLA. | Bounded closure. |

## 4. Changes

**Backend (`gt-factory-os`, PR #329):**

1. Amend `db/migrations/0362_sales_activity_tasks.sql` in place (never applied to any
   environment, so no new slot) — `sales_core.tg_lead_event_task` and `tg_lead_task_owner`:
   - D8 owner rule: `v_owner := v_lead.assignee` for every kind; reassignment drops the
     `kind<>'contact_resolution'` exclusion.
   - D5: accept `whatsapp_order_line` in the `repeat_contact` source list.
   - D6: skip the `reply` insert when an open `reply` task exists for the lead (cancellation of
     `contact_first`/`wait_review` and wait deactivation still run).
   - pgTAP test for each rule, including the reassignment of `contact_resolution`.
2. Order-line hook (`api/src/order-intake/worker.ts` message path, order line only): after the
   inbound row is logged, insert the D5 note for each matching open lead, idempotent on
   (lead, wamid), under the same per-lead advisory lock the wake send holds
   (`hashtext('sales_core.activity:'||lead_id)`), so a reply and a wake send serialise.
   A failure here is logged and never breaks the order pipeline.
3. Read scope (D3) in `api/src/sales/queries_handler.ts`: `handleSalesLeads`, `handleSalesOrgs`
   filter by `assignee = session.email` for `sales_rep`; `handleSalesLeadEvents` returns 403 for a
   rep on a lead not assigned to them. Tests: rep A denied on rep B's lead; manager allowed.

**Portal (`gt-factory-os-portal`, PR #239, tranche 185):**

4. D11: render the switch link only when `role !== "sales_rep"`.
5. D12: verify the deep-link path for a non-owned lead shows an existing approved state; test it.
6. Any change the UX gates (P4) find at P0/P1, within tranche 185 and approved copy.

## 5. Staging (D1)

Containers in the session: Supabase Postgres 17 image, GoTrue configured with an **ES256**
signing key (the API verifies ES256 via JWKS at `${SUPABASE_URL}/auth/v1/.well-known/jwks.json`),
a path proxy exposing `/auth/v1`, and a local mail catcher. Schema from `db/migrations/*.sql`
in order, with the CI stub set where the image lacks an object; every skipped file is listed in
the evidence. The API runs locally against it (`NODE_ENV=production`, dev shim off), the portal
runs as a production build pointed at both.

Test identities exist only there: one `sales_rep`, one `planner`, two synthetic leads each with
no real phone or email (`.invalid` / reserved test numbers). No production data, no provider
tokens, no Resend: the magic link lands in the local mail catcher. Everything is torn down at
the end of the session.

Limits stated in every report: Resend delivery and the Railway/Vercel runtime are proven only
in the later production session; WebKit is unavailable here, so the WebKit keyboard proof is a
HOLD.

## 6. Proof

- P2: signed-out email link → GoTrue login → `/sales/leads?lead=` → activity save; request ID
  correlated to the committed `lead_event` and `task` rows; rep denied on the manager-owned
  lead's events (403) and absent from its lead list.
- P3: atomic note/action/date on Today, Leads, Attention; reload recovers the draft; retry with
  the same key does not duplicate; two-connection race: order-line inbound vs wake send on the
  same lead — either the reply commits first and the send is skipped, or the send completes
  first and the reply still routes one task.
- P4: fixture `/ux-release-gate` (labelled fixture) + connected five-lens audit (labelled
  connected), 320/390/430/desktop, light/dark, reduced motion, keyboard.
- P5: simplify/ponytail-review, whole-branch review, verification-before-completion on final SHAs.

## 7. Error handling

- The order-line hook never throws into the order pipeline; it logs and continues.
- A rep's denied read returns 403 with no lead data in the body.
- 0362 is unapplied anywhere; its rollback is unchanged from the release checklist.
