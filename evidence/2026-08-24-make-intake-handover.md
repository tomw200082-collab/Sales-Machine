# Evidence snapshot — the intake changed hands (2026-08-24)

> **Immutable. True as of 2026-08-24 only.** Never edit; supersede with a new dated
> snapshot. Authority: `system_verified` for everything measured against the live
> Supabase project `rvadsozabmxkkrktwgnv`, the live Make account (team 1240098) and
> GitHub; `user_confirmed` for Tom's decision.
>
> Build: gt-factory-os PR #227 (merged), migration 0329, `sales-leads-poll` redeployed.
> Decision: `doctrine/decisions.md` D-006.

## What changed, and why it had to

The design assumed we would hold a Meta Graph API token (spec §6.1, §2.5). We cannot.

Tom holds **no Meta developer access**. The only Business app on the portfolio,
`Green Tea`, is WhatsApp-oriented and he is not its admin, so its token dialog
offers no lead permissions at all. Developer self-registration blocks at SMS
verification — no code arrives, in either local or international format.

This was diagnosed the slow way first (three wrong guesses across ~24h, all mine),
then settled definitively by a diagnostic built for the purpose.

## The diagnostic — what one API call proved

`GET /debug_token`, called on the poll's failure path, 2026-08-24 10:50:01Z:

```
app:            "Green Tea"
valid:          true
expires:        never
scopes:         business_management, whatsapp_business_management,
                whatsapp_business_messaging, manage_app_solution, public_profile
missing_scopes: ads_management, leads_retrieval, pages_show_list, pages_read_engagement
page_covered_by: []
verdict:        missing_scopes
```

**It was never the Page assignment.** The token was valid and non-expiring the whole
time; it simply carried none of the four permissions lead retrieval needs, because it
was minted from a WhatsApp app. Tom's page assignment work was correct and could not
have helped.

Recorded because the same ambiguity will recur: `(#100) Object does not exist ...
requires pages_read_engagement` has two causes that look identical from outside, and
`granular_scopes.target_ids` is the field that separates them.

## The new path

```
Facebook form → Make (its own Meta-approved app) → POST /ingest
  → normalise · match org · dedupe · store · alert Tom · portal link
```

Make is **transport only**. Storage, phone normalisation, org matching, deduplication,
alerting, the conversion loop and the heartbeat all remain in `sales-leads-poll`.
Make holds no data and makes no decisions.

## The honest risk, and what actually changed about it

D10 forbade Make in this module for a good reason, verified again today: connection
`gteveryday` (id 6309050) expired **2026-06-07T20:37:12Z** — the exact hour leads
stopped. A silently-expiring OAuth token is what killed the pipeline.

**Make is not safer now. The failure is louder.**

With a third party in front, a dead connection and a quiet day are indistinguishable
from inside our system, and lead volume can never separate them because leads are
irregular. So the heartbeat no longer watches lead volume alone: a scheduled Make
scenario pings `route=pulse` hourly and can only succeed while its Facebook connection
is valid. The pulse is regular, so its **absence** is unambiguous. The heartbeat
alarms when the last pulse is over 24h old.

The 2026-06-07 failure cost two months of silence. The same failure now costs one day.

## Verified today

| Fact | Value | How |
|---|---|---|
| Make Facebook connection | valid to **2026-10-23T10:49Z** | Make API, after Tom reauthorised |
| Old scenario `GT Leads — Instant` | inactive; still maps `מה_שם_המסעדה/בית_הקפה/בר_שלך?` and `city` | blueprint read |
| Heartbeat delivery | **sent**, severity `alarm`, 04:00:09Z | `poll_run` route=daily |
| Stock-truth pre-flight | **0 mismatches** | read-only `rebuild_verifier()` equivalent |
| Leads / orgs | 188 / 186, unchanged | live SQL |
| Orgs matched to Shopify | **0** — see Open below | live SQL |

The old scenario's stale mapping is worth recording: it would have written half-empty
rows even if its connection had never expired. That is why `/ingest` now takes Meta's
raw `field_data` and maps it with our own tested mapper (unknown-field alarm included)
rather than trusting a mapping hand-written inside a Make module.

## Test evidence

| Suite | Result |
|---|---|
| `node:test` (all sales) | **73/73** — 17 new: heartbeat-under-Make, `/ingest` contract |
| pgTAP `0329` | **7/7** |
| pgTAP regression `0318`–`0328` | **152/152** |
| Migration 0329 applied twice locally | idempotent |
| root typecheck · `deno check` · `deno lint` | clean (bar the repo-wide `npm:` convention) |

## Truth-rule compliance

- No customer or lead was contacted. `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` stays `false`.
- No factory-os core object read or written.
- D-006 reverses a locked decision and is recorded, dated, with the objection preserved
  on the record rather than quietly dropped.

## Still open

1. **The two Make scenarios are not built** — lead transport and the hourly pulse.
   Awaiting Tom's go-ahead; they live in his account.
2. **No org carries a `shopify_customer_id`** (0 of 186). The conversion job therefore
   cannot fire for any of the 188 imported leads — the import never ran a Shopify
   lookup, and only new leads are matched at ingest. A one-off match run is needed
   before "the pipeline closes its own loop" is true of history as well as of new leads.
3. **Direct Graph API remains the preferred end state.** Now a single defined task for
   whoever administers `Green Tea`: add the four missing permissions, or create a
   Business app Tom owns.
