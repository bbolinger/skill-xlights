"""Little Drummer Boy (for KING & COUNTRY) -> seqs/kc_drummer/kc_drummer.xsq

Same instrument map as punk-ohcome for show-wide cohesion: kick=arches, snare=moving patterns on Verts/trees,
cymbals=pixel forest, bass=fence dot, voice=spiral fill height, off-beats=house+floods.
Song-specific: candle-warm quiet verses where each sung syllable steps a light across the Verts,
nativity-spot breakdowns, a total blackout for the 3:24 silence, and AllModels moments at the big entrances.
"""
import json, sys, bisect
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from seqlib import *

SONG = 'kc_drummer'
HERE = song_dir(SONG)
ARGS = cli_args()
OUT = ARGS[0] if ARGS else str(SHOW / 'seqs' / SONG / f'{SONG}.xsq')
ev = json.load(open(HERE / 'events.json'))
T0, PER = ev['t0'], ev['per']
BAR = 4 * PER
B1 = T0 + ev['phase'] * PER
B = lambda n: B1 + (n - 1) * BAR            # start of 1-based bar n
DUR, END = 288.046, 282.4
GOLD = '#FFC832'                            # a gold that stays gold on pixels (the shared #FFAA00 reads amber)
WARM = '#FFE0A8'                            # soft candle-warm white for the quiet parts

# pixel_forest overlaps pix-evens/odds, so it only plays where those are cleared (the Waveform sections)
# 8 layers: the melody scrolling across the Verts needs several (notes overlap while they cross the wall)
sq = Seq(ELEMENTS[:6] + ['pixel_forest'] + ELEMENTS[6:], nlayers=15)
SCROLL_LAYERS = range(3, 15)

# colour families: each base colour becomes a gradient so props vary instead of all being one flat colour
FAMILY = {RED: (DEEP_RED, RED, '#FF4B4B'), GOLD: ('#E0A800', GOLD, '#FFF0C0'), GREEN: ('#00702E', GREEN, LIME),
          WHITE: ('#FFF0D8', WHITE, '#DDEBFF'), WARM: ('#FFD890', WARM, '#FFF6E8')}
def G(c, mode):
    """the colour's family as a gradient: mode 'right' varies across a group, 'up' bottom-to-top, 'time' over the effect"""
    return Grad(*FAMILY[c], mode=mode)
def tip(c):
    """dark at the bottom, the colour in the middle, white at the top: a fill reads taller the brighter its tip"""
    return Grad(FAMILY[c][0], c, WHITE, mode='up')

# ---------------------------------------------------------------- sections
quiet = dict(quiet=True, voice_steps=WARM, voice=WARM, bass=RED, bass_bright=50, verts_bg=('wave', WARM, 25),
             forest_twinkle=(WARM, 30), arch_bg=(RED, 12), house_bg=(WARM, 20), nativity=(GOLD, 70), grinch=(GREEN, 10),
             tree_breathe=WARM,
             spiral_bg=(WARM, 8))
spot = dict(quiet=True, voice_steps=WARM, voice=WARM, steps_bright=50, nativity=(GOLD, 100), house_bg=(WARM, 10),
            tree_glow=GOLD,
            stars=True)
full = dict(kick=RED, snare=WHITE, cym=WHITE, bounce=True, tree_spirals=True, bass=RED, voice=WHITE, off=True, house_bg=(RED, 30), grinch=(GREEN, 35),
            nativity=(GOLD, 35), spiral_bg=(RED, 8))
