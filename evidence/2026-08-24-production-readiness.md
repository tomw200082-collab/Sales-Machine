# Evidence snapshot — the last-mile session (2026-08-24)

> **Immutable. True as of 2026-08-24 only.** Never edit; supersede with a new
> dated snapshot. Authority: `system_verified` for everything measured against
> the live Supabase project `rvadsozabmxkkrktwgnv`, the live Shopify store
> `greenteaeveryday`, and Make team 1240098. `user_confirmed` for Tom's
> decisions taken in the session.
>
> Companion: `evidence/2026-08-24-make-intake-handover.md` (the morning's
> hand-over of the intake to Make). This snapshot is the afternoon.

## What changed, in order

### 1. The conversion loop went from complete-and-dead to firing

Before: **0 of 186 orgs** carried a `shopify_customer_id`, so
`sales_core.convert_lead()` — the sole writer of `won` — could not fire for any
of the 188 imported leads. The claim "the pipeline closes its own loop" was true
of no lead at all.

Matched the 186 orgs against the live store (5478 customers) in the tier order
of spec §5.4:

| Tier | Candidates | Matched |
|---|---|---|
| `shopify_customer_id` | 0 | 0 |
| `phone_e164` | 147 | 9 |
| exact `email` | 138 remaining | 4 |
| business email domain | 0 eligible | 0 |
| **Total** | **186** | **13 (7.0%)** — 8.8% of the 147 contactable |

The business-domain tier matched nothing and was **not** relaxed:
`sales_core.is_business_domain` rejects all 147 org domains because all 147 are
free providers. Relaxing it would have folded every `gmail.com` lead into one
fictional business.

**Where Shopify keeps the phone.** Five of the nine phone matches came from the
customer's **address**, not `customer.phone` — GT's own customer-setup
convention deliberately keeps phone and email off the Shopify customer record.
Shopify's `phone:` search covers both, which is why the live matcher already
finds them; anyone re-running the match by hand against `customer.phone` alone
would wrongly conclude that almost nothing matches.

Written by migration **0330** (gt-factory-os PR #231), applied to production via
the `deploy-production` workflow, run **32722792338**, conclusion `success` —
pre-flight `rebuild_verifier` and post-checks green.

Post-apply, live: `orgs_matched=13`, `match_events=13`, `distinct_customers=13`,
`undated=0`.

### 2. Three real conversions

`route=daily` was then run against production. Result:

```
{"ok":true,"checked":13,"converted":3,"errors":[],
 "heartbeat_severity":"alarm","heartbeat_sent":true}
```

| Lead's org | Lead arrived | Order | Amount |
|---|---|---|---|
| חן כהן (ליאבי ביץ) | 2026-05-20 | `#GT13106` | ₪740 |
| קפה ארליך | 2026-05-27 | `#GT13208` | ₪1,554 |
| Roni Ratzaby Hagay (The Monkeys) | 2026-07-10 | `#GT14181` | ₪481 |

Each is the earliest non-cancelled order placed **at or after** its lead — the
rule in `_lib/convert.ts`. Four other matched orgs have orders, all of them
older than their lead, and were correctly left alone: an earlier order proves
the business already bought from us, not that this lead converted.

### 3. The Make scenarios were built

Two scenarios now exist in team 1240098, folder "GT Sales Pipeline":

| Scenario | id | Trigger | State |
|---|---|---|---|
| GT Sales — lead intake → /ingest | 7075235 | `NewLeadMultiple`, hook 3598876 (GT page, **all forms**) | active |
| GT Sales — hourly pulse | 7075243 | `GetForm` on the live form, hourly | active, **proven** |

The pulse is proven end to end: Make reached Facebook, POSTed `route=pulse`, and
the run was recorded — `poll_run` `{"from":"make","pulse":true}` at
`2026-08-24T11:50:54Z`.

The hook watches **every form on the page**, not one form id. The scenario it
replaced watched form `1656468138571162` (`0205.2025-HiTech-2question-new`) —
not the live form at all.

## Two things that were NOT ready — both resolved the same day

*This section replaced its earlier form at 14:40Z. The earlier text recorded two
open unknowns; both were closed, and one of them was closed by discovering the
earlier reasoning was wrong. Keeping the stale version would have left a
snapshot that reads as current and is not.*

### A. The webhook now delivers — and one bad lead used to block every lead after it

Delivery works: a real lead reached Make and ran in **2.2 seconds**
(execution `48522192…`, `2026-08-24T14:20:38Z`).

The delay had a second cause, and it is the more dangerous of the two. The
scenario ran with **`sequential: true`** and Make's data-loss queue on. A bundle
that fails is held; with sequential processing, everything behind it waits —
**forever**. Measured live at 13:53Z: `dlqCount: 1`, `queueCount: 1`,
`iswaiting: true`. A real lead was sitting behind a dead one, and nothing said
so: no alarm fires for "Make is holding your leads", because from our side it
looks exactly like a quiet day.

**One malformed lead was enough to kill the entire pipeline, silently and
permanently.** `sequential` is now off. Lead order carries no meaning here —
`ingest_lead` is idempotent on `(source, external_id)` — so there was never
anything to gain from it.

### B. There is no `field_data`. The answers are in `data`, keyed by the form's own questions

The earlier entry said the app "does not expose `field_data`" and concluded A had
to be fixed before B could be settled. The first half was right; the conclusion
was wrong, and waiting was unnecessary — the shape was readable all along
through Make's `LeadInterface` RPC, which resolves per form.

The v2 `New Lead` module emits **`data`**: an object keyed by each form's own
questions, with metadata in camelCase (`leadgenId`, `dateCreated`,
`campaignName`) rather than the Graph API's snake_case.

Read from two unrelated live forms on the page:

| Form | Standard keys | Custom question |
|---|---|---|
| `0305.2025-HiTech` (1771287887148857) | `שם מלא`, `מספר טלפון`, `email`, `city` | `מה_שם_החברה_שלך?` |
| `0205.2025-2question-new` (1165807205227331) | `שם מלא`, `מספר טלפון`, `email`, `city` | `מה_שם_המסעדה/בית_הקפה/בר_שלך?` |

Different campaigns, different custom questions, **byte-identical standard
keys** — and both report those two under Meta's canonical titles ("Full name",
"Phone number"). That is what marks them as Meta-generated rather than
author-written, and it is the evidence the mapper's Hebrew entries rest on.
Custom questions differ per form and are deliberately not mapped: they surface
as `unmapped` and ride the alert.

