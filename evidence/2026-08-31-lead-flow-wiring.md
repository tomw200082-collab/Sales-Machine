# Evidence — how a lead actually flows today, end to end

> Read live 2026-08-31 evening, read-only, ahead of tomorrow's session on connecting
> `054-758-8132` and designing the flow from first interaction to close.
> **Purpose: so tomorrow is decisions, not archaeology.**
> Authority: `system_verified` for every row and every file path below.

## 1. The open question from `recipes/coexistence-liveness.md` is answered — and it's good news

That recipe said, honestly, that it could not yet tell whether `wa_event_log` can
distinguish two numbers, and told the next session to **confirm rather than assume**.

Confirmed. The payload carries `phone_number_id`, and today there is exactly one value:

| `phone_number_id` | events | senders | first | last |
|---|---|---|---|---|
| `185509261301816` | 19,678 | 475 | 2026-06-26 | 2026-08-31 |

One number connected — the order line. When `054-758-8132` joins it arrives with its
**own** `phone_number_id`, so every downstream rule can route on it: order line to
reorders, lead line to `sales_core`. **No ambiguity, and nothing has to be retrofitted.**

## 2. Three ways a lead can arrive. Two land in `sales_core`. The biggest does not.

```
FIRST INTERACTION
├─ Facebook lead form → Make → sales-leads-poll (route=ingest) → sales_core.lead   LIVE
├─ Website form       → website_lead_intake (Edge, verify_jwt=false)               NEW — deployed today 12:28Z
└─ WhatsApp inbound   → Dualhook → POST /webhooks/wa-order-bot → order_intake.*    LIVE — 19,678 events
                                                                  │
                                                                  └─ ✗ never becomes a sales_core.lead
WORKING
├─ assignee              — 188 of 200 leads have none
├─ 06:00 digest by owner — deployed today; first real firing 2026-09-01 03:00Z
└─ reply from the phone  — lands back as an `echo` row (9,501 of them)

CLOSE
└─ sales_core.convert_lead() → converted_order_ref + converted_amount
```

**That is `U-025`, drawn.** The highest-volume inbound channel writes to a different
schema and never crosses into the lead pipeline. It is not a missing integration
between us and a vendor — it is a missing join between two of our own tables.

## 3. The receiving code already exists. Most of it is not switched on.

| Piece | Where | State |
|---|---|---|
| Thin Edge receiver — verify handshake, HMAC, forward | `supabase/functions/wa-order-bot/index.ts` (94 lines) | **in repo, NOT deployed** |
| The Node brain — normalise, dedupe, store, pipeline | `api/src/order-intake/` (worker 470 · store 221 · webhook 102 · route 101) | mounted on the API; **this is the live ingress** |
| Ingress path | `POST /webhooks/wa-order-bot` | live — Dualhook points straight at it (the route's own header says it may) |
| Health | `GET /webhooks/wa-order-bot/health` | returns flags + **names** of missing secrets, no values |
| Gates | `WHATSAPP_ORDER_INTAKE_ENABLED` · `WHATSAPP_AUTO_COMMIT_ENABLED` | in `config.js` |

∴ tomorrow is mostly **wiring and switching on**, not building. Start at
`/webhooks/wa-order-bot/health` — it names exactly what is missing without printing a
single secret.

## 4. What tomorrow has to decide

1. **Where the lead line's messages go.** Same `/webhooks/wa-order-bot` route split by
   `phone_number_id`, or a separate path. The route is the cheaper answer and the code
   already receives; the split is one branch.
2. **What counts as a lead.** Not every inbound message is one — the order line proves
   it, with 475 senders who are mostly existing customers reordering. A first message
   from an **unmapped** number on the **lead** line is the obvious candidate rule, but
   it is a rule someone has to choose, and getting it wrong either floods the queue or
   silently drops real leads.
3. **Which flags flip, and in what order.** `WHATSAPP_ORDER_INTAKE_ENABLED` before
   `WHATSAPP_AUTO_COMMIT_ENABLED`, and nothing customer-facing while
   `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` is `false`.
4. **What "close" means here.** `convert_lead()` writes the order ref and amount. For a
   WhatsApp-originated lead, what supplies them — a Shopify order, a Green Invoice
   document, or a human typing it.

## 5. Two things not to trip over

- **`sales-lead-fanout` is deployed with no source in any repo.** Whatever it does to a
  new lead, it is not reviewable from the repo. Understand it before adding a second
  producer upstream of it.
- **`website_lead_intake` was deployed today at 12:28Z by a parallel session**, public
  (`verify_jwt: false`). It is a third lead producer that this session did not build and
  has not read. Read it before designing around it.

## 6. Not done

Nothing was deployed, flipped, wired or written. No flag changed. No message sent.
Every statement above is a read.
