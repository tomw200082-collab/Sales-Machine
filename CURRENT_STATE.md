# Sales-Machine — Current State

> Sole authority on build status and open unknowns. Volatile by design.
> Last updated: 2026-08-30.

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
| Live intake | **Make → `/ingest`** (was: Meta poller) | **CODE LANDED, AWAITING SCENARIOS** 2026-08-24 — gt-factory-os PR #227, migration 0329, `sales-leads-poll` redeployed. **Architecture changed today (D-006, reverses D10):** Tom holds no Meta developer access — the only Business app (`Green Tea`) is WhatsApp-only and he is not its admin, and developer registration blocks at SMS verification — so no Graph API token can be issued at all. Proven by the token diagnostic: the token he did produce is valid and non-expiring but carries **none** of `ads_management` / `leads_retrieval` / `pages_show_list` / `pages_read_engagement`. Make's own Meta-approved app carries the leads instead; its Facebook connection (`gteveryday`, 6309050) was reauthorised 2026-08-24 and is valid to 2026-10-23. **Still open:** the two Make scenarios (lead transport + hourly pulse) are not built — awaiting Tom's go-ahead |
| Conversion job + heartbeat | first Shopify order at-or-after a lead writes `won` + evidence; daily heartbeat | **LANDED** 2026-08-24. `sales_core.convert_lead()` is the sole writer of `won`. Heartbeat proven working 2026-08-24 04:00Z (sent, severity=alarm, correct). Now judges **whichever path is carrying leads** and, under Make, watches an **hourly pulse** — because with a third party in front a dead connection and a quiet day are otherwise indistinguishable, which is exactly how the 2026-06-07 failure hid for two months. Pulse route is live; the Make scenario that feeds it is not yet built |
| **Architecture under review** | Alexander's CTWA plan (2026-08-30) would replace the lead form with a Click-to-WhatsApp ad | **PROPOSED, NOT DECIDED** — `doctrine/decisions.md` **D-007**. Replaces the entry point and the transport only; `sales_core`, `lead_event`, the workspace, the conversion job and the heartbeat all carry over. Blocked before it can start by the same Meta access gap D-006 records, which CTWA cannot route around. Assessment: `evidence/2026-08-30-ctwa-plan-impact.md`; source: `evidence/2026-08-30-ctwa-plan-alexander-source.md`. Consequence already actionable: **D-008** proposes not building the Make lead-transport scenario, which D-007 would make dead work |

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
| U-013 | ~~Should the Facebook form ask for a business name again?~~ **SUPERSEDED 2026-08-30** — Alexander's plan removes the form entirely (D-007). The underlying need does not go away: a CTWA lead is *also* close to anonymous (a phone number and an ad id), so the qualifying question moves from the form into the first WhatsApp exchange | Folded into D-007; re-opens only if D-007 is rejected |
| U-014 | **Who administers the `Green Tea` Meta app and GT's ad account, and will they grant Tom or the technical owner admin?** D-006 proved GT holds none of it. Stages 1, 2 and 5 of Alexander's plan are all blocked on it, and unlike lead forms there is no Make-shaped way around it. This is a five-minute action by the right person | Alexander — proposed as task 0.0, ahead of his own stage 0 |
| U-015 | **One WhatsApp number or two?** GT already has a number in the API carrying B2B order intake. Sharing it means the CTWA auto-reply and the order bot receive one stream and must not answer over each other; separating it means two numbers, two webhooks, two quality ratings. The plan's own rule ("never put a customer-facing number in the API") was written without knowing one already is | Tom + Alexander — business decision; assessment §4.1 |
| U-016 | **What happens to the 188 imported leads under CTWA?** They have no open 72h window, so every contact is a paid business-initiated template and lands squarely in the case task 5.4's legal review exists to settle. They are also the most qualified list GT has | Tom + Alexander, with 5.4's legal answer |
| U-017 | Does a WhatsApp lead bot need an **Amendment B** to the sales module declaration? §11 lists Shopify-channel sends; this is a new integration surface | Tom — governance; `docs/decisions/modules/sales-declaration.md` |
| U-018 | **The workbook ("ספר העבודה") has never been seen by this repo.** The plan defers the first-reply wording, the answer bank, the day-5 and day-12 follow-up copy and "the boundaries" to it. Every stage-4, stage-5 and stage-7 task depends on content we do not hold | Tom — obtain it from Alexander |
| U-019 | **Unverified in the plan's cost model:** Meta's current 72-hour free-entry-point behaviour, and the Israel marketing-template tariff. The whole operational budget (task 5.3) rests on both. Reproduced from the plan, not confirmed against Meta's live pricing docs — rule 4 says check before writing | Technical — read Meta's pricing documentation directly, before any budget is approved |

## Pointers

- Module declaration (governance gate): `gt-factory-os-production-brain`
  `docs/decisions/modules/sales-declaration.md` — **APPROVED (Tom, 2026-08-04)**;
  **Amendment A APPROVED (Tom, in writing, 2026-08-17)**. The earlier
  "PR #46 — DRAFT, awaiting Tom" pointer was stale and is corrected here.
- **Alexander's CTWA build plan (2026-08-30):** source verbatim at
  `evidence/2026-08-30-ctwa-plan-alexander-source.md`; assessment against what GT already
  runs at `evidence/2026-08-30-ctwa-plan-impact.md`. Proposed decisions: D-007, D-008.
- Latest evidence snapshots (both 2026-08-24): `evidence/2026-08-24-make-intake-handover.md`
  (intake hand-over to Make) · `evidence/2026-08-24-sales-report.md` (sales report).
  Previous: `evidence/2026-08-23-live-intake-bringup.md`, `evidence/2026-07-18-two-numbers.md`.
- Sales report recipe: `recipes/sales-report.md` (taxonomy + anchors Tom-approved 2026-08-24).
- Decisions log (incl. PROPOSED items awaiting Tom): `doctrine/decisions.md`.
