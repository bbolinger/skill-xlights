"""Shine Your Way (Owl City & Yuna, from The Croods) -> seqs/new/owl/shine.xsq

The whole song is one sunrise. It starts "just before the dawn, when the light's still gone" and the bridge sings
"darkness is fading, we've found our way to the light" just as the key lifts from C# major to Eb major - so the
show is a night that turns into day, led by a spark.

- The sky clock: the Verts are the sky (a gradient from the horizon up), the roofline wears the colour of the sky
  overhead and the windows the colour of the horizon. Every bar the sky moves on: night with stars -> indigo ->
  violet twilight -> blue -> pink dawn -> the sunrise in the bridge -> daylight after the key change.
- The spark: a firefly-green light (an Owl City nod, and the show's DreamsOfFireflies) alone in the dark at the
  start. It wanders while "you may not know where to go", builds a fire on "build a fire from a spark", hides on
  "don't conceal it", takes a leap of faith over the whole yard and flies up and away, walks then runs ("don't have
  to walk, now you can run") and bursts through the arches ("nothing can get in your way"). In the bridge it rises
  and becomes the sun.
- The road: the fence is "the way". Every time "your way" is sung another stretch of it lights up, left to right,
  until "we've found our way to the light" completes it; after that it stays lit.
- "Shine, shine, shine, shine": each "shine" bursts from the next arch, left to right, and sends a ring across the
  yard.
- "All of your tears will dry faster in the sun": blue tears fall down the wall and the trunks, then on "sun" warm
  light rises up and dries them into rising sparkles; "starting today" lights the horizon.
- The bridge: "breaking" cracks the horizon open, the stars fade on "darkness is fading", and the sun rises over the
  whole yard. The key change is daybreak. "Like a star burning bright, lighting up your darkest night" - the sky
  dims and a star spins on the wall. "Sent here to show me the way" - the light walks the arches and the road.
- Owl City's sparkle: the synth line glints on the pixel sticks (low notes left, high notes right).
- Instruments underneath: kick (four on the floor) -> arches in the sky's colours; snare -> rings up the trunks;
  bass -> a dot on the road; the sung melody -> how high the spiral trees glow.

usage: build.py [out.xsq] [timeline.json] [--force]
"""
import json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from seqlib import *

SONG = 'new/owl'
HERE = song_dir(SONG)
ARGS = cli_args()
OUT = ARGS[0] if ARGS else str(SHOW / 'seqs' / SONG / 'shine.xsq')
ev = json.load(open(HERE / 'events.json'))
T0, PER = ev['t0'], ev['per']
BAR = 4 * PER
B1 = T0 + ev['phase'] * PER
B = lambda n: B1 + (n - 1) * BAR            # start of 1-based bar n (2.0 s at 120 BPM)
DUR, END = round(ev['dur'], 3), ev['end']

# ---------------------------------------------------------------- the props
LX = layout_x()
STICKS = sorted((m for m in LX if m.startswith('pixstk')), key=LX.get)
ARCHS = sorted((m for m in LX if m.startswith('arch-big')), key=LX.get)
SPIRALS = sorted(['Spiral Tree 2', 'Spiral Tree 3', 'little spiral - left', 'little spiral - right'], key=LX.get)
sq = Seq(ELEMENTS + STICKS + ARCHS + SPIRALS, nlayers=10)
# Verts layers: 0 the spark, 1 fire / star / rays, 2 tears / horizon / gold, 3 ripples, 4 stars, 5 the sky
_x = [LX[m] for m in ARCHS + STICKS + SPIRALS] + [LX[m] for m in LX if m.startswith('Vert-')]
ALLX = lambda m: (LX[m] - min(_x)) / (max(_x) - min(_x)) * 100
MID_X = 56                                   # the middle of the yard in the AllModels buffer

# ---------------------------------------------------------------- colour
FIREFLY = '#D4FF5A'                          # the spark: firefly green-gold
GOLD, PINK, CORAL, SKY, CYAN = '#FFC832', '#FF3C8C', '#FF4F6E', '#3CA0FF', '#00E5FF'
VIOLET, MAGENTA, INDIGO, NIGHT = '#8A2BFF', '#FF00C8', '#2A1490', '#04041C'
TEAR, ICE, LIME, WARMWHITE = '#5AB4FF', '#BFFFFF', '#9DFF3A', '#FFF0DC'
CANDY = [SKY, PINK, CYAN, GOLD, VIOLET, LIME]                    # daylight: Owl City candy colours

def hx(c): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
def mix(a, b, f): return '#' + ''.join(f'{round(x + (y - x) * f):02X}' for x, y in zip(hx(a), hx(b)))

# ---------------------------------------------------------------- words and notes
WORDS = [(w['word'].strip(' ,.?!').lower(), w['start'], w['end'])
         for w in json.load(open(HERE / 'lyrics.json')) if w['start'] < END]
def word(prefix, after, before=1e9):
    return next(s for w, s, e in WORDS if w.startswith(prefix) and after <= s < before)
