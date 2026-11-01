"""Sanity-check a generated .xsq against the show layout.

usage: validate_xsq.py <file.xsq> [...]
Checks: every model/group exists in xlights_rgbeffects.xml, effects within a layer don't overlap, times sit on the
25 ms frame grid and inside the sequence, and palette/EffectDB references resolve. Exit code 1 on any problem.
"""
import sys, collections
import xml.etree.ElementTree as ET
from seqlib import SHOW, cli_args

layout = ET.parse(SHOW / 'xlights_rgbeffects.xml').getroot()
names = {m.get('name') for m in layout.find('models')} | {g.get('name') for g in layout.find('modelGroups')}
failed = False
for path in cli_args():
    r = ET.parse(path).getroot()
    npal, ndb = len(r.find('ColorPalettes')), len(r.find('EffectDB'))
    dur = float(r.find('head/sequenceDuration').text) * 1000
    problems, kinds = [], collections.Counter()
    for el in r.find('ElementEffects'):
        n = el.get('name')
        if el.get('type') == 'model' and n not in names: problems.append(f'unknown model/group {n!r}')
        for li, L in enumerate(el.findall('EffectLayer')):
            prev = -1
            for e in L.findall('Effect'):
                s, t = int(e.get('startTime')), int(e.get('endTime'))
                if s % 25 or t % 25: problems.append(f'{n} L{li}: {s}-{t} off the 25 ms grid')
                if t <= s or t > dur + 25: problems.append(f'{n} L{li}: bad span {s}-{t}')
                if s < prev: problems.append(f'{n} L{li}: {s} overlaps previous effect ending {prev}')
                prev = t
                if e.get('ref') is not None and not 0 <= int(e.get('ref')) < ndb: problems.append(f'{n}: bad ref')
                if e.get('palette') is not None and not 0 <= int(e.get('palette')) < npal: problems.append(f'{n}: bad palette')
                if el.get('type') == 'model': kinds[e.get('name')] += 1
    print(f'{path}: {sum(kinds.values())} effects {dict(kinds.most_common())}')
    for p in problems[:20]: print('  PROBLEM', p)
    print(f'  {len(problems)} problems')
    failed |= bool(problems)
sys.exit(1 if failed else 0)
