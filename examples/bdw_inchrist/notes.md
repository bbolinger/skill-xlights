# In Christ (Big Daddy Weave) — sequence notes

Handoff notes for whoever picks this sequence up next (human or agent). Last updated 2026-11-01.

## Status
Built and validated (13,187 effects, 0 problems). **Not yet seen rendered by the user.** Their brief: "top that
[the Pixies show] ... check out the lyrics, the music, the key of the song, the mood of the song. Come up with
something original."

## The song
- `inchrist.mp3`: 3:52 file; music ends ~227.5 s. On a click at 117.96 BPM; bar = 2.035 s; bar n starts at
  `0.410 + (n-1) * 2.0346` s. Song key `new/bdw_inChrist`. Analysis: `extract_events.py new/bdw_inChrist`
  (no `--loose` needed); lyrics: `lyrics.py new/bdw_inChrist --model=medium.en`, which got nearly every line.
- **Key**: D major; the pre-choruses lean into B minor ("searching… a light in the dark"); the bridge builds on
  C/G/A; it **modulates to E major at bar 78 (157.07 s)** for the last chorus (checked with chroma key profiles).
- **Mood**: upbeat, confident, joyful pop-rock; drums nearly all the way through. The emotional devices are the
  **band stops**: bars 25, 33, 53, 61, 69, 98 drop the kick while the words carry the line ("He is living in my
  heart", "In Christ", "then you'll be able to say", "everything I need to be", "is in Christ"), plus a drumless
  breakdown at bars 99–101.
- Sections (`SECTIONS` in `build.py`):

| Bars | Section | Time (s) |
|---|---|---|
| 1–9 | intro | 0–18.7 |
| 10–17 | verse 1 | 18.7–35.0 |
| 18–24 | pre-chorus 1 (B minor) | 35.0–49.2 |
| 25 | stop: "living in my heart" | 49.2–51.3 |
| 26–32 | chorus 1 | 51.3–65.5 |
| 33 | stop: "In Christ" | 65.5–67.6 |
| 34–37 | guitar | 67.6–75.7 |
| 38–45 | verse 2 | 75.7–92.0 |
| 46–52 | pre-chorus 2 | 92.0–106.2 |
| 53 | stop: "able to say" | 106.2–108.2 |
| 54–60 | chorus 2 | 108.2–122.5 |
| 61 | stop: "In Christ" | 122.5–124.5 |
| 62–68 | chorus 2b (righteousness / confess / rest) | 124.5–138.8 |
| 69 | stop: "everything I need to be" | 138.8–140.8 |
| 70–77 | bridge ("In Him we live and move...") | 140.8–157.1 |
| 78–90 | chorus 3 in E | 157.1–183.5 |
| 91–97 | "everything I need to be" x3 | 183.5–197.8 |
| 98 | stop: "is in Christ" | 197.8–199.8 |
| 99–101 | breakdown (no drums) | 199.8–205.9 |
| 102– | outro | 205.9– |

## Files
| What | Where |
|---|---|
| Sequence (generated) | `seqs/new/bdw_inChrist/inchrist.xsq` |
| Generator | `tooling/songs/new/bdw_inChrist/build.py` (docstring = the whole concept) |
| Analysis | `tooling/songs/new/bdw_inChrist/events.json`, `summary.txt`, `lyrics.json`/`lyrics.txt`, `midi/` |

Rebuild: `cd tooling && ./run songs/new/bdw_inChrist/build.py`, then `./run validate_xsq.py ../seqs/new/bdw_inChrist/inchrist.xsq`.
The builder refuses to overwrite an .xsq edited in xLights (`--force` overrides).

## The concept: a light passing from heart to heart
- **The manger is the source.** The `Nativity Spot` glows the whole song. Every "In Christ" (18 of them, see the
  `In Christ` timing track) sends a ring out from the manger's position across AllModels, runs light both ways
  along the fence from the manger's spot, and flares the manger.
- **The pixel sticks are a crowd of 29 people.** A person who has the light is a soft warm body with a red
  "heart" pixel (pixel 6 of 8). The light spreads from the middle person outward on the words:
  - "living in my heart" (bar 25): 1 person
  - "...wants to live inside of you": 5
  - "take hold of the answer": 15
  - "what I confess": 21
  - "as we all live in Him": 29
  
  Each person fills up from the ground when the light reaches them. **Only people with the light dance** (bounce
  with the drums); the rest stand dim and cold, and in the pre-choruses their lights wander up and down
  (searching). Once everyone has it, the whole crowd dances (group bounces). After the key change each person's
  heart is a different colour. Track: `Crowd (light arrives)`.
- **Pixel-art hearts on the Verts.** Each single Vert (6 x 44) gets a 6 x 5 heart (rows 21–25) drawn with On
  effects in pixel-precise subbuffers. They appear on "living in my heart" on the middle two Verts, spread to
  four on "inside of you" (a streak carries them across) and to all six on "as we all". They **beat lub-dub** in
  every band stop, on each "In Christ", through the bridge and the outro, and rest at a dim glow in the choruses.
  After the key change each heart has its own colour. A pixel-art **crown** (rows 35–37) appears on "a great reward".
- **Verse 1**:
  - a small light walks along the bottom of the wall, one step per syllable ("the greatest man to walk this
    earth")
  - a beam goes to the manger on "I know who He is"
  - a meter rises only to 14 % on "may not amount to much" and shoots to the top on "but I already do to Him"
- **Verse 2**: the light puffs up on "all too prideful" and shrinks back on "something true".
- **Pre-choruses** (B minor): cold searchlights (3-arm Pinwheel) on the Verts. In pre-chorus 1 a tiny light appears
  on "a light in the dark" and opens out (H-expand) on "standing with the answer". In pre-chorus 2 a soft glow on
  "you can have peace today".
- **Chorus lines**:

| Line | Visual |
|---|---|
| "I can do all things" | every prop surges at once |
| "eagle's wings" | two wings beat up and out from the middle of the wall twice, the arches spread, the spirals climb; in E the wings span AllModels |
| "a great reward" | gold sparkles over AllModels and crowns on all Verts (gold kept for this) |
| "that I have in store" | gold fills the bottom 40 % of the wall |
| "His righteousness" | a white wash rolls up AllModels (a moment) |
| "what I confess" | VU Meter waveform: the song's own voice across the wall |
| "don't worry about all the rest" | a gentle sine wave |
| "everything I need to be" x3 | the gather tightens: arches/forest compress, then the Verts compress, then an inward ring over AllModels |
| "is in Christ" | everything falls into the hearts |

- **Bridge**: "in Him we live and move": three royal/magenta bands move through AllModels while all hearts beat.
  "Together we can sing": the whole crowd bounces in unison to the melody while the wall fills.
- **Key change (157.07 s)**: the lift. A white→cyan→magenta wave rolls up AllModels with a ring from the hearts;
  the palette steps from warm (red heart, gold, sky, warm white) to a rainbow (`E_COLS`, `E_HEARTS`).
- **Breakdown**: only the hearts, the crowd's heart pixels and the manger. **Outro**: the light pours back out
  from the manger; at the end the hearts and the manger fade, and the manger is the last light.
- Instruments underneath: kick → arches (gradient); snare → trunk rings cascading (+ Verts ripples in
  intro/guitar/outro); bass → fence dot by pitch; sung melody → spiral-tree height; house + grinch breathe.
- Palette: no amber. Gold `#FFC832` only for the reward and climbs.

## Things to check on the first render
These are unverified assumptions:
1. **Do the pixel hearts land on the right pixels?** Subbuffer edges are set just below the pixel boundaries
   (`cols()`/`rows()`). If xLights rounds differently the heart could shift by one column or row; tweak
   `cols()`/`rows()` or `HEART_ROWS`.
2. Is the stick heart pixel (pixel 6 of 8 from the bottom) visible, and does the crowd read as people?
3. Are the hearts visible over the Verts group backgrounds? Hearts are on the single Vert models; group
   backgrounds are kept ≤ 35 %.
4. Do the wings (Morph lines pivoting from the middle) read as wings?
5. The effect count is high (13k, mostly heartbeats). If rendering is slow, beat every 4 beats instead of 2
   (`heartbeat(every=...)`).

## Context
- xLights runs on the user's Mac (`/Users/jeremy/Sync/Proj/xlights/lol2026`); this Linux copy can't render.
- The user's favourites so far: `seqs/new/pixies` ("best work") and `seqs/new/tso_wizards`. Both use a character and
  lyric-timed literal moments. This song pushes further: the character is a light that multiplies.
- `seqlib.meteors(perModel=True)` was added for this song (each stick gets its own meteors).
