# MASTERPROMPT — GT Pulse sales contact loop built, audited, simplified and verified

**STATUS: LIVE — HOLD (2026-09-30 UTC). Final review branches and synthetic/disposable verification are complete; connected authenticated staging, later exact Hebrew copy entries, PR guard, runtime release and count-specific backlog approval remain open. [Final execution evidence](2026-09-30-gt-pulse-a-execution-index.md). No production deployment or customer send.**

> **Usage:** Paste this entire document as the first message of a fresh coding session with access to `tomw200082-collab/Sales-Machine`, `tomw200082-collab/gt-factory-os`, `tomw200082-collab/gt-factory-os-portal`, and `tomw200082-collab/gt-factory-os-production-brain`. The session owns Unit A from implementation through a sales-specific UX release gate, remediation, simplification and verification. Do not answer with another plan; execute the approved plan.
>
> **Provenance:** The requester approved the two written GT Pulse specs, the Unit A implementation plan, and **Native** execution in the conversation on 2026-09-29. This handoff was written from the code and documents inspected that day; it has no authority to activate customer-facing outreach or invent business policy.
>
> **Shelf life:** The repository/runtime snapshot below is only a 2026-09-29 observation. If pasted after 2026-10-13, re-run §2.5 before using any SHA, migration number, tranche number, flag or deployment claim. Re-run it even on the same day. If code has advanced, adapt the smallest implementation detail under the approved specs, record the ruling in the execution ledger, and revise this document if its contract is materially wrong. Stop on a business-policy or safety conflict.

## 0. How to work

- **Who you are here:** The primary coding agent in one new session. You can read private GitHub repositories and run the repository's code, tests, browser and database checks, or use their authorized CI/connected equivalents. If a capability is absent, say exactly which proof is unavailable; do not simulate a green result. You may make ordinary engineering decisions within the approved specs. You may not decide new service policy or activate customer messages.
- **First action, before code:** Open the approved spec, plan and governing files in the order below. Then run §2.5, record dated baseline and governance evidence, and start `superpowers:executing-plans`. Use `superpowers:using-git-worktrees` for isolated backend and portal workspaces, `superpowers:test-driven-development` within the task loop, and its ledger/task scripts. This is **Native**: implement the tasks yourself, sequentially within the dependency/governance order below; obtain the skill's whole-branch code review after the remediation/simplification work and before final completion.
- **Read first:** `gt-factory-os-production-brain/CLAUDE.md`, `CURRENT_STATE.md`, `EXECUTION_POLICY.md` §W2 modes and §Approval thresholds, `ACTIVE_NOW.md`, `AI_BRAIN_ROUTER.md`, `docs/decisions/modules/sales-declaration.md`, and `.claude/state/{runtime_ready,active_mode}.json`; then `Sales-Machine/CLAUDE.md`, `CURRENT_STATE.md`, relevant `doctrine/decisions.md`, the two approved GT Pulse specs and `docs/superpowers/plans/2026-09-29-gt-pulse-a-sales-task-loop.md` on `design/gt-pulse-crm`; then `gt-factory-os/CLAUDE.md`, relevant migrations/API, and `gt-factory-os-portal/CLAUDE.md`, `docs/portal-os/registry.md`, `scorecard.md`, `_active.txt` and its manifest. Read the Superpowers skills from the installed source, not from memory. For the UX gate read brain `.claude/commands/ux-release-gate.md` and the five auditor definitions. For simplification read the available `/simplify` instruction if installed and brain `.claude/skills/ponytail-review/SKILL.md`.
- **Authority:** Brain `CLAUDE.md` and `EXECUTION_POLICY.md` govern lanes, signals and approval, alongside each runtime repo's rules; Sales-Machine doctrine and the two approved GT Pulse specs control product behavior; the Unit A plan is the implementation map; this handoff controls sequencing and evidence, never superseding those sources. The brain UX command is a **read-only audit method**, not permission for its auditors to edit code. Its generic operations-portal language and scoring assumptions must be re-aimed at the Hebrew RTL B2B sales workspace, using the sales exception in portal `CLAUDE.md`.
- **Inherited rules:** Halt conditions, customer-write authorization, evidence standards, tranche manifest and git discipline come from the governing files and named skills. Project-specific deltas are in §§5–8. Do not duplicate or weaken the source rules.
- **Working cadence:** Post brief, concrete progress in Hebrew during a long run; continue autonomously across all tasks. Do not pause after each task or ask the requester to confirm decisions already approved. Keep the execution ledger and commits current so compaction/new context cannot restart completed work.
- **Output language: concise Hebrew.** Short, concrete status and final report. Keep code, tests and technical artifacts in the repository's established language; keep Hebrew UI strings verbatim in their own script. Do not print secrets, customer rows, phone numbers or screenshots containing personal data into this document or public PR descriptions.

