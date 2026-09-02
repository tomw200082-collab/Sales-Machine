# Sales-Machine — Current State

> Sole authority on build status and open unknowns. Volatile by design.
> Last updated: 2026-09-02 — the knowledge-book pass added the 48 recipes and the
> seasonality measurement, and opened `U-037`.
> Before that, 2026-08-31: two sessions landed the same day — the knowledge-book pass
> (`U-014`…`U-021`, `CL-1`…`CL-4`) and the social-property pass (`U-014`…`U-032`).
> **⚠ Their numbering collides — see `COLLISION` at the top of the UNRESOLVED table.**
> New findings are numbered from `U-037` up — above **both** sets (the social-property
> pass reaches `U-036`) — so the open collision does not grow while Tom arbitrates it.

## Build ladder status

| Phase | Scope | Status |
|---|---|---|
| 0 — Constitution | CLAUDE.md truth rules, structure, boundaries | **DRAFT LANDED** — awaiting Tom's written approval |
| 1 — Seed verified knowledge | research findings, evidence snapshot, recipes | **LANDED** |
| 1b — Knowledge layer | ספר העבודה as graded, dated, machine-readable cards under `knowledge/` (products · drinks · answers · boundaries · claims · segments · eval) + reconciler | **LANDED** 2026-08-31 — cards validate 0/0; 9 findings open on Tom (below) |
| 2 — Truth interviews with Tom | 5 sessions → `user_confirmed` doctrine + account dossiers | **NOT STARTED** — next up: Interview #1 (ICP) |
| 3 — System reconciliation | verify tag semantics, channel-move checks, contacts | not started (follows #2) |
| 4 — Agents (read-only first) | declarations in `agents/` | not started |
| 5 — Automations | only after base verified; outreach behind frozen flag | locked |

### Side track — the lead pipeline (factory-os lane, not this repo's phases)

| Step | Scope | Status |
|---|---|---|
| Schema | `sales_core` — org / lead / append-only lead_event, phone normalisation, one `ingest_lead` write path | **LANDED** 2026-08-17 (gt-factory-os #219, migrations 0318–0321, 43/43 pgTAP) |
| Import | the 2026-08-10 Meta export | **LANDED** — 188 leads / 186 businesses; 99 arrived after the intake died 2026-06-07 and had never been seen |
| Workspace — data | mutation functions + `api_read.v_sales_*` views + admin-gated Fastify endpoints | **LANDED** 2026-08-17 (gt-factory-os #220, migrations 0322–0323, 24/24 + 16/16 pgTAP) |
| Workspace — UI | portal `/apps` switchboard + `(sales)` route group: Today queue with the one-tap outcome loop, leads + drawer, orgs, quick-add, ⌘K search, PWA, settings. Hebrew RTL, admin-only | **LANDED** 2026-08-17 (gt-factory-os-portal #213, tranche 162) |
| Live intake | **Make → `/ingest`** (was: Meta poller) | **LIVE** — code landed 2026-08-24, scenarios verified running 2026-08-31 — gt-factory-os PR #227, migration 0329, `sales-leads-poll` redeployed. **Architecture changed today (D-006, reverses D10):** Tom holds no Meta developer access — the only Business app (`Green Tea`) is WhatsApp-only and he is not its admin, and developer registration blocks at SMS verification — so no Graph API token can be issued at all. Proven by the token diagnostic: the token he did produce is valid and non-expiring but carries **none** of `ads_management` / `leads_retrieval` / `pages_show_list` / `pages_read_engagement`. Make's own Meta-approved app carries the leads instead; its Facebook connection (`gteveryday`, 6309050) was reauthorised 2026-08-24 and is valid to 2026-10-23. **CORRECTED 2026-08-31 (read live from the Make API):** both scenarios **are built and running**. `GT Sales — lead intake → /ingest` (id 7075235, instant webhook 3598876) has been green on every run since Tom's last edit 2026-08-24 16:50Z — 11 consecutive successes, most recent lead 2026-08-29 20:16Z; its lifetime 32 errors are all from the build session that day, and 2 items sit in its DLQ. `GT Sales — hourly pulse` (id 7075243) has fired every hour with zero failures, last at 2026-08-31 12:11:15Z. The Facebook connection `gteveryday` (6309050) carries all 9 scopes incl. `leads_retrieval`, `ads_management` and `business_management`, and expires 2026-10-23T10:49:05Z |
| Conversion job + heartbeat | first Shopify order at-or-after a lead writes `won` + evidence; daily heartbeat | **LANDED** 2026-08-24. `sales_core.convert_lead()` is the sole writer of `won`. Heartbeat proven working 2026-08-24 04:00Z (sent, severity=alarm, correct). Now judges **whichever path is carrying leads** and, under Make, watches an **hourly pulse** — because with a third party in front a dead connection and a quiet day are otherwise indistinguishable, which is exactly how the 2026-06-07 failure hid for two months. Pulse route is live; the Make scenario that feeds it is not yet built |

Nothing in this track sends anything to a lead or a customer.
`SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` remains `false`.

## Interview plan (Phase 2)

1. **ICP + segment ranking** — who is a dream client, who is marginal, why.
2. **Top-10 chain dossiers** — incl. U-001/U-002 below.
3. **Pricing & terms decode** — tag semantics (U-003), then system-verify.
4. **Sales process as-is** — how orders really arrive; roles; WhatsApp reality (U-004, U-006).
5. **Competition, positioning, Core Story raw material.**

Each interview → compiled cards → Tom confirms → merged as `user_confirmed`.

## UNRESOLVED (open unknowns — rule 3: never silently filled)

| ID | Question | Route |
|---|---|---|
| U-001 | Isrotel (~₪940K lifetime, ~13 branches) went dark ~2024-09/10 — churn, channel move, or tender loss? | Interview #2 + Green Invoice check |
| U-002 | Mina Tomei: 5 branches went dark the same week (~2026-02) — one story? recoverable? | Interview #2 |
| U-003 | Tag semantics: `10off`, `50-29`, `300ml-23`, `shotef`, `net30`, `pl`/`client_key` metafields | Interview #3 + system verify |
| U-004 | B2B records use placeholder login emails — where do real ordering contacts live? | Interview #4 |
| U-005 | ICP ranking (segments × buyer type) | Interview #1 |
| U-006 | Off-Shopify sales share (Green Invoice direct? distributor?) — required before any churn claim | Interview #4 + GI check |
| U-007 | Annual-value method assumes steady rate; validate per tier | Recipe validation |
| U-008 | "The website" scope — storefront vs. marketing site vs. B2B portal (separate runtime repo either way, per D-003) | Tom decision |
| U-009 | Data quirk: account with 58 orders and ₪0.00 amountSpent — explain before trusting spend fields | Interview #3 / system check |
| U-010 | 4 identity questions from the 2026-08-06 tracker build (MUZA×2, נונומימי/נונו, קפה עם, קלאוד ניין) — merge or keep separate? | Tom, via `knowledge/accounts/customer-notes.yaml` |
| U-011 | **Re-measured live 2026-08-31: 200 leads — 142 `new`, 12 `working`, 3 `won`, 43 `lost`, and 188 with no assignee.** So the queue is being worked (Avi, 113 events) but almost nothing is owned. Tom decided 2026-08-31: he is primary, Avi and Alex take the large ones; the 142 untouched stay for a planned personal bulk outreach rather than being closed. Original entry: the Today queue currently holds all 188 leads, because every imported lead is genuinely untouched and past SLA. Honest, but a queue the size of the whole table is not "call these two, follow up on these three". Work the backlog down, or cap the daily queue? | Tom — product decision, deliberately not taken during the build |
| U-012 | Erik's role and how leads get assigned. The schema and the queue already scope per assignee (`assignee = me OR unassigned`, admins see all); only the UI to assign at scale is missing | Tom, when a second person joins |
| U-013 | Should the Facebook form ask for a business name again? The live form is two questions (name, phone, email), so an incoming lead is close to anonymous and the org has to be inferred | Tom + Alex — marketing decision with a direct data consequence |
| **COLLISION** | ⚠️ **`U-014` … `U-021` are allocated twice, to different questions.** Two sessions ran in parallel on 2026-08-31 and each numbered from the same free slot: the knowledge-book pass took `U-014`…`U-021` for the agent's asset and boundary gaps (Hebrew rows below), and the social-property pass took `U-014`…`U-032` for the ownership audit (English rows below). **Both sets are real and neither is dropped.** They are not renumbered here: `CURRENT_STATE.md` is the sole authority on this list, the IDs are already cited across playbooks, two PR bodies, the tracker artifact and the Drive action board, and a unilateral renumber by one of the two sessions would break the other's references silently. Read every `U-0xx` below **with its row**, never by number alone, until this is settled | **Tom — arbitrate.** Cheapest fix: keep the knowledge-book numbering (it reached `main` first) and re-prefix the social-property set, then sweep its references in one pass |

### Knowledge-book pass (reached `main` first — `#24`, `#25`)

| ID | Question | Route |
|---|---|---|
| ~~U-014~~ | **נסגר 2026-08-31.** ארבעת ה-300 מ״ל — טום: "לא להציע בכלל, זה היה רק להזמנה ספציפית" (הזמנת מימי ואזה). `customer_facing: false`, ⊥ מוזכרים ביוזמתנו | — |
| U-015 (→ אלכס §5) | **חצי נסגר 2026-09-02.** ✅ **עונתיות — נמדדה** (`evidence/2026-09-02-seasonality.md`): החורף רץ ב-75–89% מהזמנות הקיץ שלפניו, ושתי עונות חורף נמדדו. `answers#seasonality` עבר מ-`העברה` ל-`טיוטה` עם נוסח מהמדידה. ⛔ **עדיין פתוח:** תסריט למלון / קייטרינג / משרד — קהלים ש-`gt-acquisition-os` מגדיר כיעד ואין להם נוסח | הנוסח → אישור טום/אלכס · התסריט → החלטת טום |
| U-016 (→ אלכס §4) | מה קורה אחרי ההזמנה הראשונה: מדיניות החזרה/החלפה כשמשקה לא נמכר · מה עושים כשמוצר חסר · תדירות הזמנה חוזרת ומי מתקשר. אין מדיניות מוצהרת בשום קובץ. הראיה מ-2026-08-24 מראה 0 refunds ב-25 חודשים (GT מבטלת, ⊥ מזכה) — התנהגות היסטורית, ⊥ מדיניות | טום + אלכסנדר |
| U-017 (→ אלכס §6) | בנק התשובות חי ב-`knowledge/answers/answer-bank.yaml` (30 שורות). הגיליון שמערכת הלידים אמורה לקרוא ממנו — ⊥ נבנה, וכיוון הסנכרון ⊥ סוכם עם סשן מערכת הלידים. שני בנקים = כישלון D3 | תיאום בין-סשן + טום |
| ~~U-018~~ | **נסגר 2026-08-31.** כשרות וחיי מדף — טום: "אין מסמכים, אני מאשר את שניהם כעובדה". מדורגים `user_confirmed`. בקשת תעודה מלקוח עוברת לאלכסנדר, כי אין מה לשלוח | — |
| ~~U-019~~ | **נסגר 2026-08-31.** ארבע רשומות-השלילה נשארות פעילות בשופיפיי (טום: "תשאיר"). כלומר: ⊥ במחירון הלקוחות ו⊥ מוצעות בשיחה, אבל לקוח שמגיע לחנות יכול להזמין. זו הכרעה, ⊥ פער | — |
| U-020 | תיקיית `05 · מה שולחים ללקוח` ריקה. ✅ **המתכונים נסגרו 2026-09-02** — `knowledge/drinks/recipes.yaml`, 48/48, מנות מאושרות שנבדקו מול העלות + שיטת הגשה, מרונדרים ל-`03 · מתכונים`. ⛔ **עדיין חסר:** קטלוג המשקאות בתוקף (PDF) · מחירון ללקוח (PDF) · סרטוני ההדרכה שהספר מבטיח · תעודת כשרות | **טום — בתהליך.** הצהיר 2026-08-31 שיעלה חומרים שיווקיים ל-`06 · העלאות` |
| U-021 | 17 מתוך 17 כללי `boundaries/refusals.yaml` מסתיימים ב"מעביר לאלכסנדר" — ו**אין בשום קובץ מספר, מייל או קבוצה**. סוכן ווצאפ שיגיע לכלל כזה נעצר באמצע שיחה בלי מסלול המשך | טום — פרט קשר אחד, ואז כרטיס `user_confirmed` |
| U-037 | **אפריל 2026: ₪146,254 על 271 הזמנות** — החודש החלש ביותר ב-25 חודשים בהכנסה, אבל ⊥ במספר ההזמנות (מרץ 221, מאי 322). ה-AOV נפל מ-~₪1,400 ל-~₪540 לחודש אחד ואז חזר. זו ⊥ עונתיות — או זיכויים/ביטולים גדולים שנרשמו באותו חודש, או פער נתונים. התגלה אגב מדידת העונתיות 2026-09-02. **ממוספר U-037 בכוונה** — U-022 *וגם* U-033 כבר תפוסים ע"י מעבר נכסי הרשת, ש-U-036 הוא המספר הגבוה בו. ההתנגשות הפתוחה ⊥ אמורה לגדול | בדיקה מול Green Invoice / דוח הזמנות אפריל |
| ~~U-038~~ | **נסגר 2026-09-02.** טום הכריע: `מרכז א׳/ב׳/ה׳ · צפון ג׳ · דרום ד׳` היא ההבטחה — הימים, ⊥ טווח ימי עסקים ארצי. מאשרר את D-010(ו), מבטל את `עד 3 ימי עסקים`. ראה D-013(א) | — |

## החלטות שממתינות לטום — עודכן 2026-08-31
**נסגרו באותו יום, בכתב:** TOM-A.2 (ימי אספקה) · TOM-A.4 (אין חוזה/מינימום/בלעדיות) ·
TOM-B (רשומות-שלילה יורדות; AMERICAN ו-HOJICHA נשארים) · TOM-C (ששת השמות מותרים) ·
TOM-D (700 ו-8 שנים מאושרים) · TOM-E (HOJICHA נשאר, + 1 ק״ג ב-₪750).
הרשימה המלאה: `doctrine/decisions.md` D-010.
**מה שנשאר — הכל מרוכז ב-`open-items/alex-meeting.md`, לסגירה בישיבה אחת:**

| # | מה | חוסם |
|---|---|---|
| 1 | מדרגות ההנחה לפי צריכה חודשית — המספרים | `boundaries#discount_or_terms` |
| 2 | שלוש חבילות ההתחלה — שם, תוכן, מחיר | **שלב בקשת ההזמנה** (`sales-motion#s05`) |
| 3 | אישור **9** שורות הטיוטה בבנק התשובות (8 מ-31.08 + `seasonality` מ-02.09, שנכתב מהמדידה) | 9 נוסחים ⊥ נאמרים ללקוח |
| 4 | מה קורה אחרי ההזמנה הראשונה — החזרה/החלפה · חוסר מלאי · מי מתקשר | 2 שורות `העברה` |
| 5 | ~~עונתיות~~ **נמדדה 02.09** — נותר רק תסריט מלון/קייטרינג/משרד | U-015 (חצי) |
| 6 | כיוון הסנכרון של גיליון הלידים | U-017, D3 |
| 7 | `כ-17 קלוריות` — מקור או הסרה · ארבע רשומות-השלילה עדיין בנות-הזמנה | CLAIM-3, U-019 |

**פתוח על טום בלבד — ⊥ דורש את אלכס:**

| מה | מצב |
|---|---|
| **חומרים שיווקיים לשליחה** (U-020) — קטלוג, מחירון ללקוח, סרטוני הדרכה → `06 · העלאות` בדרייב. ~~מתכונים~~ נסגרו 02.09 | **בתהליך.** טום 2026-08-31: "אני אכניס שם חומרים שיווקיים לשליחה" |
| **פרט קשר לאלכסנדר** (U-021) — היעד של 17 כללי ההסלמה | פתוח |
| **סנכרון הדרייב** — 6 מ-10 הקבצים ⊥ זהים בייט-לבייט לבנייה שבריפו. הכלי מאפשר רק יצירה+מחיקה, ⊥ החלפה בתוכן, כלומר ה-file-ID משתנים | פתוח — נשאל, ⊥ נענה |

## פריטי ניקיון (⊥ חוסמים)
| # | מה | איפה |
|---|---|---|
| CL-1 | `docs/pricing/2026-08-05_drinks_final_figures.json` הוא גרסה **מוחלפת** ועדיין יושב במאגר. קריאה ממנו מייצרת עמוד שלם של סתירות שאינן קיימות. לסמן או להסיר | `gt-factory-os-production-brain` |
| CL-2 | חמישה פגמים בקטלוג המשקאות שהספר עצמו מונה ב-§09 (שלושה מתכונים לתמצית שלא קיימת · מתכון וניל/אגבה כפול · "20–25 כוסות" · מספור כפול · ארבעה קטלוגי קנבה) — **בבעלות סשן תפריטי הקטגוריות**, ⊥ מתוקנים כאן | קנבה |
| CL-3 | `page 12` — הספר קורא למשקה `חליטת תה ירוק לואיזה וליים`; הרשות קוראת לו `חליטת תה ירוק וליים`. הכרטיס נושא את שם הרשות | סגור בכרטיסים |
| CL-4 | `catalog-truth.md` נזרע 2026-08-06 ולא הוצלב מול שופיפיי עד 2026-08-31. שתי שורות בו טענו "אין SKU פעיל" ולשתיהן היה — ובאותה בדיקה התגלה ש-AMERICAN תומחר הפוך בחנות. תוקן. **הלקח: קובץ אמת שלא נסרק הופך לרמז בעצמו** | סגור · `scripts/knowledge/drift_scan.py` |

### Social-property pass (this branch — the ownership audit)

| ID | Question | Route |
|---|---|---|
| U-014 | **CLOSED 2026-08-31.** Legal name is `גרינטי אוירי די בע"מ` (`די`) and ח.פ `515788461`, per the Meta business record verified against official documents 2022-12-30 — `system_verified`. The earlier `doc_confirmed` reading from `/pages/אודות` had the wrong spelling and the page was corrected. Tom declined a registrar check as unnecessary given the Meta record | — |
| U-022 | Meta's verified record holds the **registered** address `מיכ"ל 4, תל אביב יפו 63261`, while `הלהב 15, חולון 5885817` is the **published** address (Tom's decision, and what Shopify and Klaviyo hold). Both can be correct — registered vs. operating — but Meta's copy is from 2022 and nobody has confirmed it is still current | Tom — confirm the registered address is unchanged before any document-bearing submission |
| U-023 | `+972547689911` is the business phone on Meta's verified record. It appears in no other GT system and nobody has said whose it is | Tom — identify, then decide whether to align it with `054-398-2444` |
| U-024 | **Merged is not deployed, and nothing checks.** `deploy-edge-function.yml` is `workflow_dispatch` only — "Never runs on push" — so an Edge Function change lands on `main` and stays dormant until a human clicks, and nothing anywhere compares what is on `main` against what is running. The morning digest was written, migrated and cron'd on 2026-08-25 and sent nothing for six days because of this. Its own header names the same failure on the LionWheel pick bridge before it, so this is the third occurrence of one class | Tom — decide the mechanism: deploy on merge for these functions, or a check that fails when a deployed function's sha is behind `main` |
| U-025 | Inbound WhatsApp is invisible to `sales_core`. `054-398-2444` is the real order line and now also linked to the Facebook Page, but a customer who writes to it never becomes a lead row — `channel: call \| whatsapp \| email` records only how a rep reached *out*. This is also the gate on any click-to-WhatsApp advertising: an ad would drive straight into the gap | Tom + the lead-system lane |
| U-026 | Avi (`avi@gteveryday.com`) is the person actually working the lead queue — 113 events, most recent 2026-08-31 09:13 — and he does not appear in `docs/ceo/reference/people_rhythm.md` at all. No documented role, hours or backup. Separately, `app_setting('whatsapp_templates').new_lead` opens with `כאן תום` while Avi is the one sending it | Tom — add Avi to people_rhythm; fix the template signature |
| U-027 | **TikTok `@gteveryday` is GT's, live, and nobody holds the login.** Public profile JSON read 2026-08-31: bio `🍃GreenTea Essences Company🍃 / עוד לא ניסיתם את זה / gteveryday.com`, created 2023-11-04, **13 videos published**, 23 followers, 383 lifetime likes, public, `nickname` still the default `gteveryday`. It is on no plan and no credentials sheet row was ever filled. An earlier note in this session recorded the handle as *free* — that was wrong: TikTok returns HTTP 200 for non-existent handles, so the status code proved nothing. Separately `@greenteaeveryday` on TikTok belongs to an unrelated Thai account — not ours, do not contact | Tom — recover access (`info@gteveryday.com`, then password reset, then TikTok business recovery). Until then: do not rename, do not delete a video, do not open a second account |
| U-028 | `sales_core.app_setting('meta_poll')` is `enabled: false` and its `last_error` is a Graph API permission refusal — `pages_read_engagement` / Page Public Content Access missing. `last_poll_ok_at` is null: the direct Meta lead poll has **never once succeeded**. Make currently carries leads to `/ingest` instead (D-006), so the pipe works — but the Meta path was written, has never run, and nothing says whether it is meant to be revived or removed | Tom + the lead-system lane — grant the permission on the Meta app, or retire the poll and delete the setting |
| U-029 | **2,537 lapsed customers are sitting in a segment nobody has ever emailed.** Klaviyo `Win-Back Opportunities (Shopify)` = bought at least once, zero orders in 180 days, holds email consent — 2,537 profiles against a consented base of 2,969, so **85% of everyone GT may email is a customer who stopped**. The segment has been computed and active since 2026-07-18. In the same account: 0 campaigns ever sent, 0 flows, 0 sending domains. `Churn Risks` reads 0 only because its filter needs "received ≥2 emails in 90 days", which is impossible when none were sent — a structural zero, not an empirical one | Tom — this is the repo's founding problem, already quantified. Sending needs `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` + written approval, and the sending domain (`e3`) must be authenticated **first**: 2,537 dormant addresses with no DKIM is how a domain gets burned |
| U-030 | Klaviyo's account contact block sets `country: United States` while the address is `הלהב 15, חולון`. That block renders in the compliance footer of every email. Five more fields are off: `organization_name` is `GreenTeaEveryday` (neither the brand nor the legal name), `default_sender_name` is lowercase `gteveryday`, `website_url` is `http`, `industry` is null, `locale` is `en-US` against an `Asia/Jerusalem`/`ILS`/Hebrew audience | Tom — confirm each value, then fix in Klaviyo account settings. Not changed here: this is account identity |
| U-031 | **Coexistence lapses silently, and nobody owns the check.** WhatsApp coexistence requires the phone app to be opened at least once every 13 days and never uninstalled, or the Cloud API link dies. Nothing announces the lapse — no alert, no red row. That is the exact signature of three failures already paid for: the Make OAuth token (silent two months), the 06:00 digest (silent six days), the LionWheel pick bridge (merged, never deployed). With **every lead automation now sitting on `054-758-8132`** (D-014), a silent lapse stops the whole intake and nobody learns. Verified live on the order line: `order_intake.wa_event_log` holds 24,162 events since 2026-06-26, last one minutes ago, 9,501 of them `echo` — coexistence demonstrably works, which is exactly why its one failure mode needs an owner | Tom — name a person, and add a machine check that fails loudly when the newest `wa_event_log` row ages past a threshold. Good intentions are not a monitor |
| U-035 | **Correction — I was wrong about the square logo, twice, in opposite directions.** This file said no square logo existed; `youtube-refresh-kit.md` said `GT_Logo_Black.png` was 800×800. Measured from the PNG header on 2026-09-02: **971×960** — 11 px off square, not 800×800, and not missing. The identical image sits at two Dropbox paths (`New/ARCHIVE/…/BRAND-IDENTITY/Logos/GT_Logo_Black.png` and `Data Center/PRODUCTION 2/B-BAGEL-Tea-Programme/assets/gt-logo-black.png`). Every platform centre-crops, so 11 px is cosmetic and **blocks nothing** — id5, LinkedIn, TikTok and Instagram covers are all unblocked | optional: pad to 1000×1000 for a pixel-exact square. Not required |
| U-036 | **Opening baseline for YouTube, captured 2026-09-02: 15 subscribers**, 7 videos, handle `@greenteaeveryday5540`. The display name is already `GT Everyday · גרינטי` — the `y2` rename is **done**, and the older record of it as `GreenTea EveryDay  גרינטי ` (double space, trailing space) is superseded. Without a dated baseline there is nothing to compare against in 90 days | closed as recorded — belongs in the credentials sheet's YouTube row |
| U-034 | **RE-OPENED 2026-09-02 — I closed this on a misread and the close was wrong.** Tom answered "2. כן. יש לוגו ריבועי" to a two-part message; I took the "כן" as confirming the channel and closed U-034 on it. His screenshot settles it: **YouTube → Settings → Account → All channels shows exactly one channel** — `GT Everyday · גרינטי`, `@greenteaeveryday5540`, **15 subscribers**. `UC8Wlby9ihV04Ky5CsZZoWWg` (`GT everyday`, still live and still empty, re-checked today) is **not under this Google account**. It may still be GT's under some other account — an old marketing login, a former agency — or it may be a stranger on our name. Unproven either way, and the name is still not evidence. ∴ `@gteveryday` cannot be taken by renaming, and the fallback `@gt_everyday` is **re-verified free today (404)** | Tom — take `@gt_everyday` and move on; it is not worth chasing. Only if he wants the exact handle: try recovery on whichever old Google account might hold `UC8Wlby9ihV04Ky5CsZZoWWg` |
| U-033 | **The digest fired — and wrote nine successes that never happened.** First real firing 2026-09-01 03:00:19Z, `il_hour: 6`: the route works and the six-day silence is over. But `ok: false`. 10 leads due, 2 recipients. Tom's email sent (1 lead). **Avi's failed: `resend 403 — You can only send testing emails to your own email address (tom@gteveryday.com). To send emails to other recipients, please verify a domain`.** Resend is still in test mode with no verified domain, so the system can only ever deliver to Tom. The damage is the record, not the miss: `reminder_sent` events were written for **all 10 leads including the 9 that were never delivered**, and `lead_event_reminder_once_per_day` (unique on `lead_id` + Israel-local date) now blocks any retry for those 9 today. The database says Avi was told about איציק בכר, Hadas Elian Levi, Wesam Amara saleh, Hussin Ayoub, אלדר נפתלייב, רפאל שי דיין, Tomer Danieli, tamer and מאור — seven of them overdue since 08-30/08-31. He was not. **This is the same class as U-024 and U-031: a system recording a success it did not achieve.** The function already knows — it wrote `claimed_but_unsent` with all nine ids — it just does not undo the event | **Two fixes, different owners.** Tom: verify a sending domain in Resend, or the digest can never reach anyone but him — the loop repeats every morning until then. Engineering: write `reminder_sent` only **after** a successful send, so a delivery failure stops being a permanent same-day skip. ⊥ delete the nine rows — `lead_event` is append-only |
| U-033-a | **CLOSED as diagnosed, 2026-09-02 — verifying the domain was never going to fix it, and the code says so in a comment.** The 03:00Z run failed with the byte-identical `resend 403`: due 12, sent 1, **11 undelivered to Avi** (9 the day before — 20 across two days, all recorded as sent). Root cause is in `supabase/functions/sales-leads-poll/index.ts:60`: `const DEFAULT_FROM = 'GT Leads <onboarding@resend.dev>'`, used at line 277 unless the `RESEND_FROM` secret is set. `onboarding@resend.dev` is **Resend's shared test sender, which Resend restricts to the account owner's own address** — that is the exact 403. A verified domain changes nothing while the `from` still points at the shared sender. The comment above that line states the assumption that expired: *"Resend's shared sender works before any DNS work … because the only recipient is the account owner."* True when Tom was the only recipient; false the moment Avi became an assignee, and nobody revisited it. **This is wider than the digest** — `poll_run` shows the same `resend 403` on the **`ingest`** route on 2026-08-31 and 2026-09-01, so **new-lead alerts to anyone but Tom have been failing too** | Tom — set the `RESEND_FROM` secret on `sales-leads-poll` to an address on the now-verified domain, e.g. `GT Leads <leads@gteveryday.com>`. One secret, no code change, no deploy. Then the next 03:00Z run proves it |
| U-032 | **CLOSED 2026-08-31 — Tom: every public call-to-action points at the lead line.** All 27 `wa.me` links across the Q4 calendar and the LinkedIn, Instagram, YouTube, TikTok and WhatsApp kits now read `wa.me/972547588132`, plus the two displayed contact numbers on acquisition surfaces (the LinkedIn location field and the YouTube channel description). The website, invoices and storefront pages keep `054-398-2444` — they speak to existing customers. **One number per job, no exceptions to remember.** The link was checked as well-formed and redirecting; that is *not* proof the number answers on WhatsApp, which needs one tap from a phone before the first post goes out | closed |
| U-015 | **CLOSED 2026-09-01 — Tom checked and reported both accounts are fine** (`user_confirmed`). This environment never could read them, so the close rests on Tom's own look, not on evidence gathered here — recorded that way deliberately. ⚠️ Still not recorded anywhere: **which handle is the official one**, and the opening baseline (`i6`). `i2`–`i5` all need the handle before anything is posted | Tom — name the handle when Instagram work starts |
| U-016 | **CLOSED 2026-08-31 — the premise was false.** GT does hold admin; the portfolio was created by Alex Berov in 2019 and business verification passed in 2022. Original entry: GT holds no admin on its own Meta Business account. Blocks the WhatsApp green tag, business verification, the lead-form fix, CTWA, and re-authorising the connection before `2026-10-23` | Tom (§6.E) — find today's admin, or open a Meta support case |
| U-017 | `judge.me` and Yotpo both run on the live storefront — the theme config points at judge.me while the Yotpo loader fires on the same page. Customer reviews may be split across two systems with half invisible | Choose one. Yotpo already runs reviews **and** loyalty (`z2`), so it is the natural survivor |
| U-018 | Google Tag Manager loads on the storefront and nobody has said who owns the container or what fires in it. GA4 itself is still not connected (`g3`) | Tom — GTM account access |
| U-019 | Registrar and renewal date for `gteveryday.com` and `greentea-everyday.com` were never checked. A domain that lapses quietly takes the whole store down | Tom — registrar login, then record in `GT — כרטיס גישה` |
| U-020 | **CLOSED 2026-08-31 — asked in two documents at once, answered twice the same day.** `054-758-8132` is Tom's work number and becomes **the lead number**: every new enquiry and every new-customer sale, with the automations sitting on it (Tom, in writing, this session; already logged as **D-014** on the parallel lead-system branch). `054-398-2444` stays the **order line** for existing customers and is untouched. Two live lines, two jobs — not a swap. It joins the Cloud API by **coexistence**, not classic onboarding (**D-015**): the number stays live in the phone app and the API reads and sends alongside it | closed — see U-031 for what this now puts at risk |
| U-021 | Cups-per-bottle is published as 33 / 30 / 13 on different live pages, and customer count as 700 / 200 (artifact `w5`). Until one approved number exists per claim, no number goes into any caption, page or profile | Tom — one number per claim |

## Pointers

- Module declaration (governance gate): `gt-factory-os-production-brain`
  `docs/decisions/modules/sales-declaration.md` — **APPROVED (Tom, 2026-08-04)**;
  **Amendment A APPROVED (Tom, in writing, 2026-08-17)**. The earlier
  "PR #46 — DRAFT, awaiting Tom" pointer was stale and is corrected here.
- Social/public-property base (2026-08-31): ownership audit
  `evidence/2026-08-31-social-property-audit.md` · handle sweep
  `evidence/2026-08-31-social-handle-sweep.md` · Q4 content calendar
  `doctrine/playbooks/social-calendar-2026-Q4.md` · launch kits
  `doctrine/playbooks/linkedin-launch-kit.md`, `doctrine/playbooks/youtube-refresh-kit.md`,
  `doctrine/playbooks/tiktok-recovery-kit.md` · lead-response SOP
  `doctrine/playbooks/lead-response-sop.md` (binding only on Tom's written approval).
  Coexistence liveness recipe `recipes/coexistence-liveness.md` (U-031).
  Credentials sheet and the 72-row action board live in Tom's Drive, **not in this repo** —
  no secret value is ever written here (`GT — כרטיס גישה` and `GT — לוח פעולות רשתות`,
  folder `GT Everyday — נכסי מותג`). Board as of 2026-08-31 end of session: 13 done,
  14 ready to paste, 23 open, 6 blocked, 16 on the website track. The credentials sheet
  still carries 24 rows and needs a 25th — TikTok (U-027).
- Latest evidence snapshots (both 2026-08-24): `evidence/2026-08-24-make-intake-handover.md`
  (intake hand-over to Make) · `evidence/2026-08-24-sales-report.md` (sales report).
  Previous: `evidence/2026-08-23-live-intake-bringup.md`, `evidence/2026-07-18-two-numbers.md`.
- Knowledge layer (2026-08-31): `knowledge/README.md` — reading order for an agent;
  `evidence/2026-08-31-knowledge-book-reconciliation.md` — the reconciliation run.
  Gate: `gt-factory-os-production-brain/scripts/knowledge/reconcile.py`.
  Rendering (generated, never hand-edited): https://claude.ai/code/artifact/513456cd-5fa3-4ff1-8616-8ea82e020b22
  — the original shared artifact `f0457ed1-…` cannot be published to from this session.
- Sales report recipe: `recipes/sales-report.md` (taxonomy + anchors Tom-approved 2026-08-24).
- Customer-count recipe (rule 2): `recipes/customer-count.md` — never quote a stored count.
- Decisions log (incl. PROPOSED items awaiting Tom): `doctrine/decisions.md`.
