# Recipe — Sleeping-Account Radar (needs-check list)

> Computes fresh every run. Output is **"needs check"** — never "churned" (U-006).
> Grounding: silent-churn research (knowledge/market §7). Status: v1 method,
> pending validation against Interview #2 answers.

## Inputs
- Shopify: per customer `orders(createdAt)` history, `amountSpent`, tags.
- Chain map (accounts/ dossiers) to roll branches up to chains.
- Optional cross-checks: Green Invoice invoices, LionWheel deliveries (channel-move).

## Method
1. Per account with ≥5 orders: baseline cadence = **median inter-order gap** over the
   trailing 12 orders (fallback: full history). Accounts with <5 orders: skip (no
   reliable baseline) — count them separately, don't silently drop (empty ≠ green).
2. `days_since_last = today − last_order_date`.
3. Flag **off-pace** when `days_since_last > 1.5 × median_gap`; **silent** when
   `> 3 × median_gap`. (Thresholds are v1 defaults — tune with Tom.)
4. Value-at-risk = annualized account value (see `recipes/account-value.md`).
5. Roll up by chain: a chain is flagged when ≥50% of its active branches are off-pace.
6. **Mandatory before any outreach:** check Green Invoice / LionWheel for channel-move;
   check seasonality (hotels!); attach the account's own history to the output.

## Output (per run — a dated evidence file or live brief, never edited into knowledge/)
`account · chain · last_order · median_gap · days_since_last · ratio · annual_value ·
flag(off-pace/silent) · channel-move-checked? · seasonality-note`

## Verification (rule 4)
- Golden case: the 2026-07-18 snapshot chains (Mina Tomei, Isrotel, King Kong, Landwer)
  must surface with correct dates/values.
- Control: total flagged accounts + skipped-short-history count reported every run
  (N/N; a zero-flag run must show why).