def word_end(prefix, after):
    return next(e for w, s, e in WORDS if w.startswith(prefix) and after <= s)
VOX = [n for n in load_notes(HERE / 'midi' / 'vocals_basic_pitch.csv') if n[3] >= 40 and n[0] < END]
def sung(t, back=0.45):
    c = [n[0] for n in VOX if t - back <= n[0] <= t + 0.1]
    return min(c) if c else t
def mono(stem, lo, hi, minv=40, gap=0.06):
    ns = [n for n in load_notes(HERE / 'midi' / f'{stem}_basic_pitch.csv') if n[3] >= minv and lo <= n[2] <= hi
          and n[0] < END]
    out, cl = [], []
    for n in ns:
        if cl and n[0] - cl[0][0] > gap: out.append(max(cl, key=lambda x: x[2])); cl = []
        cl.append(n)
    if cl: out.append(max(cl, key=lambda x: x[2]))
    return [(s, p, e - s) for s, e, p, v in out]
MELODY = mono('vocals', 50, 84)
SYNTH = mono('other', 60, 100)                # Owl City's synth sparkle
KICKS, SNARES = ev['kick'], ev['snare']
BASS = [(t, midi(nm)) for t, e, nm in ev['bass']]

# ---------------------------------------------------------------- structure (bars of 2 s)
SECTIONS = [('night', 1, 4), ('dawn', 4, 12), ('verse1', 12, 20), ('pre1', 20, 28), ('chorus1', 28, 32),
            ('synth1', 32, 34), ('verse2', 34, 50), ('pre2', 50, 58), ('chorus2', 58, 62), ('synth2', 62, 64),
            ('bridge', 64, 71), ('day', 71, 86), ('final', 86, 101), ('end', 101, None)]
SPAN = {n: (B(a) if a > 1 else 0.0, B(b) if b else DUR) for n, a, b in SECTIONS}
section = lambda t: next((n for n, (a, b) in SPAN.items() if a <= t < b), 'end')
kind = lambda t: section(t).rstrip('0123456789')
KEY_CHANGE = SPAN['day'][0]                  # C# major -> Eb major: daybreak
DRUMS_IN = SPAN['verse1'][0]

# ---------------------------------------------------------------- the sky clock
SKY_KEYS = [  # time, overhead, horizon, brightness
    (0.0, NIGHT, INDIGO, 30), (DRUMS_IN, NIGHT, '#1A1060', 35), (SPAN['pre1'][0], '#06082C', '#3C1478', 40),
    (SPAN['chorus1'][0], '#0A1450', VIOLET, 45), (SPAN['verse2'][0], '#0A1E8C', '#5028FF', 45),
    (SPAN['pre2'][0], '#1430B4', '#C83CC8', 50), (SPAN['chorus2'][0], '#1430B4', PINK, 55),
    (SPAN['bridge'][0], '#0A1E8C', '#C83CC8', 45), (KEY_CHANGE - 0.01, '#3C78E6', GOLD, 55),
    (KEY_CHANGE, SKY, '#FFE6A0', 60), (SPAN['final'][0], '#50B4FF', WARMWHITE, 65), (DUR, '#50B4FF', WARMWHITE, 65)]
def sky(t):
    for (a, ta, ha, ba), (b, tb, hb, bb) in zip(SKY_KEYS, SKY_KEYS[1:]):
        if a <= t < b or b == DUR:
            f = (t - a) / (b - a) if b > a else 0
            return mix(ta, tb, f), mix(ha, hb, f), round(ba + (bb - ba) * f)
horizon = lambda t: sky(t)[1]

STORY = []

# ---------------------------------------------------------------- helpers
def vert_glow(x, y, t, dur, c, layer=0, a=100, b=0, h=4, w=8):
    sq.on('Verts', layer, t, t + dur, Grad(WHITE, c, mode='radial-out'), a, b,
          subbuf=sub(max(x - w, 0), max(y - h, 0), min(x + w, 100), min(y + h, 100)))

def spark_path(points, end, color=FIREFLY, layer=0):
    """the spark glides through (t, x, y) points on the Verts canvas, glowing where it pauses"""
    for i, (t, x, y) in enumerate(points):
        t2, x2, y2 = points[i + 1] if i + 1 < len(points) else (end, x, y)
        if abs(x2 - x) > 3:
            sq.morph('Verts', layer, t, t2, [WHITE, color], (x, y - 3, x, y + 3), (x2, y2 - 3, x2, y2 + 3),
                     tail_start=1, tail_end=30, sparkles=30)
        elif abs(y2 - y) > 2:
            sq.morph('Verts', layer, t, t2, [WHITE, color], (0, y, 100, y), (0, y2, 100, y2), tail_start=2,
                     tail_end=25, sparkles=30, extra={'B_CUSTOM_SubBuffer': sub(max(x - 8, 0), 0, min(x + 8, 100), 100)})
        else:
            vert_glow(x, y, t, t2 - t, color, layer, 100, 80)

