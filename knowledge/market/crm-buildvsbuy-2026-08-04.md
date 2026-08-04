# Knowledge — CRM: build vs. adopt (2026-08-04)

> Authority: `doc_confirmed` (candidates: repo + license + docs read directly) +
> `system_verified` (GT-side claims verified in this workspace).
> Freshness: `review_30d` — OSS licensing and RTL status move.
> Decision it fed: **D-012 — build in-house.**

## Verdict

Build in-house. Not a default preference — three GT-specific facts drive it.

## Why

1. **The hardest part is already built.** `gt-factory-os/supabase/functions/wa-order-bot/index.ts` is a live Meta
   webhook receiver (verify-token, `X-Hub-Signature-256`, fast ACK, worker forward). `api/src/order-intake/`
   carries webhook, worker, tests, idempotent dedupe. **Facebook Lead Ads and Instagram ride the same Meta app
   and the same signature scheme.** No candidate saves this work — each requires it identically.
2. **RTL is where every candidate fails and GT is already solved.** `dir="rtl"` appears 13× across 10 files in
   `gt-factory-os-portal/src` with documented a11y reasoning. House pattern exists.
3. **Shopify order history is near-free here, DIY everywhere else.** The integration and `integration_sku_map`
   are already owned; a curated read model is cheap.
4. **The reminder scheduler already runs.** pg_cron is in production (the `*/5` reconciler).

## Candidates evaluated

| Candidate | Stack / License | Killer fact |
|---|---|---|
| **Twenty** (54K★) | TS · NestJS · Postgres · AGPL+EE | Best stack fit. **Zero RTL** — 312 physical `margin/padding-left\|right` vs 29 logical; `dir` never wired to locale. Hebrew words in an LTR layout. |
| **Chatwoot** (35K★) | Rails · Postgres · MIT core | **Wins the inbox half outright** — native Hebrew RTL, native WhatsApp/IG/FB, native Shopify sidebar. But a support desk: no pipeline, no lead entity, no due-dated tasks. |
| **EspoCRM** | PHP · MySQL · AGPL | Workflows + reports are the **Advanced Pack, $395/yr**. The paywall lands exactly on the two requirements. |
| **Frappe CRM** | Vue · MariaDB · AGPL | Best native routing (round-robin + by workload). **RTL broken and tracked — issue #1618, UI stays LTR.** |
| **Krayin** (23K★) | PHP · MySQL · MIT | Cleanest license here; wrong runtime. RTL layout quality unverified. |
| **Atomic CRM** | React · Supabase · MIT | Perfect stack match, but marmelab call it a reference implementation, not a maintained product. No routing, no multi-channel inbox. **Value = code reference, not product.** |
| NocoDB | — | **Left open source** (source-available license from v0.301.0). |
| Erxes | AGPL + hand-written non-compete | Not OSI-permissive. |
| SuiteCRM · Odoo · Vtiger · Baserow · Teable · Monica | — | Rejected on weight, open-core paywalls, or wrong shape. |

## Honest cost of building

**3–5 weeks focused engineering.** Schema 2–3d · ingest 1–1.5w (FB/IG is the real work) · routing + SLA 3–5d ·
UI 1–1.5w.

**What GT does not get:** email sync, calendar, duplicate detection/merge, mobile app, import/export, saved
views, full-text search. Twenty ships all of it free today. **If the team turns out to want a full CRM rather
than a lead-response tool, this calculus flips.**

## Fallback if kept

**Chatwoot for channel ingestion + a thin CRM layer on GT's stack against its API.** Cost: a Rails app with its
own Postgres and user model to operate, and it partly duplicates the WhatsApp receiver GT already owns.

## Calendar risk — applies to every path

Meta app review for `leads_retrieval` and Instagram messaging permissions is **waiting time, not dev time.**
Open it first regardless of the decision.

## Unverified (do not rely on)

- EspoCRM: whether Lead Capture round-robin sits in free core (docs page 404'd); Hebrew `he_IL` community pack currency.
- Krayin: RTL *layout* quality (Arabic language files confirmed; mirrored layout not confirmed).
- Atomic CRM: RTL status — no documentation either way.
