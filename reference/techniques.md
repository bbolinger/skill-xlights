# Techniques (recipes that worked, with where to find the code)

Every recipe below is in a real build under `examples/`. Copy the helper, then adapt names to show_config.

## Anchoring to the music
- **Bars**: `B(n)` from `events.json` beats (`beats[phase + 4*(n-1)]`) - works for click tracks and `--loose`
  (uneven) beats alike. Write `SECTIONS` as bar numbers read off `summary.txt`.
- **Words**: `word('prefix', after)` returns a word's start time from `lyrics.json`; anchor every lyric moment with
  it, never with hand-typed seconds. `sung(t)` snaps to the vocal note onset just before (Whisper is ~0.1-0.4 s late).
  Lines: find the key word, walk back to the line's first word (examples/bdw_inchrist `line()`).
- **Notes**: `mono(stem, lo, hi)` = the top line of a stem. Which stem holds what varies by song (the "melody" of an
  instrumental may be in `other`; a lead guitar may sit in `vocals`); check `summary.txt` and the note CSVs.
- **Hits**: `events.json` kick/snare with `kick_v/snare_v` strengths; when the bands overlap (live recordings), give
  each hit to the band it's stronger in (examples/pixies). Skip snare ghost notes closer than ~0.6 beat.
- **Stops / band drop-outs**: bars with kick count 0 in `summary.txt`. These are the song's punctuation.

## Characters (the biggest win)
A light with a personality that travels the yard and does what the words say.
- **Sprite** (examples/tso_wizards): `vert_path` (streak panel to panel at a height, or glide within a panel, with
  a fading glow where it lands), `hop_sticks` (bounce stick to stick), `run_arch`, `climb_spiral`, `climb_trunk`,
  `sprint_fence`. Single-model rows sorted by `layout_x()`; they blend on top of group backgrounds.
- **The mind** (examples/pixies): same toolkit, softer (no sparkles, long tails) - drifts, is lost, pinged, swims.
- **The spark** (examples/owl_shine): firefly that leaps (`AllModels` Morph segments along a sine arc), walks then
  runs the fence, becomes the sun.
- **A crowd** (examples/bdw_inchrist): each pixel stick is a person (dim body + one bright "heart" pixel). A light
  spreads person to person on lyric cues (`SPREAD` schedule: (t0, t1, how many lit), centre outward), and only lit
  people dance with the drums.
Give it a timing track (`Sprite`/`Story`) so the user can follow it in xLights.

## Canvas (matrix wall) motion - never flash panels
Repertoire (choose per song): melody scrolling right-to-left like sheet music (`melody_scroll`, needs ~8-12 spare
layers); ripples from a wandering point on the snare; bands sliding (`bars Left/Right`); diagonal sweeps (`DIAG`);
H-expand / H-compress bursts; smooth fill climbs; swinging 3D spirals; a character gliding panel to panel; ghosts
(a band rising with long tails, one per sustained "ooh"); a sky gradient that changes every bar (examples/owl_shine
`SKY_KEYS`); the VU waveform; Butterfly water/aurora; starfields (Twinkle in the top part).

## Pixel art on matrices
On effects in pixel-exact subbuffers on the single matrix models (examples/bdw_inchrist `art()`, `heart()`,
`crown()`): a 6x5 heart, a crown. Edges just below pixel boundaries. Beat it with brightness (lub-dub: 100→55 for
0.17 s, 90→25 for 0.28 s, rest). Needs one layer per row-segment; keep resting copies on separate layers from the
beating ones or the beats clip them. Effect counts get big - fine for xLights, but don't go wild.

## Words on a matrix (examples/bdw_joy)
A bold 6x7 pixel font (`FONT`), letters stacked top to bottom on a tall 6x44 panel - a vertical marquee sign. Each
glyph is decomposed into rectangles (`rects()`: row runs merged downward), one On effect each in a pixel-exact
subbuffer (`cell()`), so a 5-letter word needs ~25 layers on that single model. Phrases are detected in
`lyrics.json` with templates (first word + following words within 4 s) and spelled one word per panel as sung;
each panel keeps its word until the next line's word for that panel replaces it (otherwise fast lines blink).
Words of 5 letters or fewer fit 44 rows (7 per letter + 2 gap). An alternative is xLights' Text effect with an OS
font across the whole canvas (what the user's older sequences do).

## Story devices
- **Upside-down world** (pixies): the canvas is a scene (sky, stars in a subbuffer, ground band); a Morph band
  carries the ground to the top; sticks bounce with `direction='Down'`; trunk rings run down; roof and fence swap roles.
- **Collapse / nothing** (pixies): inward shockwaves, then cut everything but one small light.
- **Search / found** (pixies): a dim 2-arm searchlight pinwheel on the whole yard; a small "sonar" ring from a
  different prop each time the question is sung; the last one is big.
- **Progressive reveal** (owl_shine): the fence is "the way" - each "your way" lights another stretch until the
  line that completes it. Anything counted in the lyrics can be a progress bar on some prop.
- **Source of light** (bdw_inchrist): one prop (the manger spot) is where light comes from; every refrain sends a
  ring out from its position across the whole yard and along the fence both ways.
- **Tears dry in the sun** (owl_shine): blue Meteors down, then a warm fill rises and gold Meteors float up.
- **Rising sun** (owl_shine): a radial-out gradient (white→gold→pink→black) On in a subbuffer stepped upward across
  the whole-yard group, plus slow thin-armed pinwheel rays.
- **Call and response** (tso_wizards, from the user's joy_daddyweave): the band phrase lights the yard, the reply
  happens alone in the dark (`cut` the stop bar, then one character answers).
- **Lift** at a key change (bdw_inchrist, owl_shine): a whole-yard wave up + ring, and the palette steps up.

## Moments and contrast
- A handful of whole-yard moments per song at the structural peaks; everything else stays on groups.
- Quiet passages get *less* light: darkness, one character, the song's voice. The contrast is what makes the
  chorus land.
- End with one light left (the user's show: the Nativity spot is always the last light out).
