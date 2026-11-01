"""In Christ (Big Daddy Weave) -> seqs/new/bdw_inChrist/inchrist.xsq

A song about an ordinary man who carries a light in his heart, and about that light passing from one heart to
another until everyone sings together. The yard tells it with hearts:

- The manger (the Nativity Spot) is where the light comes from. It always glows, and every "In Christ" sends a ring
  of light out from it across the yard and along the fence to everyone.
- The pixel sticks are a crowd of 29 people. At first one person has the light (a warm body with a red heart pixel)
  and dances with the drums; the rest stand dim in the dark. The light spreads person to person: "...wants to live
  inside of you" (5 people), "take hold of the answer" (15), "what I confess" (21), "as we all live in Him" (all 29).
  Only the people who have the light dance with the drums - the yard gets more alive as the song goes on.
- Pixel-art hearts are drawn on the Verts (each Vert is 6 x 44 pixels: a 6 x 5 heart). They first appear on
  "He is living in my heart", beat (lub-dub) whenever the band stops and the words carry the song, and spread from
  the middle two Verts to all six.
- Verse 1: a small light walks along the bottom of the wall ("the greatest man to walk this earth") and sends a beam
  to the manger on "I know who He is"; a meter rises only a little on "may not amount to much" and shoots to the
  top on "but I already do to Him". Verse 2: the light puffs up on "all too prideful".
- Pre-choruses (B minor): the dark. Cold searchlights sweep the Verts and the crowd's lights wander up and down,
  searching; a tiny light appears on "a light in the dark" and opens out on "I'm standing with the answer".
- Choruses, line by line: "I can do all things" - every prop surges at once; "eagle's wings" - wings beat up and out
  from the middle of the wall and the arches spread; "a great reward" - gold sparkles over the yard and a pixel-art
  crown on every Vert; "that I have in store" - gold fills the bottom of the wall; "His righteousness" - a white wash
  rolls up over the whole yard; "what I confess" - the song's own voice as a waveform across the wall; "don't worry
  about all the rest" - everything settles into a gentle wave; "everything I need to be" - the yard gathers inward.
- Bridge: "in Him we live and move" - one slow wave moves through everything while the hearts beat together;
  "together we can sing" - the whole crowd bounces in unison to the melody.
- The key change (D major -> E major, 2:37) is a lift: a wave of light rolls up the whole yard and the colours step up
  from warm red/gold/sky to a rainbow - every heart its own colour.
- The end: "everything I need to be" three times, gathering tighter each time, "is in Christ" - everything falls into
  the hearts; the quiet breakdown is just the hearts, the crowd's hearts and the manger. The outro pours the light
  back out; the manger is the last light.

usage: build.py [out.xsq] [timeline.json] [--force]
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from seqlib import *

SONG = 'new/bdw_inChrist'
HERE = song_dir(SONG)
ARGS = cli_args()
OUT = ARGS[0] if ARGS else str(SHOW / 'seqs' / SONG / 'inchrist.xsq')
ev = json.load(open(HERE / 'events.json'))
T0, PER = ev['t0'], ev['per']
BAR = 4 * PER
B1 = T0 + ev['phase'] * PER
B = lambda n: B1 + (n - 1) * BAR            # start of 1-based bar n (2.035 s at 118 BPM)
BEATS = ev['beats']
DUR, END = round(ev['dur'], 3), ev['end']

# ---------------------------------------------------------------- the props
LX = layout_x()
STICKS = sorted((m for m in LX if m.startswith('pixstk')), key=LX.get)    # the crowd, left to right
VERTS_M = sorted((m for m in LX if m.startswith('Vert-')), key=LX.get)     # single Verts, for the pixel art
ARCHS = sorted((m for m in LX if m.startswith('arch-big')), key=LX.get)
SPIRALS = sorted(['Spiral Tree 2', 'Spiral Tree 3', 'little spiral - left', 'little spiral - right'], key=LX.get)
sq = Seq(ELEMENTS + STICKS + VERTS_M + SPIRALS, nlayers=15)
# Verts group layers: 0 specials (walker, light, wave), 1 wings/gold/meter, 2 searchlights/VU, 3 ripples, 4 background
# single Verts: 0-4 the beating heart, 5-8 the crown, 10-14 the heart at rest (underneath the beats)
_x = [LX[m] for m in ARCHS + STICKS + VERTS_M] + [LX['Spiral Tree 2'], LX['Spiral Tree 3']]
ALLX = lambda x: (x - min(_x)) / (max(_x) - min(_x)) * 100     # world X -> % across the AllModels buffer
MANGER_X = ALLX(LX['Nativity Spot'])                            # where the light comes from (~92 %)
HEART_X = (ALLX(LX[VERTS_M[2]]) + ALLX(LX[VERTS_M[3]])) / 2     # the middle of the wall
FENCE_MANGER = (LX['Nativity Spot'] - LX['fenceline']) / 2825 * 100   # the manger's spot along the fence
NATIVITY, OTHER_FLOODS = 'Nativity Spot', ['grinch-1']

# ---------------------------------------------------------------- colour: warm in D major, a rainbow after the lift to E
WARM, HEART, SKY, ROYAL = '#FFE6C8', '#FF0A28', '#3CA0FF', '#5028FF'
GOLD = '#FFC832'            # gold that stays gold on pixels; kept for the reward
COLD, NIGHT, TEAL, ICE = '#1E3CB4', '#0A0A50', '#00A0C8', '#BFFFFF'
VIOLET, MAGENTA, CYAN, EMERALD, PINK = '#8A2BFF', '#FF00C8', '#00E5FF', '#00FF80', '#FF3C8C'
D_COLS = [HEART, GOLD, SKY, WARM]
E_COLS = [MAGENTA, CYAN, EMERALD, VIOLET, HEART, SKY]
E_HEARTS = [HEART, MAGENTA, VIOLET, SKY, EMERALD, PINK]          # after the key change every heart has its own colour

# ---------------------------------------------------------------- words and notes
WORDS = [(w['word'].strip(' ,.?!').lower(), w['start'], w['end'])
         for w in json.load(open(HERE / 'lyrics.json')) if w['start'] < END]
def word(prefix, after, before=1e9):
    return next(s for w, s, e in WORDS if w.startswith(prefix) and after <= s < before)
def word_end(prefix, after):
    return next(e for w, s, e in WORDS if w.startswith(prefix) and after <= s)
VOX = [n for n in load_notes(HERE / 'midi' / 'vocals_basic_pitch.csv') if n[3] >= 40 and n[0] < END]
def sung(t, back=0.5):
    """the first sung note onset just before a Whisper word time (Whisper runs a little late)"""
    c = [n[0] for n in VOX if t - back <= n[0] <= t + 0.1]
    return min(c) if c else t
def mono(notes, lo, hi, gap=0.06):
    out, cl = [], []
    for n in (n for n in notes if lo <= n[2] <= hi):
        if cl and n[0] - cl[0][0] > gap: out.append(max(cl, key=lambda x: x[2])); cl = []
        cl.append(n)
    if cl: out.append(max(cl, key=lambda x: x[2]))
    return [(s, p, e - s) for s, e, p, v in out]
MELODY = mono(VOX, 50, 80)
KICKS, SNARES = ev['kick'], ev['snare']
BASS = [(t, midi(nm)) for t, e, nm in ev['bass']]

# ---------------------------------------------------------------- structure
SECTIONS = [('intro', 1, 10), ('verse1', 10, 18), ('pre1', 18, 25), ('stop1', 25, 26), ('chorus1', 26, 33),
            ('stop2', 33, 34), ('inst', 34, 38), ('verse2', 38, 46), ('pre2', 46, 53), ('stop3', 53, 54),
            ('chorus2', 54, 61), ('stop4', 61, 62), ('chorus2b', 62, 69), ('stop5', 69, 70), ('bridge', 70, 78),
            ('chorus3', 78, 91), ('everything', 91, 98), ('stop6', 98, 99), ('breakdown', 99, 102), ('outro', 102, None)]
SPAN = {n: (B(a) if a > 1 else 0.0, B(b) if b else DUR) for n, a, b in SECTIONS}
section = lambda t: next((n for n, (a, b) in SPAN.items() if a <= t < b), 'outro')
kind = lambda t: section(t).rstrip('0123456789b')
KEY_CHANGE = SPAN['chorus3'][0]                                  # D major -> E major
in_e = lambda t: t >= KEY_CHANGE
STOPS = [n for n, _, _ in SECTIONS if n.startswith('stop')]
QUIET = ('stop', 'breakdown')

# the chorus lines: the "In" that starts each line, and its key word
def line(key, after):
    k = word(key, after)
    i = next(j for j, (w, s, e) in enumerate(WORDS) if s == k)
    st = next((WORDS[j][1] for j in range(i, max(i - 8, 0), -1) if WORDS[j][0] == 'in'), k - 1.5)
    return dict(start=sung(st), key=k)
CHORUSES = []
for name, after in (('chorus1', SPAN['pre1'][1] - 1), ('chorus2', SPAN['pre2'][1] - 2), ('chorus3', SPAN['bridge'][1] - 2)):
    c = dict(name=name, things=line('things', after))
    c['wings'] = line('wings', c['things']['key'])
    c['reward'] = line('reward', c['wings']['key'])
    c['store'] = dict(start=word('that', c['reward']['key']), key=word('store', c['reward']['key']))
    if name != 'chorus1':
        c['right'] = line('righteous', c['store']['key'])
        c['confess'] = line('can' if name == 'chorus3' else 'confess', c['right']['key'] + 1.0)
        c['worry'] = line('worry', c['confess']['key'])
    CHORUSES.append(c)
IN_CHRIST = sorted({sung(s) for w, s, e in WORDS if w == 'in' and any(w2.startswith('christ') for w2, s2, e2 in WORDS
                                                                      if 0 < s2 - s < 1.6)})

# the crowd: the light passes from the middle person outward, a few at a time
CENTER = len(STICKS) // 2
ORDER = sorted(range(len(STICKS)), key=lambda i: (abs(i - CENTER), i > CENTER))
HEART_AT = sung(word('living', SPAN['pre1'][0]))        # "He is living in my heart": the first heart
SPREAD = [(HEART_AT, HEART_AT, 1),
          (word('wants', SPAN['verse2'][0]), word_end('you', word('inside', word('wants', SPAN['verse2'][0]))), 5),
          (word('take', SPAN['pre2'][0]), word_end('answer', word('take', SPAN['pre2'][0])), 15),
          (CHORUSES[1]['confess']['start'], CHORUSES[1]['confess']['key'] + 0.5, 21),
          (word('all', word('as', SPAN['bridge'][0])), word_end('him', word('live', word('all', SPAN['bridge'][0]))), 29)]
LIT_AT, n0 = {}, 0
for a, b, n in SPREAD:
    for j, i in enumerate(ORDER[n0:n]):
        LIT_AT[i] = a + (b - a) * j / max(n - n0 - 1, 1)
    n0 = n
ALL_LIT = max(LIT_AT.values())
lit = lambda i, t: LIT_AT.get(i, 1e9) <= t
# hearts on the Verts: the middle two, then four, then all six
HEARTS_FROM = {2: HEART_AT, 3: HEART_AT, 1: SPREAD[1][1], 4: SPREAD[1][1], 0: SPREAD[4][1], 5: SPREAD[4][1]}
hearted = lambda t: [k for k in range(6) if HEARTS_FROM[k] <= t + 0.01]
heart_col = lambda k, t: E_HEARTS[k] if in_e(t) else HEART

STORY = []

# ---------------------------------------------------------------- pixel art on a single Vert (6 x 44)
def cols(c1, c2):       # x range for columns c1..c2 (each column is 1/6 of the panel)
    return c1 * 100 / 6 - 0.01, (c2 + 1) * 100 / 6 - 0.01
def rows(r1, r2):       # y range for rows r1..r2 (of 44, 0 = bottom)
    return r1 * 100 / 44 - 0.01, (r2 + 1) * 100 / 44 - 0.01
HEART_ROWS = 21         # bottom row of the heart (rows 21-25: the middle of the panel)
HEART_ART = [((2, 3), (0, 0)), ((1, 4), (1, 1)), ((0, 5), (2, 3)), ((0, 1), (4, 4)), ((4, 5), (4, 4))]
CROWN_ROWS = 35
CROWN_ART = [((0, 5), (0, 1)), ((0, 0), (2, 2)), ((2, 3), (2, 2)), ((5, 5), (2, 2))]
def art(k, layer0, shape, base, t, dur, color, a=100, b=100):
    for j, ((c1, c2), (r1, r2)) in enumerate(shape):
        x1, x2 = cols(c1, c2); y1, _ = rows(base + r1, base + r1); _, y2 = rows(base + r2, base + r2)
        sq.on(VERTS_M[k], layer0 + j, t, t + dur, color, a, b, subbuf=sub(x1, y1, x2, y2))
def heart(k, t, dur, a=100, b=100, color=None, layer0=0):
    art(k, layer0, HEART_ART, HEART_ROWS, t, dur, color or heart_col(k, t), a, b)
def crown(k, t, dur, a=100, b=100):
    art(k, 5, CROWN_ART, CROWN_ROWS, t, dur, GOLD, a, b)

def heartbeat(t0, t1, ks=None, every=2, rest=25):
    """lub-dub on every `every` beats between t0 and t1, on the hearted Verts (or the given ones)"""
    bs = [b for b in BEATS if t0 - 0.01 <= b < t1][::every]
    if not bs or bs[0] - t0 > 0.05: bs = [t0] + bs
    for i, t in enumerate(bs):
        nx = bs[i + 1] if i + 1 < len(bs) else t1
        for k in (ks if ks is not None else hearted(t)):
            heart(k, t, 0.17, 100, 55)
            heart(k, t + 0.17, 0.28, 90, rest)
            if nx - t > 0.5: heart(k, t + 0.45, nx - t - 0.45, rest, rest)

def heart_glow(t0, t1, level=45):
    """hearts resting on the hearted Verts"""
    for k in hearted(t0):
        heart(k, t0, t1 - t0, level, level, layer0=10)

# ---------------------------------------------------------------- the crowd
PERSON_BODY, HEART_PIXEL = sub(0, 0, 100, 100), sub(5 * 12.5 - 0.01, 0, 6 * 12.5 - 0.01, 100)   # pixel 6 of 8
def person(i, t0, t1, color=None, body=18):
    """a person who has the light: a soft warm body and a red heart pixel"""
    if t1 - t0 < 0.05: return
    sq.on(STICKS[i], 3, t0, t1, WARM, body, body)
    sq.on(STICKS[i], 2, t0, t1, color or (E_HEARTS[i % 6] if in_e(t0) else HEART), 100, 100, subbuf=HEART_PIXEL)

# ---------------------------------------------------------------- small helpers
def breathe(s0, s1, cols_, lo=15, hi=70, period=None, els=HOUSE + OTHER_FLOODS, layer=1):
    period = period or BAR
    k, t = 0, s0
    while t < s1 - 0.05:
        e = min(t + period, s1)
        sq.on(els, layer, t, e, cols_[(k // 2) % len(cols_)], lo if k % 2 == 0 else hi, hi if k % 2 == 0 else lo,
              blend=None)
        t, k = e, k + 1

def vert_glow(x, y, t, dur, c, layer=0, a=100, b=0, h=4, w=8):
    sq.on('Verts', layer, t, t + dur, Grad(WHITE, c, mode='radial-out'), a, b,
          subbuf=sub(max(x - w, 0), max(y - h, 0), min(x + w, 100), min(y + h, 100)))

def walk(points, end, color=WARM, layer=0):
    """a small light walking through (t, x, y) points on the Verts canvas"""
    for i, (t, x, y) in enumerate(points):
        t2, x2, y2 = points[i + 1] if i + 1 < len(points) else (end, x, y)
        if abs(x2 - x) > 3:
            sq.morph('Verts', layer, t, t2, [WHITE, color], (x, y - 3, x, y + 3), (x2, y2 - 3, x2, y2 + 3),
                     tail_start=1, tail_end=25)
        else:
            vert_glow(x, y, t, t2 - t, color, layer, 90, 90)

def manger_ring(t, bright_cols=(WHITE, WARM), layer=1, big=True):
    """'In Christ': light goes out from the manger to the whole yard - a ring over everything, along the fence both
    ways, and the manger itself flares"""
    sq.shockwave('AllModels', layer, t, t + 1.6, list(bright_cols), cx=round(MANGER_X), cy=20,
                 r_end=300 if big else 160, w_end=40)
    for edge in (0, 100):
        f = FENCE_MANGER
        sq.morph('fenceline', 1, t, t + 1.2, [WHITE, bright_cols[-1]], (f, 0, f, 100), (edge, 0, edge, 100),
                 tail_start=2, tail_end=30)
    sq.flash(NATIVITY, 0, t, 1.5, WHITE, end_level=60)

# ================================================================ the manger: always glowing
sq.on(NATIVITY, 1, 0.0, END + 2.0, WARM, 40, 40)

# ================================================================ instruments
for i, t in enumerate(KICKS):
    k = kind(t)
    if k in QUIET: continue
    d = min(max(nxt(KICKS, i, 0.3), 0.1), 0.3)
    c1, c2 = (E_COLS[i % 6], E_COLS[(i + 2) % 6]) if in_e(t) else \
        ((COLD, TEAL) if k == 'pre' else (HEART, GOLD) if i % 2 else (SKY, WARM))
    sq.flash(ARCHES, 0, t, d, Grad(c1, c2, mode='right'), bright=50 if k == 'pre' else 100)

sn = 0
for i, t in enumerate(SNARES):
    k = kind(t)
    if k in QUIET: continue
    if i + 1 < len(SNARES) and SNARES[i + 1] - t < PER * 0.6 and k != 'intro': continue    # ghost notes
    c = E_COLS[sn % 6] if in_e(t) else (COLD if k == 'pre' else WARM)
    sq.trunk_ring(t, 0.45, c, tree=sn % 3, bright=60 if k == 'pre' else 100)
    if k in ('intro', 'inst', 'outro'):
        sq.ripple('Verts', 3, t, PER * 1.5, [WHITE, c if in_e(t) else SKY], VERT_X[pingpong(sn, 6)], 30 if sn % 2 else 70)
    sn += 1

bt = [t for t, _ in BASS]
for i, (t, p) in enumerate(BASS):
    if kind(t) in QUIET: continue
    pos = 5 + (min(max(p, 30), 54) - 30) / 24 * 90
    c = E_COLS[p % 6] if in_e(t) else (COLD if kind(t) == 'pre' else [HEART, GOLD, SKY][p % 3])
    sq.flash('fenceline', 0, t, max(nxt(bt, i, 2 * PER), 0.075), Grad(WHITE, c), bright=70,
             subbuf=sub(max(pos - 5, 0), 0, min(pos + 5, 100), 100), end_level=30)

# the singer's melody: how high the spiral trees glow
for i, (t, p, d) in enumerate(MELODY):
    if kind(t) in ('intro', 'inst', 'outro'): continue
    g = min(MELODY[i + 1][0] - t, 2 * PER) if i + 1 < len(MELODY) else min(d, 2 * PER)
    h = 15 + (min(max(p, 55), 76) - 55) / 21 * 85
    c = E_COLS[i % 6] if in_e(t) else (COLD if kind(t) == 'pre' else WARM)
    sq.on('Spiral Trees', 1, t, t + max(g, 0.075), Grad(c, WHITE, mode='up'), 100, 50, subbuf=sub(0, 0, 100, h),
          perModel=True)

# ================================================================ the crowd: people with the light dance with the drums
LIT_SPANS = [n for n in SPAN if kind(SPAN[n][0]) not in QUIET]
for i in range(len(STICKS)):
    if i not in LIT_AT: continue
    for n in LIT_SPANS:
        a, b = SPAN[n]
        a = max(a, LIT_AT[i])
        if a < b:
            if in_e(b - 0.01) and not in_e(a): person(i, a, KEY_CHANGE); person(i, KEY_CHANGE, b)
            else: person(i, a, b)
    # the moment the light arrives: the person fills up from the ground
    sq.fill(STICKS[i], 1, LIT_AT[i], LIT_AT[i] + 0.6, [Grad(WARM, WHITE, mode='up')], 0, 100, fadeout=0.3)

# until everyone has it, only the people with the light dance (kick: even ones, snare: odd ones)
for hits, parity in ((KICKS, 0), (SNARES, 1)):
    for j, t in enumerate(hits):
        k = kind(t)
        if k in QUIET or t >= ALL_LIT: continue
        d = min(max(nxt(hits, j, 0.4), 0.15), 0.4)
        for i in LIT_AT:
            if lit(i, t) and (i % 2 == parity or sum(lit(x, t) for x in LIT_AT) <= 5):
                sq.bounce(STICKS[i], 0, t, t + d, [Grad(HEART if i == CENTER else WARM, WHITE, mode='up')], height=75)
# ...and once everyone does, the whole crowd dances
kv, sv = dict(zip(KICKS, ev['kick_v'])), dict(zip(SNARES, ev['snare_v']))
for grp, hits, vals in (('pix-evens', KICKS, kv), ('pix-odds', SNARES, sv)):
    for j, t in enumerate(hits):
        k = kind(t)
        if k in QUIET or t < ALL_LIT: continue
        d = min(max(nxt(hits, j, 0.4), 0.15), 0.4)
        c = E_COLS[j % 6] if in_e(t) else WARM
        sq.bounce(grp, 0, t, t + d, [Grad(c, WHITE, mode='up')], height=40 + 60 * min(max(vals[t] - 0.35, 0) / 0.6, 1))
# the people still in the dark: dim and cold - and searching, in the pre-choruses
for n in LIT_SPANS:
    a, b = SPAN[n]
    if a >= ALL_LIT: continue
    b = min(b, ALL_LIT)
    if kind(a) == 'pre':
        sq.meteors(FOREST, 4, a, b, [COLD, TEAL], direction='Up', count=10, speed=8, bright=60, perModel=True)
    else:
        sq.on(FOREST, 4, a, b, COLD, 10, 10)

# ================================================================ backgrounds by section
def section_bg(name):
    s0, s1 = SPAN[name]
    k = kind(s0)
    if k == 'intro':
        sq.bars('Verts', 4, s0, s1, 'Left', [Grad(WARM, SKY, mode='up'), BLACK, Grad(GOLD, HEART, mode='up'), BLACK], 4,
                (s1 - s0) / (2 * BAR), 30)
        sq.wave(FOREST, 2, s0, s1, None, 40, waves=900, speed=10, kind='Sine', fill='None', thickness=50, height=50,
                colors=[WHITE, SKY])
        breathe(s0, s1, [WARM, SKY])
        sq.spirals('trees', 1, s0, s1, [HEART, WARM], count=2, rotation=20, thickness=40, movement=2.0, bright=40,
                   perModel=True)
    elif k == 'verse':
        sq.on('Verts', 4, s0, s1, Grad(NIGHT, ROYAL, mode='up'), 20, 20)
        breathe(s0, s1, [WARM, ROYAL], 10, 45)
        sq.spirals('trees', 1, s0, s1, [ROYAL, WARM], count=2, rotation=15, thickness=40, movement=2.0, bright=30,
                   perModel=True)
    elif k == 'pre':       # B minor: the dark, cold searchlights
        sq.pinwheel('Verts', 2, s0, s1, [Grad(TEAL, COLD, mode='radial-out'), BLACK], arms=3, speed=5, twist=0,
                    size=100, thickness=10, xc=0, yc=-60, bright=45)
        sq.meteors('trees', 1, s0, s1, [COLD, TEAL], direction='Down', count=6, speed=6, bright=40)
        sq.on(HOUSE + OTHER_FLOODS, 1, s0, s1, NIGHT, 20, 20)
    elif k == 'chorus':
        cs = E_COLS if in_e(s0) else [HEART, SKY, GOLD]
        sq.spirals('Verts', 4, s0, s1, cs[:3], count=3, thickness=50, movement=1.0, bright=25, three_d=True, swing=True)
        sq.spirals('trees', 1, s0, s1, cs[:2], count=2, rotation=25, thickness=40, movement=2.0, bright=45, perModel=True)
        breathe(s0, s1, cs, 20, 80)
        heart_glow(s0, s1, 35)
    elif k == 'inst':
        sq.bars('Verts', 4, s0, s1, 'Right', [Grad(HEART, GOLD, mode='up'), BLACK, Grad(SKY, WARM, mode='up'), BLACK], 4,
                (s1 - s0) / (2 * BAR), 30)
        breathe(s0, s1, [HEART, GOLD, SKY])
        sq.spirals('trees', 1, s0, s1, [HEART, WARM], count=2, rotation=20, thickness=40, movement=2.0, bright=40,
                   perModel=True)
    elif k == 'everything':
        sq.spirals('Verts', 4, s0, s1, E_COLS[:3], count=3, thickness=50, movement=1.0, bright=25, three_d=True,
                   swing=True)
        breathe(s0, s1, E_COLS, 20, 80)
        heart_glow(s0, s1, 35)
    elif k == 'outro':
        sq.spirals('Verts', 4, s0, s1, E_COLS, count=6, thickness=50, movement=1.0, bright=35, three_d=True, swing=True)
        sq.spirals('trees', 1, s0, s1, E_COLS[:3], count=3, rotation=25, thickness=40, movement=2.0, bright=45,
                   perModel=True)
        sq.spirals('Spiral Trees', 2, s0, s1, E_COLS[:3], count=3, rotation=25, thickness=40, movement=2.0, bright=45,
                   perModel=True)
        breathe(s0, s1, E_COLS, 20, 80)
for n, _, _ in SECTIONS:
    if not n.startswith('stop') and n not in ('breakdown', 'bridge'):
        section_bg(n)

# ================================================================ the opening: the light comes from the manger
first = next(t for t in KICKS if t > 1.5)
for j, t in enumerate([first] + [B(n) for n in (6,)]):
    manger_ring(t, (WHITE, WARM, GOLD))
for j, n in enumerate(range(2, 10, 2)):     # rays from the manger's side of the wall, every two bars
    a, b = DIAG['left']
    sq.morph('Verts', 0, B(n), B(n) + 1.2, [WHITE, WARM], a, b, tail_start=5, tail_end=60, bright=80)
STORY.append(('the light comes from the manger', 0.0, SPAN['intro'][1]))

# ================================================================ verse 1: an ordinary man
s0, s1 = SPAN['verse1']
walk_end = word('who', s0)
syll = [n[0] for n in VOX if s0 - 0.3 <= n[0] < walk_end]
syll = [t for i, t in enumerate(syll) if i == 0 or t - syll[i - 1] > 0.15]
pts = [(t, VERT_X[min(j * 6 // max(len(syll), 1), 5)] + 0.01 * (j % 2), 8) for j, t in enumerate(syll)]
walk(pts, walk_end)
he = word('he', walk_end)
sq.morph('Verts', 0, he, he + 1.2, [WHITE, GOLD], (VERT_X[5], 4, VERT_X[5], 12), (100, 4, 100, 12), tail_start=5,
         tail_end=60)
vert_glow(VERT_X[5], 8, walk_end, 4.0, WARM, 1, 90, 30)
sq.flash(NATIVITY, 0, he + 0.3, 1.5, WHITE, end_level=40)
STORY += [('the greatest man to walk this earth', s0, walk_end), ('I know who He is', walk_end, word('and', he))]
amount, much = word('amount', he), word_end('much', he)
but = word('but', much)
sq.fill('Verts', 1, amount, much + 0.4, [Grad(WARM, ROYAL, mode='up')], 0, 14, bright=60)
sq.fill('Verts', 1, much + 0.4, but, [Grad(WARM, ROYAL, mode='up')], 14, 14, bright=60)
him = word_end('him', but)
sq.fill('Verts', 1, but, him + 0.3, [Grad(WARM, GOLD, WHITE, mode='up')], 14, 100, bright=90)
sq.fill('Verts', 1, him + 0.3, min(him + 1.8, s1), [Grad(WARM, GOLD, WHITE, mode='up')], 100, 100, bright=90,
        fadeout=1.2)
sq.flash(NATIVITY, 0, him - 0.3, 1.5, WHITE, end_level=40)
STORY += [('I may not amount to much...', amount, but), ('...but I already do to Him', but, s1)]

# ================================================================ pre-choruses: searching in the dark
for name in ('pre1', 'pre2'):
    s0, s1 = SPAN[name]
    STORY.append(('people searching in the dark' if name == 'pre1' else 'instead of searching any longer', s0,
                  s0 + 4))
s0, s1 = SPAN['pre1']
light = word('light', s0)
standing = word('standing', light)
vert_glow((VERT_X[2] + VERT_X[3]) / 2, 50, light, standing - light, WARM, 0, 100, 100, h=3, w=12)
sq.bars('Verts', 1, standing, s1, 'H-expand', [Grad(WARM, GOLD, mode='up'), BLACK], 1, 1, 80)
sq.trunk_rise(standing, s1 - standing, WARM)
STORY += [('a light in the dark', light, standing), ("I'm standing with the answer", standing, s1)]

s0, s1 = SPAN['pre2']
peace = word('peace', s0)
sq.on('Verts', 1, sung(word('you', peace - 2)), word('can', peace + 1), Grad(WARM, ROYAL, mode='up'), 0, 40)
sq.on(HOUSE + OTHER_FLOODS, 0, peace - 1, peace + 3, WARM, 0, 60)
take = SPREAD[2][0]
sq.bars('Verts', 1, take, s1, 'H-expand', [Grad(WARM, GOLD, mode='up'), BLACK], 1, 1, 70)
STORY += [('you can have peace today', peace - 1, take), ('take hold of the answer: the light spreads', take, s1)]

# ================================================================ verse 2: the light wants to live in you
s0, s1 = SPAN['verse2']
prid = word('prideful', s0)
true_ = word_end('true', prid)
cx = (VERT_X[2] + VERT_X[3]) / 2
vert_glow(cx, 50, s0, word('sounding', s0) - s0, WARM, 0, 70, 70, h=3, w=10)
def puff(a, b, h0, h1, n=6):
    """the light swelling (or shrinking) from h0 to h1 % tall in n steps"""
    for m in range(n):
        h = h0 + (h1 - h0) * (m + 0.5) / n
        sq.on('Verts', 0, a + (b - a) * m / n, a + (b - a) * (m + 1) / n, Grad(WHITE, GOLD, WARM, mode='radial-out'),
              90, 90, subbuf=sub(cx - 10 - h / 2, 50 - h, cx + 10 + h / 2, 50 + h))
puff(word('sounding', s0), prid + 0.6, 3, 22)
puff(prid + 0.6, word('but', prid), 22, 22, 1)
puff(word('but', prid), true_, 22, 3)
STORY += [('all too prideful: the light puffs up', word('sounding', s0), word('but', prid)),
          ('let me tell you something true', word('but', prid), true_)]
lives = word('lives', true_)
heartbeat(lives - 0.3, SPREAD[1][0], ks=[2, 3])
# "wants to live inside of you": hearts jump from the middle of the wall to the next Verts
a, b, _ = SPREAD[1]
for k_from, k_to in ((2, 1), (3, 4)):
    y = (HEART_ROWS + 2.5) / 44 * 100
    sq.morph('Verts', 2, a, b, [WHITE, HEART], (VERT_X[k_from], y - 3, VERT_X[k_from], y + 3),
             (VERT_X[k_to], y - 3, VERT_X[k_to], y + 3), tail_start=1, tail_end=40)
heartbeat(b, s1, ks=[1, 2, 3, 4])
STORY += [('the very one who lives inside of me', lives, a), ('...wants to live inside of you', a, s1)]

# ================================================================ the choruses, line by line
def chorus_lines(c):
    e = in_e(c['things']['start'])
    big = c['name'] == 'chorus3'
    nxt_line = lambda key: {'things': c['wings']['start'], 'wings': c['reward']['start'],
                            'reward': c['store']['start'], 'store': c['store']['key'] + 1.6}.get(key)
    # every "In Christ": the light goes out from the manger, the hearts beat
    for key in ('things', 'wings', 'reward', 'right', 'confess', 'worry'):
        if key not in c: continue
        t = c[key]['start']
        manger_ring(t, (WHITE, E_COLS[len(STORY) % 6]) if e else (WHITE, WARM))
        heartbeat(t, t + 1.0, every=1)
    # "I can do all things": every prop at once
    t = c['things']['key'] - 0.5
    sq.bars('Verts', 1, t, t + 1.2, 'up', [Grad(WHITE, GOLD if not e else CYAN, mode='up'), BLACK], 1, 1, 90)
    sq.bounce(FOREST, 1, t, t + 1.0, [Grad(WARM, WHITE, mode='up')], height=100)
    sq.flash(ARCHES, 1, t, 1.0, WHITE)
    sq.fill('Spiral Trees', 0, t, t + 1.0, [Grad(WARM, WHITE, mode='up')], 0, 100, per_model=True, fadeout=0.5)
    sq.trunk_rise(t, 1.0, WHITE)
    STORY.append(('I can do all things: everything at once', c['things']['start'], c['wings']['start']))
    # "eagle's wings": wings beat up and out from the middle of the wall, the arches spread
    a, b = c['wings']['start'] + 1.0, c['reward']['start']      # from just after "In Christ" to the next line
    mid, y0 = 50, 35
    for side in (0, 100):
        down, up = (mid, y0, side, 15), (mid, y0, side, 95)
        half = (b - a) / 2
        for f in range(2):
            sq.morph('Verts', 1 if side == 0 else 2, a + f * half, a + (f + 0.7) * half, [WHITE, SKY if not e else CYAN],
                     down, up, tail_start=3, tail_end=70)
    sq.bars(ARCHES, 1, a, b, 'expand', [Grad(SKY, WHITE, mode='right'), BLACK], 1, 2)
    for k in range(4):
        sq.morph(SPIRALS[k], 0,
                 a + k * 0.2, a + k * 0.2 + 1.2, [WHITE, SKY], *DIAG['up'], tail_start=5, tail_end=60)
    if big:     # after the key change the wings span the whole yard
        for side in (0, 100):
            sq.morph('AllModels', 2, a, b, [WHITE, CYAN], (HEART_X, 30, side, 10), (HEART_X, 30, side, 95),
                     tail_start=3, tail_end=70)
    STORY.append(("eagle's wings", c['wings']['start'], c['reward']['start']))
    # "a great reward": gold sparkles everywhere and a crown on every Vert
    a, b = c['reward']['key'] - 0.3, c['store']['key'] + 1.4
    sq.twinkle('AllModels', 3, a, b, [GOLD, WHITE], count=25, steps=20, bright=80)
    for k in range(6):
        crown(k, a + k * 0.08, b - a - k * 0.08, 100, 40)
    # "that I have in store": gold fills the bottom of the wall
    sq.fill('Verts', 1, c['store']['start'], c['store']['key'] + 1.4, [Grad(GOLD, WARM, mode='up')], 0, 40, bright=70,
            fadeout=0.8)
    STORY.extend([('a great reward: gold and crowns', c['reward']['start'], c['store']['start']),
                  ('that I have in store', c['store']['start'], c['store']['key'] + 1.4)])
    if 'right' not in c: return
    # "His righteousness": a white wash rolls up the whole yard
    a, b = c['right']['key'] - 0.4, c['confess']['start']
    sq.moment(a, a + 1.6, lambda a_, b_: sq.bars('AllModels', 0, a_, b_, 'up', [Grad(WHITE, ICE, mode='up'),
                                                                                 BLACK], 1, 1), WHITE, 30)
    STORY.append(('His righteousness: clothed in white', c['right']['start'], c['confess']['start']))
    # "what I confess": the song's own voice drawn across the wall
    a, b = c['confess']['start'], c['worry']['start']
    sq.waveform('Verts', 2, a, b, [WHITE, GOLD if not e else MAGENTA], bars=6)
    STORY.append(('what I confess: the voice across the wall', a, b))
    # "don't worry about all the rest": everything settles into a gentle wave
    a = c['worry']['start']
    b = a + 4 * PER * 2
    sq.wave('Verts', 1, a, b, None, 60, waves=360, speed=6, kind='Sine', fill='Palette', thickness=30, height=40,
            colors=[SKY if not e else CYAN, WHITE])
    STORY.append(("don't worry about all the rest", a, b))
for c in CHORUSES:
    chorus_lines(c)

# ================================================================ the bridge: in Him we live and move
s0, s1 = SPAN['bridge']
move = word('live', s0)
being = word_end('being', move)
sq.bars('AllModels', 3, move, being, 'Right', [Grad(ROYAL, VIOLET, mode='up'), BLACK, Grad(MAGENTA, ROYAL, mode='up'),
                                               BLACK], 3, 2, 50)
sq.on(HOUSE + OTHER_FLOODS, 1, s0, s1, Grad(ROYAL, MAGENTA, mode='time'), 20, 70, blend=None)
sq.spirals('trees', 1, s0, s1, [ROYAL, MAGENTA], count=2, rotation=15, thickness=40, movement=2.0, bright=40,
           perModel=True)
heartbeat(s0, s1, every=2)
STORY += [('in Him we live and move: one wave through everything', move, being)]
together = word('together', being)
for t, p, d in [m for m in MELODY if together - 0.2 <= m[0] < KEY_CHANGE]:
    h = 30 + (min(max(p, 60), 76) - 60) / 16 * 70
    sq.bounce(FOREST, 1, t, t + max(min(d, 0.6), 0.3), [Grad(WARM, WHITE, mode='up')], height=h)
sq.fill('Verts', 1, together, KEY_CHANGE, [Grad(ROYAL, WARM, WHITE, mode='up')], 0, 100, bright=60)
STORY += [('as we all live in Him: everyone has the light', SPREAD[4][0], together),
          ('together we can sing: the crowd in unison', together, KEY_CHANGE)]

# ================================================================ the lift: D major -> E major
def lift(a, b):
    sq.bars('AllModels', 0, a, b, 'up', [Grad(WHITE, CYAN, MAGENTA, mode='up'), BLACK], 1, 1)
    sq.shockwave('AllModels', 1, a, b, [WHITE, MAGENTA], cx=round(HEART_X), cy=50, r_end=300, w_end=80)
sq.moment(KEY_CHANGE, KEY_CHANGE + BAR, lift, WHITE, 40)
STORY.append(('the key change: the lift', KEY_CHANGE, KEY_CHANGE + BAR))

# ================================================================ "everything I need to be" x3, "is in Christ"
reps = [w for w in [s for w2, s, e in WORDS if w2 == 'everything' and s > SPAN['everything'][0] - 1.5]][:3]
for j, t in enumerate(reps):
    t = sung(t)
    if j == 0:
        sq.bars(ARCHES, 1, t, t + 2.5, 'compress', [Grad(GOLD, WHITE, mode='right'), BLACK], 1, 1)
        sq.bars(FOREST, 2, t, t + 2.5, 'H-compress', [Grad(WARM, GOLD, mode='up'), BLACK], 1, 1, 80)
    elif j == 1:
        sq.bars('Verts', 1, t, t + 2.5, 'H-compress', [Grad(GOLD, WHITE, mode='up'), BLACK], 1, 1, 80)
    else:
        sq.shockwave('AllModels', 2, t, t + 3.0, [WHITE, GOLD], cx=round(HEART_X), cy=50, r_start=300, r_end=1,
                     w_start=70, w_end=10)
    heartbeat(t, t + 2.0, every=1)
    STORY.append((f'everything I need to be ({j + 1}): gathering in', t, t + 3.0))

# ================================================================ the stops: the band drops out, the hearts beat
for name in STOPS:
    a, b = SPAN[name]
    sq.cut(q(a), q(b))
    heartbeat(a, b)
    for i in LIT_AT:
        if lit(i, a): person(i, a, b, body=8)
    sq.on(NATIVITY, 0, a, b, WARM, 70, 70)
    for t in [t for t in IN_CHRIST if a <= t < b]:      # an "In Christ" sung over the stop still sends the light out
        manger_ring(t, (WHITE, WARM) if not in_e(t) else (WHITE, MAGENTA))
    if name != 'stop6':
        sq.shockwave('AllModels', 0, b, b + 1.2, [WHITE, HEART if not in_e(b) else MAGENTA], cx=round(HEART_X), cy=50,
                     r_end=300, w_end=70)
        sq.on(HOUSE + OTHER_FLOODS, 0, b, b + 0.8, WARM, 100, 0)
    STORY.append(({'stop1': 'He is living in my heart', 'stop2': 'In Christ', 'stop3': 'then you\'ll be able to say',
                   'stop4': 'In Christ', 'stop5': 'everything I need to be', 'stop6': 'is in Christ'}[name], a, b))

# "is in Christ": everything falls into the hearts; the breakdown is only hearts and the manger
isin = sung(word('is', reps[-1] + 1.5))
sq.cut(q(isin), q(SPAN['outro'][0]))
s0, s1 = isin, SPAN['outro'][0]
heartbeat(s0, s1, ks=list(range(6)))
for i in range(len(STICKS)):
    person(i, s0, s1, body=6)
sq.on(NATIVITY, 0, s0, s1, WARM, 100, 100)
sq.on(HOUSE, 1, s0, s1, VIOLET, 15, 15)
its = word('it', isin + 1.0)
manger_ring(sung(its), (WHITE, MAGENTA), big=False)
STORY += [('is in Christ: everything falls into the hearts', isin, SPAN['breakdown'][0]),
          ("it's in Christ: just the hearts and the manger", SPAN['breakdown'][0], s1)]

# ================================================================ the outro: the light pours back out
s0 = SPAN['outro'][0]
manger_ring(s0, (WHITE, MAGENTA, CYAN))
sq.moment(s0, s0 + 1.0, lambda a, b: sq.shockwave('AllModels', 0, a, b, [WHITE, CYAN, MAGENTA], cx=round(MANGER_X),
                                                  cy=20, r_end=300, w_end=90), MAGENTA, 20)
heartbeat(s0 + 1.0, END - 4, every=2)
sq.cut(q(END - 4), q(DUR), [el for el in sq.elements if el != NATIVITY])
heart_glow(END - 4, END + 1, 60)
for k in range(6):
    heart(k, END - 4, 5.0, 60, 0, color=E_HEARTS[k])
sq.cut(q(END - 4), q(DUR), [NATIVITY])
sq.on(NATIVITY, 0, END - 4, END + 3.0, WARM, 100, 0)          # the manger is the last light out
STORY.append(('the light pours back out', s0, END - 4))
STORY.append(('the hearts and the manger fade', END - 4, END + 3.0))

# ================================================================ timing tracks
labels = {'intro': 'Intro', 'verse1': 'Verse 1', 'pre1': 'Pre-chorus (B minor)', 'stop1': 'Stop - living in my heart',
          'chorus1': 'Chorus', 'stop2': 'Stop - In Christ', 'inst': 'Guitar', 'verse2': 'Verse 2',
          'pre2': 'Pre-chorus (B minor)', 'stop3': 'Stop - able to say', 'chorus2': 'Chorus', 'stop4': 'Stop - In Christ',
          'chorus2b': 'Chorus (righteousness)', 'stop5': 'Stop - everything I need to be', 'bridge': 'Bridge',
          'chorus3': 'Chorus in E (key change)', 'everything': 'Everything I need to be', 'stop6': 'Stop - is in Christ',
          'breakdown': "Breakdown - it's in Christ", 'outro': 'Outro'}
st = sorted(STORY, key=lambda x: x[1])
nbars = int((END - B1) / BAR) + 1
sq.tracks = [
    ('Sections', marks([SPAN[n][0] for n, _, _ in SECTIONS], [labels[n] for n, _, _ in SECTIONS], end=DUR)),
    ('Story', [(lab, q(s), q(min(e, st[i + 1][1]) if i + 1 < len(st) else e)) for i, (lab, s, e) in enumerate(st)
               if q(min(e, st[i + 1][1]) if i + 1 < len(st) else e) > q(s)]),
    ('Lyrics', marks([s for w, s, e in WORDS], [w for w, s, e in WORDS], maxlen=1.2)),
    ('In Christ', marks(IN_CHRIST, ['In Christ'] * len(IN_CHRIST), maxlen=1.0)),
    ('Crowd (light arrives)', marks(sorted(LIT_AT.values()), [STICKS[i] for i in sorted(LIT_AT, key=LIT_AT.get)],
                                    maxlen=0.5)),
    ('Bars', marks([B(n) for n in range(1, nbars + 1)], [str(n) for n in range(1, nbars + 1)], end=END)),
    ('Beats', marks(BEATS, [str((i - ev['phase']) % 4 + 1) for i in range(len(BEATS))], end=END)),
    ('Kick', marks(KICKS, maxlen=PER / 2)), ('Snare', marks(SNARES, maxlen=PER / 2)),
    ('Vocal Notes', marks([t for t, p, d in MELODY], [str(p) for t, p, d in MELODY], maxlen=PER)),
]

sq.write(OUT, dict(song='In Christ', artist='Big Daddy Weave', album='', media=media_path(SONG, 'inchrist.mp3'),
                   comment='Generated from stem-separated audio analysis (Demucs + Basic Pitch + Whisper): 118 BPM, '
                           'D major -> E major. A light passes from heart to heart until the whole crowd sings.'),
         DUR, timeline=ARGS[1] if len(ARGS) > 1 else None)
