# Evidence — the systems under the WhatsApp lead journey, as measured 2026-09-28

> Read live on 2026-09-28 (about 15:00 UTC), read-only, while the journey was designed with Tom.
> **True as of that moment only** — re-run the queries in §6 before building on any number.
> Authority: `system_verified` for every row read from Supabase `rvadsozabmxkkrktwgnv` or from code;
> `doc_confirmed` where the row cites the 2026-09-24 customer-portal measurements.
> The decisions built on it: D-027…D-032. The journey: `doctrine/playbooks/whatsapp-lead-journey.md`.

## 1. The lead line has never delivered a message to GT's webhook

| `phone_number_id` | line | events, last 30 days | of which messages | last event |
|---|---|---|---|---|
| `185509261301816` | order line | 6,441 | 3,488 | 2026-09-28 14:45 UTC |
| `217553368116155` | lead line `054-758-8132` | **0** | **0** | never |

- The lead line was provisioned on 2026-09-02 (`gt-factory-os-production-brain`
  `docs/decisions/2026-08-31-lead-intake-architecture.md` A3). It has carried **0 events ever**;
  the acceptance test written there ("the first non-zero count proves the whole chain") has not
  been met.
- **GT's code does not drop it.** `api/src/order-intake/route.ts` filters only by WABA id, and
  only when no app secret is set; the lead line is on the same WABA. `api/src/order-intake/worker.ts`
  logs every event that has a message id to `order_intake.wa_event_log` before routing it; the lead
  branch is the front gate in `handleMessage`.
- ∴ either nobody has written to the number, or the provider does not forward it, or coexistence
  lapsed (the 13-day rule, D-023). One WhatsApp message to `054-758-8132` tells which. **This is
  the journey's first blocker** (U-050).

## 2. Sending works, and buttons have worked before

- The order line sends today: `portal_register_link_sent` 5 times (last 2026-09-28 09:02 UTC)
  and `portal_login_link_sent` 9 times (last 2026-09-26 12:37 UTC) in `wa_event_log`.
- Reply-button taps have reached the pipeline: 17 inbound `interactive` messages, the last on
  2026-07-12.
- The send port (`api/src/order-intake/whatsapp/send.ts`) posts text and up-to-three reply buttons
  to the Cloud-API endpoint the provider exposes. Each port instance is bound to one
  `phone_number_id`; the live one is the order line's.

## 3. The ordering portal is live

- `private_core.feature_flags` `customer_portal_live` = enabled, allowlist `*`, since
  2026-09-25 15:21 UTC.
- Every portal order today is a real Shopify order (draft → complete, tag `portal`), under ₪800
  ex-VAT cannot be sent, prices shown are the customer's own or the list price
  (`gt-factory-os` `docs/superpowers/specs/2026-09-24-customer-portal-design.md` §4.1–§4.3).
- **A completed Shopify order is invoiced automatically**: Green Invoice issues a type-305 tax
  invoice 5–11 s after the order is created (50 of the 50 latest orders), and every created order
  opens a LionWheel delivery task, paid or not (same spec, §2 W0-2 and W0-3, measured 2026-09-24,
  `doc_confirmed` here). The integration that issues the invoice is unidentified. A draft order
  triggers neither — the basis of D-029.

## 4. The CRM already carries every hook the journey needs

`sales_core.lead` columns include `status`, `assignee`, `next_touch_at`, `first_touch_at`,
`converted_order_ref`, `converted_amount`, `converted_order_placed_at`.

| `lead.status` | leads |
|---|---|
| new | 145 |
| lost | 61 |
| working | 30 |
| won | 5 |

| `lead_event.event_type` | events | last |
|---|---|---|
| reminder_sent | 519 | 2026-09-28 |
| created | 241 | 2026-09-27 |
| status_change | 102 | 2026-09-28 |
| alert_sent | 54 | 2026-09-27 |
| next_touch_set | 49 | 2026-09-28 |
| note | 37 | 2026-09-28 |
| assignment | 34 | 2026-09-28 |
| outreach | 33 | 2026-09-28 |
| matched_existing_customer | 19 | 2026-09-24 |
| outcome | 13 | 2026-09-28 |
| converted | 5 | 2026-09-26 |

- `outcome` events carry `result` ∈ {`answered_progressing`, `no_answer`, `whatsapp_sent`} and a
  `next_touch_at`; follow-ups are stored at 06:00 UTC (09:00 in Israel's summer time). `answered_progressing` is the
  "we spoke, it is moving" mark that starts the wake-up sequence (D-031).
- `outreach` events carry `channel` = `whatsapp` (29) or `call` (4).
- No opt-out column or event type exists yet (U-049).

## 5. What the lead can already read

- The site's FAQ (`gt-site` `src/index.html`, `id="faq"`) holds six questions: הבקבוקים צריכים
  קירור? · כמה משקאות יוצאים מבקבוק אחד? · מה בעצם יש בפנים? · כמה זה מסובך לצוות? · יש אפשרויות
  בלי סוכר? · איפה מתחילים?
- `knowledge/answers/answer-bank.yaml` holds 31 answers, each `מאושר`, `טיוטה` or `העברה`. Only
  `מאושר` rows may be sent or published; D-018 rows are transfers.

## 6. Recipes (re-run before relying on any number above)

```sql
-- §1 events per receiving number, last 30 days
select raw_payload->>'phone_number_id' as pnid, count(*) as events,
       count(*) filter (where type='message') as msgs, max(created_at) as last_event
from order_intake.wa_event_log where created_at > now() - interval '30 days'
group by 1 order by 2 desc;

-- §2 outcomes the pipeline recorded, last 10 days
select split_part(status, ':', 1) as outcome, count(*) as n, max(created_at) as last_at
from order_intake.wa_event_log
where created_at > now() - interval '10 days' and status is not null
group by 1 order by 3 desc;

-- §3 the portal flag
select flag_key, enabled, value, updated_at from private_core.feature_flags
where flag_key = 'customer_portal_live';

-- §4 CRM events and outcomes
select event_type, count(*) as n, max(created_at) as last_at
from sales_core.lead_event group by 1 order by 2 desc;
select payload->>'result' as result, count(*) from sales_core.lead_event
where event_type = 'outcome' group by 1;
```
