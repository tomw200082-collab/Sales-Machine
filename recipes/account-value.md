# Recipe — Account Value (annualized)

> v1 method behind the 2026-07-18 evidence snapshot. Open items: U-007 (steady-rate
> assumption), U-009 (spend-field anomaly).

## Method
1. `tenure_years = (today − customer.createdAt) / 365`, floor 0.5.
2. `annual_value = amountSpent / tenure_years`.
3. Prefer a trailing-12-months sum of actual orders when order-level data is loaded —
   more truthful than lifetime-average for accounts whose rate changed (U-007).
4. Chain value = sum of branch annual values (via the chain map).

## Caveats (bind every consumer)
- `amountSpent` anomalies exist (U-009: 58 orders / ₪0.00) — cross-check big surprises
  against order-level totals before quoting.
- Off-Shopify revenue (direct Green Invoice) is invisible here (U-006).
- Currency: ILS throughout; no VAT normalization applied — state which basis when quoting.

## Verification
Rebuild check: for a sample of 10 accounts, `sum(order totals)` must equal
`amountSpent` within tolerance; report N/N.
