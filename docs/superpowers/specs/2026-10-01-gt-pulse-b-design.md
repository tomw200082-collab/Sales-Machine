# GT Pulse Unit B — one verified business, its people and its full order history

**Date:** 2026-10-01 · **Version:** v2 · **Status:** approved by Tom on 2026-10-01 (§1).

**Parents:** program spec `2026-09-29-gt-pulse-crm-program-design.md` (§4 row B, §5, §7, §8, §9), closure spec `2026-10-01-gt-pulse-a-preprod-closure-design.md` (§2 glossary, D1–D17), the D1 visual spec, and the work order `docs/plans/2026-10-01-gt-pulse-b-masterprompt.md` (definition of done D1–D12). Terms: `CONTEXT.md`. Decisions that are hard to reverse: `docs/adr/`.

**Rule for this document.** Business, commercial and product-policy decisions are Tom's. Every decision in §2 is quoted from him with its date. Where a decision is missing the work stops with a recommendation and its main alternative. §3 is engineering that implements those decisions.

**How v2 came about.** v1 was attacked by six independent reviewers (business, identity, architecture and Shopify, security, verification, UX). All six advised against approving v1. Their engineering fixes are folded into §3; the choices that were Tom's he made as T1–T12 (§2.2). v1 is in the history of PR #39 and is superseded.

## 1. Approval

Tom, 2026-10-01: **"מאשר הכל"** — in reply to the red-team summary that listed T1–T12 and this sequence: spec v2, then a build plan, then an autonomous backend build; the Hebrew UI starts only after he approves mockups and string round 1.

Approved: T1–T12 as recommended, and that sequence. v2 was written after that approval and adds no business decision; the operational defaults it sets are listed in §2.3 so he can change them.

Not covered, still his (§2.4): the backfill go on exact counts and digest (E), the Hebrew copy batch (C), the visual approval (D), the optional real-device check (F), and his own security actions.

## 2. Decisions

### 2.1 Settled before the review — Tom, 2026-10-01

| # | Decision | Notes |
|---|---|---|
| A1 | Land only migrations `0353`, `0354` and their pgTAP files on `main`, byte-identical to PR #283. | Done: PR #333, `main` `a78a849`. Production applied them on 2026-09-24. Never in a `deploy-production.yml` migrations glob. |
| A2 | B's order history is **Shopify only**, every screen labelled "source: Shopify". A second source (Green Invoice documents) is out of B. | Corrected: v1 tied this to the `distributor`-tagged customer. That customer is a distributor GT still serves (chain map `kind: מפיץ`), not Ice Dream; no Ice Dream customer exists in Shopify. How orders of customers moved to Ice Dream will appear in Shopify is an open fact (§2.4), and it affects what "active" and money mean (T5). |
| B1 | **Verified B2B customer** = a Shopify customer with (1) at least one clean order in all history and (2) `custom.client_key`. **Active** = a clean order in the last 12 months, a label and not a condition. | Refined by T1. A **clean order** is not a test, not cancelled and not a draft; a refunded order is still clean (I3). |
| B2 | **Org = one Shopify customer (a branch).** A chain is the parent. Tags and `client_type` are evidence only. | Refined by T6. |
| B3 | **Stored mirror** of Shopify orders, idempotent, refreshed, with an automated reconciliation. | ADR 0001. Reverses the 0318 header "we never mirror it". |
| B4 | Link an existing lead-born org to a Shopify customer only on an exact match that points to exactly **one** customer; anything else is *disputed* and goes to a manager. No domain tier, no name similarity. | Refined by T3 and T4. |
| B5 | A contact is a named person with a channel at the buying business; verified = a person confirmed it, or that phone placed an approved order for the org. LionWheel recipients and on-site contacts never become contacts automatically. | Refined by T10. |
| B6 | An existing customer without a lead has no owner until Tom assigns owners once, in bulk. | Corrected: v1 said all 263 leads share one assignee. Measured: 44 leads are assigned, all to one person; 219 are unassigned; no `sales_rep` account exists. Refined by T9. |
| B7 | **Money is visible to everyone with sales access** — "ב-6 אין בעיה שכולם ייראו כסף כרגע — זה בסדר גמור ורצוי אפילו." | Time-bound by T11 (I1). |
| R | After the reconciliation passes, the sleeping radar and the lead-conversion evidence read the mirror; the order bot and portal pricing stay live. | Timing refined in §3.11. |

