# Evidence — how leading companies follow up after a sales conversation

> Web research, 2026-09-28, done for Tom's request of the same day: after a salesperson talks
> with a lead who has not ordered, send automated WhatsApp messages that "wake them up",
> the first within 24 hours and then one ahead of each human follow-up
> ("תבדוק איך הגדולים והמצוינים עושים את זה בעולם, ותעשה את זה בסגנון שלהם, אבל ב-DNA שלנו").
> **True as of its date only.** Meta's rules change; re-read the linked pages before building.
> Authority: `doc_confirmed` for the Meta documentation and the statute (read at source);
> everything marked *(opinion)* or *(weak evidence)* is exactly that.
> The design built on this is `doctrine/playbooks/whatsapp-lead-journey.md` §5 (D-031).

## 1. The cadence the research supports

Four automated messages and three human touches over two weeks. The first automated message
within 24 h; each later one a few hours before a human call.

| # | When | Who | Purpose |
|---|---|---|---|
| 0 | Day 0 | human | The conversation. The rep says a recap and the ordering link will follow on WhatsApp |
| 1 | Within 24 h | automated | Recap, the ordering link, one next step |
| 2 | Day 3, morning | automated | Heads-up that the rep will call today, plus one useful asset |
| 3 | Day 3, afternoon | human | Call |
| 4 | Day 7, morning | automated | A result from a similar business, or the answer to a common hesitation |
| 5 | Day 7, afternoon | human | Call or chat |
| 6 | Day 14, morning | automated | Soft close with three choices |
| 7 | Day 14, afternoon | human | Last call, then stop |

The research brief placed the follow-ups on days 2, 6 and 13; the playbook moved them to 3, 7 and
14 to match Salesforce's day 1/3/7/14 rhythm and keep 48 h between automated messages.

- **Benchmarks.** Salesforce recommends "five to eight touchpoints… over two to four weeks" on
  days 1, 3, 7 and 14 [14]. RAIN Group found cold prospects need about 8 touches [23]; warm leads
  should need fewer *(opinion)*.
- **Closest real example.** CCU, a Chilean beverage company working through Meta partner Yalo,
  times its weekly WhatsApp offers to each store's sales-rep visit day [27] (self-reported case
  study).
- **Faire** sends a reminder 9 days after an unanswered invite, and another 3 days before a
  first-order offer expires [28] (confirmed from the search index only; the page blocks fetching).

## 2. How strong the evidence is

- **First message within 24 h:** standard practice, not a research finding [13][10]. The hard data
  ([11], [12]) measures how fast companies answer *new inbound* leads, which is related but not the
  same situation.
- **Heads-up before a call:** *weak evidence*, and only from outside sales. In randomized survey
  trials a text before the call raised cooperation on the call (28.6% vs 16.0%), not the pickup
  rate [15].
- **Keep the first touch human.** Texts sent *before* a first conversation hurt contact rates;
  texts sent *after* one went with higher conversion — a correlation only [16].
- **Human-written beats automated.** In Gong's data, emails reps wrote by hand got about twice the
  replies of automated ones (2.1% vs 1.1%) [17]. Hence: short, personal, signed by the person who
  spoke with the lead.
- **Not verified at source:** "80% of sales need 5 follow-ups" [26] (traces to a 1942 survey of
  fewer than 40 people) and Gong's "breakup emails +89%". No Gong Labs study on follow-up timing
  after a call was found.

## 3. What each automated message should do

- **1:** first name, a short recap, the ordering link as a button, one ask. At most 5 lines —
  WhatsApp truncates longer messages [10].
- **2:** name the rep and today's call; include one useful asset.
- **3:** one real result from a similar business, or the answer to a common hesitation.
- **4:** three quick replies (order now / remind me in a month / not for us). Standard practice;
  the evidence for it is anecdotal [24][25]. No guilt lines: in Gong's data "never heard back"
  cut meetings booked by 14% [18].

## 4. Stop rules and etiquette

- **Stop on:** a first order; any reply (Outreach and HubSpot unenroll on reply by default [19]);
  an opt-out — the opt-out button, "הסר", or error 131050; a block; the rep marking the lead lost.
- **Caps** *(opinion)*: at most 4 automated messages per lead, at least 48 h apart; skip a send
  if a rep messaged the lead in the last 24 h; after error 131049 wait at least 24 h.
- **Quiet hours.** Meta sets none; it asks senders to consider when people are offline [10].
  *(Opinion)* Sun–Thu 10:00–11:30 or 15:00–17:00, never Friday afternoon through Saturday or on
  holidays. For comparison, the US telemarketing window is 08:00–21:00 [20].

## 5. WhatsApp constraints (Meta, read at source 2026-09-28)

- **24-hour window.** It opens only when the lead messages or calls the business on WhatsApp.
  Inside it anything may be sent, free. Outside it only approved templates [1]. After a *phone*
  call no window is open, so message 1 is a template; after a WhatsApp chat it can go inside
  the window, free.
- **Category.** Follow-up nudges are **Marketing**: utility templates must be "non-promotional",
  and mixed content counts as marketing [2]. Every delivered marketing template is charged [3]
  (Israel rate recorded in D-022). An order confirmation is **Utility**.
- **Per-user cap.** Meta limits how many marketing templates one person receives; the limit
  adapts to read rate and inbox load. Hitting it returns error 131049. Messages inside an open
  window do not count [4].
- **Opt-out button.** Optional, recommended by Meta to "reduce block rate"; honour opt-outs on
  every number [5]. A user who turns off "Offers and announcements" silently stops receiving
  marketing messages; error 131050 [6].
