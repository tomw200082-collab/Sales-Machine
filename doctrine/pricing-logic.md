# Doctrine — Pricing & Terms Logic

**Status: UNRESOLVED (U-003). Nothing here is policy yet.**

Observed in live Shopify (2026-07-18, `system_verified` that they exist — semantics
unknown): customer tags `wh`, `net30`, `shotef`, `10off`, `50-29`, `300ml - 23`,
chain tags (`landwer`, `r2m`, `minatomei`, `isrotel`, `guta`, `unimarket`, `fattal`,
`mandarin`, `kampai`, `nord`, `bneikikar`, …), and metafields `custom.price_list`,
`custom.client_key` (segments `pl`, `WH` reference them).

Per rule 3, semantics are **not guessed**. Interview #3 decodes each; each decoded rule
is then verified against actual order pricing (rule 4) before being written here as
`user_confirmed` + `system_verified`.

## Questions Interview #3 must answer

1. Meaning + current validity of each tag above; which are dead legacy.
2. How B2B prices are actually set today (price_list mechanics, who maintains).
3. Payment terms map (net30 / shotef / prepaid) and who gets which.
4. Discount doctrine: when do we give 10%? what is `50-29`? `300ml - 23`?
5. U-009: the 58-orders/₪0.00 account — what does it mean for spend-data trust?
