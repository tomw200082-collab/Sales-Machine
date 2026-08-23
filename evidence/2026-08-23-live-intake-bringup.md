# Evidence snapshot — live lead intake, deployed dark (2026-08-23)

> **Immutable. True as of 2026-08-23 only.** Never edit; supersede with a new dated
> snapshot. Authority: `system_verified` for everything measured against the live
> Supabase project `rvadsozabmxkkrktwgnv`, the live Shopify Admin API and GitHub
> Actions; `doc_confirmed` for the design decisions cited.
>
> Build: gt-factory-os PR #226, migration 0328, Edge Function `sales-leads-poll` v1.
> Design authority: production-brain
> `docs/superpowers/specs/2026-08-10-sales-leads-pipeline-design.md` §6, §7, §10.

## What this snapshot is, and what it is not

It records that the intake **shipped and is inert**, and the exact evidence for that.
It is **not** a bring-up snapshot: no lead has been fetched from Meta, no email has
been sent, and no mapping has been verified against a real lead. Those wait on two
secrets only Tom can create. A second snapshot follows bring-up.

## State verified before building (live SQL, 2026-08-23)

| Fact | Value |
|---|---|
| Leads / orgs in `sales_core` | 188 / 186 |
| Most recent lead | 2026-08-09 |
| Leads still `status='new'` | 188 (all of them) |
| Orgs with a `shopify_customer_id` | 0 |
| `sales-leads-poll` in the repo / deployed | absent / absent |

The masterprompt's state table (§2) was accurate in every row. Nothing surprised us,
so no `assumption_failure` was raised.

## What landed

**Migration 0328** — applied to production 2026-08-23, autonomous under the
2026-07-24 deploy authorization, announced one line before dispatch.

| Object | Purpose |
|---|---|
| `sales_core.poll_run` | one row per invocation. Makes *"did the poll run?"* answerable — the question nobody could answer between 2026-06-07 and 2026-08-09 |
| `sales_core.lead_reject` | malformed payloads kept with their raw body (§10: never a silent drop) |
| `sales_core.convert_lead()` | the **sole** writer of `status='won'`, from Shopify order evidence, open leads only (D4/D12) |
| `app_setting 'meta_poll'` | the poll cursor and its gate |
| cron 27 `sales_leads_poll` | `*/10 * * * *` |
| cron 28 `sales_leads_daily` | `0 4 * * *` |

**Edge Function `sales-leads-poll`** v1, ACTIVE, `verify_jwt=true`. Six routes:
`health`, `probe`, `poll`, `backfill`, `daily`, `ingest`.

## Deploy gates (all green before dispatch)

| Gate | Result |
|---|---|
| Pre-flight stock-truth check | **0 mismatches** — read-only reproduction of `rebuild_verifier()` incl. `balance_anchors` |
| CI | `typecheck` **success** on the PR head |
| Migration applies cleanly | applied twice locally on PG16 (cron/vault stubbed) — **idempotent** |
| Post-deploy health check | below |

## Post-deploy health check — the dark no-op, observed

Cron job 27 fired at **2026-08-23 11:20:00Z**. `cron.job_run_details`: `succeeded`.
`net._http_response` id 183583, **HTTP 200**:

```json
{"ok":true,"skipped":"missing META_PAGE_ACCESS_TOKEN — intake not yet live"}
```

This proves four things at once, none of them assumed:

1. the function is reachable and returns;
2. the cron's vault-resolved service-role JWT is **accepted** — a 401 would say otherwise,
   and `verify_jwt=true` means an anonymous caller who finds the URL gets one;
3. without its credentials the function is **inert with a stated reason**, not a
   crash loop;
4. nothing was written: `poll_run` is empty, `lead` is unchanged at 188.

## Test evidence

| Suite | Result |
|---|---|
| `node:test` — field mapping | **12/12** |
| `node:test` — alert + heartbeat | **18/18** |
| `node:test` — ingest flow (mocked Graph API + mocked Resend) | **13/13** |
| `node:test` — conversion decision | **6/6** |
| pgTAP `0328` | **22/22** |
| pgTAP regression `0318`–`0327` | **130/130** |
| `npm run typecheck` (root) | clean |
| `deno check` / `deno lint` | clean (except the repo-wide `npm:` import convention `shopify_available_reconcile` shares) |

The ingest-flow suite proves the five rules that can actually break: the cursor
advances only after a successful write; an overlapping window yields no second lead
and no second email; at most one alert per lead; a malformed payload is rejected *and*
logged without wedging the batch; a backfill emails nothing.

## Truth-rule compliance

- **No customer or lead was contacted.** The only recipient in the build is a
  constant (`tom@gteveryday.com`), re-checked at the send boundary.
  `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` remains `false`.
- **No factory-os core object was touched.** 0328 reads nothing from and writes
  nothing to `stock_ledger`, `balance_anchors`, `bom_*`, `items` or `components`.
  The conversion check asks **Shopify**, not our order tables — which is D3's
  reference-not-copy rule doing its job.
- **No volatile fact was written undated.** Every number above is stamped 2026-08-23.
- **Nothing was checked against a live system and then guessed anyway.** The two
  Shopify GraphQL operations were validated against the live schema and executed
  before being used in the function.

## Still open — Tom's two secrets

`META_PAGE_ACCESS_TOKEN` (Business Manager System User, `leads_retrieval`, never
expires) and `RESEND_API_KEY`, plus the generated `LEAD_INGEST_TOKEN`. Until they are
set in the Supabase dashboard the poll is inert **and** gated: `meta_poll.enabled` is
`false`, so a token alone cannot start writing leads through a field mapping nobody
has verified against a real lead (§2.3 is the cautionary tale). The gate is flipped
only after the `probe` route shows real field names — and the heartbeat treats
`enabled=false` as an **alarm**, so the gate cannot itself become a new silence.

**The clock stays real:** Meta retains leads 90 days. Leads submitted after
2026-08-09 exist only at Meta right now, and the earliest unseen ones fall off in
early September.