SECTIONS = [
    ('roll', 0.0, B(2), dict(kick=RED, kick_bright=40, snare=RED, snare_mode='ripple', snare_bright=50, cym=WHITE,
                             cym_bright=40, forest_ramp=RED, arch_ramp=RED)),
    ('drums', B(2), B(6), dict(full, snare_mode='ripple', verts_bg=('bars', 'Right', RED, 30, 4), bg_forest=(RED, 12))),
    ('drums2', B(6), B(11), dict(full, snare_mode='xc', verts_bg=('diag', RED, 45), bg_forest=(RED, 12))),
    ('verse1', B(11), B(18), dict(quiet, bg_fadein=4)),
    ('verse2', B(18), B(24), dict(quiet, kick=RED, kick_bright=60, snare=WARM, snare_mode='ripple', snare_bright=60,
                                  cym=WHITE, cym_bright=50, voice_steps=None, verts_bg=('bars', 'Right', WARM, 25, 3),
                                  forest_waves=('phrases', WARM))),
    ('verse2b', B(24), B(29), dict(quiet, kick=RED, kick_bright=80, snare=WHITE, snare_mode='diag', snare_bright=70,
                                   cym=WHITE, cym_bright=60, voice_steps=None, verts_bg=('diag', RED, 40),
                                   forest_waves=('phrases', WHITE))),
    ('break1', B(29), B(32), dict(spot, climb=GOLD)),
    ('chorus1', B(32), B(36), dict(full, snare_mode='diag', verts_bg=('bars', 'Left', RED, 35, 3), bg_forest=(RED, 15),
                                   forest_waves=(1, RED))),
    ('chorus1b', B(36), B(44), dict(full, kick=GREEN, snare=WHITE, snare_mode='xc', voice=WHITE,
                                    verts_bg=('wave', GREEN, 35), bg_forest=(GREEN, 15), house_bg=(GREEN, 30))),
    ('chorus1c', B(44), B(55), dict(full, snare_mode='ripple', voice=WHITE, verts_bg=('diag', RED, 50), bg_forest=(RED, 15),
                                    forest_waves=(1, WHITE))),
    ('break2', B(55), B(58), dict(spot, climb=GOLD)),
    ('chorus2', B(58), B(66), dict(full, kick=GREEN, snare_mode='diag', voice=WHITE, bass=GREEN,
                                   verts_bg=('bars', 'Right', GREEN, 35, 6), bg_forest=(GREEN, 15), house_bg=(GREEN, 25),
                                   grinch=(GREEN, 60), forest_waves=(1, GREEN))),
    ('chorus2b', B(66), B(75), dict(full, snare=RED, snare_mode='xc', voice=WHITE, verts_bg=('swing', GREEN, 45),
                                    bg_forest=(RED, 15))),
    ('chorus2c', B(75), B(85), dict(full, kick=WHITE, snare=RED, snare_mode='ripple', voice=WHITE, meteors=True,
                                    bg_forest=(GREEN, 18), house_bg=(RED, 35), forest_waves=(1, WHITE))),
    ('break3', B(85), B(89), dict(spot, fade_out=True)),
    ('silence', B(89), B(90), dict(nativity=(GOLD, 30))),
    ('guitar', B(90), B(94), dict(guitar_steps=WHITE, guitar_voice=WHITE, bass=RED, bass_bright=70, arch_bg=(RED, 15),
                                  tree_breathe=RED,
                                  house_bg=(RED, 15), nativity=(GOLD, 40), spiral_bg=(WHITE, 6),
                                  verts_bg=('bars', 'Left', RED, 20, 2), waveform=[WHITE, RED])),
    ('build', B(94), B(98), dict(kick=RED, snare=WHITE, cym=WHITE, bounce=True, march=WHITE, climb=RED, arch_climb=RED,
                                 bass=RED, guitar_voice=WHITE, house_ramp=RED, nativity=(GOLD, 60), grinch=(GREEN, 30))),
    ('final', B(98), B(106), dict(full, kick=WHITE, snare=GREEN, snare_mode='diag', voice=WHITE, sparkles=60,
                                  verts_bg=('bars', 'Left', RED, 40, 6), bg_forest=(GREEN, 20), house_bg=(RED, 35),
                                  nativity=(GOLD, 60), grinch=(GREEN, 60), forest_waves=(0.5, RED))),
    ('finalb', B(106), B(115), dict(full, snare_mode='xc', voice=WHITE, sparkles=60, verts_bg=('diag', GREEN, 55),
                                    bg_forest=(RED, 20), house_bg=(GREEN, 40), nativity=(GOLD, 60), grinch=(GREEN, 60),
                                    forest_waves=(0.5, WHITE))),
    ('drumfeat', B(115), B(119), dict(full, kick=WHITE, snare=RED, snare_mode='ripple', verts_bg=('wave', RED, 45),
                                      bg_forest=(RED, 10))),
    ('outro', B(119), END, dict(kick=RED, kick_bright=60, snare=WARM, snare_mode='ripple', snare_bright=60, cym=WHITE,
                                cym_bright=40, bounce=True, bounce_bright=60, voice=WARM, tree_breathe=WARM, verts_bg=('bars', 'Right', WARM, 25, 2), house_bg=(WARM, 25),
                                nativity=(GOLD, 80), spiral_bg=(WARM, 8))),
]
SEC_START = [s for _, s, _, _ in SECTIONS]
def section(t):
    i = bisect.bisect_right(SEC_START, t + 0.001) - 1
    return SECTIONS[max(i, 0)]

