# Evidence snapshot — what Alexander's CTWA plan changes about what we built (2026-08-30)

> **Immutable. True as of 2026-08-30 only.** Never edit; supersede with a newer dated
> snapshot.
>
> **Authority per claim:**
> - `system_verified` — every statement about what exists in GT's own repositories,
>   read from the working trees on 2026-08-30 (file paths cited inline).
> - `doc_confirmed` — the plan itself (`evidence/2026-08-30-ctwa-plan-alexander-source.md`)
>   and prior GT records (`doctrine/decisions.md` D-006, `CURRENT_STATE.md`,
>   `docs/decisions/modules/sales-declaration.md`).
> - `inferred` — marked inline. **Inferred is never policy** (`CLAUDE.md` rule 1).
>
> **Nothing here is a decision.** The proposed decisions are D-007 and D-008 in
> `doctrine/decisions.md`, both `PROPOSED`, awaiting Tom.

## Verdict

The plan is sound and its central argument is correct: a Click-to-WhatsApp ad removes
the delay and the pipeline that a lead form requires. It is worth doing.

But the plan is written as if nothing exists. Three of its nine stages describe
infrastructure GT already runs in production, and one of its stages is blocked by an
access problem GT diagnosed and recorded six days ago. Executed as written, the
six-week schedule would rebuild working systems and then stall in week one on
something no amount of building can fix.

The change is therefore not "build this". It is: **grant Meta access, decide two
things, reuse three systems, and stop one piece of work that is now obsolete.**

## 1. What the plan actually changes

The plan inverts the intake direction.

| | Built (today) | Plan |
|---|---|---|
| Entry | Meta lead form on the ad | CTWA ad opens a WhatsApp chat |
| Who moves first | We do — someone must see the lead and call | The lead does — they message us |
| Transport | Make → our `/ingest` route (D-006) | Inbound WhatsApp webhook, no transport layer |
| Attribution | `form_id` / `campaign_name` on the lead record | `referral.source_id` + `ctwa_clid` on the message |
| First touch | Email alert to Tom, then a human taps a `wa.me` link | Automatic reply within seconds, routed by category |
| Cost model | Free (we never message first) | Free for 72h from the ad click; day-5 and day-12 follow-ups are paid marketing templates |

The inversion is real and it does obsolete part of what is built. It does **not**
obsolete the storage, the workspace, or the alerting — see §2.

## 2. What already exists that the plan treats as greenfield

### 2.1 WhatsApp Business API is already live in production — plan stage 1 is mostly done

`system_verified`, read 2026-08-30:

- **Provider: Dualhook**, fronting the Meta Cloud API.
  `gt-factory-os/api/src/order-intake/README.md`.
- **Send port** — text and interactive buttons, `POST {base}/{version}/{PHONE_NUMBER_ID}/messages`,
  `Authorization: Bearer {WA_SEND_TOKEN}`. `gt-factory-os/api/src/order-intake/whatsapp/send.ts`.
- **Inbound webhook** — Meta verify handshake, `X-Hub-Signature-256` HMAC verification,
  fast ACK, forward to the Node worker. `gt-factory-os/supabase/functions/wa-order-bot/index.ts`
  and `gt-factory-os/api/src/order-intake/route.ts`.
- **Secrets already provisioned:** `WA_PHONE_NUMBER_ID`, `WA_SEND_TOKEN`, `WA_VERIFY_TOKEN`,
  `WA_APP_SECRET`.
- **Purpose today:** B2B customers text orders in Hebrew; the tested order-intake engine
  prices them into a Shopify draft. Gated OFF by `WHATSAPP_ORDER_INTAKE_ENABLED` and
  `WHATSAPP_AUTO_COMMIT_ENABLED`, both `false`.

**Consequence for the plan.** Task 1.2 ("rank three providers and pick one") is asking
GT to re-decide something it already decided and shipped. Task 1.3's technical half (a
number registered to the API) is already true of at least one number. What is genuinely
open is not *which provider* but *which number* — see §4.1.

`inferred`: the plan's author did not know this infrastructure existed. Nothing in the
plan references Dualhook, the order-intake bot, or the existing webhook.

