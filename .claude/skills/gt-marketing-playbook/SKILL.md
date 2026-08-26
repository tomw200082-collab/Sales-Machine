---
name: gt-marketing-playbook
description: >
  The single entry point for any GT marketing or sales-copy work. Routes the job
  to the right vendored skill in the right order, pre-loaded with GT's own
  context so nothing interviews Tom twice. Use whenever the work is marketing,
  copy, a page, SEO, content, or positioning — "תכתוב לי", "תשפר את הטקסט",
  "דף נחיתה", "למה הדף לא ממיר", "מה לפרסם", "קופי", "שיווק", "תקציר מכר",
  "write copy", "landing page", "improve this page", "marketing", "SEO",
  "what should we publish", /gt-marketing-playbook. Prefer this over calling
  copywriting / ogilvy / page-cro / seo-audit directly — it loads GT's context
  first, and those skills interview from scratch without it.
---

# GT Marketing Playbook

One door. Fixed sequence. GT's own context loaded before anything is written.

The twelve vendored skills in `.claude/skills/` are generic and each one
interviews from scratch. This skill is the layer that makes them GT's: it holds
the order they run in, and it holds the context file they all read.

## Step 0 — always, before anything else

Read `.claude/product-marketing-context.md`.

- **It exists** → load it, do not re-ask anything it answers. Go to the routing
  table.
- **It does not exist, or the job needs a field marked `UNRESOLVED` in it** →
  run **the capture pass** (below) for the missing fields only, write them in,
  then continue. Once written, never ask again.

Also read `CURRENT_STATE.md` UNRESOLVED. If the job depends on an open ID, say
which one in a single line and work around it — do not fill it silently
(rule 3).

## The sequence

Grounded in the verified research base
(`knowledge/market/sales-buildout-research-2026-07-18.md`, finding 1, `3-0
verified`): profiling and positioning come before assets, assets before
distribution, distribution before scale. Later stages do not run on an
unresolved earlier one.

```
1  POSITION   who it is for, what it replaces, why GT      →  ogilvy
2  STORY      the one education-first narrative            →  ogilvy + content-strategy
3  ASSET      the page, the deck, the email, the post      →  copywriting  → copy-editing
4  PAGE       structure and conversion of that asset       →  landing-page → page-cro
5  FOUND      get it found                                 →  seo-audit, schema-markup
6  MEASURE    prove it did something                       →  analytics-tracking
```

Positioning is the highest-leverage decision and the cheapest to get wrong —
Ogilvy's own hierarchy, and the reason step 1 is not skippable. If a request
arrives at step 3 with step 1 unresolved, do step 1 first, in one pass, and say
so in one line.

## Routing — what Tom asks → what runs

| Tom says | Sequence |
|---|---|
| "write copy for X" / "תכתוב לי" | 1 → 3 → `stop-slop` (English only) |
| "improve this text" / "תשפר את הטקסט" | `copy-editing` → `stop-slop` (English only) |
| "landing page" / "דף נחיתה" | 1 → 4 → 3 → 5 |
| "why isn't it converting" / "למה לא ממיר" | `page-cro`, then 3 for the rewrites it asks for |
| "what should we publish" / "מה לפרסם" | 2 → `content-strategy` |
| "why aren't we found" / "למה לא מוצאים אותנו" | `seo-audit` → `schema-markup` |
| "vs a competitor" / "מול מתחרה" | `competitor-alternatives` (needs step 1 done) |
| "are we measuring this" | `analytics-tracking` |
| product description, catalog line, pricelist copy | 1 → `copywriting`, priced from `doctrine/pricing-logic.md` only |

`programmatic-seo` stays parked. It is built for hundreds of template pages
from a dataset; GT sells a few dozen SKUs. Reach for `content-strategy`.

## The capture pass — run once, never again

The questions are already written down. Do not invent new ones, and do not
invent answers.

| Missing field | Questions | Source |
|---|---|---|
| ICP, Dream-100 criteria, bad-fit | 5 questions | `doctrine/icp.md` (Interview #1, U-005) |
| Core story, proof assets, honest claims | 4 questions | `doctrine/core-story.md` (Interview #5) |
| Pricing and terms language | 5 questions | `doctrine/pricing-logic.md` (Interview #3, U-003) |

Ask them **in one batch**, in Hebrew, in that order. Not one per turn, not
again next session.

Write the answers to `.claude/product-marketing-context.md` using
`context-template.md`. Every field carries `source`, `date`, `authority`.

Two things the capture pass may never do:

- **Fill a gap with a guess.** No answer → the field stays `UNRESOLVED` with a
  new `U-0xx` line in `CURRENT_STATE.md`. Visibly open beats quietly wrong.
- **Write to `doctrine/`.** The context file is a derived working artifact and
  lives in `.claude/`. Doctrine is Tom's, approved in writing, logged in
  `doctrine/decisions.md` (rule 5). When an answer is stable enough to be
  policy, propose the doctrine edit — do not make it.

## Hebrew

GT's market is Israeli. Copy is Hebrew unless Tom says otherwise.

- `ogilvy` — principles, carries over intact.
- `copywriting`, `copy-editing`, `landing-page`, `page-cro`, `content-strategy`
  — language-neutral process. Run them, write the output in Hebrew.
- **`stop-slop` is English-only.** Its substance is English string matching:
  a phrase-removal list, "no em dashes", "sentence starts with a Wh- word",
  "kill the adverbs". Never run it over Hebrew copy and call the result clean.
- `copy-editing/references/plain-english-alternatives.md` is an English
  word-swap table. Skip it for Hebrew.

Customer-facing Hebrew additionally needs a Tom-approved register entry, per
the PRODUCTION locked decisions.

## Boundaries

- **Every number comes from a recipe run live** — `recipes/account-value.md`,
  `sleeping-radar.md`, `whitespace.md`, `sales-report.md`. Never from a
  snapshot quoted as current, never from memory (rule 2).
- **Every price comes from `doctrine/pricing-logic.md`** — which is currently
  `UNRESOLVED (U-003)`. Until it is decoded, do not state a price or a discount
  in copy. Say the field is open and leave the slot.
- **Output is `inferred` until Tom confirms it.** A headline this playbook
  writes is a proposal, not policy (rule 1).
- **Nothing sends.** These skills write words. Any customer-facing send stays
  behind `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` (default `false`) plus
  confirm-before-acting.
- **No runtime code in this repo, ever.** A page these skills design is built
  in a runtime repo, not here (D-003, U-008).
- **Never touch factory-os core.** Catalog reads via curated views only.

## Hands off to

When their doctrine inputs land, the outreach motions belong to the planned
playbooks in `doctrine/playbooks/` — `winback.md`, `land-and-expand.md`,
`dream-100.md`, `first-90-days.md` — not here. This skill makes the words and
the pages. Those make the moves.
