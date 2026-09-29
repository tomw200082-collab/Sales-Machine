<!-- Dated evidence snapshot. Authority: system_verified for cited CI/refs and read-only counts; unknowns remain explicit. Not a release-status authority. Captured 2026-09-29T20:00:13Z. -->

# GT Pulse A execution index — 2026-09-29 UTC

Plan: Sales-Machine/docs/superpowers/plans/2026-09-29-gt-pulse-a-sales-task-loop.md at 7ee2e4921d45869a21221cc3ba8baee71a6fdea6.
Method: Native executing-plans; no subagent dispatch. This index records actual evidence, not completion claims for Unit A.

## Baseline

- Sales-Machine remote design branch: 7ee2e4921d45869a21221cc3ba8baee71a6fdea6; local checkout was older 725800487dfa9ef7e1113d19a8a6d6c48fd23bce.
- Backend main: 0e3c6fb49f82e9f9bddf38e478d78c17f2173878; private Git clone denied local credentials. GitHub connector read/write works.
- Portal main: 5e45b2d91cc8938ec1945925e46f481b9146c404. Pointer _active.txt=184; PR #235 is merged, but pointer remains set.
- Production brain main: 283566bb523fe5dd2fe142bc22ae11fc7f077b82. active_mode=A; 36 RUNTIME_READY signals, none for sales/lead/CRM.
- Backend migrations in Git stop at 0361; 0362 free at baseline. Supabase migration-history tool does not list 0360 or 0361, while live lead.opt_out_at, customer_portal.lead_submission and lead_wake_sequence cron exist. Resolve history/source discrepancy before release.
- Read-only DB count: 254 leads, 180 open, 147 open unassigned, 33 open assigned. Lead wake cron active every 15 minutes; 84 cron invocations in prior 24h reported succeeded, not evidence of handler success or customer delivery. One test phone in allowlist. activity_required not present. sales_core.task absent.
- Exact Railway environment flag and deployed SHA not established. No customer outreach or backlog write authorized.

## Task map

| Task | Repo | Baseline..HEAD | Evidence / state |
|---|---|---|---|
| 1 | backend | 0e3c6fb..9eb7bec | Branch feat/gt-pulse-a-sales-contact-loop. Local exact-blob Node test 36/36 inherited; new tests RED 30/38; fixed 38/38. Commits 148b010, 26ab6fe, de48c6f (branch CI), 9eb7bec (private checkout artifact). First CI on de48c6f success; artifact CI pending. No deployment. No full backend suite yet. |
| 2 | portal | — | Deferred: Mode A, no sales RUNTIME_READY, no accepted pan-form amendment, active tranche pointer 184. |
| 3 | backend | 9eb7bec..f2ae352 | Complete. RED 36604284817; GREEN 36604827253, pgTAP 20/20 and five neighboring suites. |
| 4 | backend | f2ae352..ab9c4dd | Complete. RED 36605201123; GREEN 36605691650, pgTAP 41/41. Flag seeded false. |
| 5 | backend | ab9c4dd..5d1e1f5 | Complete. RED 36606122237/36606133684; send-lock defect caught by 36607552092; GREEN 36608260353, pgTAP 54/54, real DB race 7/7 and lead DB 11/11. |
| 6 | backend | 5d1e1f5..12fa6c3 | Complete with post-task corrections and HTTP contract proof. RED local missing export, CI 36620099225, whitespace boundary CI 36621392854, Attention ownership CI 36621987187; GREEN CI 36622854116: pgTAP 65/65, DB 18/18, role API 8/8, legacy workspace 14/14. |
| 7–9 | portal | — | Blocked behind backend contract and portal governance. |

Ruling: Task 1 used an approved exact CTA and existing contact-gap strings; no new Hebrew register copy. Did not include a new contact-details hint to avoid an unapproved copy change. Cost if wrong: staff mail may need one short hint after Tom approves a register entry.

Ruling: GitHub connector could edit private backend but shell clone had no credentials. Added a private branch-only CI workflow to produce a Git bundle for local worktree verification; it contains no production secrets or DB access. Cost if wrong: this test workflow is one extra scoped file and may need removal after release.

## Gates

- D1–D10: HOLD until Unit A end-to-end evidence. Task 1 alone is not a deployed contact loop.
- Production schema, API, portal, activity_required and backlog: unchanged.
- Staff email code on backend feature branch only; the production email still has the old direct-channel actions.
- Next gate: obtain a current sales RUNTIME_READY authorization and Tom's bounded W2 pan-form amendment, then clear the unrelated portal tranche and execute Tasks 2, 7–9. No portal authoring in Mode A.

2026-09-29 UTC update: Tasks 3–6 complete as above. CI disposable bootstrap skips 48 unrelated factory migrations; release needs target migration-history proof. No production DDL/write. Latest backend branch f7ac92c080d8b402eb67ab528771954f16c583b7; portal untouched. Brain still Mode A/no sales RUNTIME_READY and portal `_active.txt` still 184 at read-only recheck.

2026-09-29 UTC update: Attention ownership test RED 36621987187, fix GREEN 36622265795. Backend branch f32505afe7b0e1287796f7f0737875bd3be44bc2, local exact Git bundle synchronized; no production write. Supabase read-only branch list has only the main branch and an old `bom-cluster-shadow` branch in `MIGRATIONS_FAILED`, not a healthy sales staging target. Brain still Mode A with no sales RUNTIME_READY.

2026-09-29 UTC update: backend head 12fa6c3586116f8ebc5e49e62a0b1ce308537d4d, CI 36622854116 green for the targeted sales chain including in-process Fastify activity -> DB -> task -> completion and retry. Local blob matched CI bundle; worktree clean. Full `api npm test` remains unproven: tsx IPC EPERM locally, fallback fails without `.env` against unrelated live-DB-dependent suites. API package typecheck retains unrelated existing diagnostics; root typecheck passes. No sales RUNTIME_READY signal can honestly be recorded as a full-release pass. Portal and production untouched.
