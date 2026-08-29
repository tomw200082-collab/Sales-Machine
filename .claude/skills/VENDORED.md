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

---

# Vendored: `google/skills` (2026-08-29)

Copied in from a second public upstream on 2026-08-29 at Tom's direction
("download these skills — it will help with our social-networks project").

The same framing as above applies: **these are tools, not truth.** They carry no
authority grade, they make no claim about GT, and anything they produce is
`inferred` until confirmed. They are API how-to documentation, not doctrine.

| Upstream | Commit | License | Skills |
|---|---|---|---|
| [google/skills](https://github.com/google/skills) | `a7123f8` (2026-08-28) | Apache-2.0 (`LICENSE-google-skills-apache-2.0.txt`) | the 17 below |

## Read this before reaching for them

**There is no social-media skill in that repository.** The full catalog was
checked: 127 skills across `cloud/` (110), `ads/` (13), `analytics/` (2) and
`developers/` (2). Searching the whole upstream index for `instagram`,
`facebook`, `tiktok`, `linkedin`, `social media`, `threads`, `whatsapp` and
`business profile` returns **zero** hits; `youtube` appears exactly once, and
only inside one skill's own description of what it can look up. Nothing here
writes a post, plans a content calendar, or touches a social platform's API.

What it *is*: developer documentation for Google's own advertising and
measurement APIs, plus Google Cloud infrastructure. The parts that touch a
social/paid motion at all are the **measurement and paid-media** ones — GA4
reporting on the traffic social sends, and Google Ads / Customer Match on the
paid side. For the actual social content work, the skills already in this
directory (`gt-marketing-playbook` → `ogilvy`, `copywriting`, `content-strategy`)
remain the ones that do it.

## What was taken

The 110 `cloud/` skills were **deliberately left behind** — GKE, Cloud Run, IAM,
BigQuery, Spanner and the rest are factory/infrastructure concerns with no
bearing on this repo, and 110 extra skill descriptions would load into every
session's context for nothing. `finding-google-skills` (below) can fetch any of
them on demand if one is ever actually needed.

**Plausibly useful here — measurement & paid media (5)**

| Skill | What it does |
|---|---|
| `google-analytics-data-api-basics` | Query GA4 reports programmatically — sessions, users, conversions, by source/medium. This is how you'd measure what social actually sends to the Shopify store |
| `google-analytics-admin-api-basics` | GA4 account/property config: data streams, custom dimensions, conversion events, Google Ads links |
| `google-ads-api-quickstart` | Google Ads API credentials, developer token, client libraries, first "retrieve campaigns" script |
| `google-ads-api-mcp-setup` | Installs Google's open-source Google Ads MCP server so campaign/reporting data can be queried in natural language |
| `google-ads-api-account-diagnostics` | Diagnoses conversion loss, low lead flow, lost impression share |

**Audience / conversion plumbing — relevant only if paid retargeting is ever run (3)**

`data-manager-api-setup` · `data-manager-api-audience-ingestion` ·
`data-manager-api-event-ingestion` — uploading a customer list as a Customer
Match audience, and pushing offline conversions back to Google.
**These upload customer PII to Google.** That is a customer-data export, not a
copy task: it sits squarely inside the External-action authorization rules and
needs Tom's explicit word before a single row moves.

**Catalog loaders (2)**

`finding-google-skills` — looks up the right Google skill on demand from a
**remote** catalog index (it fetches over the network at run time).
`retrieving-developer-knowledge` — searches official Google developer docs, via
the Developer Knowledge MCP server or a REST fallback. Neither is vendored
knowledge; both are pointers to live Google endpoints.

**Vendored but almost certainly dead weight here (7)**

`google-mobile-ads-get-started` · `google-mobile-ads-banner` ·
`google-mobile-ads-interstitial` · `google-mobile-ads-rewarded` ·
`google-mobile-ads-android-migrate-to-next-gen` · `ima-sdk-client-side` ·
`ima-dai-sdk`

These are AdMob/Ad Manager monetization for an Android/iOS/Unity **app**, and
video-ad serving (VAST/VMAP/DAI) for a **video player**. GT has neither. They
came in because the ask was for the skills in that repo, not for a filtered
subset — but nothing in this workspace will ever fire them. Deleting the seven
is a one-line change and costs nothing; left in place pending Tom's call.

## Notes before use

- **Every one of these skills assumes Google API credentials this workspace does
  not have.** A Google Ads developer token, an OAuth client, a GA4 property ID,
  a Cloud project with the API enabled. None of that exists yet, and none of it
  is set up by reading a skill. Each is a real onboarding step with its own
  approval, not a five-minute task.
- **`finding-google-skills` and `retrieving-developer-knowledge` reach out to
  the network** at run time — a remote catalog index and Google's Developer
  Knowledge endpoints. They are read-only lookups, but they are not offline.
- **`google-ads-api-mcp-setup` installs a third-party MCP server** (Python +
  pipx) and wires it into the assistant's config. That is a workspace-level
  change, not a skill invocation — Tom's decision, not a side effect of asking
  a question about campaigns.
- **The Data Manager skills move customer PII to Google.** Email addresses and
  phone numbers, hashed, uploaded as an audience. Treat every run as a
  customer-facing external write: understand before writing, confirm before
  acting, and nothing moves without Tom.
- **Files only, no runtime code.** Markdown and one XML data asset
  (`google-mobile-ads-get-started/assets/skadnetwork-identifiers.xml`). The
  upstream repo's `plugins/`, git submodules, `index.json` and `.claude-plugin/`
  were not copied. `.claude/settings.json` was not modified.
- **No edits on adoption.** All 17 skill trees are byte-identical to upstream.

## Updating

Re-clone `https://github.com/google/skills` and copy `skills/<category>/<name>/`
over the local directory. No lockfile, no auto-update. Upstream says it is
"under active development", so expect drift.

## License

Apache-2.0. Copyright remains with Google LLC. The full license text travelled
with the skills as `LICENSE-google-skills-apache-2.0.txt` in this directory, as
Apache-2.0 §4 requires for redistribution.

---

# Vendored: `Panniantong/Agent-Reach` (2026-08-29)

Copied in on 2026-08-29 at Tom's direction, in the same breath as the Google
skills above ("download this one to all the relevant repos too").

| Upstream | Commit | License | What was taken |
|---|---|---|---|
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | `06c202b` (2026-08-25, v1.5.0) | MIT (`agent-reach/LICENSE`) | `agent_reach/skill/` only — one skill |

## This is not a skill repository

Everything else vendored in this directory is markdown that works the moment it
is read. **Agent Reach is a Python package** — a CLI that installs, routes and
health-checks *other people's* tools (OpenCLI, twitter-cli, rdt-cli, bili-cli,
yt-dlp, Jina Reader, mcporter/Exa) so an agent can read 15 platforms. The skill
taken here is one directory inside it: a routing table that tells an agent which
command to run. **The commands do not exist until the package is installed.**