def hop_sticks(t0, t1, rightward, colors, n=None, i0=0, i1=None):
    i1 = len(STICKS) if i1 is None else i1
    span = list(range(i0, i1))
    n = n or len(span)
    step = (t1 - t0) / n
    for j in range(n):
        i = span[min(int(j * len(span) / n), len(span) - 1)]
        sq.bounce(STICKS[i if rightward else len(STICKS) - 1 - i], 0, t0 + j * step,
                  t0 + j * step + max(2.5 * step, 0.2), colors, 100)

def run_arch(k, t, dur, rightward=True, color=FIREFLY):
    a, b = (0, 0, 0, 100), (100, 0, 100, 100)
    sq.morph(ARCHS[k], 0, t, t + dur, [WHITE, color], *((a, b) if rightward else (b, a)), tail_start=5,
             tail_end=45, sparkles=30)

def climb_spiral(k, t, dur, color=FIREFLY):
    sq.morph(SPIRALS[k], 0, t, t + dur, [WHITE, color], *DIAG['up'], tail_start=5, tail_end=50, sparkles=30)

def fence_run(t, dur, x0, x1, color=FIREFLY, layer=1):
    sq.morph('fenceline', layer, t, t + dur, [WHITE, color], (x0, 0, x0, 100), (x1, 0, x1, 100), tail_start=2,
             tail_end=25, sparkles=30)

