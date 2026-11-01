"""Oh Come All Ye Faithful (Garrett Breeze & David Dykstra, Christmas Punk) -> seqs/punk-ohcome/punk-ohcome.xsq

Instrument map: kick=arches, snare=moving patterns on Verts/trees, cymbals=pixel forest (evens/odds),
bass=fence dot by pitch, melody=spiral fill height by pitch, off-beats=house+floods+forest.
The 0:20 build (kick drops out, melody climbs) is a smooth gold rise up the Verts and trunks; 0:47 repeats it in red.
Verts are one canvas (no panel flashing); the matrix trees are trunks: kick rings race up them, peppermint
barber-pole spirals in verse 2, and a big spinning peppermint (from punk-joy) takes the yard into the ending.
Analysis data (events.json, events2.json) came from one-off scripts during the first session; see README.

usage: build.py [out.xsq] [timeline.json]
"""
import json, sys, bisect
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from seqlib import *

SONG = 'punk-ohcome'
HERE = song_dir(SONG)
ARGS = cli_args()
OUT = ARGS[0] if ARGS else str(SHOW / 'seqs' / SONG / f'{SONG}.xsq')
TL = ARGS[1] if len(ARGS) > 1 else None
ev = json.load(open(HERE / 'events.json')); e2 = json.load(open(HERE / 'events2.json'))
t0, per = ev['t0'], ev['per']
DUR, END = 71.627, 68.5
B = lambda n: t0 + 4 * per * (n - 1)            # start of 1-based bar n

# ---------------------------------------------------------------- timing tracks
sections_tt = [(0.0, 'Drum intro'), (B(2), 'Band enters'), (B(3), 'Verse 1'), (B(15), 'Build - no kick'),
               (B(19), 'Christ the Lord'), (B(22), 'Turnaround lick'), (B(23), 'Verse 2 - harder'),
               (B(35), 'Adore him - off-beat riff'), (B(39), 'Christ the Lord 2'), (B(42), 'Turnaround 2'),
               (B(43), 'Ending - first line again'), (B(47), 'Final - Christ the Lord'), (B(50), 'Final hit'), (END, 'Out')]
nbars = int((END - t0) / (4 * per)) + 1
TRACKS = [
    ('Sections', marks([s for s, _ in sections_tt], [l for _, l in sections_tt], end=DUR, per=per)),
    ('Bars', marks([B(n + 1) for n in range(nbars)], [str(n + 1) for n in range(nbars)], end=END)),
    ('Beats', marks(ev['beats'], [str(i % 4 + 1) for i in range(len(ev['beats']))], end=END)),
    ('Kick', marks(e2['kick'], maxlen=per / 2)),
    ('Snare', marks(e2['snare'], maxlen=per / 2)),
    ('Cymbals', marks(e2['cym'], maxlen=per)),
    ('Off-beat Hits', marks(e2['off'], maxlen=per / 2)),
    ('Bass Notes', marks([t for t, _ in e2['bass']], [n for _, n in e2['bass']], maxlen=2 * per)),
    ('Guitar Melody', marks([t for t, _ in e2['mel']], [n for _, n in e2['mel']], maxlen=2 * per)),
]

sq = Seq(ELEMENTS)
sq.tracks = TRACKS

# ---------------------------------------------------------------- sections & styles
verse1 = dict(kick=RED, snare=GREEN, snare_mode='ripple', cym=WHITE, bass=RED, mel=GREEN, off=True,
              bg_forest=(RED, 15), verts_bg=('bars', 'Right', GREEN, 25, 4), spiral_bg=(GREEN, 8), house_bg=(RED, 20),
              grinch=(GREEN, 35), nativity=(GOLD, 30))
ctl = dict(kick=GOLD, snare=WHITE, snare_mode='diag', snare_bright=70, cym=WHITE, bass=GOLD, mel=GOLD,
           off=True, meteors=True, bg_forest=(GOLD, 20), house_bg=(GOLD, 40), nativity=(GOLD, 100), grinch=(GREEN, 15),
           spiral_bg=(GOLD, 10))
