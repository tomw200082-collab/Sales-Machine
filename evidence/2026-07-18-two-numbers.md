# Evidence snapshot — the two numbers (2026-07-18)

> **Immutable. True as of 2026-07-18 only.** Never edit; supersede with a new dated
> snapshot. Source: live Shopify Admin API (`greenteaeveryday.myshopify.com`),
> read-only GraphQL, first ~100 established accounts (`orders_count > 8`), two pages.
> Authority: `system_verified` for the raw fields; derived figures per the stated
> method. Store totals cross-checked earlier the same day via ShopifyQL
> (₪1.89M gross / 1,174 orders / AOV ₪1,346 for the trailing 90d; monthly returning
> rate 87–98% over 2026-01→07).

## Method

- Tenure: B2B base mass-created ~2023-05 → tenure ≈ 3.2 years.
- **Annual value ≈ lifetime `amountSpent` ÷ 3.2** (steady-rate assumption — U-007).
- "Silent": `lastOrder.createdAt` far below the account's own historical cadence.
  **Label is "needs check", never "churned"** — off-Shopify channels not visible here
  (U-006).

## Number 1 — annual value per account

| Tier | Lifetime / account | Annual / account | vs. single order (₪1,346) |
|---|---|---|---|
| Whale (יונימרקט, 198 orders) | ₪887,553 | ~₪279K | ×207 |
| Large chain (Isrotel ~13 branches, Mina Tomei 5+, Wix) | ₪200K–940K | ₪40K–296K | ×30–220 |
| Established branch (typical) | ₪15K–95K | ~₪6K–30K | ×5–22 |

→ Account annual value is **5×–200× the single-order AOV**. KAM + targeted outbound
are economically justified (refutes the "AOV too small for outbound" framing).

## Number 2 — silent accounts (needs-check), by chain

| Chain | Branches seen | Lifetime (sum) | Annual at risk | Last orders seen |
|---|---|---|---|---|
| Isrotel | ~13 | ₪940,436 | ~₪296K | ~2024-09/10 (~21mo) — U-001 |
| Mina Tomei | 5 | ₪388,612 | ~₪122K | ~2026-01/02 (~5.5mo) — U-002 |
| King Kong | 4 | ₪78,826 | ~₪25K | ~2025-12→2026-01 (6–7mo) |
| Landwer | 7 | ₪68,040 | ~₪21K | 2023–2024 (dormant) |

Large silent singles: מתוק וטעים ₪161,689 (since 2023-10; note: 9 orders only —
high-value/low-frequency profile), ריף אילת ₪15,311 (since 2024-10), קפה עם גבעת חן
₪46,108 (since 2026-02), אולין סושי רמה"ש ₪32,829 (since 2026-01), נגיסה ר"ג ₪22,041
(since 2025-02), בייקר רמה"ש/גבעתיים/הוד"ש ~₪49K (since 2024-11).

**Sum of silent lifetime value in this sample alone: >₪1.7M.**

## Data caveats (bind every consumer of this snapshot)

1. `amountSpent` anomaly exists (58 orders / ₪0.00 — U-009); spend fields not fully
   trusted until explained.
2. Sample = first 100 accounts by customer id with >8 orders — **not** the full base
   (~1,235 active customers; more pages exist).
3. Silence here ≠ churn (channel move possible — U-006). Seasonality not modeled
   (hotels especially — Isrotel's drop clusters at 2024-09/10).
4. Lifetime spans price changes; annualization is a flat average (U-007).
