"""Wizards in Winter (Trans-Siberian Orchestra) -> seqs/new/tso_wizards/tso_wizards.xsq

A sprite dances across the yard for the whole song: a white-hot spark that leaves a rainbow trail. The song is a
call and response (the band plays three bars, stops on a stab, and a piano run answers), and the timing borrows
from seqs/joy_daddyweave: the yard plays with the band, then goes dark on the stab and the sprite answers alone,
hopping Vert to Vert with each note of the piano run (rising with the pitch, direction flipping every stop).
While the band plays, the sprite dances through the props: hopping stick to stick on the eighth notes, running
over the arches and spiralling up the spiral trees, climbing the tree trunks and sprinting along the fence. In the
lead-melody parts it plays the pixel forest like a xylophone (low notes left, high notes right); in the piano
breakdown it drifts down the Verts through falling snow; in the drum drive it bounces over the arches on the snare.

Colour: jewel tones (magenta, violet, blue, cyan, emerald, red) that change by section; melodies scroll across the
Verts in a rainbow by pitch. Yard-wide moments: rainbow shockwaves on the band hits, a 6-colour whirl in the heavy
riff, snowfall in the breakdown, a spinning rainbow shader (Statis Spiraling) when the finale kicks in, and a
final burst when the sprite flies into the last hit.

usage: build.py [out.xsq] [timeline.json] [--force]
"""
import bisect, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from seqlib import *

SONG = 'new/tso_wizards'
HERE = song_dir(SONG)
ARGS = cli_args()
OUT = ARGS[0] if ARGS else str(SHOW / 'seqs' / SONG / 'tso_wizards.xsq')
ev = json.load(open(HERE / 'events.json'))
T0, PER = ev['t0'], ev['per']
BAR = 4 * PER
B1 = T0 + ev['phase'] * PER
B = lambda n: B1 + (n - 1) * BAR            # start of 1-based bar n (1.617 s at 148.4 BPM)
DUR, END = round(ev['dur'], 3), ev['end']

# ---------------------------------------------------------------- the props the sprite visits, left to right
LX = layout_x()
STICKS = sorted((m for m in LX if m.startswith('pixstk')), key=LX.get)
ARCHS = sorted((m for m in LX if m.startswith('arch-big')), key=LX.get)
SPIRALS = sorted(['Spiral Tree 2', 'Spiral Tree 3', 'little spiral - left', 'little spiral - right'], key=LX.get)
sq = Seq(ELEMENTS + STICKS + ARCHS + SPIRALS, nlayers=15)    # Verts layers 3-14 carry the melody scroll
SCROLL_LAYERS = range(3, 15)

# ---------------------------------------------------------------- colour: jewel tones, no amber
MAGENTA, VIOLET, BLUE, CYAN, EMERALD, ICE = '#FF00C8', '#8A2BFF', '#1E50FF', '#00E5FF', '#00FF80', '#BFFFFF'
PINK = '#FF4FD8'
# a 12-colour wheel for pitch classes and the sprite's trail (orange/yellow left out on purpose)
WHEEL = ['#FF0A1E', '#FF1E78', '#FF00C8', '#C800FF', '#8A2BFF', '#4B3CFF', '#1E50FF', '#0096FF', '#00E5FF',
         '#00FFB4', '#00FF50', '#9DFF3A']
pc = lambda p: WHEEL[(p * 7) % 12]          # circle of fifths: neighbouring notes get clearly different colours
RAINBOW = [RED, MAGENTA, VIOLET, BLUE, CYAN, EMERALD]
GOLD = '#FFC832'

# ---------------------------------------------------------------- notes
def mono(stem, lo, hi, minv=40, gap=0.05):
    """monophonic top line of a stem: [(start, pitch, length)]"""
    ns = [n for n in load_notes(HERE / 'midi' / f'{stem}_basic_pitch.csv') if n[3] >= minv and lo <= n[2] <= hi]
    out, cl = [], []
    for n in ns:
        if cl and n[0] - cl[0][0] > gap: out.append(max(cl, key=lambda x: x[2])); cl = []
        cl.append(n)
    if cl: out.append(max(cl, key=lambda x: x[2]))
    return [(s, p, e - s) for s, e, p, v in out]
