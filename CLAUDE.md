# Sales-Machine — Boot Kernel (The Truth Constitution)

> **Authority layer:** boot kernel of the GT sales brain. Loaded first, every session.
> This repo is the **brain** of GT's sales machine: doctrine, knowledge, recipes,
> evidence, agent declarations. **No runtime code lives here — ever.**
>
> Governing module declaration: `gt-factory-os-production-brain` →
> `docs/decisions/modules/sales-declaration.md` (PR #46). The PRODUCTION boot kernel's
> locked decisions bind this repo wherever they touch (stock truth, frozen flags,
> factory-os core isolation).

## Identity

GT Everyday sells beverage bases wholesale to HoReCa. Revenue today is passive Shopify
reorders (87–98% monthly returning rate) with silent churn and un-captured chain
expansion invisible to every current tool. This repo exists to make the sales motion
**repeatable, system-backed, and 100% truthful** — knowledge first, agents second,
automations last.

**Tiebreakers (inherited):** reliability over elegance · trust over scope · simplest
path over irreversible complexity.

## The two kinds of truth (core doctrine)

- **Slow truth (doctrine):** ICP, pricing logic, playbooks, core story, decisions.
  Changes only by Tom's explicit decision. Lives in `doctrine/`.
- **Fast truth (live data):** who is sleeping, account values, order cadence, contacts.
  Changes daily. **May never appear in any file as an undated fact.** The repo stores
  *recipes* (how to compute — `recipes/`) and *dated evidence snapshots*
  (`evidence/`, immutable). Live numbers are always fetched fresh from source systems.

Mixing the two is the failure mode this repo is built to prevent.

## The 7 truth rules (constitution)

1. **Every knowledge card carries: source, date, and authority grade** —
   `user_confirmed` (Tom said it) / `system_verified` (checked against a live system) /
   `doc_confirmed` (cited source) / `inferred` (hypothesis). **Inferred is never
   policy.** All cards indexed in `knowledge/registry.yaml`.
2. **Volatile data = recipe + dated evidence snapshot. Never a stored "fact."**
3. **No guessing.** Unknowns are logged as `UNRESOLVED` in `CURRENT_STATE.md` — visibly
   open, never silently filled.
4. **Anything checkable against a live system is checked before it is written.**
   "Should be right" is not evidence.
5. **Tom is the sole approver of `doctrine/` and sole writer of this file.** Every
   doctrine change is dated and logged in `doctrine/decisions.md`.
6. **Knowledge expires.** Every card carries a freshness class
   (`stable` / `review_30d` / `snapshot`); periodic staleness sweeps flag overdue cards.
7. **Write boundaries:** no runtime code in this repo; an automation is built only after
   its knowledge base is verified; any customer-facing write stays behind the frozen
   flag `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` (default `false`, per the module
   declaration) and Tom's confirm-before-acting rules.

## Authority hierarchy (this repo)

1. `CLAUDE.md` (this file) — wins every conflict.
2. `doctrine/` — Tom-approved policy (with `doctrine/decisions.md` as the log).
3. `CURRENT_STATE.md` — sole authority on build status + UNRESOLVED list.
4. `knowledge/` — graded cards; trust per authority grade, never above it.
5. `evidence/` — true only as of their date; superseded, never edited.
6. `recipes/` — methods; correctness verified per rule 4.

## Repo map

```
CLAUDE.md            ← this constitution
CURRENT_STATE.md     ← build status + UNRESOLVED (sole authority)
doctrine/            ← slow truth (Tom-approved): icp, pricing-logic, core-story,
                       playbooks/, decisions.md
knowledge/           ← graded cards: market/, accounts/, registry.yaml (index)
recipes/             ← fast-truth methods: sleeping-radar, account-value, whitespace
evidence/            ← immutable dated snapshots
agents/              ← agent declarations (no agent without one)
automations/         ← deliberately empty until the base is verified
```

## Boot sequence (every session)

1. Read this file.
2. Read `CURRENT_STATE.md` (status + UNRESOLVED).
3. Read `doctrine/decisions.md` (what is decided vs. proposed).
4. Load only the knowledge cards relevant to the task, honoring authority grades.
5. Fast-truth questions → run the recipe against the live system; never quote a stale
   snapshot as current.

## Hard boundaries (inherited, non-negotiable)

- **Never touch factory-os core** (stock_ledger, balance_anchors, bom_*, items,
  components) — not read directly, not written. Catalog reads via curated views only.
- **Stock truth stays sacred** — this repo has no business writing it, ever.
- Customer-facing outreach automation: gated by `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED`
  + Tom written approval + dry-run + soak (module declaration §11).
- External writes follow PRODUCTION's External-action authorization: understand before
  writing, confirm-before-acting on high-risk/mass/customer-facing, audit + reversibility,
  when unsure — don't write, ask.
- No new authority docs, no framework layers (e.g., Ruflo/claude-flow) without an
  explicit Tom decision recorded in `doctrine/decisions.md`.

## Stop conditions (halt + surface to Tom)

1. A write would violate a truth rule (undated volatile fact, ungraded card, guess).
2. A doctrine change lacks Tom's explicit word.
3. An automation is requested whose knowledge base is not verified.
4. A customer-facing write would run with the frozen flag down.
5. Anything would touch factory-os core.

## Evidence standard

Every claimed PASS states: files changed, checks run (N/N), sources cited, authority
grades assigned, UNRESOLVED items opened/closed, Tom approvals required.

---

**Owner:** Tom (sole writer of this file).
**Created:** 2026-07-18 (Phase 0 of the knowledge-first build; drafted by Claude at
Tom's direction, pending Tom's written approval of this constitution).
