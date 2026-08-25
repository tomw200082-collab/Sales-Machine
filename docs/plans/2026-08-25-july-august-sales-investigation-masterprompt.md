# MASTERPROMPT — Why July→August 2026 sales moved, and what Tom should do about it

**STATUS: LIVE — not yet executed**
<!-- The executing session's last act is to change this line to SHIPPED / SUPERSEDED by <path> /
     ABANDONED — why, with evidence pointers. -->

> **Usage:** paste this entire file as the first message of a fresh session with the
> Shopify MCP connector and the `Sales-Machine` + `gt-factory-os` repos attached. It takes
> the question "sales relatively dropped from July to August despite the big deal" from an
> unexamined premise to a defended, evidence-graded answer with named causes. It halts for
> Tom only where a human must genuinely decide — §6 is that complete list.
>
> **Provenance:** written 2026-08-25 by the session that shipped the sales-queue integrity
> work. Every number in §2 was measured that day against the live Shopify Admin API
> (ShopifyQL + GraphQL), not recalled. Authority: `Sales-Machine/CLAUDE.md` and
> `recipes/sales-report.md` — cited below, never copied.
>
> **Shelf life:** §2 is presumed wrong if pasted after 2026-09-08. August closes 2026-08-31,
> which changes every partial-month figure here. Re-run §2.5 first. **If the re-run
> disagrees with §2 by more than 2% on any headline figure, adapt and say so in the report —
> do not halt.** August closing is expected drift, not a contract failure.

## 0. How to work

- **Who you are here:** one fresh session acting as Tom's sales analyst. You hold the
  Shopify Admin API (read), the Supabase/Postgres MCP for `gt-factory-os` (read), and the
  four repos. You decide the analysis method and the report structure alone. You do **not**
  decide anything listed in §6, and you write to no external system.
- **Read first, in order:** `Sales-Machine/CLAUDE.md` · `Sales-Machine/CURRENT_STATE.md` ·
  `Sales-Machine/recipes/sales-report.md` (the method) ·
  `Sales-Machine/evidence/2026-08-24-sales-report.md` (the most recent measured snapshot).
- **Authority:** `Sales-Machine/CLAUDE.md` §"The 7 truth rules" governs every claim you
  write. Where this document and that file disagree, that file wins and this document is
  wrong. Rule 1 (source + date + authority grade on every card) and rule 2 (volatile data =
  recipe + dated snapshot, never a stored fact) bind the report you produce.
- **Halt conditions, evidence standard, write boundaries:** inherited from
  `Sales-Machine/CLAUDE.md` §"Stop conditions" and §"Hard boundaries". Deltas specific to
  this work are in §8 — that list is additions only.
- **The standard.** Tom asked for a professional report. Translated into checkable
  prohibitions: **nothing on the page may be a number you did not personally pull** ·
  **no comparison between two windows of different length** · **every causal claim names
  the account, product or date that carries it, or it is labelled a hypothesis.**
- **Language:** this document is in English because that is the register you reason best
  in; every Hebrew literal stays in backticks and is never translated — a translated
  account name matches nothing in Shopify. **Output language: the final report artifact and
  your chat replies to Tom are in Hebrew, professional and plain** — he is the reader and
  the precedent artifact is Hebrew. Keep your own working notes and any code in English.
  No preamble, no restating the question.

## 1. Mission and definition of done

**One testable sentence:** explain, with evidence Tom can re-run, what actually changed in
GT Everyday's sales between July and August 2026 and what is causing it.

| # | Condition | The observation that would prove it false |
|---|---|---|
| D1 | The premise in the request has been tested, not assumed, and the report states plainly whether sales dropped, and on which measure | The report repeats "sales dropped" without a same-length-window figure beside it |
| D2 | Every comparison is like-for-like on window length, and states its window in the table header | Any table compares a full month to a partial one without saying so |
| D3 | The `מימי ואזה` deal is isolated, and both the with-deal and without-deal figures are shown | The report quotes one headline number that silently includes or silently excludes it |
| D4 | The decline is decomposed to named accounts, with each account's ₪ and order-count delta | The report explains the change only with aggregate rates |
| D5 | For each of the top causes, at least one non-Shopify source was checked (production plan, stock, or Tom) and the result stated — including "checked, did not matter" | A cause is asserted from order data alone where a second source exists |
| D6 | Every claim carries source + date + authority grade per `CLAUDE.md` rule 1, and hypotheses are labelled `inferred` and never presented as policy | Any `inferred` claim appears in the recommendations as established fact |
| D7 | A dated snapshot is written to `Sales-Machine/evidence/` and `CURRENT_STATE.md` points at it | The numbers exist only in the artifact or the chat |
| D8 | The report ends with a ranked, costed action list — what to do this week, per named account | The report ends at diagnosis |

