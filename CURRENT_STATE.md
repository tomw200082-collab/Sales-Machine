# Sales-Machine — Current State

## 2026-10-03 01:45 UTC — GT CRM settings phase 1: the lead conversation, live in production (D-042/D-044)

- **Backend (gt-factory-os #343, `53e5f43`, migration 0376):**
  - every lead and Today row carries its conversation: the automatic messages sent, the buttons tapped, the menu, opt-out, and a suggested situation;
  - `GET /api/v1/queries/sales/journey` serves the automatic journey, read-only (D-044);
  - six quick messages per situation in `app_setting` `whatsapp_quick_messages`, signed "{{rep}}, GT Everyday";
  - WhatsApp to an opted-out lead is refused (409 `SALES_LEAD_OPTED_OUT`). A rep asking about another rep's lead gets 403 and never learns whether it opted out.
- **Portal (#252, tranche 203, `394e054`):**
  - the drawer and the Today card suggest the quick message for the lead's situation, with "הודעה אחרת" to pick another;
  - opted-out leads show a disabled WhatsApp button that explains why;
  - settings show the automatic journey read-only and edit the quick messages with a live preview.
- **Gates:**
  - pgTAP 0376 11/11 and backend suites green;
  - vitest 2033/2033, tsc 0, mocked e2e 38/38, axe 0;
  - UX release gate round 2: SHIP (P0 0, P1 0; two P2 nits open: the pill gap before a comma, and the picker not marking the current choice);
  - CI green on both PRs.
- **Production smoke:**
  - the deploy run succeeded and API health returned 200;
  - the `whatsapp_quick_messages` key holds 6 situations;
  - `rebuild_verifier()` = 0;
  - signed out, the pages answer 307 and the APIs answer 401;
  - no portal runtime errors.
- **Next:** phase 2 (working-hours response time, D-043) is in build.

## 2026-10-02 23:25 UTC — GT CRM: one loader and a native sales report, live in production

- **Loader (portal #250, tranche 201, `aa7fbc5`):**
  - one continuous GT loader, with a factory variant and a sales variant;
  - the sales app is named "GT CRM".
- **Sales report (portal #251, tranche 202, `574bc92`):** `/sales/report` replaces the Artifact report inside the CRM.
  - five tabs: יומי, לקוחות, מוצרים, רשתות, מגמה;
  - managers only;
  - refreshed every 15 minutes by `sales_core.report_run`. The last run was 23:18 UTC and the data is current.
- **Gates:**
  - UX release gate round 2: SHIP (P0 0, P1 0, 5 non-blocking P2s);
  - vitest 1998/1998, tsc 0, eslint 0;
  - CI green.
- **Fixed on the way:**
  - The 320px month view fitted only one month beside the total under a wider fallback font. Month headers now wrap, so the figures set the column width.
  - A first-route-compile wait was added to the report e2e.
- **Production smoke (signed out):**
  - pages answer 307 and the APIs answer 401;
  - API health 200;
  - no portal runtime errors in the hour after;
  - `rebuild_verifier()` = 0.

## 2026-10-02 13:45 UTC — GT Pulse Unit B: closure decisions; "keep as a lead" is live

Tom answered the closure page on 2026-10-02: "מאשר הכל, אלכס הוא הבעלים של גרינטי". The decisions are D-040 (the 26 identity-review orgs) and D-041 (Ice Dream, which closes U-055).
- **Keep as a lead, live in production.** A `customer_not_verified` org can now be resolved: the manager keeps it as a lead, its Shopify account is unlinked, and no rejection is kept.
  - Backend gt-factory-os #340, squash `48b4535`, deploy run 37012414528. Pre-flight `rebuild_verifier` was 0. Health 200.
  - Portal #245 (tranche 197), squash `aedaa65`, Vercel `dpl_2Um2wQmaCpaN4HL6vMf6hE6kAHJm` READY.
  - Signed-out smoke: pages answer 307 and the APIs 401.
  - After the deploy, production still had 26 open identity tasks and `rebuild_verifier()` = 0.
- **Closure fixes, live the same day.**
  - An identity link or merge now names the holder it saw. The server refuses with `SALES_IDENTITY_HOLDER_CHANGED` if that holder changed.
  - The legacy `GET /queries/sales/orgs` is removed. It answers 404 in production.
  - The portal proxy ignores the dev-shim flag on a production deployment.
  - Shipped as backend #341 (`76b2a4a`, deploy run 37015914312) and portal #246 (tranche 198, `b03d4c2`, Vercel `dpl_Ghsx6Ck5BTQ7DSbZFbGCP7R6mwjq` READY).
  - After the deploy: drift 0, 26 open identity tasks, and no portal runtime errors in the following hour.
- **Identity review done (Tom, 2026-10-02 14:09–14:11 UTC).** All 26 tasks were closed by `tom@gteveryday.com`:
  - 18 confirmed (`resolved_by_manager`, now verified, no merges). This includes `תום בדיקת בוט WhatsApp`, which D-040 had left in review.
  - 8 kept as leads (`rejected_by_manager`, unlinked).
  - 0 open identity tasks afterwards. `rebuild_verifier()` = 0.
- **TLS.** `NODE_TLS_REJECT_UNAUTHORIZED=0` is a Vercel project variable. Both upstreams have valid certificates.
  - Portal tranche 199 (#247, #248) drops it at boot in the Node runtime, which covers the API routes.
  - The edge middleware, which calls Supabase, stays unverified until the variable is deleted in the Vercel dashboard. This session gets 403 on project env vars.
- **Still Tom's:**
  - deleting `NODE_TLS_REJECT_UNAUTHORIZED` from the Vercel project;
  - naming the `client_key` writer (U-056);
  - counsel (U-057);
  - the read-only mirror token (U-058).

## 2026-10-02 12:25 UTC — GT Pulse Unit B portal (Session 2): live in production

Verified against production on 2026-10-02.
- **Portal:** gt-factory-os-portal #244, squash `acfe2358`, Vercel production deployment `dpl_B4ykh8ZrwNVmpFdvRMWTGSk2iDXV`. It is READY and aliased to `gt-factory-os-portal.vercel.app`; the previous production deployment was `dpl_J6zstx3ZCfrcythvyR4xb9aPA8dL` on `89aa411`. Tranches 189 to 196:
  - the business list, server-paged;
  - the business workspace `/sales/orgs/[id]`;
  - the two-year business circle;
  - the managers' identity review;
  - bulk owners;
  - org search in the command palette;
  - the orders timeline (Tom: the circle's second view, redesigned at his word).
- **Backend:** gt-factory-os #339, squash `e9855e8`, adds `held_by` on identity candidates, so a merge names its destination before it happens.
  - Deployed by deploy-production run 37005367572. The only migration in that run was an idempotent re-apply of `0373`, used as the vehicle.
  - Pre-flight `rebuild_verifier()` was 0. After the run, exactly one `sales_shopify_mirror_refresh` job remains (`40 0 * * *`, active) and `rebuild_verifier()` is 0. Health is OK.
- **Checks on the released head:**
  - vitest 1737/1737, typecheck 0, eslint 0 errors, `next build` green.
  - Playwright `@mocked` 150/150, including the Unit B journeys, a 320 to 1440 matrix, dark mode with reduced motion, and a touch phone.
  - CI `portal-pr-guard` green.
- **UX release gate** (sales profile, strict): four rounds, from P0 2 / P1 23 to **P0 0 / P1 0**, verdict SHIP. The record is in the brain repo, `docs/phase8/dry-runs/gt-pulse-b-ux/`. An independent code review found no Critical issue; its three Important findings were fixed red-first. `/simplify` and ponytail-review were applied.
- **Production smoke, signed out:**
  - every new page redirects to login;
  - every new proxy route answers 401;
  - the API refuses its org routes without auth (401);
  - no runtime errors in the following hour.
- **Not yet observed:**
  - an authenticated read through the portal. There was no user session in this session, and none was faked.
  - the first scheduled mirror refresh (00:40 UTC, 2026-10-03).
  - a WebKit or real iPhone run. Touch was tested with Chromium touch emulation only.
- **Known limits:**
  - 8 review orgs (`customer_not_verified`) cannot be resolved from the portal: the held customer is not in the mirror, and resolving them needs a backend change.
  - The merge-target check is advisory. A server-side expected-holder check (409) is a backend follow-up.
  - The legacy backend `/orgs` route still exists; the portal no longer calls it.
- **Still Tom's:**
  - the 26 identity-review decisions, now on the screen;
  - Ice Dream (U-055);
  - his security actions (U-058);
  - the read-only mirror token.

  No real identity decision, outreach, automation or Shopify, Green Invoice or LionWheel write was made.

## 2026-10-02 08:05 UTC — GT Pulse Unit B backend (Session 1): live in production; Portal/UI is Session 2

Everything below was verified against production on 2026-10-02. Tom approved the edge-function deploy and the exact backfill (count and digest) in the session; the migrations and the merge followed the approved W6 order.
- **Accepted code:** backend `main` `893b3701` (squash of gt-factory-os #338, PR-4 + PR-5 + the review corrections; its tree is identical to the reviewed head `7f9bbcaf`, sales-db and typecheck green on it). Earlier: PR-1 to PR-3b (#331 and following).
- **Review:** three independent read-only reviews (database, API, edge functions), no Critical finding; the Important ones were fixed red-first (new leads could attach to a retired merged org; a rep saw contacts from another rep's lead; skill text promised a link the identity layer does not make). Interpretations I27 to I46 are listed in #338.
- **Edge functions** from `7f9bbcaf`: `sales-leads-poll` v31, `sales-sleeping-radar` v2 (`verify_jwt` on). The radar's `run` answers 401 to the anon key and to a forged unsigned `role:service_role` token and works with the service-role key (17 orgs, no error); `health` stays open and returns booleans only. No lead event, no message sent since the deploy.
- **Backfill** (run `d8153a6f-d3ac-4f7c-b33c-1d6832ddbeca`): count 23,470, digest `ff40a7e9b5908c0f0cd0f981c0e3ff52`, applied on Tom's go. 1,093 customers (1,075 verified, 18 in review), 21,618 orders and drafts (10,748 and 10,870), 81,052 lines, 996 phones, 338 chain members, 391 contacts (none verified); 1,084 orgs created, 8 existing orgs verified, 9 sent to review, none merged or disputed; 1,329 orgs, 26 in identity review with 26 open manager tasks. Order coverage difference 0 for orders and drafts; 2,156 customers without a client key were not stored. The dry-run forecast of automatic lead conversions was 0 (186 open leads; 4 sit on orgs that became verified).
- **First real reconcile:** pass (run `70ae1572-bd53-4940-9844-5ddd0d9831df`, 07:44:59 to 07:47:20 UTC): 1,093 customers compared, 0 mismatched; 10,748 money checks, 0 unmatched, 0 unexplained; month gate mismatches 0; ShopifyQL coverage 570 verified of 588 active customers. History is published; review, disputed and unlinked orgs expose nothing from Shopify.
- **M2 (`0372`)** applied 07:50 UTC (deploy-production run 36980625660): the 16 production objects it touches are byte-identical to the repo's file; the guard trigger refuses a direct status update, a direct id update and an insert carrying an id (probed in production inside a rolled-back block); every existing customer (1,075) holds a verified link; the radar batch is the 8 verified orgs with a lead.
- **M3 (`0373`)** applied 07:54 UTC (run 36980984687): one job, `sales_shopify_mirror_refresh`, `40 0 * * *`, active, token read from the vault at run time, no other job at that slot.
- **Backend API** deployed to Railway from `893b3701` in the same run; the new org routes are live and all 13 refuse an unauthenticated call (401) and the public anon JWT. `rebuild_verifier()` was 0 before and after every step.
- **Not yet observed (operational):** the first scheduled refresh and its reconcile (00:40 UTC on 2026-10-03, then each night). An authenticated read of the new routes through the portal was not exercised in this session (no portal user session). The mirror still runs on `SHOPIFY_ADMIN_API_TOKEN` (its scopes passed the reconcile); the dedicated read-only `SALES_MIRROR_SHOPIFY_TOKEN` is still Tom's.
- **Boundary:** the Unit B portal (tranches 189 to 191, UX gate) is Session 2. No portal change shipped, committed or pushed. A first tranche-189 draft existed only as a local, unverified git stash of that session's ephemeral container; Session 2 starts from portal `main`, the approved round-1 strings and the build plan, and treats the draft as gone. Unit A and D1 are unchanged.
- **Still Tom's:** the Hebrew string for a forbidden state (none was approved), the 26 identity-review decisions once the screen exists, his security actions (U-058), Ice Dream (U-055).

## 2026-10-01 — GT Pulse Unit B: ground truth closed, spec v2 approved, build starts

Tom approved on 2026-10-01 ("מאשר הכל") the red-team summary: T1–T12, then spec v2, a build plan and an autonomous backend build; the Hebrew UI starts only after he approves mockups and string round 1. Decisions D-035 to D-038.
- **W0 ground truth, done (D1):** the GT Pulse docs are on `main` and the two docs branches are ancestors of `main` (Sales-Machine #38 and #40, brain #242 and #243). Migrations `0353` and `0354` are on backend `main` (#333); a CI run on a database built from `main` matched production's column and grant hashes for the four objects (run 36883627787). The sales database gate runs on every PR touching `db/`, the sales API or order-intake (#331); with one assertion broken it went red (run 36874266028).
- **Spec:** `docs/superpowers/specs/2026-10-01-gt-pulse-b-design.md` (v2), glossary `CONTEXT.md`, ADRs `docs/adr/0001` and `0002`. Six independent reviewers attacked v1 first.
- **Build plan:** `docs/superpowers/plans/2026-10-01-gt-pulse-b-build.md` — 30 tasks in six backend and portal PRs. First PR: the CI gate (pinned skips and failures, idempotency check, every sales API test). Mockups and string round 1 run in parallel; the portal starts only after Tom approves them.
- **Still Tom's:** the backfill go on exact counts and digest; one batch of Hebrew strings with mockups; the visual approval; his security actions (U-058); how Ice Dream orders will appear in Shopify (U-055).
- **Not built yet:** anything of Unit B. Unit A and D1 are unchanged in production.

## 2026-10-01 13:20 UTC — copy round live (tranche 188): the five UX-gate copy decisions

Tom approved the round on 2026-10-01 ("מאשר הכל").
- **Code:** portal [#243](https://github.com/tomw200082-collab/gt-factory-os-portal/pull/243) was squash-merged as `89aa411`; `ci` was green.
- **Deploy:** Vercel `dpl_J6zstx3ZCfrcythvyR4xb9aPA8dL` is READY in production. Rollback: `dpl_8Nw7a1xL8N1AvtxNdkUzD1MUz5y2`.
- **Now live:**
  - The flow caption reads "כל הלידים".
  - The org list shows "טרם לקוח".
  - The lead card says "כתבו הערה כדי לשמור" when Save is disabled.
  - The customer status ("פעיל"/"לא פעיל") is in the register.
  - The nav landmarks are named "ניווט ראשי" and "סרגל ניווט".
- **Open copy items from the gate:** none.
- **Still not proven:** WebKit/iOS and screen-reader behaviour on a real device.
- **Next:** a planning checkpoint with Tom, then the unit B masterprompt in a new session.

## 2026-10-01 12:40 UTC — D1 corridor-wide live (tranche 187): every sales screen at the D1 level

- **Code:** portal [#242](https://github.com/tomw200082-collab/gt-factory-os-portal/pull/242) was squash-merged as `e9179d2`; `ci` was green. Vercel `dpl_8Nw7a1xL8N1AvtxNdkUzD1MUz5y2` is READY in production. `/login` returns 200, and `/sales/*` redirects to login (307). Rollback: `dpl_8fK9NzguyAvny47Pf2Meyaputhze`.
- **What changed:** a glass app bar; a floating tab bar; a round FAB on phones; a petrol band on every screen; the mini rail on lead list cards; the org card in the lead card's frame; settings, feed and states in panels. The note save now has an "in flight" ring on every save, and lost on /attention has an undo. The toast sits above the lead card, where the undo had been unreachable.
- **Copy (Tom approved 2026-10-01):** "כל הצוות" and "נשמר ✓" are live. "כל הלידים הפתוחים" is registered but not rendered (its meaning is wrong for the order node); the flow caption shows "לידים".
- **UX gate (sales profile):** **CONDITIONAL_SHIP**, 0 P0 ([report](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-10-01-gt-pulse-d1-corridor-ux-gate.md)).
- **Waiting for Tom:** resolved by the 13:20 UTC copy round (tranche 188).
- **Not proven:** WebKit/iOS and screen reader on a real device.

## 2026-10-01 10:40 UTC — D1 follow-up live: lead card redesign, no sideways scroll, simplify + UX gate

- **Code:** portal [#241](https://github.com/tomw200082-collab/gt-factory-os-portal/pull/241) was squash-merged as `49435b1`; `ci` was green on head `09a0d17`. Vercel `dpl_8fK9NzguyAvny47Pf2Meyaputhze` is READY in production with no runtime errors. Rollback: `dpl_31zwFtmuoYe3vWsJD2wKUTJQTUvu`.
- **Lead card:** long values no longer push it sideways. A regression e2e at 320/390/430 fails on the old code and passes on the new. The card also has a petrol header with the mini rail, icons, panels, and a history line, with the note above the details.
- **Gates:** the simplify pass (4 lenses) and an independent correctness review ran and their fixes landed. The UX release gate ran with the sales profile and returned **CONDITIONAL_SHIP**, 0 P0 ([report](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-10-01-gt-pulse-d1-ux-gate.md)).
- **Open:**
  - The copy HOLDs need Tom's approval: FLOW-001 (a label for the flow population), FLOW-003 (a "saved" confirmation for notes), FLOW-004 (a team label on the counts).
  - Next tranche: D1 treatment for leads, attention, orgs and settings.
  - The FAB overlap existed before D1.

## 2026-10-01 09:20 UTC — GT Pulse D1 (visual, phase 1) is live in production (Tom approved)

Tom gave the full production go after seeing the iteration-2 video ("יש לך את הgo המלא לפרודקשן").
- **Code:** portal [#240](https://github.com/tomw200082-collab/gt-factory-os-portal/pull/240) was squash-merged as `e6d7e7f`; `ci` was green on head `933d442` (127/127 mocked e2e).
- **Deploy:** Vercel `dpl_31zwFtmuoYe3vWsJD2wKUTJQTUvu` is READY in production, built from that SHA. No new runtime errors.
- **Rollback:** Vercel instant rollback to `dpl_CcCQwinFQVn6GNVmbfWvzh2Hyksx`.
- **What shipped:** the live lead-journey flow on Today, the petrol aurora band, the shape lock and motion with a reduced-motion fallback. Spec: [D1 design](docs/superpowers/specs/2026-10-01-gt-pulse-d1-visual-design.md), V1–V12.
- **Scope:** presentation only — no backend change, no new copy, no flag.
- **Not yet proven:** the live screen with real data under a real login. This session cannot log in to production.
- **Next:** D phase 2 (contact compass, event river, basket map) needs units B and C.

## 2026-10-01 08:10 UTC — Unit A backlog backfill applied

Tom gave the count-specific go ("מאשר הכל", in direct reply to 184 / `23175e69…`). The script's guards were applied in one transaction through the Supabase connector, because psql has no network route from the session container:
- task table lock and per-lead locks
- re-check of total and digest (184 / `23175e69b922d1c7861478b90271799d`, matched)
- insert with `created_by='system:gt-pulse-backfill'`, no partial insert

Result: 184 open `bootstrap:` tasks, `rebuild_verifier()=0`:
- 146 `contact_first` in the manager queue
- 37 `call` for one owner
- 1 `call` in the manager queue

No message was sent.

**Rollback if ever needed:** cancel the open `source_key like 'bootstrap:%'` tasks with an actor and a reason. Never delete them.

## 2026-10-01 08:00 UTC — GT Pulse Unit A is live in production (Tom approved)

Tom approved production ("אני מאשר הכל"), after "קודם A ואז D שלב 1".

**What went live:**
- **Migration 0362:** applied via `deploy-production` run 36830904172 on `9d423c1`. `rebuild_verifier()=0`. Tables, functions and the reply index are present. `activity_required` is false.
- **Backend:** #329 squash-merged as `30759a2`. Railway deployment SUCCESS at that SHA, `/health` ok, `/queries/sales/tasks` returns 401 without auth.
- **Portal:** #239 squash-merged as `eb36b83`. Vercel production `dpl_CcCQwinFQVn6GNVmbfWvzh2Hyksx` is READY. The signed-out deep link keeps its destination through login.

**Backlog backfill:** not applied. The production preview found 184 tasks, digest `23175e69b922d1c7861478b90271799d`:
- 146 `contact_first` in the manager queue
- 37 `call` for one owner
- 1 `call` in the manager queue

Applying it needs Tom's count-specific go.

**Still open:**
- WebKit/iOS check on a real phone.
- The outreach flag stays `true`; it was not touched.
- Next: a D phase 1 spec.

## 2026-10-01 07:40 UTC — B-FLOW-04 closed

Tom approved the disabled-Save string ("אני מאשר"). It is registered in tranche 185 and shipped in portal `4b94597`. The only open gate is now WebKit/iOS keyboard proof, which needs a real device in the production session. Status remains **LIVE — HOLD**. There was no redesign beyond the verified UX-gate fixes; that would be a separate scope.

## 2026-10-01 07:10 UTC — pre-production session result: LIVE — HOLD

The pre-production masterprompt was executed. Tom approved the Q1–Q9 recommendations and delegated the remaining design decisions. The decisions are recorded as D1–D13 in [the closure spec](docs/superpowers/specs/2026-10-01-gt-pulse-a-preprod-closure-design.md), with the [plan](docs/superpowers/plans/2026-10-01-gt-pulse-a-preprod-closure.md).

**Final heads**
- Backend [#329](https://github.com/tomw200082-collab/gt-factory-os/pull/329) `9d423c1`: `sales-db`, `staff-mail` and `typecheck` green.
- Portal [#239](https://github.com/tomw200082-collab/gt-factory-os-portal/pull/239) `a7ccffd`: `ci` green.
- Both are drafts, mergeable clean, and 0 commits behind `main`.

**What changed**
- Rep read scope covers leads, timeline, orgs and the activity feed.
- A reply on the order line routes one reply task. There is at most one open reply per lead, enforced by a partial unique index.
- Contact resolution follows the owner, and a rep can resolve their own contact gap.
- A retry from another entry point replays the original activity.
- Every scheduling date starts at the first date whose 09:00 Israel time is still ahead.
- UX gate repairs added no new copy.

**Proof on the final heads**
- pgTAP 0362: 88/88, plus all neighbouring files.
- order-intake: 267/267. API: 14/14, 14/14, 38/38.
- Portal unit: 1536/1536.
- Connected isolated staging: 22/22 at 390px and 22/22 at 1280px. The stack is local GoTrue with ES256, the production portal build, the real API and a DB built from `db/migrations`, with synthetic identities only.
- Governor: fixture gate SHIP, connected audit CONDITIONAL_SHIP, 0 P0.
- Details: [release packet](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-10-01-gt-pulse-a-release-packet.md).

**Why HOLD rather than READY**
1. WebKit/iOS keyboard-open save cannot be proven here; only Chromium is available.
2. UX finding B-FLOW-04 (P1) stays open until Tom approves one Hebrew string. A disabled Save currently shows its cause only as a red field border.

**Production observation, untouched**
- Railway has `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED=true`, and 4 real `first_menu` sends exist, the last at 2026-09-30 14:32 UTC. Tom decided on 2026-10-01 to keep it on; the line below is corrected.
- The production API deployment carries no commit SHA.

No production merge, deploy, migration, flag change, backfill or customer message happened in this session. The local staging stack lived only in the session container.

## 2026-09-30 16:05 UTC — superseding pre-production handoff

Tom deferred production and asked for a fresh Claude Code product-discovery/build session. The new [pre-production masterprompt](docs/plans/2026-09-30-gt-pulse-preproduction-claude-code-masterprompt.md) orders Caveman/Ponytail, Grill with Docs plus domain modeling, Brainstorm, plan approval, Anthropic frontend-design and UI/UX Pro Max, connected five-lens UX release gate with P0/P1 repair and rerun, /simplify, whole-branch code review, then exact-final-head verification-before-completion. The nine built tasks remain the baseline; any new design needs his approval.

Backend [draft PR #329](https://github.com/tomw200082-collab/gt-factory-os/pull/329) at `ff69e3cecc0ffcd522c69eeb09255adcf98e51f4` passed [PR typecheck](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36740413352). Portal [draft PR #239](https://github.com/tomw200082-collab/gt-factory-os-portal/pull/239) at `1ba2c98bcf8aad63b5d81b3fb1113dbe91439093` (runtime tree from `a2e1786`, later copy-assent documentation) passed [portal-pr-guard](https://github.com/tomw200082-collab/gt-factory-os-portal/actions/runs/36740472210). Tom authorized temporary watching of these two PRs. Tranche 185 now records his exact assent to the sixteen later Hebrew strings. New copy still needs its own authority.

The second cost-approved temporary Supabase branch in the **existing** project failed with `MIGRATIONS_FAILED`. Its earliest concrete replay error at 15:51:31 UTC was `relation "private_core.supplier_items" does not exist` in `0090_readiness_view_pack_conversion_fix`; migration history and sales schema were empty. The branch was deleted and absence verified. See the [connected staging attempt](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-connected-staging-attempt.md). No paid branch remains, and no production merge, migration, deploy, flag, backfill or outreach occurred.

**Current HOLD:** connected staff Auth→browser→API→DB and WebKit keyboard proof, full connected UX gate, final-head review/verification and later production decision. PR CI passing does not close those gates. Earlier dated paragraphs below preserve their historical observations; superseded claims that copy assent, draft PRs or the PR guard are pending do not describe the current state.

> Sole authority on build status and open unknowns. Volatile by design.
> Last updated: 2026-09-30 15:35 UTC — GT Pulse Unit A exact review branches prepared; release HOLD; Tom explicitly deferred production deployment.
> Before that, 2026-09-28 — Tom approved the lead journey's texts (U-051 closed; D-033, D-034); the lead line's delivery (U-050) is his next step.
> Before that, 2026-09-02 — the knowledge-book pass added the 48 recipes and the
> seasonality measurement, and opened `U-037`.
> Before that, 2026-08-31: two sessions landed the same day — the knowledge-book pass
> (`U-014`…`U-021`, `CL-1`…`CL-4`) and the social-property pass (`U-014`…`U-032`).
> **⚠ Their numbering collides — see `COLLISION` at the top of the UNRESOLVED table.**
> New findings are numbered from `U-037` up — above **both** sets (the social-property
> pass reaches `U-036`) — so the open collision does not grow while Tom arbitrates it.

## Build ladder status

### GT Pulse Unit A — 2026-09-30 15:35 UTC release preparation update

Backend branch now `ff69e3cecc0ffcd522c69eeb09255adcf98e51f4`, reconciled with newer production `main` and verified by [exact-head CI 36737309399](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36737309399): 0362 pgTAP 79/79, two-connection/lead DB 19/19, role/activity API 11/11, legacy workspace 14/14, staff mail 38/38, root typecheck and guarded disposable backfill. A RED→GREEN review fix removed a journey result's unproven task-creation claim. Portal branch remains `a2e1786c33fc8b257240d7076113222ec8a80028`; fresh local typecheck, ESLint and build exited 0, unit tests 1,525/1,525. Fresh Playwright could not start the dev server in this sandbox (`uv_interface_addresses`), so earlier 58/58 mocked browser checks remain dated evidence, not connected proof.

Tom wants this prepared up to a release decision and **does not authorize full production deployment now**. Existing Supabase project and existing portal are the targets; standalone project suggestion withdrawn. A new isolated branch in the existing project costs $0.01344/hour and has not been created without cost-specific consent. The prior branch failed migration replay; a working connected API/real Auth/DB staging run remains unproven. Later Hebrew copy entries still need exact register assent. PR creation would subscribe this session and the connector cannot unsubscribe, so no PR or PR-triggered portal guard exists. Read-only production at 15:17 UTC: 260 leads, 184 open, 147 open unassigned; `sales_core.task`, migration 0362 and `activity_required` absent. No post-schema backfill preview or batch authorization. **LIVE — HOLD**; the 08:25 snapshot below is historical.

### GT Pulse Unit A — 2026-09-30 final branch checkpoint

Backend review branch `feat/gt-pulse-a-sales-contact-loop` at `42b560422cd327533135333b12390994a39304c9`; portal review branch `feat/gt-pulse-a-sales-corridor` at `a2e1786c33fc8b257240d7076113222ec8a80028`. Backend [exact-SHA CI 36688872012](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36688872012) passed both jobs: disposable 0362 pgTAP 79/79, two-connection lead/wake 19/19 (including lost undo), role/activity API 11/11, legacy workspace 14/14, staff mail 38/38, root typecheck and guarded synthetic backfill checks. Portal local final-source verification: 1,525/1,525 unit, 58/58 sales mocked Chromium, 126/126 full mocked Chromium with zero skipped/unexpected/flaky, build, typecheck and lint (0 errors, 558 warnings). A fresh synthetic 40-cell role/route/width matrix had zero horizontal overflow or missing headings. Independent whole-branch reviews cleared all Important/Critical findings; `/simplify` was unavailable, so a labelled ponytail cut removed one redundant date wrapper. [Five-lens follow-up](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-sales-ux-gate-final-followup.md) remains HOLD: connected authenticated API/DB, true WebKit keyboard-open save and the actual PR guard were not proven.

Read-only production SQL at **2026-09-30 08:25:25 UTC**: 259 leads, 183 open, 148 open unassigned; `sales_core.task` absent, migration-history 0362 zero, `activity_required` absent. These are dated live counts, **not** a post-schema guarded backfill preview. The Vercel final-SHA deployment is READY with `target=null` (branch preview only). Vercel production deployment `dpl_CuXtU3i8wc1Rb3NzyPMU1Sn5MWqL` is READY at default-branch SHA `5e45b2d91cc8938ec1945925e46f481b9146c404`, separate from the final branch preview. Railway production API deployment `f285afb2-1a71-4f35-b625-4528cbeea043` is SUCCESS, but metadata gives no source SHA. `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` appears by name in redacted Railway variables; its value remains unverified. No migration, flag change, mass task insertion, customer send or production deploy occurred. The original exact Hebrew register table had contextual assent recorded in tranche 185; newly introduced exact strings are proposed there and await separate register assent. Tom approved the quoted $0.01344/hour Supabase development branch. It was created at 09:04 UTC, returned `MIGRATIONS_FAILED` with no `sales_core` schema or migration history, then was deleted and absent from the next branch listing. This did not prove authenticated route→API→DB. A future paid resource would need its own cost boundary; the eventual production task batch still requires a separate count/digest approval. No PR was opened because an immediate unsubscribe capability was unavailable under the no-autowatch rule. The detailed [execution index](docs/plans/2026-09-30-gt-pulse-a-execution-index.md), [staging attempt](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-connected-staging-attempt.md) and [release check](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-release-check-final-followup.md) record gates and rollback. Status remains **LIVE — HOLD**.

### Earlier 2026-09-30 checkpoint (superseded by final branch checkpoint)

Backend review branch `feat/gt-pulse-a-sales-contact-loop` remote `fa9c0454dd0856594678448c750fa22b09e58f29`; portal review branch `feat/gt-pulse-a-sales-corridor` remote `103354bdce2e93cc4b19232dadc46745640d3ffb`. Local worktree heads have identical Git trees. Migration 0362 and portal tranche 185 exist **on branches only**. Backend [push CI 36676625217](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36676625217) succeeded on the exact backend tree: sales pgTAP through assertion 68, guarded staging backfill and idempotence, two-connection wake/lead DB 18/18, role/activity API 11/11, legacy 14/14, staff alert 38/38 and root typecheck. A synthetic browser matrix covered 40 route/role/width combinations with no horizontal overflow, and the final portal head passed 57/57 relevant sales Chromium cases, 125/125 whole-portal `@mocked` Chromium cases by JSON reporter, and 1,517/1,517 unit tests; build, typecheck and lint also passed locally (lint had 558 warnings, zero errors). Two independent code reviewers found and rechecked Important defects, including a same-display-name request collision proved RED before the final fix; no remaining Important code finding was reported. The five-lens self-audit is saved under the brain's `docs/phase8/dry-runs/`; it is **HOLD**, not a live release gate pass.

Read-only production SQL on 2026-09-30 counted **257 leads, 183 open, 150 open unassigned**; `sales_core.task` is absent, migration-history version 0362 count is zero and `activity_required` has no row. A provisional pre-schema candidate breakdown was 148 unassigned first-contact, 2 unassigned call and 33 owned call tasks. This is **not** the guarded post-schema batch preview: new events can make tasks before the script runs. Exact backend/portal deployed SHAs and the frozen outreach environment flag are unverified; no production task backfill, flag change, customer send or outreach activation occurred in this execution. Final backend disposable-PostgreSQL CI is green, but authenticated browser→API→DB staging proof and production runtime checks remain unavailable. The exact new Hebrew copy register entry in portal tranche 185 awaits Tom's approval; the production backlog batch requires a separate count-specific written go/no-go after a real post-schema preview. Detailed per-task evidence and rollback boundaries: `docs/plans/2026-09-30-gt-pulse-a-execution-index.md`. Preserve `LIVE`/HOLD until these gates and exact deployed SHA/flag checks pass.

| Phase | Scope | Status |
|---|---|---|
| 0 — Constitution | CLAUDE.md truth rules, structure, boundaries | **DRAFT LANDED** — awaiting Tom's written approval |
| 1 — Seed verified knowledge | research findings, evidence snapshot, recipes | **LANDED** |
| 1b — Knowledge layer | ספר העבודה as graded, dated, machine-readable cards under `knowledge/` (products · drinks · answers · boundaries · claims · segments · eval) + reconciler | **LANDED** 2026-08-31 — cards validate 0/0; 9 findings open on Tom (below) |
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
`SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` is **`true` in production, and stays so by Tom's decision of 2026-10-01** ("להשאיר פתוח"). Every other gate on a customer-facing send still applies.

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
| U-011 | **Re-measured live 2026-08-31: 200 leads — 142 `new`, 12 `working`, 3 `won`, 43 `lost`, and 188 with no assignee.** So the queue is being worked (Avi, 113 events) but almost nothing is owned. Tom decided 2026-08-31: he is primary, Avi and Alex take the large ones; the 142 untouched stay for a planned personal bulk outreach rather than being closed. Original entry: the Today queue currently holds all 188 leads, because every imported lead is genuinely untouched and past SLA. Honest, but a queue the size of the whole table is not "call these two, follow up on these three". Work the backlog down, or cap the daily queue? | Tom — product decision, deliberately not taken during the build **Costed 2026-08-31 (lead-response pass):** at the configured `queue.daily_cap = 15` the pile is **7 working days for the recent tier, 10 for all of it**. Triage published as `api_read.v_sales_backlog_triage` (gt-factory-os migration 0341); no lead's status was changed — a mass re-state stays Tom's. | Tom — product decision, deliberately not taken during the build |
| U-012 | Erik's role and how leads get assigned. The schema and the queue already scope per assignee (`assignee = me OR unassigned`, admins see all); only the UI to assign at scale is missing | Tom, when a second person joins |
| U-013 | Should the Facebook form ask for a business name again? The live form is two questions (name, phone, email), so an incoming lead is close to anonymous and the org has to be inferred | Tom + Alex — marketing decision with a direct data consequence |
| **COLLISION** | ⚠️ **`U-014` … `U-021` are allocated twice, to different questions.** Two sessions ran in parallel on 2026-08-31 and each numbered from the same free slot: the knowledge-book pass took `U-014`…`U-021` for the agent's asset and boundary gaps (Hebrew rows below), and the social-property pass took `U-014`…`U-032` for the ownership audit (English rows below). **Both sets are real and neither is dropped.** They are not renumbered here: `CURRENT_STATE.md` is the sole authority on this list, the IDs are already cited across playbooks, two PR bodies, the tracker artifact and the Drive action board, and a unilateral renumber by one of the two sessions would break the other's references silently. Read every `U-0xx` below **with its row**, never by number alone, until this is settled | **Tom — arbitrate.** Cheapest fix: keep the knowledge-book numbering (it reached `main` first) and re-prefix the social-property set, then sweep its references in one pass |

### Knowledge-book pass (reached `main` first — `#24`, `#25`)

| ID | Question | Route |
|---|---|---|
| ~~U-014~~ | **נסגר 2026-08-31.** ארבעת ה-300 מ״ל — טום: "לא להציע בכלל, זה היה רק להזמנה ספציפית" (הזמנת מימי ואזה). `customer_facing: false`, ⊥ מוזכרים ביוזמתנו | — |
| U-015 (→ אלכס §5) | **חצי נסגר 2026-09-02.** ✅ **עונתיות — נמדדה** (`evidence/2026-09-02-seasonality.md`): החורף רץ ב-75–89% מהזמנות הקיץ שלפניו, ושתי עונות חורף נמדדו. `answers#seasonality` עבר מ-`העברה` ל-`טיוטה` עם נוסח מהמדידה. ⛔ **עדיין פתוח:** תסריט למלון / קייטרינג / משרד — קהלים ש-`gt-acquisition-os` מגדיר כיעד ואין להם נוסח | הנוסח → אישור טום/אלכס · התסריט → החלטת טום |
| U-016 (→ אלכס §4) | מה קורה אחרי ההזמנה הראשונה: מדיניות החזרה/החלפה כשמשקה לא נמכר · מה עושים כשמוצר חסר · תדירות הזמנה חוזרת ומי מתקשר. אין מדיניות מוצהרת בשום קובץ. הראיה מ-2026-08-24 מראה 0 refunds ב-25 חודשים (GT מבטלת, ⊥ מזכה) — התנהגות היסטורית, ⊥ מדיניות | טום + אלכסנדר |
| U-017 (→ אלכס §6) | בנק התשובות חי ב-`knowledge/answers/answer-bank.yaml` (30 שורות). הגיליון שמערכת הלידים אמורה לקרוא ממנו — ⊥ נבנה, וכיוון הסנכרון ⊥ סוכם עם סשן מערכת הלידים. שני בנקים = כישלון D3 | תיאום בין-סשן + טום |
| ~~U-018~~ | **נסגר 2026-08-31.** כשרות וחיי מדף — טום: "אין מסמכים, אני מאשר את שניהם כעובדה". מדורגים `user_confirmed`. בקשת תעודה מלקוח עוברת לאלכסנדר, כי אין מה לשלוח | — |
| ~~U-019~~ | **נסגר 2026-08-31.** ארבע רשומות-השלילה נשארות פעילות בשופיפיי (טום: "תשאיר"). כלומר: ⊥ במחירון הלקוחות ו⊥ מוצעות בשיחה, אבל לקוח שמגיע לחנות יכול להזמין. זו הכרעה, ⊥ פער | — |
| U-020 | תיקיית `05 · מה שולחים ללקוח` ריקה. ✅ **המתכונים נסגרו 2026-09-02** — `knowledge/drinks/recipes.yaml`, 48/48, מנות מאושרות שנבדקו מול העלות + שיטת הגשה, מרונדרים ל-`03 · מתכונים`. ⛔ **עדיין חסר:** קטלוג המשקאות בתוקף (PDF) · מחירון ללקוח (PDF) · סרטוני ההדרכה שהספר מבטיח · תעודת כשרות | **טום — בתהליך.** הצהיר 2026-08-31 שיעלה חומרים שיווקיים ל-`06 · העלאות` |
| U-021 | 17 מתוך 17 כללי `boundaries/refusals.yaml` מסתיימים ב"מעביר לאלכסנדר" — ו**אין בשום קובץ מספר, מייל או קבוצה**. סוכן ווצאפ שיגיע לכלל כזה נעצר באמצע שיחה בלי מסלול המשך | טום — פרט קשר אחד, ואז כרטיס `user_confirmed` |
| U-037 | **אפריל 2026: ₪146,254 על 271 הזמנות** — החודש החלש ביותר ב-25 חודשים בהכנסה, אבל ⊥ במספר ההזמנות (מרץ 221, מאי 322). ה-AOV נפל מ-~₪1,400 ל-~₪540 לחודש אחד ואז חזר. זו ⊥ עונתיות — או זיכויים/ביטולים גדולים שנרשמו באותו חודש, או פער נתונים. התגלה אגב מדידת העונתיות 2026-09-02. **ממוספר U-037 בכוונה** — U-022 *וגם* U-033 כבר תפוסים ע"י מעבר נכסי הרשת, ש-U-036 הוא המספר הגבוה בו. ההתנגשות הפתוחה ⊥ אמורה לגדול | בדיקה מול Green Invoice / דוח הזמנות אפריל |
| **RENUMBERED** | The ten rows below arrived as `U-022`…`U-031` from the 2026-08-31 lead-response pass. They are re-prefixed to `U-040`…`U-049` here, above both colliding sets and above `U-039`, main's current highest, because the social-property pass reached `main` first and already holds `U-022`…`U-039` — the same rule this file states at the top. No row was dropped, merged or reworded in the move; only the number changed. | — |
| U-040 | 275 distinct phone numbers have written to GT's live WhatsApp since 2026-06-28 (163 in the last 30 days) and are classified `ignored_unknown_or_disabled`; essentially none exists in `sales_core` (1 of 275). How many are leads rather than unmapped customers, suppliers or staff? No identification layer exists to answer it. Shape argues most are not enquiries (avg 20.8 messages/sender; 117 conversations span >7 days); the lead-shaped floor is the 36 single-message senders, 11 of them in the last 30 days | build the first-message write (architecture doc §Q2), then measure for 30 days |
| ~~U-041~~ | **CLOSED 2026-08-31** — Israel marketing template **$0.0353**/message (rate card effective 2026-07-01), graded `doc_confirmed` from a dated DOI-registered mirror, not from GT's console. Operating cost at current volume: **$2.78–$3.39/month**. Not a constraint. `doctrine/commercial-terms.md` §3.1 | closed; re-check after Meta's next quarterly card (~2026-10-01) |
| U-042 | `META_PAGE_ACCESS_TOKEN` carries no Leads Access on the page — the cause of two real leads rejected on 2026-08-24 (leadgen `1807021066847822`, `1469012341930658`), recoverable from Meta only until **2026-11-22**. Distinct from D-006: Make carries the lead, this token fetches its content | technical — next intake session |
| U-043 | A second Facebook form id, `1771287887148857`, appears in `lead_reject` but the pulse reports `forms_visible: 1`. Live form or stale test form? | Tom + Alex, via Meta Ads Manager |
| ~~U-044~~ | **WITHDRAWN 2026-08-31** — not an open question. Tom decided the opening menu's price is deliberately never stated (D-018); it is a transfer row by design | closed |
| ~~U-045~~ | **CLOSED 2026-08-31** — the order cutoff is **14:00** (Tom). Worth six days to a north/south customer, one to three in the centre | closed |
| ~~U-046~~ | **CLOSED 2026-08-31** — derived from 1,555 completed LionWheel deliveries: צפון=שלישי · דרום=רביעי (**including Jerusalem and the Shfela**) · מרכז=ראשון/שני/חמישי. `doctrine/commercial-terms.md` §3 | closed |
| U-047 | The deck's margin percentages (77–87 %) imply the food cost arithmetically, which D-018 says is never stated. Do the margin figures stay? | Tom |
| ~~U-048~~ | **CLOSED 2026-08-31** — owner named: **Tom** (D-023). The number **is** in use, and that is not a blocker: **coexistence** keeps it in the WhatsApp app while the Cloud API rides alongside, exactly as GT's order line has since 2026-06-26 (9,440 staff-echo events prove it). The artifact's warning that a number entering the API leaves the app permanently is true of classic onboarding, **not** of coexistence. Standing requirement: the app must be opened at least once every 13 days and never uninstalled, or coexistence lapses — needs a named owner | closed |
| U-049 | Opt-out must be recorded on the lead and must cancel every queued follow-up (D-024). No column, no event type and no scheduler exists yet — this is a build item, not a question | build, before any follow-up runs |

### WhatsApp lead journey (2026-09-28 — D-027…D-032, `doctrine/playbooks/whatsapp-lead-journey.md`)

| ID | Question | Route |
|---|---|---|
| U-050 | **The lead line has never delivered a message to GT's webhook.** `wa_event_log` holds 0 events for `phone_number_id 217553368116155`, ever, against 2,376 on the order line in the 24 h before 2026-09-28 19:00 UTC (re-measured). Two causes are possible on the provider's side (no routing for the number, or coexistence lapsed, D-023) and one on GT's: production authenticates webhooks by WABA id and dropped every entry from another WABA before logging it, so a lead number on its own WABA would vanish. That one is fixed in `gt-factory-os#321` (`WA_LEAD_WABA_ID`), and the route's `health` action reads the number's WABA and coexistence state once the lead key is on Railway | Tom is preparing the number (2026-09-28). Then one WhatsApp message to `054-758-8132`; non-zero in `wa_event_log` closes this |
| ~~U-051~~ | **CLOSED 2026-09-28 — Tom: "מאשר הכל".** The playbook's texts, round 2, with his edits from the review page (D-033, D-034), are APPROVED. `gt-factory-os` pins the approved playbook in `__fixtures__/whatsapp-lead-journey@<commit>.md`, and its D2 test holds the code to it byte for byte | closed |
| U-052 | Meta templates to submit: four marketing templates (wake-up messages 1–4, one link button each, no `פרסומת`, D-034) and one utility template (the order confirmation after 24 h), from the lead line. U-051 is closed | build: submit through `/api/v1/internal/jobs/lead-templates` once the lead connection's key (`WA_LEAD_SEND_TOKEN`) is on Railway (Tom) |
| U-053 | The site's questions and answers grow from six to 22 in three groups, an answer to every general question about working with GT (D-033), from approved sources only and with no price. **Copy APPROVED 2026-09-28 (Tom: "מאשר הכל")** | build: ships with the site's live push (`gt-site#30`) |
| U-054 | **Parked by Tom:** an AI module connected to Meta Business Suite that classifies Instagram Direct and Messenger enquiries and puts them into `sales_core` like every other lead. Tom: "בזה אל תתעסק עכשיו... נפצח את זה בהמשך" | later — not part of the journey build |
| U-055 | ~~How will Ice Dream orders appear in Shopify~~ **Closed 2026-10-02 (D-041):** as completed orders under the customer, tagged `ice-dream`. | closed |
| U-056 | `client_key` links a customer to a Green Invoice client, and D-035 depends on it. **System check 2026-10-02:** 25 of the 25 newest Shopify customers with an order (2026-08-02 to 2026-09-30) carry `custom.client_key`, written minutes to days after the customer was created. So it is written today. The writer is still unidentified: it is not an active Make scenario (team 1240098, checked) and not the customer-setup skill (it writes only a note). If the writer stops, new customers fall into review. | Tom: name the writer |
| U-057 | Obligations for contact persons' data under Israeli privacy law (registration, access logging, deletion and correction). A question for counsel, not asserted here. Unit B ships a redaction action and an access record. | Tom → counsel |
| U-058 | Security actions for Tom, details shared privately and not written in this public repository. One of them: a read-only Shopify token for the order mirror. | Tom |

## החלטות שממתינות לטום — עודכן 2026-08-31
**נסגרו באותו יום, בכתב:** TOM-A.2 (ימי אספקה) · TOM-A.4 (אין חוזה/מינימום/בלעדיות) ·
TOM-B (רשומות-שלילה יורדות; AMERICAN ו-HOJICHA נשארים) · TOM-C (ששת השמות מותרים) ·
TOM-D (700 ו-8 שנים מאושרים) · TOM-E (HOJICHA נשאר, + 1 ק״ג ב-₪750).
הרשימה המלאה: `doctrine/decisions.md` D-010.
**מה שנשאר — הכל מרוכז ב-`open-items/alex-meeting.md`, לסגירה בישיבה אחת:**

| # | מה | חוסם |
|---|---|---|
| 1 | מדרגות ההנחה לפי צריכה חודשית — המספרים | `boundaries#discount_or_terms` |
| 2 | שלוש חבילות ההתחלה — שם, תוכן, מחיר | **שלב בקשת ההזמנה** (`sales-motion#s05`) |
| 3 | אישור **9** שורות הטיוטה בבנק התשובות (8 מ-31.08 + `seasonality` מ-02.09, שנכתב מהמדידה) | 9 נוסחים ⊥ נאמרים ללקוח |
| 4 | מה קורה אחרי ההזמנה הראשונה — החזרה/החלפה · חוסר מלאי · מי מתקשר | 2 שורות `העברה` |
| 5 | ~~עונתיות~~ **נמדדה 02.09** — נותר רק תסריט מלון/קייטרינג/משרד | U-015 (חצי) |
| 6 | כיוון הסנכרון של גיליון הלידים | U-017, D3 |
| 7 | `כ-17 קלוריות` — מקור או הסרה · ארבע רשומות-השלילה עדיין בנות-הזמנה | CLAIM-3, U-019 |

**פתוח על טום בלבד — ⊥ דורש את אלכס:**

| מה | מצב |
|---|---|
| **חומרים שיווקיים לשליחה** (U-020) — קטלוג, מחירון ללקוח, סרטוני הדרכה → `06 · העלאות` בדרייב. ~~מתכונים~~ נסגרו 02.09 | **בתהליך.** טום 2026-08-31: "אני אכניס שם חומרים שיווקיים לשליחה" |
| **פרט קשר לאלכסנדר** (U-021) — היעד של 17 כללי ההסלמה | פתוח |
| **סנכרון הדרייב** — 6 מ-10 הקבצים ⊥ זהים בייט-לבייט לבנייה שבריפו. הכלי מאפשר רק יצירה+מחיקה, ⊥ החלפה בתוכן, כלומר ה-file-ID משתנים | פתוח — נשאל, ⊥ נענה |

## פריטי ניקיון (⊥ חוסמים)
| # | מה | איפה |
|---|---|---|
| CL-1 | `docs/pricing/2026-08-05_drinks_final_figures.json` הוא גרסה **מוחלפת** ועדיין יושב במאגר. קריאה ממנו מייצרת עמוד שלם של סתירות שאינן קיימות. לסמן או להסיר | `gt-factory-os-production-brain` |
| CL-2 | חמישה פגמים בקטלוג המשקאות שהספר עצמו מונה ב-§09 (שלושה מתכונים לתמצית שלא קיימת · מתכון וניל/אגבה כפול · "20–25 כוסות" · מספור כפול · ארבעה קטלוגי קנבה) — **בבעלות סשן תפריטי הקטגוריות**, ⊥ מתוקנים כאן | קנבה |
| CL-3 | `page 12` — הספר קורא למשקה `חליטת תה ירוק לואיזה וליים`; הרשות קוראת לו `חליטת תה ירוק וליים`. הכרטיס נושא את שם הרשות | סגור בכרטיסים |
| CL-4 | `catalog-truth.md` נזרע 2026-08-06 ולא הוצלב מול שופיפיי עד 2026-08-31. שתי שורות בו טענו "אין SKU פעיל" ולשתיהן היה — ובאותה בדיקה התגלה ש-AMERICAN תומחר הפוך בחנות. תוקן. **הלקח: קובץ אמת שלא נסרק הופך לרמז בעצמו** | סגור · `scripts/knowledge/drift_scan.py` |

### Social-property pass (this branch — the ownership audit)

| ID | Question | Route |
|---|---|---|
| U-038 | **לינקדאין: הדף קיים. נפתח ע"י תום מהפרופיל האישי שלו, 2026-09-03** (`user_confirmed` — "סיימתי עם לינקדאין"). מולא באנגלית: tagline 116 תווים, Overview 1,383/2,000, 20 specialties, טלפון `+972 54-758-8132` (קו הלידים, D-014). `Year founded` **נשאר ריק** — אין שנה מאומתת, ו"8 שנים" ⊥ אושרה (U-021). הניסוח הוסר מ"cold-brew" והוסיף מאצ'ה, ייצור בישראל, ו-`Israel's leading cafés` — **המילים של תום, 2026-09-03, `user_confirmed`**. הערכה בריפו עודכנה לגרסה שנשמרה בפועל | **פתוח, ובסדר יורד של סיכון:** (1) **אלכס כ-`Super admin`** — לינקדאין: *"If you're the only super admin on the Page, you must assign another super admin before removing yourself"*, ∴ בלי זה ⊥ ניתן להעביר את הדף לעולם והוא מתייתם עם הפרופיל. (2) 2FA על הפרופיל האישי — הוא הבעלים בפועל. (3) שורת `לינקדאין — דף חברה` בכרטיס הגישה. (4) עוקבים=0 + תאריך כנקודת פתיחה. (5) תיאור בעברית דרך `Manage description in another language`. (6) לאשר `2-10 employees` |
| U-039 | **טיקטוק: אין ולו מייל אחד מטיקטוק בתיבה של `tom@gteveryday.com`.** חיפוש `in:anywhere` (כולל אשפה וספאם) 2026-09-03 החזיר 14 תוצאות — **כולן ניוזלטרים שמזכירים את המילה**, אפס מטיקטוק עצמה: ⊥ הרשמה, ⊥ התחברות, ⊥ התראה, מאז 2023-11-04. ∴ החשבון ⊥ רשום על התיבה הזאת — או שהוא על מייל אחר, על טלפון, או שנפתח ב-SSO (Google/Facebook/Apple), ואז מי שמחזיק את חשבון ה-SSO מחזיק אותו. **⊥ ננחש.** הפרופיל נבדק שוב חי היום: זהה לחלוטין ל-31.08 — 13 סרטונים, 23 עוקבים, 383 לייקים, `nickname` ברירת מחדל, ציבורי | טום — (1) לשאול את אלכס: הוא פתח את פורטפוליו מטא ב-2019 והחשבון נפתח 11.2023 עם 13 סרטונים, זה מישהו שעשה שיווק. הודעה אחת. (2) איפוס סיסמה **לפי username** ב-`tiktok.com` — טיקטוק מציגה את היעד **ממוסך** (`i***@…` או `+972*****`), וזה מזהה את הערוץ בלי ניחוש. ⊥ להשלים את האיפוס, רק לקרוא את הרמז |
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
| U-031 | **Coexistence lapses silently, and nobody owns the check.** WhatsApp coexistence requires the phone app to be opened at least once every 13 days and never uninstalled, or the Cloud API link dies. Nothing announces the lapse — no alert, no red row. That is the exact signature of three failures already paid for: the Make OAuth token (silent two months), the 06:00 digest (silent six days), the LionWheel pick bridge (merged, never deployed). With **every lead automation now sitting on `054-758-8132`** (D-014), a silent lapse stops the whole intake and nobody learns. Verified live on the order line: `order_intake.wa_event_log` holds 24,162 events since 2026-06-26, last one minutes ago, 9,501 of them `echo` — coexistence demonstrably works, which is exactly why its one failure mode needs an owner | Tom — name a person, and add a machine check that fails loudly when the newest `wa_event_log` row ages past a threshold. Good intentions are not a monitor |
| U-035 | **Correction — I was wrong about the square logo, twice, in opposite directions.** This file said no square logo existed; `youtube-refresh-kit.md` said `GT_Logo_Black.png` was 800×800. Measured from the PNG header on 2026-09-02: **971×960** — 11 px off square, not 800×800, and not missing. The identical image sits at two Dropbox paths (`New/ARCHIVE/…/BRAND-IDENTITY/Logos/GT_Logo_Black.png` and `Data Center/PRODUCTION 2/B-BAGEL-Tea-Programme/assets/gt-logo-black.png`). Every platform centre-crops, so 11 px is cosmetic and **blocks nothing** — id5, LinkedIn, TikTok and Instagram covers are all unblocked | optional: pad to 1000×1000 for a pixel-exact square. Not required |
| U-036 | **Opening baseline for YouTube, captured 2026-09-02: 15 subscribers**, 7 videos, handle `@greenteaeveryday5540`. The display name is already `GT Everyday · גרינטי` — the `y2` rename is **done**, and the older record of it as `GreenTea EveryDay  גרינטי ` (double space, trailing space) is superseded. Without a dated baseline there is nothing to compare against in 90 days | closed as recorded — belongs in the credentials sheet's YouTube row |
| U-034 | **RE-OPENED 2026-09-02 — I closed this on a misread and the close was wrong.** Tom answered "2. כן. יש לוגו ריבועי" to a two-part message; I took the "כן" as confirming the channel and closed U-034 on it. His screenshot settles it: **YouTube → Settings → Account → All channels shows exactly one channel** — `GT Everyday · גרינטי`, `@greenteaeveryday5540`, **15 subscribers**. `UC8Wlby9ihV04Ky5CsZZoWWg` (`GT everyday`, still live and still empty, re-checked today) is **not under this Google account**. It may still be GT's under some other account — an old marketing login, a former agency — or it may be a stranger on our name. Unproven either way, and the name is still not evidence. ∴ `@gteveryday` cannot be taken by renaming, and the fallback `@gt_everyday` is **re-verified free today (404)** | Tom — take `@gt_everyday` and move on; it is not worth chasing. Only if he wants the exact handle: try recovery on whichever old Google account might hold `UC8Wlby9ihV04Ky5CsZZoWWg` |
| U-033 | **The digest fired — and wrote nine successes that never happened.** First real firing 2026-09-01 03:00:19Z, `il_hour: 6`: the route works and the six-day silence is over. But `ok: false`. 10 leads due, 2 recipients. Tom's email sent (1 lead). **Avi's failed: `resend 403 — You can only send testing emails to your own email address (tom@gteveryday.com). To send emails to other recipients, please verify a domain`.** Resend is still in test mode with no verified domain, so the system can only ever deliver to Tom. The damage is the record, not the miss: `reminder_sent` events were written for **all 10 leads including the 9 that were never delivered**, and `lead_event_reminder_once_per_day` (unique on `lead_id` + Israel-local date) now blocks any retry for those 9 today. The database says Avi was told about איציק בכר, Hadas Elian Levi, Wesam Amara saleh, Hussin Ayoub, אלדר נפתלייב, רפאל שי דיין, Tomer Danieli, tamer and מאור — seven of them overdue since 08-30/08-31. He was not. **This is the same class as U-024 and U-031: a system recording a success it did not achieve.** The function already knows — it wrote `claimed_but_unsent` with all nine ids — it just does not undo the event | **Two fixes, different owners.** Tom: verify a sending domain in Resend, or the digest can never reach anyone but him — the loop repeats every morning until then. Engineering: write `reminder_sent` only **after** a successful send, so a delivery failure stops being a permanent same-day skip. ⊥ delete the nine rows — `lead_event` is append-only |
| U-033-a | **CLOSED as diagnosed, 2026-09-02 — verifying the domain was never going to fix it, and the code says so in a comment.** The 03:00Z run failed with the byte-identical `resend 403`: due 12, sent 1, **11 undelivered to Avi** (9 the day before — 20 across two days, all recorded as sent). Root cause is in `supabase/functions/sales-leads-poll/index.ts:60`: `const DEFAULT_FROM = 'GT Leads <onboarding@resend.dev>'`, used at line 277 unless the `RESEND_FROM` secret is set. `onboarding@resend.dev` is **Resend's shared test sender, which Resend restricts to the account owner's own address** — that is the exact 403. A verified domain changes nothing while the `from` still points at the shared sender. The comment above that line states the assumption that expired: *"Resend's shared sender works before any DNS work … because the only recipient is the account owner."* True when Tom was the only recipient; false the moment Avi became an assignee, and nobody revisited it. **This is wider than the digest** — `poll_run` shows the same `resend 403` on the **`ingest`** route on 2026-08-31 and 2026-09-01, so **new-lead alerts to anyone but Tom have been failing too** | **CORRECTED TWICE, 2026-09-03. Final answer: one step, and the domain to use is `greentea-everyday.com`.** First correction claimed no domain is verified in Resend — that was `gteveryday.com` only, generalised from one lookup (the same error as the TikTok 200 and the logo dimensions: checked one thing, spoke about all of them). Tom asked whether it already runs through the other domain. It does: **`greentea-everyday.com` carries all three records Resend asks for** — `resend._domainkey` DKIM present, `send.greentea-everyday.com` MX → `feedback-smtp.ap-northeast-1.amazonses.com`, and its TXT → `v=spf1 include:amazonses.com ~all` (DoH, 2026-09-03). `gteveryday.com` has none of them; `greenteaeveryday.com` (no hyphen) does not resolve at all. ∴ ⊥ GoDaddy, ⊥ a new subdomain, ⊥ touching the root SPF that carries Google Workspace. **Readable without waiting for 03:00Z:** `POST {"route":"health"}` returns `RESEND_FROM` and `sends_from_shared_sender` as of `sales-leads-poll` v20 (deployed 2026-09-03), reading `false` / `true` at that moment. The 06:00 IL run of 2026-09-03 was the third: due 14, sent 1, **13 more claimed and undelivered — 33 across three days** | Tom — **one secret**: `RESEND_FROM = GT Leads <leads@greentea-everyday.com>` on `sales-leads-poll`. ⊥ code, ⊥ deploy. Then `health` flips to `true`/`false` and the next 06:00 run proves it. Two notes: the DNS proves the records are in place, the Resend dashboard's own "verified" badge is the authority and was ⊥ read from here; and replies to that address land in `greentea-everyday.com`'s Google Workspace, so it needs a mailbox or alias if anyone ever replies |
| U-032 | **CLOSED 2026-08-31 — Tom: every public call-to-action points at the lead line.** All 27 `wa.me` links across the Q4 calendar and the LinkedIn, Instagram, YouTube, TikTok and WhatsApp kits now read `wa.me/972547588132`, plus the two displayed contact numbers on acquisition surfaces (the LinkedIn location field and the YouTube channel description). The website, invoices and storefront pages keep `054-398-2444` — they speak to existing customers. **One number per job, no exceptions to remember.** The link was checked as well-formed and redirecting; that is *not* proof the number answers on WhatsApp, which needs one tap from a phone before the first post goes out | closed |
| U-015 | **CLOSED 2026-09-01 — Tom checked and reported both accounts are fine** (`user_confirmed`). This environment never could read them, so the close rests on Tom's own look, not on evidence gathered here — recorded that way deliberately. ⚠️ Still not recorded anywhere: **which handle is the official one**, and the opening baseline (`i6`). `i2`–`i5` all need the handle before anything is posted | Tom — name the handle when Instagram work starts |
| U-016 | **CLOSED 2026-08-31 — the premise was false.** GT does hold admin; the portfolio was created by Alex Berov in 2019 and business verification passed in 2022. Original entry: GT holds no admin on its own Meta Business account. Blocks the WhatsApp green tag, business verification, the lead-form fix, CTWA, and re-authorising the connection before `2026-10-23` | Tom (§6.E) — find today's admin, or open a Meta support case |
| U-017 | `judge.me` and Yotpo both run on the live storefront — the theme config points at judge.me while the Yotpo loader fires on the same page. Customer reviews may be split across two systems with half invisible | Choose one. Yotpo already runs reviews **and** loyalty (`z2`), so it is the natural survivor |
| U-018 | Google Tag Manager loads on the storefront and nobody has said who owns the container or what fires in it. GA4 itself is still not connected (`g3`) | Tom — GTM account access |
| U-019 | Registrar and renewal date for `gteveryday.com` and `greentea-everyday.com` were never checked. A domain that lapses quietly takes the whole store down. **Half measured 2026-09-03** (incidentally, while diagnosing U-033-a): `gteveryday.com` nameservers are `ns27/ns28.domaincontrol.com` — **GoDaddy DNS**, which is where any mail record goes; MX is Google Workspace; the root TXT carries a Google site verification and an SPF with a GoDaddy merge plus HubSpot. Nameservers name the **DNS host**, ⊥ prove the registrar, and say nothing about the renewal date — both still open, and `greentea-everyday.com` was ⊥ checked at all | Tom — registrar login, then record in `GT — כרטיס גישה` |
| U-020 | **CLOSED 2026-08-31 — asked in two documents at once, answered twice the same day.** `054-758-8132` is Tom's work number and becomes **the lead number**: every new enquiry and every new-customer sale, with the automations sitting on it (Tom, in writing, this session; already logged as **D-014** on the parallel lead-system branch). `054-398-2444` stays the **order line** for existing customers and is untouched. Two live lines, two jobs — not a swap. It joins the Cloud API by **coexistence**, not classic onboarding (**D-015**): the number stays live in the phone app and the API reads and sends alongside it | closed — see U-031 for what this now puts at risk |
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
  Coexistence liveness recipe `recipes/coexistence-liveness.md` (U-031).
  Credentials sheet and the 72-row action board live in Tom's Drive, **not in this repo** —
  no secret value is ever written here (`GT — כרטיס גישה` and `GT — לוח פעולות רשתות`,
  folder `GT Everyday — נכסי מותג`). Board as of 2026-08-31 end of session: 13 done,
  14 ready to paste, 23 open, 6 blocked, 16 on the website track. The credentials sheet
  still carries 24 rows and needs a 25th — TikTok (U-027).
- Latest evidence snapshots (both 2026-08-24): `evidence/2026-08-24-make-intake-handover.md`
- Latest evidence snapshot: `evidence/2026-08-31-lead-response-ground-truth.md` — measured lead,
  transport, backlog, first-response and WhatsApp ground truth; **records that GT's WhatsApp Business
  Cloud API has been live since 2026-06-26 (Dualhook coexistence, 24,028 events), which several planning
  documents still describe as not built.** Companion decisions in `gt-factory-os-production-brain`:
  `docs/decisions/2026-08-31-lead-intake-architecture.md` (awaiting Tom) and
  `docs/plans/2026-08-31-lead-setup-artifact-reconciliation.md`.
- Previous evidence snapshots (both 2026-08-24): `evidence/2026-08-24-make-intake-handover.md`
  (intake hand-over to Make) · `evidence/2026-08-24-sales-report.md` (sales report).
  Previous: `evidence/2026-08-23-live-intake-bringup.md`, `evidence/2026-07-18-two-numbers.md`.
- Knowledge layer (2026-08-31): `knowledge/README.md` — reading order for an agent;
  `evidence/2026-08-31-knowledge-book-reconciliation.md` — the reconciliation run.
  Gate: `gt-factory-os-production-brain/scripts/knowledge/reconcile.py`.
  Rendering (generated, never hand-edited): https://claude.ai/code/artifact/513456cd-5fa3-4ff1-8616-8ea82e020b22
  — the original shared artifact `f0457ed1-…` cannot be published to from this session.
- Sales report recipe: `recipes/sales-report.md` (taxonomy + anchors Tom-approved 2026-08-24).
- Customer-count recipe (rule 2): `recipes/customer-count.md` — never quote a stored count.
- Decisions log (incl. PROPOSED items awaiting Tom): `doctrine/decisions.md`.
