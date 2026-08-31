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

Food cost is **ex-VAT**; recommended consumer price is **incl. VAT**. Both as printed in
the deck, `Summer 2026`.

| # | Drink | Base | Food cost | RRP | Margin |
|---|---|---|---|---|---|
| 1 | חליטת היביסקוס וליים | FRESH | ₪3.25 | ₪20 | 81 % |
| 2 | משקה תפוח היביסקוס | FRESH + apple juice | ₪2.88 | ₪24 | 86 % |
| 3 | גזוז היביסקוס ותפוח | FRESH + apple juice + soda | ₪2.88 | ₪22 | 85 % |
| 4 | חליטת תה ירוק לואיזה וליים | DETOX | ₪3.25 | ₪20 | 81 % |
| 5 | משקה תות לואיזה | DETOX + strawberry purée | ₪4.80 | ₪31 | 82 % |
| 6 | אייס צ'אי מסאלה קלאסי | NAMASTEA + milk | ₪5.57 | ₪28 | 77 % |
| 7 | צ'אי מסאלה קולד פואם וניל | NAMASTEA + vanilla foam | ₪4.00 | ₪28 | 83 % |
| 8 | צ'אי מסאלה על הקרח | NAMASTEA + water | ₪3.70 | ₪24 | 82 % |
| 9 | אייס מאצ'ה קלאסי | MATCHA + milk | ₪4.26 | ₪26 | 81 % |
| 10 | אייס מאצ'ה תות | MATCHA + strawberry purée | ₪6.46 | ₪39 | 80 % |
| 11 | אייס מאצ'ה מסאלה | MATCHA + NAMASTEA | ₪6.86 | ₪37 | 78 % |
| 12 | מאצ'ה אגבה על הקרח | MATCHA + agave | ₪2.85 | ₪26 | 87 % |

Coverage the menu is built to give: cold · carbonated · milk-based · water-based.

**The claim GT makes about onboarding:** *"ההטמעה לוקחת יום. בלי ציוד מיוחד ובלי הכשרה
ארוכה."* — one day, no special equipment, no long training.

**Matcha preparation, the one technical detail every matcha drink depends on:**
`בסיס מאצ'ה Classic` = **1.8 g powder + 50 ml water**, mixed smooth.

### UNRESOLVED on this menu

The deck states food cost and consumer price **per drink**. It does **not** state what the
opening order itself costs, or in what quantities each component ships. Open as `U-018`
(§below). Until it closes, the price of the opening menu is a **transfer row**: a human
answers it.

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

### UNRESOLVED on delivery

- `U-019` — **the order cutoff.** How late can an order arrive and still make that day's
  or the next day's run? Without it, no exact day can be promised, only the regional
  pattern above.
- `U-020` — **where the regions divide.** "North / centre / south" has to become something
  a person or a query can decide from an address, or orders cannot be routed to a day.

Until both close, **the honest customer-facing answer is the regional pattern, never a
specific date.**

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
| U-018 | What does the recommended opening menu cost, and in what quantities does each component ship? The deck prices drinks, not the order |
| U-019 | The order cutoff — how late can an order arrive and still make the next regional run? |
| U-020 | Where do north / centre / south divide, as something decidable from an address? |