Anything not on this list is out of scope unless Tom asks.

### 1.1 Settled — do not reopen

Confirmed by Tom on 2026-08-24 (`user_confirmed`, recorded in
`evidence/2026-08-24-sales-report.md`). Re-deriving any of these wastes the session:

1. **The money basis is ex-VAT, the stored Shopify price.** Shopify is misconfigured
   `taxesIncluded=true @17%`.
2. **`total_sales` is the reconciliation anchor.** ShopifyQL's `net_sales`, `gross_sales`,
   `taxes` and `average_order_value` columns, and `customer.amountSpent`, are **forbidden** —
   they subtract a fictitious `17/117`. Compute AOV as revenue ÷ orders from your own pull.
3. **The 202-SKU taxonomy is frozen.** Family, type, sugar, category are approved. Changing
   it requires Tom, per `recipes/sales-report.md` §taxonomy.
4. **All revenue passes through Shopify.** There is no off-Shopify channel to hunt for.
5. **GT cancels orders; it does not refund.** Refunds are `0` across the whole 25-month
   window. Cancellations are the reversal mechanism.
6. **Month attribution is `Asia/Jerusalem`,** not UTC.
7. Untagged customers display as `ללא רשת`. Field `*-chain` tags were **not** adopted.

## 2. Ground truth — measured 2026-08-25; re-verify at boot

### 2.1 What already exists, and must not be rebuilt

- A verified 25-month fact table (`month × customer × SKU`) covering 2024-08 → 2026-08-24:
  `20,259` rows, `202` SKUs, `804` customers, `6,829` counted orders, passing all five
  correctness gates. Every figure in this bullet is quoted from
  `evidence/2026-08-24-sales-report.md` (run dated 2026-08-24).
- The scripts that build it: `gt-factory-os/scripts/sales-report/` — `build_facts.py`,
  `build_gate_page.py`, `build_report.py`, `build_excel.py`, `report_template.html`.
  Present on branch `claude/impaccable-caveman-4z3opj`, and on disk in this workspace.
  **Re-run these rather than writing a new extractor.** `README.md` in that directory has
  the order.
- The published report artifact and its approval-gate page — URLs in the evidence file.
  **Publish your investigation as a new artifact; do not overwrite either of those.**

### 2.2 The numbers

Pulled 2026-08-25 via ShopifyQL against `greenteaeveryday.myshopify.com`. All ₪ ex-VAT.

**Monthly, `FROM sales SHOW total_sales, orders TIMESERIES month`:**

| Month | `total_sales` ₪ | orders |
|---|---|---|
| `2026-05` | 448,283.49 | 322 |
| `2026-06` | 619,165.21 | 437 |
| `2026-07` | 703,386.65 | 453 |
| `2026-08` (to 25th, partial) | 704,207.59 | 368 |

**The like-for-like window — this is the finding that reorganizes the question.**
Both windows are day 1 → day 25, summed from the daily series in §2.5:

| Measure | `2026-07-01`→`07-25` | `2026-08-01`→`08-25` | Δ |
|---|---|---|---|
| Revenue ₪ | 587,747.61 | 704,207.59 | **+19.8%** |
| Revenue ₪ excluding the `מימי ואזה` deal | 587,747.61 | 474,707.59 | **−19.2%** |
| Orders (incl. cancelled, as ShopifyQL counts) | `370` | `368` | −0.5% |
| AOV ₪ excluding the deal | `1,588.51` | `1,300.57` | **−18.1%** |

**The deal.** Verified by GraphQL on 2026-08-25, customer `מימי ואזה חנויות`
(`gid://shopify/Customer/8331093836017`):

| Order | Created | ₪ subtotal | Cancelled |
|---|---|---|---|
| `#GT14058` | `2026-08-09T06:13:03Z` | 270,000 | yes, `09:34:07Z` |
| `#GT14067` | `2026-08-09T09:33:38Z` | 243,000 | yes, `13:27:24Z` |
| `#GT14078` | `2026-08-09T13:27:02Z` | 229,500 | **no — this is the live one** |

Three revisions of one deal inside seven hours; only the third stands. It is the 0.3L
extract line, `17,000` units per `evidence/2026-08-24-sales-report.md`.

**Where the real decline sits.** Same 1→25 windows, `GROUP BY customer_id, customer_name`:

| Account | Jul ₪ | Jul orders | Aug ₪ | Aug orders | Δ ₪ |
|---|---|---|---|---|---|
| `יונימרקט בע"מ` | 64,194 | 13 | 13,860 | 5 | **−50,334** |
| `אליטה אופק בע"מ` | 42,564 | 16 | 24,382 | 6 | **−18,182** |
| `אלי אברהמי שווק בע"מ` | 64,854 | 4 | 62,524 | 8 | −2,330 |
| `בבקה הרצליה (בבקה בייקרי בע"מ)` | 8,896 | 7 | 7,772 | 6 | −1,124 |
| `מולה בוטני בע"מ` | 6,468 | 3 | 7,726 | 5 | +1,258 |
| `נונומימי פתח תקוה בע"מ` | 6,102.72 | 4 | 7,910.9 | 6 | +1,808 |

Those two accounts alone are **−₪`68,516` of the −₪`113,040` ex-deal gap — 61% of it**
(both differences computed from the two `GROUP BY customer_id` pulls in §2.5, 2026-08-25).

Four accounts in July's top-12 are absent from August's top-12, whose 12th place is
₪5,184: `מתן בארי (לוקיישן)` at 9,196 · `החלונות הגבוהים א.ג טעים בשוק בע"מ` at 8,742 ·
`בבקה כיכר הבימה ת"א` at 7,570 · `נונומימי קרית אונו בע"מ` at 6,330.
**A `LIMIT 12` cut cannot prove absence — confirm each individually before claiming it.**

### 2.3 What is NOT built

- No per-account cadence baseline is running. `recipes/sleeping-radar.md` is a v1 method,
  never validated against Tom's answers.
- No causal link exists between the production plan and order data. Nothing joins a
  stock-out to a customer who did not order.
- No margin data in the fact table — it is revenue and units only. A mix-shift finding
  cannot yet be converted to a profit statement without the cost sheet.

### 2.4 Known-broken, adjacent, out of scope

- **April 2026 is an artefact.** `₪146,253.72` reflects a retroactive cleanup: ~60 orders
  from 2024–2025 were cancelled during April. Do not treat April as a trading collapse, and
  do not include it in a trend line without a footnote.
- **November 2025** carries a `₪77K` order placed and cancelled in-month.
- `Elita Pear Margarita 300ml` has no SKU: `₪36,108` / `1,416` units sit in the visible
  no-SKU bucket.
- `U-003` (pricing-tag semantics), `U-006` (off-Shopify share, since answered), `U-009`
  (`amountSpent` anomaly), `U-010` (`MUZA` identity) remain open in `CURRENT_STATE.md`.
  **Do not close any of them in passing.**

### 2.5 Re-verification block — regenerates every figure in §2.2

```
-- ShopifyQL. Run all four. Sum the daily series over 1..25 for the like-for-like window.
FROM sales SHOW total_sales, orders TIMESERIES month SINCE 2025-08-01 UNTIL 2026-08-31
FROM sales SHOW total_sales, orders TIMESERIES day   SINCE 2026-07-01 UNTIL 2026-08-31
FROM sales SHOW total_sales, orders GROUP BY customer_id, customer_name SINCE 2026-07-01 UNTIL 2026-07-25 ORDER BY total_sales DESC LIMIT 40
FROM sales SHOW total_sales, orders GROUP BY customer_id, customer_name SINCE 2026-08-01 UNTIL 2026-08-25 ORDER BY total_sales DESC LIMIT 40
```

```graphql
# Confirms the deal and its two cancelled revisions. Run with q =
# "created_at:>=2026-08-01 created_at:<=2026-08-31"
query { orders(first: 50, query: $q, sortKey: CREATED_AT) {
  edges { node { name createdAt cancelledAt test
                 customer { id displayName }
                 subtotalPriceSet { shopMoney { amount } } } } } }
```

## 3. What the hard part actually is

The visible deliverable is a monthly comparison. That is an hour's work and it is not the
job. Five reframes, in the order they change the answer:

1. **The premise is inverted, and saying so is the first deliverable.** Tom asked why sales
   dropped. On the like-for-like window revenue is **up 19.8%**, and even the naive
   partial-August-versus-full-July comparison is flat at `+0.12%`. What fell is revenue per
   order. Your report opens by correcting the question, respectfully and with the table
   that does it — then answers the real one.

2. **Find why it *felt* like a drop, because that perception is itself a finding.** Three
   candidates, all checkable: order count reads `453 → 368` (−18.8%) if August is taken as
   a finished month; Shopify's own dashboard surfaces the forbidden `net_sales` column; and
   the daily series has a conspicuous flat stretch after `2026-08-09`. If Tom's instrument
   is systematically misleading him, fixing the instrument outranks the analysis.

