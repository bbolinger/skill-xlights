"""Where Is My Mind? (Pixies) -> seqs/new/pixies/pixies.xsq

The song is a daydream about losing your mind under water, so the yard tells it as a story about a mind: a soft
pink-white light that drifts, gets lost, is searched for, and swims away.

- "Ooh... stop": Kim Deal's ooh raises a lavender glow over the whole yard; on "stop" it is gone.
- The lone guitar riff: the riff draws itself across the Verts like sheet music, and the mind appears, floating in
  the dark. When the drums come in it bursts into a ring across the yard.
- Kim's oohs (here and in the long outro) are ghosts: lavender light rising slowly up the Verts and spiral trees.
- Verses ("with your feet in the air and your head on the ground"): the Verts become a little world - night sky,
  stars, green ground - and on "feet in the air" the ground slides up to the top: the yard turns upside down (the
  pixel sticks hang their beats from the top, the trunks drip downward, the roof turns green and the fence fills
  with stars). "Try this trick and spin it": the whole yard spins. "Your head will collapse": rings collapse inward
  to nothing. "But there's nothing in it": darkness, and only the little mind is left, pulsing on "ask yourself".
- Choruses ("where is my mind?"): a slow searchlight sweeps the dark yard; on every "mind" a sonar ping goes out
  from a different prop and the mind is glimpsed there - left, right, then the middle. The last ping finds it.
- "Way out in the water, see it swimming": the yard goes under water (churning teal water and bubbles on the Verts,
  swells rolling through the pixel forest, bubbles racing up the trunks on the snare) and the mind swims across -
  through the Verts, leaping the arches like a dolphin, darting through the forest.
- Verse 2: the Caribbean (a sea with a sunset over it); "animals were hiding behind the rock" - the sea goes dark
  and pairs of eyes blink here and there on the Verts; "except the little fish" - a coral koi darts across the
  pixel forest and lands on a Vert, blowing a bubble for every word of "trying to talk to me".
- The breaks drain the water out of the yard; the guitar solo rises from the deep to the surface.
- Outro: an aurora with Kim's ghostly oohs rising through it while the mind wanders the yard; in the last a cappella
  ooh the band is gone and the mind floats up and out.

Drums follow the drummer (the band plays without a click; events from extract_events.py --loose).
usage: build.py [out.xsq] [timeline.json] [--force]
"""
import json, math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from seqlib import *

SONG = 'new/pixies'
HERE = song_dir(SONG)
ARGS = cli_args()
OUT = ARGS[0] if ARGS else str(SHOW / 'seqs' / SONG / 'pixies.xsq')
ev = json.load(open(HERE / 'events.json'))
BEATS, PH, PER = ev['beats'], ev['phase'], ev['per']
DUR, END = round(ev['dur'], 3), ev['end']

def B(n):
    """start of 1-based bar n (four tracker beats, ~1.46 s; the bars of summary.txt), following the drummer"""
    i = PH + 4 * (n - 1)
    return BEATS[i] if i < len(BEATS) else BEATS[-1] + (i - len(BEATS) + 1) * PER
BAR = 4 * PER

# ---------------------------------------------------------------- the props, left to right
LX = layout_x()
STICKS = sorted((m for m in LX if m.startswith('pixstk')), key=LX.get)
ARCHS = sorted((m for m in LX if m.startswith('arch-big')), key=LX.get)
SPIRALS = sorted(['Spiral Tree 2', 'Spiral Tree 3', 'little spiral - left', 'little spiral - right'], key=LX.get)
VERTS_M = sorted((m for m in LX if m.startswith('Vert-')), key=LX.get)     # single Verts, for the eyes
sq = Seq(ELEMENTS + STICKS + ARCHS + SPIRALS + VERTS_M, nlayers=15)
# Verts layers: 0 the mind/koi, 1-2 ghosts and bubbles, 3 ripples, 4 sky/water, 5 stars/bubbles, 6 ground, 7-14 riff
SCROLL_LAYERS = range(7, 15)
_x = [LX[m] for m in ARCHS + STICKS + SPIRALS + VERTS_M]
ALLX = lambda m: (LX[m] - min(_x)) / (max(_x) - min(_x)) * 100     # a prop's position across the AllModels buffer

# ---------------------------------------------------------------- colour: night, sea and dream
NIGHT, SKY, ABYSS, TEAL = '#0A0A50', '#1E50FF', '#0020C0', '#00C8A0'
TURQ, FOAM, ICE = '#00E5FF', '#7FFFD4', '#BFFFFF'
LAVENDER, VIOLET, MAGENTA, BLUE, EMERALD = '#B48CFF', '#8A2BFF', '#FF00C8', '#1E50FF', '#00FF80'
GRASS, DEEPGRASS = '#30FF50', '#00701A'
MIND = '#FF8CF0'                 # the mind: a soft pink-white light
CORAL = '#FF3050'                # the koi
EYES = '#B4FF3A'
SEA = [ABYSS, BLUE, TEAL, TURQ, FOAM, ICE]          # low to high pitch
AURORA = [VIOLET, MAGENTA, TURQ, EMERALD, BLUE]
HOUSE_FLOODS = HOUSE + FLOODS

# ---------------------------------------------------------------- what's sung and played
WORDS = [(w['word'].strip(' ,.?!').lower(), w['start'], w['end'])
         for w in json.load(open(HERE / 'lyrics.json')) if w['start'] < END]
def word(prefix, after, before=1e9):
    return next(s for w, s, e in WORDS if w.startswith(prefix) and after <= s < before)
VOX = [n for n in load_notes(HERE / 'midi' / 'vocals_basic_pitch.csv') if n[3] >= 35 and n[0] < END]
def sung(t):
    """the first sung note onset in the half second before a Whisper word time (Whisper runs late)"""
    c = [n[0] for n in VOX if t - 0.6 <= n[0] <= t + 0.1]
    return min(c) if c else t

