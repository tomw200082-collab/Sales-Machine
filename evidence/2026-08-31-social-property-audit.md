# Evidence snapshot — GT public-property ownership audit

**Date:** 2026-08-31 · **Authority:** `system_verified` unless a row says otherwise.
**Immutable.** True only as of this date. Supersede with a newer snapshot; never edit.

**Method:** live reads through the connectors this session held — Shopify Admin API,
Google Drive, Google Calendar, Dropbox, and unauthenticated HTTP against the public
web. Anything not reachable through those is marked `לא אומת` with the reason, not guessed.

---

## 1. Identity fields as published — before and after

The four identity fields were swept across every page in the live sitemap
(30 pages fetched 2026-08-31).

| Field | Found | After this session |
|---|---|---|
| Dead phone `072-3939395` | **42 occurrences** — theme footer on 29 pages, plus page bodies of `אודות` (×4), `מדיניות-המשלוח` (×5), `אמצעי-תשלום` (×4) | **29** — footer only. Bodies fixed. |
| Old email `info@greentea-everyday.com` | **9** — `אודות` (×4), `מדיניות-המשלוח` (×5) | **0** |
| Address `החרושת 19, רעננה` | 1 page (`אודות`) | **0** — replaced with `הלהב 15, חולון 5885817` per Tom's decision 2026-08-31 |
| Live phone `054-398-2444` | 2 pages only (`צור-קשר`, `for-business` — fixed 2026-08-26) | 5 pages |

The remaining 29 are one value: theme `HE-RU Vodoma 2024` (id `131669328113`),
block `1592799116158`, type `contact-info`, setting `phone: "0723939395"`.
Claude cannot write it — the Shopify MCP blocks theme-file writes to the live theme.
One field, manual, path recorded in the credentials sheet risk tab.

## 2. Legal identity — resolved later the same day against Meta's verified record

First pass, from `/pages/אודות`: **`גרינטי אוירי דיי בע"מ` · ח.פ. `515788461`**, graded
`doc_confirmed`. The page carried the name in two spellings (`די` / `דיי`); it was
normalised to `דיי`, the spelling in the formal block.

**That normalisation was wrong, and was reverted the same day.** Tom opened Meta
Business settings, which hold a record Meta verified against official documents on
**2022-12-30**:

| Field | Meta's verified record |
|---|---|
| Business portfolio | `GTeveryday`, id `385165928990715` |
| Legal business name | **`גרינטי אוירי די בע"מ`** — `די`, not `דיי` |
| Registered address | **`מיכ"ל 4, תל אביב יפו 63261`** |
| Business phone | `+972547689911` |
| Website | `greentea-everyday.com` (the old domain) |
| Tax ID | `515788461` — independently corroborates the page |
| Verification status | ✅ verified 2022-12-30 |
| Portfolio created by | Alex Berov, 2019-03-28 |
| Ad-account creation limit | 5 |

`/pages/אודות` was corrected to `די` on Tom's approval, 2026-08-31.

**Two consequences.**

1. **Business verification was never needed.** It has been done since 2022. A session
   that had not looked would have spent days re-submitting it. `f2` and the whole of
   §6.E are closed.
2. **A third address, and a fourth phone.** `מיכ"ל 4, תל אביב` is the *registered*
   address; `הלהב 15, חולון` is what Tom chose as the *published* one and what Shopify
   and Klaviyo hold. Those are two different fields for two different purposes and both
   can be right — but Meta's copy is four years old, and `+972547689911` appears in no
   other GT system and nobody has said whose it is.

**Do not casually edit the verified record.** Changing a verified business's legal name
or address can trigger re-review and put a working 2022 verification at risk.

## 3. Properties — what was actually verifiable