## 1. Mission and definition of done

**One testable sentence:** Unit A lets a GT salesperson open a B2B lead from staff email, record a real contact and next action without losing work, and receive correctly owned tasks from verified events, while the sales interface passes a fresh UX gate and the exact release is simplified and verified.

| # | Condition | Observation that proves it false |
|---|---|---|
| D1 | All nine Unit A tasks are complete on isolated, reviewable backend/portal branches, with the plan's per-task RED→GREEN/commit ledger and interface rulings. | A task has no tested result/commit, an interface changed silently, or code was authored on `main` without an isolated workspace. |
| D2 | Staff alert and reminder make `פתח את הליד` the primary path, with no direct phone/WhatsApp/email escape; a signed-out email link lands on the intended lead after login. | HTML/text includes a direct channel action or an autolinkable number; login drops `?lead=<uuid>`; external or protocol-relative redirect works. Prove with email tests and a real browser auth/deep-link test. |
| D3 | A substantive result from Today, Leads **and Attention** saves at least five trimmed characters, one action and date (or waiting review date), event/outcome/tasks atomically; quick no-answer/outbound WhatsApp does not claim a conversation. | A four-character note or missing date persists; any entrypoint still sends answered to legacy `/outcome`; a retry duplicates or a changed payload reuses a request ID; timeout loses the draft. Prove with SQL/API tests and browser paths. |
| D4 | Task ownership and source identity stay truthful: exactly one intended task per source, one personal owner or a manager queue, stable ID on reassignment, an actionable contact-gap route and no draft shown as won. | Two reps see the same unowned work, webhook/retry doubles a task, a contactless lead gets an impossible call, a closed task vanishes without history, or a draft lights conversion. Prove with pgTAP, role API tests and browser queue tests. |
| D5 | Waiting, raw inbound reply/echo, opt-out, lost and verified order stop or alter the existing wake path at the **send boundary**, including both WhatsApp lines, shared phones, forced runs and a real stop/send race; a waiting review date never itself sends a message. | A raw `order_intake.wa_event_log` reply commits before send yet the message is sent, or an email outcome reactivates an older call anchor. Prove with two-connection disposable-Postgres interleavings, wake unit/integration checks and runtime flag inspection. |
| D6 | The GT Pulse first slice is fact-backed and usable on the current CRM: clear action hierarchy, source-linked lead rail, Hebrew RTL, keyboard-safe result sheet and no horizontal page scroll at the approved mobile widths. | A visual node asserts an unrecorded fact, a contact/save control is hidden by the keyboard, a 320/390/430px screenshot overflows, or reduced-motion/keyboard use loses meaning. Preserve before/after screenshots and browser assertions; widths come from approved plan `docs/superpowers/plans/2026-09-29-gt-pulse-a-sales-task-loop.md` Task 9. |
| D7 | Run a **fresh sales-specific, render-grade** `/ux-release-gate` after implementation, fix every verified P0/P1 in the Unit A corridor and relevant small usability defects, then rerun the affected flows and full five-lens gate. | The final consolidated report has an unresolved P0/P1, a route/role/state was not inspected, an asserted fix lacks a source and before/after proof, or the verdict relies on a mock-only screen. See W2. Structural B/C findings are named and scoped honestly, not silently declared fixed. |
| D8 | Run simplification **after gate remediation** on both diffs, apply safe cuts, then whole-branch review and `superpowers:verification-before-completion` on the exact final heads. | A needless duplicate path remains without a reason, a cut removes validation/a11y/audit history, review finds unaddressed Important/Critical behavior, or any claimed passing command was run before the final changes. |
| D9 | Backend migration, API and portal are deployable in the safe order: additive schema/API → portal → `activity_required` after proof, with an idempotent, previewed backlog and rollback. A production backlog write has separate written mass-write approval after exact counts are shown. | Migration number collides, portal Mode B/amendment or tranche is absent, old answered callers remain when flag switches, customer outreach is enabled, backfill runs without the specific approval or duplicates work, or rollback needs deleting history. Verify exact SHA, migrations and flags on target before release. |
| D10 | Final report states exact SHAs, commits/PRs, command outputs and counts, UX gate verdict, screenshot/report paths, runtime state and outstanding human action. This masterprompt's status is stamped only to match reality. | A green claim refers to another SHA/environment, a PR is open/red yet called shipped, or the `LIVE` status is changed to `SHIPPED` before the agreed release evidence exists. |

