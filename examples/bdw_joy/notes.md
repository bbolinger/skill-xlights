# Joy to the World (Big Daddy Weave) — sequence notes

Handoff notes for whoever picks this sequence up next (human or agent). Last updated 2026-11-01.

## Status
Built and validated (7,011 effects, 0 problems). **User feedback (render 1): "the colors are looking more subdued than they should"** → v2: colours blend within their family (`rich()`/`PARTNER`) instead of toward white, no red→green gradients (olive midpoint on the arches), the wall behind the words is a 40 % deep-blue sky (was 18 % red/green), house/trunks/sticks/fence brighter, words in red/green/gold instead of mostly white. v2 not yet re-rendered. Brief: "with everything
learned, now try seqs/bdw_joy". It's the same song as `seqs/joy_daddyweave` (someone else's sequence, which the user
liked for its call-and-response timing and which spells JOY with the Text effect). This is an original take, not
a copy of it.

## The song
- `joy_bigdaddyweave.mp3`: 204.9 s file, music ends ~198.5 s. On a click at 95 BPM; bar = 2.527 s; bar n starts at
  `2.120 + (n-1) * 2.5266` s. **D major** throughout (`analyze_key.py`).
- Lyrics: `lyrics.py bdw_joy --model=medium.en --no-vad --prompt="Joy to the world, the Lord is come, ... He shall reign
  forever, see the shepherds bowing down, wise men offer Him their crown, go tell the world, tell everyone, God sent
  His Son"`. Without the prompt Whisper lost the opening lines. Verse 2's "He shall reign forever" answers are
  merged into other words in `lyrics.json`, so the build places them on bars 29/31/33/35 (+0.5 s, snapped to the
  vocal onset).
- Sections (`SECTIONS` in `build.py`):

| Bars | Section | Time (s) |
|---|---|---|
| 1–9 | intro ("Joy to the world" hook at 13.6) | 0–24.9 |
| 10–17 | verse 1 (rejoice / King / earth & angels / glory / majesty / He shall reign) | 24.9–45.1 |
| 18–26 | chorus 1 (4 lines, 2 bars each) | 45.1–67.8 |
| 27 | hush | 67.8–70.3 |
| 28–35 | verse 2: call (even bars) and response "He shall reign forever" (odd bars) | 70.3–90.6 |
| 36–44 | chorus 2 | 90.6–113.3 |
| 45–47 | bridge (quiet) | 113.3–120.9 |
| 48–53 | chant "He shall reign forever and ever" | 120.9–136.0 |
| 54–56 | JOY climax (high notes) | 136.0–143.6 |
| 57–59 | drums and voice only | 143.6–151.2 |
| 60–76 | final chorus + "the Lord is come" tag | 151.2–194.1 |
| 77– | end | 194.1– |

## Files
| What | Where |
|---|---|
| Sequence (generated) | `seqs/bdw_joy/bdw_joy.xsq` |
| Generator | `tooling/songs/bdw_joy/build.py` (docstring = the concept) |
| Analysis | `tooling/songs/bdw_joy/events.json`, `summary.txt`, `lyrics.json`/`lyrics.txt`, `midi/` |

Rebuild: `cd tooling && ./run songs/bdw_joy/build.py`, then `./run validate_xsq.py ../seqs/bdw_joy/bdw_joy.xsq`.

## The concept: the yard spells out the news and carries it
- **Words on the wall.** The middle four Verts are vertical marquee signs. Each chorus phrase is spelled one word
  per panel, letters stacked top to bottom, in a bold 6x7 pixel font (`FONT` in `build.py`). Each word appears as
  it's sung and stays until the next line's word for that panel replaces it. Phrases: JOY TO THE WORLD, THE LORD
  IS COME, GOD SENT HIS SON, GO TELL THE WORLD, TELL EVERY ONE. They're detected from `lyrics.json` by
  `SPELL` templates.
  
  Each letter is decomposed into rectangles (`rects()`), and each rectangle is one On effect in a pixel-exact
  subbuffer on the single Vert model (`cell()`). Letters use layers 0–27 on the single Verts. The two outer panels
  twinkle like stars beside the sign.
- **The manger is the source of the news.**
  - "the Lord is come": a ring from the manger across AllModels, and the manger flares.
  - "God sent His Son": a star streaks down from the sky (top of AllModels) to the manger.
  - "go, tell the world": heralds run out from the manger along the fence both ways, over the arches right to
    left, and through the sticks.
  - "tell everyone": a ring over the whole yard, the spirals climb, and the house flashes.
- **"He shall reign forever" = crowns.** A gold pixel crown on all six Verts with every answer (verse 1 end, 4× in
  verse 2). In the chant the crowns climb a step each bar while gold fills the wall, trunks rise and the sticks
  bounce higher.
- **Verse 1 scene**:
  - "rejoice": sparkle bursts on the spirals and arches
  - "King": a crown on the middle panels
  - "men of earth": the fence glows green, left to right
  - "angels cheer": white light drifts down the wall
  - "glory": gold rays and a slow gold ring from the manger
  - "majesty in a manger's light": everything goes dark except the manger and a warm glow along the fence
- **Verse 2 call and response**:
  - shepherds: the sticks light and bow one after another toward the manger
  - wise men: a crown carried panel to panel to the manger
  - "then till now and far beyond": a light runs the whole fence and off the end
  - "endless song": a slow pinwheel turns over everything
  - each answer: crowns
- **JOY climax**: a rainbow wave up AllModels, then JOY spelled on all six panels in rainbow on every "joy".
- **Drums and voice**: everything dark. Each kick sends a ring from the manger; each snare bounces the whole crowd
  of sticks. The words keep spelling.
- **Final chorus**: words and kicks in rainbow. **End**: an inward ring into the manger, JOY on all panels fading,
  and the manger is the last light.
- Instruments underneath:
  - kick → arches (red/green, rainbow in the finale)
  - snare → trunk rings (red/white/green)
  - bass → fence dot
  - melody → spiral heights
  - choruses: the sticks bounce, with candy-cane barber poles on the trunks

## Things to check on the first render
These are unverified:
1. **Do the letters read?** Each letter is 6 x 7 pixels, stacked vertically on a 6 x 44 panel. If they land one
   pixel off (subbuffer rounding), adjust `cell()`. If the words go by too fast, hold them longer (the `+4.5`
   caps) or spell fewer words.
2. Is the Verts background (18 % swing spirals in the choruses) dim enough behind the letters?
3. Does the star coming down to the manger ("God sent His Son") read across the yard?
4. Effect count: about 5,900 On effects for letters. If rendering is slow, drop the fade-out halves in `draw()`.
