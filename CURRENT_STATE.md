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
| U-011 | The Today queue currently holds all 188 leads, because every imported lead is genuinely untouched and past SLA. Honest, but a queue the size of the whole table is not "call these two, follow up on these three". Work the backlog down, or cap the daily queue? | Tom — product decision, deliberately not taken during the build |
| U-012 | Erik's role and how leads get assigned. The schema and the queue already scope per assignee (`assignee = me OR unassigned`, admins see all); only the UI to assign at scale is missing | Tom, when a second person joins |
| U-013 | Should the Facebook form ask for a business name again? The live form is two questions (name, phone, email), so an incoming lead is close to anonymous and the org has to be inferred | Tom + Alex — marketing decision with a direct data consequence |
| U-014 | Legal name `גרינטי אוירי דיי בע"מ` and ח.פ `515788461` are `doc_confirmed` from GT's own `/pages/אודות` — never checked against רשם החברות. Meta business verification rejects on a name/address mismatch more often than on missing documents, so this must be verified **before** any Meta submission | Tom — registrar check, or the company's accountant |
| U-015 | Which Instagram handle is GT's, and is `@greenteaeveryday` (zero posts, follows hundreds) compromised? Both handles serve a login/challenge wall to this environment — no public data obtainable. No Instagram work happens until this is answered | Tom (§6.B) — log in, or run account recovery |
| U-016 | GT holds no admin on its own Meta Business account. Blocks the WhatsApp green tag, business verification, the lead-form fix, CTWA, and re-authorising the connection before `2026-10-23` | Tom (§6.E) — find today's admin, or open a Meta support case |
| U-017 | `judge.me` and Yotpo both run on the live storefront — the theme config points at judge.me while the Yotpo loader fires on the same page. Customer reviews may be split across two systems with half invisible | Choose one. Yotpo already runs reviews **and** loyalty (`z2`), so it is the natural survivor |
| U-018 | Google Tag Manager loads on the storefront and nobody has said who owns the container or what fires in it. GA4 itself is still not connected (`g3`) | Tom — GTM account access |
| U-019 | Registrar and renewal date for `gteveryday.com` and `greentea-everyday.com` were never checked. A domain that lapses quietly takes the whole store down | Tom — registrar login, then record in `GT — כרטיס גישה` |
| U-020 | What `054-758-8132` is for — API number for the lead system, manual second line, or retired and merged into `054-398-2444`. It already carries a product catalog. Blocks stage 1 of the lead system and decides which number enters the identity card, the site, the `wa.me` link and the QR code | Tom (§6.A) — five minutes, unblocks two documents |
| U-021 | Cups-per-bottle is published as 33 / 30 / 13 on different live pages, and customer count as 700 / 200 (artifact `w5`). Until one approved number exists per claim, no number goes into any caption, page or profile | Tom — one number per claim |

## Pointers

- Module declaration (governance gate): `gt-factory-os-production-brain`
  `docs/decisions/modules/sales-declaration.md` — **APPROVED (Tom, 2026-08-04)**;
  **Amendment A APPROVED (Tom, in writing, 2026-08-17)**. The earlier
  "PR #46 — DRAFT, awaiting Tom" pointer was stale and is corrected here.
- Social/public-property base (2026-08-31): ownership audit
  `evidence/2026-08-31-social-property-audit.md` · Q4 content calendar
  `doctrine/playbooks/social-calendar-2026-Q4.md` · launch kits
  `doctrine/playbooks/linkedin-launch-kit.md`, `doctrine/playbooks/youtube-refresh-kit.md`.
  Credentials sheet lives in Tom's Drive, **not in this repo** — no secret value is ever
  written here (`GT — כרטיס גישה`, folder `GT Everyday — נכסי מותג`).
- Latest evidence snapshots (both 2026-08-24): `evidence/2026-08-24-make-intake-handover.md`
  (intake hand-over to Make) · `evidence/2026-08-24-sales-report.md` (sales report).
  Previous: `evidence/2026-08-23-live-intake-bringup.md`, `evidence/2026-07-18-two-numbers.md`.
- Sales report recipe: `recipes/sales-report.md` (taxonomy + anchors Tom-approved 2026-08-24).
- Decisions log (incl. PROPOSED items awaiting Tom): `doctrine/decisions.md`.
