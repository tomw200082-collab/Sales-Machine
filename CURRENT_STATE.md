# Sales-Machine — Current State

> Sole authority on build status and open unknowns. Volatile by design.
> Last updated: 2026-08-04.

## Build ladder status

| Phase | Scope | Status |
|---|---|---|
| 0 — Constitution | CLAUDE.md truth rules, structure, boundaries | **APPROVED** — Tom, in writing 2026-08-04 (D-006) |
| 1 — Seed verified knowledge | research findings, evidence snapshots, recipes | **LANDED** |
| 1.5 — Customer journey map | end-to-end journey, doctrine + live-systems evidence | **LANDED + CONFIRMED** 2026-08-04 (D-007…D-013) |
| 2 — Truth interviews with Tom | remaining doctrine gaps → `user_confirmed` cards | **PARTIAL** — pricing (D-008), basket (D-009), roles closed in the journey session; ICP + chain dossiers still open |
| 3 — System reconciliation | verify tag semantics, channel-move checks, contacts | not started |
| 4 — Agents (read-only first) | declarations in `agents/` | not started |
| 5 — Automations | only after base verified; outreach behind frozen flag | locked |
| 6 — Lean CRM build | in-house, portal route group + `sales_core` schema | **DECIDED, NOT STARTED** (D-012) — blocked on declaration amendment |

## What Tom decided on 2026-08-04

Journey confirmed (`doctrine/customer-journey.md`) · one automated message only · Shopify pricing ·
our products only · new marketing site + Shopify payment · 24h branded-menu incentive · build the CRM
in-house inside the portal · sales UI deliberately visual and focused. Full text: `doctrine/decisions.md`
D-006 → D-013.

## Critical path

1. **Declaration amendment** — PR #46 models `account`/`contact`/`touch_log`/`dream100_target` but has **no
   `lead`, no `assignment`, no `task`**. Until amended and re-approved, the CRM in D-012 is not buildable
   under governance.
2. **Meta app review** (`leads_retrieval` + Instagram messaging) — waiting time, not dev time. Start first.
3. **Lead capture** — nothing captures a lead today (F-1). Everything downstream is theoretical until it exists.

## UNRESOLVED (open unknowns — rule 3: never silently filled)

| ID | Question | Route |
|---|---|---|
| U-001 | Isrotel (~₪940K lifetime, ~13 branches) went dark ~2024-09/10 — churn, channel move, or tender loss? | Chain dossier interview + Green Invoice check |
| U-002 | Mina Tomei: 5 branches went dark the same week (~2026-02) — one story? recoverable? | Chain dossier interview |
| U-003 | Legacy tag semantics: `10off`, `50-29`, `300ml-23`, `shotef`, `net30`, `pl`/`client_key` | Pricing interview + system verify. **De-blocked for the journey by D-008** (v1 = public Shopify pricing) |
| U-004 | B2B records use placeholder login emails — where do real ordering contacts live? | Interview + system check |
| U-005 | ICP ranking (segments × buyer type) | Interview #1 — still open |
| U-006 | Off-Shopify sales share (Green Invoice direct? distributor?) — required before any churn claim | Interview + GI check |
| U-007 | Annual-value method assumes steady rate; validate per tier | Recipe validation |
| U-008 | **Closed 2026-08-04** — the site is a new marketing site in its own repo; payment stays on Shopify (D-010) | — |
| U-009 | Data quirk: account with 58 orders and ₪0.00 amountSpent | Interview / system check |
| U-010 | **New:** SLA — after how many hours without contact does a lead escalate? | Tom decision |
| U-011 | **New:** Erik (אריק) appears in no governance document. Role, scope, and lead-routing share undefined | Tom decision + operational map update |
| U-012 | **New:** the customer-menu-building skill was not found in any of the four repos here | Tom — locate or re-author |
| U-013 | **New:** 4 of 8 sugared 0.5L concentrates at zero stock. The interactive catalog must gate on live stock — mechanism undefined | Design decision, blocks catalog stage 4 |

## Pointers

- Journey doctrine: `doctrine/customer-journey.md` · 24h incentive: `doctrine/playbooks/menu-incentive-24h.md`.
- Decisions log: `doctrine/decisions.md` (D-001 → D-013).
- Latest evidence: `evidence/2026-08-04-journey-systems-check.md`.
- CRM evaluation: `knowledge/market/crm-buildvsbuy-2026-08-04.md`.
- Module declaration (governance gate): `gt-factory-os-production-brain/docs/decisions/modules/sales-declaration.md`.