THEME = mono('other', 60, 90)       # the strings/synth theme
LEAD = mono('vocals', 55, 90)       # the lead line in the middle sections
PIANO = mono('piano', 36, 96)       # the piano runs that answer the band

# ---------------------------------------------------------------- structure (bars)
STOPS = [4, 8, 12, 16, 17, 23, 27, 28, 30, 31, 44, 45, 51, 55, 56, 57, 78, 79, 85, 89, 90, 91]
SECTIONS = [  # name, first bar, end bar, settings
    ('intro', 1, 9, dict(dance=True, verts_bg=('bars', 'Left', [VIOLET, CYAN], 40), snare='ripple', colors=[VIOLET, CYAN],
                         spirals_bg=True)),
    ('theme1', 9, 18, dict(dance=True, scroll=THEME, verts_bg=('bars', 'Right', [MAGENTA, BLUE], 25), forest_waves=True,
                           colors=[MAGENTA, BLUE], melody=THEME)),
    ('build1', 18, 20, dict(climb=True, colors=[VIOLET, CYAN])),
    ('theme2', 20, 29, dict(dance=True, scroll=THEME, verts_bg=('swing', [CYAN, VIOLET], 35), snare='ripple',
                            forest_waves=True, colors=[CYAN, VIOLET], melody=THEME)),
    ('hit', 29, 30, {}),
    ('piano1', 30, 32, {}),
    ('whirl', 32, 36, {}),
    ('lead1', 36, 44, dict(xylophone=True, scroll=LEAD, verts_bg=('bars', 'up', [EMERALD, MAGENTA], 25),
                           colors=[EMERALD, MAGENTA], melody=LEAD, spirals_bg=False)),
    ('stops2', 44, 46, {}),
    ('build2', 46, 48, dict(climb=True, colors=[EMERALD, BLUE])),
    ('theme3', 48, 58, dict(dance=True, scroll=THEME, verts_bg=('swing', [BLUE, MAGENTA], 35), snare='ripple',
                            forest_waves=True, colors=[BLUE, MAGENTA], melody=THEME)),
    ('snow', 58, 62, {}),
    ('drive', 62, 66, dict(arch_bounce=True, verts_bg=('bars-alt', [RED, CYAN], 45), snare='ripple', bounce=True,
                           colors=[RED, CYAN])),
    ('lead2', 66, 78, dict(xylophone=True, scroll=LEAD, verts_bg=('swing', [VIOLET, EMERALD], 30), bounce=True,
                           bounce_bright=40, colors=[VIOLET, EMERALD], melody=LEAD)),
    ('stops3', 78, 80, {}),
    ('build3', 80, 82, dict(climb=True, colors=[MAGENTA, CYAN])),
    ('theme4', 82, 92, dict(dance=True, scroll=THEME, verts_bg=('bars', 'Right', [MAGENTA, CYAN], 30), snare='ripple',
                            forest_waves=True, colors=[MAGENTA, CYAN], melody=THEME)),
    ('launch', 92, 93, dict(climb=True, colors=RAINBOW)),
    ('rainbow', 93, 97, {}),
    ('finale', 97, 111, dict(dance=True, twin=True, scroll=THEME, verts_bg=('swing', RAINBOW[::2], 45), snare='ripple',
                             forest_waves=True, colors=RAINBOW, melody=THEME)),
    ('ending', 111, None, {}),
]
SEC_START = [B(a) for _, a, _, _ in SECTIONS]
def section(t):
    return SECTIONS[max(bisect.bisect_right(SEC_START, t + 0.001) - 1, 0)]
def sec_span(name):
    _, a, b, _ = next(x for x in SECTIONS if x[0] == name)
    return B(a), (B(b) if b else DUR)