Only `agent_reach/skill/` was copied — the `agent_reach/` Python source, `tests/`,
`config/`, `scripts/` and `pyproject.toml` were **not**, and must not be: this
repo takes no runtime code, ever (`CLAUDE.md`, write boundaries). Installing the
tool is `pip install agent-reach`, which happens in an environment, not in a
commit.

## What it would unlock — mapped to the digital roadmap

This is the capability the Google skills did not have. Read-only access to:

| Platform | What it can read | Roadmap tasks |
|---|---|---|
| Instagram | user search, profile, a user's recent posts, Explore | `i1` which account is official · `i6` opening baseline · competitor scans |
| Facebook | search, pages, feed, group lists | `f3` page details |
| LinkedIn | profile detail, company pages, people search, job search | `l1` company page · `l2` personal profile · `l6` target connection list |
| YouTube | transcripts + video search | `y1` locating the channel · `y3` content recycling |
| Web / RSS / Exa | any page as clean text, semantic web search | competitor and content research feeding `content-strategy` |
| Twitter/X, Reddit | search, threads, discussion | market listening |

## What actually works, and where — read this before promising anything

**Zero config, works anywhere:** web page reading (Jina Reader), YouTube
transcripts (yt-dlp), RSS, GitHub, Exa web search, V2EX, Bilibili.

**Needs a desktop with the user's own logged-in Chrome:** Instagram, Facebook,
LinkedIn, Reddit, XiaoHongShu. These route through OpenCLI, which reuses a real
browser session. **They cannot work from the remote Claude Code container** — it
has no Chrome profile and no GT logins, and never will. That is precisely the set
of platforms the roadmap cares most about. They work in Claude Code running
locally on Tom's own machine; nowhere else.

**`pip install agent-reach` is blocked in the remote container** (the sandbox
denied it on 2026-08-29). So in web/remote sessions this skill is documentation,
not a working capability.

## Account risk — Tom's call, stated once

Reading Instagram, Facebook and LinkedIn through a logged-in browser session is
against those platforms' terms of service. The session at risk is a real GT
business account, and the failure mode is a restriction or a ban on the account
the roadmap is trying to build up. The zero-config channels above carry no such
exposure. Nobody should point this at a GT-owned social login without Tom saying
so explicitly.

## The frozen-copy problem

Upstream's entire value proposition is that **they chase platform breakage** —
their own README's example is yt-dlp getting blocked by Bilibili and the router
switching to bili-cli with no user action. A copy committed here does not
receive those fixes. Treat this tree as a map of what the tool does, not as a
current command reference: when the tool is actually installed, its own shipped
skill is the authority, and this copy is a snapshot of 2026-08-25.

## One edit on adoption

Upstream's `SKILL_en.md` opens with `MUST USE when user wants to
research/search/look up/find anything on the internet`. That fires on a large
share of ordinary requests, in a workspace where the CLI is usually not
installed — every one of those would send a session chasing commands that do not
exist. A short **GT note** was prepended to the body of `SKILL.md` (not to the
frontmatter, not to any reference) saying: check `agent-reach doctor --json`
first, and if the command is not found, say so and stop instead of guessing.
That is the only change. The seven `references/` files and `SKILL_zh.md` are
byte-identical to upstream.

## Layout note

Upstream ships the Chinese `SKILL.md` and an English `SKILL_en.md` side by side.
Here `SKILL.md` is the **English** one (so the skill loader reads English) and
the Chinese original is kept alongside as `SKILL_zh.md` for fidelity. Note that
`references/` is **Chinese only** upstream — the English skill points at Chinese
reference files, including `career.md`, the LinkedIn one.

## Where else this lives

Vendored in this repo only. Social and market research is sales-and-marketing
work, and this is the sales brain. `gt-factory-os` (backend), `gt-factory-os-portal`
(UI) and `gt-factory-os-production-brain` (governance) have no use for reading
Instagram, and their lane rules say not to write outside the dispatched lane —
so no copies there. The brain's workspace-wide ledger carries a pointer back to
this entry. Say the word if it should be duplicated.

## Updating

`git clone https://github.com/Panniantong/Agent-Reach` and copy
`agent_reach/skill/` over this directory, re-applying the English/Chinese
filename swap and the GT note. Better: install the real tool and let it ship its
own current skill.

## License

MIT. Copyright (c) 2025 Agent Eyes. The full licence text travelled with the
skill as `agent-reach/LICENSE`, as MIT requires.