Also settled: the trigger's `fields` parameter is a **single-select string on
the webhook**, not an array on the module. Setting it as an array did nothing at
all.

### The Graph API path has never worked, and the record said otherwise

An interim fix routed `/ingest` to read each lead back from Meta, on the stated
grounds that "188 historical leads map with zero unmapped fields" proved that
path. Those leads are `source='import_meta_export'` — **a CSV**. The Graph path
has never once succeeded against this page.

`debug_token`, live, now names the cause exactly:

```
verdict: missing_scopes
missing: ads_management, leads_retrieval, pages_show_list, pages_read_engagement
```

The read-back code is kept as a *preference* — correct the day those scopes
exist, and it fails with a named error rather than silently — but nothing
depends on it.

### A cron that failed 144 times a day, by design

`routePoll` never checked `state.enabled`. The gate was honoured inside
`runPoll`, but form discovery runs **before** it, so a poll that is off forever
by design still called Meta every ten minutes and wrote a failed row. Measured:
6 runs in the last hour, 6 failed. A permanently-red table is a table people
stop reading, and `poll_run` is the one the heartbeat is built on. A disabled
poll now records a skip and makes no network call.

## A correction to the record

The masterprompt and the 2026-08-10 spec both describe the live form
(`0205.2025-2question-new`, id `1165807205227331`) as asking two questions —
name, phone, email — and open U-013 on whether to ask for the business name
again.

Read live from Meta today, the form asks **six**:

| key | type |
|---|---|
| `שם מלא` | FULL_NAME |
| `מספר טלפון` | PHONE |
| `email` | EMAIL |
| `city` | CITY |
| `מה_שם_המסעדה/בית_הקפה/בר_שלך?` | CUSTOM |
| `האם_את.ה_מנהל.ת_או_בעלים_בתחום_המסעדנות?` | CUSTOM |

The business name **is** already being asked, and so is a manager/owner
qualifier. U-013 is therefore not a decision about whether to add the question —
it is answered in the field. What remains open is why 39 imported leads carry
neither phone nor email despite the form collecting both.

## Portal defects found and fixed

| Defect | Why it mattered | Fix |
|---|---|---|
| `lead_event.actor` rendered raw: `system` (188 events), `system:backfill-0330` (13), `system:sales-leads-poll` (6) | engineering slugs on a Hebrew screen, in the drawer timeline and the admin activity feed; `lead_event` is append-only so the stored value can never be tidied | `actorLabel()` translates them and degrades any unknown `system:*` to "מערכת" |
| `matched_existing_customer` had no timeline line | the badge claimed the business already buys from us and showed no evidence for it | the timeline now names the tier: לפי טלפון / לפי אימייל / לפי מזהה לקוח |
| the Today queue never stated the rule behind its count | "why these 15?" was unanswerable from the screen | the line now ends "מתוך מכסה יומית של 15 לכל התור" |

gt-factory-os-portal PR #218. `vitest` 246/246, `tsc --noEmit` clean.

## Queue shape, live

| Number | Value |
|---|---|
| leads | 188 |
| Today queue rows | 149 (39 uncontactable excluded by 0326) |
| daily cap | 15, one budget across the whole queue |
| conversions at the top of Today | 3 |
| orgs with no display name | 0 |
| flagged duplicates | 2 |

## Truth-rule compliance

- No lead and no customer was contacted. `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED`
  remains `false`.
- No factory-os core object read or written. The Shopify reads were customer and
  order reads through the Admin API, not catalog or stock.
- The two adjacent failures (`lionwheel_poll` date parsing, `dispatch-alerts-cron`)
  were **not** touched: they are outside this lane. Recorded in
  `recipes/intake-monitoring.md`.

---
_Snapshot taken 2026-08-24. Superseded, never edited._