| Property | Verified | Result |
|---|---|---|
| Shopify store | ✅ Admin API, read + write | `GreenTeaEveryday`, primary `gteveryday.com`, SSL on, ILS, Asia/Jerusalem, billing `הלהב 15, חולון 5885817` |
| Email consent base | ✅ Admin API | Segment `Email subscribers` (`363334238449`) = **2,969** — unchanged from the 2026-08-26 measurement |
| Domain `greentea-everyday.com` | ✅ HTTP | 301 → `https://gteveryday.com/`, apex and `www`. Not a duplicate store. Confirms artifact `id2` |
| Meta expiry calendar event | ✅ Calendar API | Exists: `gh2i3vff17eu562hvr5cr461bs`, 2026-10-23 09:00 Asia/Jerusalem, reminders 14d popup + 14d email + 10h popup. **Zero attendees** — no human owner. D6 fails on this |
| YouTube channel | ✅ public HTTP | `@greenteaeveryday5540` live, 7 videos, real Hebrew About. Two are 5-second test uploads titled `3` and `ya`. Admin access not verified |
| Google Drive / Calendar | ✅ read + write | `tom@gteveryday.com` |
| Dropbox marketing assets | ✅ file-by-file | `all bottles/` 33 files · `small products/` 28 · `CATALOG/2 slide/` 18 — every filename in `marketing-assets.md` resolves |
| Instagram, both handles | ❌ **blocked** | `@greenteaeveryday` → HTTP 302 to `/accounts/login/`. `@gteveryday` → HTTP 200 but a login/challenge shell, no profile data. Headless Chromium also blocked (`ERR_CONNECTION_RESET`). **No public data obtainable from this environment.** Stays §6.B |
| Meta Business, LinkedIn, TikTok, X | ❌ no credentials | By design — the asymmetry this whole job is about |

## 4. Warehouse accuracy — two negative records

- `docs/warehouses/marketing-assets.md` cites `CATALOG/MATCHA UBE HOJICHA/hf_20260727_092139_….png`
  and two siblings at the folder root. **The folder returns 0 files at top level** —
  the images sit in subfolders (`PRODUCT PHOTOS/`, `+ colors/`). Paths as written do not resolve.
- The three ODK purée files it cites (`hf_20260720_1555…`) were not on the first page
  of that folder's listing. Not disproven, not confirmed.

Neither is a content gap. Both are warehouse-path errors. Recorded so the next session
does not re-discover them. The Q4 calendar routes around both.

## 5. Third-party code on the live storefront — read from page source

Landmine 5 of the masterprompt says: assume more exist than anyone's plan lists.
Reading `gteveryday.com` homepage source, 2026-08-31:

| What | Evidence | Status |
|---|---|---|
| HubSpot | `js.hs-scripts.com/40143933` | Known (`id4`). Leads go here. Record, do not fix — website session owns it |
| Yotpo | `cdn-widgetsrepository.yotpo.com/v1/loader/…` | Known (`z2`). Reviews + loyalty |
| **judge.me** | theme config: `review: { enable: true, app: "judge.me" }` | **NEW 2026-08-31.** In no plan. Theme points at judge.me while Yotpo loads on the same page — two review systems in parallel |
| **Google Tag Manager / gtag** | `googletagmanager.com` | **NEW 2026-08-31.** Container owner unknown. GA4 itself still not connected (`g3`) |
| unidentified | `d3ryumxhbd2uw7.cloudfront.net/webtracking/rmShopifyUtils.min.js` | **NEW.** Not identified — deliberately not guessed |

Shopify's `appInstallations` query returned `access denied` for this token, so the app
list could not be enumerated the direct way. Page source was the fallback, which is what
landmine 5 prescribes anyway.

## 6. Changes written this session

| Where | Change | Authorisation |
|---|---|---|
| Shopify page `71365755040` (`אודות`) | name normalised · address → `הלהב 15, חולון 5885817` · phone → `054-398-2444` · email → `info@gteveryday.com` | Tom, in writing, this session |
| Shopify page `84325892256` (`מדיניות-המשלוח`) | email + phone, incl. `mailto:` and `tel:+972543982444` | same |
| Shopify page `84474364064` (`אמצעי-תשלום`) | phone | same |
| Google Drive | created `GT — כרטיס גישה` (24 rows + risk block) | §W2 |
| Google Drive | created identity card v2; renamed the 2026-08-26 card to mark it superseded | §W3 |

Original page bodies and the theme `settings_data.json` were captured before any write.
Rollback = restore the recorded strings; each is a single-field revert.

Nothing was published to any social account. Nothing was sent to any customer.
`SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` untouched, still `false`.
