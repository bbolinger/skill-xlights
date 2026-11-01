# Oh Come All Ye Faithful (Christmas Punk) — sequence notes

Handoff notes for whoever picks this sequence up next (human or agent). Last updated 2026-10-31.

## The song
- `punk_ohcome.mp3`: Garrett Breeze & David Dykstra, *Christmas Punk*. Instrumental (drums, bass, guitar only),
  175 BPM on a click, G major, 1:11 (DUR 71.627 s, music ends ~68.5 s). Bars are 4 beats from `t0` (see `build.py`).
- What the user loves: the **syncopation** and the **guitar riff**, especially the **0:20–0:25 build** (kick drops
  out, a cymbal on every beat, melody climbs A→B→C). Its sibling build is at 0:47.

## Files
| What | Where |
|---|---|
| Sequence (generated) | `seqs/punk-ohcome/punk-ohcome.xsq` |
| Generator | `tooling/songs/punk-ohcome/build.py` |
| Analysis | `tooling/songs/punk-ohcome/events.json`, `events2.json`, `midi/` |

`events.json`/`events2.json` came from one-off scripts in the very first session, **before** `tooling/extract_events.py`
existed, so their format differs from the newer songs (no `summary.txt`). Re-running `extract_events.py punk-ohcome`
would overwrite `events.json` with the new format and `build.py` would need adapting. Don't do that casually.

Rebuild: `cd tooling && ./run songs/punk-ohcome/build.py`, then `./run validate_xsq.py ../seqs/punk-ohcome/punk-ohcome.xsq`.
The builder refuses to overwrite the .xsq if it was edited in xLights since the last build (`--force` overrides;
back up first). As of 2026-10-31 the .xsq is unchanged since the last build.

## History and feedback
1. v1: first draft with per-model effects. The user was impressed, but asked for **groups over individual models**,
   periodic **AllModels** moments, and **Verts that don't all do the same thing**.
2. v2: moved to groups, 8 AllModels moments, moving patterns on the Verts.
3. v3 (canvas rework): **Verts are one canvas, so no flashing them as solid panels**. Snare ripples, smooth fill
   climbs and a gliding dot replaced the flashes. The matrix trees (tree-1..3) are panels wrapped around real tree
   trunks, so they get kick rings racing up and barber-pole spirals. The spinning **peppermint** pinwheel from
   `seqs/punk-joy` crosses AllModels from bar 42 into the ending.

The user has not yet commented on v3.

## Design (the shared instrument map, kept the same in every song for cohesion)
- kick → arches (`arches_big`); snare → moving patterns on the Verts / trunk rings; cymbals → pixel forest
  (`pix-evens`/`pix-odds` alternating); bass → a dot on the `fenceline` placed by pitch; melody → `Spiral Trees`
  fill height by pitch; off-beat hits → house (`roofline-1`, windows) + floods (`grinch-1`, `Nativity Spot`) + forest.
- Colours: red/green verses, gold for the hymn's sacred moments ("come let us adore him", "Christ the Lord"),
  white for hits. Build/adore = a climb, one step per bar. "Christ the Lord" = gold meteors falling.
- Sections are in `SECTIONS` in `build.py` (intro, verse1/1b, build, ctl1, turn1, verse2/2b, adore2, ctl2, turn2,
  ending, finalctl, final).

## Open items
- **Amber**: this song still uses the shared `GOLD = '#FFAA00'` from `seqlib.py`, which reads amber on pixels. The
  user pushed back on amber in another song. kc_drummer and hailmary switched to `'#FFC832'`; do the same here
  (offered, not done yet).
- Await the user's render feedback on v3.

## Context
- xLights runs on the user's Mac (`/Users/you/xlights/show`); this Linux copy can't render. The
  user is the only one who sees the result, so ask for visual feedback.
- `tooling/README.md` documents the pipeline and shared design conventions. `seqs/tobymac-loc` is the reference
  for the current (2026) layout and file format.