### 2.2 Lead storage, the workspace, and the queue already exist — plan stages 4, 6.3 and 8 have a home

`system_verified` (schema + tests recorded in `CURRENT_STATE.md`, code read 2026-08-30):

- `sales_core` — org / lead / **append-only** `lead_event`, phone normalisation, one
  `ingest_lead` write path. gt-factory-os migrations 0318–0321, 43/43 pgTAP.
- Read models `api_read.v_sales_*` + admin-gated Fastify endpoints. Migrations 0322–0323,
  24/24 + 16/16 pgTAP.
- Portal `(sales)` route group — Today queue with a one-tap outcome loop, leads list +
  drawer, orgs, quick-add, ⌘K search, PWA, settings. Hebrew RTL, admin-only.
  `gt-factory-os-portal/src/app/(sales)/`.
- **188 leads / 186 businesses already imported** from the 2026-08-10 Meta export.

**Consequence for the plan.** Stage 8's six metrics (first-response time, qualification
rate, kit-request rate, first-order rate, cost per order, conversion by category) do not
need a new dashboard — four of the six are derivable from `lead_event`, which is
append-only and already carries outcome capture. Stage 6.3's pilot measurement can run
on the workspace that exists rather than on a spreadsheet.

`inferred`: the answer bank (stage 4) is specified as a Google Sheet. That is a
reasonable choice for a human-edited bank, but the "status = escalate to Alexander" rule
in 4.2 is the same shape as the existing outcome loop. Worth checking before building a
second state machine.

### 2.3 A heartbeat that makes silent death loud — the plan has no equivalent

`doc_confirmed` (`doctrine/decisions.md` D-006, `CURRENT_STATE.md`):

GT's lead intake died on 2026-06-07 when a Make Facebook OAuth token expired, and
**nobody knew for two months**. 99 of the 188 imported leads arrived after the intake
died and had never been seen by anyone.

What was built in response: a daily heartbeat that sends **even when everything is
fine** (proven working 2026-08-24 04:00Z), plus an hourly pulse, so silence alarms
within 24 hours instead of two months.

**Consequence for the plan.** A CTWA architecture has the same failure class — a
webhook subscription can be dropped, an app can be disabled, a number's quality rating
can be throttled — and the plan specifies no liveness check at all. The heartbeat must
be inherited, not left behind. This is the single most important thing to carry across
the migration.

## 3. The blocker: Meta access. It stops stages 1, 2 and 5 on day one.

`doc_confirmed`, recorded 2026-08-24 in D-006 and diagnosed against the live token:

- Tom holds **no Meta developer access**.
- The only Business app on the portfolio, **`Green Tea`, is WhatsApp-only, and Tom is
  not its admin**.
- Developer self-registration **blocks at SMS verification** — no code arrives, in
  either local or international format.
- The token Tom could produce is valid and non-expiring but carries **none** of
  `ads_management`, `leads_retrieval`, `pages_show_list`, `pages_read_engagement`.

That is precisely why D-006 put Make in front of the leads: Make's own Meta-approved app
holds the permissions GT cannot obtain.

**CTWA has no equivalent escape hatch.** Every one of these plan tasks requires access
GT does not currently hold:

| Plan task | Requires |
|---|---|
| 1.1 business verification | Business Manager **admin** |
| 1.5 messaging tiers / quality rating | WhatsApp Manager access on the WABA |
| 2.1 CTWA campaign, WABA linked to ad account | Business Manager admin **+** ad account access |
| 2.3(b) `referral` object in the webhook | webhook subscription on the app that owns the WABA (`Green Tea`) — Tom is not its admin |
| 2.5 custom-audience upload + exclusion | ad account access |
| 5.2 template submission and approval | WABA access |

`inferred`, and the most consequential inference in this document: **the plan's week-1
schedule is not achievable by GT's technical side alone.** Someone who is already an
admin — Alexander, or whoever administers `Green Tea` and the ad account — has to grant
it. That is a five-minute action by the right person and an infinite one by the wrong
person.