turn = dict(kick=GOLD, cym=WHITE, bass=GOLD, stabs=WHITE, snare=WHITE, snare_mode='diag', off=True,
            nativity=(GOLD, 60), grinch=(GREEN, 15))
verse2 = dict(kick=GREEN, kick_mode='halves', snare=RED, snare_mode='diag', cym=WHITE, bass=GREEN, mel=WHITE, off=True,
              bg_forest=(GREEN, 15), verts_bg=('bars', 'Left', RED, 30, 8), spiral_bg=(WHITE, 6), house_bg=(GREEN, 20),
              grinch=(GREEN, 50), nativity=(GOLD, 30), tree_spirals=True)
SECTIONS = [
    ('intro', 0.0, B(2), dict(bass=RED)),
    ('enter', B(2), B(3), dict(kick=RED, snare=GREEN, snare_mode='ripple', cym=WHITE, bass=RED, mel=GREEN, off=True)),
    ('verse1', B(3), B(11), verse1),
    ('verse1b', B(11), B(15), dict(verse1, snare_mode='hexpand', verts_bg=('diag', GREEN, 50))),  # "come and behold him" lifts
    ('build', B(15), B(19), dict(cym=WHITE, march=WHITE, climb=GOLD, arch_climb=GOLD, mel=GOLD,
                                 fence_pulse=RED, house_ramp=GOLD, nativity_ramp=GOLD, grinch=(GREEN, 15),
                                 spiral_bg=(GOLD, 8), off=True)),
    ('ctl1', B(19), B(22), ctl),
    ('turn1', B(22), B(23), turn),
    ('verse2', B(23), B(29), verse2),
    ('verse2b', B(29), B(35), dict(verse2, snare_mode='xc', verts_bg=('wave', RED, 45), bg_forest=(GREEN, 25))),  # four-on-the-floor
    ('adore2', B(35), B(39), dict(kick=WHITE, snare=WHITE, snare_mode='compress', snare_bright=70,
                                  climb=RED, arch_climb=RED, mel=GOLD, bass=RED, ands=True, spiral_bg=(GOLD, 8),
                                  house_ramp=GOLD, nativity_ramp=GOLD, grinch=(GREEN, 40), tree_spirals=True)),
    ('ctl2', B(39), B(42), dict(ctl, sparkles=True)),
    ('turn2', B(42), B(43), turn),
    ('ending', B(43), B(47), verse1),
    ('finalctl', B(47), B(50), dict(ctl, sparkles=True)),
    ('final', B(50), DUR, {}),
]
SEC_START = [s for _, s, _, _ in SECTIONS]
def section(t):
    i = bisect.bisect_right(SEC_START, t + 0.001) - 1
    return SECTIONS[max(i, 0)]
def sec(name): return [s for s in SECTIONS if s[0] == name][0]

# ---------------------------------------------------------------- intro roll call (crash hits)
sq.morph('Verts', 0, 0.036, 0.336, [WHITE, WHITE], *DIAG['up'], tail_end=100)
sq.trunk_rise(0.036, 0.4, WHITE)
roll = [(0.207, [ARCHES]), (0.464, FOREST), (0.55, ['Spiral Trees']), (0.721, HOUSE), (0.893, ['fenceline']), (1.064, FLOODS)]
for t, els in roll:
    sq.flash(els, 0, t, 0.30, WHITE, perModel=(els == ['Spiral Trees']))

# ---------------------------------------------------------------- kick -> arches
kicks = [t for t in e2['kick'] if t > 1.5]
k_count = 0
for i, t in enumerate(kicks):
    name, s0, s1, st = section(t)
    if not st.get('kick') or name == 'final': continue
    d = max(nxt(kicks, i, 0.30), 0.075)
    sb = (sub(0, 0, 50, 100) if k_count % 2 == 0 else sub(50, 0, 100, 100)) if st.get('kick_mode') == 'halves' else None
    sq.flash(ARCHES, 0, t, d, st['kick'], subbuf=sb)
    sq.trunk_ring(t, max(d, 0.2), st['kick'], tree=k_count % 3)
    k_count += 1