### 1.1 Settled — do not reopen

The requester approved the written specs and Native execution on 2026-09-29. The CRM customer is the **business buying from GT**, never the café's end consumer. Use the existing system and GT Pulse visual direction, not a purchased UI template or a new CRM frontend. `פתח את הליד` is the staff email's main action. A meaningful contact requires a note of at least five trimmed characters and a next action/date or waiting review date. The agent confirms notes/tasks; no AI summary, server transcription or new outreach is in Unit A. Order history/account cycle, calibrated retention and expansion, and AI are subsequent Units B–E. Do not stretch this run into them to make a visual element look complete.

## 2. Ground truth — observed 2026-09-29; re-verify at boot

### 2.1 Built and documented

- Approved documents: `Sales-Machine` branch `design/gt-pulse-crm`; the plan and its governance/race corrections were saved at remote commit `eee47fd260c8cf2209ea3c0e5ce7121aa567431f`. It explicitly includes Attention, because `gt-factory-os-portal/src/app/(sales)/sales/attention/page.tsx` also calls the legacy outcome mutation.
- `gt-factory-os` default head was `0e3c6fb49f82e9f9bddf38e478d78c17f2173878`. It has `sales_core.org/lead/lead_event`, outcome/next-touch functions, staff email in `supabase/functions/sales-leads-poll/_lib/email.ts`, and a wake sender in `api/src/order-intake/sales/wake.ts`. The next migration slot appeared to be `0362` after `0361`; this is a **recheck requirement**, not an allocation.
- `gt-factory-os-portal` default head was `5e45b2d91cc8938ec1945925e46f481b9146c404`. The active tranche file said `184`, built in PR `#235` for unrelated catalogue work. It must be cleared before creating the sales tranche; the plan's `185` is conditional. Today, Leads and Attention use outcome capture; middleware used only pathname for signed-out redirect, losing the lead query.
- `gt-factory-os-production-brain` default head was `283566bb523fe5dd2fe142bc22ae11fc7f077b82`. At inspection its `active_mode.json` said Mode A and `runtime_ready.json` had no sales/lead form signal. `EXECUTION_POLICY.md` §W2 modes requires a fresh, bounded, user-authorized pan-form amendment for a multi-screen corridor; a portal tranche alone is insufficient. Auth changes also have a written-approval gate. Its `.claude/commands/ux-release-gate.md` coordinates five read-only lenses and a governor verdict. The previous sales gate work in portal tranches `171` and `172` found and fixed defects on earlier code; it is **history**, not a pass for the new build.