def mono(stem, lo, hi, minv=40, gap=0.08):
    """monophonic top line of a stem: [(start, pitch, length)]"""
    ns = [n for n in load_notes(HERE / 'midi' / f'{stem}_basic_pitch.csv') if n[3] >= minv and lo <= n[2] <= hi]
    out, cl = [], []
    for n in ns:
        if cl and n[0] - cl[0][0] > gap: out.append(max(cl, key=lambda x: x[2])); cl = []
        cl.append(n)
    if cl: out.append(max(cl, key=lambda x: x[2]))
    return [(s, p, e - s) for s, e, p, v in out if s < END]
RIFF = mono('guitar', 59, 90, minv=45)             # Joey Santiago's lead line, on top of the rhythm guitar
FRANK = mono('vocals', 45, 71)                      # the sung melody
OOH_NOTES = [n for n in VOX if n[2] >= 72]          # Kim Deal's falsetto oohs (E5 and around)
OOHS, cur = [], None                                # ...merged into phrases
for s, e, p, v in OOH_NOTES:
    if cur and s - cur[1] < 0.35: cur[1] = max(cur[1], e)
    else:
        if cur: OOHS.append(tuple(cur))
        cur = [s, e]
if cur: OOHS.append(tuple(cur))
OOHS = [(s, e) for s, e in OOHS if e - s >= 0.2]

# drums: the kick and snare bands overlap on this recording, so each hit goes to whichever band it is stronger in
kv = dict(zip(ev['kick'], ev['kick_v'])); sv = dict(zip(ev['snare'], ev['snare_v']))
HITS = sorted(set(kv) | set(sv))
KICKS = [(t, kv[t]) for t in HITS if kv.get(t, 0) >= sv.get(t, 0)]
SNARES = [(t, sv[t]) for t in HITS if sv.get(t, 0) > kv.get(t, 0)]
BASS = [(t, midi(nm)) for t, e, nm in ev['bass']]

# ---------------------------------------------------------------- structure (bars of summary.txt)
SECTIONS = [('ooh-stop', 1, 3), ('intro', 3, 10), ('ooh', 10, 18), ('verse1', 18, 31), ('chorus1', 31, 38),
            ('water1', 38, 47), ('break1', 47, 49), ('verse2', 49, 63), ('chorus2', 63, 70), ('water2', 70, 79),
            ('break2', 79, 81), ('solo', 81, 88), ('verse3', 88, 101), ('chorus3', 101, 108), ('water3', 108, 117),
            ('break3', 117, 118), ('outro', 118, 148), ('coda', 148, None)]
SPAN = {n: (B(a), B(b) if b else DUR) for n, a, b in SECTIONS}
def section(t):
    return next((n for n, (a, b) in SPAN.items() if a <= t < b), 'coda')
kind = lambda t: section(t).rstrip('0123456789')

STOP = 2.675                                         # the "t" of Frank's "stop" (vocal envelope)
INTRO0 = next(t for t, p, d in RIFF if t > 3.0)      # the first guitar note
DRUMS_IN = next(t for t, v in KICKS + SNARES if t > 14.0)

VERSES = []
for name in ('verse1', 'verse3'):
    s0, s1 = SPAN[name]
    v = dict(name=name, s0=s0, s1=s1, air=word('air', s0), spin=word('spin', s0), collapse=word('collapse', s0),
             nothing=word('nothing', s0), ask=word('ask', s0))
    v['ground'] = word('ground', v['air'])
    v['flipped'] = v['ground'] + 0.5                 # the flip lands just after "ground"
    v['spun'] = min(word('yeah', v['spin']) + 0.6, v['collapse'] - 0.5)
    VERSES.append(v)
def upside_down(t):
    return any(v['air'] <= t < v['spin'] for v in VERSES)
def emptied(t):
    """inside a collapse or the empty stretch after it"""
    return any(v['collapse'] <= t < v['s1'] for v in VERSES)

CHORUS_PINGS = {}
for name in ('chorus1', 'chorus2', 'chorus3'):
    s0, s1 = SPAN[name]
    CHORUS_PINGS[name] = [sung(s) for w, s, e in WORDS if w.startswith('mind') and s0 - 1.0 <= s < s1][:3]

WATER = {}
for name in ('water1', 'water2', 'water3'):
    s0, s1 = SPAN[name]
    wt = word('water', s0, s1)
    i = next(j for j, (w, s, e) in enumerate(WORDS) if s == wt)
    WATER[name] = dict(start=sung(WORDS[i - 3][1]), water=wt, swim=word('s', wt + 0.3, s1))   # "...see it swimming"

CARIB = word('caribbean', SPAN['verse2'][0])
ANIMALS, EXCEPT = word('animals', CARIB), word('except', CARIB)
FISH_TALK = word('but', EXCEPT)

