# Answer bank — Tom's approval applied, and what it could not cover

**Date:** 2026-09-02 · **Grade:** `system_verified` for the Dropbox findings,
`user_confirmed` for the approval itself.

Tom, 2026-09-02: `קראתי- מאושר, תוודא אל מול ספר העבודה של GT בדרופבוקס`,
and when asked whether the approval covered the nine drafts as well as the
eighteen approved rows: `גם אותן`.

---

## 1. The verification he asked for is circular by construction

`ספר העבודה` resolves to `/Business/Gt Knowledge Base` in Dropbox — seven
folders, `00 · קרא אותי קודם` through `06 · העלאות — גולמי`.

**That folder is the answer bank's output, not its source.** The file
`/Business/Gt Knowledge Base/02 · בנק התשובות/בנק התשובות.md` opens with its
own provenance:

> `נוצר אוטומטית — ⊥ לערוך כאן` · `מקור: Sales-Machine/knowledge/` ·
> `נבנה 2026-09-02` · `קומיט 0ea90d3`

Checking the bank against it compares the bank to a render of itself. It can
prove the renderer works; it cannot confirm a single answer.

**Second finding: the Dropbox copy is stale.** It was uploaded
`2026-08-31T16:23Z`; the pack the repo now builds carries `2026-09-02` and
commit `0ea90d3`. Anyone reading Dropbox today is two days behind — and
specifically behind the 48 recipes that landed in `#26`/`#197`.

**Third finding: `ספר העבודה §07` still resolves to nothing.** Fifteen source
lines across `answer-bank`, `sales-motion`, `buyers`, `refusals`,
`public-claims`, `chapters` and `questions` cite it. The Knowledge Base is
numbered `00`–`06`; there is no `§07`. `GT_Playbook_HE_.xlsx` — the only other
candidate — is the factory-OS operator manual (weekly routine, stock counts,
purchase approval, MRP glossary) and contains no customer answers at all.
Those fifteen citations are graded `doc_confirmed` against a document nobody
can open. → `U-039`.

## 2. Six of the nine drafts approved

`switch_cost` · `switch_no_replace` · `invoicing_practice` ·
`after_first_order` · `one_bottle_many_drinks` · `powder_price_shock`

Each read before flipping. `one_bottle_many_drinks` and `powder_price_shock`
carry arithmetic that checks out against the record: `₪3.25`/cup at 20 cups a
litre, and `₪590 ÷ 277` servings `= ₪2.13`. `powder_price_shock` already
carries the caution that keeps `MATCHA 50 גרם` out of the answer.

## 3. Three held, each because Tom's own later ruling invalidated it

| Row | Why it was not approved |
|---|---|
| `who_delivers` | Said `מגיע לכל אזור בארץ לפחות פעמיים בשבוע`. **D-013(א), signed the same day, sets north to Tuesday only and south to Wednesday only** — one day, not two. Said to a Haifa customer it is a promise GT breaks in week one. Rewritten to name the days; the corrected text needs his word, because his approval was given on the old text. |
| `seasonality` | Said `בסביבות 90% מהקיץ`. Its own source measures **two** winters: `75%` (2024/25) and `89%` (2025/26). `~90%` quotes the better year and drops the worse. Rewritten to `75%–89%, והפער הולך ומצטמצם` — still answers the objection, and is true. |
| `switch_trial_size` | Describes the contents of the starter package. **Tom deferred starter packages to the next meeting the same day (D-012(יד)).** An answer describing an undecided package is not said to a customer. Also still `blocked_by: [TOM-A.1]`. |

## 4. State

`31` answers — **`24` מאושר · `3` טיוטה · `4` העברה** (was 18/9/4).

## 5. What is still owed

- Tom's word on the two corrected texts (`who_delivers`, `seasonality`).
- `switch_trial_size` unblocks when the starter packages are decided.
- The drive pack needs re-uploading to Dropbox; the live copy is two days stale.
- `U-039` — fifteen citations to a `§07` that does not exist.

**Nothing was said to a customer.** `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED=false`.