### 2.2 Settled after the review — Tom, 2026-10-01 ("מאשר הכל" on T1–T12)

| # | Decision | What it means in the build |
|---|---|---|
| T1 | A customer with a clean order and **no `client_key`** is not an org and gets no task. Active customers without `client_key` (about 9) and customers carrying `needs-verification` or `whatsapp-bot-test` go to review. Tom can promote a customer by hand. `client_key` counts only when non-blank after trim. | About 2,100–2,450 customers (mostly 2020–2023 single-order buyers) stay out. The dry-run counts them (`excluded_no_client_key`, split by order recency) and lists them read-only. Orders are mirrored only for customers that become orgs. |
| T2 | **Gate 4 wins over "Unit A does not change".** | Every view and column that derives from the mirror, and `is_existing_customer` and `returning_customer`, is non-null only when the link status is `verified`. Measured: of the 17 existing links, 8 meet B1 and 9 do not (7 point at customers with no orders); 8 Today "returning customer" cards sit on those orgs and lose the signal. The dry-run reports Today card changes in both directions. |
| T3 | B may change `ingest_lead`, `sales-leads-poll` and the customer-setup step that write `shopify_customer_id`: they record **evidence only**. | One function, `link_org_shopify`, is the only writer. An id the identity layer did not set starts as `review` until B4 re-derives it. The radar and `convert_lead` require `verified`. |
| T4 | B4 matches on **phone only**; the email tier is dropped. | Shopify B2B customers carry no phone or email on the record; phones sit on addresses and emails are placeholders. The mirror keeps every customer phone (default and addresses), normalised. A phone found on two or more customers, or on a branch of a chain with two or more branches, makes the link disputed. |
| T5 | How an Ice Dream customer's order appears in Shopify is Tom's open fact. Until he decides: no "days since last order" is counted as silence for orgs whose chain is `moved_to_distributor` or served by Ice Dream, and money carries the label "order value (Shopify, customer price)". | The Hebrew wording goes through the string batch. |
| T6 | `chain_map.json` remains the chain authority. | `sales_core.chain` keeps every field of the file (kind, status, moved_to, moved_on, group, exclude, serves, roster_badge, single_record_note) with the file's SHA; memberships are explicit per customer and approved with the dry-run; a daily check compares the seeded SHA with the file; a new rule hit goes to review instead of attaching; `branch_merge` is a display-only group. `client_key` means a Green Invoice client link (code-verified); this is recorded in the decision log. |
| T7 | A local PostgreSQL 16 for the test inner loop. | Used with `env -i`; CI on PG17 stays the authority. |
| T8 | **Coverage** = verified active customers ÷ active customers in the Shopify census (ShopifyQL customers with a clean order in 12 months), shown to managers with its source and time. | Measured today: 589 ÷ 595. |
| T9 | The org list defaults to active customers plus orgs with an open lead. One bulk owner-assignment action; no per-org owner screen until the first `sales_rep` exists. | Unowned orgs create no tasks. |
| T10 | Contacts are a **list** in B; the radial compass is deferred. Extra inputs: `customer_book.contact_*` only where `field_sources` is not `lionwheel`, approved portal access rows, and a staff-mapped ordering number as an org channel even without a name. | |
| T11 | Security: rotate the Shopify token; deactivate the demo admin; confirm whether the gmail planner is staff; B7 is time-bound. | The first three are Tom's own actions (§2.4). B7 is revisited before any `sales_rep` or non-GT user gets sales access. |
| T12 | A question for counsel on contact data under Israeli privacy law. | Not blocking; B ships a redaction path and an access record (§3.9). |

