"""Draw a generated .xsq as a timeline image: one row per element/layer, effects as bars in their first palette
colour (dimmer = lower brightness), section marks from the "Sections" timing track. Handy for eyeballing a
design without xLights.

usage: timeline.py <file.xsq> <out.png> [start_s end_s]
"""
import sys
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from seqlib import cli_args

xsq, out = cli_args()[:2]
r = ET.parse(xsq).getroot()
dur = float(r.find('head/sequenceDuration').text)
a, b = (float(x) for x in cli_args()[2:4]) if len(cli_args()) >= 4 else (0.0, dur)
pals = []
for p in r.find('ColorPalettes'):
    kv = dict(x.split('=', 1) for x in (p.text or '').split(','))
    c = kv.get('C_BUTTON_Palette1', '#FFFFFF')
    if 'Values=' in c: c = c.split('^c=')[1][:7]          # colour curve: show its first colour
    pals.append((c, int(kv.get('C_SLIDER_Brightness', 100))))

rows, secs = [], []
for el in r.find('ElementEffects'):
    if el.get('type') == 'timing':
        if el.get('name') == 'Sections':
            secs = [(int(e.get('startTime')) / 1000, e.get('label')) for e in el.iter('Effect')]
        continue
    for li, L in enumerate(el.findall('EffectLayer')):
        fx = L.findall('Effect')
        if fx: rows.append((f"{el.get('name')} L{li}", fx))

fig, ax = plt.subplots(figsize=(24, 0.3 * len(rows) + 1.5)); ax.set_facecolor('black')
for i, (label, fx) in enumerate(rows):
    y = len(rows) - i - 0.9
    for e in fx:
        s, t = int(e.get('startTime')) / 1000, int(e.get('endTime')) / 1000
        if t < a or s > b: continue
        c, br = pals[int(e.get('palette'))]
        ax.add_patch(Rectangle((s, y), t - s, 0.8, color=c, alpha=max(0.15, min(1, br / 100)), lw=0))
for x, l in secs:
    if a <= x <= b: ax.axvline(x, color='w', lw=0.8); ax.text(x + 0.1, len(rows) + 0.2, l, fontsize=8)
ax.set_xlim(a, b); ax.set_ylim(0, len(rows) + 1.2)
ax.set_yticks([len(rows) - i - 0.5 for i in range(len(rows))]); ax.set_yticklabels([l for l, _ in rows], fontsize=8)
plt.tight_layout(); plt.savefig(out, dpi=50); plt.close()
print('wrote', out)
