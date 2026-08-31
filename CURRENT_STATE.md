# Sales-Machine — Current State

> Sole authority on build status and open unknowns. Volatile by design.
> Last updated: 2026-08-31 — two landings the same day: the knowledge layer (U-020/U-021)
> and the Q4 existing-customer plan (U-022–U-031).

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
| Live intake | **Make → `/ingest`** (was: Meta poller) | **CODE LANDED, AWAITING SCENARIOS** 2026-08-24 — gt-factory-os PR #227, migration 0329, `sales-leads-poll` redeployed. **Architecture changed today (D-006, reverses D10):** Tom holds no Meta developer access — the only Business app (`Green Tea`) is WhatsApp-only and he is not its admin, and developer registration blocks at SMS verification — so no Graph API token can be issued at all. Proven by the token diagnostic: the token he did produce is valid and non-expiring but carries **none** of `ads_management` / `leads_retrieval` / `pages_show_list` / `pages_read_engagement`. Make's own Meta-approved app carries the leads instead; its Facebook connection (`gteveryday`, 6309050) was reauthorised 2026-08-24 and is valid to 2026-10-23. **Still open:** the two Make scenarios (lead transport + hourly pulse) are not built — awaiting Tom's go-ahead |
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
| U-011 | The Today queue currently holds all 188 leads, because every imported lead is genuinely untouched and past SLA. Honest, but a queue the size of the whole table is not "call these two, follow up on these three". Work the backlog down, or cap the daily queue? | Tom — product decision, deliberately not taken during the build |
| U-012 | Erik's role and how leads get assigned. The schema and the queue already scope per assignee (`assignee = me OR unassigned`, admins see all); only the UI to assign at scale is missing | Tom, when a second person joins |
| U-013 | Should the Facebook form ask for a business name again? The live form is two questions (name, phone, email), so an incoming lead is close to anonymous and the org has to be inferred | Tom + Alex — marketing decision with a direct data consequence |
| ~~U-014~~ | **נסגר 2026-08-31.** ארבעת ה-300 מ״ל — טום: "לא להציע בכלל, זה היה רק להזמנה ספציפית" (הזמנת מימי ואזה). `customer_facing: false`, ⊥ מוזכרים ביוזמתנו | — |
| U-015 (→ אלכס §5) | עונתיות: כל 48 המשקאות קרים והקטלוג בתוקף נקרא `GT_Summer_Menu_2026`. אין ניתוח עונתי בשום קובץ, ואין תסריט למלון / קייטרינג / משרד — קהלים ש-`gt-acquisition-os` מגדיר כיעד. טבלת העובדות מכילה חודש×לקוח ויכולה לענות | ניתוח מטבלת העובדות + טום |
| U-016 (→ אלכס §4) | מה קורה אחרי ההזמנה הראשונה: מדיניות החזרה/החלפה כשמשקה לא נמכר · מה עושים כשמוצר חסר · תדירות הזמנה חוזרת ומי מתקשר. אין מדיניות מוצהרת בשום קובץ. הראיה מ-2026-08-24 מראה 0 refunds ב-25 חודשים (GT מבטלת, ⊥ מזכה) — התנהגות היסטורית, ⊥ מדיניות | טום + אלכסנדר |
| U-017 (→ אלכס §6) | בנק התשובות חי ב-`knowledge/answers/answer-bank.yaml` (30 שורות). הגיליון שמערכת הלידים אמורה לקרוא ממנו — ⊥ נבנה, וכיוון הסנכרון ⊥ סוכם עם סשן מערכת הלידים. שני בנקים = כישלון D3 | תיאום בין-סשן + טום |
| ~~U-018~~ | **נסגר 2026-08-31.** כשרות וחיי מדף — טום: "אין מסמכים, אני מאשר את שניהם כעובדה". מדורגים `user_confirmed`. בקשת תעודה מלקוח עוברת לאלכסנדר, כי אין מה לשלוח | — |
| ~~U-019~~ | **נסגר 2026-08-31.** ארבע רשומות-השלילה נשארות פעילות בשופיפיי (טום: "תשאיר"). כלומר: ⊥ במחירון הלקוחות ו⊥ מוצעות בשיחה, אבל לקוח שמגיע לחנות יכול להזמין. זו הכרעה, ⊥ פער | — |
| U-020 | תיקיית `05 · מה שולחים ללקוח` בדרייב ריקה. הסוכן יודע מה להגיד ו**אין לו קובץ אחד לשלוח**: קטלוג המשקאות בתוקף (PDF), מחירון ללקוח (PDF), סרטוני ההדרכה שהספר מבטיח, ו-48 המתכונים. שלב 03 ברצף השיחה הוא "שולחים ערכה" — בלי הקבצים הוא ⊥ ניתן לביצוע | **טום — בתהליך.** הצהיר 2026-08-31 שיעלה חומרים שיווקיים ל-`06 · העלאות` |
| U-021 | 17 מתוך 17 כללי `boundaries/refusals.yaml` מסתיימים ב"מעביר לאלכסנדר" — ו**אין בשום קובץ מספר, מייל או קבוצה**. סוכן ווצאפ שיגיע לכלל כזה נעצר באמצע שיחה בלי מסלול המשך | טום — פרט קשר אחד, ואז כרטיס `user_confirmed` |
| U-022 | Cocktail collateral. **Partly closed 2026-08-31:** MUZA is gone entirely (cocktails and mixers), and Tom ruled that the only alcohol GT markets which is not another customer's private label is GT Pink / White Sangria — white then dropped for zero stock. The replacement was re-founded on **tea extract as the cocktail base** (₪65/L, 20 serves, better food cost than MUZA gave) with Pink Sangria as the ready-to-pour fallback. Two collateral pieces built: `mixer-serve-cards.md`, `muza-migration-map.md`. **Still open:** the Pink Sangria product page, and kitchen calibration of the suggested ratios | Tom / Denis |
| U-023 | 19 brand groupings await Tom's approval. Decides whether a board row is one conversation or five — changes both workload and script | Tom |
| U-024 | `פתאל` (₪47,304) and `ליאוני` (₪24,278) have no LionWheel delivery since 2026-05-10, so their route day is defaulted to centre rather than measured, unlike the other 151 | Check Green Invoice / a different delivery channel |
| ~~U-025~~ | **CLOSED 2026-08-31.** Avi absent from the system — — `private_core.app_users`: `avi@gteveryday.com`, display_name `Avi`, role `planner`, active since 2026-08-25, portal password set. No fixed hours by design; 3–4 calls a day (Tom). Now owns 22 accounts solo plus 15 joint meetings with Alex | closed |
| U-026 | Chains spanning several regions (`גאפן גאפן`: Ashkelon, Jerusalem, Netanya) carry one dominant route day in the plan. Correct at chain level, wrong at branch level — a chain call that ends in a branch list must split by region | Method fix in the next planning run |
| U-027 | `GTCC-NM-SAN-3.85L` is titled "GT Sangria Cocktail 3850ml" but its SKU carries `NM`, and `GTCC-NON-SAN-3.85L` (Nonomimi) exists alongside it. Ours or theirs? Until Tom rules, it is offered to nobody | Tom |
| U-028 | `GT-HIB-LOW-1L` (FRESH) and `GT-LUI-LOW-1L` (DETOX) are both at **zero stock** in Shopify (verified 2026-08-31). **79 accounts and ₪490,702 of opportunity** depend on one of them. CALM 340 · NAMASTEA 353 · ENERGY 251 · REVIVE 259 are ready | **Production — first task in the plan, 2026-09-01** |
| U-029 | `sales-leads-poll` `routeDaily()` selects conversion candidates with `status in (new,working) and shopify_customer_id is not null`. Loading the 153 plan accounts as leads would mark every one `won` on their next routine order. One-line fix: `and l.source <> 'q4_existing_2026'`. **The plan is not loaded into the sales system until this lands** | Backend |
| U-030 | Stock of `GT-SHI-CER-500` is **80 bags against 74 target accounts** (verified 2026-08-31). Enough for one wave, not a quarter — and matcha is the plan's lead motion, so this blocks it before it starts | **Production — first task in the plan, 2026-09-01** |
| U-031 | The contents of `GT-MAT-KIT` (₪170) are undocumented in every file checked. Until Tom rules, the kit is not offered — a whisk and a frother are quoted separately | Tom |

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
| 3 | אישור 8 שורות הטיוטה בבנק התשובות | 8 נוסחים ⊥ נאמרים ללקוח |
| 4 | מה קורה אחרי ההזמנה הראשונה — החזרה/החלפה · חוסר מלאי · מי מתקשר | 2 שורות `העברה` |
| 5 | עונתיות + תסריט מלון/קייטרינג/משרד | U-015 |
| 6 | כיוון הסנכרון של גיליון הלידים | U-017, D3 |
| 7 | `כ-17 קלוריות` — מקור או הסרה · ארבע רשומות-השלילה עדיין בנות-הזמנה | CLAIM-3, U-019 |

