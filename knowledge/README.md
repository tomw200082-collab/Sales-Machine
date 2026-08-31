# `knowledge/` — המאגר שסוכן קורא ממנו כדי לענות ללקוח

> **המאגר הזה הוא האמת. הארטיפקט הוא תצוגה שלו.**
> עד 2026-08-31 היה הפוך: הידע חי בעמוד HTML, ולכן ⊥ ניתן היה לצטט אותו,
> להחתים עליו תאריך, לדרג אותו או להוכיח איזו גרסה סוכן השתמש בה.

## סדר הקריאה של סוכן

```
1. boundaries/refusals.yaml     ← קודם. סירוב גובר על תשובה, תמיד.
2. answers/answer-bank.yaml     ← שורה מאושרת? ענה כלשונה.
3. products/catalog.yaml        ← מחיר/אריזה/עלות למנה. customer_facing: false ⇒ ⊥ להציע.
4. drinks/catalog.yaml          ← עלות/מחיר/רווח לכל אחד מ-48 המשקאות.
5. claims/public-claims.yaml    ← לפני שאומרים טענה. authority: unsourced ⇒ ⊥ אומרים.
6. segments/                    ← מי הלקוח, מה סוגר אותו, מה שולחים ומתי.
   ⊥ נמצאה תשובה בשום מקום ⇒ boundaries#unmatched_default ⇒ מעבירים לאלכסנדר.
```

**⊥ להסיק.** `Sales-Machine/CLAUDE.md` כלל 1: inferred ⊥ policy.
שורת `העברה לאלכסנדר` היא תשובה תקינה. ניחוש הוא ⊥.

## מה נבדק, ואיך

```bash
cd gt-factory-os-production-brain
python3 scripts/knowledge/reconcile.py           # book + cards
python3 scripts/knowledge/reconcile.py cards     # השער: חייב 0 שורות
python3 scripts/knowledge/reconcile.py --selftest
```

הבודק מצליב כל מחיר לכל SKU מול `docs/pricing/2026-08-05_shopify_products_exvat.tsv`,
כל עלות/מחיר/רווח מול `.claude/skills/drinks-pricelist/drinks_final_figures.json`
(2026-08-27 — **הרשות היחידה**), וכל מוצר מול `docs/warehouses/catalog-truth.md`.
כל כרטיס חייב `source` · `date` · `authority` · `freshness` ורישום ב-`registry.yaml`.

`docs/pricing/2026-08-05_drinks_final_figures.json` הוא **גרסה מוחלפת**. קריאה ממנו
מייצרת עמוד שלם של סתירות שאינן קיימות.

## מה ⊥ נכנס לכאן

מספרי לקוחות, מחזור, מי ישן, מלאי — **אמת מהירה**. כלל 2: מתכון + תצלום מתוארך.
`recipes/customer-count.md` · `recipes/sales-report.md` · `evidence/`.
כתיבת מספר לקוחות לתוך כרטיס תהיה נכונה בערך לשבוע.

## הגיליון של מערכת הלידים

`answers/answer-bank.yaml` הוא **המקור היחיד**. הגיליון נבנה ממנו, ⊥ להפך.
שני בנקי תשובות = כישלון D3.

## מה חסר, ולמה

`Sales-Machine/CURRENT_STATE.md` §UNRESOLVED — הרשימה היחידה.
ארבע החלטות מסחריות (חבילות, זמן אספקה, מדרגות הנחה, התחייבות) ⊥ נסגרות במחקר.
רק טום סוגר אותן. עד אז — הכרטיסים מעבירים לאלכסנדר, והמכונה עובדת ביום שהן נוחתות.
