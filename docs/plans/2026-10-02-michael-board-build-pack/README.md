# Michael workshop board: build pack (2026-10-02)

Preparation for the Tom and Michael customer-journey workshop on 2026-10-04. Read-only preparation: no production, customer or CRM state was changed.

Why this exists: the Miro MCP daily limit (100 calls, Free plan, organisation-wide) was reached on 2026-10-02, so the board could not be created that day. The board content is generated here so it can be built in about 12 Miro calls once the limit resets. Tom asked for an automatic attempt on 2026-10-03 at 10:00 Israel time, retried at 11:00 and 12:00.

## Files

- `gen.py`, `lib.py`: one layout source. `python3 gen.py` writes `out/all.svg` (all 12 frames), `out/frame_*.svg` and `out/preview.html`.
- `shot.js`: renders `out/preview.html` with Chromium and prints text overflows (expected: `[]`). Needs the `playwright` node module.
- `evidence_notes.md`: summaries of the read-only evidence runs (counts only, no customer data), with timestamps and commits.

## Build steps in Miro

1. `board_create`, name `GT · מסע הלקוח · הכנה לסדנה עם מיכאל · 04.10.2026`. The masterprompt asks for a new board.
2. `canvas_create_from_svg` in three calls: frames A, B, C, D, E; then F, G, H, MB; then I, K, J. Frame coordinates are absolute and already spaced.
3. `canvas_read_as_svg` on each frame: check rendered bounds and fix anything the create result reports as resized. Tune `data-scale` on the sources table in frame K.
4. Read the board as Michael would (the seven questions in the masterprompt), fix, run verification-before-completion, then `board_show` once.

Do not modify the two older boards in the account (`uXjVEf8tMKE=`, `uXjVEfDhWhM=`). Michael's benchmark board returned "Board access denied".
Design: flows left to right, Hebrew text, status chips (LIVE, MANUAL, PARTIAL, BUILT NOT LIVE, PROPOSED, DEFERRED, UNKNOWN, אין היום), TO-BE frames on faint purple with an IDEA chip, Tom's private frame placed far right.
