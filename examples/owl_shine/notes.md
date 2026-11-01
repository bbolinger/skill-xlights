# Shine Your Way (Owl City & Yuna, from The Croods) — sequence notes

Handoff notes for whoever picks this sequence up next (human or agent). Last updated 2026-11-01.

## Status
Built and validated (2,827 effects, 0 problems). **The user rendered it: "i like it!"** No changes requested. Brief: "work on that one"
(after In Christ, which the user liked but ranked below Pixies "because the song is just better").

## The song
- `shine.mp3`: 205.9 s file, music ends ~205.5 s (last chord rings from 201 s). On a click at 120 BPM; bar = 2.0 s;
  bar n starts at `1.160 + (n-1) * 1.9998` s. Song key `new/owl`. `extract_events.py new/owl`;
  `lyrics.py new/owl --model=medium.en` got every line.
- **Key**: C# major; the bridge leans on A# minor; **key change up a whole step to Eb major at bar 71 (141.15 s)**,
  right after "darkness is fading, we've found our way to the light, it's such a beautiful sight".
- **Mood**: bright, hopeful, sparkly electropop. Four-on-the-floor kick, synth sparkle in the `other` stem, no drums
  until bar 12 (23.15 s). Guitar and piano stems are nearly empty.
- Sections (`SECTIONS` in `build.py`):

| Bars | Section | Time (s) |
|---|---|---|
| 1–3 | night (synth) | 0–7.2 |
| 4–11 | "just before the dawn" (no drums) | 7.2–23.2 |
| 12–19 | verse 1 | 23.2–39.2 |
| 20–27 | pre-chorus (tears / sun / starting today) | 39.2–55.2 |
| 28–31 | shine chorus | 55.2–63.2 |
| 32–33 | synth hook | 63.2–67.2 |
| 34–49 | verse 2 (open sky… leap of faith) | 67.2–99.2 |
| 50–57 | pre-chorus 2 (walk / run / nothing in your way) | 99.2–115.2 |
| 58–61 | shine chorus | 115.2–123.2 |
| 62–63 | synth hook | 123.2–127.2 |
| 64–70 | bridge: sunrise | 127.2–141.2 |
| 71–85 | daybreak, Eb (anytime anywhere / star / show me the way) | 141.2–171.2 |
| 86–100 | final chorus | 171.2–201.1 |
| 101– | end | 201.1– |

## Files
| What | Where |
|---|---|
| Sequence (generated) | `seqs/new/owl/shine.xsq` |
| Generator | `tooling/songs/new/owl/build.py` (docstring = the whole concept) |
| Analysis | `tooling/songs/new/owl/events.json`, `summary.txt`, `lyrics.json`/`lyrics.txt`, `midi/` |

Rebuild: `cd tooling && ./run songs/new/owl/build.py`, then `./run validate_xsq.py ../seqs/new/owl/shine.xsq`.
The builder refuses to overwrite an .xsq edited in xLights (`--force` overrides).

## The concept: the whole song is one sunrise, led by a spark
- **Sky clock** (`SKY_KEYS`, `sky(t)`): every bar the Verts show a sky gradient from the horizon up. The roofline
  takes the overhead colour and the windows the horizon colour. The sky goes:
  - night with stars → indigo → violet twilight (chorus 1) → blue "open sky" (verse 2) → pink dawn (chorus 2)
  - the sunrise in the bridge, then daylight after the key change
  
  Arches, trunk rings and spiral heights all take the horizon colour before the key change and Owl City candy
  colours (`CANDY`) after it.
- **The spark**: firefly green `#D4FF5A`, a nod to Owl City and the show's DreamsOfFireflies.
  - It drifts alone in the dark, flares on each "shine", and dithers left and right on "you may not know where to go".
  - It goes to the start of the road on "open road", and a **Fire** effect grows at the bottom of the Verts on
    "build a fire from a spark", flaring on "feed".
  - "don't conceal it": the wall goes dark. "find your way": the spark runs the fence and the forest.
  - In verse 2 it rises in the spiral trees on "feeling deep inside" and leads across the wall on "guide".
  - **Leap of faith**: an arc over the whole AllModels canvas, then "fly, fly away" up the spirals and off the top.
  - Pre-chorus 2: walks, then runs back and forth along the fence; "nothing can get in your way" bursts it through
    the four arches.
  - In the bridge it settles at the horizon and becomes the sun.
- **The road** is the fence. Each of the 10 "way"s before the bridge lights another stretch of it, left to right,
  and it completes on "we've found our way to the light". After that it stays lit.
- **"Shine, shine, shine, shine"**: each shine bursts from the next arch (left to right) with a ring across the yard
  and a spiral climb. The count restarts on each line.
- **Tears / sun** (both pre-choruses and the day section): blue meteors fall on the Verts and trunks. On "sun" a
  warm fill rises and gold sparkles float up. "starting today" draws a horizon line.
- **Bridge sunrise**:
  - "breaking" cracks the horizon open from the middle, on the wall and the fence
  - stars fade on "darkness is fading"
  - a sun disk (radial gradient) rises over AllModels in 16 steps from "light" to the key change, with slow sun
    rays on the Verts
- **Key change** = daybreak: a ring and a wave of gold to white to sky over AllModels.
- **Day section**:
  - "anytime, anywhere": little rings pop all over the yard
  - "turn around": a pinwheel
  - "like a star burning bright…darkest night": the sky dims to night and an 8-arm star spins on the wall
  - "show me the way": light walks the arches and the road
  - "tears dry in the sun": a yard-wide sun burst
- **Final chorus**: "we're on our way" runs the road and forest; "that's what we say" flashes the house pink;
  "there's a reason why you shine" makes the arches and spirals sparkle. The last "shine your way" is a 6-colour 3D
  pinwheel over everything. At the end a sun glow on the wall and the Nativity Spot fade last.
- **Owl City's synth**: synth notes (`other` stem) glint on single pixel sticks, spread across the forest by how
  common each pitch is. They play in the night/dawn intro, the synth hooks and the bridge.

## Render assumptions (the user liked the result, so these held up well enough)
1. **The Fire effect** (verse 1): it's real fire colours, so orange/yellow. The user disliked overused amber; this
   is ~8 s and literal. If it bothers them, raise `E_SLIDER_Fire_HueShift` in `fire_fx()` toward pink, or shorten it.
2. The rising sun: On effects with a radial gradient fading to black, in subbuffers stepping up AllModels. Does it
   read as a disk?
3. Does the sky clock read? Verts sky brightness is 30–65 %. Is the night too dark or the day too washed out?
4. The leap-of-faith arc on AllModels (Morph segments along a sine arc).
5. The road on the fence (layer 2 at 35 %) under the bass dots.

## Library changes made for this song
- `Seq.write()` now trims anything past the end of the audio. Earlier songs rebuild byte-identical.
