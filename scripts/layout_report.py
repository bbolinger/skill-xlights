"""Describe a show's layout (xlights_rgbeffects.xml) so you can plan a sequence around it.

usage: layout_report.py [--draft-config]
Prints every model (type, size in pixels, world position) and every group (members left to right, and where each
member's centre falls across the group's width in % - what show_config's *_X lists hold). Models in no group are
flagged: they need their own row in the sequence. --draft-config prints a starting show_config.py instead.

Positions are model centres from WorldPosX, so the % values are approximate (good enough to aim a ripple or ring
at one member); check the extremes against the layout in xLights if precision matters.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import os

SHOW = Path(os.environ.get('XLIGHTS_SHOW', Path(__file__).resolve().parent.parent))
root = ET.parse(SHOW / 'xlights_rgbeffects.xml').getroot()
models = {m.get('name'): m for m in root.find('models')}
groups = {g.get('name'): [x for x in (g.get('models') or '').split(',') if x] for g in root.find('modelGroups')}


def size(m):
    """(description, pixel count) for a model"""
    a, kind = m.attrib, m.get('DisplayAs')
    i = lambda k, d=0: int(float(a.get(k, d)))
    if kind == 'Matrix':
        strands = i('NumStrings', 1) * i('StrandsPerString', 1)
        per = i('NodesPerString') * i('NumStrings', 1) // max(strands, 1)
        w, h = (strands, per) if a.get('Vertical') == 'true' else (per, strands)
        return f'matrix {w}x{h}', w * h
    if kind == 'Arches':
        return f'{i("NumArches", 1)} arch x {i("NodesPerArch")} px', i('NumArches', 1) * i('NodesPerArch')
    if kind == 'Custom':
        return f'custom {a.get("CustomWidth")}x{a.get("CustomHeight")} grid', None
    n = i('NodesPerString') * i('NumStrings', 1)
    return (f'{kind.lower()} {n} px' if n else kind.lower()), n


def x(name):
    if name in models: return float(models[name].get('WorldPosX', 0))
    xs = [x(m) for m in groups.get(name, []) if m in models or m in groups]
    return sum(xs) / len(xs) if xs else 0.0


def leaves(g, seen=()):
    out = []
    for m in groups.get(g, []):
        if m in groups and m not in seen: out += leaves(m, seen + (g,))
        elif m in models: out.append(m)
    return out


def member_pct(g):
    ms = sorted(groups[g], key=x)
    xs = [x(m) for m in ms]
    lo, hi = min(xs), max(xs)
    return [(m, (v - lo) / (hi - lo) * 100 if hi > lo else 50.0) for m, v in zip(ms, xs)]


in_group = {m for g in groups for m in leaves(g)}

if '--draft-config' not in sys.argv:
    print(f'show: {SHOW}\n')
    print('MODELS (left to right)')
    for n in sorted(models, key=x):
        desc, _ = size(models[n])
        flag = '' if n in in_group else '   <- in no group'
        print(f'  {n:28} {desc:26} x={x(n):8.0f} y={float(models[n].get("WorldPosY", 0)):7.0f}{flag}')
    print('\nGROUPS')
    for g in sorted(groups, key=lambda g: -len(leaves(g))):
        ls = leaves(g)
        px = sum((size(models[m])[1] or 0) for m in ls)
        print(f'  {g}  ({len(ls)} models, ~{px} px, layout {next(e.get("layout") for e in root.find("modelGroups") if e.get("name") == g)})')
        mp = member_pct(g) if len(groups[g]) > 1 else []
        if len(mp) <= 12:
            print('     ' + ', '.join(f'{m} {p:.0f}%' for m, p in mp))
        else:
            print(f'     {len(mp)} members, {mp[0][0]} .. {mp[-1][0]}')
    sys.exit()

# ---------------------------------------------------------------- draft show_config.py
big = sorted(groups, key=lambda g: -len(leaves(g)))
allg = big[0] if big else None
print('"""Draft show_config.py from layout_report.py - EDIT IT: pick the rows, say what each prop physically is."""\n')
print('MEDIA_ROOT = None    # the show folder on the machine running xLights, if not this one\n')
print('# groups (largest first) and models in no group; trim to a disjoint set of rows')
rows = [g for g in big if g != allg][:12] + sorted(n for n in models if n not in in_group)
print(f'ELEMENTS = {[allg] + rows!r}\n')
print(f'ALL = {allg!r}           # whole-yard group for moments')
print("CANVAS = None         # TODO: the matrix group that acts as one big canvas")
print("TRUNKS = None         # TODO: matrices wrapped on real objects (tree trunks, columns), if any")
print("ARCHES = None         # TODO")
print("FOREST = []           # TODO: pixel sticks / mini trees, ideally split in two alternating groups")
print("SPIRAL = None\nFENCE = None\nHOUSE = []\nFLOODS = []")
print(f'NON_MEMBERS = []      # TODO: rows not inside {allg!r}\n')
print('# member positions across each group (% of its width), left to right')
for g in big:
    if 1 < len(groups[g]) <= 12:
        print(f'# {g}: ' + ', '.join(m for m, _ in member_pct(g)))
        print(f'{g.upper().replace(" ", "_").replace("-", "_")}_X = {[round(p, 1) for _, p in member_pct(g)]}')
print('VERT_X, TREE_X, ARCH_X = [], [], []   # TODO: point these at the canvas / trunk / arch lists above')