# ---------------------------------------------------------------- snare -> motion across the Vert canvas
snares = [t for t in e2['snare'] if t > 1.5]
s_count = 0
for i, t in enumerate(snares):
    name, s0, s1, st = section(t)
    if not st.get('snare') or name == 'final': continue
    d = max(nxt(snares, i, per), 0.075); c = st['snare']; br = st.get('snare_bright', 100)
    mode = st.get('snare_mode')
    if mode == 'ripple':          # a ring spreads across the canvas from a point that wanders left and right
        sq.ripple('Verts', 0, t, max(d, per), [c, WHITE], VERT_X[pingpong(s_count, 6)], 35 if s_count % 2 else 65)
    elif mode == 'hexpand':       # burst from the middle out to both edges
        sq.bars('Verts', 0, t, t + max(d, per), 'H-expand', [c, BLACK], 1, 1, br)
    elif mode == 'compress':      # collapse from both edges into the middle
        sq.bars('Verts', 0, t, t + max(d, per), 'H-compress', [c, BLACK], 1, 1, br)
    elif mode == 'xc':
        sq.bars('Verts', 0, t, t + max(d, per), 'H-expand' if s_count % 2 == 0 else 'H-compress', [c, BLACK], 1, 1, br)
    elif mode == 'diag':          # a diagonal streak flying across, alternating direction
        a, b = DIAG['up-right' if s_count % 2 == 0 else 'up-left']
        sq.morph('Verts', 0, t, t + max(d, per), [WHITE, c], a, b, tail_end=40, bright=br)
    s_count += 1

# build: a white light glides Vert to Vert along the top edge of the rising gold fill, one hop per beat
name, s0, s1, st = sec('build')
for k in range(16):
    h = 100 * (k + 0.5) / 16
    x0, x1 = VERT_X[pingpong(k, 6)], VERT_X[pingpong(k + 1, 6)]
    sq.morph('Verts', 0, s0 + k * per, s0 + (k + 1) * per, [WHITE, WHITE], (x0, h - 8, x0, h), (x1, h - 8, x1, h), tail_end=35)

# ---------------------------------------------------------------- cymbals -> pixel forest (evens/odds alternate)
cyms = [t for t in e2['cym'] if t > 1.5]
c_count = 0
for i, t in enumerate(cyms):
    name, s0, s1, st = section(t)
    if not st.get('cym') or name == 'final': continue
    d = max(nxt(cyms, i, 0.35), 0.075)
    sq.flash(FOREST[c_count % 2], 1, t, d, st['cym'], bright=85, sparkles=60)
    c_count += 1

# ---------------------------------------------------------------- off-beat hits -> house, floods, whole forest
offs = [t for t in e2['off'] if t > 1.5]
for i, t in enumerate(offs):
    name, s0, s1, st = section(t)
    if not st.get('off'): continue
    d = max(nxt(offs, i, per / 2), 0.075)
    sq.flash(HOUSE + FLOODS + FOREST, 0, t, d, WHITE)

# adore2: every "&" -> forest ping-pong against the kick on the beat
name, s0, s1, st = sec('adore2')
for k in range(16):
    t = s0 + k * per + per / 2
    sq.flash(FOREST[k % 2], 0, t, per / 2, RED if k % 2 == 0 else GREEN)
    sq.flash(FLOODS[k % 2], 0, t, per / 2, WHITE)
    sq.flash(HOUSE, 0, t, per / 2, WHITE, bright=60)

# ---------------------------------------------------------------- bass -> fence position dot
bass = [(t, midi(n)) for t, n in e2['bass'] if t > 1.5]
bt = [t for t, _ in bass]
for i, (t, p) in enumerate(bass):
    name, s0, s1, st = section(t)
    if not st.get('bass') or name == 'final': continue
    d = max(nxt(bt, i, 2 * per), 0.075)
    pos = 5 + (min(max(p, 28), 45) - 28) / 17 * 90
    sq.flash('fenceline', 0, t, d, st['bass'], subbuf=sub(max(pos - 5, 0), 0, min(pos + 5, 100), 100), end_level=30)

