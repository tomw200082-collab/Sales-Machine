# GT Pulse Unit B: portal design (Session 2)

**Date:** 2026-10-02 · **Status:** decided by the executor under Tom's delegation of 2026-10-02 (Session 2 masterprompt §1: visual, layout, interaction and normal Unit B microcopy decisions are delegated; business policy is not).

**Parents:** Unit B spec v2 `2026-10-01-gt-pulse-b-design.md` (§3.8 read API, §3.10 portal), D1 visual spec `2026-10-01-gt-pulse-d1-visual-design.md` (V1–V12), build plan Tasks 24–27, glossary `CONTEXT.md`. Nothing here changes a business decision. Where this document and those disagree, they win.

## 1. Ground truth this design was checked against (2026-10-02)

- Backend `main` `893b3701`: `api/src/sales/orgs_routes.ts` and `orgs_handler.ts` are the contract (13 routes).
- Production read-only (Supabase, 2026-10-02): `rebuild_verifier() = 0`; latest reconcile `pass` 07:47 UTC; no scheduled refresh yet (first at 00:40 UTC on 2026-10-03); 1,329 orgs (1,075 verified, 26 review, 228 unlinked); the 26 open identity tasks are 17 `b1_review_tag`, 8 `customer_not_verified`, 1 `b1_active_no_client_key`; 0 open mirror exceptions; 391 contacts, **0 verified**; 0 orgs with an owner; the largest org holds 424 order and draft records; the longest org name is 66 characters.

## 2. Contract findings that shape the design

- **F1. `circle.drafts` counts every draft record, completed ones included.** A completed draft is also a Shopify order (glossary: "a completed draft is an order"), so the count double-counts and would paint an "open draft" mark beside almost every real order. The portal does not draw `circle.drafts`. Open drafts on the ring come from `river.pending_drafts` (OPEN and INVOICE_SENT only). The river's drafts chip labels each draft by its own status (open, invoice sent, completed). No backend change.
- **F2. The 8 `customer_not_verified` tasks cannot be resolved from the portal.** Confirm answers `SALES_IDENTITY_NOT_MIRRORED`, reject answers `SALES_IDENTITY_NOT_REJECTABLE`, and the customer id the org holds is not exposed to the portal, so `promote-customer` cannot be called with it. The review screen states this plainly and offers no dead button. Opening it needs a backend change (expose the held id to managers, or promote by org); recorded for Tom.
- **F3. No verified contact exists in production.** The primary-contact slot therefore usually reads "no verified contact", with a link to the contacts awaiting review. Managers get *verify* and *reject* on each review row (`POST /mutations/sales/contacts/:id/(verify|reject)`, approved in spec §3.8). That is the only way the call button can ever appear. *Promote* and *redact* stay unbuilt in this session.
- **F4. Next action has no field on the org payload.** It is derived from data the session already reads: the open tasks (`/tasks`, scope `all` for a manager and `mine` for a rep) whose org is this org or whose lead belongs to it, and the open leads' `next_touch_at`. The earliest wins. Nothing is invented: no task and no promise reads "no open action".

## 3. Screens

### 3.1 Businesses list `/sales/orgs`
- Petrol compact band: title, the filter's total ("1,075 עסקים"), a search field, filter chips and a sort select. Managers also see a chip to the identity review with its count.
- Filters (server-side): פעילים (default: active customers plus orgs with an open lead, T9) · טרם לקוח · הכל · בבדיקת זהות (managers). Sort: הזמנה אחרונה · מחזור 12 חודשים · שם.
- Rows link to `/sales/orgs/[id]`. Each row carries the name (wraps to two lines, never clipped mid-word), the chain, and one state badge: active customer, inactive customer, not yet a customer, identity under review, or closed record. The badge carries icon plus text, never colour alone. An open lead gets a blue pill. The meta line holds the last order (relative), the 12-month value before VAT, and the owner (managers).
- Paging: 50 a page, "מוצגים X מתוך Y", and a "הצג עוד" button (cursor).
- Search (two characters or more) uses `/orgs/search` and replaces the list with its hits; "no results" differs from "no businesses yet" and from "nothing in this filter".
- Managers: a "בחירה" mode with checkboxes and a sticky bar holding a roster select, "שייך בעלים" and "נקה" (one transaction, T9).

### 3.2 Business workspace `/sales/orgs/[id]`
First viewport at 390px, top to bottom:
1. **Header (petrol band):** back link, full name (wraps, `break-words`), chain or moved-to-distributor line, state badges (customer state, identity state), owner, and a freshness pill ("Shopify · נכון ל-…") that opens the source sheet.
2. **Next action:** what, when (overdue in coral with text), why, and one action that opens the lead in the existing Unit A flow (where calling and recording happen). Otherwise "אין פעולה פתוחה".
3. **Primary verified contact:** name, phone, email, with call, WhatsApp and email buttons (44px). Otherwise the empty state of F3.
4. **Summary:** last order (tap opens its lines), orders in 12 months, value in 12 months before VAT, and an "as of" line that opens the source sheet. For history that is unverified, stale, or behind a link that is not verified, see §4.
5. **Business circle** (§3.3).