# ---------------------------------------------------------------- drums
kicks = ev['kick']
for i, t in enumerate(kicks):
    name, s0, s1, st = section(t)
    if st.get('kick'):
        d = max(nxt(kicks, i, 0.30), 0.075)
        sq.flash(ARCHES, 0, t, d, G(st['kick'], 'right'), bright=st.get('kick_bright', 100))
        sq.trunk_ring(t, max(d, 0.2), st['kick'], tree=i % 3, bright=st.get('kick_bright', 100))

snares = ev['snare']; n = 0
for i, t in enumerate(snares):
    name, s0, s1, st = section(t)
    if not st.get('snare') or st.get('march'): continue
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

cyms = ev['cym']; n = 0
for i, t in enumerate(cyms):
    name, s0, s1, st = section(t)
    if not st.get('cym') or st.get('bounce'): continue
    sq.flash(FOREST[n % 2], 1, t, max(nxt(cyms, i, 0.35), 0.075), st['cym'], bright=st.get('cym_bright', 85),
             sparkles=st.get('sparkles', 40))
    n += 1

# pixel sticks bounce with the drums: kick fills the even sticks, snare the odd ones, as high as the hit was hard
for grp, times, vals, key in (('pix-evens', ev['kick'], ev['kick_v'], 'kick'), ('pix-odds', ev['snare'], ev['snare_v'], 'snare')):
    for i, (t, v) in enumerate(zip(times, vals)):
        name, s0, s1, st = section(t)
        if not st.get('bounce') or not st.get(key): continue
        d = min(max(nxt(times, i, 0.45), 0.15), 0.45)
        px = round(2 + max(v - 0.35, 0) / 0.65 * 6)                # 2..8 of the stick's 8 pixels
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
    pos = 5 + (min(max(p, 26), 50) - 26) / 24 * 90
    sq.flash('fenceline', 0, t, max(nxt(bt, i, 2 * PER), 0.075), Grad(WHITE, st['bass']), bright=st.get('bass_bright', 100),
             subbuf=sub(max(pos - 5, 0), 0, min(pos + 5, 100), 100), end_level=30)

# ---------------------------------------------------------------- voice -> spiral height; in quiet parts the melody also scrolls across the Verts
vox = [(t, midi(nm)) for t, e, nm in ev['vox']]
vt = [t for t, _ in vox]; n = 0
scroll_notes = []
for i, (t, p) in enumerate(vox):
    name, s0, s1, st = section(t)
    d = max(nxt(vt, i, 2 * PER), 0.075)
    if st.get('voice'):
        h = 10 + (min(max(p, 50), 81) - 50) / 31 * 90
        sq.on('Spiral Trees', 1, t, t + d, tip(st['voice']), 100, 70, subbuf=sub(0, 0, 100, h), perModel=True)
    if st.get('voice_steps'):
        scroll_notes.append((t, p, min(d, PER), st['voice_steps'], st.get('steps_bright', 80)))

# guitar interlude: guitar takes over the voice's job
gnotes, last = [], -1
for s, e, p, v in load_notes(HERE / 'midi' / 'guitar_basic_pitch.csv'):
    if B(90) <= s < B(98) and v >= 45 and s - last > 0.08: gnotes.append((s, p)); last = s