# build: steady bass pedal -> whole fence pulses on every eighth
name, s0, s1, st = sec('build')
for k in range(32):
    sq.flash('fenceline', 1, s0 + k * per / 2, per / 2, st['fence_pulse'], bright=60)

# ---------------------------------------------------------------- melody -> spiral trees fill height
mel = [(t, midi(n)) for t, n in e2['mel'] if t > 1.5]
mel = [(t, p if p < 84 else p - 12) for t, p in mel if p >= 62]
mt = [t for t, _ in mel]
for i, (t, p) in enumerate(mel):
    name, s0, s1, st = section(t)
    if name == 'final': continue
    d = max(nxt(mt, i, 2 * per), 0.075)
    if st.get('stabs'):
        sq.flash('Spiral Trees', 0, t, min(d, 0.25), st['stabs'], perModel=True)
    elif st.get('mel'):
        h = 10 + (min(p, 83) - 62) / 21 * 90
        sq.on('Spiral Trees', 1, t, t + d, st['mel'], 100, 70, subbuf=sub(0, 0, 100, h), perModel=True)

# ---------------------------------------------------------------- per-section backgrounds and set pieces
for name, s0, s1, st in SECTIONS:
    if name == 'final': continue
    if 'bg_forest' in st: sq.on(FOREST, 2, s0, s1, st['bg_forest'][0], bright=st['bg_forest'][1])
    if 'spiral_bg' in st: sq.on('Spiral Trees', 2, s0, s1, st['spiral_bg'][0], bright=st['spiral_bg'][1])
    vb = st.get('verts_bg')
    if vb and vb[0] == 'bars':        # bands sliding sideways across the whole wall
        _, direction, c, br, cyc = vb
        sq.bars('Verts', 2, s0, s1, direction, [c, BLACK], 2, cyc, br)
    elif vb and vb[0] == 'diag':      # one diagonal sweep per bar, alternating up-right / up-left
        _, c, br = vb
        nb = int(round((s1 - s0) / (4 * per)))
        for k in range(nb):
            a, b = DIAG['up-right' if k % 2 == 0 else 'up-left']
            sq.morph('Verts', 2, s0 + k * 4 * per, s0 + (k + 1) * 4 * per, [c, c], a, b, tail_end=50, bright=br)
    elif vb and vb[0] == 'wave':
        _, c, br = vb
        sq.wave('Verts', 2, s0, s1, c, br)
    if 'house_bg' in st: sq.on(HOUSE, 1, s0, s1, st['house_bg'][0], bright=st['house_bg'][1], blend=None)
    if 'house_ramp' in st: sq.on(HOUSE, 1, s0, s1, st['house_ramp'], 5, 100, blend=None)
    if 'grinch' in st: sq.on('grinch-1', 1, s0, s1, st['grinch'][0], bright=st['grinch'][1], blend=None)
    if 'nativity' in st: sq.on('Nativity Spot', 1, s0, s1, st['nativity'][0], bright=st['nativity'][1], blend=None)
    if 'nativity_ramp' in st: sq.on('Nativity Spot', 1, s0, s1, st['nativity_ramp'], 20, 100, blend=None)
    if st.get('meteors'):
        sq.add(MATRIX, 1, 'Meteors', s0, s1, {'E_CHECKBOX_Meteors_UseMusic': 0, 'E_CHOICE_Meteors_Effect': 'Down',
                                           'E_CHOICE_Meteors_Type': 'Palette', 'E_SLIDER_Meteors_Count': 25,
                                           'E_SLIDER_Meteors_Length': 30, 'E_SLIDER_Meteors_Speed': 12,
                                           'E_SLIDER_Meteors_Swirl_Intensity': 0, 'T_CHOICE_LayerMethod': 'Max'},
            [GOLD, WHITE], 100, 40 if st.get('sparkles') else 0)
    if st.get('climb'):          # the Verts and the trunks fill smoothly from the bottom over the four bars
        sq.fill('Verts', 1, s0, s1, [Grad(st['climb'], WHITE, mode='up')], 0, 100)
        sq.fill('trees', 1, s0, s1, [Grad(st['climb'], WHITE, mode='up')], 0, 100, per_model=True)
    if st.get('tree_spirals'):   # peppermint barber-pole bands wrapping around the trunks
        sq.spirals('trees', 2, s0, s1, [WHITE, RED], count=2, rotation=20, thickness=40, movement=2.0, bright=60,
                   perModel=True)
    if st.get('arch_climb'):     # both legs of every arch rise toward the apex
        for k in range(4):
            a, b = s0 + k * 4 * per, s0 + (k + 1) * 4 * per; w = 12.5 * (k + 1)
            sq.on(ARCHES, 1, a, b, st['arch_climb'], subbuf=sub(0, 0, w, 100), perModel=True)
            sq.on(ARCHES, 2, a, b, st['arch_climb'], subbuf=sub(100 - w, 0, 100, 100), perModel=True)

