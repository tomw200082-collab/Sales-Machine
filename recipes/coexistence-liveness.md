# Recipe — proving the WhatsApp coexistence link is still alive

> **Method, not a fact.** Every number below is fetched live; nothing here is a
> stored count. Verified against the live order line on 2026-08-31. Authority:
> `system_verified` for each query, `inferred` for the threshold until one lapse
> has actually been observed.
>
> Read with: `doctrine/decisions.md` D-014 (`054-758-8132` is the lead number) and
> D-015 (it joins the API by coexistence), `doctrine/playbooks/whatsapp-setup-kit.md`,
> and `CURRENT_STATE.md` U-031.

## Why this recipe exists

Coexistence lets one number live in the WhatsApp phone app **and** on the Cloud API
at the same time. It has one condition: **the app must be opened at least once every
13 days and never uninstalled.** Miss that and the link lapses.

**The lapse is silent.** No alert, no error, no red row. Messages keep arriving on
the phone, so nothing looks wrong to the person holding it — while the API stops
seeing them.

That is the same failure shape GT has already paid for three times:

| What | How long it was silent | What hid it |
|---|---|---|
| Make's Facebook OAuth token | **two months** | nothing watched the token, only the leads |
| The 06:00 lead digest | six days | `net.http_post` never learns the response; no row = no red row |
| The LionWheel pick bridge | until someone looked | merged is not deployed, and nothing compared them |

Every one was invisible because **the absence of a signal looked exactly like a quiet
period.** The fix is never "remember to check" — it is a signal that has to keep
arriving, so its absence is itself the alarm.

With D-014, **every lead automation sits on one number.** A silent lapse there stops
the entire intake.

## What proves the link is alive

`order_intake.wa_event_log` receives a row for every message the Cloud API sees on a
coexisting number — including `echo` rows, which are replies a human typed **in the
phone app**. An `echo` is therefore proof of both halves at once: the app is in use,
and the API can see it.

Baseline read on the order line `054-398-2444`, 2026-08-31:

| | |
|---|---|
| rows since 2026-06-26 | 24,162, unbroken |
| newest row | minutes old |
| distinct phones | 476 |
| `inbound`/`message` | 10,168 |
| `inbound`/`echo` | **9,501** |

## The query

```sql
-- Liveness. Run per coexisting number once its own rows are distinguishable.
select
  max(created_at)                       as last_event,
  (now() - max(created_at))::interval(0) as silence,
  count(*) filter (where created_at > now() - interval '13 days') as rows_13d,
  count(*) filter (where type='echo' and created_at > now() - interval '13 days') as echo_13d
from order_intake.wa_event_log;
```

## Thresholds

| Silence | Reading | Action |
|---|---|---|
| < 48h | healthy | heartbeat line only |
| 48h – 7d | **suspicious** | raise in the daily heartbeat by name |
| > 7d | **treat as lapsed** | alarm, and Tom opens the app that day |
| `echo_13d = 0` | **the specific danger** | the app has not been used to reply in 13 days — the exact precondition for lapse |

7 days, not 13, on purpose: the alarm has to fire while there is still time to act.
An alarm on day 13 announces the lapse instead of preventing it.

⚠️ `echo_13d = 0` is the sharper signal and the one worth watching. Total row count
can stay healthy on inbound traffic alone while nobody opens the app at all.

## Where this gets implemented — and where it does not

**Not here.** This repo holds no runtime code, ever (`CLAUDE.md`).

**Extend the daily heartbeat that already exists** — `sales-leads-poll`, route
`daily`, D11 — rather than adding a second mechanism. It already runs daily, already
emails Tom, already computes a severity. It needs one more line and one more severity
input. A separate monitor would be a second thing that can itself go quiet, which is
the failure this recipe is about.

Owner: **Tom** (D-014, his number, his phone). The automated check is not a
replacement for the owner — it is what makes the owner's absence visible.

## The honest limits

- **The threshold is `inferred`.** No lapse has been observed on GT's own numbers;
  13 days is the platform's published condition, and 7 is a margin chosen to leave
  room to act. Revisit once a real lapse or near-miss exists.
- **This recipe cannot yet split by number.** The baseline above is the order line;
  once `054-758-8132` is connected, confirm `wa_phone` (or the payload) actually
  distinguishes the two lines before trusting a per-number reading. **Do not assume
  it does.**
- **A healthy row count is not a healthy link.** Only `echo` proves the app side.