### 2.2 Numbers and runtime not yet established

Do **not** invent current lead/task counts, active migration numbers, cron success, WhatsApp delivery, production feature flags or deployment SHAs. The repository observations above are dated code facts, not proof of production state. At boot record counts and last-success timestamps through authorized read-only access, with sensitive rows redacted. If production access is unavailable, identify the missing runtime proof explicitly and use a staging/local throwaway DB for development. A successful cron POST alone does not prove a customer message was delivered or even that the handler succeeded.

### 2.3 Not built in the observed plan baseline

There is no approved Unit A task source of truth, atomic activity command, waiting guard at wake send, or complete mobile GT Pulse rail. The code may have advanced by paste time; measure instead of rebuilding existing work.

### 2.4 Known adjacent work

The plan's portal tranche cannot share the catalogue tranche. Factory production, Shopify order truth, existing customer ordering and café end consumers are outside this build. No service promise or retention score may be inferred from a draft order, a stale Shopify snapshot or an open policy question.

### 2.5 Re-verification block

Run from clean checkouts of the four repositories, changing the root names if your workspace differs. Record outputs with UTC timestamps and full SHAs in the ledger; do not paste secrets or customer rows. Use the repository's authorized database tooling for the read-only queries after inspecting its schema.

```bash
git -C Sales-Machine status --short --branch
git -C Sales-Machine rev-parse HEAD
git -C gt-factory-os status --short --branch
git -C gt-factory-os rev-parse HEAD
git -C gt-factory-os-portal status --short --branch
git -C gt-factory-os-portal rev-parse HEAD
git -C gt-factory-os-production-brain rev-parse HEAD
rg -n '"w2_mode"|"w2_scoped_form"' gt-factory-os-production-brain/.claude/state/active_mode.json | head -8
rg -n '"form": "(Sales|Lead|CRM)' gt-factory-os-production-brain/.claude/state/runtime_ready.json | head -20
cat gt-factory-os-portal/docs/portal-os/tranches/_active.txt
rg --files gt-factory-os/db/migrations | sort | tail -12
rg -n 'useOutcome\(|/outcome|OutcomeSheet' gt-factory-os-portal/src/app/\(sales\)
rg -n 'SALES_CUSTOMER_OUTREACH_WRITE_ENABLED|activity_required|lead_wake' gt-factory-os/api gt-factory-os/db/migrations | head -80
```

Inspect the active tranche manifest and open PRs, migration history in the target database, actual deployed backend/portal SHA and outreach/cron flags with read-only calls. Count relevant open leads by owner/unowned and existing task-equivalent states **without exporting rows**. Run the existing backend/portal tests named by the plan **before edits** and mark inherited failures. If a repo or test environment is unavailable, keep that proof red; never substitute a code search or a mocked 200 for runtime verification.

## 3. The hard parts

1. The email button is only end-to-end if the login redirect preserves the lead UUID and staff cannot bypass the CRM with a direct channel link in the same email. A mail-client-autolinked plain phone number is also a bypass.
2. A note, outcome, next action, owner and due date form one business event. Client-only validation or an optimistic UI cannot substitute for an atomic, idempotent server write and durable draft on network failure.
3. `lead_event` records facts; a task represents work. Outbound attempts, automatic sends, a Shopify draft and a genuine reply have different meanings. Dedupe keys must include source identity and lead identity; reassignment moves open work without cloning history.
4. `ממתין ללקוח` is a backend send guard, not a label. `worker.ts` logs a reply through `store.logEvent` to `order_intake.wa_event_log` **before** dispatch; wake reads that raw table. A later lead_event lock alone misses this race. Order the raw inbound insert and the send under the same per-lead lock for every active lead sharing the phone, including the order line and echo, and test both commit orders. An email outcome must not revive a previous call anchor.
5. A sales UX gate must watch a salesperson complete the workflow, on mobile and desktop, in Hebrew RTL, with true data. A visually convincing card that invents a conversation, owner, order or customer health is a P0 truth problem.

