"""Sign of the Times (the Project Hail Mary trailer version) -> seqs/hailmary_signtimes/hailmary_signtimes.xsq

Space theme, using what Seqs_Misc/interstellar_cornfield does: ISF shaders across the yard for the set pieces
(a starfield fading in from black, a solar flare at the first full-band hit, hyperspace on "break into the
atmosphere", a spiral galaxy drifting away at the end), long fades, and a deep-blue / cyan / starlight palette
that warms to gold as the song turns hopeful.
Same instrument map as the other songs: kick=arches, snare=moving patterns on the Verts, drums=pixel sticks
bounce, bass=fence dot, voice=spiral fill height. Verts are one canvas (no panel flashing): the sung melody scrolls
across them in the quiet parts, snares ripple. The matrix trees are trunks: rings race up them on kicks, they
breathe in the quiet parts and wear blue barber-pole stripes in the full band. Signature: every "Just stop your
crying" a soft white line rises up the Verts (and the trunks) for the length of the line.

usage: build.py [out.xsq] [timeline.json] [--force]
"""
import json, re, sys, bisect
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from seqlib import *

SONG = 'hailmary_signtimes'
HERE = song_dir(SONG)
ARGS = cli_args()
OUT = ARGS[0] if ARGS else str(SHOW / 'seqs' / SONG / f'{SONG}.xsq')
ev = json.load(open(HERE / 'events.json'))
words = json.load(open(HERE / 'lyrics.json'))
T0, PER = ev['t0'], ev['per']
BAR = 4 * PER
B1 = T0 + ev['phase'] * PER
B = lambda n: B1 + (n - 1) * BAR            # start of 1-based bar n (2.0 s at 120 BPM)
DUR, END = 128.31, ev['end']

sq = Seq(ELEMENTS, nlayers=15)               # layers 3-14 carry the melody scrolling across the Verts
SCROLL_LAYERS = range(3, 15)
SH = 'Seqs_Misc/interstellar_cornfield/Shaders'

# ---------------------------------------------------------------- colours: space blues, starlight, and the sun
BLUE, CYAN, ICE = '#1E50FF', '#00E5FF', '#BFFFFF'
GOLD = '#FFC832'                    # a gold that stays gold on pixels (the shared #FFAA00 reads amber)
FAMILY = {BLUE: ('#000060', BLUE, '#46A3FF'), CYAN: ('#007DFB', CYAN, ICE), ICE: ('#46A3FF', ICE, WHITE),
          WHITE: ('#BFD9FF', WHITE, WHITE), GOLD: ('#E0A800', GOLD, '#FFF0C0')}
G = lambda c, mode: Grad(*FAMILY[c], mode=mode)
tip = lambda c: Grad(FAMILY[c][0], c, WHITE, mode='up')

def word_time(w, after=0.0):
    return next(x for x in words if re.sub(r'[^a-z]', '', x['word'].lower()) == w and x['start'] >= after)
LAUNCH = word_time('break', 90)['start']                    # "Break into the atmosphere"
GOOD_FROM_HERE = word_time('and', LAUNCH + 1)['start']      # "And it all looks good from here"

# ---------------------------------------------------------------- sections
quiet = dict(voice=CYAN, voice_steps=ICE, steps_bright=80, tree_breathe=BLUE, bass=BLUE, bass_bright=60, verts_bg=('wave', BLUE, 25),
             stars=True, house_bg=(BLUE, 20), nativity=(GOLD, 20))
full = dict(kick=BLUE, snare=WHITE, bounce=True, tree_spirals=True, bass=CYAN, voice=WHITE, off=True, house_bg=(BLUE, 35),
            nativity=(GOLD, 40), grinch=(GREEN, 20))
space = dict(voice=WHITE, stars=True, galaxy=True, tree_breathe=CYAN, kick=BLUE, kick_bright=50, bass=BLUE, bass_bright=70,
             house_bg=(BLUE, 25), nativity=(GOLD, 50))