Below the fold: the river, the contacts (verified, then a separate "awaiting verification" area), and the org's leads. From 1024px up the first block becomes two columns (next action with contact; summary with circle).

### 3.3 Business circle (the signature)
- SVG. Outer ring = the last 12 calendar months, inner ring = the 12 before (Asia/Jerusalem). It reads clockwise from 12 o'clock, so the current month ends at the top. Each month is a `<button>`-role segment with a full accessible name ("ספטמבר 2026: 3 הזמנות, 1 בוטלה, טיוטה פתוחה אחת"). At 390px the targets are about 77px (outer) and 44px (inner).
- Marks inside a month are not interactive: a filled dot for completed or refunded, a hollow dot for cancelled, an amber ring for an open draft (from F1); tests are never drawn. More than five marks collapse to five plus a count.
- Centre: last order date, days since (neutral ink), "נכון ל-…" and "מקור: Shopify". For a chain moved to a distributor, the centre shows "עבר ל-X מ-<date>" and **no** days-since (T5).
- Below 360px the ring becomes a 6 × 4 grid of month buttons (four rows of six, oldest first) with the same names and marks.
- A month opens a bottom sheet with that month's orders (paged from `/orders`), each one tappable for its lines, plus source and time.
- A visible legend. Under reduced motion nothing animates; otherwise segments draw in once.

### 3.4 River
Chips: הכל · הזמנות · קשר · בוטלו (n) · טיוטות (n). Open drafts are pinned on top with their age. Every type has a human label, and a test fails on a type without one. Orders show name, line count and value before VAT, and open their lines. Paged with "הצג עוד".

### 3.5 Source sheet
One bottom sheet for any number: the source in plain words, the time it was read, and the basis ("סכום שורות ההזמנה במחיר הלקוח, לפני מע״מ"). For history it also says that history is shown only while the nightly comparison with Shopify passes. No table or column names.

### 3.6 Identity review `/sales/orgs/review` (managers)
- The band shows the coverage line ("570 מתוך 588 לקוחות פעילים ב-Shopify מאומתים · נכון ל-…", source ShopifyQL).
- One card per org: its reason in plain Hebrew, the candidates side by side (name, clean orders, last order, basis: held by the org or shared phone, labelled "ראיה להחלטה"), and only the actions the backend accepts for that reason:
  - id_unproven / phone_shared / chain_branch: "זה העסק" per candidate, plus "אף אחד מהם".
  - b1_review_tag / b1_active_no_client_key: "אשר את הלקוח".
  - chain_rule_hit: "אשר שיוך לרשת".
  - customer_not_verified: none (F2).
- Every action passes through a confirmation dialog that says exactly what will change. Mutations here use synthetic fixtures only; no production decision is taken in this session.
- Unresolved mirror exceptions are listed by kind and time.

### 3.7 States
- 403 and malformed id: "לא ניתן להציג את העסק", with "ייתכן שהקישור שגוי, או שהעסק אינו משויך אליך" and a way back. The same words cover a missing org for a rep (the API answers 403 for both), so nothing leaks.
- 404 (managers only): "העסק לא נמצא".
- Retired or merged: a banner. When the destination is readable it says "העסק אוחד לתוך X" and links there; otherwise "רשומה סגורה". Next action, contact buttons and owner assignment are hidden.
- Loading: skeletons shaped like the blocks. A refetch keeps the current data on screen.
- Error: a retry, with "what failed" named.

### 3.8 Command palette
Leads stay local. Businesses come from `/orgs/search` (debounced, two characters or more) and open `/sales/orgs/[id]`. The legacy `/orgs` list is no longer loaded on every screen.

### 3.9 Unit A links
The lead drawer gains "לעמוד העסק" (`/sales/orgs/[org_id]`). That is journey B: Today, then the lead, then the business.

## 4. Truth presentation

| Condition | Summary and circle | River orders | Banner |
|---|---|---|---|
| link verified, history `ok` | shown, with "as of" | shown | none |
| link verified, history `stale` | shown | shown | "הנתונים לא עודכנו מאז <as_of>" (amber, icon) |
| link verified, history `unverified` | "היסטוריית ההזמנות לא זמינה כרגע" plus why (comparison with Shopify not passing) | hidden, no "0" | same message once |
| link review / disputed | identity panel: rep sees the status only, manager sees the reasons and a link to the review | lead events only | "זהות העסק בבדיקה" |
| no link (prospect) | "טרם לקוח" and no history area | lead events only | none |
| retired | §3.7 | none | §3.7 |

Money is always labelled "לפני מע״מ"; its source sheet says "Shopify, מחיר לקוח". "0 orders" appears only when history is `ok` and the count is 0.

## 5. Out of scope here
Contact promote and redact; promote-customer; Unit C; any write to Shopify, Green Invoice or LionWheel; deciding any of the 26 identity reviews; Ice Dream (U-055); removing the legacy backend `/orgs` route (backend lane; the portal stops calling it).
