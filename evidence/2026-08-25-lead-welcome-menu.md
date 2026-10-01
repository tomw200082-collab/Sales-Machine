# Evidence snapshot — lead-welcome menu built (2026-08-25)

> **Immutable. True as of 2026-08-25 only.** Never edit; supersede with a new dated
> snapshot. Authority grades assigned per `CLAUDE.md` §The 7 truth rules.
>
> This repo receives **only this record.** The deliverable and every script live in
> `gt-factory-os-production-brain/.claude/skills/lead-welcome-menu/` — `build.py` is
> runtime code and the constitution forbids it here.

## What was built

One Hebrew, right-to-left, 9:16 mobile-native PDF of exactly 15 screens presenting
four GT products and twelve costed drinks to a business lead who has just left their
details. Small enough to send on WhatsApp. Path:
`gt-factory-os-production-brain/.claude/skills/lead-welcome-menu/lead-menu.pdf`.

Built to the masterprompt `20260825leadwelcomemenumasterprompt.md` (Tom, 2026-08-25).

## Files changed

**`gt-factory-os-production-brain`**, branch `claude/caveman-copywriting-6mbzz8`:

| Path | What |
|---|---|
| `.claude/skills/lead-welcome-menu/SKILL.md` | the re-runnable package |
| `.claude/skills/lead-welcome-menu/copy.md` | all 15 screens' Hebrew copy, sourced line by line |
| `.claude/skills/lead-welcome-menu/DIRECTION.md` | the committed design direction |
| `.claude/skills/lead-welcome-menu/SYSTEM.md` | type and spacing scale |
| `.claude/skills/lead-welcome-menu/tokens.css` | colour tokens, each with its record |
| `.claude/skills/lead-welcome-menu/build.py` · `shot.py` · `shot_png.py` | the build |
| `.claude/skills/lead-welcome-menu/validate.py` · `verify.py` | the proofs |
| `.claude/skills/lead-welcome-menu/assets/` | 7 assets, 1.6 MB |
| `.claude/skills/lead-welcome-menu/lead-menu.html` · `lead-menu.pdf` | the deliverable |
| `docs/warehouses/marketing-assets.md` | 7 asset rows + 2 negative records, dated |

**`Sales-Machine`**: this file only.

## Checks run

| # | Condition | Result |
|---|---|---|
| D1 | 9:16 and exactly 15 screens | PASS — `pages 15`, MediaBox 810×1440 pt, `ratio 0.5625` |
| D2 | sends on WhatsApp | PASS — 2,338,979 bytes against a 4,194,304 limit |
| D3 | every drink figure is the approved figure | PASS — `deviations 0`, 48/48 fields |
| D4 | nothing unreadable on a phone | PASS — `min content font-size 36px` |
| D5 | no wholesale price reaches the lead | PASS — 16 checked, 0 matches |
| D6 | no discontinued product is shown | PASS — 5 checked, 0 matches |
| D7 | renders with no network | PASS — 0 network references; only `Rubik-SemiBold`, `Rubik-Bold`, `Heebo-Regular` embed |
| D8 | the closing screen leads with the promise | PASS — promise 150px is the largest, contact 42px is at body scale, promise precedes contact |
| D9 | reproducible and recorded | PASS — `build.py` regenerates a byte-identical HTML; warehouse rows dated; this file |

**Validators proven able to fail: 7/7.** Each was run against a deliberately broken
scratch copy and rejected it — a tampered profit, a tampered margin, sub-36px content
type, an injected wholesale price, an injected discontinued product, an injected
Google Fonts link, and a contact block raised above the promise. Originals verified
unchanged afterward.

The first version of `validate.py` **passed** the tampered-profit control, because it
only checked that each approved figure was *present* and `₪17.09` appears on two
screens. It now also requires every figure-shaped token on the page to *be* an
approved one. This is the whole reason the masterprompt requires testing a validator
against a failing input.

## Sources cited

