# Recipe — what breaks in the lead intake, and how you find out

> **Method, not a fact.** Every number below is fetched live; nothing here is a
> stored count. Verified against the live path on 2026-08-24. Authority:
> `system_verified` for each query and each observed run.
>
> Read with: `doctrine/decisions.md` D-006 (Make carries the leads),
> `evidence/2026-08-24-make-intake-handover.md` (why), and
> `gt-factory-os/supabase/functions/sales-leads-poll/` (the code).

## The path, in one line

```
Facebook form → Make scenario "GT Sales — lead intake" (instant, hook 3598876)
  → POST /functions/v1/sales-leads-poll  route=ingest
  → normalise · match org · dedupe · store · alert Tom · portal link
```

Everything except transport lives in the Edge Function. Make holds no data and
makes no decisions. A second Make scenario, **"GT Sales — hourly pulse"**, exists
only to prove the Facebook connection is still alive.

## The five ways it breaks

| # | Failure | What it looks like from inside | How you find out | Time to notice |
|---|---|---|---|---|
| 1 | **Make's Facebook connection expires** (the 2026-06-07 failure) | leads simply stop; indistinguishable from a quiet week | the hourly pulse stops, because the pulse module *calls Facebook*. The daily heartbeat alarms when the last pulse is over 24h old | ≤ 24h |
| 2 | **Make scenario switched off / out of operations** | same silence | same pulse gap | ≤ 24h |
| 3 | **Meta stops delivering the webhook** (page subscription lost) | the pulse is still green — it reads the form, it does not receive pushes — but no lead arrives | pulse green + zero leads for longer than the quiet-day threshold; and the reconciliation query below | needs the query |
| 4 | **A lead arrives in a shape the mapper does not know** | one lead missing, everything else fine | a row in `sales_core.lead_reject` with the full raw body, and a non-`ok` `poll_run` | immediate, on query |
| 5 | **The alert email fails** | the lead is stored, Tom never hears | the lead carries no `alert_sent` event; the poll's sweep retries it | next sweep |

Failure 3 is the one the pulse alone cannot catch, because the pulse proves the
connection, not the subscription. That is what the reconciliation query is for.

## The queries

### Is the pulse alive?

```sql
select max(finished_at) as last_pulse_at,
       now() - max(finished_at) as age
  from sales_core.poll_run
 where route = 'ingest' and ok and summary->>'pulse' = 'true';
```

Older than ~2h means Make stopped running it. Older than 24h is what the daily
heartbeat alarms on.

### Did anything get rejected?

```sql
select created_at, source, reason, raw
  from sales_core.lead_reject
 order by created_at desc
 limit 20;
```

`raw` holds the exact body that was refused, so a form change is recoverable
rather than lost. Never delete rows here.

### Reconciliation — the check the pulse cannot do

Compares what Meta holds against what we hold. Run it when the pulse is green
and the queue still feels too quiet.

1. In Make, run the scenario **"GT Sales — hourly pulse"**'s Facebook module
   against the live form, or use `listLeads` on form `1165807205227331`.
2. Take the newest `leadgenId` and `dateCreated`.
3. Compare:

```sql
select external_id, created_at
  from sales_core.lead
 where source = 'facebook'
 order by created_at desc
 limit 5;
```

A `leadgenId` present in Meta and absent here means the webhook is not being
delivered — failure 3. The fix is to delete and recreate the Make hook so Make
re-subscribes the page.

### Is exactly one email going out per lead?

```sql
select l.id, count(e.id) as alerts
  from sales_core.lead l
  left join sales_core.lead_event e
    on e.lead_id = l.id and e.event_type = 'alert_sent'
 where l.created_at > now() - interval '7 days'
 group by l.id
having count(e.id) <> 1;
```

Empty is correct. Two rows would mean a duplicate email; zero means the alert
never went and the sweep has not caught up.

### Is the conversion loop able to fire at all?

```sql
select count(*) filter (where shopify_customer_id is not null) as matched,
       count(*)                                                as orgs
  from sales_core.org;
```

`matched = 0` means the loop is dead no matter how healthy everything else looks
— that was the state until the 0330 backfill on 2026-08-24.

## The heartbeat

Cron job 28, `0 4 * * *` UTC, calls `route=daily`. It does two things: the
conversion sweep, then the heartbeat email. Under `intake_mode = 'make'` it
judges the Make path and the pulse, not the (permanently disabled) poll — an
alarm that is always red is worse than no alarm, because it buries the real one.

Severity is decided in `_lib/email.ts`; the run is recorded in
`sales_core.poll_run` with `route = 'daily'`, so a heartbeat that failed to send
is itself visible:

```sql
select started_at, ok, summary, error
  from sales_core.poll_run
 where route = 'daily'
 order by started_at desc
 limit 7;
```

## Adjacent, and deliberately out of this lane

Two failures live next door and are **not** part of the sales intake. They are
named here so they are not mistaken for it:

- **`lionwheel_poll`** fails intermittently with
  `date/time field value out of range: "23/08/2026 14:36"` — a DD/MM date parsed
  as MM/DD, so it only fires when the day of month is greater than 12. A real
  bug, unfixed, in the LionWheel lane.
- **`dispatch-alerts-cron`** has been failing every run for days, with durations
  that predate the 2026-08-23 GitHub Actions outage. Separate root cause,
  uninvestigated.

Neither touches `sales_core`.

---
_Method verified 2026-08-24. Re-verify the queries, not this page._
