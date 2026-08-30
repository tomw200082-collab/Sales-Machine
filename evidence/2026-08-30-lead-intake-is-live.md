# Evidence snapshot — the Make intake was built, is live, and has a two-week hole (2026-08-30)

> **Immutable. True as of 2026-08-30 only.** Never edit; supersede with a newer dated snapshot.
>
> **Authority: `system_verified`.** Read directly from the live Make account (team 1240098)
> via its API, and from the live Supabase project `rvadsozabmxkkrktwgnv`.
>
> **This snapshot corrects two things this repo asserted and one thing Claude repeated.**

## What the repo said, and why it was wrong

`CURRENT_STATE.md` recorded, on 2026-08-24:

> "**Still open:** the two Make scenarios (lead transport + hourly pulse) are not built —
> awaiting Tom's go-ahead"

That was true when written and stopped being true the same day. Tom built both scenarios on
2026-08-24, starting at 11:40 and finishing with an edit at 16:50. The note was never updated,
so the repo has carried a stale "not built" for six days — and on 2026-08-30 Claude read it,
believed it, and told Tom his leads were not flowing anywhere. They were.

The lesson is the repo's own rule 4, failed in the one direction it does not usually guard:
**a fact that was checked once and then went stale reads exactly like a fact that is true.**
`CURRENT_STATE.md` is the sole authority on build status precisely so this cannot happen;
here it was the source of the error.

## What is actually true

### The scenarios exist and are active

| Scenario | ID | State | Modules | Since |
|---|---|---|---|---|
| `GT Sales — lead intake → /ingest` | 7075235 | **active**, instant trigger | facebook-lead-ads `NewLeadMultiple` → `TransformToJSON` → http `MakeRequest` → `Break` | created 2026-08-24 11:40, last edit 16:50 |
| `GT Sales — hourly pulse (proves the Facebook connection is alive)` | 7075243 | **active**, hourly | facebook-lead-ads `GetForm` → http `MakeRequest` | created 2026-08-24 11:41 |

The Facebook connection they run on: `gteveryday` (id 6309050), OAuth, 9 scopes, authored by
Tom Witt, **valid to 2026-10-23** — the reauthorisation D-006 describes.

### The pipeline works, proven at the far end and not at the near one

`status: 1` (success) on every `EXECUTION_END` from 2026-08-24 14:20 onward, including
2026-08-29 20:16. The only two `status: 2` runs are 13:44 and 13:53 on 2026-08-24 — both
**before** Tom's final edit at 16:50, i.e. setup-day churn, not live failures.

A successful Make run only proves the HTTP call returned. What proves the lead exists is the
table. Counted in `sales_core.lead`:

| Day | Source | Leads |
|---|---|---|
| 2026-08-29 | `facebook` | 1 |
| 2026-08-28 | `facebook` | 1 |
| 2026-08-27 | `facebook` | 2 |
| 2026-08-26 | `facebook` | 1 |
| 2026-08-25 | `facebook` | 1 |
| 2026-08-24 | `facebook` | 5 |
| **2026-08-10 → 2026-08-23** | **— nothing —** | **0** |
| 2026-08-01 … 2026-08-09 | `import_meta_export` | 11 |

This also settles U-020 without reading a secret: leads with `source = 'facebook'` are landing,
so `LEAD_INGEST_TOKEN` is set and correct — an unauthenticated POST returns 401 and writes
nothing.

### The hole: 2026-08-10 to 2026-08-23

Fourteen days with zero leads, between the manual Meta export (imported as
`import_meta_export`, last row 2026-08-09) and the moment the scenario went live
(2026-08-24 14:20).

At the observed rate of the live days — 6 leads over 5 days, ~1.2/day — the hole is
**roughly 15–20 leads that reached Meta and never reached us**. They are still retrievable
from Meta's Lead Center: retention is 90 days, so the earliest of them expire in early
November 2026.

`inferred`, and the estimate is a rate extrapolation, not a count. The real number comes from
the export, not from this file.

Recovery path: export the range from Lead Center and POST it to `/ingest`. The route derives a
stable `external_id` from the normalised phone plus `created_at`, so re-posting a lead that is
already stored is idempotent and cannot duplicate.

### Two items in the dead-letter queue

`dlqCount: 2`, `allDlqCount: 5` on scenario 7075235. Not yet inspected. Each is a lead that
entered the scenario and did not complete, so they are additional to the hole above.

## What this changes in doctrine

**D-008 is wrong as written** and is corrected in `doctrine/decisions.md` in the same commit.
It proposed *not building* the Make lead-transport scenario, on the reasoning that D-007 would
leave it no form submissions to carry. The scenario was already built and has been carrying
leads for six days. The live question is not whether to build it but **when to retire it** —
and the answer is: when the lead-form campaign is actually paused, not before, because until
then it is the only automatic capture GT has.

D-007 is unaffected. Nothing here touches the CTWA decision.

## What was not checked

The contents of the two dead-letter items. The exact count of leads in the 2026-08-10 → 2026-08-23
hole, which needs the Lead Center export. Whether the `errors` counters Make reports on the
scenario list (32 of 48 on 7075235, 9 of 113 on 7075243) count retried operations rather than
failed runs — the per-execution record shows no live failure after setup, so the counter and the
execution log disagree and the counter was not trusted.
