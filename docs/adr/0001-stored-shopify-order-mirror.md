---
status: accepted
---

# Store a mirror of Shopify orders

GT Pulse stores every Shopify order of an org (header and lines, classified, ex-VAT) and refreshes it daily, with an automated reconciliation against Shopify. Migration 0318 wrote "we never mirror" a Shopify customer, and every reader fetched live and kept nothing. Tom accepted the reversal on 2026-10-01 (B3).

**Considered options.** Live-only fetch with a cache: no new tables, but no event river, no unit C, no reconciliation, and the live readers are silently wrong (one reads `first:20` oldest-first, so a customer with more than 20 orders never converts; a throttled response reads as "not a customer").

**Consequences.** Shopify remains the source of truth; the mirror is a projection that can be rebuilt. Personal data is stored only for orgs that exist (verified or in review). Money and history are shown only while the latest reconciliation passes.
