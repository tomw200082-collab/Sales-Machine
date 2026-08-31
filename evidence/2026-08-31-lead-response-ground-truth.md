# Evidence — lead response ground truth, 2026-08-31

> **Immutable snapshot.** True as of `2026-08-31 11:32Z–12:10Z`. Superseded, never edited.
> **Authority grade:** `system_verified` for every figure below — each is the output of a
> read-only query against Supabase `rvadsozabmxkkrktwgnv`, run in this session.
> **Method:** `recipes/intake-monitoring.md` for the transport checks; ad-hoc SQL,
> reproduced inline, for the rest.
> **Context:** `docs/plans/2026-08-31-lead-response-system-masterprompt.md` (gt-factory-os-production-brain).

---

## 1. The lead table

```
leads_total 199 · leads_new 141 · leads_won 3 · events_total 359
leads_ever_touched 69 · orgs 196
oldest_lead 2023-06-18 · newest_lead 2026-08-29 20:16:27Z
```

By status: `new 141` (0 ever touched) · `lost 43` (43 touched) · `working 12` (12) ·
`won 3` (3). **58 leads have been worked**, all of them recently — `status_change`,
`assignment` and `note` events run to `2026-08-31 09:13Z`.

Arrivals, trailing 30 days:
`08-01: 1 · 08-03: 1 · 08-06: 1 · 08-07: 4 · 08-08: 3 · 08-09: 1 · 08-24: 5 · 08-25: 1 ·
08-26: 1 · 08-27: 2 · 08-28: 1 · 08-29: 1`.

## 2. Transport health — the intake is alive

| Check | Value | Verdict |
|---|---|---|
| Last hourly pulse | `2026-08-31 11:11:17Z`, age 21 min, `forms_visible: 1` | green |
| `poll_run` rows, last 48 h | 339 | green |
| Rows in `lead_reject` | 7 | see §5 |

The `08-30 → 08-31` lead gap is one working day (`08-29` was a Saturday) against an
affirmative pulse. That is a quiet day, not the 2026-06-07 signature. The masterprompt's
two-working-day halt condition was checked and **not** tripped.

## 3. Backlog triage — the 141

| Tier | Count | Handling |
|---|---|---|
| recent (≤90 days) | **94** | the call list |
| cold (>90 days) | **35** | revival batch, not a warm lead |
| already a Shopify customer | **10** | belongs to the existing-customer motion |
| flagged duplicate | **2** | merge; do not contact twice |

All 141 carry a phone number. **There is no dead-by-missing-contact bucket** — the
backlog cannot be reduced by data hygiene, only by someone contacting people.

At the configured cap (`sales_core.app_setting.queue.daily_cap = 15`): **7 working days
to clear the recent tier, 10 to clear all 141.** That is the number `U-011` was missing.

## 4. First response — the honest baseline

| Measure | Value |
|---|---|
| Median first response, all touched leads | 23,099 h (≈ 2.6 years — imported 2023–2026 leads only now being worked) |
| Median first response, 30-day window | **4,718 min ≈ 3.3 days** |
| Leads in the 30-day window / answered | 22 / 14 |
| First-order rate, 30-day cohort | **0 of 22** |
| First-order rate, 90-day cohort | **1 of 117 = 0.85 %** |
| Configured SLA | 24 h |

**Trap recorded so it is not repeated:** three `converted` events fall inside the 30-day
window but belong to older leads converted by the 2026-08-24 backfill. Dividing them by
the 22 leads in the window gives a **13.6 % conversion rate that never happened.** Cohort
and calendar counts must never share a denominator.

## 5. Two leads lost, recoverable until 2026-11-22

`sales_core.lead_reject` holds two real Facebook leads that never became rows:

| leadgen id | Meta timestamp | form id | reason |
|---|---|---|---|
| `1807021066847822` | `2026-08-24T13:44:20Z` | `1165807205227331` | Meta lookup returned no `field_data` |
| `1469012341930658` | `2026-08-24T13:47:45Z` | `1771287887148857` | same |

Reason text, verbatim: *"a lead needs at least a phone or an email — and the Meta lookup
for leadgen id … returned no field_data (check META_PAGE_ACCESS_TOKEN and its Leads
Access on the page)"*. Retried 2026-08-28, rejected again. Meta retains lead content for
90 days, so these are recoverable **until 2026-11-22** and not after.

Also visible here: **a second form id, `1771287887148857`**, which no current document
mentions and which the pulse does not see (`forms_visible: 1`).

## 6. The finding that changes the plan — WhatsApp is already live

The masterprompt's §2.3 states *"No WhatsApp Business API account. No provider. No
dedicated number in the API."* Measured, all three are false.