**Recommendation: this becomes task 0.0, ahead of 0.1.** Not because the packages
matter less, but because 0.1 blocks the *pilot* while access blocks the *build*, and
they can be unblocked in parallel.

## 4. Two decisions the plan does not take

### 4.1 Which number — and the plan's own rule collides with production

The plan's "אסור" §4 says: never move a number used for existing customers or personal
calls into the API, because it leaves the WhatsApp app the moment it does.

The rule is correct. But `system_verified`: GT **already** has a number in the API that
existing B2B customers text their orders to. So the choice is not the plan's clean
greenfield choice. It is:

- **(a) One number.** Leads and customer orders share an inbox. Cheaper, one WABA, one
  quality rating, one identity for the business. But the CTWA auto-reply and the
  order-intake bot then receive the same inbound stream and **must not answer over each
  other** — a first-message router becomes mandatory, and a lead's "כן, תשלח" must never
  be parsed as an order.
- **(b) Two numbers.** Clean separation, no router, independent quality ratings. But two
  WABAs (or two numbers on one WABA), two webhook subscriptions, two provider line items,
  and a business that answers on two numbers.

`inferred`: (b) is the safer first move, because it keeps a live, revenue-carrying
order channel out of the blast radius of a brand-new lead bot with an unproven quality
rating. But this is a business decision about how GT presents itself, not a technical
one, and it is Alexander's and Tom's to take. Task 0.5 already assigns "dedicated
number" to Alexander — it needs this context attached to be answerable.

### 4.2 What happens to the 188 leads already in the system

The plan is silent on them. They are phone numbers of people who filled in a form —
they have **no open CTWA window**, so under the plan's own cost model every one of them
is a paid business-initiated marketing template, and under the plan's own "אסור" §3
("do not contact anyone who did not initiate") they are the ambiguous case that task
5.4's legal review exists to settle.

They are also the most qualified list GT has. Leaving them undecided is the expensive
option.

## 5. Governance gates the plan does not mention

These are not objections to the plan. They are the sequence GT already committed to.

1. **Stage 7 in its entirety is customer-facing automated outreach.** 7.1 auto-reply,
   7.2 auto kit send, 7.3 Q&A layer, 7.5 follow-up scheduler — every one of them sends
   to a lead without a human in the loop. That is gated by
   **`SALES_CUSTOMER_OUTREACH_WRITE_ENABLED`, currently `false`**, per D-005 (CONFIRMED)
   and `docs/decisions/modules/sales-declaration.md` §11: **Tom's written approval +
   dry-run + ≥24h soak + RUNTIME_READY** before the flag moves. Nothing in stage 7 ships
   without that. Stages 0–6 are entirely unaffected.
2. **The sales module is approved; this outreach surface is not in its declaration.**
   `sales-declaration.md` §11 lists Shopify-channel customer-facing sends. A WhatsApp
   lead bot is a new integration surface and `inferred` needs an Amendment B to the
   declaration, the way Amendment A was approved on 2026-08-17.
3. **Doctrine is Tom's.** `CLAUDE.md` rule 5: Tom is the sole approver of `doctrine/`.
   Alexander's document sets direction and is authoritative on the commercial decisions
   it assigns to him (packages, pricing, terms, answer approval). It does not by itself
   change GT doctrine. Hence D-007 and D-008 land as `PROPOSED`.
4. **Stage 7.3's own rule matches ours.** "המערכת לא מנסחת תשובה משלה על מחיר, אספקה,
   כשרות או אלרגנים. היא משכפלת מה שכתוב, או מעבירה." That is `CLAUDE.md` rule 3 (no
   guessing; unknowns are logged, never silently filled) stated in the plan's own words.
   Good sign: the two documents agree on the thing that matters most.

## 6. The 36 tasks, against what exists

Status key: **EXISTS** = already built · **PARTLY** = substantial reuse available ·
**BLOCKED** = needs Meta access first · **NEW** = genuine new work · **DECIDE** = a
decision, not a build.

