"""Find how an effect is really configured in the show's existing sequences - the safest source of settings keys.

usage: effect_examples.py <EffectName> [max=4] [path-glob ...]
Searches seqs/*/*.xsq, Seqs_Misc/*/*.xsq and Sequences/*.xsq by default (or the globs you give, relative to the show
folder) and prints distinct settings strings for that effect: which sequence, which model, how long, then the
EffectDB string. Copy keys from here instead of guessing them - a wrong key is silently ignored by xLights.

  ./run effect_examples.py Butterfly
  ./run effect_examples.py Shader 10 'Seqs_Misc/*/*.xsq'
"""
import glob, os, sys
import xml.etree.ElementTree as ET
from pathlib import Path

SHOW = Path(os.environ.get('XLIGHTS_SHOW', Path(__file__).resolve().parent.parent))
args = [a for a in sys.argv[1:]]
want = args[0]
limit = int(args[1]) if len(args) > 1 and args[1].isdigit() else 4
pats = [a for a in args[1:] if not a.isdigit()] or ['seqs/*/*.xsq', 'seqs/*/*/*.xsq', 'Seqs_Misc/*/*.xsq',
                                                       'Sequences/*.xsq']
seen, found = set(), 0
for pat in pats:
    for f in sorted(glob.glob(str(SHOW / pat))):
        try:
            r = ET.parse(f).getroot()
        except ET.ParseError:
            continue
        db = [e.text or '' for e in r.find('EffectDB')] if r.find('EffectDB') is not None else []
        for el in r.iter('Element'):
            for lay in el.iter('EffectLayer'):
                for e in lay:
                    if e.get('name') != want or e.get('ref') is None: continue
                    s = db[int(e.get('ref'))]
                    if s in seen: continue
                    seen.add(s); found += 1
                    print(f'{Path(f).relative_to(SHOW)}  [{el.get("name")}]  {int(e.get("endTime")) - int(e.get("startTime"))} ms')
                    print(f'    {s}\n')
                    if found >= limit: sys.exit()
if not found: print(f'no {want} effects found under {SHOW} ({", ".join(pats)})')
