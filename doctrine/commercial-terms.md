# Doctrine — commercial terms

> **Authority: `user_confirmed`.** Tom answered these directly on **2026-08-31**, in
> writing, in response to the four questions the lead-response masterprompt §6.C names as
> blocking. Logged in `doctrine/decisions.md` as D-007 … D-010.
> **Freshness: `review_30d`** for prices and delivery days; `stable` for the ex-VAT rule.
>
> This file is the source the answer bank quotes from. **A machine may reproduce a line
> from here verbatim. It may never rephrase one, and it may never answer a question this
> file does not cover** — that case is a transfer to a human, not a guess.

---

## 1. Pricing convention — applies to every number GT states

**Every price GT quotes to a business is ex-VAT (`ללא מע"מ`), and is said so out loud.**
GT sells wholesale to businesses; the business reclaims VAT, so ex-VAT is the number that
means something to the buyer.

**The single exception:** a **recommended consumer price** (`מחיר מומלץ לצרכן`) — what the
café should charge its own customer — is stated **including VAT**, because that is the
number on the café's menu board.

Both kinds of number therefore appear in the same conversation, and confusing them is the
expensive error. **Rule: never state a price without its VAT basis attached.**

| Kind | Basis | Example phrasing |
|---|---|---|
| What the business pays GT | **ex-VAT** | `₪65 ללא מע"מ` |
| What the business should charge | **incl. VAT** | `מחיר מומלץ לצרכן ₪24 כולל מע"מ` |

---

## 2. The recommended opening menu (`תפריט הפתיחה המומלץ`)

**Source:** Canva design `DAHTY5nfDxo`, *"תפריט פתיחה מומלץ חדש"*, 20 pages, last updated
2026-08-30. Tom named it as **the** starter offer on 2026-08-31.

**Structural note, recorded rather than smoothed over:** the setup artifact (task 0.1)
proposes **three** starter packages, one per drink category. Tom's answer is **one**
recommended opening menu that spans all three. That is a simplification, not an omission —
but it means the three category campaigns converge on a single offer, and only the content
kit differs by category. §W1 of the architecture decision is affected accordingly.

### What is in it

| Component | What | Why it is in the menu |
|---|---|---|
| **FRESH** | Thai infusion — hibiscus flowers + lime | **Caffeine-free.** Vivid red, visually distinctive; gently sour, brings customers back |
| **DETOX** | Israeli infusion — green tea, lemon verbena, mint, lime | Light and refreshing, works at every age; a clear health narrative |
| **NAMASTEA** | Indian infusion — two black teas, cinnamon, cardamom, ginger, black pepper, clove | Huge seller with Israeli audiences. Works cold, with coconut water, hot, and as a latte |
| **MATCHA** | Japanese ceremonial matcha, Shizuoka prefecture | Flown from the growers from the moment of picking. Not a passing trend |
| **SMOOTHIE** | Fruit purées — mango, strawberry, peach, 50 % fruit | Pairs with matcha, ube and more |

### The 12 drinks it builds, with GT's own figures

Recommended consumer prices as printed in the deck, `Summer 2026`.

| # | Drink | Base | מחיר מומלץ לצרכן |
|---|---|---|---|
| 1 | חליטת היביסקוס וליים | FRESH | ₪20 |
| 2 | משקה תפוח היביסקוס | FRESH + apple juice | ₪24 |
| 3 | גזוז היביסקוס ותפוח | FRESH + apple juice + soda | ₪22 |
| 4 | חליטת תה ירוק לואיזה וליים | DETOX | ₪20 |
| 5 | משקה תות לואיזה | DETOX + strawberry purée | ₪31 |
| 6 | אייס צ'אי מסאלה קלאסי | NAMASTEA + milk | ₪28 |
| 7 | צ'אי מסאלה קולד פואם וניל | NAMASTEA + vanilla foam | ₪28 |
| 8 | צ'אי מסאלה על הקרח | NAMASTEA + water | ₪24 |
| 9 | אייס מאצ'ה קלאסי | MATCHA + milk | ₪26 |
| 10 | אייס מאצ'ה תות | MATCHA + strawberry purée | ₪39 |
| 11 | אייס מאצ'ה מסאלה | MATCHA + NAMASTEA | ₪37 |
| 12 | מאצ'ה אגבה על הקרח | MATCHA + agave | ₪26 |