SECTIONS = [
    ('intro', 0.0, B(3), {}),
    ('verseA', B(3), B(11), dict(quiet, bg_fadein=3)),
    ('verseB', B(11), B(19), dict(quiet, verts_bg=('bars', 'Right', BLUE, 25, 4))),
    ('build', B(19), B(26), dict(kick=BLUE, kick_bright=70, snare=CYAN, snare_mode='ripple', bounce=True, bass=BLUE,
                                 voice=CYAN, climb=CYAN, stars=True, house_ramp=CYAN, nativity=(GOLD, 25))),
    ('hit', B(26), B(27), {}),
    ('fullA', B(27), B(35), dict(full, snare_mode='diag', verts_bg=('bars', 'Left', BLUE, 40, 4), bg_forest=(BLUE, 15),
                                 forest_waves=(2, CYAN))),
    ('fullB', B(35), B(43), dict(full, kick=CYAN, snare=GOLD, snare_mode='xc', voice=GOLD, verts_bg=('swing', CYAN, 40),
                                 bg_forest=(CYAN, 15), house_bg=(GOLD, 30), forest_waves=(1, GOLD))),
    ('ignition', B(43), LAUNCH, dict(kick=GOLD, snare=GOLD, snare_mode='ripple', bounce=True, bass=GOLD, voice=GOLD,
                                     climb=GOLD, house_ramp=GOLD, nativity_ramp=GOLD)),
    ('launch', LAUNCH, GOOD_FROM_HERE, {}),
    ('space', GOOD_FROM_HERE, B(51), space),
    ('after', B(51), B(58), dict(space, snare=CYAN, snare_mode='ripple', snare_bright=50, bounce=True, bounce_bright=50)),
    ('outro', B(58), DUR, {}),
]
SEC_START = [s for _, s, _, _ in SECTIONS]
def section(t):
    return SECTIONS[max(bisect.bisect_right(SEC_START, t + 0.001) - 1, 0)]

# ---------------------------------------------------------------- drums
kicks = ev['kick']
for i, t in enumerate(kicks):
    name, s0, s1, st = section(t)
    if st.get('kick'):
        d = max(nxt(kicks, i, 0.30), 0.075)
        sq.flash(ARCHES, 0, t, d, G(st['kick'], 'right'), bright=st.get('kick_bright', 100))
        sq.trunk_ring(t, max(d, 0.2), st['kick'], tree=i % 3, bright=st.get('kick_bright', 100))

snares, n = ev['snare'], 0
for i, t in enumerate(snares):
    name, s0, s1, st = section(t)
    if not st.get('snare'): continue
    d = max(nxt(snares, i, PER), 0.075); c = st['snare']; br = st.get('snare_bright', 100)
    mode = st.get('snare_mode')
    if mode == 'ripple':          # a ring spreads across the wall from a point that wanders left and right
        sq.ripple('Verts', 0, t, max(d, PER), [WHITE, c], VERT_X[pingpong(n, 6)], 35 if n % 2 else 65)
    elif mode == 'xc':
        sq.bars('Verts', 0, t, t + max(d, PER / 2), 'H-expand' if n % 2 == 0 else 'H-compress', [G(c, 'up'), BLACK], 1, 1, br)
    elif mode == 'diag':
        a, b = DIAG['up-right' if n % 2 == 0 else 'up-left']
        sq.morph('Verts', 0, t, t + max(d, PER / 2), [WHITE, c], a, b, tail_end=40, bright=br)
    n += 1

for grp, times, vals, key in (('pix-evens', ev['kick'], ev['kick_v'], 'kick'), ('pix-odds', ev['snare'], ev['snare_v'], 'snare')):
    for i, (t, v) in enumerate(zip(times, vals)):
        name, s0, s1, st = section(t)
        if not st.get('bounce') or not st.get(key): continue
        d = min(max(nxt(times, i, 0.45), 0.15), 0.45)
        px = round(2 + max(v - 0.35, 0) / 0.65 * 6)
        sq.bounce(grp, 1, t, t + d, [tip(st[key])], height=12.5 * px, bright=st.get('bounce_bright', 100))

