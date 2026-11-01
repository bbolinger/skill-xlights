"""Joy to the World (Big Daddy Weave) -> seqs/bdw_joy/bdw_joy.xsq

The song is an announcement - "go tell the world, tell everyone" - so the yard spells it out and carries the news.

- The words: the middle four Verts are vertical marquee signs. As each chorus line is sung, its words light up one
  per panel, stacked letter over letter in a 6x7 pixel font: JOY / TO / THE / WORLD, then THE / LORD / IS / COME,
  JOY TO THE WORLD / GOD SENT HIS SON, GO / TELL / THE / WORLD, TELL / EVERY / ONE. The two outer Verts twinkle like
  stars on either side of the sign.
- The manger (the Nativity Spot) is where the news comes from: every "the Lord is come" sends a ring out from it
  across the yard; "God sent His Son" brings a star down out of the sky to the manger; "go, tell the world, tell the
  world, tell everyone" sends heralds running out from the manger along the fence, over the arches, through the
  pixel sticks, and on "everyone" the whole yard lights.
- "He shall reign forever": crowns. Every time it's sung a gold pixel-art crown sits on every Vert. In the chanting
  bridge ("He shall reign forever and ever") the crowns climb a little higher each bar while the wall fills with
  gold, until the band hits "JOY to the world" - then JOY is spelled on all six panels in rainbow colours.
- Verse 1 tells the scene: "rejoice, rejoice" (bursts of sparkle), "our King is here" (a crown), "men of earth"
  (the fence glows green, left to right) "and angels cheer" (white light drifting down), "glory right before our
  eyes" (gold rays from the manger), "majesty in a manger's light" (everything falls quiet but the manger).
- Verse 2 is call and response: "see the shepherds bowing down" (the pixel sticks light and bow, one after another,
  toward the manger), "wise men offer Him their crown" (a crown carried panel to panel toward the manger), "then till
  now and far beyond" (a light runs the whole fence and off the end), "the endless song" (everything turns) - and
  every "He shall reign forever" answer is the crowns.
- The drums-and-voice breakdown: the yard goes dark and only the drums light it - every kick a ring from the manger,
  every clap the whole crowd of sticks. The final choruses add rainbow colour; at the end everything gathers back
  into the manger, which is the last light out.
- Christmas colours (red, green, white, gold for crowns and glory), rainbow only for the JOY climax and the finale.
  D major all the way.

usage: build.py [out.xsq] [timeline.json] [--force]
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from seqlib import *

SONG = 'bdw_joy'
HERE = song_dir(SONG)
ARGS = cli_args()
OUT = ARGS[0] if ARGS else str(SHOW / 'seqs' / SONG / 'bdw_joy.xsq')
ev = json.load(open(HERE / 'events.json'))
T0, PER = ev['t0'], ev['per']
BAR = 4 * PER
B1 = T0 + ev['phase'] * PER
B = lambda n: B1 + (n - 1) * BAR            # start of 1-based bar n (2.527 s at 95 BPM)
BEATS = ev['beats']
DUR, END = round(ev['dur'], 3), ev['end']

# ---------------------------------------------------------------- the props
LX = layout_x()
STICKS = sorted((m for m in LX if m.startswith('pixstk')), key=LX.get)
ARCHS = sorted((m for m in LX if m.startswith('arch-big')), key=LX.get)
SPIRALS = sorted(['Spiral Tree 2', 'Spiral Tree 3', 'little spiral - left', 'little spiral - right'], key=LX.get)
VERTS_M = sorted((m for m in LX if m.startswith('Vert-')), key=LX.get)
sq = Seq(ELEMENTS + STICKS + ARCHS + SPIRALS + VERTS_M, nlayers=34)
# single Verts: 0-27 letters, 28-31 the crown, 32 stars on the outer panels
# Verts group: 0 the herald/star, 1 angels / gold fill, 2 stars, 3 sweeps, 4 background
_x = [LX[m] for m in ARCHS + STICKS + SPIRALS + VERTS_M]
ALLX = lambda x: (x - min(_x)) / (max(_x) - min(_x)) * 100
MANGER = ALLX(LX['Nativity Spot'])
FENCE_MANGER = (LX['Nativity Spot'] - LX['fenceline']) / 2825 * 100
NAT = 'Nativity Spot'

# ---------------------------------------------------------------- colour
RED, GREEN, GOLD, WARM = '#FF0A1E', '#00E040', '#FFC832', '#FFE6C8'
NIGHT, ROYAL, SKY = '#0A0A50', '#3C28C8', '#3CA0FF'
RAINBOW = [RED, '#FF00C8', '#8A2BFF', SKY, '#00E5FF', GREEN]
# vivid on pixels: blend each colour toward a neighbour of the same family, never toward white (pastel) and never
# red straight into green (the middle of that blend is olive brown)
PARTNER = {RED: '#FF2878', GREEN: '#00FFA0', GOLD: '#FFE650', '#FF00C8': '#FF2878', '#8A2BFF': '#C83CFF',
           SKY: '#1E50FF', '#00E5FF': '#00FFC8', ROYAL: '#1E50FF'}
rich = lambda c, mode='up': Grad(c, PARTNER.get(c, c), mode=mode)

# ---------------------------------------------------------------- words and notes
WORDS = [(w['word'].strip(' ,.?!').lower(), w['start'], w['end'])
         for w in json.load(open(HERE / 'lyrics.json')) if w['start'] < END]
def word(prefix, after, before=1e9):
    return next(s for w, s, e in WORDS if w.startswith(prefix) and after <= s < before)
VOX = [n for n in load_notes(HERE / 'midi' / 'vocals_basic_pitch.csv') if n[3] >= 40 and n[0] < END]
def sung(t, back=0.4):
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
KICKS, SNARES = ev['kick'], ev['snare']
BASS = [(t, midi(nm)) for t, e, nm in ev['bass']]

# ---------------------------------------------------------------- structure (bars of 2.527 s)
SECTIONS = [('intro', 1, 10), ('verse1', 10, 18), ('chorus1', 18, 27), ('hush', 27, 28), ('verse2', 28, 36),
            ('chorus2', 36, 45), ('bridge', 45, 48), ('chant', 48, 54), ('joy', 54, 57), ('drums', 57, 60),
            ('final', 60, 77), ('end', 77, None)]
SPAN = {n: (B(a) if a > 1 else 0.0, B(b) if b else DUR) for n, a, b in SECTIONS}
section = lambda t: next((n for n, (a, b) in SPAN.items() if a <= t < b), 'end')
kind = lambda t: section(t).rstrip('0123456789')
BAND = ('intro', 'chorus', 'verse', 'chant', 'joy', 'final')
STORY = []

# ---------------------------------------------------------------- the pixel font (6 wide x 7 tall, bold)
FONT = {
    'J': ['..####', '....##', '....##', '....##', '##..##', '##..##', '.####.'],
    'O': ['.####.', '##..##', '##..##', '##..##', '##..##', '##..##', '.####.'],
    'Y': ['##..##', '##..##', '.####.', '..##..', '..##..', '..##..', '..##..'],
    'T': ['######', '######', '..##..', '..##..', '..##..', '..##..', '..##..'],
    'H': ['##..##', '##..##', '##..##', '######', '##..##', '##..##', '##..##'],
    'E': ['######', '##....', '##....', '#####.', '##....', '##....', '######'],
    'W': ['#....#', '#....#', '#....#', '#.##.#', '#.##.#', '######', '##..##'],
    'R': ['#####.', '##..##', '##..##', '#####.', '##.##.', '##..##', '##..##'],
    'L': ['##....', '##....', '##....', '##....', '##....', '##....', '######'],
    'D': ['#####.', '##..##', '##..##', '##..##', '##..##', '##..##', '#####.'],
    'I': ['######', '..##..', '..##..', '..##..', '..##..', '..##..', '######'],
    'S': ['.#####', '##....', '##....', '.####.', '....##', '....##', '#####.'],
    'C': ['.#####', '##....', '##....', '##....', '##....', '##....', '.#####'],
    'M': ['#....#', '##..##', '######', '#.##.#', '#....#', '#....#', '#....#'],
    'G': ['.#####', '##....', '##....', '##.###', '##..##', '##..##', '.####.'],
    'N': ['#....#', '##...#', '###..#', '#.##.#', '#..###', '#...##', '#....#'],
    'V': ['##..##', '##..##', '##..##', '##..##', '##..##', '.####.', '..##..'],
}
CROWN = ['#.##.#', '######', '######']
LETTER_H, GAP = 7, 2

def rects(bitmap):
    """a bitmap (rows top to bottom) as rectangles (c1, c2, r_top1, r_top2): runs in each row, merged downward
    while the run repeats in the next row"""
    open_, out = {}, []
    for r, row in enumerate(bitmap + ['.' * 6]):
        runs, c = set(), 0
        while c < 6:
            if row[c] == '#':
                c2 = c
                while c2 + 1 < 6 and row[c2 + 1] == '#': c2 += 1
                runs.add((c, c2)); c = c2 + 1
            else:
                c += 1
        for run in list(open_):
            if run not in runs: out.append((*run, open_.pop(run), r - 1))
        for run in runs:
            open_.setdefault(run, r)
    return out

def cell(c1, c2, row_lo, row_hi):
    """subbuffer for columns c1..c2 and rows row_lo..row_hi (of 44, 0 = bottom) on a single 6x44 Vert, edges just
    below pixel boundaries"""
    return sub(c1 * 100 / 6 - 0.01, row_lo * 100 / 44 - 0.01, (c2 + 1) * 100 / 6 - 0.01, (row_hi + 1) * 100 / 44 - 0.01)

def draw(k, bitmaps, t0, t1, colors, layer0=0, top=None, fade=0.25):
    """draw bitmaps (letters) stacked top to bottom on Vert k, centred unless `top` (row of the top edge) is given"""
    n = len(bitmaps)
    total = sum(len(b) for b in bitmaps) + GAP * (n - 1)
    top = top if top is not None else (44 + total) // 2 - 1
    L = layer0
    for i, bm in enumerate(bitmaps):
        c = colors[i % len(colors)]
        for c1, c2, r1, r2 in rects(bm):
            lo, hi = top - r2, top - r1
            sb = cell(c1, c2, lo, hi)
            if t1 - fade > t0 + 0.05:
                sq.on(VERTS_M[k], L, t0, t1 - fade, c, 100, 100, subbuf=sb)
                sq.on(VERTS_M[k], L, t1 - fade, t1, c, 100, 0, subbuf=sb)
            else:
                sq.on(VERTS_M[k], L, t0, t1, c, 100, 0, subbuf=sb)
            L += 1
        top -= len(bm) + GAP
    return L

def spell(k, text, t0, t1, colors):
    draw(k, [FONT[ch] for ch in text], t0, t1, colors)

def crowns(t0, t1, top=None, ks=range(6), color=GOLD):
    for k in ks:
        draw(k, [CROWN], t0, t1, [color], layer0=28, top=top, fade=0.4)

# ---------------------------------------------------------------- helpers
def breathe(s0, s1, cols_, lo=30, hi=100, els=HOUSE + ['grinch-1'], layer=1):
    k, t = 0, s0
    while t < s1 - 0.05:
        e = min(t + BAR, s1)
        sq.on(els, layer, t, e, cols_[(k // 2) % len(cols_)], lo if k % 2 == 0 else hi, hi if k % 2 == 0 else lo,
              blend=None)
        t, k = e, k + 1

def manger_ring(t, cols=(WHITE, GOLD), big=True, layer=1):
    sq.shockwave('AllModels', layer, t, t + 1.5, list(cols), cx=round(MANGER), cy=15, r_end=300 if big else 150,
                 w_end=45)
    sq.flash(NAT, 0, t, 1.3, WHITE, end_level=70)

def fence_run(t, dur, x0, x1, color, layer=3):
    sq.morph('fenceline', layer, t, t + dur, [WHITE, color], (x0, 0, x0, 100), (x1, 0, x1, 100), tail_start=2,
             tail_end=30, sparkles=30)

def run_arch(k, t, dur, rightward, color):
    a, b = (0, 0, 0, 100), (100, 0, 100, 100)
    sq.morph(ARCHS[k], 0, t, t + dur, [WHITE, color], *((a, b) if rightward else (b, a)), tail_start=5, tail_end=45,
             sparkles=30)

def climb_spiral(k, t, dur, color):
    sq.morph(SPIRALS[k], 0, t, t + dur, [WHITE, color], *DIAG['up'], tail_start=5, tail_end=50, sparkles=30)

def hop_sticks(t0, t1, order, colors):
    step = (t1 - t0) / len(order)
    for j, i in enumerate(order):
        sq.bounce(STICKS[i], 0, t0 + j * step, t0 + j * step + max(2.5 * step, 0.25), colors, 100)

# ================================================================ the manger glows all song
sq.on(NAT, 1, 0.0, END + 2.5, WARM, 35, 35)

# ================================================================ instruments
for i, t in enumerate(KICKS):
    k = kind(t)
    if k not in BAND: continue
    d = min(max(nxt(KICKS, i, 0.3), 0.1), 0.3)
    c = RAINBOW[i % 6] if section(t) == 'final' else (RED if i % 2 else GREEN)
    sq.flash(ARCHES, 0, t, d, rich(c, 'right'), bright=85 if k == 'verse' else 100)

sn = 0
for i, t in enumerate(SNARES):
    k = kind(t)
    if k not in BAND: continue
    if i + 1 < len(SNARES) and SNARES[i + 1] - t < PER * 0.6: continue          # claps and ghost notes
    sq.trunk_ring(t, 0.45, RAINBOW[sn % 6] if section(t) == 'final' else [RED, GREEN, RED, GREEN, GOLD][sn % 5], tree=sn % 3)
    sn += 1

bt = [t for t, _ in BASS]
for i, (t, p) in enumerate(BASS):
    if kind(t) not in BAND: continue
    pos = 5 + (min(max(p, 30), 54) - 30) / 24 * 90
    sq.flash('fenceline', 0, t, max(nxt(bt, i, 2 * PER), 0.075), rich([RED, GREEN][p % 2], 'right'), bright=95,
             subbuf=sub(max(pos - 4, 0), 0, min(pos + 4, 100), 100), end_level=25)

for i, (t, p, d) in enumerate(MELODY):
    g = min(MELODY[i + 1][0] - t, 2 * PER) if i + 1 < len(MELODY) else min(d, 2 * PER)
    h = 15 + (min(max(p, 57), 79) - 57) / 22 * 85
    c = RAINBOW[i % 6] if section(t) in ('joy', 'final') else [RED, GREEN][i % 2]
    sq.on('Spiral Trees', 1, t, t + max(g, 0.075), rich(c), 100, 70, subbuf=sub(0, 0, 100, h),
          perModel=True)

# the pixel sticks bounce with the drums in the choruses
kv, sv = dict(zip(KICKS, ev['kick_v'])), dict(zip(SNARES, ev['snare_v']))
for grp, hits, vals in (('pix-evens', KICKS, kv), ('pix-odds', SNARES, sv)):
    for j, t in enumerate(hits):
        if kind(t) not in ('chorus', 'joy', 'final', 'intro'): continue
        if grp == 'pix-odds' and j + 1 < len(hits) and hits[j + 1] - t < PER * 0.6: continue
        d = min(max(nxt(hits, j, 0.4), 0.15), 0.4)
        c = RAINBOW[j % 6] if section(t) in ('joy', 'final') else [RED, GREEN][j % 2]
        sq.bounce(grp, 1, t, t + d, [rich(c)], height=40 + 60 * min(max(vals[t] - 0.35, 0) / 0.6, 1))

# ================================================================ backgrounds
for name, (s0, s1) in SPAN.items():
    k = kind(s0)
    if k in ('intro', 'chorus', 'final'):
        cs = [RED, GREEN] if k != 'final' else RAINBOW[::2]
        # the sign hangs on a deep blue night sky: saturated, and the red/green/gold letters stand out against it
        sq.spirals('Verts', 4, s0, s1, [ROYAL, SKY, '#8A2BFF'] if k != 'final' else RAINBOW[2:5], count=3,
                   thickness=50, movement=1.0, bright=40, three_d=True, swing=True)
        sq.spirals('trees', 1, s0, s1, [RED, WHITE] if k != 'final' else [RED, WHITE, GREEN], count=2, rotation=25,
                   thickness=40, movement=2.0, bright=80, perModel=True)          # candy-cane trunks
        breathe(s0, s1, [RED, GREEN] if k != 'final' else RAINBOW)
        sq.twinkle(VERTS_M[0], 32, s0, s1, [GOLD, RED, GREEN], count=35, steps=20, bright=100)  # stars beside the sign
        sq.twinkle(VERTS_M[5], 32, s0, s1, [GOLD, GREEN, RED], count=35, steps=20, bright=100)
        if k != 'intro':
            j = 0
            while s0 + j * BAR < s1 - 0.1:
                t = s0 + j * BAR
                sq.wave(FOREST[j % 2], 2, t, min(t + 2 * PER, s1), None, 75, waves=900, speed=10, kind='Sine',
                        fill='None', thickness=50, height=50, direction='Right to Left' if j % 2 else 'Left to Right',
                        colors=[cs[j % len(cs)], PARTNER.get(cs[j % len(cs)], WHITE)])
                j += 1
    elif k in ('verse', 'hush', 'bridge'):        # night: a dark blue sky with stars, the house warm and low
        sq.on('Verts', 4, s0, s1, Grad(NIGHT, ROYAL, mode='up'), 40, 40)
        sq.twinkle('Verts', 2, s0, s1, [WHITE, GOLD], count=10, steps=35, bright=70, subbuf=sub(0, 50, 100, 100))
        sq.spirals('trees', 1, s0, s1, [ROYAL, RED], count=2, rotation=12, thickness=40, movement=1.0, bright=55,
                   perModel=True)
        sq.on('roofline-1', 1, s0, s1, RED, 50, 50)
        sq.on(['window-master', 'window-char', 'grinch-1'], 1, s0, s1, GREEN, 50, 50)
        sq.twinkle(FOREST, 3, s0, s1, [GOLD, RED, GREEN], count=8, steps=40, bright=55)

# ================================================================ the words on the wall
SPELL = [('joy', ['to', 'the', 'world'], ['JOY', 'TO', 'THE', 'WORLD'], [RED, GREEN, RED, GREEN]),
         ('the', ['lord', 'is', 'come'], ['THE', 'LORD', 'IS', 'COME'], [GREEN, GOLD, RED, GOLD]),
         ('god', ['sent', 'his', 'son'], ['GOD', 'SENT', 'HIS', 'SON'], [GOLD, RED, GREEN, GOLD]),
         ('go', ['tell', 'the', 'world'], ['GO', 'TELL', 'THE', 'WORLD'], [GREEN, RED, GREEN, RED]),
         ('tell', ['everyone'], ['TELL', 'EVERY', 'ONE'], [RED, GREEN, RED])]
CLIMAX = (SPAN['joy'][0], SPAN['drums'][0])
groups, used, i = [], set(), 0
while i < len(WORDS):
    w, s, e = WORDS[i]
    for first, rest, labels, cols in SPELL:
        if w != first or i in used: continue
        nxt_ok = [j for j in range(i + 1, min(i + 4, len(WORDS)))]
        if rest and (not nxt_ok or WORDS[nxt_ok[0]][0] != rest[0]): continue      # "the" only before "lord", ...
        times, j = [sung(s)], i + 1
        for r in rest:
            while j < len(WORDS) and WORDS[j][0] != r and WORDS[j][1] - s < 4.0: j += 1
            if j < len(WORDS) and WORDS[j][0] == r and WORDS[j][1] - s < 4.0:
                times.append(WORDS[j][1]); used.add(j); j += 1
            else:
                times.append(times[-1] + 0.4)
        if labels[-1] == 'ONE': times.append(times[-1] + 0.35)
        groups.append((times, labels, cols)); used.add(i)
        break
    i += 1
groups.sort()
for g, (times, labels, cols) in enumerate(groups):
    if CLIMAX[0] - 0.3 <= times[0] < CLIMAX[1] or kind(times[0]) == 'end': continue
    nt = groups[g + 1][0] if g + 1 < len(groups) else None
    end = min(nt[0] if nt else times[0] + 4.0, times[0] + 4.5)
    final = section(times[0]) == 'final'
    for p, (t, lab) in enumerate(zip(times, labels)):
        # each panel keeps its word until the next line's word for the same panel replaces it
        e = nt[min(p, len(nt) - 1)] if nt else t + 3.0
        e = min(e, t + 4.5, CLIMAX[0] if t < CLIMAX[0] else DUR, SPAN['end'][0])
        spell(1 + p, lab, t, max(e, t + 0.6), [RAINBOW[(g + p) % 6]] if final else [cols[p]])
    STORY.append((' '.join(labels), times[0], end))
    # what each line does to the yard
    if labels[1] == 'LORD':                 # "the Lord is come": a ring out from the manger
        manger_ring(times[3], (WHITE, GOLD) if not final else (WHITE, RAINBOW[g % 6]))
    elif labels[0] == 'GOD':                # "God sent His Son": a star comes down out of the sky to the manger
        a, b = times[0] - 0.2, times[3] + 0.3
        sq.morph('AllModels', 0, a, b, [WHITE, GOLD], (MANGER - 45, 100, MANGER - 45, 92), (MANGER, 8, MANGER, 0),
                 tail_start=2, tail_end=60, sparkles=50)
        sq.flash(NAT, 0, b, 1.5, WHITE, end_level=70)
    elif labels[0] == 'GO':                 # "go, tell the world": heralds run out from the manger
        a = times[0]
        fence_run(a, 1.6, FENCE_MANGER, 0, GOLD); fence_run(a, 0.9, FENCE_MANGER, 100, GOLD)
        for k in range(4): run_arch(3 - k, a + k * 0.35, 0.7, False, GOLD)
        hop_sticks(a + 0.4, a + 2.6, list(range(len(STICKS) - 1, -1, -1)), [rich(GOLD)])
    elif labels[0] == 'TELL':               # "...tell everyone": everybody
        t = times[1]
        sq.shockwave('AllModels', 2, t, t + 1.2, [WHITE, RED, GREEN] if not final else [WHITE] + RAINBOW[:3], cx=50,
                     cy=30, r_end=300, w_end=90)
        for k in range(4): climb_spiral(k, t, 0.8, [RED, GREEN][k % 2])
        sq.on(HOUSE + ['grinch-1'], 0, t, t + 1.0, Grad(RED, GOLD, GREEN, mode='right'), 100, 0)

# ================================================================ verse 1: the scene
s0, s1 = SPAN['verse1']
rj = [s for w, s, e in WORDS if w == 'rejoice' and s0 - 1 <= s < s1]
for t in rj:      # "rejoice, rejoice": bursts of sparkle on the spirals and arches
    sq.twinkle(['Spiral Trees', ARCHES], 2, sung(t), sung(t) + 1.2, [GOLD, WHITE], count=40, steps=10, bright=90)
king = word('king', s0)
crowns(king, king + 2.0, ks=[2, 3])
earth, angels = word('earth', king), word('angels', king)
fence_run(earth - 0.4, 2.0, 0, 100, GREEN)
sq.on('fenceline', 2, earth + 1.0, word('glory', earth) - 0.3, GREEN, 40, 0)
sq.meteors('Verts', 1, angels - 0.2, angels + 3.0, [WHITE, '#BFFFFF'], direction='Down', count=8, speed=5, bright=80)
sq.twinkle('Spiral Trees', 2, angels - 0.2, angels + 3.0, [WHITE], count=30, steps=20, bright=80)
glory, majesty = word('glory', angels), word('majesty', angels)
sq.shockwave('AllModels', 1, glory, majesty, [GOLD, WARM], cx=round(MANGER), cy=10, r_end=250, w_end=120)
sq.pinwheel('Verts', 3, glory, majesty, [Grad(GOLD, WARM, mode='radial-out'), BLACK], arms=10, speed=3, twist=0,
            size=100, thickness=8, xc=60, yc=-70, bright=55)
reign1 = word('reign', majesty) - 0.5
sq.cut(q(majesty), q(reign1), ['Verts', 'trees', ARCHES, 'Spiral Trees', 'fenceline'] + HOUSE + ['grinch-1'] + FOREST)
sq.on(NAT, 0, majesty, reign1 + 0.5, WHITE, 40, 100)
sq.on('fenceline', 1, majesty, reign1, Grad(BLACK, WARM, mode='right'), 0, 60)
STORY += [('rejoice, rejoice', rj[0], king), ('our King is here: a crown', king, earth - 0.4),
          ('men of earth (the fence) and angels cheer', earth - 0.4, glory), ('glory: gold rays from the manger', glory,
                                                                               majesty),
          ("majesty in a manger's light", majesty, reign1)]

# ================================================================ "He shall reign forever": crowns
RESPONSES = [reign1 + 0.3] + [sung(B(29 + 2 * k) + 0.5) for k in range(4)]      # verse 2 answers on bars 29/31/33/35
for t in RESPONSES:
    crowns(t, t + 2.0)
    for k in range(4): climb_spiral(k, t + k * 0.15, 0.9, GOLD)
    STORY.append(('He shall reign forever: crowns', t, t + 2.0))

# ================================================================ verse 2: call and response
s0, s1 = SPAN['verse2']
calls = [B(28 + 2 * k) + 0.2 for k in range(4)]
# "see the shepherds bowing down": the sticks light up and bow toward the manger, one after another
a = calls[0]
for j, i in enumerate(range(len(STICKS))):
    t = a + j * 1.6 / len(STICKS)
    sq.fill(STICKS[i], 1, t, t + 1.4, [rich([GREEN, RED][j % 2])], 100, 15, fadeout=0.3)
STORY.append(('see the shepherds bowing down', a, RESPONSES[1]))
# "wise men offer Him their crown": a crown carried panel to panel toward the manger
a = calls[1]
for k in range(6):
    draw(k, [CROWN], a + k * 0.38, a + k * 0.38 + 0.6, [GOLD], layer0=28, top=12, fade=0.3)
sq.flash(NAT, 0, a + 6 * 0.38, 1.2, GOLD, end_level=60)
STORY.append(('wise men offer Him their crown', a, RESPONSES[2]))
# "then till now and far beyond": a light runs the whole fence and off the end
a = calls[2]
fence_run(a, 2.2, 0, 115, SKY)
for k in range(4): run_arch(k, a + k * 0.5, 0.7, True, SKY)
STORY.append(('then till now and far beyond', a, RESPONSES[3]))
# "we're standing on the endless song": everything turns
a = calls[3]
sq.pinwheel('AllModels', 3, a, RESPONSES[4], [Grad(WARM, GOLD, mode='radial-out'), BLACK, Grad(RED, WARM, mode='radial-out'),
                                              BLACK], arms=4, speed=6, twist=60, size=100, thickness=35, bright=40)
STORY.append(('the endless song', a, RESPONSES[4]))

# ================================================================ the bridge and the chant: crowns climb, gold fills
s0, s1 = SPAN['bridge']
c0, c1 = SPAN['chant']
nb = round((c1 - c0) / BAR)
for j in range(nb):
    a = c0 + j * BAR
    crowns(a, a + BAR, top=6 + j * 6 + 2)
    sq.fill('Verts', 1, a, a + BAR, [Grad(ROYAL, '#8A2BFF', GOLD, mode='up')], j * 100 / nb, (j + 1) * 100 / nb,
            bright=75)
    sq.trunk_rise(a, BAR, GOLD, bright=90)
    sq.bounce(FOREST, 1, a, a + BAR * 0.6, [rich(GOLD)], height=20 + j * 80 / nb)
sq.spirals('trees', 1, c0, c1, [ROYAL, GOLD], count=2, rotation=30, thickness=40, movement=2.0, bright=75, perModel=True)
sq.on(HOUSE + ['grinch-1'], 1, c0, c1, Grad(ROYAL, GOLD, mode='time'), 20, 80, blend=None)
STORY += [('quiet: stars', s0, c0), ('He shall reign forever and ever: the crowns climb', c0, c1)]

# ================================================================ JOY!
a, b = CLIMAX
sq.moment(a, a + BAR, lambda a_, b_: (sq.bars('AllModels', 0, a_, b_, 'up', [Grad(*RAINBOW, mode='up'), BLACK], 1, 1),
                                      sq.shockwave('AllModels', 1, a_, b_, [WHITE, GOLD], cx=round(MANGER), cy=10,
                                                   r_end=300, w_end=100)), WHITE, 40)
joys = [sung(s) for w, s, e in WORDS if w == 'joy' and a - 0.5 <= s < b]
for j, t in enumerate(joys):
    e = joys[j + 1] if j + 1 < len(joys) else b
    for k in range(6):
        spell(k, 'JOY', t + k * 0.06, e, [RAINBOW[(k + j) % 6]])
STORY.append(('JOY on every panel', a, b))

# ================================================================ drums and voice: only the drums light the yard
a, b = SPAN['drums']
sq.cut(q(a), q(b), [el for el in sq.elements if el not in VERTS_M])
sq.on(NAT, 1, a, b, WARM, 60, 60)
for t in [t for t in KICKS if a <= t < b]:
    sq.shockwave('AllModels', 0, t, t + 0.7, [WHITE, RED], cx=round(MANGER), cy=10, r_end=180, w_end=40)
    sq.flash(NAT, 0, t, 0.4, WHITE, end_level=60)
for j, t in enumerate([t for t in SNARES if a <= t < b]):
    sq.bounce(FOREST, 1, t, t + 0.3, [rich(GREEN if j % 2 else RED)], height=70)
STORY.append(('drums and voice: only the drums light the yard', a, b))

# ================================================================ the end: everything gathers into the manger
a = SPAN['end'][0]
sq.cut(q(a), q(DUR))
sq.shockwave('AllModels', 0, a, a + 2.5, [WHITE, GOLD], cx=round(MANGER), cy=10, r_start=300, r_end=1, w_start=80,
             w_end=10)
for k in range(6):
    spell(k, 'JOY', a, END + 0.5, [RAINBOW[k]])
sq.on([HOUSE[0], HOUSE[1], HOUSE[2], 'grinch-1'], 0, a, a + 2.5, WARM, 70, 0)
sq.on(NAT, 0, a, END + 2.5, WHITE, 100, 0)                       # the manger is the last light out
STORY.append(('everything gathers into the manger', a, END + 2.5))

# ================================================================ timing tracks
labels = {'intro': 'Intro', 'verse1': 'Verse 1 (rejoice)', 'chorus1': 'Chorus', 'hush': 'Hush',
          'verse2': 'Verse 2 (call & response)', 'chorus2': 'Chorus', 'bridge': 'Bridge', 'chant': 'He shall reign (chant)',
          'joy': 'JOY!', 'drums': 'Drums & voice', 'final': 'Final chorus', 'end': 'End'}
st = sorted(STORY, key=lambda x: x[1])
nbars = int((END - B1) / BAR) + 1
sq.tracks = [
    ('Sections', marks([SPAN[n][0] for n, _, _ in SECTIONS], [labels[n] for n, _, _ in SECTIONS], end=DUR)),
    ('Story', [(lab, q(s), q(min(e, st[i + 1][1]) if i + 1 < len(st) else e)) for i, (lab, s, e) in enumerate(st)
               if q(min(e, st[i + 1][1]) if i + 1 < len(st) else e) > q(s)]),
    ('Lyrics', marks([s for w, s, e in WORDS], [w for w, s, e in WORDS], maxlen=1.2)),
    ('Bars', marks([B(n) for n in range(1, nbars + 1)], [str(n) for n in range(1, nbars + 1)], end=END)),
    ('Beats', marks(BEATS, [str((i - ev['phase']) % 4 + 1) for i in range(len(BEATS))], end=END)),
    ('Kick', marks(KICKS, maxlen=PER / 2)), ('Snare', marks(SNARES, maxlen=PER / 2)),
    ('Vocal Notes', marks([t for t, p, d in MELODY], [str(p) for t, p, d in MELODY], maxlen=PER)),
]

sq.write(OUT, dict(song='Joy to the World', artist='Big Daddy Weave', album='', media=media_path(SONG,
                   'joy_bigdaddyweave.mp3'),
                   comment='Generated from stem-separated audio analysis (Demucs + Basic Pitch + Whisper): 95 BPM, '
                           'D major. The Verts spell the words; the manger sends the news out; crowns for "He shall reign".'),
         DUR, timeline=ARGS[1] if len(ARGS) > 1 else None)
