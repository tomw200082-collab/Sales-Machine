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
| Live intake | **Make → `/ingest`** (was: Meta poller) | **LIVE** — code landed 2026-08-24, scenarios verified running 2026-08-31 — gt-factory-os PR #227, migration 0329, `sales-leads-poll` redeployed. **Architecture changed today (D-006, reverses D10):** Tom holds no Meta developer access — the only Business app (`Green Tea`) is WhatsApp-only and he is not its admin, and developer registration blocks at SMS verification — so no Graph API token can be issued at all. Proven by the token diagnostic: the token he did produce is valid and non-expiring but carries **none** of `ads_management` / `leads_retrieval` / `pages_show_list` / `pages_read_engagement`. Make's own Meta-approved app carries the leads instead; its Facebook connection (`gteveryday`, 6309050) was reauthorised 2026-08-24 and is valid to 2026-10-23. **CORRECTED 2026-08-31 (read live from the Make API):** both scenarios **are built and running**. `GT Sales — lead intake → /ingest` (id 7075235, instant webhook 3598876) has been green on every run since Tom's last edit 2026-08-24 16:50Z — 11 consecutive successes, most recent lead 2026-08-29 20:16Z; its lifetime 32 errors are all from the build session that day, and 2 items sit in its DLQ. `GT Sales — hourly pulse` (id 7075243) has fired every hour with zero failures, last at 2026-08-31 12:11:15Z. The Facebook connection `gteveryday` (6309050) carries all 9 scopes incl. `leads_retrieval`, `ads_management` and `business_management`, and expires 2026-10-23T10:49:05Z |
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
| U-011 | **Re-measured live 2026-08-31: 200 leads — 142 `new`, 12 `working`, 3 `won`, 43 `lost`, and 188 with no assignee.** So the queue is being worked (Avi, 113 events) but almost nothing is owned. Tom decided 2026-08-31: he is primary, Avi and Alex take the large ones; the 142 untouched stay for a planned personal bulk outreach rather than being closed. Original entry: the Today queue currently holds all 188 leads, because every imported lead is genuinely untouched and past SLA. Honest, but a queue the size of the whole table is not "call these two, follow up on these three". Work the backlog down, or cap the daily queue? | Tom — product decision, deliberately not taken during the build |
| U-012 | Erik's role and how leads get assigned. The schema and the queue already scope per assignee (`assignee = me OR unassigned`, admins see all); only the UI to assign at scale is missing | Tom, when a second person joins |
| U-013 | Should the Facebook form ask for a business name again? The live form is two questions (name, phone, email), so an incoming lead is close to anonymous and the org has to be inferred | Tom + Alex — marketing decision with a direct data consequence |
| U-014 | **CLOSED 2026-08-31.** Legal name is `גרינטי אוירי די בע"מ` (`די`) and ח.פ `515788461`, per the Meta business record verified against official documents 2022-12-30 — `system_verified`. The earlier `doc_confirmed` reading from `/pages/אודות` had the wrong spelling and the page was corrected. Tom declined a registrar check as unnecessary given the Meta record | — |
| U-022 | Meta's verified record holds the **registered** address `מיכ"ל 4, תל אביב יפו 63261`, while `הלהב 15, חולון 5885817` is the **published** address (Tom's decision, and what Shopify and Klaviyo hold). Both can be correct — registered vs. operating — but Meta's copy is from 2022 and nobody has confirmed it is still current | Tom — confirm the registered address is unchanged before any document-bearing submission |
| U-023 | `+972547689911` is the business phone on Meta's verified record. It appears in no other GT system and nobody has said whose it is | Tom — identify, then decide whether to align it with `054-398-2444` |
| U-024 | **Merged is not deployed, and nothing checks.** `deploy-edge-function.yml` is `workflow_dispatch` only — "Never runs on push" — so an Edge Function change lands on `main` and stays dormant until a human clicks, and nothing anywhere compares what is on `main` against what is running. The morning digest was written, migrated and cron'd on 2026-08-25 and sent nothing for six days because of this. Its own header names the same failure on the LionWheel pick bridge before it, so this is the third occurrence of one class | Tom — decide the mechanism: deploy on merge for these functions, or a check that fails when a deployed function's sha is behind `main` |
| U-025 | Inbound WhatsApp is invisible to `sales_core`. `054-398-2444` is the real order line and now also linked to the Facebook Page, but a customer who writes to it never becomes a lead row — `channel: call \| whatsapp \| email` records only how a rep reached *out*. This is also the gate on any click-to-WhatsApp advertising: an ad would drive straight into the gap | Tom + the lead-system lane |
| U-026 | Avi (`avi@gteveryday.com`) is the person actually working the lead queue — 113 events, most recent 2026-08-31 09:13 — and he does not appear in `docs/ceo/reference/people_rhythm.md` at all. No documented role, hours or backup. Separately, `app_setting('whatsapp_templates').new_lead` opens with `כאן תום` while Avi is the one sending it | Tom — add Avi to people_rhythm; fix the template signature |
| U-027 | **TikTok `@gteveryday` is GT's, live, and nobody holds the login.** Public profile JSON read 2026-08-31: bio `🍃GreenTea Essences Company🍃 / עוד לא ניסיתם את זה / gteveryday.com`, created 2023-11-04, **13 videos published**, 23 followers, 383 lifetime likes, public, `nickname` still the default `gteveryday`. It is on no plan and no credentials sheet row was ever filled. An earlier note in this session recorded the handle as *free* — that was wrong: TikTok returns HTTP 200 for non-existent handles, so the status code proved nothing. Separately `@greenteaeveryday` on TikTok belongs to an unrelated Thai account — not ours, do not contact | Tom — recover access (`info@gteveryday.com`, then password reset, then TikTok business recovery). Until then: do not rename, do not delete a video, do not open a second account |
| U-028 | `sales_core.app_setting('meta_poll')` is `enabled: false` and its `last_error` is a Graph API permission refusal — `pages_read_engagement` / Page Public Content Access missing. `last_poll_ok_at` is null: the direct Meta lead poll has **never once succeeded**. Make currently carries leads to `/ingest` instead (D-006), so the pipe works — but the Meta path was written, has never run, and nothing says whether it is meant to be revived or removed | Tom + the lead-system lane — grant the permission on the Meta app, or retire the poll and delete the setting |
| U-029 | **2,537 lapsed customers are sitting in a segment nobody has ever emailed.** Klaviyo `Win-Back Opportunities (Shopify)` = bought at least once, zero orders in 180 days, holds email consent — 2,537 profiles against a consented base of 2,969, so **85% of everyone GT may email is a customer who stopped**. The segment has been computed and active since 2026-07-18. In the same account: 0 campaigns ever sent, 0 flows, 0 sending domains. `Churn Risks` reads 0 only because its filter needs "received ≥2 emails in 90 days", which is impossible when none were sent — a structural zero, not an empirical one | Tom — this is the repo's founding problem, already quantified. Sending needs `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` + written approval, and the sending domain (`e3`) must be authenticated **first**: 2,537 dormant addresses with no DKIM is how a domain gets burned |
| U-030 | Klaviyo's account contact block sets `country: United States` while the address is `הלהב 15, חולון`. That block renders in the compliance footer of every email. Five more fields are off: `organization_name` is `GreenTeaEveryday` (neither the brand nor the legal name), `default_sender_name` is lowercase `gteveryday`, `website_url` is `http`, `industry` is null, `locale` is `en-US` against an `Asia/Jerusalem`/`ILS`/Hebrew audience | Tom — confirm each value, then fix in Klaviyo account settings. Not changed here: this is account identity |
| U-015 | Which Instagram handle is GT's, and is `@greenteaeveryday` (zero posts, follows hundreds) compromised? Both handles serve a login/challenge wall to this environment — no public data obtainable. No Instagram work happens until this is answered | Tom (§6.B) — log in, or run account recovery |
| U-016 | **CLOSED 2026-08-31 — the premise was false.** GT does hold admin; the portfolio was created by Alex Berov in 2019 and business verification passed in 2022. Original entry: GT holds no admin on its own Meta Business account. Blocks the WhatsApp green tag, business verification, the lead-form fix, CTWA, and re-authorising the connection before `2026-10-23` | Tom (§6.E) — find today's admin, or open a Meta support case |
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
  `evidence/2026-08-31-social-property-audit.md` · handle sweep
  `evidence/2026-08-31-social-handle-sweep.md` · Q4 content calendar
  `doctrine/playbooks/social-calendar-2026-Q4.md` · launch kits
  `doctrine/playbooks/linkedin-launch-kit.md`, `doctrine/playbooks/youtube-refresh-kit.md`,
  `doctrine/playbooks/tiktok-recovery-kit.md` · lead-response SOP
  `doctrine/playbooks/lead-response-sop.md` (binding only on Tom's written approval).
  Credentials sheet and the 72-row action board live in Tom's Drive, **not in this repo** —
  no secret value is ever written here (`GT — כרטיס גישה` and `GT — לוח פעולות רשתות`,
  folder `GT Everyday — נכסי מותג`). Tracker artifact: the digital roadmap, 72 tasks,
  12 done as of 2026-08-31.
- Latest evidence snapshots (both 2026-08-24): `evidence/2026-08-24-make-intake-handover.md`
  (intake hand-over to Make) · `evidence/2026-08-24-sales-report.md` (sales report).
  Previous: `evidence/2026-08-23-live-intake-bringup.md`, `evidence/2026-07-18-two-numbers.md`.
- Sales report recipe: `recipes/sales-report.md` (taxonomy + anchors Tom-approved 2026-08-24).
- Decisions log (incl. PROPOSED items awaiting Tom): `doctrine/decisions.md`.
