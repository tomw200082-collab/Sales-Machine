# GT Pulse A — Sales Activity and Task Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** סוכן פותח ליד מהמייל, מתעד קשר מהותי עם פעולה ומועד, ורואה משימות אמיתיות מהטריגרים המאומתים בתור האישי שלו; המתנה ללקוח חוסמת הודעות wake-up.

**Architecture:** Sales-Machine מחזיק את המפרט בלבד. gt-factory-os מוסיף משימות ופקודת תיעוד אטומית ל-sales_core, קורא אותן דרך Fastify ומגן על שולח ה-wake-up. gt-factory-os-portal מעביר את הקישור העמוק דרך הזדהות, מציג Today וליד מתוך ה-API, ושומר טיוטת תיעוד מקומית עד הצלחה.

**Tech Stack:** PostgreSQL 17/pgTAP ב-Supabase; Fastify, Kysely, Zod, Node test ו-Vitest; Next.js 15, React 18, TanStack Query, Vitest ו-Playwright. אין תלות מוצר חדשה.

**Spec:** docs/superpowers/specs/2026-09-29-sales-activity-task-loop-design.md; מסמך האב docs/superpowers/specs/2026-09-29-gt-pulse-crm-program-design.md.

**Status:** התוכנית אושרה על ידי טום ב־2026-09-29 לביצוע Native בסשן חדש. אין באישור זה הפעלה של פניות אוטומטיות ללקוחות; מיזוג ופריסה כפופים לשערי הריפואים ולהוכחת runtime.

## Global Constraints

- הבסיס שנבדק: gt-factory-os main ב-0e3c6fb49f82e9f9bddf38e478d78c17f2173878; gt-factory-os-portal main ב-5e45b2d91cc8938ec1945925e46f481b9146c404. לקבע SHA מחדש עם תחילת ביצוע, כי שניהם עשויים להשתנות.
- לפני קובץ מיגרציה: למנות db/migrations/ מיד לפני ומיד אחרי; 0362 הוא המספר הבא רק בבסיס הנבדק. אם המספר נתפס, לעצור ולעדכן את התוכנית, בהתאם ל-gt-factory-os/CLAUDE.md. בדיקות רק מול Postgres מקומי זמני; אין להשתמש בנתוני לקוח חיים כ-fixture.
- הפורטל פעיל כרגע תחת tranche 184 שאינו קשור למכירות. אין לערוך קוד פורטל לפני סיום/שחרורו ויצירת tranche מכירות חדש עם manifest מדויק ב-docs/portal-os/tranches/ וכניסה ב-registry.md. לא לערוך שום קובץ פורטל מחוץ למניפסט.
- לפני כתיבת פורטל לקרוא גם את gt-factory-os-production-brain/{CLAUDE.md,CURRENT_STATE.md,EXECUTION_POLICY.md,ACTIVE_NOW.md,AI_BRAIN_ROUTER.md,docs/decisions/modules/sales-declaration.md} ואת .claude/state/{runtime_ready,active_mode}.json. אות RUNTIME_READY לטופס יחיד אינו אישור לעריכת מסדרון מכירות רב־מסכי. יש להסדיר Mode B דרך amendment תחום לפי EXECUTION_POLICY.md §W2 modes, עם תוכנית מאושרת, רשימות מותר/אסור, שער יציאה ותנאי פקיעה; לא להסיק שה־tranche לבדו מספיק. שינוי auth ו-copy כפוף לשערי האישור שם.
- אין שינוי ב-factory core, מלאי, הזמנות Shopify או קו ההזמנות של לקוחות קיימים. אין הפעלת SALES_CUSTOMER_OUTREACH_WRITE_ENABLED, שליחת הודעת לקוח חדשה, שינוי טקסט מסע WhatsApp או AI. מיילי ההתראה נשארים לעובדי GT בלבד.
- ליד = הזדמנות מול עסק B2B; אין ישות של לקוח הקצה של בית הקפה. רשומות עסק והזמנות מלאות, שימור והרחבה הם B/C ולא תנאי למסירת A.
- אחרי שיחה שנענתה, WhatsApp דו-כיווני מאומת או מענה מהותי במייל: הערה באורך ≥5 אחרי trim + פעולה עיקרית ומועד, או ״ממתין ללקוח״ + מועד בדיקה. ״לא ענה״ ו״נשלח WhatsApp״ נשמרים במהירות בלי הערת חובה. נסיון tel:/wa.me אינו תוצאה.
- מקור אמת למשימות הוא השרת; lead_event נשאר append-only. כל משימה נושאת יעד, מקור, סוג, סיבה, בעלים או needs_assignment, מועד ומצב. retry ושינוי שיוך אינם משכפלים; request_id עם תוכן שונה נדחה. הסוכן מאשר תיעוד ומשימות, ואין קישור מייל שמאפשר לעקוף את הליד. ליד ללא דרך קשר מקבל בירור פרטים נפרד אצל מנהל, ואחרי תיקון מתועד חוזר למסלול קשר רגיל.
- הפורטל עברית RTL scoped ל-(sales); 320–430px ללא גלילת עמוד אופקית, מקלדת בטוחה, reduced motion, מצבי חסר/שגיאה. אין קישוט שמציג עובדה שלא נרשמה.
- בחלק ה-Knowledge-book של Sales-Machine/CURRENT_STATE.md שורת U-016 (→ אלכס §4) היא מדיניות שירות פתוחה; באותו קובץ U-016 אחר מתייחס ל-Meta. לא להסיק מדיניות שירות ממספר לבדו.
- מסד הנתונים הוא schema פרטי; Fastify מאמת Session וגוזר הרשאות ובעלים מ-private_core.app_users, לא מתוכן הבקשה. לא להעניק anon/authenticated גישה ל-sales_core; לבדוק RLS/advisors ומענקי EXECUTE לאחר DDL. משתמש sales_rep אינו יכול לבקש תור של עמית על ידי assignee query.
- לפרוס הרחבה לפני צמצום: schema ו-API החדשים לפני הפורטל; מניעת המסלול הישן של answered_progressing רק אחרי בדיקת פורטל חדש. משימות פנימיות אינן מפעילות customer outreach. כל release כולל חזרה לאחור תואמת נתונים, dry-run ועדות runtime.

