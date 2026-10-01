---
status: accepted
---

# One writer for the Shopify link; identity is retired, never deleted

Only `sales_core.link_org_shopify` may set an org's `shopify_customer_id` and `shopify_link_status`. Lead ingest, the daily backfill and the customer-setup step record what they found as evidence and no longer write the link. An id the identity layer did not set starts as `review` until the B4 rule derives it again. A guard trigger enforces this in the database.

Orgs, events and evidence are append-only history, so an identity change is undone by retiring (`retired`, with an `identity_reverted` event), never by deleting. Rolling back a backfill deletes only mirror rows by run id.

**Why.** Four writers took "the first hit" of a Shopify search with no uniqueness check, and several readers treated any non-null id as a proven customer. Once B creates orgs at scale that would show another business's history to a rep. **Considered:** keep the writers and add a check to each; rejected because the next writer would bypass it.

**Consequences.** `ingest_lead` and `sales-leads-poll` change (Tom, T3). The radar and lead conversion require `verified`.