# ---------------------------------------------------------------- AllModels moments
# Each moment owns the whole yard: everything underneath is cleared, AllModels plays the yard-wide effect,
# and the props AllModels doesn't cover flash along with it.
sq.moment(1.236, 1.85, lambda a, b: sq.shockwave('AllModels', 0, a, b, [WHITE]), WHITE)                     # last intro crash
sq.moment(B(3), B(3) + 2 * per, lambda a, b: sq.morph('AllModels', 0, a, b, [RED, RED], *DIAG['right'], tail_end=60), RED)
sq.moment(B(19), B(19) + 3 * per, lambda a, b: sq.shockwave('AllModels', 0, a, b, [GOLD, WHITE]), GOLD, 20)  # climb pays off
def lick(a, b):                                       # ping-pong sweeps, one per beat of the lick bar
    for k in range(4):
        sq.morph('AllModels', 0, a + k * per, a + (k + 1) * per, [WHITE, WHITE], *DIAG['right' if k % 2 == 0 else 'left'], tail_end=40)
sq.moment(B(22), B(23), lick, WHITE, 30)
sq.moment(B(23), B(23) + 2 * per, lambda a, b: sq.morph('AllModels', 0, a, b, [GREEN, GREEN], *DIAG['left'], tail_end=60), GREEN)
sq.moment(B(39), B(39) + 3 * per, lambda a, b: sq.shockwave('AllModels', 0, a, b, [GOLD, WHITE], sparkles=60), GOLD, 20)
def peppermint(a, b):
    for k in range(3):
        sq.peppermint('AllModels', 0, a + k * 4 * per, a + (k + 1) * 4 * per, clockwise=k % 2 == 0)
sq.moment(B(42), B(45), peppermint, RED, 40, fade_from=70)
# finale: white hit, then everything fades out in gold
a, b = q(B(50)) / 1000, q(70.6) / 1000
sq.cut(q(a), q(b))
sq.shockwave('AllModels', 0, a, a + 0.35, [WHITE])
sq.on('AllModels', 0, a + 0.35, b, GOLD, 100, 0)
others = [el for el in NON_MEMBERS if el != 'trees']
sq.flash(others, 0, a, 0.35, WHITE)
sq.on(others, 0, a + 0.35, b, GOLD, 100, 0)
sq.trunk_rise(a, b - a, GOLD)

sq.write(OUT, dict(song='Oh Come All Ye Faithful', artist='Garrett Breeze,David Dykstra', album='Christmas Punk',
                   media=media_path(SONG, 'punk_ohcome.mp3'),
                   comment='Generated from stem-separated audio analysis (Demucs + Basic Pitch): 175 BPM. Kick=arches, '
                           'snare=moving patterns on Verts/trees, cymbals=pixel forest, bass=fence dot, melody=spiral '
                           'fill height, off-beats=house/floods; AllModels moments at the turning points.'),
         DUR, timeline=TL)
