# Evidence — social handle sweep, 2026-08-31

**Method.** Unauthenticated HTTP against each public profile URL, then the embedded
profile JSON was parsed out of the returned HTML. No login. No API token. Nothing written.
Captured to `scratchpad/social/tt_*.html`.

**Why this exists.** An earlier note this same day recorded the GT brand name as *free*
on TikTok and X. Half of that was wrong, and the error is worth recording because of how
it happened: the first check used the HTTP status code alone. **TikTok returns `200` for
a handle that does not exist**, rendering a page whose i18n dictionary contains the string
`Couldn't find this account` on every profile — present or absent. The status code and
that string are both worthless as evidence. Only the embedded JSON separates the cases.

## TikTok

| Handle | Verdict | Evidence |
|---|---|---|
| `@gteveryday` | **GT's own account. Live, public, 13 videos.** | `uniqueId: gteveryday` · `id: 7297668950497952769` · `signature: 🍃GreenTea Essences Company🍃 / עוד לא ניסיתם את זה / gteveryday.com` · `createTime 1699121005` = 2023-11-04 · `videoCount 13` · `followerCount 23` · `followingCount 2` · `heartCount 383` · `privateAccount false` · `verified false` · `nickname gteveryday` (still the default) |
| `@greenteaeveryday` | **Not ours.** Unrelated third party | `nickname: ชอบกินชาเขียวไข่มุก🍵` (Thai) · `privateAccount true` · `videoCount 0` · `followerCount 14` · `followingCount 596` · `createTime 1678949779` = 2023-03-16 |
| `@greentea_everyday` | Free | No `uniqueId` in the returned document |

The video list is loaded by a later API call and is **not** in the initial HTML, so the
13 videos were counted but **not read**. What they show is unknown and is not guessed.

## X

Calibrated first: `x.com/nasa` → `200`. So a `404` here does discriminate.

| Handle | Result |
|---|---|
| `x.com/gteveryday` | `404` — free |
| `x.com/greenteaeveryday` | `404` — free |
| `x.com/GTEveryday` | `404` — free |

## LinkedIn

| URL | Result |
|---|---|
| `linkedin.com/company/gteveryday` | `404` |
| `linkedin.com/company/greentea-everyday` | `404` |

Consistent with `l1` (no company page exists) but **weaker evidence than the TikTok
finding** — LinkedIn serves auth walls to unauthenticated clients and a `404` here is not
proof of absence. Recorded as consistent-with, not as confirmation.

## What this changes

- `z1` is no longer "grab a free name". It is **account recovery on a live published
  property** (→ `U-027`) plus a five-minute name grab on X.
- The credentials sheet needs a real TikTok row: owner, login method, password-manager
  entry name, 2FA, recovery mail — all currently unknown.
- Per masterprompt §7: a property whose owner cannot be established is not closed, not
  renamed, not cleaned up. Nothing on that account was touched.

## Not done

Nothing was posted. No account was contacted. No recovery flow was started — recovery
requires credentials this environment does not have and must not have.