## 4. Workstreams — execute in this order

### W1 — Build Unit A with Native Superpowers

Use `superpowers:executing-plans` on `Sales-Machine/docs/superpowers/plans/2026-09-29-gt-pulse-a-sales-task-loop.md` and both approved specs. Complete Tasks 1–9 **as a staging-proven build**, their red/green tests, independent repo commits and ledgers. This plan is external to both runtime repos: pass its **absolute path** to `sdd-workspace`, `task-start`, `task-done` and `review-package`, and invoke those scripts from the **owning repo's worktree** (backend Tasks 1 and 3–6; portal Tasks 2 and 7–9). Each script resolves git HEAD in its current repository. Maintain two per-repo ledgers plus a small execution index mapping task, repo, BASE..HEAD, and deferred/ruling status; never fabricate one cross-repo range. Run whole-branch review packages separately for backend and portal. Task 9 prepares the backlog and rollout; its production flag/backfill happen in W4, after the UX gate and simplification. Refresh file names/migration/tranche before editing; record plan rulings. Implement backend and email first. Before **any** portal code, inspect brain Mode A/B, the exact sales RUNTIME_READY signal and the bounded multi-screen amendment in §6-A; have the governor record the authorized mode and required backend evidence. Clear the unrelated active tranche, then create the sales manifest. If Task 2 is blocked by governance, record it as deferred (not complete), execute backend Tasks 3–6 and return to Task 2 before Tasks 7–9. If authorization remains unaccepted, present the concrete amendment for approval rather than editing in Mode A. Keep the legacy answered path until Today, Leads **and Attention** have moved; gate `activity_required` only after exact deployed SHA and rollback proof. No new customer send is authorized. Read the current Supabase skill/guidance when touching its schema; follow backend migration naming and privilege rules.

**Acceptance:** D1–D6 and the implementation portion of D9.

### W2 — Sales-specific UX Release Gate, remediation and second look

After W1 is working in a browser, invoke the brain's `/ux-release-gate` as a **read-only audit**. If its command or agent dispatch is not exposed in your harness, read the command and auditor definitions and run equivalent five-lens reviews yourself; state the method honestly. Create a short sales brief in the gate record: target is GT's internal B2B sales workspace (`/sales/today`, `/sales/leads`, `/sales/attention`, `/sales/orgs`, `/sales/settings` and the entry from staff email). The portal's sales language exception is Hebrew RTL. Never apply the customer-ordering portal brief or ops English/LTR rubric to this surface.

Capture render-grade evidence with the repository's sanctioned dev-shim or authenticated staging browser, not a fake-session header. Include rep and manager roles; 320/390/430px and desktop per approved plan `docs/superpowers/plans/2026-09-29-gt-pulse-a-sales-task-loop.md` Task 9; light/dark and reduced motion; keyboard focus and iPhone-sized keyboard-open result sheet. Walk the **actual** email → login → correct lead → call/WhatsApp arm → return → note/action/date → task → completion flow, plus Attention card/drawer, quick no-answer, waiting/reply, permission denial, unassigned/contactless, timeout/reload and empty/error states. Inspect the connected API/event evidence so the rail and colours never claim an unverified fact. Use screenshots for visual findings and file:line/response for flow, interaction, copy, accessibility and truth findings. Redact personal data.

Have the governor verify each auditor finding against current code/runtime, dedupe overlaps, grade severity × effort and issue one ranked report. The gate itself never edits code. In a portal tranche whose manifest includes every touched file, fix **all verified P0 and P1** affecting Unit A or the current sales workflow, plus small, demonstrable P2 defects that prevent comfortable daily use; add a failing reproduction for behavioral findings and confirm green. Fix a backend root cause in the backend repo when needed. If an apparent finding actually requires Unit B/C order history or an unapproved service policy, document it as an explicit scoped blocker/dependency instead of fabricating data. Run a second five-lens gate on fresh renders after remediation; if a fix exposes another P0/P1, repeat until zero or report HOLD without pretending to ship. The final gate verdict must state its real threshold and whether any conditional approval remains.

