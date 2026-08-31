# Sales-Machine — Current State

> Sole authority on build status and open unknowns. Volatile by design.
> Last updated: 2026-08-31.

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
| U-011 | Work the backlog down, or cap the daily queue? **Now costed (2026-08-31):** 141 `new`, all with a phone — 94 recent (≤90d) · 35 cold (>90d) · 10 already Shopify customers · 2 duplicates. At the configured `queue.daily_cap = 15` that is **7 working days for the recent tier, 10 for all 141**. 58 leads have already been worked. Triage published as `api_read.v_sales_backlog_triage` (gt-factory-os migration 0341); no lead's status was changed — a 141-row re-state is a mass write and stays Tom's | Tom — product decision, deliberately not taken during the build |
| U-012 | Erik's role and how leads get assigned. The schema and the queue already scope per assignee (`assignee = me OR unassigned`, admins see all); only the UI to assign at scale is missing | Tom, when a second person joins |
| U-013 | Should the Facebook form ask for a business name again? The live form is two questions (name, phone, email), so an incoming lead is close to anonymous and the org has to be inferred | Tom + Alex — marketing decision with a direct data consequence |
| U-014 | 275 distinct phone numbers have written to GT's live WhatsApp since 2026-06-28 (163 in the last 30 days) and are classified `ignored_unknown_or_disabled`; essentially none exists in `sales_core` (1 of 275). How many are leads rather than unmapped customers, suppliers or staff? No identification layer exists to answer it. Shape argues most are not enquiries (avg 20.8 messages/sender; 117 conversations span >7 days); the lead-shaped floor is the 36 single-message senders, 11 of them in the last 30 days | build the first-message write (architecture doc §Q2), then measure for 30 days |
| U-015 | Meta's current marketing-template rate for Israel. The public pricing page defers to an interactive rate card that serves no fetchable document | Tom — GT holds a WABA, so the authoritative rate is in GT's own Meta Business Manager billing page. ~2 minutes |
| U-016 | `META_PAGE_ACCESS_TOKEN` carries no Leads Access on the page — the cause of two real leads rejected on 2026-08-24 (leadgen `1807021066847822`, `1469012341930658`), recoverable from Meta only until **2026-11-22**. Distinct from D-006: Make carries the lead, this token fetches its content | technical — next intake session |
| U-017 | A second Facebook form id, `1771287887148857`, appears in `lead_reject` but the pulse reports `forms_visible: 1`. Live form or stale test form? | Tom + Alex, via Meta Ads Manager |
| ~~U-018~~ | **WITHDRAWN 2026-08-31** — not an open question. Tom decided the opening menu's price is deliberately never stated (D-013); it is a transfer row by design | closed |
| ~~U-019~~ | **CLOSED 2026-08-31** — the order cutoff is **14:00** (Tom). Worth six days to a north/south customer, one to three in the centre | closed |
| ~~U-020~~ | **CLOSED 2026-08-31** — derived from 1,555 completed LionWheel deliveries: צפון=שלישי · דרום=רביעי (**including Jerusalem and the Shfela**) · מרכז=ראשון/שני/חמישי. `doctrine/commercial-terms.md` §3 | closed |
| U-021 | The deck's margin percentages (77–87 %) imply the food cost arithmetically, which D-013 says is never stated. Do the margin figures stay? | Tom |
| ~~U-022~~ | **CLOSED 2026-08-31** — the number **is** in use, and that is not a blocker: **coexistence** keeps it in the WhatsApp app while the Cloud API rides alongside, exactly as GT's order line has since 2026-06-26 (9,440 staff-echo events prove it). The artifact's warning that a number entering the API leaves the app permanently is true of classic onboarding, **not** of coexistence. Standing requirement: the app must be opened at least once every 13 days and never uninstalled, or coexistence lapses — needs a named owner | closed |

## Pointers

- Module declaration (governance gate): `gt-factory-os-production-brain`
  `docs/decisions/modules/sales-declaration.md` — **APPROVED (Tom, 2026-08-04)**;
  **Amendment A APPROVED (Tom, in writing, 2026-08-17)**. The earlier
  "PR #46 — DRAFT, awaiting Tom" pointer was stale and is corrected here.
- Latest evidence snapshot: `evidence/2026-08-31-lead-response-ground-truth.md` — measured lead,
  transport, backlog, first-response and WhatsApp ground truth; **records that GT's WhatsApp Business
  Cloud API has been live since 2026-06-26 (Dualhook coexistence, 24,028 events), which several planning
  documents still describe as not built.** Companion decisions in `gt-factory-os-production-brain`:
  `docs/decisions/2026-08-31-lead-intake-architecture.md` (awaiting Tom) and
  `docs/plans/2026-08-31-lead-setup-artifact-reconciliation.md`.
- Previous evidence snapshots (both 2026-08-24): `evidence/2026-08-24-make-intake-handover.md`
  (intake hand-over to Make) · `evidence/2026-08-24-sales-report.md` (sales report).
  Previous: `evidence/2026-08-23-live-intake-bringup.md`, `evidence/2026-07-18-two-numbers.md`.
- Sales report recipe: `recipes/sales-report.md` (taxonomy + anchors Tom-approved 2026-08-24).
- Decisions log (incl. PROPOSED items awaiting Tom): `doctrine/decisions.md`.
