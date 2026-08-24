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

## Adjacent — checked, and NOT broken

The 2026-08-24 masterprompt lists two neighbouring failures as live. Both were
verified against the live system today and **neither is failing any more**. They
are recorded here so nobody re-opens them from a stale note:

| Was reported as | Live state on 2026-08-24 | Why |
|---|---|---|
| `lionwheel_poll` failing intermittently on `date/time field value out of range: "23/08/2026 14:36"` | cron `lionwheel_poll` (`*/15`): **192 runs in 48h, 0 failures** | Fixed by gt-factory-os #230. LionWheel switched from ISO-8601 to `DD/MM/YYYY HH:MM`; `normalizeLwTimestamp` now handles both, with regression cover in `api/test/lionwheel_timestamp_normalisation.test.ts`. Today is the 24th — a day-of-month above 12 — so the old bug would be firing right now if it were still there. |
| `dispatch-alerts-cron` failing every run for days | cron `dispatch_alerts` (`*/5`): **576 runs in 48h, 0 failures** | The failing GitHub Actions workflow was deleted by #229 ("stop the scheduled runs that starved this repo of Actions minutes"). The work itself runs as a Supabase cron job, and that job is green. |

Verify before believing either row:

```sql
select j.jobname, j.schedule, j.active,
       count(*) filter (where d.start_time > now() - interval '48 hours')                        as runs_48h,
       count(*) filter (where d.status='failed' and d.start_time > now() - interval '48 hours')  as failed_48h
  from cron.job j
  left join cron.job_run_details d on d.jobid = j.jobid
 group by 1,2,3
 order by failed_48h desc;
```

Neither touches `sales_core`.

---
_Method verified 2026-08-24. Re-verify the queries, not this page._
