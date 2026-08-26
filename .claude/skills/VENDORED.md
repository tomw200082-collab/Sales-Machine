# Vendored third-party skills

Copied in from a public upstream repository on 2026-08-26 at Tom's direction.

**These are tools, not truth.** Nothing here is a knowledge card, doctrine, or
evidence. They carry no authority grade because they make no claim about GT —
they are general-purpose copy, SEO and conversion methods that a person could
have read in a book. The authority hierarchy in `CLAUDE.md` is unaffected, and
the 7 truth rules apply to their *output* exactly as they apply to anything
else: a headline these skills generate is `inferred` until Tom confirms it, and
any number they put in a sentence still has to come from a recipe run against
a live system.

| Upstream | Commit | License | Skills |
|---|---|---|---|
| [boraoztunc/skills](https://github.com/boraoztunc/skills) | `645553c` (2026-08-15) | MIT — README only, see below | the 12 below |

## What is here

**Copy** — write and sharpen the words.

| Skill | Command | What it does |
|---|---|---|
| `ogilvy` | `/ogilvy` | Ogilvy's advertising principles: positioning first, the promise, headline discipline, long-form copy, visual logic |
| `copywriting` | `/copywriting` | Write or rewrite page copy. Ships PAS/AIDA and other frameworks under `references/` |
| `copy-editing` | `/copy-editing` | Improve existing copy through focused single-dimension passes |
| `stop-slop` | `/stop-slop` | Strip AI writing tells from prose |

**Pages** — decide what a page is for and make it convert.

| Skill | Command | What it does |
|---|---|---|
| `landing-page` | `/landing-page` | Design or rewrite a single-offer landing page |
| `page-cro` | `/page-cro` | Raise conversion on an existing marketing page |
| `competitor-alternatives` | `/competitor-alternatives` | Comparison and alternative pages — SEO plus sales enablement |

**Findability** — get found, and measure whether it worked.

| Skill | Command | What it does |
|---|---|---|
| `seo-audit` | `/seo-audit` | Audit and diagnose SEO issues on a site |
| `schema-markup` | `/schema-markup` | Add or fix structured data |
| `programmatic-seo` | `/programmatic-seo` | Template-plus-data pages at scale |
| `content-strategy` | `/content-strategy` | Decide what to publish and why |
| `analytics-tracking` | `/analytics-tracking` | Set up or audit tracking and measurement |

## Provenance and licence — read before redistributing

`boraoztunc/skills` is a **re-publisher**, not the origin of everything it
ships: it carries four separate `LICENSE-*` files for trees vendored from other
authors. Of the twelve skills taken here:

- `ogilvy` and `stop-slop` declare `license: MIT` in their own frontmatter.
  `stop-slop` also names its author (Hardik Pandya) and its origin
  (`hardikpandya/stop-slop`).
- **The other ten declare no licence of their own.** They are covered only by
  the upstream README's one-word `## License / MIT`, and **the repo ships no
  root `LICENSE` file** — so no copyright holder and no permission notice
  travel with them.

That is thinner provenance than the MIT skills in
`gt-factory-os-production-brain/.claude/skills/`, where each upstream ships a
real `LICENSE`. Internal use only. Do not redistribute this directory, and do
not treat its text as GT-owned. Flagged for Tom.

## Notes before use

- **The set is English-calibrated to different degrees.** `ogilvy` is
  principle-level and carries over to Hebrew intact. `copywriting`,
  `copy-editing`, `landing-page`, `page-cro` and `content-strategy` are
  language-neutral process with English examples. `copy-editing/references/plain-english-alternatives.md`
  is an English word-swap table and does nothing for Hebrew.
  **`stop-slop` is the outlier:** most of its substance is English string
  matching — a removal list of English throat-clearing phrases, "no em dashes",
  "sentence starts with a Wh- word", "kill the adverbs". Its general rules
  transfer; its lists do not. Do not run it over Hebrew copy and call the
  result a clean pass.
- **Do not call these skills directly — go through `gt-marketing-playbook`.**
  It is the single entry point: it holds the order they run in (position →
  story → asset → page → found → measure) and it loads GT's context before
  anything is written. Called bare, each of these skills interviews from
  scratch.
- **Several skills read `.claude/product-marketing-context.md` before asking
  questions** (`copywriting`, `copy-editing`, `content-strategy`, `page-cro`,
  and others). That file does not exist yet. `gt-marketing-playbook` owns it:
  first run it asks the capture-pass questions **once**, in one batch, using
  the questions already written in `doctrine/icp.md`, `doctrine/core-story.md`
  and `doctrine/pricing-logic.md` — then writes the answers with source, date
  and authority grade, and never asks again. Unanswered fields stay
  `UNRESOLVED` with a `U-0xx` line rather than being filled in. The file lives
  in `.claude/` because it is a derived working artifact, **not doctrine** —
  doctrine is Tom's, approved in writing and logged in `doctrine/decisions.md`
  (rule 5).
- **`programmatic-seo` assumes scale GT does not have.** It is built for
  hundreds of template-generated pages from a dataset. GT sells a few dozen
  SKUs. Vendored because the ask was for everything useful, but reach for
  `content-strategy` first.
- **The SEO skills assume a site you control end to end.** GT sells through
  Shopify, where theme templates and URL structure are partly Shopify's.
  Check what is actually editable before promising a fix.
- **`copywriting` points at sibling skills that were not vendored** —
  `email-sequence`, `popup-cro`. `content-strategy` points at `seo-audit`,
  which *is* here. The first two pointers resolve to nothing.
- **Customer-facing output stays behind the frozen flag.** These skills write
  words, they do not send them. Anything that would reach a customer is still
  gated by `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` (default `false`) and Tom's
  confirm-before-acting rules.

## One edit on adoption

`ogilvy/SKILL.md` declared `name: ogilvy-copywriting` while its directory is
`ogilvy`. Skill `name` should equal its directory name, and upstream's own
README documents the command as `/ogilvy`, so the `name` field was aligned.
That is the only edit; every other file is byte-identical to upstream.

## Updating

Re-clone the upstream repo and copy `<name>/` over the local directory. There
is no lockfile and no auto-update. Re-apply the `ogilvy` name fix.

## Also vendored elsewhere in this workspace

The four copy skills (`ogilvy`, `copywriting`, `copy-editing`, `stop-slop`) also
live in `gt-factory-os-production-brain/.claude/skills/`, which carries the
workspace-wide provenance ledger for every vendored skill. Keep the two copies
byte-identical when updating.