## Review Focus

1. מייל נפתח ללא session עם ?lead=<uuid> → אחרי login מגיעים לאותו ליד; next חיצוני או //evil נדחה. בדיקות Task 1.
2. לחיצה כפולה, timeout או webhook חוזר לאותו מקור → הערה/תוצאה/משימה אחת; בדיקות Tasks 3–6.
3. ליד לא משויך או שיוך שזז בזמן התגובה → אינו מופיע בשלושה תורים אישיים ואינו הולך לאיבוד; בדיקות Tasks 3, 6, 7.
4. opt-out/תשובה/הזמנה/״ממתין ללקוח״ מתחרים ב-wake שנמצא רגע לפני send → לא נשלחת הודעה אחרי commit של מצב העצירה; בדיקות Task 5.
5. iPhone עם מקלדת פתוחה, רענון, רשת שנפלה, RTL ו-320px → הטיוטה נשמרת, שמור נגיש, אין הצלחת שווא או גלילה אופקית; בדיקות Tasks 8–9.

## File Map and Interfaces

| בעלות | קבצים | אחריות |
|---|---|---|
| Backend SQL | db/migrations/0362_sales_activity_tasks.sql; db/tests/0362_sales_activity_tasks.test.sql | sales_core.task, task_event, activity_request, lead_wait, event routing, owner propagation, atomic capture, contact correction |
| Backend API | api/src/sales/schemas.ts, mutations_handler.ts, queries_handler.ts, route.ts; api/test/sales_workspace_tasks.test.ts | POST activity, GET tasks, POST task completion, PATCH contact, auth-bound reads/writes |
| Backend journey/email | api/src/order-intake/sales/wake.ts; api/src/order-intake/{store,worker}.ts (raw event boundary); api/src/order-intake/sales/__tests__/{wake,lead_db}.test.ts; api/src/order-intake/__tests__/worker.test.ts; supabase/functions/sales-leads-poll/_lib/email.ts; api/test/sales_leads_poll_alerts.test.ts | wake guard including inbound event log, verified source triggers, staff email CTA |
| Portal auth/proxy | src/middleware.ts; src/lib/auth/safe-redirect.ts; src/app/(auth)/login/page.tsx; src/app/auth/callback/page.tsx; src/app/api/sales/tasks/route.ts; src/app/api/sales/tasks/[task_id]/complete/route.ts; src/app/api/sales/leads/[lead_id]/{activity,contact}/route.ts | safe deep link, thin API proxy |
| Portal UI | src/app/(sales)/_lib/{types,api,labels,useOutcomeCapture,useQueueScope}.ts; _components/{OutcomeSheet,TodayQueue,TodayCard,LeadDrawer}.tsx; sales/{today,leads,attention}/page.tsx; sales-tokens.css; new _lib/activityDraft.ts; new _components/{TaskCard,LeadJourneyRail}.tsx | source-backed task cards and fast, durable mobile capture from every existing outcome entrypoint |
| Portal verification | tests/unit/middleware.test.ts; tests/unit/sales/{outcome-sheet,today-queue,activity-draft}.test.tsx; tests/e2e/{sales-outcome-integrity,sales-attention,sales-visual-a11y,mobile-sales-today}.spec.ts; new tests/e2e/sales-email-to-task.spec.ts | real user journey and responsive gate |
| Documentation | New portal tranche manifest and registry entry; Sales-Machine/CURRENT_STATE.md only after observed release | scoped execution and dated evidence |

One plan spans two runtime repos because the delivered contact loop crosses their API. Commit independently in each repo. No runtime code is added to Sales-Machine. If the backend SHA or migration slot advances, re-map names and tests before touching code.

**Native Superpowers bookkeeping across repositories:** Keep one execution index keyed to this approved plan, with the backend and portal base/head SHAs and links to their distinct ledgers. Run `executing-plans/scripts/task-start` and `task-done` from the **runtime repository that owns the task**, passing the same absolute path to this plan: backend Tasks 1 and 3–6; portal Tasks 2 and 7–9. Each `sdd-workspace` is relative to the current runtime repository, and each task's BASE..HEAD must be a range in that repository. Generate two whole-branch review packages, one per runtime repository. Never make a combined cross-repository git range or record a portal task as complete in the backend ledger. If portal governance blocks Task 2, mark it deferred (not complete), execute backend Tasks 3–6, then resume Task 2 before Tasks 7–9; record this order as a ruling in the execution index and both ledgers. Preserve ledgers through compaction; do not treat a deferred task as delivered.

---

### Task 1: Staff email opens the lead

**Files:**
- Modify: gt-factory-os/supabase/functions/sales-leads-poll/_lib/email.ts
- Modify: gt-factory-os/api/test/sales_leads_poll_alerts.test.ts

**Interfaces:**
- Consumes: buildLeadAlert(LeadAlertInput) and buildReminderDigest(ReminderDigestInput).
- Produces: the existing /sales/leads?lead=<uuid> deep link as the primary CTA; no tel:, wa.me or mailto: anchor in lead alert/digest.

