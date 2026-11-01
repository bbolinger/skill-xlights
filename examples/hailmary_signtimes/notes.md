# Sign of the Times (Project Hail Mary trailer version) — sequence notes

Handoff notes for whoever picks this sequence up next (human or agent). Last updated 2026-10-31.

## The song
- `sign.mp3`, supplied by the user. The user first asked me to download it from YouTube and I declined; don't
  rip audio from YouTube. 2:08, on a click at 120 BPM. Bar = 2.0 s; bar n starts at `1.560 + (n-1) * 1.9998` s.
- Structure:
  - piano and vocal for the first half
  - **band hits at 0:51**
  - "**Break into the atmosphere**" at 1:32
  - instrumental outro from 1:55
- Lyrics with timestamps: `tooling/songs/hailmary_signtimes/lyrics.txt`.

## Files
| What | Where |
|---|---|
| Sequence (generated) | `seqs/hailmary_signtimes/hailmary_signtimes.xsq` |
| Generator | `tooling/songs/hailmary_signtimes/build.py` |
| Analysis | `tooling/songs/hailmary_signtimes/events.json`, `summary.txt`, `lyrics.json`, `midi/` |

Rebuild: `cd tooling && ./run songs/hailmary_signtimes/build.py`, then validate with `./run validate_xsq.py ...`.
The builder refuses to overwrite the .xsq if it was edited in xLights (`--force` overrides). As of 2026-10-31 it is
unchanged since the last build.

## Design
The user asked me to use what I learned from `Seqs_Misc/interstellar_cornfield`: ISF shaders across the yard for
set pieces, long fades and buffer motion.
- **Palette**: deep blue, cyan and starlight, warming to gold (`#FFC832`, not amber) as the song turns hopeful.
- **Spacels** starfield fades in from black and sits under the quiet parts.
- **Cosmic Flare** at the first full-band hit (0:51).
- An "ignition" climb, then the **Hyper Space** shader across AllModels on "break into the atmosphere".
- **Galaxy** shader on the Verts in the space section and across the yard for the outro.
- The `Nativity Spot` plays the sun and is the last light out.
- Signature: on every "**Just stop your crying**", a soft white line rises up the Verts and the trunks for the
  length of the line.
- The shared instrument map: kick → arches; snare → moving patterns on the Verts; drums → pixel sticks bounce;
  bass → fence dot; voice → `Spiral Trees` fill height.
- Canvas rework (v2):
  - the melody scrolls across the Verts in the piano verses (72 of 75 notes)
  - snare ripples, smooth fill climbs, a swinging 3D spiral in Full B
  - trunks get kick rings, blue barber-pole spirals in the full band, and a breathing glow in quiet and space parts

Sections are in `SECTIONS` in `build.py` (intro, verseA, verseB, build, hit, fullA, fullB, ignition, launch, space,
after, outro).

## Open items
- Shaders come from `Seqs_Misc/interstellar_cornfield/Shaders/` (Spacels, Cosmic Flare, Hyper Space, Galaxy), which
  only works if that folder is synced to the Mac. Offered to copy them into the top-level `Shaders/` (not done yet).
- The user hasn't commented on this one after the canvas rework; await render feedback.

## Context
- xLights runs on the user's Mac (`/Users/jeremy/Sync/Proj/xlights/lol2026`); this Linux copy can't render.
- `tooling/README.md` documents the pipeline and shared conventions.