### 2.3 Operational defaults this spec sets (safety, not policy; Tom may change)

A refresh run that would create more than 10 orgs, 10 links or 20 contacts stops its identity step and raises an exception; mirror rows still update. Data older than 36 hours shows a banner. The daily refresh runs at `40 0 * * *` UTC. The reconciliation sample is stratified (§3.5).

### 2.4 Still needs Tom — none of it blocks the build

E the backfill go on exact counts and digest. C one batch of Hebrew strings (about 140–180) with the mockups. D mockups first, then before/after and a short video before merge. F optional real-device check. T11 actions: rotate the Shopify token, deactivate the demo admin, confirm the gmail planner. A read-only Shopify token for the mirror (preferred; the existing token is the fallback). The open Ice Dream fact (T5). T12 counsel.

### 2.5 Interpretations

- **I1 (B7).** "Everyone" is every user `roleAllowsSales` allows. Row scope stays: a rep reads only own orgs (masterprompt D7). Gate 4 stays. Revisit before a `sales_rep` or non-GT user gets access.
- **I2 (B2, T6).** The chain map matches by name substring after whitespace and punctuation are collapsed, `exclude` wins, and a customer matching two chains is left unassigned. "No similarity" means no matching beyond those rules.
- **I3 (B1).** Class precedence: draft, test, cancelled, refunded, completed. A cancelled order never counts as refunded. A completed ₪0 order counts as clean; the dry-run reports customers verified only by ₪0 orders.
- **I4 (T9).** Orgs without a lead and without a link are not listed by default.
- **I5.** The mirror refreshes once a day; there is no manual refresh in B.

## 3. Engineering design

### 3.1 Shape

```
Shopify bulk operations (orders, customers) and updated_at queries — one Node client, pinned API version
   │
   ▼  Railway job → 202 + run id; heartbeat lease in mirror_run
sales_core.mirror_stage_*   (parsed rows, per run)
   │
   ├─ dry-run:  mirror_promote(run, commit := false)   — the full apply in a subtransaction, rolled back; returns the report and digest
   └─ apply:    mirror_promote(run, commit := true, expected_count, expected_digest, approver)   — SQL function, run by an authorised person
        ▼
   shopify_customer / shopify_customer_phone / shopify_order / shopify_order_line
   identity layer → org (link status) · org_identity_evidence · org_event · task (identity review) · chain_member
   contacts → contact / contact_source
        ▼
   api_read views (shaped by link status, published only while reconciled) → /api/v1/queries/sales/orgs/* → portal
```

### 3.2 Schema (additive; no DROP)

Three migration groups, each with FR1 and FR2 listings of `db/migrations/` around the write (highest today `0362`; `0353` and `0354` are landed).