| Stage | Tasks | Assessment |
|---|---|---|
| 0 — Decisions | 0.1–0.5 | **DECIDE**, all five, all Alexander's. Unchanged by anything here, except 0.5 which needs §4.1's context. Add **0.0 — obtain Meta Business Manager + ad account admin**, ahead of all of them. |
| 1 — WhatsApp infra | 1.1 | **BLOCKED** — Business Manager admin. |
| | 1.2 | **EXISTS** — Dualhook, in production. Re-open only if the shared-inbox requirement genuinely fails against it. |
| | 1.3 | **PARTLY / DECIDE** — a number is already in the API; §4.1 is the real question. |
| | 1.4 | **NEW** — business profile fields. Cheap. |
| | 1.5 | **BLOCKED** — WhatsApp Manager access. |
| 2 — Campaigns | 2.1, 2.2, 2.4, 2.5 | **BLOCKED** — ad account access. 2.4 (naming convention) can be drafted now at zero cost. |
| | 2.3 | **NEW**, and the one piece of real engineering. `referral` / `ctwa_clid` appear **nowhere** in GT's code today (verified by search across `api/src`, `supabase/functions`, portal `src`). The webhook that would carry them exists; the handler for them does not. |
| 3 — Content kits | 3.1–3.3 | **NEW** — marketing work, unblocked, can start today. |
| | 3.4 | **PARTLY** — media upload is a provider call on infrastructure that exists. |
| 4 — Answer bank | 4.1–4.3 | **NEW** — but check §2.2 before building a second escalation state machine. |
| 5 — Templates | 5.1 | **NEW** — mapping only, no access needed. Verify the 72h claim before relying on it (U-019). |
| | 5.2, 5.3 | **BLOCKED** — WABA access. |
| | 5.4 | **DECIDE** — Alexander + a lawyer. Also governs the 188 (§4.2). |
| 6 — Manual pilot | 6.1–6.4 | **NEW**, and correct. 6.3's measurement can run on the existing workspace (§2.2). 6.4's gate matches D-002's build order exactly. |
| 7 — Automation | 7.1–7.5 | **NEW**, and **all five gated** by `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` (§5.1). |
| 8 — Measurement | 8.1 | **PARTLY** — four of six metrics derive from `lead_event`, which already exists. |
| — | (missing) | **NEW — the heartbeat.** Not in the plan. Must be carried across (§2.3). |

## 7. What should stop

`CURRENT_STATE.md` records two Make scenarios as "not built — awaiting Tom's go-ahead":
a **lead transport** scenario and an **hourly pulse** scenario.

If the plan is adopted, the lead-transport scenario is **dead on arrival** — it exists
only to carry Meta *lead-form* submissions, which the plan removes. Building it would be
work thrown away.

The hourly pulse is a different matter: it is liveness, and liveness survives the
architecture change (§2.3) — but its input changes from "did Make deliver a lead" to
"did the WhatsApp webhook deliver a message".

This is the one immediately actionable item in this document, and the only one that
saves money today rather than spending it. It is proposed as **D-008**.

## Open unknowns opened by this assessment

Filed in `CURRENT_STATE.md`: U-014 (Meta access), U-015 (number strategy), U-016 (the
188), U-017 (Amendment B scope), U-018 (the workbook), U-019 (the 72h window and the
Israel tariff). U-013 is superseded — Alexander's plan removes the form the question was
about.

## What was checked, and what was not

**Checked** (`system_verified`, 2026-08-30): the four working trees; `sales-leads-poll`
and its `_lib`; `wa-order-bot`; `api/src/order-intake/` including the WhatsApp send port
and README; the portal `(sales)` route group and `_lib/wa.ts`; a repository-wide search
for `referral`, `ctwa`, `source_id` across backend, edge functions and portal source.

**Not checked, and deliberately not guessed** (`CLAUDE.md` rule 3): Meta's current
72-hour free-entry-point behaviour and the Israel marketing-template tariff — neither
was read from Meta's live pricing documentation in this session, so the plan's cost
model is reproduced, not confirmed (U-019). The state of the `Green Tea` app's
admin list. Whether the Dualhook contract permits a second number or a second WABA. The
workbook ("ספר העבודה"), which this session has never seen (U-018).
