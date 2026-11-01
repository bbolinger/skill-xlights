# Where Is My Mind? (Pixies) — sequence notes

Handoff notes for whoever picks this sequence up next (human or agent). Last updated 2026-10-31.

## Status
Built and validated (2,623 effects, 0 problems). Brief: "create a light show inspired by the lyrics in this song and
by the distinct sound". **The user rendered it and called it "legit your best work so far. it's fantastic."** No
changes requested. It's the reference for how to approach songs with lyrics: find the story, give it a character,
time literal moments to the words, and give each signature sound one consistent motif.

## The song
- `mind.mp3`: 3:53 file; music ends ~222.5 s (Kim Deal's a cappella ooh). Song key `new/pixies`.
- **Played without a click.** A fixed grid drifts up to ±150 ms, so the analysis was run with
  `extract_events.py new/pixies --loose`. That option was added for this song: it follows the drummer with a beat
  tracker, and drum hits keep their real times. Measured accuracy: ~15 ms vs. 100–150 ms with the fixed grid.
  `events.json` beats are uneven, so `build.py` gets bars from `beats[phase::4]` (`B(n)`), not `t0 + n*per`.
- The tracker runs at ~164 BPM (the song feels like ~82). One "bar" in `summary.txt` = 4 tracker beats ≈ 1.46 s,
  which is half a felt bar.
- Kick and snare bands overlap on this recording. `build.py` gives each hit to whichever band it is stronger in.
- **Lyrics**: Whisper alone found only ~7 lines. With
  `lyrics.py new/pixies --model=medium.en --no-vad --prompt="Pixies song lyrics: feet in the air, ..."` (options added
  for this song) it got nearly everything. Key word times are looked up from `lyrics.json` by `word()`, and
  `sung()` snaps them to vocal note onsets because Whisper runs late. The opening "stop" was placed by hand at
  2.675 s from the vocal envelope; the "ooh" is 0.70–2.45 s.
- Sections (bars of `summary.txt`; times in `SPAN` in `build.py`):

| Bars | Section | Time (s) |
|---|---|---|
| 1–2 | ooh-stop | 0–4.2 |
| 3–9 | intro (guitar alone) | 3.8–14.8 |
| 10–17 | band in + Kim's oohs | 14.8–26.8 |
| 18–30 | verse 1 | 26.8–46.1 |
| 31–37 | chorus 1 | 46.1–56.3 |
| 38–46 | water 1 ("way out in the water", lead guitar) | 56.3–69.6 |
| 47–48 | break 1 (drums out) | 69.6–72.4 |
| 49–62 | verse 2 (Caribbean, koi) | 72.4–92.8 |
| 63–69 | chorus 2 | 92.8–103.1 |
| 70–78 | water 2 | 103.1–116.3 |
| 79–80 | break 2 | 116.3–119.4 |
| 81–87 | guitar solo (climbs to F#5 at 124–129 s) | 119.4–129.2 |
| 88–100 | verse 3 | 129.2–148.2 |
| 101–107 | chorus 3 | 148.2–158.3 |
| 108–116 | water 3 | 158.3–171.5 |
| 117 | break 3 | 171.5–172.9 |
| 118–147 | outro (Kim's oohs) | 172.9–216.7 |
| 148– | coda (a cappella ooh) | 216.7– |

- Stems:
  - Kim's falsetto oohs = vocal notes ≥ pitch 72 (`OOH_NOTES` → `OOHS` phrases)
  - Frank's melody = vocals 45–71
  - the lead guitar = top line of the guitar stem ≥ 59 (`RIFF`)

## Files
| What | Where |
|---|---|
| Sequence (generated) | `seqs/new/pixies/pixies.xsq` |
| Generator | `tooling/songs/new/pixies/build.py` (the docstring tells the whole story) |
| Analysis | `tooling/songs/new/pixies/events.json`, `summary.txt`, `lyrics.json`/`lyrics.txt`, `midi/` |

Rebuild: `cd tooling && ./run songs/new/pixies/build.py`, then `./run validate_xsq.py ../seqs/new/pixies/pixies.xsq`.
Draw a timeline to check: `./run timeline.py ../seqs/new/pixies/pixies.xsq out.png 0 60`. The builder refuses to
overwrite an .xsq edited in xLights (`--force` overrides).

## Design: the story of a mind
The character is **the mind**, a soft pink-white light (`MIND = '#FF8CF0'`).

- **"Ooh… stop"**: a lavender glow rises over the whole yard and snaps to black on "stop".
- **Guitar intro**: the riff scrolls across the Verts like sheet music; the mind appears floating in the dark and
  bursts into a ring across the yard when the drums come in.
- **Verses**: the Verts become a little world with sky, stars (Twinkle in a subbuffer) and green ground.
  - "Feet in the air": the ground slides to the top and the world is **upside down** until "spin". The pixel
    sticks bounce from the top (`direction='Down'`), the trunks run downward (`trunk_down`), the roof turns green
    and stars move onto the fence.
  - "Spin it": AllModels 3D pinwheel moment.
  - "Your head will collapse": three rings collapse inward (`shockwave(r_start=300, r_end=1)`).
  - "Nothing in it": darkness except the mind dot, which pulses on "ask yourself".
- **Choruses**: a slow 2-arm searchlight pinwheel on AllModels. On each "mind?" a sonar ping (small AllModels
  shockwave) goes out from a prop and the mind is glimpsed there: spirals in chorus 1, arches in chorus 2, little
  spirals in chorus 3, the middle Verts last. The third ping of chorus 3 is big: the mind is **found**.
- **Water**: Butterfly water and Circles bubbles on the Verts, swells through the forest, bubbles up the trunks on
  snares. The mind swims a different path each time: through the Verts then the forest; leaping the arches like a
  dolphin then along the fence; through the Verts then up the spirals.
- **Verse 2**: a Caribbean sea with a sunset above. "Animals hiding behind the rock": the sea darkens and pairs of
  green eyes blink, drawn on the **individual Vert models** (`VERTS_M`) for pixel precision. "Except the little fish":
  a coral koi darts across the forest and lands on a Vert, letting out a bubble per sung syllable.
- **Breaks**: the water drains (fills falling from 100 to 0). **Solo**: rising from the deep to the surface while the
  mind climbs with the guitar.
- **Outro**: a Butterfly aurora; Kim's oohs are lavender ghosts rising up the Verts and spiral trees; the mind
  wanders a different prop per ooh; the two loudest oohs roll a wave up the whole yard.
- **Coda**: the band is cut, ghosts follow the oohs, and the mind floats up the middle and fades. A lavender
  Nativity Spot glow is the last light.
- The sound: Kim's oohs are always ghosts; the lead guitar scrolls across the Verts coloured deep blue (low) to foam
  (high); bass is the fence dot; quiet choruses and breaks get darkness, not more light.
- Palette: night and sea (abyss, teal, turquoise, foam), dream colours (lavender, violet, magenta), coral koi, green
  ground. No amber.
- Timing tracks: Sections, **Story** (every lyric moment and what the mind is doing), Lyrics, Ooh (Kim), Bars,
  Beats, Kick, Snare, Guitar Riff.
- Exception to groups-first: the mind and koi use the individual sticks, arches and spirals; the eyes use single Verts.

## Render assumptions (the user approved the result, so these held up well enough)
1. Does the upside-down flip read?
2. Do Shockwave rings with `r_start > r_end` really shrink inward?
3. What do the Butterfly (style 1) water and Circles bubble mode look like on this layout?
4. Are the eyes on the single Verts visible over the dark sea?
5. Is the chorus searchlight (Pinwheel, brightness 45) too dim?
6. Does `Grad(..., mode='down')` render as intended?

## Library changes made for this song (backward compatible; the other songs rebuild byte-for-byte the same)
- `extract_events.py --loose`; `lyrics.py --prompt/--no-vad`
- `seqlib`: `butterfly()`, `bubbles()`, `twinkle(subbuf=)`, `fill/bounce(direction=)`,
  `shockwave(r_start=, w_start=)`, `pinwheel(bright=)`

## Context
- xLights runs on the user's Mac (`/Users/jeremy/Sync/Proj/xlights/lol2026`); this Linux copy can't render.
- `tooling/README.md` documents the pipeline and shared conventions; `seqs/new/tso_wizards/notes.md` covers the
  sprite technique this song's mind light is based on.