3. **The deal and the decline may be the same event, not two.** `17,000` units of 0.3L
   extract entered production in mid-August. If that consumed tank time, raw material or
   packaging that normal replenishment needed, then the big deal *caused* the softness in
   the ordinary book. This is the single most valuable hypothesis in the document and the
   only one that changes what Tom does next. Test it against the production plan and the
   stock ledger in `gt-factory-os`, and against availability: an account cannot order what
   the storefront showed as unavailable.

4. **Two accounts are 61% of the gap, so this is an account story, not a market story.**
   `יונימרקט` and `אליטה אופק` both roughly halved their order *frequency*, not just their
   basket. Frequency collapse at a chain has a small number of real causes — a stock-out, a
   payment or credit hold, a competitor, a seasonal closure, or a person who stopped
   ordering. Each is checkable. Do not stop at "they ordered less".

5. **Total order count held flat while the big accounts halved.** Something added roughly
   as many small orders as the chains removed. Identify what — new accounts, a long tail
   waking up, or one branch splitting its orders — because a business replacing wholesale
   volume with retail-sized orders is a materially different business, and nobody has
   noticed it happening.

## 4. Workstreams

Run W1 and W2 before W3–W5; the rest are independent of each other.

### W1 — Rebuild the like-for-like base
**The window rule, so you do not have to invent one:** compare day `1`→day `N` of each month,
where `N` is the last day that has fully elapsed in *both*. On or after `2026-09-01` that is
`N = 31` and both months are whole; before then it is yesterday's date in `Asia/Jerusalem`.
State `N` in every table header. Never compare a whole month to a partial one.
Re-run §2.5 for the window you land on. Rebuild the fact table with
`gt-factory-os/scripts/sales-report/build_facts.py` rather than a fresh extractor. Produce
one table: `window × customer × SKU` for both months, with and without `#GT14078`.
Apply the five correctness gates in `recipes/sales-report.md` and report each `N/N`.
**Acceptance:** D1, D2, D3.

### W2 — Decompose the delta to named accounts
Every account whose ₪ moved by more than `±5,000` between the two windows, with its ₪ and
order-count delta, ranked. Confirm or refute the four suspected drop-outs in §2.2 —
individually, not by a `LIMIT` cut. Separate frequency change from basket change for each.
**Acceptance:** D4.

### W3 — Test the supply hypothesis (§3 reframe 3)
Join to `gt-factory-os`: the production plan for August, `stock_ledger` movements for the
0.3L extract line, and any availability exceptions. Answer one question: **was any product
that `יונימרקט` or `אליטה אופק` normally buys unavailable, or late, during August?**
A clean negative is a valuable result — state it as one.
**Acceptance:** D5, and reframe 3 closed either way.

### W4 — Product and category mix
Same two windows, `GROUP BY` family and category using the frozen taxonomy. Identify what
the −18.1% AOV is made of: fewer lines per order, cheaper lines, or a shift between
categories. Note where a margin statement would need the cost sheet, and stop there.
**Acceptance:** contributes to D8.

### W5 — The report
A Hebrew artifact, structured: the corrected premise · the like-for-like table · the deal
isolated · the account decomposition · causes with their grade · what was checked and found
not to matter · the ranked action list. Then a dated snapshot to
`Sales-Machine/evidence/2026-08-25-july-august-investigation.md` following the shape of the
2026-08-24 file, and a `CURRENT_STATE.md` pointer to it.
**Acceptance:** D6, D7, D8.

## 5. Scope

**IN:** everything in §4.

**OUT — do not touch, do not "improve":**
- Any write to Shopify, Green Invoice, LionWheel, or any customer-facing system. This is a
  read-only investigation. `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` stays `false`.
- The frozen 202-SKU taxonomy, and the two published artifact URLs in the 2026-08-24
  evidence file.
- `gt-factory-os` core tables — `stock_ledger`, `balance_anchors`, `bom_*`, `items`,
  `components` are **read-only** to this work, per `Sales-Machine/CLAUDE.md`
  §"Hard boundaries". Reading is allowed for W3; writing is never allowed.
- The open `UNRESOLVED` items. Add to them if you find something; close none.
- `doctrine/` — Tom is its sole approver.

## 6. Tom's part — the complete list, nothing else is his

**A. The `מימי ואזה` chain assignment.** The account carries `₪267,962` cumulative and no
chain tag, and `מימי ואזה חנויות` is a *different* Shopify customer from
`מימי ספורטן בע"מ (מימי הוד השרון)`. Whether they are one commercial relationship is
Tom's call, not an inference. Two minutes; changes how the deal is attributed.