**M1 — additive, no behaviour change** (applied early): tables and functions.
- `sales_core.org` gains `shopify_link_status` (`verified | review | disputed | retired`, null while unlinked), `owner_email`, `created_by_run`, `retired_by_run`, `merged_into_org_id`. The partial unique index on `shopify_customer_id` already guarantees one org per Shopify customer.
- `sales_core.chain` (+ `chain_rule`, `chain_member`, `chain_branch_group`): stable uuid ids; `source_sha`; every field of `chain_map.json`.
- `sales_core.org_event` — append-only like `lead_event` (UPDATE and DELETE raise). Payloads carry ids only. Types: `identity_linked`, `identity_review`, `identity_disputed`, `identity_resolved`, `identity_reverted`, `identity_merged`, `org_retired`, `owner_assigned`, `contact_added`, `contact_verified`, `contact_rejected`, `contact_redacted`.
- `sales_core.org_identity_evidence` — append-only: org, customer, source (`shopify`, `lead`, `customer_portal_access`, `customer_book`), kind (`shopify_id`, `phone_exact`), a salted hash of the normalised value, the source row reference, the source row's `updated_at` at match time, run id. A DB-held random salt (in `app_setting`) keeps evidence replayable and erasable-by-design: no raw values.
- `sales_core.link_org_shopify(org, customer, status, evidence, actor, run)` — the only writer of `shopify_customer_id` and `shopify_link_status`; rejects ids that are not `gid://shopify/Customer/%`; writes the event and the evidence.
- `sales_core.shopify_customer` (gid, display name, trimmed `client_key`, tags, created and updated times, run) and `shopify_customer_phone` (gid, E.164 via `normalize_phone_il`, field: default or address). No email, no `id_nomber`, no customer notes. Only customers who become orgs are stored.
- `sales_core.shopify_order` (order GID; customer GID; `kind` order or draft; created, processed, cancelled, closed times; `test`; financial and fulfilment status; source name; tags; `refund_count`; `edited`; `subtotal`, `current_subtotal`; `lines_ex_vat`; currency; `shopify_updated_at`; draft status; `deleted_at`; first and last run) and `shopify_order_line` (order, line GID, SKU, title, `quantity`, `current_quantity`, original and discounted line totals, product and variant GID). Order class is **not stored**: it is `sales_core.order_class(kind, test, cancelled_at, refund_count)` evaluated in a view, so replacing the function cannot leave stale values.
- `sales_core.mirror_run` and `mirror_stage_*` (§3.4). A partial unique index allows one `running` run.
- `sales_core.contact` and `contact_source` (§3.7); `sales_core.access_log` (§3.9).
- `sales_core.rep_can_read_org(email, org_id)` — one SQL function behind every org route.

**M3 — schedule** (applied after the apply): the `pg_cron` entry for the refresh.

**M2 — cutover** (applied right after the apply): `ingest_lead` records evidence only; a guard trigger on `org` rejects direct writes to the link columns; the shaped views (§3.8); the radar and `convert_lead` require `verified`.

### 3.3 Classes and money

Class order: draft, test, cancelled, refunded, completed (I3). Money is the sum of line `discountedTotalSet.shopMoney`, ex-VAT (`recipes/sales-report.md`, D-012); tax, net and gross columns, `amountSpent` and `currentTotalPriceSet` are never used. The order also stores `subtotal`, `current_subtotal`, `edited` and the line `current_quantity`; an invariant (sum of discounted lines versus subtotal) flags every exception with its cause (edit, order-level discount, refund, shipping), and flagged orders are listed in the method sheet. Refund money is stored raw and is not netted. Buckets use Asia/Jerusalem. Amounts are `numeric(14,2)`.

### 3.4 Mirror job