| Fact | Value |
|---|---|
| WhatsApp Cloud API live since | **2026-06-26 21:10Z** |
| `order_intake.wa_event_log` rows | **24,028**, latest `2026-08-31 11:30:05Z` |
| Inbound events per day, last full week | ~300–500 |
| `order_intake.wa_session` | 805 |
| `order_intake.wa_customer_map` | 195 numbers |
| Provider | **Dualhook**, coexistence — staff keep the WhatsApp Business app on the same number |
| Staff-echo events (proof coexistence works) | **9,440** |

**Consequence:** the two-to-three-week WhatsApp queue the plan treats as its long pole is
already served. Business verification, provider, number and coexistence are done.

### 6.1 The un-captured stream

| Measure | Value |
|---|---|
| Inbound messages classified `ignored_unknown_or_disabled` | **5,707** |
| Distinct unknown senders, since 2026-06-28 | **275** |
| …last 30 days | **163** |
| …last 7 days | **58** |
| Of the 275, matching `sales_core.lead` | **1** |
| Of the 275, matching a `new` lead | **0** |
| Of the 275, matching `sales_core.org` | **1** |
| Of the 275, matching `order_bot.customer` (93 rows) | **1** |

**Stated with its limits, per truth rule 3.** `unknown` means "no row in
`wa_customer_map`", not "new lead". The conversation shapes argue most are not enquiries:
average **20.8** inbound messages per sender, **131** senders with more than 5 messages,
**117** whose conversation spans over 7 days. `wa_customer_map` holds 195 numbers against
roughly 700 Shopify customers, so most real customers land in this bucket too.

The defensible claim is therefore narrow and still serious: **GT's largest inbound
channel has no identification layer, so the number of real leads inside it is unknown.**
The only lead-shaped population that can be named today is the single-message tail —
**36 senders all time, 11 in the last 30 days** — and that is a floor, not an estimate.
Opened as `U-020`.

## 7. Attribution is nearly absent

Of 199 leads: **11** carry `campaign_name`, **11** carry `ad_name`, **11** carry
`form_id`, 198 carry `platform`. Two distinct campaign names, one distinct form id.
Conversion-by-category is therefore computable **going forward only** — the 188 imported
leads cannot be attributed retroactively.

## 8. Live-versus-repository check (landmine 7)

Established with `list_edge_functions`, not grep:

- `sales-lead-fanout` — **deployed and ACTIVE**, with **no source in `gt-factory-os` or on
  `origin/main`**. A live function nobody can read.
- `wa-order-bot` — **present in the repository, NOT deployed.** The live ingress is the
  Node Fastify route, exactly as its README says. Grepping the repo would have concluded
  the opposite in both cases.

## 9. Live production error, unrelated to leads but nobody has surfaced it

`order_intake.wa_event_log` carries seven rows of
`error: Anthropic messages failed status=400 … "Your credit balance is too low to access
the Anthropic API."` — from `2026-07-27 06:44Z` to **`2026-08-31 08:11Z`**. The order
bot's parse step is failing in production on billing, today.

---

## Queries

Every figure above came from one of these. They are methods, not facts; re-run them
rather than quoting this file as current.

```sql
-- §1
select (select count(*) from sales_core.lead)                                as leads_total,
       (select count(*) from sales_core.lead where status='new')             as leads_new,
       (select count(*) from sales_core.lead where status='won')             as leads_won,
       (select count(*) from sales_core.lead_event)                          as events_total,
       (select count(distinct lead_id) from sales_core.lead_event
          where event_type not in ('imported','created'))                    as leads_ever_touched,
       (select max(created_at) from sales_core.lead)                         as newest_lead;

-- §3  backlog triage (shipped as api_read.v_sales_backlog_triage, migration 0341)
select case when l.possible_duplicate_of is not null then 'duplicate'
            when o.shopify_customer_id is not null   then 'existing_customer'
            when l.created_at >= now() - interval '90 days' then 'recent'
            else 'cold' end as tier, count(*)
  from sales_core.lead l left join sales_core.org o on o.id = l.org_id
 where l.status='new' group by 1;

-- §4  first response (shipped as api_read.v_sales_first_response, migration 0340)
select round(percentile_cont(0.5) within group (order by
         extract(epoch from (fr.first_response_at - l.created_at))/60.0)::numeric, 1)
  from sales_core.lead l
  join lateral (select min(e.created_at) as first_response_at
                  from sales_core.lead_event e
                 where e.lead_id = l.id
                   and e.event_type in ('outreach','outcome','status_change')) fr on true
 where fr.first_response_at is not null
   and l.created_at >= now() - interval '30 days';

-- §6.1  the un-captured WhatsApp stream
select count(distinct wa_phone)                                              as senders,
       count(distinct wa_phone) filter (where created_at > now() - interval '30 days') as senders_30d
  from order_intake.wa_event_log
 where direction='inbound' and type='message' and status='ignored_unknown_or_disabled';
```
