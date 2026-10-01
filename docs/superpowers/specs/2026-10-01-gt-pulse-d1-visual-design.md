# GT Pulse D, phase 1 — visual pass on Today, the lead and the result sheet

**Date:** 2026-10-01 (iteration 2 the same day) · **Status:** approved direction — Tom: "קודם A ואז D שלב 1, תמשיך בכל
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
| V6 | **Amended 2026-10-01 (Tom: "הרבה יותר חי … אנימציות חיות"):** motion is part of the language. Arrivals rise on a spring, one after another. The journey draws itself in. Light travels the lead path. A count that grows on a real change pings once (never on first load or on a scope switch). Every motion stops under `prefers-reduced-motion` and leaves the final picture. Only transform/opacity (and the SVG stroke offset) animate. | Tom's iteration request; taste-skill MOTION 7 with its reduced-motion and GPU rules; ui-ux-pro-max: motion carries meaning, no linear UI easing. |
| V7 | Rubik stays; tabular numerals for dates/counts. No new font or dependency. | Shortest path; Hebrew coverage already proven. |
| V8 | **Shape lock:** controls are pills, fields 14px, cards 22px, bands and sheets 28px. Depth is a three-layer shadow tinted to the petrol hue. The primary action's icon sits in its own round well (button-in-button). | taste-skill shape-consistency lock; soft-skill soft structuralism. |
| V9 | **Hero, the journey flow:** in the Today band, four orbs on one river (received → contacted → next action set → verified order) with live counts. Each open lead is counted once at its furthest node; verified orders land in the last node; lost leads have left the path. Counts follow the queue scope. A dashed ring turns slowly around the order node: the business circle. | Program spec §8 "illuminated lead event path … into a recurring business circle"; Tom's "זרימה ויזואלית של מסע הלקוח והליד". Same rows already loaded, so no new query. |
| V10 | **Living band:** a slow aurora of the two action inks drifts behind the petrol band. Today's date (locale-formatted, not copy) sits in a pill with a breathing dot. The scope switch becomes a glass track with a turquoise thumb, and the triage counts become glass chips. The aurora's peak tint is asserted ≥ 4.5:1 against the band text in light and dark. | The band stays readable everywhere it can paint. |
| V11 | **Cards and rails in motion:** the mini rail's lit segments draw in and the current node rings twice. The lead drawer's milestones rise in turn, their connector grows, and the latest one glows. A verified-order card is crossed once by a light sweep. Cards lift under a pointer, never on touch. | One hero loop (the river) plus brief one-shot moments; ui-ux-pro-max "1–2 key animated elements per view". |
| V12 | No animation library: CSS keyframes and one `requestAnimationFrame` count-up that writes the DOM directly (no React state per frame). | taste-skill dependency verification and the no-rAF-into-state rule; zero bundle cost. |

## 3. Files (portal tranche 186)

`src/app/(sales)/sales-tokens.css`, `_components/TaskCard.tsx`, `_components/TodayCard.tsx`,
new `_components/MiniRail.tsx`, new `_components/JourneyFlow.tsx`, `_components/LeadJourneyRail.tsx`,
`_lib/leadMilestones.ts` (row-based derivation and flow counts), `sales/today/page.tsx`, tests for
the mini rail, the journey flow and the token contrast.

Skills applied: Anthropic frontend-design, taste-skill (`Leonxlnx/taste-skill`, fetched from
GitHub: `design-taste-frontend`, `high-end-visual-design`, `redesign-existing-projects`),
ui-ux-pro-max. Design read: a phone-first Hebrew sales cockpit with a premium, alive language.
Dials: VARIANCE 6, MOTION 7, DENSITY 5.

## 4. Proof

Unit tests for row → nodes; contrast assertions for every new text/background pair (light and
dark); fixture render shots before/after at 390 and 1280, light, dark and reduced motion; a recorded video of the motion; existing sales
suites green; PR `ci` green; Tom sees before/after before merge.
