# Sales-Machine — Current State

> Sole authority on build status and open unknowns. Volatile by design.
> Last updated: 2026-08-23.

## Build ladder status

| Phase | Scope | Status |
|---|---|---|
| 0 — Constitution | CLAUDE.md truth rules, structure, boundaries | **DRAFT LANDED** — awaiting Tom's written approval |
| 1 — Seed verified knowledge | research findings, evidence snapshot, recipes | **LANDED** (this commit) |
| 2 — Truth interviews with Tom | 5 sessions → `user_confirmed` doctrine + account dossiers | **NOT STARTED** — next up: Interview #1 (ICP) |
| 3 — System reconciliation | verify tag semantics, channel-move checks, contacts | not started (follows #2) |
| 4 — Agents (read-only first) | declarations in `agents/` | not started |
| 5 — Automations | only after base verified; outreach behind frozen flag | locked |

### Side track — the lead pipeline (factory-os lane, not this repo's phases)

| Step | Scope | Status |
|---|---|---|
| Schema | `sales_core` — org / lead / append-only lead_event, phone normalisation, one `ingest_lead` write path | **LANDED** 2026-08-17 (gt-factory-os #219, migrations 0318–0321, 43/43 pgTAP) |
| Import | the 2026-08-10 Meta export | **LANDED** — 188 leads / 186 businesses; 99 arrived after the intake died 2026-06-07 and had never been seen |
| Workspace — data | mutation functions + `api_read.v_sales_*` views + admin-gated Fastify endpoints | **LANDED** 2026-08-17 (gt-factory-os #220, migrations 0322–0323, 24/24 + 16/16 pgTAP) |
| Workspace — UI | portal `/apps` switchboard + `(sales)` route group: Today queue with the one-tap outcome loop, leads + drawer, orgs, quick-add, ⌘K search, PWA, settings. Hebrew RTL, admin-only | **LANDED** 2026-08-17 (gt-factory-os-portal #213, tranche 162) |
| Live intake | Meta poller + Resend alert | **LANDED (deployed dark)** 2026-08-23 — gt-factory-os PR #226, migration 0328, Edge Function `sales-leads-poll` v1 (ACTIVE, `verify_jwt=true`), cron jobs 27 (`*/10`) + 28 (`0 4 * * *`). Code, schedule and gate are in production; the poll ships `enabled=false` and no-ops without secrets. **Bring-up still BLOCKED on Tom** — `META_PAGE_ACCESS_TOKEN` (Business Manager System User) + `RESEND_API_KEY`, set in the Supabase dashboard. Meta keeps leads 90 days; the earliest unseen ones expire early September |
| Conversion job + heartbeat | first Shopify order at-or-after a lead writes `won` + evidence; daily heartbeat reports leads/24h, last lead, poll status | **LANDED (deployed dark)** 2026-08-23 — same PR. `sales_core.convert_lead()` is now the sole writer of `won` (still unwritable by any user, by CHECK constraint and by the API). Heartbeat sends daily whether healthy or not, and treats a disabled poll as an alarm. Waits on the same two secrets |

Nothing in this track sends anything to a lead or a customer.
`SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` remains `false`.

## Interview plan (Phase 2)

1. **ICP + segment ranking** — who is a dream client, who is marginal, why.
2. **Top-10 chain dossiers** — incl. U-001/U-002 below.
3. **Pricing & terms decode** — tag semantics (U-003), then system-verify.
4. **Sales process as-is** — how orders really arrive; roles; WhatsApp reality (U-004, U-006).
5. **Competition, positioning, Core Story raw material.**

Each interview → compiled cards → Tom confirms → merged as `user_confirmed`.

## UNRESOLVED (open unknowns — rule 3: never silently filled)

| ID | Question | Route |
|---|---|---|
| U-001 | Isrotel (~₪940K lifetime, ~13 branches) went dark ~2024-09/10 — churn, channel move, or tender loss? | Interview #2 + Green Invoice check |
| U-002 | Mina Tomei: 5 branches went dark the same week (~2026-02) — one story? recoverable? | Interview #2 |
| U-003 | Tag semantics: `10off`, `50-29`, `300ml-23`, `shotef`, `net30`, `pl`/`client_key` metafields | Interview #3 + system verify |
| U-004 | B2B records use placeholder login emails — where do real ordering contacts live? | Interview #4 |
| U-005 | ICP ranking (segments × buyer type) | Interview #1 |
| U-006 | Off-Shopify sales share (Green Invoice direct? distributor?) — required before any churn claim | Interview #4 + GI check |
| U-007 | Annual-value method assumes steady rate; validate per tier | Recipe validation |
| U-008 | "The website" scope — storefront vs. marketing site vs. B2B portal (separate runtime repo either way, per D-003) | Tom decision |
| U-009 | Data quirk: account with 58 orders and ₪0.00 amountSpent — explain before trusting spend fields | Interview #3 / system check |
| U-010 | 4 identity questions from the 2026-08-06 tracker build (MUZA×2, נונומימי/נונו, קפה עם, קלאוד ניין) — merge or keep separate? | Tom, via `knowledge/accounts/customer-notes.yaml` |
| U-011 | The Today queue currently holds all 188 leads, because every imported lead is genuinely untouched and past SLA. Honest, but a queue the size of the whole table is not "call these two, follow up on these three". Work the backlog down, or cap the daily queue? | Tom — product decision, deliberately not taken during the build |
| U-012 | Erik's role and how leads get assigned. The schema and the queue already scope per assignee (`assignee = me OR unassigned`, admins see all); only the UI to assign at scale is missing | Tom, when a second person joins |
| U-013 | Should the Facebook form ask for a business name again? The live form is two questions (name, phone, email), so an incoming lead is close to anonymous and the org has to be inferred | Tom + Alex — marketing decision with a direct data consequence |

## Pointers

- Module declaration (governance gate): `gt-factory-os-production-brain`
  `docs/decisions/modules/sales-declaration.md` — **APPROVED (Tom, 2026-08-04)**;
  **Amendment A APPROVED (Tom, in writing, 2026-08-17)**. The earlier
  "PR #46 — DRAFT, awaiting Tom" pointer was stale and is corrected here.
- Latest evidence snapshot: `evidence/2026-08-23-live-intake-bringup.md`
  (previous: `evidence/2026-07-18-two-numbers.md`).
- Decisions log (incl. PROPOSED items awaiting Tom): `doctrine/decisions.md`.