| Source | Used for | Grade |
|---|---|---|
| `drinks_final_figures.json` (Tom, 2026-08-05) | every cost / price / margin / profit | `user_confirmed` |
| Canva drinks catalog `DAHPi9gpfts`, read-only | preparation, descriptions, ingredient panels | `doc_confirmed` |
| Canva products catalog `DAHQrpThEBE`, read-only | product blurbs, ingredients, contact block | `doc_confirmed` |
| `docs/warehouses/catalog-truth.md` (2026-08-06) | what GT actually sells — overrides the catalog | `user_confirmed` |
| Dropbox B-Bagel `index.html` + its shipped PDF | vision line, three-move pour, 5:1, storage, clean-label claims, 17 kcal, and the glass photography | `doc_confirmed` |
| Tom, this session | NAMASTEA ingredients follow the products catalog; contact block approved | `user_confirmed` |

Neither Canva design was opened for editing. Reads only.

## Tom decisions recorded today

1. **NAMASTEA ingredients follow the products catalog** — `לך לפי הקטלוג מוצרים`.
   Two black teas, cinnamon, cardamom, ginger, black pepper, clove. No Pu-erh, no star
   anise; the B-Bagel brochure's longer list does not carry into this deck.
2. **Contact block approved** — `מאשר את פרטי הקשר`: `gteveryday.com` ·
   `info@gteveryday.com` · `054-398-2444` · `@gteveryday`.
3. **Go for the full build** — `צא לדרך`.

## UNRESOLVED opened

- **U-LWM-01 — no MATCHA packshot at bottle quality.** S11 and S12 are deliberately
  typographic. Masterprompt §6.A says explicitly not to block on it.

  **The contact sheet §6.A asks for could not be built in this environment**, and the
  reason is worth recording so it is not rediscovered. The folder is
  `/AI YASTREBOVA/CATALOG/MATCHA UBE HOJICHA/PRODUCT PHOTOS/` (Dropbox ns_path
  `ns:14671628787//CATALOG/MATCHA UBE HOJICHA/PRODUCT PHOTOS`, **not** the
  `ns:13945604755` namespace the masterprompt cites — that path returns
  `FILE_NOT_FOUND`). It holds **71 PNGs, 4.4–8.7 MB each**, hashed names.

  All 71 are under the Google Drive MCP's 10 MB download cap, but **Drive does not
  mirror this folder** — a title search for two of the filenames and for the folder
  name returns nothing. And the Dropbox byte hosts are hard policy denials at the
  egress proxy (`dl.dropboxusercontent.com`, `content.dropboxapi.com` → 403 CONNECT).
  The PDF-extraction trick that rescued the glass photographs does not apply: these
  images are not embedded in any deliverable that is reachable.

  So there is no byte channel to them from here. Either Tom opens the folder himself,
  or someone copies a handful into the Drive folder that already mirrors
  `B-BAGEL-Tea-Programme` and a later session builds the sheet from there.

  Related and already registered in `marketing-assets.md` (מאושר-טום 2026-08-06), in
  case one of them serves: the matcha still-life
  `PRODUCT PHOTOS/hf_20260727_113138_1cc0f989-38c9-48d0-8cc0-050c509d9c90.png`. It is
  a lifestyle still-life (whisks + ice + pouch), not a clean packshot at the quality
  of the three bottles, which is why it was not used.
- **U-LWM-02 — the asterisk disagreement.** The drinks catalog marks eleven of the
  twelve with `* כולל הערכת עלות גרניש/קצף`; `drinks_final_figures.json` marks one
  (key `12`). The deck follows the catalog per masterprompt §2.2. Neither side was
  changed. Tom's ruling on the products catalog does not reach this — the asterisk
  lives in the drinks catalog.

## UNRESOLVED closed

- NAMASTEA ingredient conflict (masterprompt §6.B) — closed by Tom, above.
- Contact block for the closing screen (masterprompt §6.C) — closed by Tom, above.

## Tom approvals still required

- **Approval of the finished PDF before it reaches any lead** (masterprompt §6.D).
  Not yet given.

## Not done, and deliberately

Nothing was sent to any lead or customer. `SALES_CUSTOMER_OUTREACH_WRITE_ENABLED`
is `false`; building the PDF is permitted, delivering it to a lead is a
customer-facing write and is out of scope for this session.

factory-os core was not read or written. No Canva design was edited.
