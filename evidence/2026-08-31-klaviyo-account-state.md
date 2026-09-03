# Evidence — Klaviyo account state, 2026-08-31

**Method.** Klaviyo API, read-only, account `VimR5N`. Nothing was created, changed,
suppressed or sent. Every metric ID below was resolved to its name before being
interpreted — no filter definition here is inferred.

---

## 1. The headline

**`Win-Back Opportunities (Shopify)` holds 2,537 profiles.**

Its definition, resolved field by field:

| Condition | Metric | Meaning |
|---|---|---|
| count > 0, all time | `YyGAHc` = **Placed Order** | has bought from GT at least once |
| count = 0, last 180 days | `YyGAHc` = **Placed Order** | has not bought in six months |
| marketing consent | email, `can_receive_marketing: true` | may legally be emailed |

Against the consented base of **2,969** measured the same day, that is **85%**.

Five-sixths of everyone GT is allowed to email is a customer who bought, stopped,
and was never contacted. The segment has been sitting there, computed and active,
since **2026-07-18**. **Zero emails have ever been sent from this account** (§3).

This is the silent churn the whole repo was built around. It is not un-measured.
It is measured, correct, and idle.

## 2. `Churn Risks (Shopify)` is 0 — and cannot be anything else yet

Same first two conditions, plus:

| Condition | Metric | Resolved name |
|---|---|---|
| count ≥ 2, last 90 days | `RL8kfH` | **Received Email** |
| count = 0, last 90 days | `XLr3pM` | **Opened Email** |

"Received at least 2 emails in the last 90 days" can be true of nobody, because no
email has ever been sent. **The segment is structurally empty, not empirically empty.**
It will stay 0 until GT actually sends, and it will populate on its own afterwards.

Reading this 0 as "we have no churn risk" would be the exact inversion of the truth.

## 3. Everything in the account was created by the installer

| Object | Count | Evidence |
|---|---|---|
| Email campaigns, ever | **0** | `data: []` |
| Flows | **0** | `data: []` |
| Sending domains | **0** | `data: []` |
| Lists | 2 | `Preview List` · `Email List` — both created 2026-07-18 13:13:30, same second, `single_opt_in` |
| Segments | 9 | all created 2026-07-18 **13:12:56 → 13:13:35** — a 39-second window |

Nine segments, two lists, one 39-second window. **Nothing in this account was ever
made by a person.** Six weeks installed, never used.

The nine: `Potential Purchasers` · `Repeat Buyers` · `VIP Customers` ·
`Win-Back Opportunities` · `Churn Risks` · `New Subscribers` ·
`Engaged (30 Days)` · `Engaged (60 Days)` · `Engaged (90 Days)`.

Two of them — `Repeat Buyers` and `VIP Customers` — are exactly the population the
sales motion is about, already computed.

**Not idle, though:** `Delivered Shipment` appeared 2026-08-24, and
`Added to Cart` + `Viewed Collection` appeared **2026-08-31 08:33–08:34** — onsite
tracking started firing today. The integration is live and syncing. Only the
sending side is untouched.

## 4. Account details — concrete errors, on the footer of every future email

Klaviyo's `contact_information` is what renders in the compliance footer.

| Field | Live value | Problem |
|---|---|---|
| `country` | **`United States`** | The address is `הלהב 15, חולון`. Israel. Wrong country on every footer |
| `organization_name` | `GreenTeaEveryday` | Matches neither the brand (`GT Everyday`) nor the legal name (`גרינטי אוירי די בע"מ`) |
| `default_sender_name` | `gteveryday` | Lowercase. This is the "From" name every recipient sees |
| `website_url` | `http://gteveryday.com` | `http`, not `https` |
| `industry` | `null` | Affects deliverability benchmarking |
| `locale` | `en-US` | Timezone is `Asia/Jerusalem`, currency `ILS`, audience Hebrew |
| `address1` / `city` / `zip` / `region` | `הלהב 15` · `חולון` · `5885817` · `HAMERCAZ` | Correct — matches the published address and Shopify |

Only the last row is right. `country` is the one that is plainly false.

## 5. What this changes in the task board

| Task | Was | Now |
|---|---|---|
| `e0` decide one email tool | open | **settled by fact** — Klaviyo installed, syncing, and the only candidate |
| `e1` fix account details | open, unspecified | **six named fields**, §4 |
| `e3` verify sending domain | open | **verified absent.** Zero domains. Not "probably not done" |
| `e4` win-back journey | open | **audience already exists and is 2,537** |
| `e5` welcome journey | open | 0 flows — confirmed unbuilt |
| `e6` regular newsletter | open | 0 campaigns ever — confirmed unbuilt |
| `e7` use existing segments | open | **9 exist**, listed in §3 with IDs |

## 6. The order these must happen in

**Sending domain first (`e3`), and this is not a preference.** With no authenticated
domain, 2,537 six-month-dormant addresses receiving their first-ever mail from GT is
the textbook shape of a spam-trap hit. Volume plus dormancy plus no DKIM alignment
punishes the domain, and the damage lands on transactional mail too.

∴ `e3` → warm up on the engaged segments → **only then** the win-back.

⚠️ Nothing here authorises a send. A campaign to 2,537 people is a mass customer-facing
write: it needs `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED` (currently `false`) **and**
Tom's written approval, per the module declaration §11.

## 7. Not done

No campaign created, drafted or scheduled. No flow created. No profile suppressed,
imported or modified. No segment edited. No account setting changed — the six errors
in §4 are reported, not fixed, because they are Tom's account identity to confirm.