is_stop = lambda t: int((t - B1 + 0.001) // BAR) + 1 in STOPS

# ---------------------------------------------------------------- drums and bass
kicks, kn = ev['kick'], 0
for i, t in enumerate(kicks):
    name, a, b, st = section(t)
    if not st.get('colors') or is_stop(t): continue
    d = max(nxt(kicks, i, 0.30), 0.075)
    c1, c2 = WHEEL[kn % 12], WHEEL[(kn + 4) % 12]
    sq.flash(ARCHES, 0, t, d, Grad(c1, c2, mode='right'), bright=60 if st.get('arch_bounce') else 100)
    sq.trunk_ring(t, max(d, 0.25), c1, tree=kn % 3)
    kn += 1

snares, sn = ev['snare'], 0
for i, t in enumerate(snares):
    name, a, b, st = section(t)
    if st.get('snare') != 'ripple' or is_stop(t): continue
    d = max(nxt(snares, i, PER), PER)
    c = st['colors'][sn % len(st['colors'])]
    sq.ripple('Verts', 0, t, d, [WHITE, c], VERT_X[pingpong(sn, 6)], 30 if sn % 2 else 70)
    sn += 1

for grp, times, vals in (('pix-evens', ev['kick'], ev['kick_v']), ('pix-odds', ev['snare'], ev['snare_v'])):
    for i, (t, v) in enumerate(zip(times, vals)):
        name, a, b, st = section(t)
        if not st.get('bounce') or is_stop(t): continue
        d = min(max(nxt(times, i, 0.45), 0.15), 0.45)
        px = round(2 + max(v - 0.35, 0) / 0.65 * 6)
        c = st['colors'][i % len(st['colors'])]
        sq.bounce(grp, 1, t, t + d, [Grad(c, WHITE, mode='up')], height=12.5 * px, bright=st.get('bounce_bright', 100))

bass = [(t, midi(nm)) for t, e, nm in ev['bass']]
bt = [t for t, _ in bass]
for i, (t, p) in enumerate(bass):
    name, a, b, st = section(t)
    if not st.get('colors') or is_stop(t): continue
    pos = 5 + (min(max(p, 28), 52) - 28) / 24 * 90
    sq.flash('fenceline', 0, t, max(nxt(bt, i, 2 * PER), 0.075), Grad(WHITE, pc(p)), bright=70,
             subbuf=sub(max(pos - 5, 0), 0, min(pos + 5, 100), 100), end_level=30)

# ---------------------------------------------------------------- melodies: rainbow sheet music on the Verts, spiral heights
scroll_notes = []
for name, a, b, st in SECTIONS:
    if not st.get('scroll'): continue
    lo, hi = (64, 88) if st['scroll'] is THEME else (60, 76)
    for t, p, d in st['scroll']:
        if B(a) <= t < (B(b) if b else DUR) and not is_stop(t):
            scroll_notes.append((t, p, min(d, PER), [WHITE, pc(p)], 90, lo, hi))
# notes glide right to left at the height of their pitch; theme and lead use their own ranges
placed = 0
for rng in ((64, 88), (60, 76)):
    placed += sq.melody_scroll('Verts', [n[:5] for n in scroll_notes if n[5:] == rng], None, travel=BAR,
                               lo=rng[0], hi=rng[1], layers=SCROLL_LAYERS)
print(f'melody scroll: {placed} of {len(scroll_notes)} notes placed')

for name, a, b, st in SECTIONS:
    mel = st.get('melody')
    if not mel: continue
    lo, hi = (64, 88) if mel is THEME else (60, 76)
    ts = [n for n in mel if B(a) <= n[0] < B(b) and not is_stop(n[0])]
    for i, (t, p, d) in enumerate(ts):
        g = min(ts[i + 1][0] - t, 2 * PER) if i + 1 < len(ts) else min(d, 2 * PER)
        h = 15 + (min(max(p, lo), hi) - lo) / (hi - lo) * 85
        sq.on('Spiral Trees', 1, t, t + max(g, 0.075), Grad(pc(p), WHITE, mode='up'), 100, 60,
              subbuf=sub(0, 0, 100, h), perModel=True)

# ---------------------------------------------------------------- per-section backgrounds
for name, a, b, st in SECTIONS:
    s0, s1 = B(a), (B(b) if b else DUR)
    cols = st.get('colors')
    vb = st.get('verts_bg')
    if vb and vb[0] == 'bars':          # colour bands rolling across the canvas
        _, direction, cs, br = vb
        sq.bars('Verts', 2, s0, s1, direction, [Grad(*cs, mode='up'), BLACK, Grad(*cs[::-1], mode='up'), BLACK], 4,
                (s1 - s0) / (2 * BAR), br)
    elif vb and vb[0] == 'bars-alt':    # bands change direction every bar
        _, cs, br = vb
        for k in range(b - a):
            sq.bars('Verts', 2, B(a + k), B(a + k + 1), 'Left' if k % 2 else 'Right',
                    [Grad(cs[k % 2], WHITE, mode='up'), BLACK], 2, 1, br)
    elif vb and vb[0] == 'swing':       # a 3D spiral rocking back and forth (DreamsOfFireflies)
        _, cs, br = vb
        sq.spirals('Verts', 2, s0, s1, cs, count=len(cs), thickness=50, movement=1.0, bright=br, three_d=True, swing=True)
    if st.get('forest_waves'):          # sine waves rolling across the pixel sticks, a new colour each bar
        for k in range(b - a):
            t = B(a + k)
            if is_stop(t): continue
            sq.wave(FOREST[k % 2], 2, t, t + 2 * PER, None, 50, waves=900, speed=10, kind='Sine', fill='None',
                    thickness=50, height=50, direction='Right to Left' if k % 2 == 0 else 'Left to Right',
                    colors=[WHITE, cols[k % len(cols)]])
    if cols and not st.get('climb'):
        # trunks wear barber-pole stripes in the section's colours
        sq.spirals('trees', 2, s0, s1, [cols[0], cols[1 % len(cols)]], count=2, rotation=20, thickness=40,
                   movement=2.0, bright=50, perModel=True)
        if st.get('spirals_bg', not st.get('melody')):
            sq.spirals('Spiral Trees', 2, s0, s1, cols, count=len(cols), rotation=30, thickness=45, movement=2.0,
                       bright=45, perModel=True)
        # the house and the floods breathe in and out every two beats (joy_daddyweave's big lights)
        for k in range(int((s1 - s0) / (2 * PER))):
            t = s0 + k * 2 * PER
            if is_stop(t): continue
            c = cols[(k // 2) % len(cols)]
            sq.on(HOUSE + FLOODS, 1, t, t + 2 * PER, c, 15 if k % 2 == 0 else 80, 80 if k % 2 == 0 else 15, blend=None)
    if st.get('climb'):                 # the Verts and trunks fill with rainbow light into the next section
        sq.fill('Verts', 1, s0, s1, [Grad(*cols, mode='up')], 0, 100)
        sq.fill('trees', 1, s0, s1, [Grad(*cols, mode='up')], 0, 100, per_model=True)
        sq.on(HOUSE + FLOODS, 1, s0, s1, Grad(*cols, mode='right'), 10, 100, blend=None)
        sq.twinkle(FOREST, 2, s0, s1, cols, count=20, steps=20, bright=60)

# ---------------------------------------------------------------- AllModels moments (everything underneath is cleared)
h0, h1 = sec_span('hit')
hit_kicks = [t for t in kicks if h0 - 0.05 <= t < h1 - 0.1]
def draw_hit(a, b):     # each band hit sends a rainbow ring across the yard from alternating sides
    for j, t in enumerate(hit_kicks):
        sq.shockwave('AllModels', j % 3, t, min(t + 0.9, b), [WHITE, RAINBOW[(j * 2) % 6]], cx=[20, 80, 50][j % 3],
                     cy=30, r_end=300, w_end=70)
sq.moment(h0, h1, draw_hit, MAGENTA)

w0, w1 = sec_span('whirl')              # the heavy riff: a six-colour wizard's wheel over the whole yard
sq.moment(w0, w1, lambda a, b: sq.whirl('AllModels', 0, a, b, RAINBOW, xc=0), VIOLET, 30, fade_from=80)

s0_, s1_ = sec_span('snow')             # piano breakdown: snow falls on the whole yard
def draw_snow(a, b):
    sq.meteors('AllModels', 0, a, b, [WHITE, ICE, '#9FD8FF'], direction='Down', count=8, speed=6, bright=55)
    sq.twinkle('AllModels', 1, a, b, [ICE, WHITE], count=6, steps=40, bright=50)
sq.moment(s0_, s1_, draw_snow, ICE, 10, fade_from=30)

r0, r1 = sec_span('rainbow')            # the finale kicks in: a spinning rainbow over everything
sq.moment(r0, r1, lambda a, b: sq.shader('AllModels', 0, a, b, 'Shaders/Statis Spiraling.fs',
                                         params=dict(rate=1.2, loops=16), bools=dict(mirror=1, rotate=1, offset=1, noise=0),
                                         fadein=0.15, fadeout=0.8), MAGENTA, 40)

# ending: rainbow rings on the hammer hits, a breath of silence, then the last hit
HAMMER = [t for t in ev['kick'] + ev['snare'] if 174.0 <= t < 179.0]
HAMMER = sorted({q(t): t for t in HAMMER}.values())
LAST = next(t for t in kicks if t > 181.0)
sq.cut(q(HAMMER[0] - 0.05), q(DUR))     # the hammer hits land before bar 111: the finale stops for them
for j, t in enumerate(HAMMER):
    sq.shockwave('AllModels', j % 3, t, t + 0.8, [WHITE, RAINBOW[j % 6]], cx=20 if j % 2 == 0 else 80, cy=30,
                 r_end=300, w_end=70)
    sq.on([el for el in NON_MEMBERS if el != 'trees'], 0, t, t + 0.6, RAINBOW[j % 6], 100, 0)
    sq.trunk_rise(t, 0.6, RAINBOW[j % 6])
sq.shockwave('AllModels', 0, LAST, LAST + 1.6, [WHITE, MAGENTA, CYAN], cx=50, cy=50, r_end=400, w_end=120)
sq.shader('AllModels', 1, LAST, DUR, 'Shaders/Statis Spiraling.fs', params=dict(rate=0.6, loops=16),
          bools=dict(mirror=1, rotate=1, offset=1, noise=0), bright=80, fadeout=DUR - LAST - 0.5)
sq.on([el for el in NON_MEMBERS if el not in ('trees', 'Nativity Spot')], 0, LAST, LAST + 2.5, WHITE, 100, 0)
sq.trunk_rise(LAST, 2.5, MAGENTA)
sq.on('Nativity Spot', 0, LAST, DUR, ICE, 100, 0)       # the last light out

# ---------------------------------------------------------------- the stops: stab, darkness, the sprite answers
SPRITE_TRACK = []
trail_n = [0]
def trail():
    """the next colour of the sprite's rainbow trail"""
    trail_n[0] += 1
    return WHEEL[trail_n[0] % 12]

def vert_glow(k, y, t, dur, c, layer):
    """the sprite resting on Vert k at height y: a small spark the width of the panel, fading"""
    vx = VERT_X[k]
    sq.on('Verts', layer, t, t + dur, Grad(WHITE, c, mode='radial-out'), 100, 0, subbuf=sub(max(vx - 8, 0), max(y - 4, 0),
                                                                                         min(vx + 8, 100), min(y + 4, 100)))

def vert_path(points, end, layer0=0):
    """the sprite flies through (t, Vert k, height y) points on the Verts canvas: streaks between panels, glides
    within one, and a fading spark wherever it lands"""
    for i, (t, k, y) in enumerate(points):
        t2, k2, y2 = points[i + 1] if i + 1 < len(points) else (end, k, min(y + 30, 100))
        c = trail()
        if k2 != k:
            x1, x2 = VERT_X[k], VERT_X[k2]
            sq.morph('Verts', layer0, t, t2, [WHITE, c], (x1, y - 3, x1, y + 3), (x2, y2 - 3, x2, y2 + 3),
                     tail_start=1, tail_end=35, sparkles=40)
        else:
            vx = VERT_X[k]
            sq.morph('Verts', layer0, t, t2, [WHITE, c], (0, y, 100, y), (0, y2, 100, y2), tail_start=1, tail_end=40,
                     sparkles=40, extra={'B_CUSTOM_SubBuffer': sub(max(vx - 8, 0), 0, min(vx + 8, 100), 100)})
        vert_glow(k, y, t, min(0.5, max(t2 - t, 0.25) * 1.5), c, layer0 + 1 + i % 2)

for si, bar in enumerate(STOPS):
    a, b = B(bar), B(bar + 1)
    sq.cut(q(a - 0.03), q(b))
    stab = next((t for t in kicks if a - 0.08 <= t < a + 0.25), None)
    c = WHEEL[(si * 5) % 12]
    if stab is not None:        # the stab: a ring across the yard, the trunks and the house answer, then dark
        sq.shockwave('AllModels', 2, stab, stab + 0.6, [WHITE, c], cx=50, cy=30, r_end=300, w_end=80)
        sq.trunk_ring(stab, 0.5, c)
        sq.on(HOUSE + FLOODS, 0, stab, stab + 0.5, c, 100, 0)
    run = [n for n in PIANO if a + 0.2 * PER <= n[0] < b - 0.1 * PER]
    if not run: run = [(a + j * PER, 60 + 3 * j, PER) for j in range(1, 4)]
    rightward = si % 2 == 0
    n = len(run)
    ps = [p for _, p, _ in run]
    pl, ph = min(ps), max(ps)
    pts = []
    for j, (t, p, d) in enumerate(run):
        k = round(j * 5 / max(n - 1, 1)) if n > 1 else 2
        y = 50 if ph == pl else 12 + (p - pl) / (ph - pl) * 72
        pts.append((t, k if rightward else 5 - k, y))
    if stab is not None: pts.insert(0, (stab + 0.05, pts[0][1], 8))       # it wakes at the foot of the first Vert
    vert_path(pts, b - 0.02)
    SPRITE_TRACK.append((f'stop {bar}: Verts run {"->" if rightward else "<-"}', a, b))

# ---------------------------------------------------------------- the sprite while the band plays
def hop_sticks(t0, t1, rightward, step, layer=0):
    """hop stick to stick on every `step`, crossing the whole pixel forest between t0 and t1"""
    n = max(int(round((t1 - t0) / step)), 1)
    off = (trail_n[0] * 0.37) % 1          # a different handful of sticks is skipped each crossing
    for j in range(n):
        i = min(int((j + off) * len(STICKS) / n), len(STICKS) - 1)
        t = t0 + j * step
        sq.bounce(STICKS[i if rightward else len(STICKS) - 1 - i], layer, t, t + min(2 * step, 0.4),
                  [Grad(trail(), WHITE, mode='up')], 100)

def run_arch(k, t, dur, rightward):
    a, b = (0, 0, 0, 100), (100, 0, 100, 100)
    sq.morph(ARCHS[k], 0, t, t + dur, [WHITE, trail()], *((a, b) if rightward else (b, a)), tail_start=5, tail_end=45,
             sparkles=40)

def climb_spiral(k, t, dur, down=False):
    sq.morph(SPIRALS[k], 0, t, t + dur, [WHITE, trail()], *DIAG['down' if down else 'up'], tail_start=5, tail_end=50,
             sparkles=40)

def climb_trunk(k, t, dur):
    sq.trunk_ring(t, dur, trail(), tree=k, layer=3)

def sprint_fence(t, dur, rightward):
    a, b = (0, 0, 0, 100), (100, 0, 100, 100)
    sq.morph('fenceline', 3, t, t + dur, [WHITE, trail()], *((a, b) if rightward else (b, a)), tail_start=2,
             tail_end=25, sparkles=40)

def dance(t0, t1, mode, rightward):
    nb = max(int(round((t1 - t0) / BAR)), 1)
    if mode == 'forest':
        hop_sticks(t0, t1, rightward, PER / 2)
    elif mode == 'arches':      # over the arches two beats each, then up the spiral trees on the beats
        order = list(range(4)) if rightward else list(range(3, -1, -1))
        for j in range(2 * (nb - 1)):
            run_arch(order[j % 4], t0 + j * 2 * PER, 2 * PER, rightward)
        for j in range(4):
            climb_spiral(order[j], t0 + (nb - 1) * BAR + j * PER, PER)
    elif mode == 'fence':       # up the three trunks, then sprints along the fence, back and forth
        trunks = [0, 1, 2] if rightward else [2, 1, 0]
        tb = t0 if rightward else t1 - BAR
        for j, k in enumerate(trunks):
            climb_trunk(k, tb + j * BAR / 3, BAR / 3)
        fs = t0 + BAR if rightward else t0
        for j in range(nb - 1):
            sprint_fence(fs + j * BAR, BAR, rightward == (j % 2 == 0))

MODES = ['forest', 'arches', 'forest', 'fence']
ph_n = 0
for name, a, b, st in SECTIONS:
    if st.get('dance'):
        # phrases are the runs of bars between stops; long stretches are cut into three-bar phrases
        bars = [x for x in range(a, b) if x not in STOPS]
        runs, cur = [], []
        for x in bars:
            if cur and (x != cur[-1] + 1 or len(cur) == 3): runs.append(cur); cur = []
            cur.append(x)
        if cur: runs.append(cur)
        for r in runs:
            mode, rightward = MODES[ph_n % 4], ph_n % 2 == 0
            if len(r) < 2 and mode != 'forest': mode = 'forest'
            dance(B(r[0]), B(r[-1] + 1), mode, rightward)
            if st.get('twin'):      # in the finale a second sprite crosses the forest the other way
                hop_sticks(B(r[0]), B(r[-1] + 1), not rightward, PER / 2, layer=1)
            SPRITE_TRACK.append((f'{mode} {"->" if rightward else "<-"}' + (' + twin' if st.get('twin') else ''),
                                 B(r[0]), B(r[-1] + 1)))
            ph_n += 1
    if st.get('climb'):         # winding up: around the spiral trees, faster in the last bar
        t, j = B(a), 0
        while t < B(b) - 0.05:
            step = PER if t < B(b) - BAR - 0.01 else PER / 2
            climb_spiral(j % 4, t, step * 1.5)
            t += step; j += 1
        SPRITE_TRACK.append(('winding up the spirals', B(a), B(b)))
    if st.get('xylophone'):     # the lead melody: the sprite plays the pixel forest, low notes left, high right
        ts = [n for n in LEAD if B(a) <= n[0] < B(b) and not is_stop(n[0])]
        keys = sorted({p for _, p, _ in ts})
        for j, (t, p, d) in enumerate(ts):
            # each pitch owns a stretch of the forest; repeated notes step around inside it
            i = keys.index(p) / max(len(keys) - 1, 1) * (len(STICKS) - 1) + [0, 2, -2, 1, -1][j % 5]
            i = min(max(round(i), 0), len(STICKS) - 1)
            sq.bounce(STICKS[i], 0, t, t + min(max(d, 0.25), 0.6), [Grad(pc(p), WHITE, mode='up')], 100)
        SPRITE_TRACK.append(('xylophone on the forest', B(a), B(b)))
    if st.get('arch_bounce'):   # the drum drive: over an arch on every snare, back and forth across the yard
        ts = [t for t in snares if B(a) <= t < B(b)]
        for j, t in enumerate(ts):
            k = pingpong(j, 4)
            rightward = pingpong(j + 1, 4) > k
            run_arch(k, t, min(nxt(ts, j, 0.5), 0.5), rightward)
        SPRITE_TRACK.append(('bouncing over the arches', B(a), B(b)))

# the hammer hits at the end belong to the whole yard: the dancing stops there
sq.cut(q(HAMMER[0] - 0.05), q(DUR), STICKS + ARCHS + SPIRALS)
sq.cut(q(HAMMER[0] - 0.05), q(DUR), ['trees', 'fenceline'], layers=[3])

# piano breakdown: the sprite drifts down the Verts through the snow, right to left, one note at a time
s0_, s1_ = sec_span('snow')
notes = [n for n in PIANO if s0_ <= n[0] < s1_]
pts = [(t, round(5 - j * 5 / max(len(notes) - 1, 1)), 10 + (min(max(p, 47), 90) - 47) / 43 * 80)
       for j, (t, p, d) in enumerate(notes)]
vert_path(pts, s1_ - 0.05)
SPRITE_TRACK.append(('drifting down through the snow', s0_, s1_))

# the silence before the last hit: the sprite gathers itself in the middle of the wall and flies up into it
quiet0 = max(HAMMER) + 0.4
pts = [(quiet0, 2, 10), (quiet0 + 0.6, 3, 25), (quiet0 + 1.2, 2, 40), (quiet0 + 1.7, 3, 55), (quiet0 + 2.1, 2, 70),
       (LAST - 0.25, 3, 85)]
vert_path(pts, LAST)
SPRITE_TRACK.append(('gathering... into the last hit', quiet0, LAST))
vert_glow(2, 92, LAST + 2.0, DUR - LAST - 2.0, ICE, 0)                  # one last spark, fading with the song

# ---------------------------------------------------------------- timing tracks
labels = {'intro': 'Intro riff', 'theme1': 'Theme', 'build1': 'Build', 'theme2': 'Theme (high)', 'hit': 'Band hits',
          'piano1': 'Piano', 'whirl': 'Heavy riff - whirl', 'lead1': 'Lead melody', 'stops2': 'Stops',
          'build2': 'Build', 'theme3': 'Theme', 'snow': 'Piano breakdown - snow', 'drive': 'Drum drive',
          'lead2': 'Lead melody', 'stops3': 'Stops', 'build3': 'Build', 'theme4': 'Theme', 'launch': 'Launch',
          'rainbow': 'Finale - rainbow', 'finale': 'Finale', 'ending': 'Ending'}
nbars = int((END - B1) / BAR) + 1
sp = sorted(SPRITE_TRACK, key=lambda x: x[1])
sq.tracks = [
    ('Sections', marks([B(a) if a > 1 else 0.0 for _, a, _, _ in SECTIONS], [labels[n] for n, _, _, _ in SECTIONS],
                       end=DUR)),
    ('Sprite', [(lab, q(s), q(min(e, sp[i + 1][1]) if i + 1 < len(sp) else e)) for i, (lab, s, e) in enumerate(sp)]),
    ('Stops (call & response)', marks([B(x) for x in STOPS], [f'stop {x}' for x in STOPS], maxlen=BAR)),
    ('Bars', marks([B(k + 1) for k in range(nbars)], [str(k + 1) for k in range(nbars)], end=END)),
    ('Beats', marks(ev['beats'], [str((i - ev['phase']) % 4 + 1) for i in range(len(ev['beats']))], end=END)),
    ('Kick', marks(ev['kick'], maxlen=PER / 2)), ('Snare', marks(ev['snare'], maxlen=PER / 2)),
    ('Theme Notes', marks([t for t, p, d in THEME], [f'{p}' for t, p, d in THEME], maxlen=PER)),
    ('Lead Notes', marks([t for t, p, d in LEAD], [f'{p}' for t, p, d in LEAD], maxlen=PER)),
    ('Piano Notes', marks([t for t, p, d in PIANO], [f'{p}' for t, p, d in PIANO], maxlen=PER)),
]

sq.write(OUT, dict(song='Wizards in Winter', artist='Trans-Siberian Orchestra', album='',
                   media=media_path(SONG, 'wis.mp3'),
                   comment='Generated from stem-separated audio analysis (Demucs + Basic Pitch): 148.4 BPM. '
                           'A sprite dances across the yard; it answers the band alone in every stop bar.'),
         DUR, timeline=ARGS[1] if len(ARGS) > 1 else None)