gt = [t for t, _ in gnotes]; n = 0
for i, (t, p) in enumerate(gnotes):
    name, s0, s1, st = section(t)
    d = max(nxt(gt, i, PER), 0.075)
    if st.get('guitar_voice'):
        h = 10 + (min(max(p, 50), 81) - 50) / 31 * 90
        sq.on('Spiral Trees', 1, t, t + d, tip(st['guitar_voice']), 100, 60, subbuf=sub(0, 0, 100, h), perModel=True)
    if st.get('guitar_steps'):
        scroll_notes.append((t, p, d, st['guitar_steps'], 75))
# sung (and in the interlude, played) notes glide right to left across the Verts at the height of their pitch
placed = sq.melody_scroll('Verts', [(t, p, d, [WHITE, c], b) for t, p, d, c, b in scroll_notes], None,
                          travel=1.5 * BAR, lo=50, hi=74, layers=SCROLL_LAYERS)
print(f'melody scroll: {placed} of {len(scroll_notes)} notes placed')

# ---------------------------------------------------------------- per-section backgrounds and set pieces
for name, s0, s1, st in SECTIONS:
    if 'bg_forest' in st: sq.on(FOREST, 2, s0, s1, G(st['bg_forest'][0], 'radial-out'), bright=st['bg_forest'][1])
    if 'forest_twinkle' in st: sq.twinkle(FOREST, 2, s0, s1, [st['forest_twinkle'][0]], 40, 40, st['forest_twinkle'][1])
    if 'forest_ramp' in st: sq.on(FOREST, 2, s0, s1, st['forest_ramp'], 0, 40)
    if 'arch_bg' in st: sq.on(ARCHES, 2, s0, s1, st['arch_bg'][0], bright=st['arch_bg'][1])
    if 'arch_ramp' in st: sq.on(ARCHES, 2, s0, s1, st['arch_ramp'], 0, 40)
    if 'spiral_bg' in st: sq.on('Spiral Trees', 2, s0, s1, st['spiral_bg'][0], bright=st['spiral_bg'][1])
    vb = st.get('verts_bg')
    if vb and vb[0] == 'bars':
        _, direction, c, br, cyc = vb; sq.bars('Verts', 2, s0, s1, direction, [G(c, 'up'), BLACK], 2, cyc, br)
    elif vb and vb[0] == 'diag':
        _, c, br = vb
        for k in range(int(round((s1 - s0) / BAR))):
            a, b = DIAG['up-right' if k % 2 == 0 else 'up-left']
            sq.morph('Verts', 2, s0 + k * BAR, s0 + (k + 1) * BAR, [FAMILY[c][2], G(c, 'right')], a, b, tail_end=50, bright=br)
    elif vb and vb[0] == 'wave':
        _, c, br = vb; sq.wave('Verts', 2, s0, s1, c, br, colors=[G(c, 'up')], fadein=st.get('bg_fadein', 0))
    elif vb and vb[0] == 'swing':     # a 3D spiral rocking back and forth across the wall (DreamsOfFireflies)
        _, c, br = vb; sq.spirals('Verts', 2, s0, s1, [c, WHITE], count=1, thickness=50, movement=1.0, bright=br,
                                  three_d=True, swing=True)
    if st.get('tree_spirals'):        # barber-pole bands wrapping the trunks in the section's colour
        sq.spirals('trees', 2, s0, s1, [st.get('kick', RED), WHITE], count=2, rotation=20, thickness=40, movement=2.0,
                   bright=60, perModel=True)
    if st.get('tree_breathe'):        # a soft glow rises from the roots and settles, every two bars
        for k in range(int((s1 - s0) // (2 * BAR))):
            a = s0 + k * 2 * BAR
            sq.fill('trees', 2, a, a + BAR, [Grad(st['tree_breathe'], WHITE, mode='up')], 0, 60, per_model=True, bright=50)
            sq.fill('trees', 2, a + BAR, a + 2 * BAR, [Grad(st['tree_breathe'], WHITE, mode='up')], 60, 0, per_model=True, bright=50)
    if st.get('tree_glow'):           # breakdowns: a low candle glow creeping up the trunks
        sq.fill('trees', 2, s0, s1, [Grad(st['tree_glow'], WHITE, mode='up')], 0, 40, per_model=True, bright=60)
    if 'house_bg' in st: sq.on(HOUSE, 1, s0, s1, G(st['house_bg'][0], 'right'), bright=st['house_bg'][1], blend=None)
    if 'house_ramp' in st: sq.on(HOUSE, 1, s0, s1, st['house_ramp'], 5, 100, blend=None)
    if 'grinch' in st: sq.on('grinch-1', 1, s0, s1, st['grinch'][0], bright=st['grinch'][1], blend=None)
    if 'nativity' in st: sq.on('Nativity Spot', 1, s0, s1, st['nativity'][0], bright=st['nativity'][1], blend=None)
    if st.get('meteors'): sq.meteors(MATRIX, 1, s0, s1, [GOLD, WHITE], sparkles=40)
    if st.get('climb'):            # the Verts and the trunks fill smoothly into the next big entrance
        sq.fill('Verts', 1, s0, s1, [G(st['climb'], 'up')], 0, 100, bright=60 if st.get('quiet') else 100)
        sq.fill('trees', 1, s0, s1, [G(st['climb'], 'up')], 0, 100, per_model=True, bright=60 if st.get('quiet') else 100)
    if st.get('arch_climb'):
        for k in range(4):
            a, b = s0 + k * BAR, s0 + (k + 1) * BAR; w = 12.5 * (k + 1)
            sq.on(ARCHES, 1, a, b, st['arch_climb'], subbuf=sub(0, 0, w, 100), perModel=True)
            sq.on(ARCHES, 2, a, b, st['arch_climb'], subbuf=sub(100 - w, 0, 100, 100), perModel=True)
    if st.get('march'):             # a white light glides Vert to Vert along the top of the rising fill, one hop per beat
        for k in range(16):
            h = 100 * (k + 0.5) / 16
            x0, x1 = VERT_X[pingpong(k, 6)], VERT_X[pingpong(k + 1, 6)]
            sq.morph('Verts', 0, s0 + k * PER, s0 + (k + 1) * PER, [WHITE, WHITE], (x0, h - 8, x0, h), (x1, h - 8, x1, h),
                     tail_end=35)

    if st.get('stars'):             # breakdowns: a dim starfield over the yard while the manger glows
        end = s1 - BAR if name == 'break3' else s1          # break3's last bar fades to black on its own
        sq.shader(FOREST + [ARCHES, 'Spiral Trees'], 2, s0, end, 'Seqs_Misc/interstellar_cornfield/Shaders/Spacels.fs',
                  params=dict(brightness=0.25, density=0.75, depth=0.25, distfading=0.25, morph=0.89, rate=0,
                              saturation=0.5, zoom=2.5, moveX=0, moveY=0), bools=dict(nebula=0),
                  bright=40, fadein=1.5, fadeout=1.0)
    fw = st.get('forest_waves')
    if fw:                          # a sine wave rolls across the pixel sticks, alternating group and direction
        every, c = fw
        if every == 'phrases':
            starts = [p[0] for p in ev['phrases'] if s0 <= p[0] < s1]
        else:
            starts = [s0 + k * every * BAR for k in range(int(round((s1 - s0) / (every * BAR))))]
        for k, t in enumerate(starts):
            sq.wave(FOREST[k % 2], 0, t, t + 2 * PER, None, 100, waves=900, speed=10, kind='Sine', fill='None',
                    thickness=50, height=50, direction='Right to Left' if k % 2 == 0 else 'Left to Right',
                    colors=[WHITE, c])
    if st.get('waveform'):          # the song's own waveform drawn across the whole pixel forest
        sq.cut(q(s0), q(s1), FOREST)
        sq.waveform('pixel_forest', 0, s0, s1, st['waveform'])

# break3 dims everything into the silence; the silence itself is black except a faint nativity spot
_, s0, s1, _ = [s for s in SECTIONS if s[0] == 'break3'][0]
sq.cut(q(s1 - BAR), q(s1), [el for el in ELEMENTS if el != 'Nativity Spot'])
sq.fill('Verts', 1, s1 - BAR, s1, [G(GOLD, 'up')], 30, 0, bright=40)
sq.fill('trees', 1, s1 - BAR, s1, [G(GOLD, 'up')], 40, 0, per_model=True, bright=50)
sq.on(HOUSE, 1, s1 - BAR, s1, GOLD, 20, 0, blend=None)

# ---------------------------------------------------------------- "pa rum pum pum pum": the same signature every time
# Words come from Whisper on the vocal stem (lyrics.json). While it's sung, the song's own waveform (VU Meter
# Waveform, drawn live by xLights from the audio) runs jagged across the whole Vert canvas; on the last "pum" the
# wall bursts gold with the spiral trees and the Nativity Spot (the drummer plays for the baby).
import re
words = json.load(open(HERE / 'lyrics.json'))
clean = lambda w: re.sub(r'[^a-z]', '', w['word'].lower())
vox_on = [v[0] for v in ev['vox']]
def snap(t):                                    # Whisper word times are approximate; use the sung note onset
    near = min(vox_on, key=lambda v: abs(v - t)); return near if abs(near - t) < 0.15 else t
units, cur = [], []
for w in words:
    c = clean(w)
    if c not in ('pa', 'pah', 'rum', 'pum'):
        if cur: units.append(cur); cur = []
        continue
    starts_unit = c in ('pa', 'pah') or (c == 'rum' and cur and clean(cur[-1]) == 'pum')
    if cur and (starts_unit or w['start'] - cur[-1]['end'] > 0.8): units.append(cur); cur = []
    cur.append(w)
if cur: units.append(cur)
def snap_unit(u):                               # keep syllables in order and apart even if two snap to one note
    out = []
    for w in u:
        t = snap(w['start'])
        if out and t < out[-1][0] + 0.08: t = max(w['start'], out[-1][0] + 0.08)
        out.append((t, clean(w)))
    return out
units = [snap_unit(u) for u in units if len(u) >= 4]
HOOK = Grad('#E0A800', GOLD, WHITE, mode='up')
hook_marks = []
for u in units:
    times = [t for t, _ in u]
    first, last = times[0], times[-1]
    sq.cut(q(first - 0.05), q(last + 1.5 * PER), ['Verts'], layers=[0])   # the hook takes over the Verts' top layer
    sq.waveform('Verts', 0, first, last + PER / 2, [WHITE, GOLD])
    sq.morph('Verts', 0, last + PER / 2, last + 1.5 * PER, [WHITE, GOLD], *DIAG['up'], tail_start=10, tail_end=100,
             extra={'T_TEXTCTRL_Fadeout': '0.30'})
    sq.trunk_rise(last, 1.5 * PER, GOLD)
    sq.flash('Spiral Trees', 0, last, 1.5 * PER, HOOK, perModel=True)
    sq.flash('Nativity Spot', 0, last, 1.5 * PER, GOLD, end_level=40)
    for t, syl in u:
        hook_marks.append((syl, t))

# ---------------------------------------------------------------- AllModels moments (everything underneath is cleared)
sq.moment(B(2), B(2) + 2 * PER, lambda a, b: sq.shockwave('AllModels', 0, a, b, [RED, WHITE]), RED)              # drums hit
sq.moment(B(11), B(11) + 4 * PER, lambda a, b: sq.morph('AllModels', 0, a, b, [WARM, WARM], *DIAG['right'], tail_end=70), WARM, 25)
sq.moment(B(32), B(32) + 3 * PER, lambda a, b: sq.shockwave('AllModels', 0, a, b, [WHITE, RED]), WHITE, 20)      # chorus 1
sq.moment(B(58), B(58) + 2 * PER, lambda a, b: sq.morph('AllModels', 0, a, b, [GREEN, RED], *DIAG['left'], tail_end=60), GREEN)
sq.moment(B(90), B(90) + 3 * PER, lambda a, b: sq.shockwave('AllModels', 0, a, b, [WHITE]), WHITE)                # out of the silence
sq.moment(B(98), B(99), lambda a, b: sq.shader('AllModels', 0, a, b, 'Seqs_Misc/interstellar_cornfield/Shaders/Cosmic Flare.fs',
          params=dict(brightness=2, ray_brightness=6, gamma=2, spot_brightness=5, ray_density=10, curvature=300, freq=8,
                      red=7, green=2, blue=1), bools=dict(warp=1), bright=60, fadein=0.2, fadeout=0.8), RED, 30)    # final chorus: solar flare
sq.moment(B(115), B(117), lambda a, b: sq.whirl('AllModels', 0, a, b, [RED, WHITE, GREEN]), RED, 30)    # drum feature: whirl
def finale(a, b):                   # warm rays across the yard, fading out
    sq.shader('AllModels', 0, a, b, 'Shaders/Sleepy Rays.fs',
              params=dict(Count=18.13, posX=0, posY=-0.33, rate=-0.02, soft=0.28, width=0.28), fadein=0.5, fadeout=2.5)
sq.moment(B(122), END + 1.2, finale, WARM)
sq.cut(q(END + 1.2), q(DUR), ['Nativity Spot'])
sq.on('Nativity Spot', 0, END + 1.2, END + 4.5, GOLD, 100, 0)          # the manger is the last light out

# ---------------------------------------------------------------- timing tracks
labels = {'roll': 'Drum roll', 'drums': 'Drum intro', 'drums2': 'Drum intro 2', 'verse1': 'Verse 1 (no drums)',
          'verse2': 'Verse 2 (light drums)', 'verse2b': 'Verse 2 build', 'break1': 'Breakdown 1', 'chorus1': 'Chorus 1',
          'chorus1b': 'Chorus 1b', 'chorus1c': 'Chorus 1c', 'break2': 'Breakdown 2', 'chorus2': 'Chorus 2',
          'chorus2b': 'Chorus 2b', 'chorus2c': 'Chorus 2c', 'break3': 'Breakdown 3', 'silence': 'Silence',
          'guitar': 'Guitar interlude', 'build': 'Drums return - build', 'final': 'Final chorus', 'finalb': 'Final chorus b',
          'drumfeat': 'Drum feature', 'outro': 'Outro'}
nbars = int((END - B1) / BAR) + 1
sq.tracks = [
    ('Sections', marks([s for _, s, _, _ in SECTIONS] + [END], [labels[n] for n, _, _, _ in SECTIONS] + ['End'], end=DUR)),
    ('Bars', marks([B(k + 1) for k in range(nbars)], [str(k + 1) for k in range(nbars)], end=END)),
    ('Beats', marks(ev['beats'], [str((i - ev['phase']) % 4 + 1) for i in range(len(ev['beats']))], end=END)),
    ('Kick', marks(ev['kick'], maxlen=PER / 2)), ('Snare', marks(ev['snare'], maxlen=PER / 2)),
    ('Cymbals', marks(ev['cym'], maxlen=PER)), ('Off-beat Hits', marks(ev['off'], maxlen=PER / 2)),
    ('Bass Notes', marks([t for t, e, n in ev['bass']], [n for t, e, n in ev['bass']], maxlen=2 * PER)),
    ('Vocal Notes', marks([t for t, e, n in ev['vox']], [n for t, e, n in ev['vox']], maxlen=2 * PER)),
    ('Vocal Phrases', marks([p[0] for p in ev['phrases']], maxlen=None, end=None, per=1.0)),
]
# phrases get their real lengths
sq.tracks[-1] = ('Vocal Phrases', [('', q(a), q(b)) for a, b, _ in ev['phrases'] if q(b) > q(a)])
sq.tracks.insert(1, ('Pa Rum Pum', marks([t for _, t in hook_marks], [s for s, _ in hook_marks], maxlen=PER)))
sq.tracks.insert(2, ('Lyrics', marks([w['start'] for w in words], [w['word'] for w in words], maxlen=1.0)))

sq.write(OUT, dict(song='Little Drummer Boy', artist='for KING & COUNTRY', album='A Drummer Boy Christmas',
                   media=media_path(SONG, 'kc_drummer.mp3'),
                   comment='Generated from stem-separated audio analysis (Demucs + Basic Pitch): 104 BPM. Kick=arches, '
                           'snare=moving patterns on Verts/trees, cymbals=pixel forest, bass=fence dot, voice=spiral fill '
                           'height, off-beats=house/floods; AllModels moments at the big entrances.'),
         DUR, timeline=ARGS[1] if len(ARGS) > 1 else None)