offs = ev['off']
for i, t in enumerate(offs):
    name, s0, s1, st = section(t)
    if st.get('off'): sq.flash(HOUSE + FLOODS, 0, t, max(nxt(offs, i, PER / 2), 0.075), WHITE)

# ---------------------------------------------------------------- bass -> fence dot
bass = [(t, midi(nm)) for t, e, nm in ev['bass']]
bt = [t for t, _ in bass]
for i, (t, p) in enumerate(bass):
    name, s0, s1, st = section(t)
    if not st.get('bass'): continue
    pos = 5 + (min(max(p, 28), 52) - 28) / 24 * 90
    sq.flash('fenceline', 0, t, max(nxt(bt, i, 2 * PER), 0.075), Grad(WHITE, st['bass']), bright=st.get('bass_bright', 100),
             subbuf=sub(max(pos - 5, 0), 0, min(pos + 5, 100), 100), end_level=30)

# ---------------------------------------------------------------- voice -> spiral height; in quiet parts syllables step across the Verts
vox = [(t, midi(nm)) for t, e, nm in ev['vox']]
vt, n = [t for t, _ in vox], 0
scroll_notes = []
for i, (t, p) in enumerate(vox):
    name, s0, s1, st = section(t)
    d = max(nxt(vt, i, 2 * PER), 0.075)
    if st.get('voice'):
        h = 10 + (min(max(p, 55), 79) - 55) / 24 * 90
        sq.on('Spiral Trees', 1, t, t + d, tip(st['voice']), 100, 70, subbuf=sub(0, 0, 100, h), perModel=True)
    if st.get('voice_steps'):
        scroll_notes.append((t, p, min(d, PER), [WHITE, st['voice_steps']], st.get('steps_bright', 80)))
# the sung melody glides right to left across the Verts at the height of its pitch, like sheet music
placed = sq.melody_scroll('Verts', scroll_notes, None, travel=1.5 * BAR, lo=55, hi=79, layers=SCROLL_LAYERS)
print(f'melody scroll: {placed} of {len(scroll_notes)} notes placed')

# ---------------------------------------------------------------- per-section backgrounds and set pieces
STARS = dict(brightness=0.25, density=0.75, depth=0.25, distfading=0.25, morph=0.89, rate=0, saturation=0.5, zoom=2.5,
             moveX=0, moveY=0)
GALAXY = dict(COLOUR=1, CentralCore=0.9, CoreHaze=0.06, CoreIntensity=0.9, DustDensity=0.02, ITERATIONS=80, SPIRAL=0.87,
              STRUCTURE=0.65, ShiftX=0.5, ShiftY=0.5, StarsBlue=0.51, StarsGreen=0.56, TIMEOFFSET=0, TINT=1, ZOOM=0.1)
