# Evidence notes (working file, no PII)

## Agent4 — portal corridor + Menu Builder (received)
Portal commit read: 94e77b2 (2026-10-02 17:53, #248 tranche 199). Unit B live at b03d4c2 (#246).
- /sales/today: queue (task cards, new leads capped 15/day default, returning customers, due follow-ups, wins). Rep: call/WA/email = opens phone app, system sends nothing. Log outcome (note>=5 chars + next action+date), postpone, lost (reason, 4.5s undo), won (invoice no.), complete task, fix missing contact.
- /sales/leads: table by status; lead card; set working/lost/note/next touch; assign (mgr); bulk assign (mgr); quick-add (name, phone, business, source note). Timeline includes WhatsApp journey events (auto message, button tap, question logged, kit sent, opt-out) as labelled events, NO message text.
- /sales/attention: overdue / unowned / stalled buckets + last 50 team events.
- /sales/orgs: paged list; filters active/prospect/all/review; managers bulk assign.
- /sales/orgs/[id]: next action, primary contact, last order, 12m orders/value ex-VAT, 2-year circle, order river, contacts, leads. No outcome/note on business itself. Only verified businesses show orders.
- /sales/orgs/review: manager-only identity queue (26 closed by Tom 2026-10-02, 0 open).
- /sales/settings: managers edit daily cap, queue order, lost reasons, 3 WhatsApp templates, SLA hrs.
- NOT visible to salesperson: WhatsApp conversation text; any order-cadence/second-order signal (customer w/o open lead shows "no open action"); Menu Builder activity.
- Menu Builder: spec approved (brain branch claude/menu-builder-discovery @2965266c, 09-final-reviewed-product-spec.md): mobile Hebrew page, lead picks from 48 drinks -> starter kit (800 NIS min round-up), menu poster, cart with cost/cups/"profit"; send creates Shopify draft via existing lead path. Status PROPOSED (spec) / BUILT-NOT-LIVE (backend draft PR #330, unmerged, 117 files under api/src/portal/builder/, routes.ts untouched). Not on main; not customer-reachable; nothing routes to it. Placement (P3 behind existing order link recommended) DEFERRED (Tom). CRM integration does not exist. Hard blocked until Sales Foundation Gate + Tom written unlock. Seen 2026-10-01: 4 order taps, 2 live links, 0 orders (lead-line order link).
- Findings: Builder README stale (Unit A live since 2026-10-01 08:00 UTC); spec 09 vs doc 11 (poster, "profit") conflict + D-018 amendment not recorded; PR #330 body stale (8/8 vs 14/14), based on old main 30759a2; builder docs call Unit B/D1 "not started" (both live); brain PR #241 draft; whether any lead received WA journey events = UNKNOWN per agent4 (check agent1).

## Prior Miro boards found in account (pre-existing, NOT mine, do not modify)
- uXjVEf8tMKE= "GT — Michael Prep — AS-IS + Target Journey — 2026-10-04": 24 frames, 397 items, E-numbered evidence, includes Sunday Workshop Flow, Alex/Avi mention => over-dense, out of this prep's scope. Use only for cross-check.
- uXjVEfDhWhM= "GT — מסע הלקוח כיום — AS-IS — 04.10.2026": 2 frames (new customer / returning customer), derived from Michael's PDFs. Visual language: Hebrew big text, stage headers purple #7966cf, grey steps #ececef, green choices #b1efcc, dashed = unverified, short connector labels.
- Michael's benchmark board uXjVHlDAulA= : "Board access denied" (different team). Proxy = board above.

## Agent1 — WhatsApp lead line (received; runtime 2026-10-02 15:28-15:31 UTC; gt-factory-os@76b2a4a, Sales-Machine@78ba5e7; no Railway tool -> env UNKNOWN)
- Lead line (phone_number_id 217553368116155) RECEIVES: 21 inbound + 3 staff echoes; first 2026-09-28 20:09 UTC, last inbound 2026-10-01 12:49 UTC. (U-050 "never" is STALE.) LIVE.
- Capture to CRM LIVE: 5 whatsapp_unattributed leads; 0 CTWA leads ever; site form 20, Facebook 51 (7 in last 7d).
- Staff alert + reminder emails LIVE: alert_sent 25, reminder_sent 210 in 7d.
- Ownership PARTIAL/MANUAL: 148 of 149 new leads unassigned; 149 open contact_first tasks, 148 unowned; 0 reply tasks ever.
- First-menu reply (PDF + 3 buttons) LIVE barely: 5 live sends (4 non-test phones, 1 test), delivered/read, last 10-01 12:48; real stranger vs internal test UNKNOWN (timing looks like tests).
- Generic "thanks, we'll reply": BUILT, never delivered (1 dry-run row only).
- Button order -> personal link -> Shopify draft + confirmation: LIVE one pass (5 taps; 1 draft_order 10-01 12:51, likely test). Hear more: LIVE (2 taps, 2 replies). Not now / opt-out: BUILT never used.
- Free-text auto reply LIVE against doctrine (D-027 says none): 1 live free_text_reply 09-30 06:21 ("we will call" + FAQ once/day, PR #328 Tom's 09-29 test).
- 4 wake-up messages BUILT NOT LIVE: cron lead_wake_sequence every 15 min, 266/266 ok; considered 8, sent 0 (not_eligible); 0 wake rows ever. Rules implemented in code, never exercised. Meta templates approval UNKNOWN.
- Lead-line silence machine check: PROPOSED only (none). 13-day coexistence rule MANUAL Tom (D-023): last echo 09-30 14:50; proxy deadline ~10-13.
- Site doors LIVE: 5 buttons -> lead line with approved texts; ~22 FAQ items live.
- Findings: F1 U-050 stale; F2 sends exist though docs say none before D-005 (flag was kept on by Tom 10-01 "להשאיר פתוח"; 24h soak not evidenced; no decisions.md row); F3 free-text auto reply contradicts D-027; F4 U-049 stale (opt-out column+fn+cron exist, never fired); F5 wake can't fire today (needs delivered live first msg + logged answered_progressing); F6 coexistence recipe cites wrong D-ids, heartbeat extension never done; F7 142 phones wrote to ORDER line in 30d -> ignored_unknown_or_disabled (no lead, no reply; site contact section still advertises it); F8 repeat Facebook contact 10-02 -> note but no reply task (low conf); F9 code holds msg1 >=2h after call vs "within 24h".
- Facebook-form leads and old-order-number contacts do not enter automated journey.

## Agent3 — customer / repeat / retention (received; RT 2026-10-02 15:29-15:40 UTC; Sales-Machine 78ba5e7, gt-factory-os 76b2a4a, portal 94e77b28)
- First order via personal link -> Shopify draft -> WA confirmation -> task `draft_followup` for owner: PARTIAL (one draft_order+order_confirm 10-01 12:48-12:51Z, looks like test).
- Completed order -> Green Invoice invoice + LionWheel delivery task: LIVE (D-029; 50/50). green_invoice_poll + lionwheel_poll crons active.
- After first order: call, customer set-up, staff complete draft: MANUAL (no code).
- Welcome / onboarding / training videos / second-order nudge: no automation exists; videos promise PROPOSED (assets missing U-020); after-first-order policy absent (U-016 "after first order" row open).
- Customer portal repeat ordering LIVE but barely used: flag on allowlist *; 196 phone approvals; 4 portal orders, all 2026-09-25. 3,878 of 3,883 clean orders in 12m created as Shopify draft orders (staff keying inferred); only 3 carry `portal` tag. MANUAL.
- Sleeping radar PARTIAL: lists, no action; 29 nightly runs since 2026-09-04; latest covered 8 accounts (7 insufficient history, 1 silent, 0 off-pace); only walks verified orgs that have a lead; no trigger/view/reader; no radar-sourced task.
- Retention/check task: DEFERRED (Unit C, no spec). 188 open tasks all on leads, 0 on orgs; 0 orgs have an owner.
- Win-back (Klaviyo U-029): BUILT-NOT-LIVE doc-only as of 2026-08-31: 2,537 in segment; 0 campaigns/flows/sending domains (32 days old, not re-read).
- Mirror refresh: cron job 44 (40 0 * * *) 0 runs yet; one manual reconcile (07:47Z) passed; first scheduled run 2026-10-03 00:40Z; three passes pending -> 2026-10-05 earliest.
- Expansion: new branch PARTIAL (manager review item at next refresh); rest DEFERRED. 48 chains, 338 members. 81,052 order lines; no basket map; whitespace recipe never run.
- Off-Shopify sales share UNKNOWN (U-006; Tom said 2026-08-24 none outside Shopify; Green Invoice never checked).
- Counts: orgs 1,330 (1,093 verified, 237 unlinked, 0 review); 238 customers new in 12m; verified: 588 active / 505 dormant; clean-order counts: 285 verified w/ 1 order, 320 w/ 2-4, 488 w/ 5+ (381 active). Median 39.8 days first->second order among reorderers (biased). Leads: 5 won ever; 30 new verified customers since 2026-08-01.
- Findings: U-006 vs Tom 08-24; radar reach 8 not whole-base; radar uses live Shopify totals not ex-VAT line sum; outreach flag D-005 default false vs CURRENT_STATE true by Tom 10-01 vs "nothing sends" (RT: 5 leads got real automated sends, only 1 on test allowlist); training-video promise w/o assets; U-016 duplicated numbering; delivery wording "via distributor Ice Dream" vs own regional runs: who delivers UNKNOWN; portal confirmation not logged per order (cannot prove delivery to existing customers), 2 portal registrations pending 4-5 days; two win-back counts (2,537 vs 505).
- D-041 says Ice Dream orders tagged ice-dream; RT shows 0.

## Agent2 — channels + salesperson loop (received; RT 2026-10-02 15:29-15:35Z; MK = Make read; gt-factory-os@76b2a4a; gt-site@5d3e69c)
CHANNELS
- Meta lead form LIVE: Make hook -> /ingest -> lead+org+Shopify lookup; knows name/phone/email/campaign, no business name (U-013). Response: alert email to 3 staff + unassigned contact_first task; no auto-assign, no auto-message. 51 leads total, 36 in 30d, last 10-02 12:04Z; hourly pulse + 04:00Z heartbeat; blind to lost page subscription / per-source quiet. FB login expires 2026-10-23 10:49Z (~21 days). Both Make scenarios active, last OK, DLQ 0.
- Instagram DM / Messenger: DEFERRED (U-054 parked by Tom). No pipe. 38 old rows from 08-10 Meta export (IG 30 last 2024-03; Messenger 8 last 2026-04); 0 in 90d.
- Website forms (home + 4 landing pages) LIVE: Edge fn -> /ingest source website_form + note; 20 rows (>=3 tests), same alert+task. Failure visible only in fn logs; heartbeat pools sources so dead form hides behind Facebook. Which site build is live: UNKNOWN.
- WhatsApp lead line entry LIVE: 80 lead-line events since 09-28 20:09Z, 5 leads (whatsapp_unattributed), 0 CTWA. No machine check on 13-day rule; heartbeat ignores WhatsApp. Site's "or write us on WhatsApp" link under form points to ORDER line (creates no lead).
- Email: UNKNOWN (no inbound parser; old Make "GT Leads - Instant" inactive).
- Manual quick-add: MANUAL built, never used (0 manual rows).
- Existing customers returning: PARTIAL (orders outside CRM by design; matched_existing_customer flag 6 in 30d; open lead's order-line msg -> note + reply task; radar 8 orgs read-only; portal access requests emailed to Doreen 3/3).
LOOP
- Task creation LIVE auto (new lead -> contact_first; no phone/email -> contact_resolution; repeat contact -> reply; draft order -> draft_followup). 188 open lead tasks (146 contact_first + 38 call from 10-01 backfill, 4 live).
- Ownership MANUAL: no round-robin; 0 sales_rep users; Avi is planner; 148 of 149 new leads unassigned.
- Next action/outcome LIVE unproven: 0 tasks ever completed; 15 legacy outcomes (8 progressing, 4 WA sent, 3 no answer), last 10-01.
- Next touch LIVE: 187 open leads; 40 have a touch (38 overdue); 147 none and untouched >24h. Median first touch since 08-24: Facebook 62h (n=51), website 15h (n=20), WhatsApp 0.3h (n=5).
- Morning digest LIVE: 06:00 IL, per assignee; covers leads with due/overdue next_touch (not tasks); unowned to Tom; 10-02 03:00Z ok: due 38, sent 2/2; clean daily since 09-04. Code writes "reminded" before send.
- Conversion LIVE: convert_lead sole writer of won; 5 won ever (all Shopify evidence; 3 on imports 08-24, 2 since). Lost = human click; 66 of 72 "not relevant"; no auto-expiry.
FINDINGS: U-025/U-050 stale; U-033 stale (digest 2/2); Make forwards answers itself (hydrated:false on all 82), Graph token dead but harmless; unowned leads w/o next touch in no digest; repeat Facebook enquiry on open lead -> note only (no task/alert; source list omits facebook); 0 CTWA vs D-021 expectation; cron sales_leads_poll 10-min no-op.

## BLOCKER (2026-10-02 ~15:45 UTC): Miro MCP daily limit (100 calls, Free plan, org-wide) REACHED. board_create refused. Resets "tomorrow". Earlier sessions today built 2 other boards (probably consumed budget).
Plan: generate DSL SVG + local HTML preview in scratchpad/board/, validate, then build in Miro after reset (about 10-15 calls).
Spot-check by me (SELECT, 2026-10-02 15:36:49 UTC): lead-line events 80 (last 10-01 12:51), leads 264, new 149, new unassigned 148, won 5, wake events 0, open tasks 188 -> matches agents.
