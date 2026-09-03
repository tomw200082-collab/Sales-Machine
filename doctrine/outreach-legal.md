# Doctrine — the Israeli spam law and GT's follow-up sequence

> **NOT LEGAL ADVICE.** Claude is not a lawyer. This is a sourced reading of the statute
> applied to GT's specific sequence, done 2026-08-31 at Tom's instruction, to replace an
> open-ended "check with a lawyer" with a short list of answered questions and three
> narrow ones that remain.
> **Authority: `doc_confirmed`** — statutory text and its conditions read from public
> sources; **not** `user_confirmed` and **not** a legal opinion.
> Closes setup-artifact task **5.4**.

---

## 1. The law, and whether it reaches us

**סעיף 30א לחוק התקשורת (בזק ושידורים), התשמ"ב-1982** — "חוק הספאם", תיקון 40 (2008).

**`דבר פרסומת`** = *"מסר המופץ באופן מסחרי שמטרתו לעודד רכישת מוצר או שירות או הוצאת
כספים"*. A day-5 message asking a café owner whether the opening menu is still relevant is
squarely inside that definition. It is not saved by being short or friendly.

**Channel.** The prohibition covers email, SMS/MMS, fax, automated dialling **and messages
in instant-messaging applications, WhatsApp named explicitly** in the Hebrew sources.
Printed mail and live human telemarketing are outside it.

∴ **§30א applies to the day-5 and day-12 templates.** That question is settled and does not
need a lawyer.

## 2. The three messages, separated — they are not one risk

The sequence is usually discussed as one thing. It is three, with very different exposure.

| Message | Legal shape | Risk |
|---|---|---|
| **First response**, right after the lead writes | A reply to someone who asked GT a question. Answering an enquiry is not distributing an unsolicited advertisement | **Low.** Also inside the 24 h service window |
| **Day-2 follow-up**, inside the free window | Proactive, but inside a conversation the customer opened and about the thing they asked about | **Moderate** |
| **Day-5 and day-12 marketing templates** | Proactive, outside any window, to someone who did not order | **This is the whole question** |

## 3. Where GT actually stands — and it is two sentences away from safe

There is no explicit prior written consent, so the sequence would have to rely on the
exception in **§30א(ג)**: advertising may be sent without prior consent when **all four**
of these hold.

| # | Condition | GT today |
|---|---|---|
| 1 | The recipient gave their details **in the course of a purchase or a negotiation for a purchase** | **Probably yes, and this is the one genuinely arguable point.** A person who clicks a Click-to-WhatsApp ad about beverage bases and writes asking about them is plausibly in `משא ומתן לרכישה` — but "plausibly" is doing work here |
| 2 | The advertiser **told them the details would be used for advertising** | ❌ **Not done.** GT says nothing of the sort today |
| 3 | They were **given the opportunity to refuse**, and did not | ❌ **Not done** |
| 4 | The advertising concerns a **similar type** of product or service | ✅ Yes — the opening menu is exactly what they asked about |

**Two of the four are missing, and both are one line of copy.**

**The timing is on GT's side.** Under **ע"א לפיד (2019)** the notice under condition 2 does
**not** have to be given at the moment the details are handed over — it is enough that it
precedes the start of sending. So it can live in the **first response**, which is free,
inside the window, and something a human already approves.

### What every advertising message must carry anyway — §30א(ד)

Independent of the exception, a `דבר פרסומת` must state, prominently:

- that it **is** an advertisement,
- the advertiser's **name and contact details**,
- the recipient's **right to refuse** and how to exercise it — and refusing must cost
  nothing.

**The day-5 and day-12 templates must be written to satisfy this**, and Meta's template
approval is a separate gate from this one: an approved template can still be an unlawful
one.

## 4. Exposure, so the size of the risk is not guessed at

- **Up to ₪1,000 per message** without proof of damage (§30א(י)). It is a **ceiling, not an
  automatic award** — but it is claimed in **small-claims court, where no lawyer is needed**,
  which is what makes it cheap to bring.
- **Class actions are the real exposure**, not individual claims. At GT's volume (~90 paid
  messages a month) a single claim is noise; a certified class over months of sending is not.
- The offence is also **criminal**, with a fine up to **₪226,000** (2026), and **company
  officers can bear personal liability**.

## 5. What GT should do — and it is small

1. **Add two sentences to the first response** (free, inside the window, human-approved):
   that GT will send a couple of follow-ups about the products, and exactly how to stop it —
   *"אם לא מעוניינים, כתבו 'הסר' ונפסיק."* This is what closes §30א(ג) conditions 2 and 3.
2. **Record the refusal in `sales_core`, and make it cancel every future follow-up.** A
   refusal that is not honoured is worse than never having asked — it converts a defensible
   position into a knowing violation, which is the standard §30א(י) turns on. The scheduler
   rule that any reply or order cancels the remaining follow-ups (artifact 7.5) is the same
   mechanism; opt-out is one more reason it must be tested before go-live.
3. **Write the day-5/day-12 templates to §30א(ד)**: labelled as advertising, GT named with
   contact details, refusal line in every one.
4. **Never import a list.** The exception protects people who came to GT. It protects
   nothing about a café that never made contact.

## 6. The three questions left for a lawyer — 15 minutes, not an open brief

Everything above is answerable from the statute. These are not:

1. **Does an inbound enquiry from a CTWA ad amount to `משא ומתן לרכישה`** under
   §30א(ג)(1)? This is the load-bearing assumption of the whole design.
2. **Does the proposed opt-in line satisfy §30א(ג)(2)–(3)** as drafted, or does it need
   specific wording?
3. **Must the day-5/day-12 templates carry the word `פרסומת`** explicitly, or does the
   §30א(ד) labelling requirement admit softer phrasing?

## 7. The honest bottom line

**As designed today, the day-5 and day-12 templates would not sit inside the §30א(ג)
exception** — not because the idea is unlawful, but because two of the four conditions are
simply not implemented yet. Both are copy, both go in the first response, and both are free.

**Nothing has been sent.** `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` is `false`, the templates
are not written, and no follow-up scheduler exists. There is no live exposure to remediate —
only a design to get right before it runs.

---

## Sources

- `חוק הספאם` — סעיף 30א לחוק התקשורת (בזק ושידורים), התשמ"ב-1982, תיקון 40:
  definitions, the §30א(ג) exception and its four conditions, §30א(ד) message requirements,
  §30א(י) statutory damages. Read 2026-08-31 via public summaries of the statute.
- **ע"א לפיד (2019)** — the §30א(ג)(2) notice need not be contemporaneous with giving the
  details; it must precede the start of sending.
- Criminal fine figure (₪226,000, 2026) and the coverage of instant-messaging applications
  from the same Hebrew public sources.
- The regulator's own FAQ (`gov.il`, משרד התקשורת) and the ISOC verdicts index were both
  **unreachable from this session (HTTP 403)** — worth reading before the lawyer call.
