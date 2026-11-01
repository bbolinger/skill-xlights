# Little Drummer Boy (for KING & COUNTRY) — sequence notes

Handoff notes for whoever picks this sequence up next (human or agent). Last updated 2026-10-31.

## The song
- `kc_drummer.mp3`: 4:48, on a click at 104.0 BPM, D major. Bar = 2.3075 s; bar n starts at
  `0.647 + (n-1) * 2.3075` s (`tooling/songs/kc_drummer/summary.txt`).
- Structure:
  - drum roll 0–3 s, then the drum intro to 0:24
  - verse 1 with no drums; verse 2 with light drums
  - breakdowns (voice + pad only) at 1:05, 2:05 and 3:14
  - full choruses 1:12–2:05 and 2:12–3:14
  - **total silence 3:24–3:26**, then a guitar interlude
  - drums return with a build at 3:35, final chorus at 3:45, drum feature at 4:24, outro to 4:42

## Files
| What | Where |
|---|---|
| Sequence (generated) | `seqs/kc_drummer/kc_drummer.xsq` |
| Generator | `tooling/songs/kc_drummer/build.py` (also the template other songs were copied from) |
| Analysis | `tooling/songs/kc_drummer/events.json`, `summary.txt`, `lyrics.json`/`lyrics.txt`, `midi/` |

Rebuild: `cd tooling && ./run songs/kc_drummer/build.py`, then `./run validate_xsq.py ../seqs/kc_drummer/kc_drummer.xsq`.
The builder refuses to overwrite the .xsq if it was edited in xLights (`--force` overrides). As of 2026-10-31 it is
unchanged since the last build.

## History and user feedback
- Asked to learn from `seqs/tobymac-marysboy`: **sine waves rolling across the pixel sticks** and **gradients** (colour
  curves) for colour variety. Both were added.
- **"Pa rum pum pum pum"** signature: the user wanted a pronounced repeating element. Per-Vert steps and then a
  straight line sweeping up/down both felt too weak. The user's idea, now built: **the song's own VU Meter
  waveform, jagged across the whole Vert canvas** while it's sung. The last "pum" bursts gold up the wall, with the
  spiral trees and Nativity Spot joining. Whisper (`medium.en`) found 19 hooks, **all before 3:24**. It lost the
  lyrics after the silence.
- **Pixel sticks bounce with the drums** (Fill per stick, height from hit strength; kick → `pix-evens`,
  snare → `pix-odds`) in drum-driven sections.
- From `Seqs_Misc/interstellar_cornfield`:
  - Spacels starfield shader under the three breakdowns
  - Cosmic Flare across AllModels at the final chorus (3:45)
  - Sleepy Rays (`Shaders/`) as the ending
  - a 4 s fade-in for verse 1
- **"You're using a lot of that amber color"**: gold changed from `#FFAA00` to `#FFC832`, and amber was taken out of
  the gradients. Gold is reserved for meaningful moments.
- Canvas rework (v4):
  - no panel flashing on the Verts or trees
  - the melody scrolls across the Verts like sheet music in quiet verses, breakdowns and the guitar interlude
  - snare ripples, smooth fill climbs
  - trunks get kick rings, barber-pole spirals in the choruses, and a breathing glow in quiet parts
  - the DreamsOfFireflies **whirl** plays over the 2-bar drum feature, and a swinging 3D spiral runs on the Verts
    in chorus 2b

The user hasn't given feedback on the latest version yet.

## Design
- The shared instrument map: kick → arches; snare → moving patterns on the Verts / trunk rings; cymbals → pixel
  forest; bass → fence dot by pitch; voice → `Spiral Trees` fill height; off-beats → house + floods.
- Song-specific:
  - candle-warm quiet verses
  - breakdowns spotlight the **Nativity Spot** and climb into the next chorus
  - **blackout for the 3:24 silence**
  - 8 AllModels moments at the big entrances
  - the manger spot is the last light out

## Open items
- **"Pa rum pum pum pum" hooks after 3:24 are missing** because Whisper lost the lyrics there. Either get timestamps
  from the user, or try `tooling/lyrics.py kc_drummer --model=medium.en --no-vad --prompt="pa rum pum pum pum, little
  drummer boy, ..."`. That trick recovered nearly every line of the Pixies song. `build.py` finds the hooks
  automatically from `lyrics.json` (runs of ≥4 pa/rum/pum words, snapped to sung notes), so a better `lyrics.json`
  plus a rebuild adds them. Check `lyrics.txt` first, because the new transcript replaces the old one.
- Shaders are referenced from `Seqs_Misc/interstellar_cornfield/Shaders/` (`Spacels.fs`, `Cosmic Flare.fs`). That
  only works if that folder is synced to the Mac. Offered to copy them into the top-level `Shaders/` (not done yet).
- Await render feedback.

## Context
- xLights runs on the user's Mac (`/Users/jeremy/Sync/Proj/xlights/lol2026`); this Linux copy can't render.
- `tooling/README.md` documents the pipeline and shared conventions.
