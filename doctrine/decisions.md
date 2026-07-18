# Doctrine — Decisions Log

> Only Tom decides. `CONFIRMED` = Tom said it explicitly (date + context).
> `PROPOSED` = recommended by Claude, awaiting Tom's word — **not policy yet**.

| ID | Decision | Status | Date | Context |
|---|---|---|---|---|
| D-001 | The sales machine's knowledge/agents layer lives in this dedicated repo (`Sales-Machine`), separate from PRODUCTION and from runtime repos. | **CONFIRMED** (Tom) | 2026-07-18 | Tom opened the repo and directed the knowledge-first build in it. |
| D-002 | Build order is knowledge-first: constitution → seed verified knowledge → truth interviews → system reconciliation → agents (read-only first) → automations last. | **CONFIRMED** (Tom) | 2026-07-18 | Tom approved the 5-phase plan ("נשמע מצוין") with the explicit goal: 100% accurate, current, correct before building. |
| D-003 | The website (any variant: storefront work, marketing site, B2B portal) is **not** built in this repo. It gets its own runtime repo when built; its content/brief (core story, ICP, messaging) is authored here in `doctrine/`. | **CONFIRMED** (Tom) | 2026-07-18 | Confirmed in writing by Tom 2026-07-18 (ICP-interview session boot). Keeps the brain/runtime split that already works (PRODUCTION vs. portal). Site scope itself is U-008. |
| D-004 | No Ruflo / claude-flow framework layer in this repo. Native tooling (Claude Code agents, workflows, skills, this repo's registry) covers the need with full auditability. | **CONFIRMED** (Tom) | 2026-07-18 | Confirmed in writing by Tom 2026-07-18 (ICP-interview session boot). Grounded in GT's own evaluation (TEST-GT-START `docs/ruflo-session-final-report.md`, 2026-05-22): verdict "not ready for another repo", auto-hooks on every message, `auto-commit.sh`, writes outside the repo, unrequested MCP servers, untrustworthy verify summary — conflicts with truth rules 1/3/5. Revisit only if upstream blocking issues close AND a concrete gap native tooling can't fill is named. |
| D-005 | Customer-facing outreach automation stays behind `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` (default `false`) + Tom written approval + dry-run + ≥24h soak. | CONFIRMED (inherited) | 2026-07-18 | Module declaration §11 (PR #46); PRODUCTION External-action authorization. |
| D-006 | Constitution (`CLAUDE.md`: the 7 truth rules + authority hierarchy + boundaries) ratified. Phase 0 complete. | **CONFIRMED** (Tom) | 2026-07-18 | Tom approved the constitution in writing this session, alongside confirming D-003 & D-004. `CLAUDE.md` footer ("pending Tom's written approval") to be updated by Tom (sole writer of that file). |
