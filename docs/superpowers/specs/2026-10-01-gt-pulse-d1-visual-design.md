# GT Pulse D, phase 1 — visual pass on Today, the lead and the result sheet

**Date:** 2026-10-01 · **Status:** approved direction — Tom: "קודם A ואז D שלב 1, תמשיך בכל
הכוח" (2026-10-01), under the program spec §8 he approved on 2026-09-29. Before/after
screenshots are shown to Tom before merge.

**Parent:** `design/gt-pulse-crm` → `2026-09-29-gt-pulse-crm-program-design.md` §4 (unit D, first
stage) and §8 (visual language). Unit A is live (backend `30759a2`, portal `eb36b83`).

## 1. Scope

In: the sales corridor's colour tokens, the Today header, Today task cards and queue cards, the
lead drawer's journey rail, the result sheet. Out: business circle, contact compass, event river,
basket map (stage 2, needs units B/C); any new copy; any backend change; factory screens.

## 2. Decisions

| # | Decision | Reason |
|---|---|---|
| V1 | Palette from §8 as named tokens, light and dark: **petrol** `#0E3B43` (opening surface, primary text on action), **electric turquoise** `#19C9B9` (action fill, focus, the lit rail node), **lead blue** `#2F6FDB` (lead path, "new"), **order green** `#1E8A5A` (verified order), **review amber** `#B7791F` (waiting/review), **coral** `#E0574F` (overdue fill; text uses a darker coral). | §8, with every text pair at WCAG AA. Turquoise is never text on white; it is a fill under petrol text (contrast ≥ 7:1). |
| V2 | Primary buttons: turquoise fill, petrol label. Secondary stay outlined. | §8 "action in electric turquoise" without failing contrast. |
| V3 | Today opens on a petrol band holding the title, the scope switch and (manager) the triage counts. | §8 "opening surface in deep petrol"; it separates "where am I" from the work below. |
| V4 | **Signature:** each Today card carries a mini journey rail — four nodes (received → contacted → next action set → order) derived from the row's own fields (`created_at`, `first_touch_at`, `next_touch_at`, `converted_order_ref`). Reached nodes are filled lead-blue; the current one is turquoise; the order node turns green only on a verified order. Accessible name reuses the approved rail labels. | §8 "Today shows one clear job, why, and a mini rail"; no extra query per card, no new copy. |
| V5 | State is never colour alone: overdue keeps its text badge; rail nodes carry the approved milestone names as accessible names and a filled vs hollow shape. | §8 rule. |
| V6 | Motion: none in this phase. A pulse needs the previous rail state per card; deferred until a card outlives a save. | §8 allows motion only for a real state change; none is shown on reload. |
| V7 | Rubik stays; tabular numerals for dates/counts. No new font or dependency. | Shortest path; Hebrew coverage already proven. |

## 3. Files (portal tranche 186)

`src/app/(sales)/sales-tokens.css`, `_components/TaskCard.tsx`, `_components/TodayCard.tsx`,
new `_components/MiniRail.tsx`, `_lib/leadMilestones.ts` (row-based derivation),
`sales/today/page.tsx`, tests for the mini rail and the token contrast.

## 4. Proof

Unit tests for row → nodes; contrast assertions for every new text/background pair (light and
dark); fixture render shots before/after at 390 and 1280, light and dark; existing sales
suites green; PR `ci` green; Tom sees before/after before merge.