**Acceptance:** D6–D7. Save the read-only gate report under the brain command's permitted report path, and the authorized portal tranche/remediation evidence where its rules allow. A prior gate's SHIP verdict cannot be reused.

### W3 — Simplify, then whole-branch review

After W2 fixes, invoke the installed `/simplify` skill/command if actually available; do not claim it ran merely because this document names it. Also read and apply brain `.claude/skills/ponytail-review/SKILL.md` to both backend and portal diffs. If `/simplify` is unavailable, perform an explicit equivalent pass and label it as such. Trace code first, then remove redundant branches, speculative abstraction, duplicate validation/formatting, dead UI and unnecessary dependencies. Preserve atomicity, idempotency, authorization, error recovery, source links, Hebrew RTL and accessibility. Record cuts and deliberately retained complexity with reasons, implement safe cuts, and rerun their meaningful checks.

Now complete Native `executing-plans`' whole-branch review with a fresh reviewer if the tool is available, under `superpowers:requesting-code-review`; provide the spec, plan, ledger rulings, review focus, both final diffs and the UX gate record. Fix Important/Critical findings with RED→GREEN tests and a green suite; document minor/rulings exactly as that skill requires. If no independent reviewer is available, report the weaker self-review explicitly; do not call it independent.

**Acceptance:** D8's simplify and review portions. No post-review code change is exempt from final verification.

### W4 — Verification before completion and controlled release

Load `superpowers:verification-before-completion` and rerun the **full applicable** commands on the final backend and portal heads: SQL pgTAP around the new migration and neighboring sales migrations; root/backend typecheck and Node/Vitest suites; portal typecheck, lint, unit tests, focused and whole relevant sales Playwright, `portal-pr-guard` and repo CI. Verify route-to-API-to-DB state transitions on a throwaway/staging database, not just mocked responses; read outputs, exit codes and counts. Re-run the sales UX gate if simplification touched its behavior or rendering. Check release verifier/lane safety separately; UX SHIP is not release approval.

Prepare backend-first and portal-second reviewable PRs with migration/flag order, data backfill preview, rollback steps and exact screenshots. Do not apply a data migration to production before schema/security/code review and a local/staging proof. Brain `CLAUDE.md` §Authorization permits autonomous merge/deploy on green, verified gates with an announcement; follow the current policy, not a generic blanket approval request. On the exact authorized target SHA, verify migration applied, API serving, portal serving, flags and task counts. Only then turn on the internal `activity_required` gate with an audited write if its current setting is not classified as a frozen flag and the old answered paths are gone; otherwise request the specified written approval. Keep `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` frozen and never send a test or marketing message to a real customer in this program. An existing cron/wake path must be observed and guarded, not assumed inactive. **Production backlog insertion is mass-scale:** prepare an idempotent script, staging proof, exact production dry-run counts, affected-scope summary and rollback; obtain written go/no-go for that specific batch before writing. If approval is pending, D9 stays HOLD and the final report names the sole next action. Do not call preview-only work production-deployed.

Finally update Sales-Machine `CURRENT_STATE.md` only with dated, observed state (and open unknowns), stamp this document `SHIPPED` only after the agreed shipped/runtime proof exists, or leave it `LIVE` with a dated blocking reason and exact next action. No fake green, no open-ended "later" in a success report.

**Acceptance:** D8–D10.

## 5. Scope and boundaries

**IN:** Unit A implementation in the backend and current sales portal; staff alert; honest task/event and waiting logic; first GT Pulse visual slice; sales-specific five-lens UX gate and its in-scope fixes; simplification, whole-branch review, tests and controlled rollout evidence.

