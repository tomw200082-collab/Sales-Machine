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

## Two things that are NOT ready, stated plainly

### A. The webhook has never delivered a lead

Tom created a test lead through Meta's lead-ads testing tool at
`2026-08-24T11:53:41Z`. It exists in Meta — `leadgen_id 1771408137623570`,
confirmed by reading the form's newest lead through Make. It never reached Make:
hook queue 0, zero scenario executions.

The stale hook (2797155, bound to the dead `GT Leads — Instant` scenario) was
deleted along with the new one, and a single fresh hook (3598876) created so
Make re-subscribes the page. **Unverified until another test lead is created.**

### B. `field_data` is not in the Make app's lead output

The test lead was pushed through the exact production mapping. It was **rejected
and kept**, which is the designed behaviour:

```
reason: field_data missing or not an array
raw:    {"route":"ingest","source":"facebook","form_id":"1165807205227331",
         "created_at":"2026-08-24T11:53:41.000Z","field_data":null,
         "external_id":"1771408137623570", ...}
```

`external_id` and `created_at` mapped correctly; every other field came back
empty. Probing the app's v2 modules directly showed the same: `listLeads` and
`GetLeadDetails` return `leadgenId`, `dateCreated`, `formId`, `adId`, `adName`,
`adsetName`, `campaignId`, `campaignName`, `platform`, `isOrganic` — and no
answers, no `field_data`, no `fields`, no `answers`.

`NewLeadMultiple` (the production trigger) is the one module with a `fields`
parameter whose enum includes `field_data`, and it cannot be exercised without a
webhook delivery. So A must be fixed before B can be settled.

**No lead is lost by this.** `/ingest` stores every rejection with its full raw
body, and the scenario has Make's data-loss queue on, so a refused bundle is
replayable.

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