- [ ] **Step 1: Write the failing test.** Replace S16, which currently asserts direct tel:/wa.me/mailto: anchors, and replace the digest test that expects tel:. Use the existing base and dueCallback fixtures:
~~~ts
const alert = buildLeadAlert(base);
assert.match(alert.html, />פתח את הליד</);
assert.match(alert.html, /\/sales\/leads\?lead=11111111-2222-3333-4444-555555555555/);
assert.doesNotMatch(alert.html, /href="(?:tel:|mailto:|https:\/\/wa\.me\/)/);
assert.ok(!alert.html.includes('+972526380055'));
const digest = buildReminderDigest({
  to: 'erik@gteveryday.com', name: 'אריק',
  now: new Date('2026-08-25T03:00:00Z'),
  due: [dueCallback()], portal_base_url: 'https://portal.example',
});
assert.doesNotMatch(digest.html, /href="(?:tel:|mailto:|https:\/\/wa\.me\/)/);
assert.ok(!digest.html.includes('+972521234567'));
~~~
Preserve no-lead-recipient, phone-less and escaping assertions; update their expected display text only where the link was intentionally removed.

- [ ] **Step 2: Run red.** From gt-factory-os/api: npx tsx --test test/sales_leads_poll_alerts.test.ts; expected the direct-link assertion to fail.

- [ ] **Step 3: Implement the mail hierarchy.** Render button(esc(link), 'פתח את הליד', '#ffffff', '#111827', '#d7dbe0') before details; remove the actions table's direct channel anchors and phone/email contact strings from staff mail, because mobile mail clients can auto-link plain numbers. In buildReminderDigest, make each due row open /sales/leads?lead=<encoded id> and retain the Today button. Keep the contextual name/source and a short cue that contact details are in the lead. Never show an unverified snapshot amount as a money claim. Example link derivation:
~~~ts
const base = input.portal_base_url.replace(/\/+$/, '');
const leadHref = (leadId: string) =>
  base + '/sales/leads?lead=' + encodeURIComponent(leadId);
~~~

- [ ] **Step 4: Run green.** Run api/test/sales_leads_poll_alerts.test.ts with npx tsx --test and the existing email/recipient tests; inspect HTML/text for phone-less leads and a reminder with two leads.

- [ ] **Step 5: Commit in gt-factory-os.** Stage only the two email files and commit "feat(sales): make lead link primary in staff mail".

### Task 2: Deep link survives authentication and portal tranche opens

**Files:**
- Create: gt-factory-os-portal/docs/portal-os/tranches/185-sales-activity-task-loop.md (185 הוא המספר הבא בבסיס הנבדק; לבדוק שוב לפני יצירה)
- Modify: gt-factory-os-portal/docs/portal-os/tranches/_active.txt, docs/portal-os/registry.md
- Create: gt-factory-os-portal/src/lib/auth/safe-redirect.ts
- Modify: gt-factory-os-portal/src/middleware.ts, src/app/(auth)/login/page.tsx, src/app/auth/callback/page.tsx
- Test: gt-factory-os-portal/tests/unit/middleware.test.ts; tests/e2e/sales-leads.spec.ts

**Interfaces:**
- Consumes: /sales/leads?lead=<uuid> generated in Task 1.
- Produces: a same-origin relative redirectTo including query; callback accepts only one leading slash and rejects // or protocol URLs.

- [ ] **Step 1: Before any portal edit, check brain governance and complete/clear active tranche 184.** Read the brain boot/policy/router/module declaration and the current runtime_ready/active_mode JSON. This is a pan-form sales corridor, not a single form: record a bounded Mode B amendment citing this approved plan, enumerating exact allowed paths and forbidden factory/customer flows, the per-tranche typecheck/build/lint/smoke/role-matrix exit and expiry after this corridor closes, plus the required Tom authorization under EXECUTION_POLICY.md §W2 modes. If the 2026-09-29 plan/Native approval does not satisfy the governor's written-authorization check, complete backend independent work and present the concrete amendment for approval before portal authoring. Verify backend readiness before consuming new API contracts. Then create a new sales tranche manifest listing every portal path in the File Map and tests; enter its exact path in registry.md and number in _active.txt. A tranche cannot inherit 184's catalogue manifest.

- [ ] **Step 2: Write the failing auth tests.**
~~~ts
const res = await middleware(new NextRequest('https://portal.example/sales/leads?lead=11111111-2222-3333-4444-555555555555'));
const login = new URL(res.headers.get('location')!);
expect(login.searchParams.get('redirectTo')).toBe('/sales/leads?lead=11111111-2222-3333-4444-555555555555');
~~~
Add callback/login tests that next=https://evil.example and next=//evil.example resolve to /apps; a valid local /sales/leads?lead=<uuid> stays intact.

- [ ] **Step 3: Run red.** npm test -- tests/unit/middleware.test.ts; expected redirectTo to equal /sales/leads without its query.

- [ ] **Step 4: Implement safe redirect.**
~~~ts
const target = request.nextUrl.pathname + request.nextUrl.search;
loginUrl.pathname = '/login';
loginUrl.search = '';
loginUrl.searchParams.set('redirectTo', target);
~~~
At both login and callback, normalize next/redirectTo with src/lib/auth/safe-redirect.ts:
~~~ts
export function safeRedirectTarget(raw: string | null): string {
  if (!raw || !raw.startsWith('/') || raw.startsWith('//') ||
      raw.includes('\\') || /[\x00-\x1f\x7f]/.test(raw) ||
      /%(?:2f|5c|0[0-9a-f]|1[0-9a-f]|7f)/i.test(raw)) return '/apps';
  return raw;
}
~~~
Do not turn a user-provided absolute URL into window.location.href/router.replace.

- [ ] **Step 5: Run green and commit portal-only.** Unit auth tests, a browser login/deep-link route test, typecheck, then stage only manifest/registry/auth files and commit.

### Task 3: Task source of truth, ownership and idempotent event routing

**Files:**
- Create: gt-factory-os/db/migrations/0362_sales_activity_tasks.sql
- Create: gt-factory-os/db/tests/0362_sales_activity_tasks.test.sql

**Interfaces:**
- Produces sales_core.task: id uuid, lead_id/org_id exclusive nullable targets, kind, title, due_at, status, owner_email nullable, source_kind/source_id/source_key, source_event_id nullable, created/updated/completed/cancelled actor/time/reason. owner_email NULL means needs_assignment; no anonymous owner.
- Produces sales_core.task_event: append-only task history with actor/action/payload/time. Unique task.source_key dedupes across event retries and includes lead UUID, source namespace and external source ID.

- [ ] **Step 1: List migrations and confirm 0362 is free. Write failing pgTAP cases** for a contactable new lead → one contact_first task due now; a lead with neither phone nor email → manager contact_resolution instead of a salesperson's impossible call; duplicate source_key → one task; the same external ID on different lead IDs → two tasks; no owner → owner_email NULL; reassignment → same task ID and new owner; viewer/authenticated cannot read sales_core.task. Start the fixture in a rollback transaction:
~~~sql
begin;
select plan(5);
insert into sales_core.org(id, display_name)
values ('aaaa1111-1111-1111-1111-111111111111', 'test B2B');
insert into sales_core.lead(id, org_id, source, external_id, phone_e164)
values ('bbbb2222-2222-2222-2222-222222222222',
        'aaaa1111-1111-1111-1111-111111111111', 'test', 'task-seed', '+972501234567');
insert into sales_core.lead_event(lead_id, event_type)
values ('bbbb2222-2222-2222-2222-222222222222', 'created');
select is((select count(*)::int from sales_core.task where lead_id='bbbb2222-2222-2222-2222-222222222222'), 1, 'one first-contact task');
select is((select kind from sales_core.task where lead_id='bbbb2222-2222-2222-2222-222222222222'), 'contact_first', 'first contact kind');
select is((select owner_email from sales_core.task where lead_id='bbbb2222-2222-2222-2222-222222222222'), null::text, 'unowned routes to manager');
update sales_core.lead set assignee='rep@example.com' where id='bbbb2222-2222-2222-2222-222222222222';
select is((select owner_email from sales_core.task where lead_id='bbbb2222-2222-2222-2222-222222222222'), 'rep@example.com', 'open task follows owner');
select is((select count(*)::int from sales_core.task where lead_id='bbbb2222-2222-2222-2222-222222222222'), 1, 'reassignment never clones task');
select * from finish();
rollback;
~~~

- [ ] **Step 2: Run red.** pg_prove -d "$DATABASE_URL" db/tests/0362_sales_activity_tasks.test.sql on throwaway local DB; expected relation sales_core.task missing.

- [ ] **Step 3: Implement focused schema and triggers.** Use CHECK ((lead_id is null) <> (org_id is null)), status in (open,done,cancelled), due_at NOT NULL, source_key UNIQUE; index (owner_email,due_at) WHERE status='open' and (lead_id,due_at). Source is an existing lead_event ID for A. Enable RLS with no public policies and revoke anon/authenticated/PUBLIC direct privileges on tables/functions; only server-side role may call functions. On lead_event insert, route created, note.kind=repeat_contact, button_tap.button_id=lj.more and draft_order; skip auto_message/outreach/alert_sent. created for no phone/email becomes contact_resolution with owner_email NULL and never a call card. On lead.assignee update, move all open tasks except contact_resolution; write a task_event. Illustrative idempotent insert:
~~~sql
insert into sales_core.task(lead_id, kind, title, due_at, owner_email,
                            source_kind, source_id, source_key, source_event_id)
select new.lead_id, 'reply', 'לחזור לליד', new.created_at, l.assignee,
       'lead_event', new.id::text,
       'button:more:' || new.lead_id::text || ':' || (new.payload->>'wamid'), new.id
from sales_core.lead l where l.id = new.lead_id
  and new.event_type = 'button_tap'
  and new.payload->>'button_id' = 'lj.more'
  and nullif(new.payload->>'wamid','') is not null
on conflict (source_key) do nothing;
~~~
For draft use lead id + idem_key; repeat use lead id + source + external_id; created use lead id. Unknown or malformed source stays an event for manager review, never becomes a fabricated contact task. Cancellation/restore logic is Task 5.

- [ ] **Step 4: Run green.** pgTAP proves target XOR, source uniqueness across leads, assignee move, null owner, uncontactable manager resolution, and no task on auto_message. Then run existing 0318/0322/0324/0360/0361 SQL tests against the same throwaway DB.

- [ ] **Step 5: Commit only migration and pgTAP test** in gt-factory-os. Do not apply to production as part of this task.

### Task 4: Atomic contact capture and explicit waiting state

**Files:**
- Modify: gt-factory-os/db/migrations/0362_sales_activity_tasks.sql
- Modify: gt-factory-os/db/tests/0362_sales_activity_tasks.test.sql

**Interfaces:**
- Produces sales_core.record_activity(p_lead_id uuid, p_request_id uuid, p_channel text, p_result text, p_note text, p_primary jsonb, p_extra jsonb, p_actor text) RETURNS jsonb. An activity_request row stores lead_id, canonical input hash and the completed result under a globally unique request_id.
- p_primary: {kind: call|whatsapp|email|other|wait_review, due_at: ISO string}; p_extra: up to five distinct additional actions of the same shape; quick no_answer/whatsapp_sent may pass p_primary null, and the server chooses next_business_touch(1/2). The result includes lead_id, note_event_id nullable, outcome_event_id and task_ids.
- Produces sales_core.lead_wait keyed by lead_id with review_at, source_event_id, actor, active; task due_at=review_at exists immediately, appears in Today when due.

- [ ] **Step 1: Write failing pgTAP cases.** Four trimmed chars, missing answered due date, extra action without due date, closed lead, and a repeat request ID must fail or return the same result without writes; the same request ID with a different note/lead must raise SALES_ACTIVITY_REQUEST_CONFLICT. One valid five-char answered action inserts note/outcome/task atomically; no_answer works without note and uses Israel business time. Example:
~~~sql
select throws_ok(
  $$select sales_core.record_activity(
    'bbbb2222-2222-2222-2222-222222222222',
    'cccc3333-3333-3333-3333-333333333333',
    'call', 'answered_progressing', ' ab ',
    '{"kind":"call","due_at":"2026-10-01T09:00:00+03:00"}'::jsonb,
    '[]'::jsonb, 'test')$$,
  'P0001', null, 'trimmed note shorter than five rejected');
~~~
Assert the event and task counts remain unchanged after the failure.

- [ ] **Step 2: Run red.** pg_prove on the new test; expected function absent.

- [ ] **Step 3: Implement one transaction at the DB boundary.** Acquire pg_advisory_xact_lock(hashtext('sales_core.activity:' || p_lead_id::text)) and then lock the lead; reject won/lost/opt-out and invalid channel/result, validate note for answered and all selected dates before inserting anything. Claim p_request_id in sales_core.activity_request; compare the lead and canonical input hash before returning its stored result on retry, and reject a reused ID for changed input. Insert the note event first, then update first_touch_at/status/next_touch_at, insert outcome with channel, result, request_id and note_event_id, then primary/additional tasks and a task_event for each. Each action gets source_key='activity:' || lead_id || ':' || request_id || ':' || ordinal (0 for primary), so five extras never collide. For waiting, upsert lead_wait active=true; other human result clears wait. For quick no_answer/whatsapp_sent derive next_business_touch and action kind without a note. Seed app_setting.activity_required as {"enabled":false}; amend the existing five-argument record_outcome to reject answered_progressing with SALES_ACTIVITY_REQUIRED only when that setting is true. Keep the old /outcome route compatible until Task 9's rollout gate.
~~~sql
if p_result = 'answered_progressing' and
   length(btrim(coalesce(p_note, ''))) < 5 then
  raise exception 'SALES_ACTIVITY_NOTE_TOO_SHORT' using errcode='P0001';
end if;
if p_result = 'answered_progressing' and
   (p_primary is null or nullif(p_primary->>'due_at','') is null) then
  raise exception 'SALES_ACTIVITY_ACTION_REQUIRED' using errcode='P0001';
end if;
~~~

- [ ] **Step 4: Run green.** pgTAP includes rollback-on-error, retry after simulated timeout, changed-payload conflict, five Unicode Hebrew characters, waiting task due, old /outcome compatibility while activity_required=false and server rejection of old answered_progressing while true. Count note/outcome/task once and primary + two distinct extras as three tasks.

- [ ] **Step 5: Commit focused SQL/test change** in gt-factory-os; still no prod DDL.

### Task 5: Route existing triggers and block wake-up at the send boundary

**Files:**
- Modify: gt-factory-os/db/migrations/0362_sales_activity_tasks.sql; db/tests/0362_sales_activity_tasks.test.sql
- Modify: gt-factory-os/api/src/order-intake/sales/wake.ts
- Inspect/modify the raw inbound boundary as needed: gt-factory-os/api/src/order-intake/store.ts, worker.ts
- Test: gt-factory-os/api/src/order-intake/sales/__tests__/wake.test.ts; api/src/order-intake/sales/__tests__/lead_db.test.ts; api/src/order-intake/__tests__/worker.test.ts

**Interfaces:**
- Consumes lead_event.created, note.kind=repeat_contact, button_tap.button_id=lj.more, draft_order.idem_key, status_change, opt_out, converted and lead_wait.active.
- Produces one open human task per actionable source; stop events cancel only irrelevant open tasks with a reason; a reply supersedes an open wait_review with reply. The wake store excludes and rechecks any active wait. The raw `order_intake.wa_event_log` inbound message/echo insertion for every affected lead participates in the same send-order lock.
- Produces sales_core.resolve_contact_gap(p_lead_id uuid, p_phone text, p_email text, p_provenance text, p_actor text) RETURNS jsonb for a manager to verify a formerly unreachable lead; no customer outreach is triggered.

- [ ] **Step 1: Write failing tests.** A duplicate lj.more wamid, repeated website/WA contact and duplicate draft idem_key yield one task each; lj.not_now and dry-run auto_message yield none. A reply cancels the wait_review and opens a reply task. lost cancels open lead-contact tasks, undo lost restores only tasks cancelled by that exact status event. An uncontactable lead with verified contact + provenance closes only its contact_resolution and opens a new contact_first; blank/malformed contact leaves it in manager queue. Add wake unit cases for active wait in forced and normal mode, a newer email answered outcome superseding an older call anchor. On disposable Postgres with two connections, pause at the send boundary: log inbound on the lead line and the order line, including two open leads sharing one phone. In both commit orders assert no send when the raw reply commits first; test waiting/opt-out/echo similarly. `worker.ts` logs through `store.logEvent` before dispatch; this raw write, not only a later lead_event, must be covered.

- [ ] **Step 2: Run red.** pg_prove on 0362 and npx vitest run api/src/order-intake/sales/__tests__/wake.test.ts; expected the new wait guard and task transitions to fail.

- [ ] **Step 3: Implement source mapping and stop precedence.** A repeat_contact with source whatsapp_ctwa/whatsapp_unattributed or website_form is a new human reply only if the lead is open and the source has external_id. lj.more maps to reply, draft_order maps to draft_review; neither a draft nor a button is won. For lost/opt-out/conversion, cancel inappropriate open tasks while preserving history; do not cancel a separate future service task. Use source_key built from lead id + external_id/wamid/idem_key, never only lead_event.id. Legacy first-contact tasks are superseded when a human contact is recorded. In the event trigger, the repeat path inserts once:
~~~sql
insert into sales_core.task(lead_id, kind, title, due_at, owner_email,
                            source_kind, source_id, source_key, source_event_id)
select new.lead_id, 'reply', 'לענות לפנייה חוזרת', new.created_at,
       l.assignee, 'lead_event', new.id::text,
       'repeat:' || new.lead_id::text || ':' || (new.payload->>'source') || ':' || (new.payload->>'external_id'), new.id
from sales_core.lead l
where l.id = new.lead_id and l.status in ('new','working')
  and new.event_type = 'note' and new.payload->>'kind' = 'repeat_contact'
  and new.payload->>'source' in ('whatsapp_ctwa','whatsapp_unattributed','website_form')
  and nullif(new.payload->>'external_id','') is not null
on conflict (source_key) do nothing;
~~~

- [ ] **Step 4: Implement contact resolution in the same migration.** resolve_contact_gap accepts only a previously contactless open lead, requires a normalized Israeli phone or plausible email plus a nonblank provenance (where staff confirmed the detail), and writes a note event with kind=contact_verified and the old/new values. It atomically closes contact_resolution with a task_event, creates contact_first with source_key='contact-resolved:' || lead_id || ':' || note_event_id, and retains a NULL owner if the lead is unassigned. Updating an existing phone/email by this narrow route is rejected. Its API is manager-only; no outbound message or call occurs. A later broader contact-edit flow can have its own design.

- [ ] **Step 5: Implement the wake guard with ordering.** Extend WakeCandidate with waitingForCustomer; decideWake refuses it before any slot or force decision. createWakeStore.candidates reads sales_core.lead_wait.active; claim rechecks it. A WakeStore.withLeadLock method holds the per-lead session advisory lock while reloading the candidate, claiming and calling line.send; record_activity, opt_out_phone, conversion/status changes and relevant lead_event inserts acquire the matching transaction advisory lock before changing their stop state. Also coordinate the **raw** `order_intake.wa_event_log` insertion in `store.logEvent` for inbound message/echo: it is committed before `worker.ts` dispatch, and wake reads this table directly. Use one scoped DB boundary (a selective insert trigger or an explicit transactional store path) that resolves every open lead on the normalized phone across both lines and acquires the identical per-lead lock for IDs in sorted order **before** inserting. Do not wait for later lead_event routing; test both commit orders with two connections. Acquire before mutating the lead, in the same order for every writer (including legacy record_outcome while accepted), avoiding lead-row/advisory-lock inversion. For phone-wide opt-out, lock affected lead IDs in sorted order before updates. A committed stop precedes or follows the send under one order. A failed send releases the lock in finally. Email outcomes carry channel=email and cannot create a new wake anchor. Example pure check:
~~~ts
if (c.waitingForCustomer) return { send: false, reason: 'waiting_for_customer' };
~~~
In wake.ts, select the latest answered_progressing event first, including payload.channel, and only then reject it as an anchor if channel=email. Filtering email before DISTINCT ON would revive an older call's wake sequence. Existing null-channel historical events retain call semantics. The existing order/reply/opt-out/lost stops still win even for forced test phones. A review date never clears the wait or triggers a send: only an explicit human action does.

- [ ] **Step 6: Run green.** pgTAP + wake Vitest + lead_db/worker integration on a local throwaway DB; verify sent count stays zero in waiting, raw inbound-before-send and opt-out race cases, across both WhatsApp lines, and no existing nonwaiting candidate changed. Force two leads sharing a phone through opt-out and inbound during a wake claim; verify no deadlock or later send. Re-run the existing order-intake worker suite after any shared-store change.

- [ ] **Step 7: Commit backend journey/SQL/test files** without flipping any outreach flag.

### Task 6: Fastify task and activity API with owner-bound access

**Files:**
- Modify: gt-factory-os/api/src/sales/schemas.ts, mutations_handler.ts, queries_handler.ts, route.ts
- Create: gt-factory-os/api/test/sales_workspace_tasks.test.ts

**Interfaces:**
- POST /api/v1/mutations/sales/leads/:lead_id/activity accepts request_id, channel, result, note, primary_action, additional_actions.
- PATCH /api/v1/mutations/sales/leads/:lead_id/contact accepts {phone?, email?, provenance}; admin/planner only, calls resolve_contact_gap.
- GET /api/v1/queries/sales/tasks?scope=mine|unassigned|all returns {rows:[{id,lead_id,org_id,kind,title,due_at,status,owner_email,source_kind,source_id,reason,lead_context}]}.
- POST /api/v1/mutations/sales/tasks/:task_id/complete accepts {note}; no direct client DB. Existing POST /outcome rejects answered_progressing only after the final gate is enabled.
- Handler names: handleRecordActivity(db,session,leadId,body), handleResolveContactGap(db,session,leadId,body), handleSalesTasks(db,session,scope), handleCompleteSalesTask(db,session,taskId,body). They bind the corresponding SQL functions; the portal calls only the HTTP routes.

- [ ] **Step 1: Write failing API tests** with existing inRolledBackTx harness. sales_rep cannot spoof ?assignee=other@example.com on Today or GET tasks?scope=all, and cannot PATCH contact; manager sees unassigned or inactive-owner work for reassignment and can resolve a contact gap with provenance; unknown task is 404; closed/another owner's task cannot be marked done by a rep; malformed UUID and missing due are 422 with stable SALES_ codes; POST same request_id returns same response, but changed payload with same ID is a conflict. For example:
~~~ts
const mine = await handleSalesTasks(trx, rep, 'mine');
assert.ok(mine.body.rows.every((task) => task.owner_email === rep.email));
await assert.rejects(
  () => handleSalesToday(trx, rep, 'other@example.com'),
  AuthError,
);
~~~

- [ ] **Step 2: Run red.** From gt-factory-os/api: npx tsx --test test/sales_workspace_tasks.test.ts; expected new handler imports missing.

- [ ] **Step 3: Add Zod and handlers.** Schema trims note, max length caps, maximum five extras, ISO offset dates and UUID request_id; DB performs the same essential checks. Task completion requires a note of at least five trimmed characters and writes a task_event; contact_resolution is excluded from generic completion, and only verified contact update can close it. Use actorOf(session) and roleAllowsSales, but enforce that sales_rep sees only own tasks and cannot complete a colleague's task or PATCH contact; admin/planner can view all and unassigned and resolve contact gaps. A task owned by a deactivated/nonexistent roster member appears in manager reassignment view, never in a ghost personal queue; the manager reassigns the lead, and the lead trigger moves its open tasks. Expose source event ID for drilldown, no private raw payload in card. Tighten handleSalesToday so sales_rep may request only their own exact email and never receives unassigned rows; admin/planner may explicitly request all/unassigned as defined.
~~~ts
if (session.role === 'sales_rep' && assignee && assignee !== session.email) {
  throw new AuthError('Not authorised', 403);
}
const ownerFilter = session.role === 'sales_rep' ? session.email : assignee ?? null;
const scope = session.role === 'sales_rep'
  ? sql`where assignee = ${session.email}`
  : ownerFilter ? sql`where assignee = ${ownerFilter}` : sql``;
~~~
For sales_rep, the query uses exact equality to ownerFilter, without an OR owner_email IS NULL branch. Admin/planner unassigned scope uses owner_email IS NULL.

- [ ] **Step 4: Run green.** Node tests for role matrix, errors, retries, task completion, original sales_workspace.test.ts; root npm run typecheck. Verify 401/403 never become a 200 HTML response.

- [ ] **Step 5: Commit API files and tests** in gt-factory-os.

### Task 7: Portal task API and Today as the assigned agent's work

**Files:**
- Create: gt-factory-os-portal/src/app/api/sales/tasks/route.ts, src/app/api/sales/tasks/[task_id]/complete/route.ts
- Create: gt-factory-os-portal/src/app/api/sales/leads/[lead_id]/contact/route.ts
- Create: gt-factory-os-portal/src/app/(sales)/_components/TaskCard.tsx
- Modify: gt-factory-os-portal/src/app/(sales)/_lib/types.ts, api.ts, labels.ts, useQueueScope.ts; _components/TodayQueue.tsx, TodayCard.tsx; sales/today/page.tsx
- Test: gt-factory-os-portal/tests/unit/sales/today-queue.test.tsx, api-stubs.test.ts; tests/e2e/sales-today.spec.ts

**Interfaces:**
- Consumes Task 6 endpoints, returns task IDs for mutations; existing Today lead rows remain available for conversion news but are not duplicated as personal work cards.
- Produces "שלי" showing only owner_email=session.email; manager "ללא שיוך" with one assignment action, plus "בירור פרטי קשר" for contact_resolution with a verified detail/provenance form. Capping applies only to untouched new leads, not promised due tasks.

- [ ] **Step 1: Write failing tests.** Two reps and one unowned lead → one task in each intended scope, zero duplication; button completes task only after a note, failure restores card; card shows action, due, why-now and source; no raw event code or snapshot money. A manager contact_resolution card rejects blank phone/email or provenance, submits verified detail, and changes to contact_first only on server success; no rep sees the manager form. Test navigation to /sales/leads?lead=<id>.
~~~tsx
expect(screen.getByText('ללא שיוך')).toBeVisible();
expect(screen.getAllByTestId('task-card')).toHaveLength(1);
expect(screen.getByText('למה עכשיו: הלקוח ביקש לשמוע עוד')).toBeVisible();
~~~

- [ ] **Step 2: Run red.** npm test -- tests/unit/sales/today-queue.test.tsx tests/unit/sales/api-stubs.test.ts; expected task card absent.

- [ ] **Step 3: Add thin proxy routes and typed hooks.** Follow src/app/api/sales/leads/[lead_id]/outcome/route.ts and proxyRequest, forwardQuery only for GET tasks, no Supabase browser DB client. A sales_rep starts in mine even if a stored local preference says all; admin/planner can deliberately select all or unassigned. TaskCard keeps the existing in-CRM call/WhatsApp arm-and-return behavior; contact_resolution instead opens a manager-only correction form for phone/email and confirmation source, using PATCH contact. Suppress duplicate lead-work cards when a task already represents the same contact/follow-up; keep conversion as news.
~~~ts
export const taskKey = (scope: 'mine' | 'unassigned' | 'all') =>
  ['sales', 'tasks', scope] as const;
~~~
Render task source as a short Hebrew reason; link to lead/event. Personal task completion posts note and invalidates sales queries; contact correction invalidates lead detail and manager queue together. No optimistic "done" before server confirms. Keep conversion as news in existing Today.

- [ ] **Step 4: Run green.** Focused Vitest, Playwright Today and assignment specs, typecheck and lint on touched files.

- [ ] **Step 5: Commit portal tranche files** (only paths in its manifest).

### Task 8: One durable, fast result sheet on Today and Leads

**Files:**
- Create: gt-factory-os-portal/src/app/api/sales/leads/[lead_id]/activity/route.ts; src/app/(sales)/_lib/activityDraft.ts
- Modify: gt-factory-os-portal/src/app/(sales)/_lib/api.ts, types.ts, labels.ts, useOutcomeCapture.ts; _components/OutcomeSheet.tsx, LeadDrawer.tsx; sales/today/page.tsx, sales/leads/page.tsx, sales/attention/page.tsx
- Test: gt-factory-os-portal/tests/unit/sales/{activity-draft,outcome-sheet,use-outcome-capture}.test.tsx; tests/e2e/{sales-outcome-integrity,sales-attention}.spec.ts

**Interfaces:**
- Consumes Task 6 activity endpoint. A draft key is authenticated user email + lead UUID; it stores raw form fields and a stable request_id in sessionStorage, with no remote write until Save.
- Produces answered + note≥5 + action/date or wait review; quick no_answer/whatsapp_sent one tap with previewed date; "won"/"lost" stay on their evidence/reason routes.

- [ ] **Step 1: Write failing tests.** Four trimmed chars block Save; five Hebrew chars enable; date required; waiting review future date required; quick no_answer posts no fake note; timeout then retry keeps same request_id; same agent/lead reload restores draft, different lead or agent does not; after 200 clear draft+armed intent, after 422/500 keep both. Exercise the existing outcome entrypoints on Today, Leads and Attention, including Attention card and drawer, with the new /activity endpoint.
~~~tsx
await user.type(screen.getByLabelText('מה קרה?'), 'אבגד');
expect(screen.getByRole('button', {name: 'שמור'})).toBeDisabled();
await user.type(screen.getByLabelText('מה קרה?'), 'ה');
expect(screen.getByRole('button', {name: 'שמור'})).toBeEnabled();
~~~

- [ ] **Step 2: Run red.** npm test -- tests/unit/sales/outcome-sheet.test.tsx tests/unit/sales/use-outcome-capture.test.tsx; expected textarea/action behavior missing.

- [ ] **Step 3: Implement draft helper and sheet.** Keep request_id across retry, generate via crypto.randomUUID on first draft, purge only on confirmed success or explicit user deletion; avoid storing cross-agent text under a shared key. The sheet's relevant body is:
~~~ts
type PrimaryAction = {
  kind: 'call' | 'whatsapp' | 'email' | 'other' | 'wait_review';
  due_at: string;
};
type ActivitySubmission = {
  request_id: string;
  channel: 'call' | 'whatsapp' | 'email';
  result: 'answered_progressing' | 'no_answer' | 'whatsapp_sent';
  note?: string;
  primary_action?: PrimaryAction;
  additional_actions?: PrimaryAction[];
};
~~~
A native keyboard microphone writes into the same textarea. No recording/upload/AI. Today, Leads and Attention use the same submit helper; remove every answered path that still calls useOutcome, while the explicit lost path may keep the old route. Arm the existing mailto link in LeadDrawer with channel=email so a substantive reply can be captured; do not call a sent email a two-way exchange automatically. Preserve explicit lost undo and won evidence behavior.

- [ ] **Step 4: Run green.** Focused Vitest and sales-outcome-integrity + sales-attention Playwright. Simulate pagehide, app return, reload, offline/timeout, stale lead ID, and a server 422. Verify the sheet remains keyboard safe at 320 and 390 px. Search all /(sales) callers of useOutcome and /outcome before enabling activity_required; only explicit lost remains on the legacy route.

- [ ] **Step 5: Commit portal files** within the sales tranche.

### Task 9: GT Pulse first slice, mobile gate and controlled release

**Files:**
- Create: gt-factory-os-portal/src/app/(sales)/_components/LeadJourneyRail.tsx; src/app/(sales)/_lib/leadMilestones.ts; tests/unit/sales/lead-milestones.test.ts
- Modify: gt-factory-os-portal/src/app/(sales)/_components/{LeadDrawer,TodayCard,OutcomeSheet}.tsx; src/app/(sales)/sales-tokens.css; tests/e2e/{sales-visual-a11y,mobile-sales-today}.spec.ts
- Create: gt-factory-os-portal/tests/e2e/sales-email-to-task.spec.ts
- Modify after actual verified release only: Sales-Machine/CURRENT_STATE.md with dated evidence, no new doctrine.

**Interfaces:**
- Consumes lead_event rows and task source from Tasks 3–8. Rail nodes: created, outreach attempt, answered two-way, next action, conversion evidence. Never infer answered from outreach, reply from outbound, won from a Shopify draft.
- Produces interactive source drilldown and readable mobile vertical rail; fuller account cycle/order pulse belongs to B/C.

- [ ] **Step 1: Write failing derivation and browser tests.**
~~~ts
expect(deriveLeadMilestones([{event_type: 'outreach', id: 'e1'}]))
  .not.toContainEqual(expect.objectContaining({kind: 'answered'}));
expect(deriveLeadMilestones([{event_type: 'draft_order', id: 'e2'}]))
  .not.toContainEqual(expect.objectContaining({kind: 'converted'}));
~~~
Browser asserts on 320, 390 and 430px: document.documentElement.scrollWidth <= window.innerWidth; focus/Save visible above virtual keyboard; reduced motion keeps labels and source links; role and name on buttons.

- [ ] **Step 2: Run red.** Focused Vitest and Playwright sales-visual-a11y/mobile-sales-today; expected absent rail or overflow assertions to fail.

- [ ] **Step 3: Implement visual slice.** GT Pulse tokens are scoped to (sales): petrol background/hero, turquoise primary, blue lead path, green verified order, amber review, coral late. Each state has label and accessible shape; glow follows saved state or selected action, never a guessed status. Dense data folds behind source disclosure; no tiny action text. Rail becomes vertical on mobile; OutcomeSheet uses max-height 100dvh, internal scroll and sticky Save above safe-area/keyboard. Check light/dark and prefers-reduced-motion without hiding meaning.
~~~css
@media (prefers-reduced-motion: reduce) {
  .s-pulse-active { animation: none; }
}
@media (max-width: 430px) {
  .s-lead-rail { flex-direction: column; min-width: 0; }
  .s-sheet { max-height: 100dvh; overflow-y: auto; }
}
~~~

- [ ] **Step 4: Verify full flow and prepare deployment gates.** Local throwaway DB: pg_prove 0362 and neighboring 0322/0324/0360/0361; backend npm run typecheck, api npm test, journey Vitest; portal npm run typecheck, npm run lint, npm test, targeted Playwright including sales-attention, portal-pr-guard. Email login → same lead → call/WA return from Today/Leads/Attention → valid note/action → exactly one assigned task → completion with note; unassigned manager path and contactless resolution; waiting plus raw inbound stop/send race path. Screenshot before/after for Tom. Record target runtime migrations, flags and SHA **read-only**. The activity_required switch waits until after UX gate, simplification, final review/verification, deployed new portal and rollback proof. No new wake sends are enabled by this plan.

- [ ] **Step 5: Prepare the one-time backlog.** Preview counts by owner/unowned/status and new task type; prove an idempotent backfill for open leads on staging after owner triage (contact_resolution for neither phone nor email; otherwise first contact when first_touch_at null, or due follow-up). Create only if no equivalent open task exists. Use stable source_key bootstrap:<lead-id>, source_kind=bootstrap and source_id=<lead-id>; never invent a lead_event ID for history that lacks one. Record exact dry-run counts, affected scope, rollback and tests. No production write occurs in this task: after UX gate, simplification and verification, obtain the written mass-write go/no-go required by brain CLAUDE.md §Authorization before running it. Do not notify or call a customer. CURRENT_STATE changes only after observed release.

- [ ] **Step 6: Commit focused visual/tests in portal and staging evidence in Sales-Machine.** Do not merge or deploy on the strength of a mock-only green test; follow each repo's gates and the approved Native execution method.

## Execution and rollback

The nine tasks yield a reviewable, staging-proven build. After them, run the sales-specific UX release gate, remediate, simplify, perform Native whole-branch review and verification on final heads **before** production rollout. Keep old lead/outcome reads working during rollout; task/activity endpoints are additive. Deploy additive backend then portal under brain release gates. Only after the portal serves on the exact target SHA and rollback is proven, set activity_required=true via audited sales_core.set_app_setting. Obtain a separate written mass-write go/no-go on the reviewed production dry-run before the one-time task backfill. Verify task counts/URLs and date the CURRENT_STATE evidence. If the new portal fails, restore its prior deployment, leave internal task rows intact, set activity_required=false and pause new task surfacing while investigating; do not drop tables or rewrite append-only history. If the wake guard cannot be proven under forced and real test paths, do not release waiting behavior. No customer-facing message/flag is turned on.

## Plan self-review

- Spec §1–3: Tasks 1–4 and 6–8; §4 triggers/ownership: Tasks 3, 5–7; §5 mobile: Tasks 8–9; §6 repo boundaries: Global Constraints/File Map; §7 acceptance: Tasks 1–9; §8 risks: rollout and guards.
- The five Review Focus conditions each have a named test task. Backlog bootstrap is staged after runtime verification. B/C/E and the richer account visual elements remain separately specified later.
- Before execution, refresh all three repo SHAs, the portal active tranche, Supabase migration slot, deployed runtime flags and the exact source event payloads. A source shape that differs from this pinned snapshot triggers plan revision, not guessed adaptation.
