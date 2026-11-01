"""Measure how vivid a sequence is, per row: brightness x time, coverage, average colour saturation, and time spent
in muddy gradients (two saturated colours whose midpoint is dark/olive, e.g. red -> green).

usage: color_check.py <a.xsq> [b.xsq ...]   - compare against a sequence the user called vivid
"""
import sys, re, colorsys, xml.etree.ElementTree as ET
def stats(path, rows=('arches_big','Verts','trees','pix-evens','Spiral Trees','fenceline','roofline-1','AllModels')):
    r = ET.parse(path).getroot()
    pals = []
    for p in r.find('ColorPalettes'):
        kv = dict(x.split('=',1) for x in (p.text or '').split(','))
        cols = []
        for k,v in kv.items():
            if k.startswith('C_BUTTON_Palette'):
                cols += re.findall(r'#[0-9a-fA-F]{6}', v)
        bright = int(kv.get('C_SLIDER_Brightness', 100))
        sats, vals, mud = [], [], 0
        for c in cols:
            rr,gg,bb = (int(c[i:i+2],16)/255 for i in (1,3,5))
            h,s,v = colorsys.rgb_to_hsv(rr,gg,bb); sats.append(s); vals.append(v)
        grad = [re.findall(r'#[0-9a-fA-F]{6}', v) for k,v in kv.items() if k.startswith('C_BUTTON') and 'Values' in v]
        for g in grad:
            for a,b in zip(g, g[1:]):
                A=[int(a[i:i+2],16) for i in (1,3,5)]; Bc=[int(b[i:i+2],16) for i in (1,3,5)]
                m=[(x+y)/2/255 for x,y in zip(A,Bc)]; h,s,v=colorsys.rgb_to_hsv(*m)
                if v < 0.6 and s > 0.3: mud += 1
        pals.append((bright, sum(sats)/len(sats) if sats else 0, mud))
    db = [e.text or '' for e in r.find('EffectDB')]
    out = {}
    dur = float(r.find('head/sequenceDuration').text)
    for el in r.find('ElementEffects'):
        n = el.get('name')
        if n not in rows: continue
        tot, lit, sat, mud = 0, 0, 0, 0
        for L in el.findall('EffectLayer'):
            for e in L.findall('Effect'):
                d = (int(e.get('endTime'))-int(e.get('startTime')))/1000
                b, s, m = pals[int(e.get('palette'))]
                st = db[int(e.get('ref'))]
                a1 = re.search(r'Eff_On_Start=(\d+)', st); a2 = re.search(r'Eff_On_End=(\d+)', st)
                lvl = ((int(a1.group(1)) + int(a2.group(1)))/2 if a1 else 100)/100
                tot += d * b/100 * lvl; lit += d; sat += d*s; mud += m*d
        out[n] = (round(tot/dur,2), round(lit/dur,2), round(sat/max(lit,1e-9),2), round(mud/dur,2))
    return out
for p in sys.argv[1:]:
    print(p.split('/')[-1]); 
    for k,v in stats(p).items(): print(f'   {k:13} bright·time {v[0]:5}  coverage {v[1]:5}  sat {v[2]:4}  muddy-grad·time {v[3]}')