- **Quality rating** uses the last 7 days of blocks and reports [7]; templates pause after
  negative feedback or low read rates [8].
- **Coexistence.** Messages the rep sends from the WhatsApp Business app are copied to the API
  as echoes and stay free; the app must be opened about every 14 days or the number disconnects
  [9] (GT's rule is 13 days, D-023).
- **Policy (updated 2026-09-23).** Opt-in must name the business; opt-outs must be honoured
  "on or off WhatsApp"; any automation needs a path to a human [22]. Meta's guide asks for
  messages that are "expected, timely, and relevant", "not pushy", with one call to action [10].

## 6. Israeli law (§30א) — already GT doctrine

The research agrees with `doctrine/outreach-legal.md` and D-024: a lead who wrote to GT is
arguably "in negotiation for a purchase", so advertising may be sent without prior consent only
if they were told their details would be used for advertising and given a way to refuse; every
advertising message must say it is one (`פרסומת`), name the sender and give a free way to refuse
[21]. Damages up to ₪1,000 per message. Counsel's three open questions stay in
`doctrine/outreach-legal.md` §6.

## Sources

1. https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages — the 24 h window opens on a user message or call; only templates outside it.
2. https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization and https://developers.facebook.com/docs/whatsapp/updates-to-pricing/new-template-guidelines/ — the utility rule; mixed content counts as marketing; "pending application follow-up" is listed as marketing.
3. https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing — per-message pricing since 2025-07-01; marketing always charged; inside the window free.
4. https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits/ — dynamic per-user cap, error 131049, wait 24 h, exemption inside the window.
5. https://www.facebook.com/business/help/448422200528701 — the opt-out button: optional, reduces blocks, placement, honour on all numbers.
6. https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates · https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/user_preferences · https://developers.facebook.com/documentation/business-messaging/whatsapp/changelog — dropped when "Offers and announcements" is off; stop/resume webhook; error 131050.
7. https://www.facebook.com/business/help/896873687365001 — quality rating from 7 days of feedback and block reasons.
8. https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview — templates pause on negative feedback or low read rates.
9. https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users/ — app messages copied to the API and free; open the app about every 14 days.
10. https://whatsappbusiness.com/wp-content/uploads/2026/04/Best-Practices-for-Marketing-Messages-on-WhatsApp-.pdf — Meta's guide (April 2026): soon after engaging, not pushy, truncation after 5 lines, single CTA, pause messages to non-readers, avoid offline times.
11. https://25649.fs1.hubspotusercontent-na2.net/hub/25649/file-13535879-pdf/docs/mit_study.pdf — MIT/InsideSales (2007): 21× better odds of qualifying at 5 vs 30 minutes (inbound web leads).
12. https://hbr.org/2011/03/the-short-life-of-online-sales-leads — HBR: contact within 1 h about 7× more likely to qualify; 60× vs 24 h or more.
13. https://blog.hubspot.com/sales/follow-up-email-after-meeting-networking — follow up within 12–24 h; recap, next step, one CTA.
14. https://www.salesforce.com/blog/small-business/how-to-follow-up-with-a-lead/ — 5–8 touches over 2–4 weeks on days 1/3/7/14; one low-friction CTA; soft close.
15. https://pmc.ncbi.nlm.nih.gov/articles/PMC4769066/ and https://poverty-action.org/publication/methods-note-messaging-improve-response-rates-effectiveness-pre-survey-sms-messages — randomized trials of a text before a survey call.
16. https://www.slideshare.net/Velocify/text-messaging-for-better-sales-conversion-25969164 — Velocify (2012, ~3.5M leads): texts before contact cut contact 39%; after contact, more than 2× conversion.
17. https://help.gong.io/docs/engage-analytics-benchmarks-and-best-practices — manually written emails 2.1% replies vs 1.1% automated.
18. https://www.gong.io/blog/7-tips-for-writing-the-perfect-follow-up-sales-email-according-to-science — "never heard back" −14% meetings (304,174 emails).
19. https://support.outreach.io/support/solutions/articles/159000426253-outreach-sequence-states-overview and https://knowledge.hubspot.com/sequences/unenroll-from-sequence — sequences stop on reply by default.
20. https://www.law.cornell.edu/cfr/text/47/64.1200 — US rule: no telemarketing before 08:00 or after 21:00.
21. https://fs.knesset.gov.il/17/law/17_lsr_299991.pdf and https://www.afiklaw.com/articles/a397 — §30א text; an Israeli law firm applying it to WhatsApp.
22. https://whatsappbusiness.com/policy/ — WhatsApp Business Messaging Policy: opt-in, opt-out, human escalation.
23. https://www.rainsalestraining.com/blog/how-many-touchpoints-does-it-take-to-make-a-sale — 8 touches on average to a first meeting.
24. https://www.outreach.ai/resources/blog/timeless-tips-for-sales-sequences — a 21-day sequence ending with a breakup email.
25. https://blog.hubspot.com/sales/the-power-of-breakup-emails-templates-to-close-the-loop — one rep's 33% breakup-email response (anecdote).
26. https://smei.org/sales-statistics/ — the "80%" statistic's 1942 origin.
27. https://whatsappbusiness.com/resources/success-stories/ccu/ — CCU (Chile) via Yalo: offers timed to the rep's visit day.
28. https://www.faire.com/blog/selling/how-to-send-effective-email/ — Faire's reminder timing.
