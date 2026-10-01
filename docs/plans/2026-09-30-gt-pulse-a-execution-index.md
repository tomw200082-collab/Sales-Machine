# GT Pulse Unit A — execution index (2026-09-30 UTC)

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
- Railway has `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED=true`, and 4 real `first_menu` sends exist, the last at 2026-09-30 14:32 UTC. This contradicts the line below that says it "remains `false`".
- The production API deployment carries no commit SHA.

No production merge, deploy, migration, flag change, backfill or customer message happened in this session. The local staging stack lived only in the session container.

## 2026-09-30 16:05 UTC — superseding pre-production handoff

Tom deferred production and asked for a fresh Claude Code product-discovery/build session. The new [pre-production masterprompt](https://github.com/tomw200082-collab/Sales-Machine/blob/status/gt-pulse-a-2026-09-30/docs/plans/2026-09-30-gt-pulse-preproduction-claude-code-masterprompt.md) orders Caveman/Ponytail, Grill with Docs plus domain modeling, Brainstorm, plan approval, Anthropic frontend-design and UI/UX Pro Max, connected five-lens UX release gate with P0/P1 repair and rerun, /simplify, whole-branch code review, then exact-final-head verification-before-completion. The nine built tasks remain the baseline; any new design needs his approval.

Backend [draft PR #329](https://github.com/tomw200082-collab/gt-factory-os/pull/329) at `ff69e3cecc0ffcd522c69eeb09255adcf98e51f4` passed [PR typecheck](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36740413352). Portal [draft PR #239](https://github.com/tomw200082-collab/gt-factory-os-portal/pull/239) at `1ba2c98bcf8aad63b5d81b3fb1113dbe91439093` (runtime tree from `a2e1786`, later copy-assent documentation) passed [portal-pr-guard](https://github.com/tomw200082-collab/gt-factory-os-portal/actions/runs/36740472210). Tom authorized temporary watching of these two PRs. Tranche 185 now records his exact assent to the sixteen later Hebrew strings. New copy still needs its own authority.

The second cost-approved temporary Supabase branch in the **existing** project failed with `MIGRATIONS_FAILED`. Its earliest concrete replay error at 15:51:31 UTC was `relation "private_core.supplier_items" does not exist` in `0090_readiness_view_pack_conversion_fix`; migration history and sales schema were empty. The branch was deleted and absence verified. See the [connected staging attempt](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-connected-staging-attempt.md). No paid branch remains, and no production merge, migration, deploy, flag, backfill or outreach occurred.

**Current HOLD:** connected staff Auth→browser→API→DB and WebKit keyboard proof, full connected UX gate, final-head review/verification and later production decision. PR CI passing does not close those gates. Earlier dated paragraphs below preserve their historical observations; superseded claims that copy assent, draft PRs or the PR guard are pending do not describe the current state.

**Status: LIVE / HOLD.** This is a dated engineering evidence index, not a change to the approved specs or a production release declaration. The detailed Native task ledgers remain in each isolated worktree's `.superpowers/sdd/2026-09-29-gt-pulse-a-sales-task-loop/progress.md`.

## Resume execution — final review heads, 2026-09-30 UTC

This section supersedes the earlier branch/check rows below. The nine original tasks were verified, not restarted. Backend `feat/gt-pulse-a-sales-contact-loop` is at `42b560422cd327533135333b12390994a39304c9`; portal `feat/gt-pulse-a-sales-corridor` is at `a2e1786c33fc8b257240d7076113222ec8a80028`; brain `audit/gt-pulse-a-ux` at `dc5bb8dae511604dff371865c7bb1dce0afaaf4a`. Local worktree base commits are earlier ancestors with uncommitted tree-equivalent changes; the canonical remote SHAs above identify the reviewable artifacts. Sales-Machine's pinned resume source was `a22ff30e46173f324480f4cd75478d8b7c2dd74c`.

Backend remediation commits after the handoff: `9049f8c`, `2566a90`, `d4df086`, `96b3f6a`, `34b50fc`, `487e939`, `42b5604`. The final work isolates the performed task via `source_task_id`, keeps unrelated due tasks open, resolves waiting and draft cancellation/undo, records repeat lead-line free text as source work without an advisory/row-lock inversion, and stops wake after lost→undo until a new answered conversation. SQL/API journey and race regressions accompany the changes. [Final exact-SHA CI](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36688872012): two green jobs; 0362 pgTAP 79/79, neighboring sales SQL green, wake/lead DB 19/19, role/activity API 11/11, legacy workspace 14/14, staff alert 38/38, disposable guarded backfill checks and root typecheck. Earlier [run 36687895494](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36687895494) exposed nondeterministic timestamp/UUID selection under lost undo; the final SQL selects the cancellation event actually referenced by openable tasks. Two subsequent exact-SQL CI runs, including the final head, passed 79/79.

Portal remediation commits after the handoff: `a91c915`, `7a06478`, `399798c`, `b002d9d`, `a2e1786`. Today/Leads/Attention use a channel-valid outcome sheet with durable drafts; TaskCard preserves source ID; rep ownership, missing deep links, email-only actions, date/DST and Leads background inertness are covered. The original approved Hebrew table is recorded in tranche 185 with its contextual assent; **additional exact strings** remain proposed there pending register assent. Final local source: Vitest 1,525/1,525; sales Chromium `@mocked` 58/58; all Chromium `@mocked` 126 expected with zero skipped/unexpected/flaky; `npm run build`, `npm run typecheck`, `npx eslint .` exit 0 (558 warnings); synthetic matrix 40/40 with zero horizontal overflow and zero missing headings. Vercel [final preview](https://gt-factory-os-portal-oc0b75ert-tom-1486s-projects.vercel.app) is READY at `target=null`, not production. No actual PR-triggered `portal-pr-guard` ran because safe immediate unsubscribe is not exposed.

The equivalent post-remediation five-lens [UX report](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-sales-ux-gate-final-followup.md) found zero verified open P0/P1 **in synthetic render/interaction coverage only**. Fresh 320/390/430/1440 screenshots and matrix are linked there. `/simplify` was unavailable. A labelled ponytail pass removed the redundant `atNineAM` wrapper; request identity, locks, audit history and access checks remained. Independent backend/portal whole-branch reviewers rechecked their final findings and reported no Important/Critical code issue. The [read-only release check](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-release-check-final-followup.md) is HOLD.

| Gate | Verdict | Exact reason |
|---|---|---|
| D1 | HOLD | Task 9's controlled release is unfinished; tasks 1–8 and the implementation portion of 9 are reviewable. |
| R1 | PASS | Scoped remote branches, task/commit index and original copy ruling are recorded; no PR watcher was created. |
| D2 / R2 | HOLD | Staff email and safe link have test coverage; signed-out real Supabase auth→browser→API→DB is unproved. |
| D3–D4 | PASS | Atomic activity, source tasks, rep/manager roles and retry pass disposable DB and mocked browser coverage; the separate R2 connected gate stays HOLD. |
| D5 / R3 | HOLD | Two-connection stop/send, wait, lost undo and forced wake tests pass; deployed SHA/flag and actual runtime path unverified. |
| D6 | HOLD | Hebrew RTL, mobile widths, source-backed rail and keyboard tests pass synthetically; real keyboard/WebKit unproved. |
| D7 / R4 | HOLD | Five-lens follow-up has zero synthetic P0/P1, but connected staging UX gate is absent. |
| D8 | PASS | Equivalent ponytail cut, two independent clear reviews and exact-head code checks ran. |
| R5 | HOLD | Authenticated path and actual PR-triggered check are absent, so full release verification cannot pass. |
| D9 / R6 | HOLD | No production 0362 schema, post-schema preview/digest, batch-specific approval, merge, deployment or flag switch. |
| D10 / R7 | PASS | Exact SHAs and limits recorded, no `SHIPPED` claim. |

Read-only production SQL at **2026-09-30 08:25:25 UTC**: 259 leads, 183 open, 148 open unassigned; `sales_core.task` absent, `activity_required` absent, migration-history 0362 count zero. Preliminary pre-schema counts from the earlier snapshot are stale and cannot authorize a batch. Vercel production `dpl_CuXtU3i8wc1Rb3NzyPMU1Sn5MWqL` is READY at default-branch SHA `5e45b2d91cc8938ec1945925e46f481b9146c404`; the final portal SHA is only a `target=null` preview. Railway production API `f285afb2-1a71-4f35-b625-4528cbeea043` is SUCCESS without source SHA in deployment metadata. `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` is present by name, but the connector redacts its value. No production migration, deploy, customer message, flag flip or backfill happened. The documented rollback cancels only digest-matched open bootstrap tasks with append-only audit after a separately approved write; it never deletes task history. Tom expressly approved the quoted **$0.01344/hour** Supabase branch; it was created at 09:04 UTC, found `MIGRATIONS_FAILED` with zero migrations and no `sales_core` schema, and deleted by approximately 09:08 UTC. [Dated staging attempt](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-connected-staging-attempt.md) records the checks and verified cleanup. No connected R2 proof was obtained. A future paid resource needs a new cost boundary. The eventual production backfill needs an exact count/digest and separate written go/no-go. **Next human action:** provide an authorized staging database/API path with the canonical sales migrations through 0362 and real staff auth, so the connected gate can run; then review exact new copy before release/batch approval.

## Earlier implementation ledger (dated baseline)

| Plan task | Owning repo | Local commit evidence | State and missing proof |
|---|---|---|---|
| 1 staff email | backend | `148b010`, `26ab6fe`, `de48c6f`; later email correction on branch | Code built; final-head staff alert tests 38/38. Real signed-out staff-email login still unproved. |
| 2 safe deep link | portal | `1c3f917`, follow-up `130c2f2` | Code built, same-route A→close→A→close→B browser proof; real Supabase login unproved. |
| 3 source tasks | backend | `f2ae352` | Code built; final isolated PostgreSQL pgTAP and guarded backfill green. |
| 4 atomic activity | backend | `ab9c4dd`, review fixes `2fa73ec`, `8865f58`, `1234c5c`, `c50e591` | Code built; owner retry, first-contact closure, future review and same-display-name account identity pass exact-tree database CI. |
| 5 wake guard | backend | `5d1e1f5` | Code built; final-tree two-connection CI 18/18. |
| 6 role API | backend | `12fa6c3`, review fixes `2fa73ec`, `8865f58`; final tests `6d4f564`, `93a9db6` | Code built; final-tree role/activity API 11/11 and legacy 14/14 in disposable DB. |
| 7 owned portal queue | portal | `2af1698`, review fix `130c2f2` | Code built; synthetic rep/manager browser proof; connected DB proof pending. |
| 8 three-entry activity | portal | `a03f133`, review fix `130c2f2` | Code built; Today, Leads and Attention browser cases green; authenticated API/DB proof pending. |
| 9 GT Pulse, backlog, release | portal + backend | `3ed7769`, `81973d1`, `130c2f2`, `3c8f987`; backend `2bf9af7` | First visual slice and idempotent preview/apply script built; release/production batch explicitly deferred. |

**Branch ranges.** Backend base `0e3c6fb49f82e9f9bddf38e478d78c17f2173878` → local `c50e59195dbd8922a80f4ce93e129550e64bf759`, remote tree-equivalent `fa9c0454dd0856594678448c750fa22b09e58f29` (tree `234d93bd1f48c44e92c24f5947b500206091a5d8`). Portal base `5e45b2d91cc8938ec1945925e46f481b9146c404` → local `3c8f987953e827b7a7ce3e86eea373017eab6d23`, remote tree-equivalent `103354bdce2e93cc4b19232dadc46745640d3ffb`. Remote connector commits preserve exact final Git trees but not the local per-task parent history. Brain UX/release evidence branch `audit/gt-pulse-a-ux` has the gate and release report.

**Checks on final portal tree.** Unit 1,517/1,517; relevant sales Chromium 57/57; whole portal `@mocked` Chromium JSON reporter 125 expected, zero unexpected/skipped/flaky; build, typecheck and lint exit 0 (558 warnings); tranche registry presence 1/1; 40 synthetic route×role×width renders at 320/390/430/1440px with zero horizontal overflow. Five-lens equivalent audit found and fixed two initial P1s plus a small P2 and subsequent reviewer findings; zero verified open P0/P1 in synthetic corridor. It remains HOLD without connected staging/auth, real WebKit keyboard and exact runtime proof. `/simplify` was unavailable; an explicit ponytail/equivalent pass removed stale optimistic UI text, duplicate reason display, unused type and repeated sorting, retaining transactional locking, idempotency and audit history. Two independent reviewers inspected backend and portal diffs and rechecked their Important findings; no Important code finding remains.

**Checks on final backend tree.** [Branch-push CI 36676625217](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36676625217) succeeded on the exact remote tree in both jobs: root typecheck, staff alert 38/38, sales SQL pgTAP through assertion 68 with no failure, guarded backfill stale-preview rejection and three synthetic paths plus idempotent rerun, two-connection wake/lead DB 18/18, role/activity API 11/11, legacy workspace 14/14. The same-display-name request takeover was reproduced RED on [run 36676430834](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36676430834), fixed and rechecked by an independent reviewer. Earlier local wake unit 23 pass/18 DB skips; full API package typecheck retains inherited unrelated diagnostics, and broad Node suite was stopped after database-dependent inherited failures. CI is isolated disposable PostgreSQL proof, not an authenticated staging browser or production proof.

**Production read-only snapshot, 2026-09-30.** 257 leads, 183 open, 150 open unassigned; `sales_core.task` absent, version 0362 absent from migration history, `activity_required` absent. Provisional pre-schema candidates: 148 manager first-contact, 2 manager call, 33 owned call. These can change after schema and events, so they are **not** the exact guarded backfill preview and cannot authorize a batch. Deployed API/portal SHAs and outreach environment flag unverified. No migration, deploy, flag switch, customer message or backlog write was performed.

**Governance rulings.** Brain scoped signal 36 and bounded Mode B authorized sales corridor development only; portal tranche 185 lists the touched paths. New Hebrew labels are proposed verbatim in that manifest and await Tom's exact-entry approval. The production backlog requires separate written count-specific go/no-go after the schema, reviewed code, staging proof and exact preview. No PR was opened: Sales-Machine's no-autowatch rule requires immediate `unsubscribe_pr_activity` after creation, but that capability is unavailable here. Separate remote branches remain reviewable. Return Mode B to A at corridor closure under the governor; no agent may self-issue a release signal. Masterprompt remains `LIVE`, not `SHIPPED`.

## 2026-09-30 15:20 UTC — resumed release gate

Canonical GitHub refs rechecked. Backend branch `feat/gt-pulse-a-sales-contact-loop` reconciled a newer `main` change (`04cb0f6`) with merge commit `f6698edb4ccfd44dcf3d7714b7fcada9634940cd`; now ahead of main, behind zero. Its follow-up preserves the existing once-daily FAQ response and routes repeat-contact events to Unit A owned tasks. RED: three journey cases failed on the prior implementation. GREEN: local sales Vitest 91/91 runnable (19 database cases skipped locally), root typecheck exit 0; [branch CI 36735415815](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36735415815) success on the exact SHA, 0362 pgTAP 79/79, two-connection/lead DB 19/19, role/activity 11/11, legacy 14/14, staff mail 38/38. No claim of connected staging.

Portal branch `feat/gt-pulse-a-sales-corridor` remains `a2e1786c33fc8b257240d7076113222ec8a80028`; prior preview and mocked checks remain branch-only proof. Brain audit correction commit `62c14eadf181bcac655b3349f4e42ed026831ebd` records Tom's explicit preference: existing Supabase project and existing portal only. Standalone-project proposal withdrawn. The prior paid development branch was deleted; a new branch within the existing project is currently quoted at $0.01344/hour and has not been created without fresh cost-specific consent. Existing unrelated `bom-cluster-shadow` remains untouched.

Production read-only at 15:17 UTC: 260 leads, 184 open, 147 open unassigned; `sales_core.task` absent and migration 0362 not in history. Backfill has no post-schema exact count/digest or batch authorization. Additional Hebrew entries proposed after the first exact table still await their own register assent. PR watcher exit capability remains unavailable. Status: **LIVE — HOLD** on connected Auth/browser/API/DB and WebKit UX evidence, copy register, PR guard/watch constraint, and controlled release. No production write or new project.

## 2026-09-30 15:35 UTC — exact release-candidate head and deferment

Tom explicitly requested preparation up to a production decision, with **no full production deployment now**. Backend final review SHA `ff69e3cecc0ffcd522c69eeb09255adcf98e51f4` supersedes the earlier `f6698ed` evidence line above. A self-review found that an event insert did not prove task creation under a concurrent close/opt-out; three RED journey assertions led to removal of the false `task` result field. Latest local sales Vitest 91 pass/19 DB skip, root typecheck exit 0; [exact-SHA CI 36737309399](https://github.com/tomw200082-collab/gt-factory-os/actions/runs/36737309399) success with 0362 pgTAP 79/79, two-connection/lead DB 19/19, API role/activity 11/11, legacy 14/14, staff mail 38/38 and disposable backfill guards. The earlier `f6698ed` CI remains historical.

Portal SHA `a2e1786c33fc8b257240d7076113222ec8a80028` did not move. Fresh local typecheck, ESLint `--quiet`, Next build passed; unit suite 1,525/1,525. Fresh Playwright was blocked before tests by sandbox Node `uv_interface_addresses` error. Prior 58/58 mocked browser evidence is dated, never connected proof. [Release check update](https://github.com/tomw200082-collab/gt-factory-os-production-brain/blob/audit/gt-pulse-a-ux/docs/phase8/dry-runs/2026-09-30-gt-pulse-a-release-check-final-followup.md) records the exact limits. Production still lacks 0362/task schema; no schema, flag, deploy, PR or backlog write. Release status **LIVE — HOLD** until connected staging, copy register, rendered UX/WebKit, PR guard/watch exit and exact target preflight can be evidenced. Production deploy remains explicitly deferred by Tom even after those gates close.
