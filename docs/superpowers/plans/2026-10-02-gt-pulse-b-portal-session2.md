# GT Pulse Unit B portal: Session 2 execution delta

> Execution mode: inline in this session (executing-plans), TDD per task. This is a **delta** on the canonical build plan `2026-10-01-gt-pulse-b-build.md` (Tasks 24–27); it does not restate it.

**Goal:** the Unit B portal (tranches 189–191) is live in production, at UX gate P0 = 0 and P1 = 0.
**Design:** `docs/superpowers/specs/2026-10-02-gt-pulse-b-portal-design.md`.
**Stack:** Next.js 15, React 18, TanStack Query 5, Vitest + Testing Library (happy-dom), Playwright (`@mocked`), lucide-react (already a dependency; no new dependency).

## Global constraints (delta)

- Tom's delegation of 2026-10-02 replaces the plan's "stop for mockups and string round 1". Hebrew strings land in `_lib/labels.ts`, and each tranche manifest lists them as its copy register.
- Delivery: **one release PR with three tranche commits** (189, 190, 191), each with its own manifest under `docs/portal-os/tranches/`, registered in `registry.md`, and `_active.txt` set per commit. Reason: each portal merge to `main` deploys production, and 189 alone would link the list to a workspace that does not exist yet.
- No backend change. Contract findings F1–F4 (design §2) are handled in the portal.
- Fixtures are synthetic: no real name, phone, email, amount or order.
- No em dash in new user-visible strings.

## Files

| Path | Responsibility |
|---|---|
| `src/app/api/sales/orgs/page/route.ts`, `orgs/search/route.ts`, `orgs/[id]/route.ts`, `orgs/[id]/orders/route.ts`, `orgs/[id]/orders/[gid]/route.ts`, `orgs/[id]/river/route.ts`, `orgs/[id]/contacts/route.ts`, `orgs/[id]/circle/route.ts`, `identity-review/route.ts`, `orgs/owner/route.ts`, `orgs/[id]/identity/route.ts`, `contacts/[id]/[action]/route.ts` | one-file proxies (`proxyRequest`) |
| `(sales)/_lib/types.ts` | Unit B shapes, copied from `orgs_handler.ts` |
| `(sales)/_lib/api.ts` | hooks `useOrgsPage`, `useOrgSearch`, `useOrg`, `useOrgContacts`, `useOrgCircle`, `useOrgRiver`, `useOrgOrders`, `useOrder`, `useIdentityReview`, `useSetOrgOwner`, `useResolveIdentity`, `useContactAction`; `SalesApiError.status` drives 403/404 |
| `(sales)/_lib/labels.ts` | the copy: link, customer, identity-reason, exception, order-class, draft-status, org-event and river labels, plus `UI` keys |
| `(sales)/_lib/orgTruth.ts` | `historyView(detail)`: `ok \| stale \| unverified \| identity \| prospect \| retired` |
| `(sales)/_lib/nextAction.ts` | `nextActionFor(orgId, tasks, leads, now)` |
| `(sales)/_lib/ring.ts` | `buildRing(months, pendingDrafts)`, arc geometry, `monthLabel(ym)` |
| `(sales)/_lib/format.ts` | `fmtAgorot`, `fmtMonthYear`, `daysSinceIsrael` (one Asia/Jerusalem calendar-day helper) |
| `(sales)/_components/OrgList.tsx`, `OrgListBand.tsx`, `BulkOwnerBar.tsx` | the list (189) |
| `(sales)/_components/CommandK.tsx`, `SalesShell.tsx` | palette on `/orgs/search` (189) |
| `(sales)/_components/org/OrgHeader.tsx`, `NextAction.tsx`, `PrimaryContact.tsx`, `OrgSummary.tsx`, `ContactsList.tsx`, `OrderRiver.tsx`, `SourceSheet.tsx`, `OrderSheet.tsx`, `OrgStates.tsx`, `Sheet.tsx` | the workspace (190) |
| `(sales)/_components/org/BusinessCircle.tsx`, `MonthSheet.tsx`, `IdentityReview.tsx` | ring and review (191) |
| `(sales)/sales/orgs/page.tsx`, `orgs/[id]/page.tsx`, `orgs/review/page.tsx` (+ layouts for titles) | routes |
| `(sales)/_components/LeadDrawer.tsx` | link to the business |
| removed: `OrgCard.tsx`, `useOrgs`, `OrgRow`, `matchesOrgQuery` | replaced by the route (the legacy drawer) |
| `tests/unit/sales/orgs.test.tsx` (replaced), `org-workspace.test.tsx`, `org-labels.test.ts`, `org-truth.test.ts`, `next-action.test.ts`, `ring.test.ts`, `business-circle.test.tsx`, `identity-review.test.tsx`, `command-k.test.tsx` | unit |
| `tests/e2e/sales-orgs.spec.ts`, `tests/e2e/_fixtures/salesOrgs.ts` | journeys A–K plus responsive, theme and motion matrix (`@mocked`) |

## Tasks

1. **T189** (`docs/portal-os/tranches/189-gt-pulse-b-org-list.md`): proxies (all twelve, so 190 and 191 add none), types, list hooks, list screen, bulk owner, palette, removal of the legacy drawer and `useOrgs`; `orgs.test.tsx` replaced (the D8 carve-out for "נטש"). Red first: the list requests `/api/sales/orgs/page?filter=active&sort=last_order&limit=50`, renders "הצג עוד" when `next` is set, separates three empty states, the palette queries `/orgs/search` and never `/api/sales/orgs`, and a row links to `/sales/orgs/<id>`.
2. **T190** (`190-gt-pulse-b-workspace.md`): the route, header, next action, primary contact, summary, river, contacts (manager verify and reject), source and order sheets, states, lead-drawer link. Red first: `historyView` truth table; `nextActionFor` picks the earliest open task or touch of this org only; every lead-event and org-event type in the backend check constraints has a label (completeness test); an unverified contact renders no `tel:`, `wa.me` or `mailto:`; money carries "לפני מע״מ"; `unverified` renders no "0"; 403 and 404 states; a retired org shows its destination and no actions.
3. **T191** (`191-gt-pulse-b-circle-review.md`): ring, month sheet, identity review. Red first: 24 segments, the current month last; marks never come from `circle.drafts`; moved-to-distributor shows no days-since; below 360px a 6 × 4 grid; each segment is a named button; reduced motion leaves `getAnimations().length === 0`; the review shows only the actions its reason allows, confirms before writing, and posts `{action, customer_gid}`.
4. **Rendered matrix**: e2e at 320/360/390/430/768/1024/1280/1440, light and dark, reduced motion, stress fixtures (design §1 sizes), no horizontal overflow, 44px targets, `elementFromPoint` checks for sheets; screenshots to the scratchpad.
5. **Gates**: `/ux-release-gate` (sales profile; P0 = P1 = 0, rerun), visual micro-audit, independent reviews, `/simplify`, `ponytail-review`, final verification, release, production smoke, docs.