**B. Context on `יונימרקט` and `אליטה אופק`.** Ask him directly, once you have the numbers:
does he know of a closure, a tender, a credit hold, a competitor, or a personnel change at
either? He may answer in one sentence what the data cannot answer at all.

**C. Whether the 0.3L extract deal was produced from existing stock or displaced planned
production.** He knows; the ledger may only imply it.

**D. Approval before anything reaches a customer.** No outreach, no email, no call list
executed — recommendations only.

## 7. Landmines — do not rediscover these

1. **The partial month.** August is incomplete until `2026-08-31`. Comparing it to a full
   July manufactures a fake 19% order-count drop. Every table states its window length.
2. **The three `מימי ואזה` orders.** ShopifyQL counts `3` orders and `₪229,500` for that
   account in August: the ₪ excludes the two cancelled revisions, the order count includes
   them. Summing subtotals across all three yields `₪742,500` and a report that is wrong by
   half a million shekels. Filter `cancelledAt = null` for money, keep them for counts.
3. **Two different customers share a first word.** `מימי ואזה חנויות`
   (`8331093836017`) and `מימי ספורטן בע"מ (מימי הוד השרון)` (`7046963626225`) are separate
   accounts. A name-substring match merges them and destroys both stories.
4. **The forbidden columns.** `net_sales`, `gross_sales`, `taxes`, `average_order_value`,
   `customer.amountSpent` all carry the fictitious `17/117` deduction or documented
   anomalies. They will return plausible numbers. Use `total_sales` and compute the rest.
5. **UTC vs `Asia/Jerusalem`.** Order timestamps come back as `Z`. Attributing by UTC shifts
   evening orders into the wrong day and breaks reconciliation against ShopifyQL.
6. **Friday and Saturday are structural zeros.** The daily series has legitimate `0` days.
   A "sales stopped" finding that lands on a weekend is a calendar artefact. Count trading
   days, not calendar days, when comparing pace.
7. **A negative day is real.** `2026-07-30` returns `total_sales` of `-1,500` on `5` orders —
   an in-window cancellation or order edit outweighing that day's sales. It is not a bug and
   not a data-pull error. Do not clamp it to zero and do not drop the day; both silently
   inflate July and shrink the gap you are trying to explain.
8. **April 2026 is a cleanup, not a collapse** — see §2.4. It will wreck any trend line.
9. **`LIMIT` cuts cannot prove absence.** An account missing from a top-12 may sit at
   position 13. Query the account directly before writing that it stopped ordering.
10. **A flat total can hide two large opposite movements.** Order count moved `−0.5%` while
   the two largest chains halved. Never conclude "nothing changed" from a stable aggregate.

## 8. Halt conditions

Inherited set is cited in §0. **Additions specific to this work only:**

- A figure you are about to publish disagrees with `evidence/2026-08-24-sales-report.md` by
  more than 2% **on a window that closed before 2026-08-24** → **STOP.** History does not
  move; one of the two is wrong. Find which before writing another line, and do not average
  them. This is a different rule from the shelf-life clause at the top: movement in the
  *August-to-date* figures is expected as the month fills, and you adapt to that silently.
- Any correctness gate in `recipes/sales-report.md` fails and you cannot explain the
  residual → **STOP**, report the gate and the number, publish nothing.
- The analysis would require a write to any external system → **STOP.** There is no such
  requirement in §4; if you believe there is, you have left scope.
- The Shopify connector is not attached, or a §2.5 query returns an authentication error →
  **STOP** and tell Tom. Do **not** fall back to the figures in §2 and present them as
  current: they are a dated snapshot, and §2 exists to be re-verified, never to be quoted
  as live truth.
- A conclusion depends on `U-003`, `U-009` or `U-010` being resolved → **STOP**, state the
  dependency, and hand that decision to Tom rather than assuming it.

## 9. Final report

Deliver in Hebrew, in this order:

1. **The corrected premise**, in two sentences and one table.
2. Each done-condition D1–D8, ✅ or ❌, with its evidence pointer. No partial credit.
3. **The numbers** — like-for-like, deal isolated, decomposed to accounts.
4. **The causes**, each with source, date and authority grade; `inferred` clearly marked.
5. **What was checked and found not to matter** — this section is mandatory and is what
   separates an analysis from a story.
6. The artifacts and where they are; the evidence snapshot path.
7. What is still Tom's (§6), and what remains genuinely unfinished.
8. **The single next action.**

If anything is not ready, say so first and plainly. `"It should be right"` is not evidence.