**פתוח על טום בלבד — ⊥ דורש את אלכס:**

| מה | מצב |
|---|---|
| **חומרים שיווקיים לשליחה** (U-020) — קטלוג, מחירון ללקוח, סרטוני הדרכה, מתכונים → `06 · העלאות` בדרייב | **בתהליך.** טום 2026-08-31: "אני אכניס שם חומרים שיווקיים לשליחה" |
| **פרט קשר לאלכסנדר** (U-021) — היעד של 17 כללי ההסלמה | פתוח |
| **סנכרון הדרייב** — 6 מ-10 הקבצים ⊥ זהים בייט-לבייט לבנייה שבריפו. הכלי מאפשר רק יצירה+מחיקה, ⊥ החלפה בתוכן, כלומר ה-file-ID משתנים | פתוח — נשאל, ⊥ נענה |

## פריטי ניקיון (⊥ חוסמים)

| # | מה | איפה |
|---|---|---|
| CL-1 | `docs/pricing/2026-08-05_drinks_final_figures.json` הוא גרסה **מוחלפת** ועדיין יושב במאגר. קריאה ממנו מייצרת עמוד שלם של סתירות שאינן קיימות. לסמן או להסיר | `gt-factory-os-production-brain` |
| CL-2 | חמישה פגמים בקטלוג המשקאות שהספר עצמו מונה ב-§09 (שלושה מתכונים לתמצית שלא קיימת · מתכון וניל/אגבה כפול · "20–25 כוסות" · מספור כפול · ארבעה קטלוגי קנבה) — **בבעלות סשן תפריטי הקטגוריות**, ⊥ מתוקנים כאן | קנבה |
| CL-3 | `page 12` — הספר קורא למשקה `חליטת תה ירוק לואיזה וליים`; הרשות קוראת לו `חליטת תה ירוק וליים`. הכרטיס נושא את שם הרשות | סגור בכרטיסים |
| CL-4 | `catalog-truth.md` נזרע 2026-08-06 ולא הוצלב מול שופיפיי עד 2026-08-31. שתי שורות בו טענו "אין SKU פעיל" ולשתיהן היה — ובאותה בדיקה התגלה ש-AMERICAN תומחר הפוך בחנות. תוקן. **הלקח: קובץ אמת שלא נסרק הופך לרמז בעצמו** | סגור · `scripts/knowledge/drift_scan.py` |

