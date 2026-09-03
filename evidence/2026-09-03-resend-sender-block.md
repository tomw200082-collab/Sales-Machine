# ראיה — מה בדיוק חוסם את דואר הלידים

> **תאריך:** 2026-09-03 · **דירוג:** `system_verified`
> **שיטה:** קריאת `sales_core.poll_run` · חיפוש DNS דרך DoH · קריאת `health` של הפונקציה החיה
> נכון **ליום הזה בלבד**. מספרים חיים ⊥ נטענים כעובדה — לחשב מחדש עם השאילתה שלמטה.

## 1 · מה קורה כל בוקר

`sales_core.poll_run`, מסלול `reminders`, שעון ישראל:

| ריצה | ok | due | sent | שגיאה |
|---|---|---|---|---|
| 2026-09-01 06:00 | false | 10 | 1 | `resend 403 — You can only send testing emails to your own email address (tom@gteveryday.com)` |
| 2026-09-02 06:00 | false | 12 | 1 | זהה |
| 2026-09-03 06:00 | false | 14 | 1 | זהה |

**33 לידים בשלושה ימים** נושאים `reminder_sent` על דואר שנדחה. רק העותק של תום יוצא.
ריצת 07:00 מחזירה `due: 0` — ⊥ תקלה: כל הלידים כבר "נתבעו" ב-06:00 ומנגנון מניעת-הכפילות עובד כמתוכנן.

```sql
-- לחישוב מחדש
select started_at at time zone 'Asia/Jerusalem' as il, ok,
       summary->>'due' as due, summary->>'sent' as sent, left(error,120) as err
from sales_core.poll_run where route in ('reminders','ingest')
order by started_at desc limit 20;
```

## 2 · למה — שתי עובדות, ⊥ אחת

**א. השולח.** `supabase/functions/sales-leads-poll/index.ts:60` → `DEFAULT_FROM = 'GT Leads <onboarding@resend.dev>'`,
בשימוש בשורה 277 אלא אם `RESEND_FROM` מוגדר. זה **השולח המשותף של Resend**, שמוסר **רק לכתובת שבבעלות חשבון ה-Resend**.

**ב. הדומיין — ותיקון.** הגרסה הראשונה של הקובץ הזה אמרה "אף דומיין ⊥ מאומת ב-Resend". זה נבדק על `gteveryday.com` **בלבד** והוכלל ממנו. תום שאל על הדומיין השני, ושם התמונה הפוכה:

| דומיין | `resend._domainkey` | `send.<d>` MX | `send.<d>` SPF |
|---|---|---|---|
| `greentea-everyday.com` | ✅ `p=MIGfMA0GCSqGSIb3…` | ✅ `feedback-smtp.ap-northeast-1.amazonses.com` | ✅ `v=spf1 include:amazonses.com ~all` |
| `gteveryday.com` | ⊥ | ⊥ | ⊥ |
| `greenteaeveryday.com` (בלי מקף) | הדומיין עצמו ⊥ קיים (NXDOMAIN) | — | — |

∴ **`greentea-everyday.com` מוגדר ב-Resend במלואו.** נותרה עובדה א' בלבד: ה-`from` מצביע על השולח המשותף. **∴ שלב אחד: `RESEND_FROM`.** DMARC ⊥ קיים על הדומיין — Resend ⊥ דורש אותו.

## 3 · מה שה-DNS מראה

| רשומה | ערך |
|---|---|
| NS | `ns27.domaincontrol.com` · `ns28.domaincontrol.com` → **GoDaddy** |
| MX | `aspmx.l.google.com` + alt1–4 → Google Workspace |
| TXT | `google-site-verification=…` · `v=spf1 include:dc-aa8e722993._spfm.gteveryday.com include:40143933.spf02.hubspotemail.net ~all` |
| `resend._domainkey` | ריק |

**רלוונטי רק אילו היינו מקימים את `gteveryday.com` — ⊥ נדרש, כי הדומיין השני כבר מוגדר.** אילו כן: תת-דומיין, ⊥ השורש. ה-SPF בשורש כבר נושא שני `include:`; שלישי מקרב אותו לתקרת 10 ה-lookups של SPF — וכשהיא נחצית, דואר Google Workspace של כל הדומיין מתחיל להיכשל. `send.gteveryday.com` ⊥ נוגע בו.

## 4 · מה תוקן כאן — והמגבלה שלו

`sales-leads-poll` v20 (נפרס 2026-09-03 דרך `deploy-edge-function.yml`) מדווח ב-`health`:

```json
{ "secrets": { "RESEND_FROM": false, … }, "sends_from_shared_sender": true }
```

זו הקריאה החיה מרגע הפריסה — ⊥ הסקה. **⊥ שינה את השליחה בכלום**: זה עושה את התקלה קריאה, ⊥ מתקן אותה.

**לפני הפריסה נבדק drift:** גרסה 19 ACTIVE, כל 8 הקבצים זהים בייט-לבייט ל-`origin/main`. זו הבדיקה ש-U-024 אומר שאיש ⊥ מריץ.

## 5 · מה נשאר, לפי הסדר

1. Supabase → `sales-leads-poll` → Secrets → `RESEND_FROM = GT Leads <leads@greentea-everyday.com>`
2. הוכחה: `health` יחזיר `RESEND_FROM: true` ו-`sends_from_shared_sender: false`. ואז ריצת 06:00 הבאה.

זהו. ⊥ GoDaddy, ⊥ רשומות DNS חדשות, ⊥ פריסה.
**מה שה-DNS ⊥ מוכיח:** את מצב ה-"verified" בלוח הבקרה של Resend. הרשומות במקום — זה מה שהאימות בודק — אבל הקריאה הסמכותית היא במסך של Resend ו⊥ נקראה מכאן.
**ותשומת לב אחת:** תשובות לכתובת הזאת נוחתות ב-Google Workspace של `greentea-everyday.com`. צריך תיבה או alias אם מישהו אי-פעם ישיב.

⊥ מטופל כאן: `reminder_sent` נכתב לפני השליחה (GAP-033) — 33 השורות נשארות, `lead_event` הוא append-only.
