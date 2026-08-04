# Evidence snapshot — live systems behind the journey (2026-08-04)

> **Immutable. True as of 2026-08-04 only.** Never edit; supersede with a newer dated snapshot.
> Authority: `system_verified` — every line below was read from the live system, not inferred.

## Klaviyo — empty

`GET /api/forms` → `data: []` · `GET /api/flows` → `data: []`.
**Zero forms, zero flows.** No customer email automation exists.

## Make.com — the lead pipeline is dark

Org 6913249 · team 1240098. 14 scenarios.

| Scenario | State |
|---|---|
| GT Leads — Instant (FB Lead Ads → Sheets → email) | **inactive** |
| GT Leads — Health Check | **inactive** |
| GT — התראת ליד חדש | **inactive + invalid** |
| GT WA · Brain · GT WA · Order & Pay (Jun prototypes) | **inactive**, 0 executions |
| GT B2B — Checkout → Green Invoice | **inactive** |
| GT Order Agent — Shopify Draft Runner | active (webhook → Shopify draft order) |
| GT Guardian — Daily Email | active, 28 executions |

**No live lead→payment path exists. None.**

## Shopify — plan and stock

`shop.plan`: `displayName: "Shopify"`, `shopifyPlus: false` → **no native Companies, no B2B price lists.**

0.5L concentrates (the size a new customer wants for a first order):

| SKU | Product | On hand |
|---|---|---|
| GT-LUI-LOW-0.5L | DETOX | **0** |
| GT-LEM-LOW-0.5L | ENERGY | **0** |
| GT-JAS-LOW-0.5L | CONSCIOUSNESS | **0** |
| GT-SEN-LOW-0.5L | REVIVE | **0** |
| GT-HIB-LOW-0.5L | FRESH | 196 |
| GT-MAS-CHA-0.5L | NAMASTEA | 183 |
| GT-INF-DES-0.5L | DESERT | 120 |
| GT-CHA-LOW-0.5L | CALM | 56 |
| GT-LUI-FRE-0.5L | DETOX Sugar-Free | 180 |
| GT-HIB-FRE-0.5L | FRESH Sugar-Free | 96 |
| GT-ELT-STR-0.5L | Elita Strawberry Detox | 106 |

**4 of 8 sugared concentrates at zero.** An interactive catalog that promises menus built on them ships a
broken promise. Stock gating in stage 4 is not optional.

## Canva catalog — read

Design `DAHPi9gpfts`, "קטלוג משקאות מעודכן", 64 pages, updated 2026-08-03.
10 collections · 48 drinks · 4 prep pages. Every drink page carries prep method, ingredients, FOOD COST,
recommended price (ex-VAT), margin % and ₪ profit per cup.
Prep pages confirm the cold-foam base (cream + milk + vanilla pudding as stabilizer) underpins ~20 drinks —
none of those ingredients are GT products. Per **D-009** they stay in the recipe, out of the basket.

## GT-side capability (verified in this workspace)

- `gt-factory-os/supabase/functions/wa-order-bot/` — live Meta webhook receiver.
- `gt-factory-os/api/src/order-intake/` — webhook, worker, tests, idempotent dedupe.
- `gt-factory-os-portal/src/app/(inbox)/` — existing queue + detail + approvals pattern.
- `dir="rtl"` — 13 occurrences across 10 files in `gt-factory-os-portal/src`.

## Caveats

1. Erik (אריק) appears in **no** governance document in this workspace. Doreen, Denis, Maxim, Maidan, Adi and
   Alex all do.
2. The customer-menu-building skill Tom refers to was **not found** in any of the four repos here.
3. Stock figures are a point-in-time read; re-check before any customer-facing promise.
