# Template — `.claude/product-marketing-context.md`

Copy this to `.claude/product-marketing-context.md` and fill it from the capture
pass. Every vendored copy skill reads that path before asking questions, so a
filled field is a question Tom never answers twice.

**Rules that bind this file**

- Every field carries `source` · `date` · `authority`
  (`user_confirmed` / `system_verified` / `doc_confirmed` / `inferred`).
- **`inferred` is never policy.** It may seed a draft; it may not be stated as
  fact in customer-facing copy.
- **No guessing.** An unanswered field stays `UNRESOLVED` and gets a `U-0xx`
  line in `CURRENT_STATE.md`. Never quietly filled.
- **Volatile data does not live here.** No account counts, no revenue, no
  "sleeping since". Those are recipe runs against live systems, dated at the
  moment of the run.
- **This file is not doctrine.** It is a derived working artifact. When a field
  is stable enough to be policy, propose the `doctrine/` edit for Tom's
  approval and log it in `doctrine/decisions.md` — do not write it yourself.

---

```markdown
# GT Everyday — product marketing context

last_capture: YYYY-MM-DD
captured_by: <who>

## Who we sell to
segment_ranking:        # source: doctrine/icp.md · date: · authority:
target_buyer:           # single-site owner vs chain HQ / purchasing
dream_account:          # size, branches, menu fit, payment behaviour, logistics
bad_fit:                # who we decline or price differently
margin_source:          # which product families × which segment

## What we sell
what_it_is:             # beverage bases, wholesale to HoReCa
what_it_replaces:       # the status quo in the customer's kitchen
category_language:      # what the buyer calls this, in their words

## The story
before_gt:              # what the best customers got wrong before GT
outcomes_we_can_claim:  # each with the evidence that backs it
proof_assets:           # named accounts and numbers we may use publicly
we_win_on:              # truthfully, vs competitors and substitutes

## Voice
language:               # Hebrew unless stated
tone:
words_we_use:
words_we_never_use:

## Pricing language
# UNRESOLVED (U-003) until doctrine/pricing-logic.md is decoded.
# Until then: no price and no discount appears in copy.
can_state_publicly:
never_state_publicly:

## Channels
owned:                  # Shopify storefront, and what else
constraint:             # Shopify owns part of theme + URL structure
```

---

## Where each field comes from

| Section | Interview | Doctrine file | Open ID |
|---|---|---|---|
| Who we sell to | #1 | `doctrine/icp.md` | U-005 |
| The story | #5 | `doctrine/core-story.md` | — |
| Pricing language | #3 | `doctrine/pricing-logic.md` | U-003 |
| Channels | Tom decision | — | U-008 |

Ask all of a section's questions in one batch. The questions are already
written in those doctrine files — use them verbatim rather than inventing new
ones.