- **Runtime.** A Railway API internal job, `POST /api/v1/internal/jobs/sales-shopify-mirror`, bearer `JOB_RUNNER_TOKEN`. It returns 202 with the run id and works asynchronously: the full pull is a bulk operation of several minutes, beyond a request limit, and a redeploy can kill it. Single-flight comes from the partial unique index on `mirror_run` plus a `heartbeat_at` lease (a run silent for 15 minutes is failed by the next starter). No `private_core` write, no advisory lock (pooled connections break session locks), no reuse of the LionWheel run gate.
- **Client.** `createShopifyGraphQL` (`api/src/order-intake/shopify/graphql.ts`) is reused and returns `extensions` additively. The mirror module pins its **own** API version constant (the shared `SHOPIFY_ADMIN_API_VERSION` stays with the order bot), checks the served `X-Shopify-API-Version`, polls bulk operations by id, requests ungrouped JSONL and joins children by `__parentId` without assuming order. `THROTTLED` (HTTP 200 with errors) retries by cost and otherwise fails the run loudly; it is never "no data". Token: `SALES_MIRROR_SHOPIFY_TOKEN`, falling back to `SHOPIFY_ADMIN_API_TOKEN`; the module contains no `mutation`, enforced by a test. The bulk download URL is never stored, logged or returned; `mirror_run.error` holds codes and GIDs only.
- **Stage.** A pull writes parsed rows to `mirror_stage_*` under the run, with the raw file's sha256 and the served API version in `mirror_run`. Customers of excluded classes are counted, never stored.
- **Dry-run.** `mirror_promote(run, commit := false)` runs the whole apply, including B1, identity, chain proposals and contacts, inside a subtransaction that is rolled back, and returns the report and digest: counts by class and kind; customers verified, to review and excluded (with recency split); orgs to create, link, review and dispute; contacts to add; customers verified only by ₪0 orders; Today card changes in both directions; chain memberships; the order-coverage ledger (every Shopify order is either mirrored or counted under an excluded customer). Cutoff T is 00:00 Asia/Jerusalem of the preview day, aligned with ShopifyQL days. The digest is computed in SQL in integer agorot over orders (`gid | class | agorot | customer`), identity (`customer | org | action | evidence kinds`), contacts and chain members.
- **Apply.** `mirror_promote(run, commit := true, expected_count, expected_digest, approver)` is a SQL function, as the Unit A backfill was. It consumes exactly the staged rows, recomputes the digest and refuses on any mismatch; if the live database changed the plan, a fresh preview is one SQL call. It is run by an authorised person after Tom's count-specific go, which is recorded in `mirror_run`. It is not reachable from cron or from the job token.
- **Refresh.** A scheduled run (`40 0 * * *` UTC, clear of the radar at `30 1`, the leads job at `0 4`, ShopifyQL at `17 4`, the reconciler `*/5` and the shop sync `*/15`) refuses to start until a completed apply exists. It pulls orders by `updated_at` from the maximum seen watermark minus 10 minutes, refreshes open drafts as a set, and nightly pulls the customers who ever ordered (`client_key`, tags, phones) and re-evaluates B1. Weekly it anti-joins order GIDs: a GID gone from Shopify gets `deleted_at`, never a silent removal, and an org whose customer no longer resolves becomes `review`. Mirror rows update freely; the identity step obeys the caps in §2.3.
- **Rollback.** Before promotion, rollback is "do not promote". After it, orgs and links are **retired**, never deleted: status `retired`, `retired_by_run`, an `identity_reverted` event, review tasks cancelled with a reason; leads are never moved back silently. Mirror rows created by a backfill are deleted by `first_run_id`; order lines cascade. A CI test runs apply, rollback, then compares hashes of the tables that are not append-only.

### 3.5 Reconciliation and publication (D4)

The reconcile runs after every refresh under the same lease, and once straight after the apply.
- **Census (every customer).** Per mirrored customer, ShopifyQL `FROM sales SHOW orders, total_sales GROUP BY customer_id` equals the mirror: non-test order counts exactly; revenue with zero unexplained residual once each order's difference is attributed to edit, order-level discount, refund or shipping. The recipe's gate 1 (≤ 0.5% over the window) and gate 2 (exact monthly counts including cancelled, Asia/Jerusalem) run on every reconcile.
- **Live sample.** Every org with any refunded, test, cancelled, edited or draft order, the ten largest by revenue, and 20 random orgs. Seed: the first 8 hex digits of the apply digest. Shopify is read live and to the end, restricted to `created_at < T`; the comparison is of **sets** of `(gid, class, agorot)`, tolerance 0. Orders whose `updatedAt` is later than the mirror's watermark are reported as in flight and excluded; more than 1% in flight fails the run.
- **Independent of the class function.** The census and the stored `subtotal`/`current_subtotal` invariants do not depend on `order_class`, so a wrong class or money rule cannot pass silently.
- **Publication gate.** Orders, money, the circle and river money are returned only while the latest reconcile is `pass`. A failed reconcile returns `history_status: unverified` and the screen says so; before the first apply, "no history loaded" differs from "0 orders". A last good refresh older than 36 hours shows a stale banner and writes an exception row.
- **D4b.** Three consecutive scheduled reconciles pass after the apply, covering orders created and changed after T from real traffic. This session reports D4b as pending until they have run.

