# Recipe — דוח המכירות (fact-table rebuild)

> השיטה בלבד. המספרים חיים ב-`evidence/2026-08-24-sales-report.md` (וכל snapshot עתידי).
> Scripts (runtime): `gt-factory-os/scripts/sales-report/` — לעולם לא בריפו הזה.
> נבנה 2026-08-24; טקסונומיה ועוגנים אושרו ע"י תום באותו יום (`user_confirmed`).

## עקרון

טבלת עובדות **אחת**: `חודש × לקוח × SKU → {units, revenue_exvat, orders}`.
כל תצוגה = rollup שלה. מספר יכול להיווצר רק בדרך אחת.

## בסיס כספי (נעול)

- שורת מוצר = `discountedTotalSet.shopMoney` = המחיר השמור בשופיפיי = **ללא מע"מ** (תום 2026-08-05).
- שופיפיי מוגדרת (בטעות) `taxesIncluded=true @17%` ⇒ עמודות המס/net/gross של ShopifyQL מחסירות "מס" פיקטיבי `17/117`. **אסורות לשימוש.**
- העוגן הבלתי-תלוי: **`total_sales`** של ShopifyQL = בסיס המחיר-השמור (אושר תום 2026-08-24).
- `customer.amountSpent` ו-`average_order_value` של ShopifyQL — אסורים (אנומליות מתועדות). AOV = מחזור ÷ הזמנות מהטבלה.

## משיכה

1. Bulk Operation אחת (GraphQL `bulkOperationRunQuery`) על `orders(query:"created_at:>=<start-1d>")`
   עם: order header (test, cancelledAt, source, taxes/shipping/subtotal/discounts sets), customer{id,displayName,tags},
   lineItems{sku,quantity,title,discounted/originalTotalSet,discountAllocations,product,variant}, refunds{createdAt,totalRefundedSet}.
2. Poll עד `COMPLETED`, הורדת ה-JSONL לדיסק. **שומרים את הגולמי; לא מושכים פעמיים.**
3. שיוך חודש לפי **Asia/Jerusalem** (לא UTC) — אחרת ספירת ההזמנות לא תתאים ל-ShopifyQL.

## כללי הכללה

| מקרה | כלל |
|---|---|
| `test:true` | החרגה |
| `cancelledAt≠null` | החרגה מהמחזור; נספר ומדווח בנפרד (לפי חודש יצירה + חודש ביטול) |
| Draft שלא הושלם | לא הזמנה (לא מגיע מה-API) |
| שורה בלי SKU | דלי `(ללא SKU)` גלוי, עם הכותרות |
| Refunds | ברמת חודש, שורת התאמה (בפועל: 0 בכל החלון — GT מבטלת, לא מחזירה) |
| משלוח | מחוץ להכנסות מוצר (בפועל 0) |

## טקסונומיה (קפואה — שינוי רק עם תום)

1. `type` — join `sku` → `gt-factory-os-production-brain/docs/pricing/2026-08-05_shopify_products_exvat.tsv`.
2. `משפחה` — מהכותרת (המותג האנגלי המצוטט קיים גם בכותרות עבריות: `"FRESH"` וכו').
3. `סוכר` — `Sugar-Free` בכותרת (תה בלבד).
4. `קטגוריה` — פרקי `catalog-truth.md` + `תפעולי/אריזות` + `משלוח/פיקדונות/התחשבנות`.
5. SKU היסטורי ∉ TSV — טבלת חריגים גלויה; סיווג אוטומטי מאושר (Maruei→MATCHA, טפיוקה ישנה→BUBBLES, 0.3ל→תמציות, ערק→ARAK…). **אסור להשליך/להחביא.**
6. רשת — תגיות: isrotel, nonomimi, minatomei, minasarona, r2m, nord, bneikikar, guta, unimarket,
   elitaofek, wix, fattal, mandarin, kampai, nabi, leonie, matok, distributor
   + שיוכים ידניים מאושרים (2026-08-24): נונו ג'ירף מודיעין→נונומימי · בבקה הרצליה+הבימה→בבקה · מוזה קוקטיילים+MUZA COCKTAILS→"MUZA (מוזה)" (איחוד תצוגה; U-010 נשאר פתוח).
   תגיות `*-chain` מהשטח — **לא** אומצו (תום, 2026-08-24). לקוח בלי תגית = "ללא רשת", לא ניחוש.
7. מדרג תמחור — תגיות גולמיות בלבד (U-003).

## חמשת שערי הנכונות (חובה לפני פרסום)

1. **התאמה חודשית** — `מחיר-שמור − הנחות − היפוכים` מול `total_sales` פר חודש; חלון מלא ≤0.5%.
   היפוכים = ביטולים לפי חודש-ביטול (+עריכות הזמנה כשארית מוסברת).
2. **התאמת הזמנות** — ספירה חודשית **כולל מבוטלות** מול `FROM sales SHOW orders TIMESERIES month` — התאמה מדויקת.
3. **כיסוי** — כל SKU ממופה או בדלי גלוי; לדווח `N/N + ₪ חריגים`.
4. **הצלבה** — מול העוגנים של האבחון/ה-evidence הקודם; פער מהותי ⇒ למצוא מי טועה לפני שממשיכים.
5. **שפיות ידנית** — 3 הזמנות אקראיות, שליפה חוזרת ישירה מה-API, השוואה שורה-שורה. `3/3` או עצירה.

## תוצרים ולוחות זמנים (תום, 2026-08-25)

| תוצר | קצב | מי מריץ | יעד |
|---|---|---|---|
| Artifact הדוח | **שבועי**, רביעי 07:30 | `weekly-sales-report` | אותו URL קבוע |
| `מכירות MM.YY.xlsx` | **חודשי**, 1 לחודש 08:00 | `monthly-sales-excel` | דרופבוקס `/Business/Sales` |

- שניהם על אותה טבלת עובדות ואותם 5 שערים. האקסל מכסה ינואר→החודש שנסגר; ב-1 לחודש
  הוא כבר לא חלקי. שם הקובץ = החודש שנסגר (1/9/2026 ⇒ `מכירות 08.26.xlsx`).
- עמוד שער-אישור נפרד; snapshot ל-`evidence/` בכל ריצה מהותית. CURRENT_STATE מצביע על האחרון.
- הרצה מחדש: `build_facts.py → build_gate_page.py (בשינוי טקסונומיה — שער תום!) →
  build_report.py → Artifact` · לאקסל: `build_facts.py → build_excel.py → upload_dropbox.py`.

## מלכודות שנמדדו (2026-08-25)

- **שאילתת ה-bulk נעולה** ב-`gt-factory-os/scripts/sales-report/orders_bulk.graphql`. בלי
  `id` על `lineItems`, שורות ה-JSONL מגיעות בלי gid, נופלות ל-`__UNKNOWN__`, ו-`fact_rows`
  יוצא **0 בלי שגיאה** — אקסל ריק שנראה תקין. `build_excel.py` חוסם את זה מאז.
- **ShopifyQL רק דרך ה-MCP.** ל-`shopifyqlQuery` של ה-Admin API ב-`2025-07` אין
  `sales_reversals`; והמספרים חוזרים כמחרוזות — להמיר לפני `build_facts.py`.
