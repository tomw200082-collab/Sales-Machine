# Evidence snapshot — 19 hours of dead intake, three leads recovered (2026-08-28)

> **Immutable. True as of 2026-08-28 07:20Z only.** Never edit; supersede with a new
> dated snapshot. Authority: `system_verified` for everything measured against the live
> Supabase project `rvadsozabmxkkrktwgnv`, the live Make account (team 1240098) and
> GitHub; `user_confirmed` for Tom's approvals.
>
> Full engineering post-mortem: `gt-factory-os-production-brain/docs/lessons_learned.md`
> § 2026-08-28. Open items: GAP-032, GAP-033.

## What happened

Tom rotated the Postgres password in the Supabase dashboard around **2026-08-27 12:00Z**.
Every service that reaches the database through the hand-maintained
`DATABASE_URL_POOLED` secret failed from **12:05Z** with
`password authentication failed for user "postgres"`. That set includes
`sales-leads-poll` — the sole write path of the lead intake.

Recovery landed **2026-08-28 07:05Z**. Nineteen hours.

## What it cost the sales pipeline

**Three Facebook leads reached Make and could not be written.** The Make scenario
`GT Sales — lead intake → /ingest` (id 7075235) ran three times inside the window and
`sales_core.lead` gained nothing:

| Make execution | Lead | Business | Ad |
|---|---|---|---|
| 2026-08-27 15:40:23Z | tamer | mood | `Matcha Tut` |
| 2026-08-27 18:05:43Z | אלדר נפתלייב | עגלת נוב | `Matcha Tut` |
| 2026-08-28 04:08:01Z | Elinor Ifergan | — | `Matcha Tut` |

All three are `status='new'`, all carry a phone, all from campaign `MACHA Leads`.
Longest wait before a human could see it: **15 hours** (tamer).

`order_intake.wa_event_log` also stopped at 2026-08-27 11:57:19Z for the duration.

## Why nothing was lost

Two decisions made earlier — neither aimed at this — saved the leads:

1. The Make scenario carries a **`Break` module**, which parks a failed run in the
   dead-letter queue instead of dropping it. `dlqCount` stood at 5 when the outage was
   found.
2. `sales_core.lead` carries **`UNIQUE (source, external_id)`**, so replaying the whole
   DLQ was safe — an already-stored lead simply does not enter twice.

Tom retried all five DLQ items at ~07:15Z. The three missing leads landed with their
**original timestamps preserved** — 15:40:17Z, 18:05:38Z, 04:07:57Z — not rewritten to
the replay time. Nothing was duplicated.

## The alerts did go to all three people

Three `alert_sent` events fired at 07:15:43–47Z. `sales-leads-poll` is still **v12**, so
its own alert addressed `tom@gteveryday.com` alone; the bridge Edge Function
`sales-lead-fanout` carried the other two. All three fan-out calls returned HTTP 200
with a Resend message id:

```
07:15:43  200  to: [alex.berov@gmail.com, avi@gteveryday.com]  id 0678cc3d…
07:15:44  200  to: [alex.berov@gmail.com, avi@gteveryday.com]  id 61f26e38…
07:15:47  200  to: [alex.berov@gmail.com, avi@gteveryday.com]  id 8452aa16…
```

That is delivery **to the provider**, not proof of inbox. It is also still the bridge,
not the merged path: gt-factory-os#240 has been merged since 2026-08-25 and has never
been deployed, because GitHub Actions on that repo had no runner from 2026-08-24 20:44
until 2026-08-27. Actions is restored, so the deploy is no longer blocked (GAP-032).

## What this says about the intake, beyond this incident

The 2026-06-07 failure hid for two months. This one was found the same afternoon,
because the daily heartbeat exists. But the heartbeat watches **intake**, not the
**fan-out**: `fn_lead_alert_fanout` ends in `exception when others then return null`
and `pg_net` is fire-and-forget, so if the bridge to Alex and Avi breaks, nothing
alarms and nothing records it. `net._http_response` retains roughly six hours, which is
shorter than a weekend.

The 24-hour loudness property that D-006 relies on covers the pipe, not the last mile.

## One further lead fact worth carrying

**Elinor Ifergan is a returning lead** — she also came in on 2026-05-29. Same person,
three months apart, both still `new`. Not a churn signal; a follow-up that never
happened.

## Unresolved, opened by this snapshot

| ID | Question |
|---|---|
| U-014 | The fan-out to Alex and Avi has no alarm and no durable record. Should a failed fan-out write a `lead_event`, so the heartbeat can see it? |
| U-015 | Three leads waited 15h / 13h / 3h before any human could see them. Does the 24-hour KPI (D-006 §1.1.6) start at form submission or at first human visibility? They are not the same clock, and this outage put 15 hours between them. |