### 3.6 Identity layer

- **Single writer.** Only `link_org_shopify` sets `shopify_customer_id` and `shopify_link_status`. `ingest_lead`, the daily backfill and the customer-setup step record their hit as evidence. The leads-poll lookup returns no link when the search finds more than one customer.
- **Derivation, in order.** (1) Verified set = B1 over the mirror. (2) For each, find the org holding the id and re-derive its status from evidence. (3) Otherwise apply B4 to lead-born orgs by phone against every customer phone: exactly one candidate that is not a branch of a multi-branch chain links the org (a lead-born org whose customer already has an org is **merged**: its leads are re-pointed, it is retired and `merged_into_org_id` is set, with an `identity_merged` event on both); two or more candidates make the org *disputed*, with no placeholder org. (4) Otherwise create an org for a verified customer: display name from Shopify, `phone_e164`, `email` and `email_domain` left null so `match_org` cannot pick an arbitrary branch. (5) Customers tagged for review, and active customers without `client_key`, get an org in `review`. (6) Chain memberships are proposed from the map's rules and included in the digest.
- **Transitions.** Status re-derives from evidence on every run, never from an id being present. A table of status × B1 result gives the action, event and task effect; a condition that clears closes its task with `system:identity` and a reason.
- **Review tasks.** `task.org_id`, kind `other`, `source_kind = 'identity_review'`, key `identity_review:<gid>:<reason>:<evidence digest>`, owner null, never reassigned. They never appear in Today or `/tasks` (those filter `source_kind <> 'identity_review'`); a manager review screen lists them.
- **Manager resolution.** Confirm a link, pick a candidate, or reject: one transaction writes the event, the status and the task.
- **Evidence.** No raw values, a salted hash only; a mapped `wa_customer_map` row is evidence only when it was mapped by a person, and a row that records several accounts sharing a number is never evidence.

### 3.7 Contacts