# ---------------------------------------------------------------- small helpers
def breathe(s0, s1, cols, lo=15, hi=70, period=None, els=HOUSE_FLOODS, layer=1):
    """the house and floods breathe in and out (joy_daddyweave's big lights)"""
    period = period or BAR
    k, t = 0, s0
    while t < s1 - 0.05:
        e = min(t + period, s1)
        sq.on(els, layer, t, e, cols[(k // 2) % len(cols)], lo if k % 2 == 0 else hi, hi if k % 2 == 0 else lo,
              blend=None)
        t, k = e, k + 1

def forest_waves(s0, s1, cols, bright=50, height=50):
    """sine waves rolling through the pixel sticks, evens and odds taking turns, direction flipping each bar"""
    k = 0
    while B_after(s0, k) < s1 - 0.1:
        t = B_after(s0, k)
        sq.wave(FOREST[k % 2], 2, t, min(t + 2 * PER, s1), None, bright, waves=900, speed=10, kind='Sine',
                fill='None', thickness=50, height=height, direction='Right to Left' if k % 2 == 0 else 'Left to Right',
                colors=[WHITE, cols[k % len(cols)]])
        k += 1
def B_after(t, k):
    """the k-th bar start at or after t"""
    n = next(n for n in range(1, 400) if B(n) >= t - 0.02)
    return B(n + k)

def vert_glow(x, y, t, dur, c, layer=0, a=100, b=0, h=4):
    """a small glow on the Verts canvas at (x, y) %"""
    sq.on('Verts', layer, t, t + dur, Grad(WHITE, c, mode='radial-out'), a, b,
          subbuf=sub(max(x - 8, 0), max(y - h, 0), min(x + 8, 100), min(y + h, 100)))

def mind_path(points, end, color=MIND, layer=0, glow=True):
    """the mind glides through (t, x, y) points on the Verts canvas, leaving a soft glow where it pauses"""
    for i, (t, x, y) in enumerate(points):
        t2, x2, y2 = points[i + 1] if i + 1 < len(points) else (end, x, y)
        if abs(x2 - x) > 3:
            sq.morph('Verts', layer, t, t2, [WHITE, color], (x, y - 3, x, y + 3), (x2, y2 - 3, x2, y2 + 3),
                     tail_start=1, tail_end=30, sparkles=15)
        else:
            sq.morph('Verts', layer, t, t2, [WHITE, color], (0, y, 100, y), (0, y2, 100, y2), tail_start=2,
                     tail_end=25, extra={'B_CUSTOM_SubBuffer': sub(max(x - 8, 0), 0, min(x + 8, 100), 100)})
        if glow: vert_glow(x, y, t, min(0.8, max(t2 - t, 0.3) * 1.5), color, 1 + i % 2, 70, 0)

def hop_sticks(t0, t1, rightward, colors, n=None):
    """light hopping stick to stick across the whole pixel forest between t0 and t1"""
    n = n or len(STICKS)
    step = (t1 - t0) / n
    for j in range(n):
        i = min(int(j * len(STICKS) / n), len(STICKS) - 1)
        t = t0 + j * step
        sq.bounce(STICKS[i if rightward else -1 - i], 0, t, t + max(2.5 * step, 0.2), colors, 100)

def run_arch(k, t, dur, rightward, color=MIND):
    a, b = (0, 0, 0, 100), (100, 0, 100, 100)
    sq.morph(ARCHS[k], 0, t, t + dur, [WHITE, color], *((a, b) if rightward else (b, a)), tail_start=5,
             tail_end=45, sparkles=20)

def climb_spiral(k, t, dur, color=MIND, down=False):
    sq.morph(SPIRALS[k], 0, t, t + dur, [WHITE, color], *DIAG['down' if down else 'up'], tail_start=5, tail_end=50,
             sparkles=20)

def trunk_down(t, dur, color, tree=None, layer=0):
    """a band of light running down a trunk - the upside-down world's version of trunk_ring"""
    sb = None if tree is None else sub(max(TREE_X[tree] - 8, 0), 0, min(TREE_X[tree] + 8, 100), 100)
    sq.morph('trees', layer, t, t + dur, [WHITE, color], *DIAG['down'], tail_start=10, tail_end=45,
             extra={'B_CUSTOM_SubBuffer': sb} if sb else {})

def ghost(t, dur, layer, cols=(WHITE, LAVENDER), bright=80):
    """Kim's ooh: a soft band of light rising slowly up the whole Verts canvas"""
    sq.morph('Verts', layer, t, t + dur, list(cols), *DIAG['up'], tail_start=25, tail_end=60, bright=bright)

STORY = []        # (label, start, end) for the 'Story' timing track

# ================================================================ "Ooh... stop"
o0 = OOH_NOTES[0][0] - 0.15
sq.fill('Verts', 2, o0, STOP, [Grad(LAVENDER, WHITE, mode='up')], 0, 85)
sq.fill(['trees', 'Spiral Trees'], 2, o0, STOP, [Grad(LAVENDER, WHITE, mode='up')], 0, 85, per_model=True)
sq.on([ARCHES] + FOREST + ['fenceline'] + HOUSE_FLOODS, 2, o0, STOP, LAVENDER, 0, 60)
ghost(o0, STOP - o0 + 0.6, 1)
sq.cut(q(STOP), q(INTRO0))
STORY += [('ooh...', o0, STOP), ('STOP', STOP, INTRO0)]

# ================================================================ the lone guitar: the mind appears in the dark
s0, s1 = INTRO0, SPAN['intro'][1]
sq.meteors('trees', 1, s0, s1, [ABYSS, TURQ], direction='Down', count=6, speed=6, bright=35)
sq.on('roofline-1', 1, s0, s1, NIGHT, 0, 30)
pts, n = [], 0
t = s0
while t < DRUMS_IN - 0.6:
    pts.append((t, VERT_X[2] if n % 2 == 0 else VERT_X[3], 18 + n * 6 + (8 if n % 2 else 0)))
    t, n = t + BAR, n + 1
mind_path(pts, DRUMS_IN)
STORY.append(('a mind, floating in the dark', s0, DRUMS_IN))

# ================================================================ instruments, by section
KICK_COLS = {'ooh': (VIOLET, LAVENDER), 'verse': (VIOLET, MAGENTA), 'verse2': (CORAL, MAGENTA), 'chorus': (ABYSS, BLUE),
             'water': (TEAL, TURQ), 'solo': (TURQ, MAGENTA)}
kt = [t for t, _ in KICKS]
for i, (t, v) in enumerate(KICKS):
    k, sec = kind(t), section(t)
    if k in ('ooh-stop', 'intro', 'break', 'coda') or emptied(t): continue
    d = min(max(nxt(kt, i, 0.35), 0.1), 0.35)
    j = int(t / BAR)
    cols = KICK_COLS.get('verse2' if sec == 'verse2' else k, (AURORA[j % 5], AURORA[(j + 2) % 5]))
    sq.flash(ARCHES, 0, t, d, Grad(cols[0], cols[1], mode='right'), bright=45 if k == 'chorus' else 100)
    if sec in ('verse1', 'verse3'):   # the trunks: rings up a trunk - or down it, once the world is upside down
        if upside_down(t): trunk_down(t, 0.45, VIOLET, tree=i % 3)
        else: sq.trunk_ring(t, 0.45, VIOLET, tree=i % 3)
    elif k == 'solo':
        sq.trunk_ring(t, 0.45, TURQ, tree=i % 3)

sn_n = 0
for i, (t, v) in enumerate(SNARES):
    k, sec = kind(t), section(t)
    if k in ('ooh-stop', 'intro', 'break', 'coda', 'chorus') or emptied(t): continue
    if k == 'water':                  # bubbles racing up the trunks, one trunk after another
        sq.trunk_ring(t, 0.6, FOAM, tree=sn_n % 3, bright=80)
    elif sec == 'verse2':
        if ANIMALS - 0.2 <= t < EXCEPT: continue      # the sea holds its breath
        sq.ripple('Verts', 3, t, PER * 1.5, [WHITE, FOAM], VERT_X[pingpong(sn_n, 6)], 22, radius=35, width=14)
    elif k == 'verse':                # ripples in the sky, wherever the sky currently is
        sq.ripple('Verts', 3, t, PER * 1.5, [WHITE, TURQ], VERT_X[pingpong(sn_n, 6)], 30 if upside_down(t) else 70,
                  radius=40, width=15)
    elif k in ('ooh', 'outro'):
        c = VIOLET if k == 'ooh' else AURORA[sn_n % 5]
        sq.ripple('Verts', 3, t, PER * 1.5, [WHITE, c], VERT_X[pingpong(sn_n, 6)], 30 if sn_n % 2 else 65)
    elif k == 'solo':
        sq.trunk_ring(t, 0.45, FOAM, tree=sn_n % 3)
    sn_n += 1

# the pixel sticks bounce with the drums in the verses (hanging from the top while the world is upside down)
# and in the solo (higher and higher)
for grp, hits in (('pix-evens', KICKS), ('pix-odds', SNARES)):
    times = [t for t, _ in hits]
    for i, (t, v) in enumerate(hits):
        k, sec = kind(t), section(t)
        if (k not in ('verse', 'solo')) or emptied(t): continue
        d = min(max(nxt(times, i, 0.45), 0.15), 0.45)
        if k == 'solo':
            s0, s1 = SPAN['solo']
            h = 30 + 70 * (t - s0) / (s1 - s0)
            c = SEA[min(int((t - s0) / (s1 - s0) * 6), 5)]
            sq.bounce(grp, 1, t, t + d, [Grad(c, WHITE, mode='up')], height=h)
        else:
            down = upside_down(t)
            c = TURQ if sec == 'verse2' else VIOLET
            sq.bounce(grp, 1, t, t + d, [Grad(c, WHITE, mode='down' if down else 'up')],
                      height=25 + 75 * min(max(v - 0.35, 0) / 0.6, 1), direction='Down' if down else 'Up')

# the bass: a dot on the fence, placed by pitch
bt = [t for t, _ in BASS]
for i, (t, p) in enumerate(BASS):
    k = kind(t)
    if k in ('ooh-stop', 'intro', 'break', 'coda') or emptied(t): continue
    pos = 5 + (min(max(p, 28), 52) - 28) / 24 * 90
    sq.flash('fenceline', 0, t, max(nxt(bt, i, 2 * PER), 0.075), Grad(WHITE, TURQ if k != 'verse' else GRASS),
             bright=40 if k == 'chorus' else 70, subbuf=sub(max(pos - 5, 0), 0, min(pos + 5, 100), 100), end_level=30)

# the guitar riff draws itself across the Verts, coloured from the deep (low) to foam (high)
scroll = [(t, p, min(d, PER), [WHITE, SEA[min(max((p - 59) // 3, 0), 5)]], 70 if kind(t) == 'intro' else 85)
          for t, p, d in RIFF if kind(t) in ('intro', 'water', 'solo', 'outro')]
placed = sq.melody_scroll('Verts', scroll, None, travel=BAR, lo=59, hi=80, layers=SCROLL_LAYERS)
print(f'riff scroll: {placed} of {len(scroll)} notes placed')

# the spiral trees: the riff's height in the guitar parts, the sung melody in the verses (from the top when
# the world is upside down)
def spiral_heights(notes, lo, hi, cols, keep):
    ts = [n for n in notes if keep(n[0])]
    for i, (t, p, d) in enumerate(ts):
        g = min(ts[i + 1][0] - t, 2 * PER) if i + 1 < len(ts) else min(d, 2 * PER)
        h = 15 + (min(max(p, lo), hi) - lo) / (hi - lo) * 85
        down = upside_down(t)
        sq.on('Spiral Trees', 1, t, t + max(g, 0.075), Grad(cols[0], cols[1], mode='down' if down else 'up'), 100, 50,
              subbuf=sub(0, 100 - h, 100, 100) if down else sub(0, 0, 100, h), perModel=True)
spiral_heights(RIFF, 59, 80, (TURQ, WHITE), lambda t: kind(t) in ('intro', 'water', 'solo'))
spiral_heights(FRANK, 52, 68, (MAGENTA, WHITE), lambda t: kind(t) == 'verse' or section(t) == 'verse2')

# ================================================================ Kim's oohs: ghosts
for j, (s, e) in enumerate(OOHS):
    if kind(s) not in ('ooh', 'outro', 'coda') or s < 3: continue
    dur = max(e - s + 1.2, 2.0)
    ghost(s, dur, 1 + j % 2)
    sq.fill('Spiral Trees', 0, s, s + dur, [Grad(LAVENDER, WHITE, mode='up')], 0, 100, per_model=True, bright=70,
            fadeout=dur * 0.5)

# ================================================================ backgrounds
# the band arrives (Kim's oohs over the drums)
s0, s1 = DRUMS_IN, SPAN['ooh'][1]
sq.spirals('Verts', 4, s0, s1, [ABYSS, VIOLET], count=2, thickness=50, movement=1.0, bright=25, three_d=True, swing=True)
forest_waves(s0, s1, [VIOLET, BLUE])
sq.spirals('trees', 1, s0, s1, [VIOLET, ABYSS], count=2, rotation=20, thickness=40, movement=2.0, bright=40, perModel=True)
breathe(s0, s1, [VIOLET, LAVENDER])

# the verses: a little world on the Verts that turns upside down
for v in VERSES:
    s0, air, grd, flp, spin, spun, col = v['s0'], v['air'], v['ground'], v['flipped'], v['spin'], v['spun'], v['collapse']
    for a, b, down in ((s0, air, False), (flp, spin, True), (spun, col, False)):
        sq.on('Verts', 4, a, b, Grad(NIGHT, SKY, mode='down' if not down else 'up'), bright=45)   # sky darkest overhead
        sq.twinkle('Verts', 5, a, b, [WHITE, ICE], count=12, steps=30, bright=80,
                   subbuf=sub(0, 0, 100, 50) if down else sub(0, 50, 100, 100))     # stars: wherever the sky is
        sq.on('Verts', 6, a, b, Grad(DEEPGRASS, GRASS, mode='down' if down else 'up'), bright=80,
              subbuf=sub(0, 82, 100, 100) if down else sub(0, 0, 100, 18))
        sq.on('roofline-1', 1, a, b, GRASS if down else SKY, 55 if down else 25, 55 if down else 25)
        sq.on(['window-master', 'window-char'], 1, a, b, LAVENDER, 20, 20)
        breathe(a, b, [VIOLET, MAGENTA], 10, 50, els=FLOODS)
        if down:      # the stars have fallen onto the fence
            sq.twinkle('fenceline', 1, a, b, [WHITE, ICE, SKY], count=20, steps=25, bright=70)
        sq.spirals('trees', 1, a, b, [VIOLET, ABYSS], count=2, rotation=-20 if down else 20, thickness=40,
                   movement=2.0, bright=30, perModel=True)
    # the flip: the ground slides from the bottom of the canvas to the top
    sq.on('Verts', 4, air, flp, Grad(NIGHT, SKY, mode='down'), bright=45)
    sq.morph('Verts', 6, air, flp, [GRASS, DEEPGRASS], (0, 9, 100, 9), (0, 91, 100, 91), tail_start=20, tail_end=20)
    sq.fill(FOREST, 2, air, flp, [Grad(GRASS, DEEPGRASS, mode='up')], 0, 100, per_model=True, bright=60,
            direction='Down', fadeout=0.3)
    STORY += [('feet in the air: the world turns upside down', air, flp), ('upside down', flp, spin)]

# choruses: a slow searchlight in the dark
for name in ('chorus1', 'chorus2', 'chorus3'):
    s0, s1 = SPAN[name]
    sq.pinwheel('AllModels', 3, s0, s1, [Grad(ICE, ABYSS, mode='radial-out'), BLACK], arms=2, speed=4, twist=0,
                size=100, thickness=14, xc=0, yc=-40, clockwise=name != 'chorus2', bright=45)
    sq.meteors('trees', 1, s0, s1, [ABYSS, TURQ], direction='Down', count=6, speed=6, bright=35)
    sq.twinkle(FOREST, 2, s0, s1, [ICE, BLUE], count=10, steps=40, bright=30)
    sq.on(HOUSE, 1, s0, s1, NIGHT, 20, 20)
    breathe(s0, s1, [ABYSS, VIOLET], 5, 35, period=2 * BAR, els=FLOODS)

# under water
for name in ('water1', 'water2', 'water3'):
    s0, s1 = SPAN[name]
    sq.butterfly('Verts', 4, s0, s1, [ABYSS, TEAL, BLUE, TURQ], style=1, speed=8, bright=50)
    sq.bubbles('Verts', 5, s0, s1, [WHITE, FOAM], count=5, size=3, speed=6, bright=70)
    forest_waves(s0, s1, [BLUE, TURQ, TEAL], bright=60, height=60)
    sq.spirals('trees', 1, s0, s1, [TEAL, ABYSS], count=2, rotation=12, thickness=50, movement=1.0, bright=35,
               perModel=True)
    sq.butterfly([ARCHES], 1, s0, s1, [ABYSS, TEAL, BLUE], style=1, speed=6, bright=30)
    breathe(s0, s1, [TEAL, ABYSS, TURQ], 15, 60)

# the breaks: the water drains out of the yard
for name in ('break1', 'break2', 'break3'):
    s0, s1 = SPAN[name]
    sq.cut(q(s0), q(s1))
    sq.fill('Verts', 4, s0, s1, [Grad(ABYSS, TEAL, TURQ, mode='up')], 100, 0, bright=60)
    sq.fill('trees', 1, s0, s1, [Grad(ABYSS, TEAL, mode='up')], 100, 0, per_model=True, bright=50)
    sq.fill(FOREST, 2, s0, s1, [Grad(ABYSS, TURQ, mode='up')], 100, 0, per_model=True, bright=50)
    sq.morph('Spiral Trees', 1, s0, s1, [TURQ, ABYSS], *DIAG['down'], tail_start=40, tail_end=60, bright=60)
    sq.on(HOUSE_FLOODS, 1, s0, s1, TEAL, 40, 0)
    STORY.append(('the water drains away', s0, s1))

# verse 2: the Caribbean - sea below, a sunset above; dark while the animals hide; the koi
s0, s1 = SPAN['verse2']
for a, b, sea_b, sky_b in ((s0, CARIB, 50, 0), (CARIB, ANIMALS, 55, 45), (ANIMALS, EXCEPT, 15, 8),
                           (EXCEPT, s1, 55, 40)):
    sq.butterfly('Verts', 4, a, b, [TURQ, FOAM, TEAL, BLUE], style=1, speed=9, bright=sea_b, subbuf=sub(0, 0, 100, 55))
    if sky_b:
        sq.on('Verts', 5, a, b, Grad(MAGENTA, VIOLET, NIGHT, mode='up'), sky_b if a != CARIB else 0, sky_b,
              subbuf=sub(0, 55, 100, 100))
forest_waves(s0, s1, [TURQ, FOAM, MAGENTA], bright=55)
sq.spirals('trees', 1, s0, s1, [TURQ, MAGENTA], count=2, rotation=20, thickness=40, movement=2.0, bright=35, perModel=True)
breathe(s0, ANIMALS, [MAGENTA, TURQ], 15, 65)
sq.on(HOUSE_FLOODS, 1, ANIMALS, EXCEPT, NIGHT, 10, 10)
breathe(EXCEPT, s1, [CORAL, TURQ], 15, 65)
STORY += [('swimming in the Caribbean', CARIB - 1.5, ANIMALS), ('animals hiding: eyes in the dark', ANIMALS, EXCEPT)]

# the eyes: pairs of eyes blinking here and there on the Verts while the animals hide behind the rock
rnd = random.Random(7)
n_eyes = 9
for j in range(n_eyes):
    t = ANIMALS + j * (EXCEPT - ANIMALS - 0.7) / n_eyes
    m = VERTS_M[[0, 3, 5, 1, 4, 2, 5, 0, 3][j]]
    y = rnd.uniform(15, 65)
    for x1, x2 in ((18, 32), (68, 82)):
        L = 0 if x1 == 18 else 1
        sq.on(m, L, t, t + 0.45, EYES, 90, 90, subbuf=sub(x1, y, x2, y + 2.2))
        sq.on(m, L, t + 0.6, t + 1.3, EYES, 90, 0, subbuf=sub(x1, y, x2, y + 2.2))

# the koi: darts across the forest on "except the little fish", lands on a Vert and blows a bubble per word
hop_sticks(EXCEPT, FISH_TALK, True, [Grad(CORAL, WHITE, mode='up')], n=16)
KOI_X, KOI_Y = VERT_X[4], 38
koi_end = s1 - 0.1
sq.on('Verts', 0, FISH_TALK, koi_end, Grad(WHITE, CORAL, mode='radial-out'), 100, 100,
      subbuf=sub(KOI_X - 8, KOI_Y - 3, KOI_X + 8, KOI_Y + 3))
talk = [n[0] for n in VOX if FISH_TALK <= n[0] < koi_end - 0.4]
talk = [t for i, t in enumerate(talk) if i == 0 or t - talk[i - 1] > 0.18]
for j, t in enumerate(talk):
    sq.morph('Verts', 1 + j % 2, t, t + 0.9, [WHITE, FOAM], (0, KOI_Y + 4, 100, KOI_Y + 4), (0, 100, 100, 100),
             tail_start=3, tail_end=3, extra={'B_CUSTOM_SubBuffer': sub(KOI_X - 8, 0, KOI_X + 8, 100)})
STORY += [('except the little fish (koi)', EXCEPT, FISH_TALK), ('trying to talk to me: bubbles', FISH_TALK, s1)]

# the solo: rising from the deep to the surface
s0, s1 = SPAN['solo']
sq.fill('Verts', 4, s0, s1, [Grad(ABYSS, TEAL, TURQ, FOAM, WHITE, mode='up')], 0, 100, bright=55)
sq.on(HOUSE_FLOODS, 1, s0, s1, Grad(ABYSS, TURQ, mode='time'), 10, 80, blend=None)
sq.spirals('trees', 1, s0, s1, [TEAL, ABYSS], count=2, rotation=25, thickness=40, movement=2.0, bright=35, perModel=True)
STORY.append(('rising to the surface', s0, s1))

# the outro: an aurora; Kim's oohs rise through it
s0, s1 = SPAN['outro']
sq.butterfly('Verts', 4, s0, s1, AURORA, style=1, speed=7, bright=40)
forest_waves(s0, s1, AURORA, bright=55)
sq.spirals('trees', 1, s0, s1, [VIOLET, TURQ, MAGENTA], count=3, rotation=15, thickness=40, movement=1.5, bright=40,
           perModel=True)
sq.spirals('Spiral Trees', 2, s0, s1, [VIOLET, TURQ], count=2, rotation=25, thickness=40, movement=1.5, bright=30,
           perModel=True)
breathe(s0, s1, AURORA, 15, 70)

# ================================================================ the yard-wide moments
def drums_in(a, b):
    sq.shockwave('AllModels', 0, a, b, [WHITE, LAVENDER, VIOLET], cx=50, cy=30, r_end=300, w_end=80)
sq.moment(DRUMS_IN, DRUMS_IN + 1.2, drums_in, LAVENDER)
STORY.append(('drums: the mind bursts into a ring', DRUMS_IN, DRUMS_IN + 1.2))

for vi, v in enumerate(VERSES):
    # "try this trick and spin it": the whole yard spins
    cols = [MAGENTA, TURQ, VIOLET, GRASS, BLUE, LAVENDER] if vi == 0 else [MAGENTA, VIOLET, BLUE, TURQ, EMERALD, CORAL]
    sq.moment(v['spin'], v['spun'],
              lambda a, b, cols=cols, cw=vi == 0: sq.pinwheel('AllModels', 0, a, b, cols, arms=6, speed=16, twist=90,
                                                              size=100, thickness=45, xc=0, clockwise=cw, style3d='3D'),
              MAGENTA, 0)
    STORY.append(('spin it!', v['spin'], v['spun']))
    # "your head will collapse": rings fall inward to nothing
    a, b = v['collapse'], v['nothing']
    sq.cut(q(a), q(v['s1']))
    for j in range(3):
        sq.shockwave('AllModels', j, a + j * 0.35, b, [WHITE, VIOLET if j % 2 else MAGENTA], cx=50, cy=40,
                     r_start=300, r_end=1, w_start=70, w_end=10)
    sq.on([el for el in NON_MEMBERS if el != 'trees'], 0, a, b, VIOLET, 100, 0)
    sq.fill('trees', 0, a, b, [Grad(VIOLET, WHITE, mode='up')], 100, 0, per_model=True)
    STORY.append(('your head will collapse', a, b))
    # "but there's nothing in it": dark, but for the mind; it pulses on "ask yourself"
    b2 = v['s1']
    vert_glow(VERT_X[2], 50, b, b2 - b, MIND, 0, 50, 50, h=2.5)
    for t in [n[0] for n in VOX if v['ask'] - 0.6 <= n[0] < b2 - 0.2][:4]:
        vert_glow(VERT_X[2], 50, t, 0.5, MIND, 1, 100, 0, h=5)
    STORY += [('nothing in it', b, v['ask'] - 0.5), ('ask yourself', v['ask'] - 0.5, b2)]

# the outro opens with a lavender wash over everything
a = SPAN['outro'][0]
sq.moment(a, a + BAR, lambda a, b: sq.shockwave('AllModels', 0, a, b, [WHITE, LAVENDER, VIOLET], cx=50, cy=0,
                                                r_end=300, w_end=100), LAVENDER, 0)
# ...and its two loudest oohs roll a wave of light up the whole yard
o0, o1 = SPAN['outro']
def ooh_level(s, e):
    return sum(n[3] for n in OOH_NOTES if s <= n[0] < e) / max(e - s, 0.1)
big = sorted([o for o in OOHS if o0 + 15 < o[0] < o1 - 2 and o[1] - o[0] > 1.0], key=lambda o: -ooh_level(*o))[:2]
WASHES = sorted((s, min(max(e, s + 2.5), s + 4.0)) for s, e in big)
for s, e in WASHES:
    sq.moment(s, e, lambda a, b: sq.bars('AllModels', 0, a, b, 'up', [Grad(LAVENDER, WHITE, mode='up'), BLACK], 1, 1),
              LAVENDER, 20, fade_from=80)
    STORY.append(('ooh: a wave of light rolls up the yard', s, e))

# ================================================================ the mind: lost and found
# choruses: a sonar ping from a different prop on every "mind?", and the mind glimpsed there
TARGETS = {'chorus1': [('spiral', 0), ('spiral', 3), ('verts', 0)],
           'chorus2': [('arch', 0), ('arch', 3), ('verts', 0)],
           'chorus3': [('spiral', 1), ('spiral', 2), ('verts', 1)]}
for name, pings in CHORUS_PINGS.items():
    for j, t in enumerate(pings):
        what, k = TARGETS[name][j]
        found = name == 'chorus3' and j == 2
        if what == 'spiral':
            cx = ALLX(SPIRALS[k]); sq.on(SPIRALS[k], 0, t, t + 1.4, Grad(WHITE, MIND, mode='up'), 100, 0)
        elif what == 'arch':
            cx = ALLX(ARCHS[k]); sq.on(ARCHS[k], 0, t, t + 1.4, Grad(MIND, WHITE, MIND, mode='right'), 100, 0)
        else:
            cx = (ALLX(VERTS_M[2]) + ALLX(VERTS_M[3])) / 2
            for x in (VERT_X[2], VERT_X[3]):
                vert_glow(x, 50, t, 2.5 if found else 1.4, MIND, 0, 100, 40 if found else 0, h=6 if found else 4)
        sq.shockwave('AllModels', 1, t, t + (2.0 if found else 1.4), [WHITE, ICE if not found else MIND], cx=round(cx),
                     cy=35, r_end=300 if found else 70, w_end=60 if found else 25)
        STORY.append(('where is my mind? ' + ('found!' if found else f'not at the {what}'), t, t + 1.4))

# under water: the mind swims
def swim_verts(t0, t1, rightward, wiggle=22):
    n = max(int((t1 - t0) / 0.55), 4)
    order = list(range(6)) if rightward else list(range(5, -1, -1))
    pts = [(t0 + j * (t1 - t0) / n, VERT_X[order[min(j * 6 // n, 5)]] + (j % 2) * 0.01,
            50 + wiggle * math.sin(j * math.pi / 2)) for j in range(n)]
    mind_path(pts, t1)

w = WATER['water1']
swim_verts(w['start'], w['swim'], False)
hop_sticks(w['swim'], w['swim'] + 1.6, False, [Grad(MIND, WHITE, mode='up')], n=20)
STORY.append(('way out in the water: the mind swims', w['start'], w['swim'] + 1.6))

w = WATER['water2']
span = w['swim'] - w['start']
for k in range(4):                    # leaping the arches like a dolphin
    run_arch(k, w['start'] + k * span / 4, span / 4 + 0.2, True)
sq.morph('fenceline', 3, w['swim'], min(w['swim'] + 2.0, SPAN['water2'][1]), [WHITE, MIND], (100, 0, 100, 100), (0, 0, 0, 100),
         tail_start=2, tail_end=25, sparkles=20)
STORY.append(('see it swimming: leaping the arches', w['start'], w['swim'] + 2.0))

w = WATER['water3']
mind_path([(SPAN['water3'][0], VERT_X[2], 50), (w['start'] - 0.3, VERT_X[3], 45)], w['start'], glow=True)
swim_verts(w['start'], w['swim'], True)
for k in range(4):
    climb_spiral(3 - k, w['swim'] + k * 0.45, 0.7)
STORY.append(('found, and swimming away', SPAN['water3'][0], w['swim'] + 2.0))

# the solo: the mind rises with the guitar's climb
s0, s1 = SPAN['solo']
climb = [n for n in RIFF if 124.0 <= n[0] < s1 - 0.2]
pts = [(s0 + 0.1, VERT_X[2], 8), (s0 + 2 * BAR, VERT_X[3], 14), (climb[0][0] - 0.8, VERT_X[2], 18)]
lo_, hi_ = min(p for _, p, _ in climb), max(p for _, p, _ in climb)
for j, (t, p, d) in enumerate(climb):
    if t - pts[-1][0] < 0.18: continue
    pts.append((t, VERT_X[2 + j % 2], 20 + (p - lo_) / max(hi_ - lo_, 1) * 75))
mind_path(pts, s1)
STORY.append(('the mind rises with the guitar', s0, s1))

# the outro: the mind wanders the yard, one place per ooh
o0, o1 = SPAN['outro']
busy = [(a, b) for a, b in WASHES] + [(o0, o0 + BAR)]
free = [o for o in OOHS if o0 + BAR < o[0] < o1 - 1.0 and not any(a - 0.5 < o[0] < b for a, b in busy)]
for j, (s, e) in enumerate(free):
    e = min(max(e, s + 1.6), s + 3.0)
    mode, right = ['spiral', 'verts', 'arches', 'trunks', 'fence'][j % 5], j % 2 == 0
    if mode == 'spiral':
        for k in range(4): climb_spiral(k if right else 3 - k, s + k * (e - s) / 4, (e - s) / 3)
    elif mode == 'verts':
        swim_verts(s, e, right, wiggle=30)
    elif mode == 'arches':
        for k in range(4): run_arch(k if right else 3 - k, s + k * (e - s) / 4, (e - s) / 4 + 0.15, right)
    elif mode == 'trunks':
        for k in range(3): sq.trunk_ring(s + k * (e - s) / 3, (e - s) / 2, MIND, tree=k if right else 2 - k, layer=3)
    else:
        a_, b_ = (0, 0, 0, 100), (100, 0, 100, 100)
        sq.morph('fenceline', 3, s, e, [WHITE, MIND], *((a_, b_) if right else (b_, a_)), tail_start=2, tail_end=25,
                 sparkles=20)
    STORY.append((f'the mind wanders: {mode}', s, e))

# ================================================================ coda: Kim alone; the mind floats up and away
c0 = SPAN['coda'][0]
sq.cut(q(c0), q(DUR))
last_ooh = max(e for s, e in OOHS)
for j, (s, e) in enumerate([o for o in OOHS if o[0] >= c0 - 0.3]):
    ghost(s, max(e - s + 1.5, 2.0), 1 + j % 2, bright=60)
    sq.fill('Spiral Trees', 0, s, s + max(e - s + 1.5, 2.0), [Grad(LAVENDER, WHITE, mode='up')], 0, 100, per_model=True,
            bright=55, fadeout=1.0)
sq.on(HOUSE, 1, c0, last_ooh + 1.0, LAVENDER, 35, 0)
pts = [(c0 + j * (last_ooh - c0) / 6, VERT_X[2 + j % 2], 15 + j * 13) for j in range(7)]
mind_path(pts, last_ooh + 0.6)
vert_glow(VERT_X[2], 97, last_ooh + 0.6, 2.4, MIND, 0, 70, 0, h=3)
sq.on('Nativity Spot', 0, c0, last_ooh + 3.0, LAVENDER, 30, 0)
STORY.append(('the mind floats up and away', c0, last_ooh + 3.0))

# ================================================================ timing tracks
labels = {'ooh-stop': 'Ooh... stop', 'intro': 'Guitar intro', 'ooh': 'Band in - oohs', 'verse1': 'Verse 1',
          'chorus1': 'Where is my mind?', 'water1': 'Way out in the water', 'break1': 'Break', 'verse2': 'Verse 2',
          'chorus2': 'Where is my mind?', 'water2': 'Way out in the water', 'break2': 'Break', 'solo': 'Guitar',
          'verse3': 'Verse 3', 'chorus3': 'Where is my mind?', 'water3': 'Way out in the water', 'break3': 'Break',
          'outro': 'Outro - oohs', 'coda': 'Ooh (a cappella)'}
st = sorted(STORY, key=lambda x: x[1])
nbars = next(n for n in range(1, 400) if B(n) > END)
sq.tracks = [
    ('Sections', marks([SPAN[n][0] if n != 'ooh-stop' else 0.0 for n, _, _ in SECTIONS], [labels[n] for n, _, _ in SECTIONS],
                       end=DUR)),
    ('Story', [(lab, q(s), q(min(e, st[i + 1][1]) if i + 1 < len(st) else e)) for i, (lab, s, e) in enumerate(st)
               if q(min(e, st[i + 1][1]) if i + 1 < len(st) else e) > q(s)]),
    ('Lyrics', marks([s for w, s, e in WORDS], [w for w, s, e in WORDS], maxlen=1.2)),
    ('Ooh (Kim)', [('ooh', q(s), q(e)) for s, e in OOHS if q(e) > q(s)]),
    ('Bars', marks([B(n) for n in range(1, nbars)], [str(n) for n in range(1, nbars)], end=END)),
    ('Beats', marks(BEATS, [str((i - PH) % 4 + 1) for i in range(len(BEATS))], end=END)),
    ('Kick', marks([t for t, _ in KICKS], maxlen=PER / 2)), ('Snare', marks([t for t, _ in SNARES], maxlen=PER / 2)),
    ('Guitar Riff', marks([t for t, p, d in RIFF], [str(p) for t, p, d in RIFF], maxlen=PER)),
]

sq.write(OUT, dict(song='Where Is My Mind?', artist='Pixies', album='Surfer Rosa', media=media_path(SONG, 'mind.mp3'),
                   comment='Generated from stem-separated audio analysis (Demucs + Basic Pitch + Whisper); beats follow '
                           'the drummer. A mind drifts, is lost under water, searched for and found.'),
         DUR, timeline=ARGS[1] if len(ARGS) > 1 else None)
