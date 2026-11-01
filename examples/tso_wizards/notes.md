# Wizards in Winter (Trans-Siberian Orchestra) — sequence notes

Handoff notes for whoever picks this sequence up next (human or agent). Last updated 2026-10-31.

## Status
**The user rendered it and said "that looked great!"** No changes were requested. Treat it as done unless they
ask for more, and change it carefully.

## The song
- `wis.mp3`: instrumental, on a click at 148.4 BPM, 186 s (music ends ~182.2 s). Bar = 1.617 s; first beat 0.315 s,
  phase 0. Song key in the tooling is `new/tso_wizards` (the slash works).
- Built around **call and response**: the band plays three bars, then a **stop bar** (one stab + a ~6-note piano
  run). There are 22 stop bars (`STOPS` in `build.py`).
- Where the parts are:
  - the theme melody is in the `other` stem (`THEME`, pitch 60–90)
  - the middle lead melody is in the `vocals` stem (`LEAD`)
  - the stop-bar runs are in `piano` (`PIANO`)
  - the guitar stem is just E3 chugs
- Piano breakdown bars 58–61; busy drum section 62–77; ending hammer hits ~174.1–178.2 s, silence, then the final
  hit at 181.42 s.

## Files
| What | Where |
|---|---|
| Sequence (generated) | `seqs/new/tso_wizards/tso_wizards.xsq` |
| Generator | `tooling/songs/new/tso_wizards/build.py` |
| Analysis | `tooling/songs/new/tso_wizards/events.json`, `summary.txt`, `midi/` (`extract_events.py new/tso_wizards --melody=guitar`) |

Rebuild: `cd tooling && ./run songs/new/tso_wizards/build.py`. It refuses to overwrite an .xsq edited in xLights
(`--force` overrides). As of 2026-10-31 it is unchanged since the last build.

## Design
Brief: "Get creative. Use more color. Make it feel like there's a sprite dancing across the yard through the song."
The timing ideas came from `seqs/joy_daddyweave` (call and response, alternating directions, big lights breathing).

**The sprite**: a white-hot spark with a rainbow trail. It's drawn on individual models on top of the group
effects; this relies on xLights ModelBlending, and it rendered fine. It uses the 29 `pixstk-*`, 4 `arch-big-*` and
4 spiral models, sorted left to right with `seqlib.layout_x()`.
- **Stop bars**: everything is cut. The stab sends an AllModels ring, and the trunks and house answer it. Then the
  sprite **hops Vert to Vert with each piano note** (height by pitch, direction alternating each stop). Helpers:
  `vert_path`, `vert_glow`.
- **Band phrases** (runs of non-stop bars, max 3 bars) cycle through modes, alternating direction:
  - forest: hopping stick to stick on the eighth notes (`hop_sticks`)
  - arches: over the arches, then up the spiral trees (`run_arch`, `climb_spiral`)
  - fence: up the trunks (`climb_trunk`), then sprinting along the fence (`sprint_fence`)
- **Lead melody**: xylophone on the pixel sticks, low notes left and high notes right.
- **Drum drive**: bounces over an arch on every snare.
- **Piano breakdown**: drifts down the Verts through falling snow.
- **Finale**: twin sprites cross the forest.
- **Ending**: the sprite gathers in the silence and flies into the last hit.

**Colour**: jewel tones per section (magenta, violet, blue, cyan, emerald, red), with no amber or orange. The
melody scrolls across the Verts in rainbow colours by pitch (12-colour `WHEEL`, circle of fifths).

**Yard-wide moments**:
- rainbow shockwaves on the band hits
- a 6-colour DreamsOfFireflies whirl in the heavy riff
- snowfall in the breakdown
- the `Shaders/Statis Spiraling.fs` rainbow when the finale kicks in
- rings on the hammer hits, then a final burst

Timing tracks: Sections, **Sprite** (what the sprite is doing), **Stops (call & response)**, Bars, Beats, Kick,
Snare, Theme/Lead/Piano notes.

## Lessons kept for other songs
- A travelling character plus call-and-response gaps works well on this yard. The sprite helpers in `build.py` are
  reusable (the Pixies song copied the pattern for its "mind" light).
- The sprite on individual models over group backgrounds shows up fine.