## Pointers

- Module declaration (governance gate): `gt-factory-os-production-brain`
  `docs/decisions/modules/sales-declaration.md` — **APPROVED (Tom, 2026-08-04)**;
  **Amendment A APPROVED (Tom, in writing, 2026-08-17)**. The earlier
  "PR #46 — DRAFT, awaiting Tom" pointer was stale and is corrected here.
- **Q4 existing-customer plan — v3 LANDED 2026-08-31, led by catalog expansion.**
  Tom's correction: switching a customer off MUZA is less likely than adding matcha or ube.
  So the plan measured **real 12-month penetration** from 3,872 Shopify orders instead of
  trusting the growth board's comparison-group model — which is circular on an
  under-penetrated category. Tea is **94%** penetrated; **matcha 48% and already GT's
  second-largest category at ₪423,949** against the board's ₪43,942 (×9.6). **74 accounts
  buy tea and no matcha, worth ₪351,270** priced at the median comparable buyer in the
  same revenue band; six of them are A-band, hold ₪202,860, and already sit in the
  joint-meeting lane. Target rises ₪147,644 → **₪262,661** run-rate, ₪212,492 gross.
  **MUZA is demoted to a second sentence** — a gate now enforces that it never opens a
  call with an account still buying tea, and it caught one that had slipped through.
  Only the **5 accounts that stopped buying tea as well** get a win-back conversation.
  New collateral: `matcha-business-case.md` (21 of 48 catalogue drinks are matcha or ube;
  a ₪590 bag is 277 serves and ₪7,756 on the menu — ×13.1 against tea's ×5.8).
  Builder: `q4_plan_v3.py`, 15/15 gates. Penetration: `q4_penetration.py`.
  Opened U-030 (80 matcha bags for 74 target accounts) and U-031 (`GT-MAT-KIT` contents undocumented).
- ~~Q4 existing-customer plan — v2, 2026-08-31~~ **superseded by v3 the same day** (v1 of the same day superseded after Tom's
  corrections). **Three sales channels**, not a flat partner split: T1 joint Alex+Avi meetings (15
  accounts, 51% of revenue, ₪86,465 of the target) · T2 Avi solo calls (22) · T3 Tom WhatsApp (116).
  755 dated tasks over 84 working days; target ₪147,644 run-rate / ₪119,444 gross profit.
  **Product gate:** 37 opportunity lines in 35 accounts (₪168,418) had been pointing at Nonomimi's
  and Babka's own private-label SKUs — fixed in the SKU *and* in the script copy.
  Dashboard: `https://claude.ai/code/artifact/9267cc69-a432-43d5-8e18-94b6057db483`.
  Plan: `evidence/2026-08-31-q4-plan.md` · assignment: `evidence/2026-08-31-q4-assignment.md` ·
  task list: `evidence/2026-08-31-q4-daily-plan.csv` · collateral: `evidence/2026-08-31-q4-collateral/` ·
  method: `recipes/q4-scoreboard.md` · runtime: `gt-factory-os/scripts/sales-report/q4_scoreboard.py` ·
  screen: `https://claude.ai/code/artifact/39c9dc45-7e50-487e-8013-f255f1b84de7`.
  Source masterprompt + execution record: `gt-factory-os-production-brain/docs/plans/2026-08-31-existing-customers-q4-masterprompt.md`.
  **Nothing was sent to any customer** — `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` stays `false`.
  Open against it: U-022 (blocking, ₪192,147), U-023, U-024, U-025, U-026.
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