Recommended consumer prices are **incl. VAT** (§1) — they are what the café puts on its own
menu board, so they are a selling argument and are safe to state.

**Food cost is deliberately absent from this table.** See §2.1.

Coverage the menu is built to give: cold · carbonated · milk-based · water-based.

**The claim GT makes about onboarding:** *"ההטמעה לוקחת יום. בלי ציוד מיוחד ובלי הכשרה
ארוכה."* — one day, no special equipment, no long training.

**Matcha preparation, the one technical detail every matcha drink depends on:**
`בסיס מאצ'ה Classic` = **1.8 g powder + 50 ml water**, mixed smooth.

### 2.1 The two numbers GT deliberately does not state

**Tom, 2026-08-31, explicitly:** neither the **price of the opening menu** nor the
**food cost per drink** is stated by the system.

This is not a gap waiting to be filled. It is the offer's design. Those two numbers are the
ones a café owner most wants, which makes them the reason to have the conversation at all —
*"זה פיתוי של סקרנות הלקוח כי זה הכי מעניין ולכן דווקא את שניהם אנחנו לא אומרים."*

∴ In the answer bank both are **transfer rows**. Asked either question, the system says a
person will answer and hands over. It never quotes a figure, never estimates one, and never
says "it depends" as a way of half-answering.

| Asked | The system does |
|---|---|
| "כמה עולה החבילה?" | transfers to a human |
| "מה העלות למנה / כמה זה עולה לי לייצר?" | transfers to a human |
| "כמה אני יכול למכור את זה?" | **answers** — the recommended consumer price is public |

**One consequence Tom should decide on, flagged rather than acted on:** the margin
percentages printed on the deck (77–87 %) together with the consumer price imply the food
cost by arithmetic — ₪20 at 81 % is ₪3.80. If the food cost is meant to be genuinely
withheld, the margin figures leak it. They are on Tom's own deck, so they stay here until he
says otherwise; this file only records that the two are not independent.

Food cost figures themselves live in `gt-factory-os-production-brain/docs/pricing/`
(`2026-08-27_COST_MODEL.md`, `GT_FOOD_COST_2026-08-27.xlsx`) and are **internal**. They are
not repeated in this repo, so the answer bank cannot quote them by accident.

---

## 3. Delivery

**Confirmed by Tom, 2026-08-31.** GT delivers **Sunday to Thursday**, on fixed regional
days:

| Day | Region |
|---|---|
| ראשון · Sunday | **מרכז** — centre |
| שני · Monday | **מרכז** — centre |
| שלישי · Tuesday | **צפון** — north |
| רביעי · Wednesday | **דרום** — south |
| חמישי · Thursday | **מרכז** — centre |

### What that means, derived

| Region | Runs per week | Longest gap between runs | The sentence a customer can be told |
|---|---|---|---|
| **מרכז** | 3 — Sun, Mon, Thu | **3 days** (Mon→Thu, Thu→Sun) | *"עד 3 ימי עסקים."* |
| **צפון** | 1 — Tue | **7 days** | *"ביום שלישי הקרוב"* — up to a week |
| **דרום** | 1 — Wed | **7 days** | *"ביום רביעי הקרוב"* — up to a week |

**The consequence worth knowing before a salesperson promises anything:** a northern
customer who orders on Tuesday afternoon waits a **full week**. That is the worst
experience the delivery grid can produce, and it is structural — it is a function of one
run per week, not of anything going wrong.

∴ For north and south, **the order cutoff is a bigger lever on delivery time than the
truck is.** Moving a customer from just-missed to just-made is worth six days.

### The order cutoff — **14:00**

**Confirmed by Tom, 2026-08-31.** An order that arrives by **14:00** makes the next run for
its region. After 14:00 it waits for the one after.

Combined with §3, that gives an exact answer for the first time:

| Region | Order in by 14:00 on… | Arrives |
|---|---|---|
| **מרכז** | Sat / Sun | Sunday / Monday |
| | Mon–Wed | Thursday |
| | Thu | Sunday |
| **צפון** | Mon | Tuesday |
| | Tue (after 14:00) – Sun | the **following** Tuesday |
| **דרום** | Tue | Wednesday |
| | Wed (after 14:00) – Mon | the **following** Wednesday |

**The 14:00 line is worth six days to a northern or southern customer.** For the centre it
is worth one to three. That asymmetry is the single most useful operational fact in this
file, and it should be said out loud in the conversation — *"אם ההזמנה אצלנו עד 14:00 ביום
שני, זה מגיע מחר"* is a far better sentence than any delivery-time promise.