def breathe(s0, s1, cols_, lo=15, hi=70, els=('grinch-1',), layer=1):
    k, t = 0, s0
    while t < s1 - 0.05:
        e = min(t + BAR, s1)
        sq.on(list(els), layer, t, e, cols_[(k // 2) % len(cols_)], lo if k % 2 == 0 else hi, hi if k % 2 == 0 else lo,
              blend=None)
        t, k = e, k + 1

# ================================================================ the sky, bar by bar
n = 1
while B(n) < END + 2:
    a, b = B(n), min(B(n + 1), DUR)
    top, hor, br = sky(a)
    top2, hor2, br2 = sky(b - 0.01)
    sq.on('Verts', 5, a, b, Grad(hor, top, mode='up'), br, br2)
    sq.on('roofline-1', 1, a, b, top, 35, 35)
    sq.on(['window-master', 'window-char'], 1, a, b, hor, 40, 40)
    n += 1
# stars, until the darkness fades
FADING = word('darkness', SPAN['bridge'][0])
sq.twinkle('Verts', 4, 0.0, FADING + 2.0, [WHITE, ICE], count=10, steps=35, bright=70, subbuf=sub(0, 45, 100, 100))
sq.twinkle(FOREST, 2, 0.0, DRUMS_IN, [WHITE, ICE], count=6, steps=40, bright=40)
breathe(DRUMS_IN, END, [VIOLET, PINK, SKY])
sq.on('Nativity Spot', 1, 0.0, END + 3, WARMWHITE, 25, 25)

# ================================================================ instruments
for i, t in enumerate(KICKS):
    k = kind(t)
    if k in ('night', 'dawn', 'end'): continue
    d = min(max(nxt(KICKS, i, 0.3), 0.1), 0.3)
    c2 = CANDY[i % 6] if t >= KEY_CHANGE else WHITE
    sq.flash(ARCHES, 0, t, d, Grad(horizon(t), c2, mode='right'), bright=85)

for i, t in enumerate(SNARES):
    k = kind(t)
    if k in ('night', 'dawn', 'end'): continue
    if i + 1 < len(SNARES) and SNARES[i + 1] - t < PER * 0.6: continue
    sq.trunk_ring(t, 0.45, CANDY[i % 6] if t >= KEY_CHANGE else horizon(t), tree=i % 3)
    if k in ('synth', 'day', 'final'):
        sq.ripple('Verts', 3, t, PER * 1.5, [WHITE, CANDY[i % 6] if t >= KEY_CHANGE else horizon(t)],
                  VERT_X[pingpong(i, 6)], 30 if i % 2 else 70)

bt = [t for t, _ in BASS]
for i, (t, p) in enumerate(BASS):
    if kind(t) in ('night', 'dawn', 'end'): continue
    pos = 5 + (min(max(p, 30), 54) - 30) / 24 * 90
    sq.flash('fenceline', 0, t, max(nxt(bt, i, 2 * PER), 0.075), Grad(WHITE, CANDY[p % 6] if t >= KEY_CHANGE else SKY),
             bright=60, subbuf=sub(max(pos - 4, 0), 0, min(pos + 4, 100), 100), end_level=25)

for i, (t, p, d) in enumerate(MELODY):
    if kind(t) in ('synth', 'end'): continue
    g = min(MELODY[i + 1][0] - t, 2 * PER) if i + 1 < len(MELODY) else min(d, 2 * PER)
    h = 15 + (min(max(p, 58), 80) - 58) / 22 * 85
    c = CANDY[i % 6] if t >= KEY_CHANGE else horizon(t)
    sq.on('Spiral Trees', 1, t, t + max(g, 0.075), Grad(c, WHITE, mode='up'), 100, 50, subbuf=sub(0, 0, 100, h),
          perModel=True)

# Owl City's synth sparkle: glints on the pixel sticks, low notes left, high notes right
GLINTS = [n for n in SYNTH if kind(n[0]) in ('night', 'dawn', 'synth', 'bridge', 'end')]
pitches = sorted(p for _, p, _ in GLINTS)
cdf = lambda p: (sum(x < p for x in pitches) + sum(x == p for x in pitches) / 2) / len(pitches)   # spread by how
for j, (t, p, d) in enumerate(GLINTS):                                                             # common each note is
    i = cdf(p) * (len(STICKS) - 1) + [0, 2, -2, 1, -1][j % 5]
    i = min(max(round(i), 0), len(STICKS) - 1)
    c = CANDY[j % 6] if t >= KEY_CHANGE else [ICE, FIREFLY, PINK][j % 3]
    sq.bounce(STICKS[i], 1, t, t + min(max(d, 0.25), 0.6), [Grad(c, WHITE, mode='up')], 100)

# sine waves through the forest while the band plays (the forest is quiet in the night and dawn)
for name in ('verse1', 'pre1', 'chorus1', 'verse2', 'pre2', 'chorus2', 'day', 'final'):
    s0, s1 = SPAN[name]
    k = 0
    while s0 + k * BAR < s1 - 0.1:
        t = s0 + k * BAR
        c = CANDY[k % 6] if t >= KEY_CHANGE else horizon(t)
        sq.wave(FOREST[k % 2], 2, t, min(t + 2 * PER, s1), None, 50, waves=900, speed=10, kind='Sine', fill='None',
                thickness=50, height=50, direction='Right to Left' if k % 2 == 0 else 'Left to Right',
                colors=[WHITE, c])
        k += 1
    if name not in ('verse1', 'verse2'):
        sq.spirals('trees', 1, s0, s1, [horizon(s0), WHITE if s0 < KEY_CHANGE else CANDY[0]], count=2, rotation=20,
                   thickness=40, movement=2.0, bright=40, perModel=True)

# ================================================================ the road: every "your way" lights more of it
WAYS = [s for w, s, e in WORDS if w == 'way' and s < FADING + 6]
road_end = word_end('way', FADING)       # "...we've found our way to the light"
for j, t in enumerate(WAYS):
    frac = min((j + 1) / len(WAYS) * 100, 100)
    t_next = WAYS[j + 1] if j + 1 < len(WAYS) else END
    lo_ = (j / len(WAYS)) * 100
    fence_run(t, 0.8, max(lo_ - 2, 0), frac, color=WARMWHITE, layer=1)
    sq.on('fenceline', 2, t + 0.8, t_next, Grad(WARMWHITE, horizon(t), mode='right'), 35, 35,
          subbuf=sub(0, 0, frac, 100))
STORY.append(('the road lights up a little with every "your way"', WAYS[0], road_end))

# ================================================================ night and dawn: the spark alone
s0, s1 = 1.0, SPAN['dawn'][1]
sung_dawn = word('dawn', s0)
pts = [(1.2, VERT_X[2], 30), (3.2, VERT_X[3], 42), (5.2, VERT_X[2], 55), (sung_dawn - 0.6, VERT_X[3], 45)]
spark_path(pts, sung_dawn)
STORY.append(('a spark in the dark', 1.2, sung_dawn))
shines_dawn = [sung(s) for w, s, e in WORDS if w == 'shine' and s0 < s < s1]
lost0, lost1 = word('you', word('and', 15)), word('go', 15) + 0.4
pts = [(sung_dawn, VERT_X[3], 45)]
for j, t in enumerate(shines_dawn):
    if t < lost0:
        pts.append((t, VERT_X[2 + j % 2], 50 + 8 * (j % 2)))
for j, x in enumerate([1, 4, 2, 3]):          # "you may not know where to go": this way... that way...
    pts.append((lost0 + j * (lost1 - lost0) / 4, VERT_X[x], 40))
for j, t in enumerate([s for s in shines_dawn if s > lost1]):
    pts.append((t, VERT_X[2 + j % 2], 52))
spark_path(pts, DRUMS_IN)
for t in shines_dawn:
    vert_glow(pts[0][1], 50, t, 0.8, FIREFLY, 1, 100, 0, h=10, w=12)
STORY += [('shine, shine your way', sung_dawn, lost0), ('you may not know where to go', lost0, lost1)]

# ================================================================ verse 1
road, fire, spark_w = word('open', DRUMS_IN), word('fire', DRUMS_IN), word('spark', DRUMS_IN)
feed, conceal, find = word('feed', spark_w), word('conceal', spark_w), word('find', spark_w)
sq.moment(DRUMS_IN, DRUMS_IN + 0.8, lambda a, b: sq.shockwave('AllModels', 0, a, b, [WHITE, FIREFLY], cx=MID_X, cy=40,
                                                              r_end=300, w_end=60), FIREFLY, 0)
# "open road but it's still dark": the spark goes to the start of the road
fence_run(road, fire - road, 0, 12, FIREFLY)
spark_path([(DRUMS_IN + 0.8, VERT_X[2], 50), (road + 0.5, VERT_X[2], 30), (fire - 0.6, VERT_X[2], 8)], fire)
# "build a fire from a spark": a fire grows at the bottom of the wall, flares on "feed", dies to embers
def fire_fx(a, b, height, fadeout=0):
    st = {'E_CHECKBOX_Fire_GrowWithMusic': 0, 'E_CHOICE_Fire_Location': 'Bottom', 'E_SLIDER_Fire_Height': height,
          'E_SLIDER_Fire_HueShift': 0, 'E_TEXTCTRL_Fire_GrowthCycles': 0.0}
    if fadeout: st['T_TEXTCTRL_Fadeout'] = f'{fadeout:.2f}'
    sq.add('Verts', 1, 'Fire', a, b, st, [WHITE])
fire_fx(fire, spark_w + 0.6, 20)
fire_fx(spark_w + 0.6, feed, 35)
fire_fx(feed, feed + 1.4, 55)
fire_fx(feed + 1.4, conceal, 35, fadeout=0.8)
sq.trunk_rise(fire, 1.5, CORAL)
STORY += [('open road but it\'s still dark', road, fire), ('build a fire from a spark', fire, feed),
          ('feed the feeling in your heart', feed, conceal)]
# "don't conceal it": the light hides, "then you'll start to find, find your way": the spark runs the road
sq.cut(q(conceal), q(find), ['Verts'], layers=[3, 4])
sq.on('Verts', 4, conceal, find, NIGHT, 60, 60)
find_end = word_end('way', find)
fence_run(find, find_end - find + 0.6, 0, 100, FIREFLY, layer=3)
hop_sticks(find, find_end + 0.6, True, [Grad(FIREFLY, WHITE, mode='up')], n=16)
STORY += [("don't conceal it", conceal, find), ('find your way: the spark runs the road', find, find_end + 0.6)]

# ================================================================ pre-choruses: tears dry faster in the sun
def tears_and_sun(name):
    s0, s1 = SPAN[name]
    tears, sun = word('tears', s0), word('sun', s0)
    today = word('today', sun)
    sq.meteors('Verts', 2, tears - 0.6, sun, [TEAR, ICE], direction='Down', count=12, speed=10, bright=80)
    sq.meteors('trees', 0, tears - 0.6, sun, [TEAR, ICE], direction='Down', count=8, speed=10, bright=80)
    sq.fill('Verts', 2, sun, sun + 1.6, [Grad(PINK, GOLD, WARMWHITE, mode='up')], 0, 100, bright=85, fadeout=0.6)
    sq.meteors('Verts', 1, sun + 0.4, today, [GOLD, WHITE], direction='Up', count=10, speed=12, bright=70)
    sq.trunk_rise(sun, 1.6, GOLD)
    sq.on(HOUSE + ['grinch-1'], 0, sun, sun + 1.6, GOLD, 100, 30)
    # "starting today": the horizon lights up
    sq.morph('Verts', 2, today - 0.3, today + 1.2, [WHITE, GOLD], (0, 3, 100, 3), (0, 10, 100, 10), tail_start=10,
             tail_end=10)
    STORY.extend([('all of your tears...', tears - 0.6, sun), ('...dry faster in the sun', sun, today - 0.3),
                  ('starting today', today - 0.3, s1)])
    return sun

s0 = SPAN['pre1'][0]
begun = word('begun', s0)
sq.bars('Verts', 2, word('no', s0 - 1), begun + 0.6, 'up', [Grad(horizon(s0), WHITE, mode='up'), BLACK], 3, 2, 60)
STORY.append(('no one can stop what has begun', word('no', s0 - 1), begun + 0.6))
tears_and_sun('pre1')

s0 = SPAN['pre2'][0]
walk_w, run_w, nothing = word('walk', s0 - 1), word('run', s0 - 1), word('nothing', s0 - 1)
way2 = word_end('way', nothing)
fence_run(sung(word("don't", s0 - 1)), run_w - word("don't", s0 - 1), 0, 25, FIREFLY, layer=3)     # walking...
for j in range(3):                                                                          # ...running
    fence_run(run_w + j * (nothing - run_w) / 3, (nothing - run_w) / 3, 0 if j % 2 == 0 else 100,
              100 if j % 2 == 0 else 0, FIREFLY, layer=3)
for k in range(4):                     # "nothing can get in your way": it bursts through the arches
    run_arch(k, nothing + k * (way2 - nothing) / 4, (way2 - nothing) / 4 + 0.2)
    sq.shockwave('AllModels', 1, nothing + k * (way2 - nothing) / 4, nothing + k * (way2 - nothing) / 4 + 0.8,
                 [WHITE, FIREFLY], cx=round(ALLX(ARCHS[k])), cy=10, r_end=60, w_end=25)
STORY += [("don't have to walk...", walk_w - 1, run_w), ('...now you can run', run_w, nothing),
          ('nothing can get in your way', nothing, way2)]
tears_and_sun('pre2')

# ================================================================ "shine, shine, shine, shine": one arch after another
def shine_burst(t, k, color):
    sq.flash(ARCHS[k], 0, t, 0.6, Grad(WHITE, color, mode='right'))
    sq.shockwave('AllModels', 1, t, t + 1.0, [WHITE, color], cx=round(ALLX(ARCHS[k])), cy=10, r_end=130, w_end=35)
    climb_spiral(k, t, 0.6, color)
for name in ('chorus1', 'chorus2', 'final'):
    s0, s1 = SPAN[name]
    shines = [sung(s) for w, s, e in WORDS if w == 'shine' and s0 - 1.5 <= s < s1 - 0.5]
    group, last = 0, None
    for t in shines:
        if last is not None and t - last > 2.5: group = 0          # a new "shine, shine..." line starts at the left
        c = CANDY[group % 6] if t >= KEY_CHANGE else [GOLD, PINK, SKY, FIREFLY][group % 4]
        shine_burst(t, group % 4, c)
        group, last = group + 1, t
    STORY.append((f'shine, shine, shine: arch after arch', shines[0], shines[0] + 5))

# synth hooks after the choruses: rays across the wall
for name in ('synth1', 'synth2'):
    s0, s1 = SPAN[name]
    for j in range(int((s1 - s0) / BAR)):
        a, b = DIAG['right' if j % 2 == 0 else 'left']
        sq.morph('Verts', 1, s0 + j * BAR, s0 + j * BAR + 1.4, [WHITE, [PINK, SKY][j % 2]], a, b, tail_start=5,
                 tail_end=60, bright=80)

# ================================================================ verse 2
s0, s1 = SPAN['verse2']
sky_w = word('sky', s0)
sq.bars('Verts', 2, sung(word('open', s0)), sky_w + 1.0, 'H-expand', [Grad(SKY, WHITE, mode='up'), BLACK], 1, 1, 70)
STORY.append(("there's an open sky", word('open', s0), sky_w + 1.0))
pts = [(sky_w + 1.0, VERT_X[2], 50)]
for j, t in enumerate([sung(s) for w, s, e in WORDS if w == 'shine' and s0 < s < s1]):
    pts.append((t, VERT_X[[1, 4, 0, 5, 2, 3][j % 6]], 45 + 10 * (j % 2)))
guide = word('guide', s0)
deep = word('deep', s0)
sq.fill('Spiral Trees', 0, deep, guide, [Grad(FIREFLY, WHITE, mode='up')], 0, 70, per_model=True, bright=80)
pts = [p for p in pts if p[0] < deep] + [(deep, VERT_X[2], 30), (guide, VERT_X[0], 50), (guide + 2.5, VERT_X[5], 50)]
spark_path(pts, word('waste', s0) - 1.0)
STORY += [('a feeling deep inside you', deep, guide), ('let it be your guide', guide, guide + 2.5)]
# "gotta take a leap of faith and fly, fly away": a leap over the whole yard, then up and away
leap, fly = word('leap', s0), word('fly', s0)
away = word_end('away', fly)
N = 10
for j in range(N):
    x1, x2 = 2 + j * 96 / N, 2 + (j + 1) * 96 / N
    y1, y2 = [8 + 85 * math.sin(math.pi * x / 100) for x in (x1, x2)]
    sq.morph('AllModels', 0, leap - 0.4 + j * (fly - leap + 0.4) / N, leap - 0.4 + (j + 1.6) * (fly - leap + 0.4) / N,
             [WHITE, FIREFLY], (x1, y1 - 3, x1, y1 + 3), (x2, y2 - 3, x2, y2 + 3), tail_start=1, tail_end=40, sparkles=40)
for k in range(4):
    climb_spiral(k, fly + k * 0.25, 1.0)
spark_path([(fly, VERT_X[5], 20), (fly + 0.7, VERT_X[4], 45), (fly + 1.3, VERT_X[3], 70), (away, VERT_X[2], 99)], away + 0.3)
STORY += [('a leap of faith over the whole yard', leap - 0.4, fly), ('fly, fly away', fly, away)]

# ================================================================ the bridge: the sunrise
s0, s1 = SPAN['bridge']
breaking, light_w, sight = word('breaking', s0), word('light', s0), word('sight', s0)
spark_path([(s0, VERT_X[2], 70), (breaking - 0.5, VERT_X[3], 40), (breaking, VERT_X[2], 12)], breaking + 0.2)
sq.morph('Verts', 2, breaking, breaking + 1.5, [WHITE, PINK], (50, 4, 50, 4), (0, 4, 100, 4), tail_start=20, tail_end=20)
fence_run(breaking, 1.5, 50, 0, PINK, layer=3)
STORY += [('breaking: the horizon cracks open', breaking, FADING), ('darkness is fading', FADING, light_w - 1.2)]
# the spark rises and becomes the sun - a sun rising over the whole yard
sun0, sun1 = light_w - 1.2, KEY_CHANGE
STEPS = 16
for j in range(STEPS):
    a = sun0 + j * (sun1 - sun0) / STEPS
    cy = -30 + j * 70 / (STEPS - 1)
    r = 18 + j * 0.8
    sq.on('AllModels', 2, a, a + (sun1 - sun0) / STEPS + 0.05,
          Grad((0, WHITE), (0.25, GOLD), (0.6, PINK), (1, BLACK), mode='radial-out'), 100, 100,
          subbuf=sub(MID_X - r, cy - r * 2, MID_X + r, cy + r * 2))
sq.pinwheel('Verts', 1, sight - 0.5, sun1, [Grad(GOLD, PINK, mode='radial-out'), BLACK, Grad(WHITE, GOLD, mode='radial-out'),
                                             BLACK], arms=12, speed=3, twist=0, size=100, thickness=8, xc=0, yc=-80,
            bright=70)
STORY += [("we've found our way to the light: the sun rises", sun0, sight - 0.5), ("such a beautiful sight", sight - 0.5, sun1)]

# ================================================================ the key change: daybreak
def daybreak(a, b):
    sq.shockwave('AllModels', 0, a, b, [WHITE, GOLD, SKY], cx=MID_X, cy=0, r_end=300, w_end=120)
    sq.bars('AllModels', 1, a, b, 'up', [Grad(GOLD, WHITE, SKY, mode='up'), BLACK], 1, 1)
sq.moment(KEY_CHANGE, KEY_CHANGE + BAR, daybreak, WARMWHITE, 40)
STORY.append(('daybreak (key change)', KEY_CHANGE, KEY_CHANGE + BAR))

# "anytime, anywhere": light pops up all over the yard; "turn around"
s0 = KEY_CHANGE
anyt, turn = word('anytime', s0), word('turn', s0)
for j, (m, t) in enumerate(zip([SPIRALS[0], ARCHS[3], SPIRALS[2], ARCHS[0], SPIRALS[3], ARCHS[1]],
                               [anyt + j * (turn - anyt) / 6 for j in range(6)])):
    sq.shockwave('AllModels', 1, t, t + 0.8, [WHITE, CANDY[j]], cx=round(ALLX(m)), cy=30, r_end=50, w_end=25)
sq.pinwheel('AllModels', 3, turn, turn + 2.0, [GOLD, BLACK, SKY, BLACK], arms=4, speed=12, twist=40, size=100,
            thickness=40, bright=50)
STORY += [('anytime, anywhere', anyt, turn), ('turn around', turn, turn + 2.0)]
# "like a star burning bright, lighting up your darkest night": the sky dims and a star spins on the wall
star, night_w = word('star', s0), word('night', s0)
star_end = word_end('way', night_w)
sq.cut(q(star - 0.3), q(star_end), ['Verts'], layers=[5])
sq.on('Verts', 5, star - 0.3, star_end, Grad(INDIGO, NIGHT, mode='up'), 40, 40)
sq.twinkle('Verts', 4, star - 0.3, star_end, [WHITE, ICE], count=10, steps=30, bright=70)
sq.pinwheel('Verts', 1, star - 0.2, star_end, [Grad(WHITE, ICE, mode='radial-out'), BLACK], arms=8, speed=8, twist=0,
            size=60, thickness=12, xc=0, yc=0, bright=100)
sq.twinkle(FOREST, 3, star - 0.3, star_end, [WHITE, ICE], count=15, steps=25, bright=70)
STORY.append(('like a star burning bright', star - 0.3, star_end))
# "you are the one sent here to show me the way": the light walks the arches and the road
show, way3 = word('show', s0), word_end('way', word('show', s0))
for k in range(4):
    run_arch(k, show - 1.6 + k * 0.7, 0.9, True, GOLD)
fence_run(show, way3 - show + 0.6, 0, 100, GOLD, layer=3)
STORY.append(('sent here to show me the way', show - 1.6, way3 + 0.6))
tears = word('tears', show)
sun = word('sun', tears)
sq.meteors('Verts', 2, tears - 0.6, sun, [TEAR, ICE], direction='Down', count=12, speed=10, bright=80)
sq.moment(sun, sun + 1.6, lambda a, b: sq.shockwave('AllModels', 0, a, b, [WHITE, GOLD, PINK], cx=MID_X, cy=0,
                                                    r_end=300, w_end=100), GOLD, 30)
sq.meteors('Verts', 1, sun + 1.6, word('today', sun) + 0.5, [GOLD, WHITE], direction='Up', count=10, speed=12, bright=70)
STORY += [('all of our tears...', tears - 0.6, sun), ('...dry faster in the sun', sun, sun + 1.6)]

# ================================================================ the final chorus
s0, s1 = SPAN['final']
for phrase, color in (('on', GOLD), ('what', PINK)):
    t = word(phrase, s0)
    e = word_end('way' if phrase == 'on' else 'say', t)
    if phrase == 'on':        # "we're on our way": the light runs the road and the forest
        fence_run(t, e - t + 0.5, 0, 100, GOLD, layer=3)
        hop_sticks(t, e + 0.5, True, [Grad(GOLD, WHITE, mode='up')], n=14)
        STORY.append(("we're on our way", t, e + 0.5))
    else:                     # "that's what we say": the house sings it
        sq.on(HOUSE, 0, t, e + 0.4, PINK, 100, 20)
        for k in range(4): climb_spiral(k, t + k * 0.12, 0.9, PINK)
        STORY.append(("that's what we say", t, e + 0.4))
reason = word('reason', s0)
sq.twinkle(['Spiral Trees', ARCHES], 3, reason - 0.4, reason + 2.2, CANDY, count=40, steps=15, bright=90)
STORY.append(("there's a reason why you shine", reason - 0.4, reason + 2.2))
tears = word('tears', reason)
sun = word('sun', tears)
sq.meteors('Verts', 2, tears - 0.4, sun, [TEAR, ICE], direction='Down', count=12, speed=10, bright=80)
sq.fill('Verts', 2, sun, sun + 1.2, [Grad(PINK, GOLD, WARMWHITE, mode='up')], 0, 100, bright=85, fadeout=0.4)
sq.trunk_rise(sun, 1.2, GOLD)
STORY.append(('tears will dry faster in the sun', tears - 0.4, sun + 1.2))
last = word('shine', sun)
def last_shine(a, b):
    sq.pinwheel('AllModels', 0, a, b, [WHITE, GOLD, PINK, SKY, CYAN, LIME], arms=6, speed=10, twist=60, size=100,
                thickness=45, xc=0, clockwise=True, style3d='3D')
sq.moment(last, SPAN['end'][0], last_shine, GOLD, 60)
STORY.append(('shine your way: the whole yard', last, SPAN['end'][0]))

# ================================================================ the end: the sun stays a little longer
e0 = SPAN['end'][0]
sq.cut(q(e0), q(DUR))
sq.shockwave('AllModels', 0, e0, e0 + 1.5, [WHITE, GOLD, PINK], cx=MID_X, cy=20, r_end=300, w_end=100)
sq.on([el for el in NON_MEMBERS if el not in ('trees', 'Nativity Spot')], 0, e0, e0 + 3.0, GOLD, 100, 0)
sq.trunk_rise(e0, 3.0, GOLD)
sq.on('Verts', 1, e0 + 0.5, END + 1.5, Grad((0, WHITE), (0.3, GOLD), (0.7, PINK), (1, BLACK), mode='radial-out'), 100, 0,
      subbuf=sub(30, 20, 70, 80))
sq.on('Verts', 5, e0, END + 1.0, Grad(GOLD, SKY, mode='up'), 50, 0)
sq.on('Nativity Spot', 0, e0, END + 3.0, WARMWHITE, 100, 0)       # the last light out
STORY.append(('the sun stays a little longer', e0, END + 3.0))

# ================================================================ timing tracks
labels = {'night': 'Night (synth)', 'dawn': 'Just before the dawn', 'verse1': 'Verse 1 (drums in)', 'pre1': 'Pre-chorus',
          'chorus1': 'Shine chorus', 'synth1': 'Synth hook', 'verse2': 'Verse 2', 'pre2': 'Pre-chorus',
          'chorus2': 'Shine chorus', 'synth2': 'Synth hook', 'bridge': 'Bridge - sunrise (A# minor)',
          'day': 'Daybreak (key change to Eb)', 'final': 'Final chorus', 'end': 'End'}
st = sorted(STORY, key=lambda x: x[1])
nbars = int((END - B1) / BAR) + 1
sq.tracks = [
    ('Sections', marks([SPAN[n][0] for n, _, _ in SECTIONS], [labels[n] for n, _, _ in SECTIONS], end=DUR)),
    ('Story', [(lab, q(s), q(min(e, st[i + 1][1]) if i + 1 < len(st) else e)) for i, (lab, s, e) in enumerate(st)
               if q(min(e, st[i + 1][1]) if i + 1 < len(st) else e) > q(s)]),
    ('Lyrics', marks([s for w, s, e in WORDS], [w for w, s, e in WORDS], maxlen=1.2)),
    ('Bars', marks([B(n) for n in range(1, nbars + 1)], [str(n) for n in range(1, nbars + 1)], end=END)),
    ('Beats', marks(ev['beats'], [str((i - ev['phase']) % 4 + 1) for i in range(len(ev['beats']))], end=END)),
    ('Kick', marks(KICKS, maxlen=PER / 2)), ('Snare', marks(SNARES, maxlen=PER / 2)),
    ('Synth Notes', marks([t for t, p, d in SYNTH], [str(p) for t, p, d in SYNTH], maxlen=PER)),
    ('Vocal Notes', marks([t for t, p, d in MELODY], [str(p) for t, p, d in MELODY], maxlen=PER)),
]

sq.write(OUT, dict(song='Shine Your Way', artist='Owl City & Yuna', album='The Croods', media=media_path(SONG, 'shine.mp3'),
                   comment='Generated from stem-separated audio analysis (Demucs + Basic Pitch + Whisper): 120 BPM, '
                           'C# major -> Eb major. The whole song is one sunrise, led by a spark.'),
         DUR, timeline=ARGS[1] if len(ARGS) > 1 else None)