**OUT:** factory inventory/production core; customer ordering journey or Shopify order semantics; every café end consumer; full B2B account/order history, retention scoring, expansion maps, AI/transcription; a purchased CRM template; changes to customer-facing WhatsApp copy, sends or outreach flags; guessed service policy; repository-wide portal redesign. Do not use scope OUT to excuse a regression in an existing sales entrypoint touched by Unit A.

## 6. Requester's part — the complete human-only actions

**A. Bounded portal amendment, only if governance does not accept the existing written approval.** The requester's 2026-09-29 approval covered the approved Unit A plan, its explicit middleware/login/callback changes, the existing sales UI and Native execution. The user pasting this document also authorizes requesting the following **one** W2 pan-form sales-corridor amendment, subject to brain `EXECUTION_POLICY.md` §W2 modes and the governor's check:

- **Plan and corridor:** the approved Unit A plan §§Global Constraints, File Map and Tasks 2, 7–9; the current `/sales/today`, `/sales/leads`, `/sales/attention`, and sales-only `/sales/orgs`/`/sales/settings` findings from W2. No general portal Mode B.
- **Allowed portal paths:** `src/app/(sales)/**`, `src/app/api/sales/**`, `src/middleware.ts`, `src/app/(auth)/login/page.tsx`, `src/app/auth/callback/page.tsx`, `src/lib/auth/safe-redirect.ts`, relevant `tests/unit/sales/**`, `tests/e2e/sales*.spec.ts`, `tests/e2e/mobile-sales-today.spec.ts`, and only the new sales tranche/registry/active pointer under `docs/portal-os/`. Every touched path must also be explicitly listed in that tranche manifest. Auth edits are limited to preserving and validating the approved sales deep link; no unrelated login behavior.
- **Forbidden:** all `(ops)`/factory/inventory paths, customer checkout and Shopify ordering, portal browser-to-DB writes, new outreach, unrelated auth, and paths absent from the tranche. Brain/backend files remain in their own lanes.
- **Entry:** verified backend endpoint shape and a current `RUNTIME_READY` authorization for the corridor's consumed contract, current Mode A/B checked, no colliding active portal tranche; governor records the authorized bounded mode without overwriting prior signal history.
- **Exit/expiry:** per-tranche typecheck, build, lint, touched-surface smoke and role-matrix walkthrough, then UX gate/review; return `active_mode.json` to A when the corridor closes. This amendment expires when Unit A tranche closes or on 2026-10-13, whichever comes first. A delayed paste requires a fresh authorization check.

Do not treat a plan approval, tranche or this agent-authored explanation as a self-issued runtime signal. If the governor/policy requires a separate explicit assent to the amendment text, present this exact bounded request after completing backend work and wait before portal authoring. New Hebrew copy outside the approved spec/existing register needs its exact proposed register entry and the policy's user approval; collect it in the same concrete checkpoint rather than guessing.

**B. Production backlog write:** This is a distinct, mandatory written go/no-go because it inserts tasks for many existing leads. Ask only after the code, staging dry run, exact production preview counts by type/owner, affected scope, rollback and UX/release evidence are ready. No approval by elapsed time. A refusal or missing approval leaves the batch unrun and D9 on HOLD.

No other product-design decision is needed. Brain `CLAUDE.md` already permits autonomous merge/deploy when its gates are met; announce as required, without asking a redundant generic permission. If a genuinely new service policy is required, isolate that path, finish independent work and ask only the policy question with evidence. Do not request tokens or customer data in chat. Customer-facing outreach activation is outside this run.

## 7. Landmines — do not rediscover these