`contact` (org, name, phone E.164, email, kind `person` or `org_channel`, verification `unverified | verified | rejected`, `verified_by`, `verified_at`, `verification_basis`, redaction) with unique `(org, e164)` and `(org, lower(email))`. `contact_source` is append-only provenance (system, source row, field, observed time, the source's `updated_at`, value hash, run); a contact without a source row cannot exist. A verified contact must be re-verified when its source changes or after a period. Auto-verification: only a session phone linked to a completed mirror order of this org (`wa_session.shopify_draft_id`) or a portal submission's order. Green Invoice contacts enter only with a reader keyed by `client_key`, otherwise they stay out of B. Unverified contacts render no `tel:`, `wa.me` or `mailto:` link. Phones that fail `normalize_phone_il` plausibility are rejected.

### 3.8 Views and read API

- Views only **append** columns (`CREATE OR REPLACE VIEW` keeps the old columns and order): `shopify_snapshot` becomes `null::jsonb`; new columns (order count, last order, active, 12-month ex-VAT total, link status, chain) are `case when shopify_link_status = 'verified' and published … end`. `is_existing_customer` is `shopify_link_status = 'verified'` in `v_sales_orgs`, `v_sales_today` and every view that derives it. A test fails the build for any view column that derives from the mirror without the gate.
- **Org detail** `/api/v1/queries/sales/orgs/:id`: one payload (header, chain or moved status, link status, counts, active label, coverage line), plus cursor-paged `/orders`, `/river` (orders and events in one stream, internal notifications hidden by default) and `/contacts` (verified and review lists), and `/circle` (monthly counts and the last order — facts, never drawing coordinates). Manager-only: `GET /identity-review` and the mutations for bulk owner assignment, identity resolution, and contact verify, reject, promote and redact.
- **List scale.** The org list route filters, sorts and pages on the server (active, not yet a customer, all; in review for managers; sort by last order, 12-month ex-VAT total, name; pages of 50); search uses a lean `{id, name, phone}` index or endpoint instead of loading every org on every screen.
- **Rep scope.** A rep reads an org through `rep_can_read_org` (an org behind own leads, or `owner_email`) on every route. The river and contacts carry lead-derived rows only for leads the session can read. Owner mutations are manager-only. A rep on a review or disputed org gets a status code and no candidates. Any other org: 403 with no data in the body.
- **Gate 4.** Review, disputed and retired orgs return their own leads, lead events and lead-sourced contacts and nothing derived from Shopify (orders, money, circle, chain, Shopify contacts). A manager's candidate view shows each candidate's order count and last order labelled as candidate evidence.

### 3.9 Security and privacy controls

Customer personal data is stored only for verified and review customers and never in append-only tables; phones are normalised and kept in one service-role-only table. `id_nomber`, emails and notes are not stored. An access record (actor, org, route, time) is kept for the contacts, orders and river routes; the API otherwise runs with `logger:false`. A manager-only redact action nulls a contact's values and writes `contact_redacted`. New routes validate ids. The radar function gets a bearer check. Committed files and images in the three public repositories contain no customer name, id, amount, order or contact: screenshots use synthetic fixtures, and proof on real data goes to Tom privately.

### 3.10 Portal (starts only after Tom approves mockups and string round 1)

A full route `/sales/orgs/[id]` replaces the 448px drawer. First viewport at 390px, top to bottom: header (name, branch or chain, link badge, owner); the next open task or promise; the primary verified contact with call and WhatsApp buttons; summary (last order with lines on tap, 12-month count and ex-VAT total, "as of"); the circle. River and contacts below.

Proposed visuals, shown as mockups before any build:
- **Business circle** — a two-year ring: the outer ring the last 12 months, the inner ring the 12 before. Each calendar month is a segment and the tap target (about 63 px outer, 44 px inner at 390 px; a 6×4 month grid below 360 px). Ticks inside a segment are not interactive: filled for completed or refunded orders, hollow for cancelled, an amber outline for open drafts, tests never drawn. A tap opens a sheet of that month's orders with source and time. The centre shows the last order date and days since, in neutral ink, with "as of <sync>" and a Shopify-only line; for orgs moved to a distributor it shows "moved to X since <date>" with the map as source, never a silence count.
- **Event river** — the same stream as the order history, with chips (all, orders, contact); cancelled orders and drafts behind chips; open drafts pending at the top with their age.
- **Contacts** — a list of verified contacts, and a separate review area for unverified ones; the radial compass is deferred.

Every node and number opens its source and time. Phone: the visuals collapse to a vertical sequence. Reduced motion keeps the meaning without animation, and no animation runs forever. Mockups at 390 and 1280 cover 0, 1, 8, 28 and 216 orders, a distributor gap, review, disputed and a no-lead org, and ship together with string round 1 (grouped by category). Later rounds hold only UX-gate fixes. Tranches follow `docs/portal-os/tranches`. Money always states its VAT basis; one calendar-day helper in Asia/Jerusalem is used for "days since".

### 3.11 Readers

Before the apply, the radar is limited to orgs with at least one lead (today's behaviour; it would otherwise walk about 600+ new orgs and truncate at 500). After M2 the radar and `convert_lead` require `verified`. Rule R — both read the mirror — ships after D4b, in its own tranche, with a preview of the leads that would become `won`.

### 3.12 Tests and CI

- **CI scaffolding (the first PR).** `sales-db` fails on any skipped migration at or above the first B slot and diffs today's skipped set against a pinned file; B migrations are applied twice and the schema fingerprints compared; all `db/tests/03*.test.sql` and `api/test/sales_*` run by glob with a pinned list of expected failures; a missing test file fails; the check fails on `# Looks like`; the paths include `supabase/functions/**` and `api/src/internal/**`; an end-to-end mirror step over recorded fixtures runs twice and compares table hashes, resumes after a crash, refuses a stale preview and passes the rollback test; hashes of every table outside `sales_core` are unchanged.
- **Inner loop.** PostgreSQL 16 in the scratch directory, same apply loop and cron stub, `env -i`; CI on PG17 is the authority. Each SQL task lands red, then green.
- **pgTAP.** One customer, one org; a chain is never merged by name; a public email domain never links; a disputed or review link returns no money, count, last order, active or existing-customer flag on the list, today and detail; append-only triggers; the `order_class` truth table; view aggregates equal the sum of the mirror rows; the sole-writer guard; the merge of a lead-born org; the transition table.
- **Node.** Client (throttle retry by cost, paging to the end, bulk JSONL parse including orphan and out-of-order children, a failed or "already in progress" bulk operation); digest stability and Node digest equal to SQL digest; stale-preview refusal; reconcile logic; a test that fails if the mirror module contains `mutation`.
- **Fixtures** (recorded read-only and scrubbed; CI fails on any phone or email pattern): completed; ₪0 line; cancelled with a refund record; refunded in full and in part; edited; order-level discount; line with no SKU; no lines; the one test order; `taxesIncluded=false`; presentment currency; no customer; customer reassigned; created before T and updated after; the 2026-04 mass cancel; drafts open, invoice-sent, completed and older than a year; customers with no `client_key`, with `needs-verification`, with only cancelled orders, with only drafts.
- **API role matrix.** A rep gets 403 on another owner's org, orders, river, contacts, circle and the identity review list; a manager succeeds; the river carries only the rep's own lead events; owner and contact mutations are manager-only.
- **Portal.** Unit and mocked e2e; no horizontal overflow at 320/390/430/1280, light, dark and reduced motion (`getAnimations().length === 0`); labels in HTML or measured by glyph box so the 12 px check cannot be fooled; long fixtures (a 64-character Hebrew name, long product titles, "₪123,456", ten contacts and twelve unverified rows, 300 river items); a test that fails on any event type without a label; `orgs.test.tsx` is replaced because it asserted the snapshot word "נטש", an explicit carve-out from D8. Performance: seed 3,500 orgs, 14,000 orders and 50,000 lines and hold a p95 and payload budget on the list.
- Unit A and D1 suites stay green on the final heads (the four known local `tel:` artifacts excepted), except the carve-out above.

### 3.13 Deploy

Per masterprompt W6, with the cutover order below.
1. Before dispatch, `rebuild_verifier()` must be 0 (Supabase connector). Each B migration is wrapped in `begin … commit` with `set local lock_timeout = '5s'` and is idempotent. Evidence that a migration is applied is the workflow log plus `information_schema`, never `schema_migrations`.
2. Apply **M1** through `deploy-production.yml` from the feature branch (`confirm=APPLY`, the exact `migrations` glob, `skip_deploy=true`). Applied files are frozen; fixes go forward in a new slot.
3. Merge with checks green so Railway deploys from git; verify the deployment commit. Deploy the edge functions (leads-poll, radar) and the portal.
4. Dry-run from the job; give Tom the counts and digest; apply only on his count-specific go; run the reconcile straight after.
5. Apply **M2**, then verify the views, `rebuild_verifier()` and the Today change counts.
6. Apply **M3** (the cron entry) only after step 4 has completed; the job also refuses to run until a completed apply exists.
Rollback: §3.4. The announcement line precedes every production dispatch.

### 3.14 Out of scope

Unit C (retention, check tasks, basket map) — it inherits the stored order lines and the active label. Unit E. The Menu Builder. Any send path. Any write to Shopify, Green Invoice or LionWheel. `list_price` and `customer_price` contents. Factory core. The open portal PRs listed in masterprompt §2.4.