for name, s0, s1, st in SECTIONS:
    if 'bg_forest' in st: sq.on(FOREST, 2, s0, s1, G(st['bg_forest'][0], 'radial-out'), bright=st['bg_forest'][1])
    vb = st.get('verts_bg')
    if vb and vb[0] == 'bars':
        _, direction, c, br, cyc = vb; sq.bars('Verts', 2, s0, s1, direction, [G(c, 'up'), BLACK], 2, cyc, br)
    elif vb and vb[0] == 'wave':
        _, c, br = vb; sq.wave('Verts', 2, s0, s1, c, br, colors=[G(c, 'up')], fadein=st.get('bg_fadein', 0))
    elif vb and vb[0] == 'swing':       # a 3D spiral rocking back and forth across the wall (DreamsOfFireflies)
        _, c, br = vb; sq.spirals('Verts', 2, s0, s1, [c, WHITE], count=1, thickness=50, movement=1.0, bright=br,
                                  three_d=True, swing=True)
    if st.get('tree_spirals'):          # blue barber-pole bands wrapping the trunks
        sq.spirals('trees', 2, s0, s1, [st.get('kick', BLUE), WHITE], count=2, rotation=20, thickness=40, movement=2.0,
                   bright=60, perModel=True)
    if st.get('tree_breathe'):          # a soft glow rises from the roots and settles, every two bars
        for k in range(int((s1 - s0) // (2 * BAR))):
            a = s0 + k * 2 * BAR
            sq.fill('trees', 2, a, a + BAR, [Grad(st['tree_breathe'], WHITE, mode='up')], 0, 60, per_model=True, bright=50)
            sq.fill('trees', 2, a + BAR, a + 2 * BAR, [Grad(st['tree_breathe'], WHITE, mode='up')], 60, 0, per_model=True, bright=50)
    if st.get('stars'):                 # starfield behind the forest, arches and spiral trees
        sq.shader(FOREST + [ARCHES, 'Spiral Trees'], 2, s0, s1, f'{SH}/Spacels.fs', params=STARS, bools=dict(nebula=0),
                  bright=45, fadein=1.0, fadeout=1.0)
    if st.get('galaxy'):                # a spiral galaxy turning on the Vert canvas
        sq.shader('Verts', 2, s0, s1, f'{SH}/Galaxy.fs', params=GALAXY, bright=70, fadein=1.5, fadeout=1.0)
    if 'house_bg' in st: sq.on(HOUSE, 1, s0, s1, G(st['house_bg'][0], 'right'), bright=st['house_bg'][1], blend=None)
    if 'house_ramp' in st: sq.on(HOUSE, 1, s0, s1, G(st['house_ramp'], 'right'), 5, 100, blend=None)
    if 'grinch' in st: sq.on('grinch-1', 1, s0, s1, st['grinch'][0], bright=st['grinch'][1], blend=None)
    if 'nativity' in st: sq.on('Nativity Spot', 1, s0, s1, st['nativity'][0], bright=st['nativity'][1], blend=None)
    if 'nativity_ramp' in st: sq.on('Nativity Spot', 1, s0, s1, st['nativity_ramp'], 20, 100, blend=None)
    if st.get('climb'):                 # the Verts and the trunks fill smoothly into the next big moment
        sq.fill('Verts', 1, s0, s1, [G(st['climb'], 'up')], 0, 100)
        sq.fill('trees', 1, s0, s1, [G(st['climb'], 'up')], 0, 100, per_model=True)
    fw = st.get('forest_waves')
    if fw:                              # sine waves rolling across the pixel sticks
        every, c = fw
        for k in range(int(round((s1 - s0) / (every * BAR)))):
            t = s0 + k * every * BAR
            sq.wave(FOREST[k % 2], 0, t, t + 2 * PER, None, 100, waves=900, speed=10, kind='Sine', fill='None',
                    thickness=50, height=50, direction='Right to Left' if k % 2 == 0 else 'Left to Right', colors=[WHITE, c])

# ---------------------------------------------------------------- "Just stop your crying": a soft white line rises up the Verts
lines = []
for i, w in enumerate(words):
    if re.sub(r'[^a-z]', '', w['word'].lower()) == 'just' and i + 1 < len(words) and \
            re.sub(r'[^a-z]', '', words[i + 1]['word'].lower()) == 'stop':
        end_w = next(x for x in words[i:i + 12] if re.sub(r'[^a-z]', '', x['word'].lower()) in ('times', 'time', 'alright', 'life'))
        lines.append((w['start'], end_w['end']))
for a, b in lines:
    sq.cut(q(a - 0.05), q(b + 0.5), MATRIX, layers=[0])
    sq.morph('Verts', 0, a, b + 0.5, [WHITE, ICE], *DIAG['up'], tail_start=5, tail_end=60)
    sq.trunk_ring(a, b + 0.5 - a, ICE)
sky = word_time('sky')                  # "...on your way to the sky": a quick sweep upward
sq.cut(q(sky['start']), q(sky['end'] + 0.6), MATRIX, layers=[0])
sq.morph('Verts', 0, sky['start'], sky['end'] + 0.6, [WHITE, CYAN], *DIAG['up'], tail_end=40)
sq.trunk_ring(sky['start'], sky['end'] + 0.6 - sky['start'], CYAN)

# ---------------------------------------------------------------- AllModels moments (everything underneath is cleared)
sq.moment(0.0, B(3), lambda a, b: sq.shader('AllModels', 0, a, b, f'{SH}/Spacels.fs', params=STARS, bools=dict(nebula=0),
                                            bright=60, fadein=4.0, fadeout=1.0), BLUE, 25, fade_from=0)   # stars out of the dark
sq.moment(B(26), B(27), lambda a, b: sq.shader('AllModels', 0, a, b, f'{SH}/Cosmic Flare.fs',
          params=dict(brightness=2, ray_brightness=6, gamma=2, spot_brightness=5, ray_density=10, curvature=300, freq=8,
                      red=7, green=3, blue=1), bools=dict(warp=1), bright=60, fadein=0.1, fadeout=0.6), GOLD, 20)  # the band hits
sq.moment(LAUNCH, GOOD_FROM_HERE, lambda a, b: sq.shader('AllModels', 0, a, b, f'{SH}/Hyper Space.fs', bright=80,
                                                         fadein=0.3, fadeout=0.8), WHITE, 30)  # break into the atmosphere
sq.moment(B(58), DUR, lambda a, b: sq.shader('AllModels', 0, a, b, f'{SH}/Galaxy.fs', params=GALAXY, bright=70,
                                             fadein=1.5, fadeout=6.0), BLUE, 0, fade_from=35)  # drifting far away from here
sq.cut(q(B(58)), q(DUR), ['Nativity Spot'])
sq.on('Nativity Spot', 0, B(58), DUR, GOLD, 60, 0)    # the sun is the last light out

# ---------------------------------------------------------------- timing tracks
labels = {'intro': 'Intro - stars', 'verseA': 'Verse A (piano)', 'verseB': 'Verse B', 'build': 'Build',
          'hit': 'Band hits', 'fullA': 'Full A', 'fullB': 'Full B', 'ignition': 'Ignition',
          'launch': 'Break into the atmosphere', 'space': 'Space', 'after': 'Everything will be alright',
          'outro': 'Outro - galaxy'}
seg = [l.split(None, 1) for l in (HERE / 'lyrics.txt').read_text().splitlines() if l.strip()]
nbars = int((END - B1) / BAR) + 1
sq.tracks = [
    ('Sections', marks([s for _, s, _, _ in SECTIONS], [labels[n] for n, _, _, _ in SECTIONS], end=DUR)),
    ('Lyric Lines', marks([float(a) for a, _ in seg], [t for _, t in seg], end=END)),
    ('Lyrics', marks([w['start'] for w in words], [w['word'] for w in words], maxlen=1.0)),
    ('Bars', marks([B(k + 1) for k in range(nbars)], [str(k + 1) for k in range(nbars)], end=END)),
    ('Beats', marks(ev['beats'], [str((i - ev['phase']) % 4 + 1) for i in range(len(ev['beats']))], end=END)),
    ('Kick', marks(ev['kick'], maxlen=PER / 2)), ('Snare', marks(ev['snare'], maxlen=PER / 2)),
    ('Bass Notes', marks([t for t, e, n in ev['bass']], [n for t, e, n in ev['bass']], maxlen=2 * PER)),
    ('Vocal Notes', marks([t for t, e, n in ev['vox']], [n for t, e, n in ev['vox']], maxlen=2 * PER)),
]

sq.write(OUT, dict(song='Sign of the Times', artist='', album='',
                   media=media_path(SONG, 'sign.mp3'),
                   comment='Generated from stem-separated audio analysis (Demucs + Basic Pitch + Whisper): 120 BPM. '
                           'Space theme with Interstellar shaders; kick=arches, snare=Verts/trees, drums=pixel sticks '
                           'bounce, bass=fence dot, voice=spiral height.'),
         DUR, timeline=ARGS[1] if len(ARGS) > 1 else None)