### Which region a city belongs to — derived from GT's own deliveries

**Method:** 1,555 completed LionWheel deliveries over the last 365 days
(`private_core.orders_mirror`, mirrored from `/api/v1/tasks.json`), grouped by destination
city and by the weekday the delivery actually completed. This is not a guess at a map — it
is where the truck has been going. Authority `system_verified`, measured 2026-08-31.

| Region | Day | Cities that ride it | How consistent |
|---|---|---|---|
| **צפון** | שלישי | חיפה · הקריות · נשר · זכרון יעקב · נתניה · תל יצחק · בני דרור | **88 %** — the tightest of the three; these cities are served on Tuesday and essentially no other day |
| **דרום** | רביעי | **ירושלים** · מודיעין · רחובות · ראשון לציון · נס ציונה · אשדוד · אשקלון · באר שבע · כנות | 71 % |
| **מרכז** | ראשון · שני · חמישי | תל אביב · רמת גן · גבעתיים · בני ברק · חולון · בת ים · פתח תקווה · ראש העין · הרצליה · רעננה · כפר סבא · הוד השרון · רמת השרון · קרית אונו · רשפון | 32–47 % per day — low **because** centre cities appear on all three centre days, which is correct, not noise |

**Two things the plain three-region label hides, and a salesperson needs:**

1. **Jerusalem and the Shfela ride the Wednesday "south" run.** ירושלים, מודיעין, רחובות,
   ראשון לציון and נס ציונה are not centre. A Jerusalem café is a Wednesday customer with a
   one-run-a-week cadence, and telling it "up to 3 business days" would be wrong.
2. **The boundaries are two belts, not lines.**
   - South: the ראשון לציון / נס ציונה / רחובות belt is where centre becomes south — those
     cities appear on both Wednesday and centre days in the data.
   - North: between הרצליה / רעננה (centre) and נתניה (north).

**The simple rule that follows:** anything in Gush Dan and the Sharon up to Herzliya/Ra'anana
is centre. Netanya and north is Tuesday. Rishon LeZion and south, plus Jerusalem and
Modi'in, is Wednesday. Anything on a belt — ask.

**Data-quality note, because it blocks automating this:** the same city appears under
several spellings in the mirror (`Tel Aviv-Yafo`, `Tel Aviv-Jaffa`, `תל אביב יפו`,
`תל אביב`; `Haifa` / `חיפה`). Routing a lead's address to a delivery day by string match
would need normalisation first. For a human reading the table this is a non-issue.

---

## 4. Minimum order

**₪800 + VAT.** (Per §1, stated to the customer as `800 ש"ח ללא מע"מ`.)

Confirmed by Tom, 2026-08-31.

---

## 5. Commitment and exclusivity

| Question | Answer | Confirmed |
|---|---|---|
| Is there a contract? | **No** | Tom, 2026-08-31 |
| Is there a monthly minimum? | **No** — the ₪800 minimum is **per order**, not per month | Tom, 2026-08-31 |
| Is there regional exclusivity? | **No** | Tom, 2026-08-31 |

This is a genuinely simple answer and it is a selling point: a café can start without
signing anything and without committing to a monthly volume.

---

## 6. Discount tiers — deliberately open

**Tom's answer on 2026-08-31 was: leave it open.** That is a decision, not an omission.

∴ In the answer bank, *"is there a discount as I buy more?"* is a **transfer row**. The
system says a human will answer and hands over. It does **not** say "no", because no is not
what Tom said, and it does not invent a tier.

Tracked as `U-003`-adjacent and as the one remaining item of masterprompt §6.C.

---

## New UNRESOLVED opened by this file

| ID | Question |
|---|---|
| U-018 | **Withdrawn, not answered** — Tom decided on 2026-08-31 that the opening menu's price is deliberately not stated (§2.1). It is a transfer row by design, not an open question |
| U-019 | **CLOSED** 2026-08-31 — the cutoff is 14:00 |
| U-020 | **CLOSED** 2026-08-31 — derived from 1,555 LionWheel deliveries (§3). Residual: city-name normalisation before any automated routing |
| U-021 | The margin percentages on the deck imply the food cost by arithmetic. If food cost is meant to be withheld (§2.1), is the margin figure meant to stay? | Tom |