1. **The plan still says `0362`/`185`** — those were free in the 2026-09-29 snapshot, not reservations → list migrations and portal tranches immediately before creating either; portal `184` was active in PR `#235`.
2. **An email link looks correct but loses its lead after login** — portal middleware used pathname without search → verify the signed-out redirect and safe same-origin callback in a browser. Plain phone strings in mail can also become tappable links.
3. **Today/Leads work while Attention fails after the flag switch** — Attention also mounts `useOutcome` and `OutcomeSheet` → the approved plan now names its card and drawer explicitly; grep all current callers before gating the legacy route.
4. **Three agents see a no-owner lead** — old Today query included `assignee IS NULL` for personal scope → enforce the owner filter in Fastify, not merely the UI.
5. **Two visually identical tasks come from one event** — event UUID is not always external identity and one activity may have extra actions → key by lead/source/external ID or request/action ordinal, compare retry payloads and preserve stable task IDs on reassignment.
6. **A waiting chip appears while a wake send escapes** — a pre-claim UI check or lead_event lock does not serialize the raw `wa_event_log` write: `worker.ts` logs it first → lock that inbound/echo insert for every affected lead on the phone, test both lines and shared phones with two DB connections; never infer safety from a pure `decideWake` unit test alone.
7. **The lead rail shows a successful order or conversation too early** — Shopify draft is not won, outbound WhatsApp is not a reply and old snapshots can be incomplete → derive nodes from committed, named events and evidence links.
8. **`CURRENT_STATE.md` has two `U-016` references** — the Knowledge-book `U-016 (→ אלכס §4)` is the unresolved service question; the other concerns Meta → cite the full row, never use the number alone.
9. **A prior sales UX gate once said SHIP** — tranches `171`/`172` audited older code and initially missed an Attention drawer path → run a fresh gate on this diff, every entrypoint, role and state, then review the remediation itself.
10. **A cleared tranche is not portal authorization** — brain Mode A and no sales RUNTIME_READY were observed on 2026-09-29; multi-screen authoring also needs the bounded amendment in §6-A → check signals/mode and governor before Task 2. The approved plan explicitly names auth files but new Hebrew copy still needs its register gate.
11. **A green build is not production proof** — code SHA, migration application, feature flag and browser behavior can differ at runtime → verify the exact target after authorized deployment, or report ready-for-release rather than shipped. A staging backfill is not consent for the production batch; see `gt-factory-os-production-brain/CLAUDE.md` §Authorization.

## 8. Additional halt conditions

- A change would touch factory core, silently reassign a B2B business, assert unverified order/retention facts, send to a customer or bypass the frozen outreach flag → **STOP that path** and surface it; complete safe independent work.
- Portal tranche `184` or its successor still owns the relevant paths, or a migration slot is occupied → **do not edit outside a manifest or overwrite a migration**; resolve the coordination gate first and update the ledger/plan ruling.
- Brain Mode B authorization, the corridor amendment or backend readiness signal is absent → **HOLD portal authoring**, finish safe backend work and present §6-A if needed. Do not manufacture a RUNTIME_READY signal or silently treat the tranche as approval.
- A P0/P1 remains in the final Unit A sales gate, a required test/CI is red, or a runtime check cannot run → **HOLD**; do not use conditional language to call it production-grade.
- Security/role isolation, personal data in an artifact, or a production data backfill cannot be proved safe or lacks the written batch approval → **HOLD** the affected release/write and present the concrete blocker, not an invented workaround.

## 9. Final report

Reply in concise Hebrew with:

1. What a salesperson and manager can now watch working end to end; distinguish preview from production.
2. D1–D10 PASS/HOLD with exact evidence links, final SHAs, migration/flag state and command counts; no partial credit.
3. UX gate report: scope, five dimensions, initial findings, fixes, final P0/P1 counts and verdict, representative before/after screenshots with data redacted.
4. Simplification cuts, independent review findings/rulings and verified post-cut checks.
5. Backend/portal PRs or merge/deploy links, rollback, remaining blockers and the **single** next human action, or `לא נדרש ממך כלום` if none.

Stamp this file's status only according to W4 and link the stamped version. If anything is not ready, say that first and plainly.
