"""The channel layout of a show, read from its own files. Read-only.

`Layout(show_folder)` reads `xlights_rgbeffects.xml` and `xlights_networks.xml` and answers, for every model, its
absolute 1-based start channel, its channels per node (stride), and the node list of each submodel; for every group,
what it expands to. Every render reader needs this before it can decode an `.fseq` at the right bytes.

    lay = Layout(SHOW)
    lay.start["Arch 1"]         -> 3937            absolute 1-based start channel
    lay.stride["Arch 1"]        -> 3               4 for an "RGBW Nodes" model
    lay.subnodes["Arch 1"]      -> {"left": [1, 2, 3], ...}   1-based nodes per submodel
    lay.expand("AllModels")     -> {"Arch 1", ...}            the concrete models a group reaches
    lay.bases                   -> {"Controller A": 1, "Controller B": 2560, ...}

Two facts this encodes:
- Controller bases come from THIS show's `xlights_networks.xml`, in definition order, never from a table typed in
  once: a table goes stale the day a controller loses a port or a prop is added, and every render read through it
  decodes three props off by hundreds of channels while still looking plausible.
- A `StartChannel` of the form `!Controller:offset` is controller-relative; the absolute channel is
  `base + offset - 1`. A bare number is an xLights-assigned "No Controller" channel and is taken as is. The byte
  index into a decoded frame is the absolute channel MINUS ONE; `fseq.rgb()` does that subtraction, so never do it
  twice.
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def show_folder_of(p):
    """The show folder above `p`: the first parent holding `xlights_rgbeffects.xml`, or None."""
    p = Path(p).resolve()
    for d in [p, *p.parents]:
        if (d / "xlights_rgbeffects.xml").exists():
            return d
    return None


def bases_from_network(show):
    """Controller name -> absolute 1-based base channel, from the show's xlights_networks.xml in definition order."""
    bases, base = {}, 1
    for c in ET.parse(Path(show) / "xlights_networks.xml").getroot().findall("Controller"):
        bases[c.get("Name")] = base
        base += sum(int(n.get("MaxChannels", "0")) for n in c.findall("network"))
    return bases


def _nodes(sm):
    """1-based node list of a <subModel>: every `lineN` attribute, ranges `a-b` expanded."""
    out = set()
    for k, v in sm.attrib.items():
        if not re.fullmatch(r"line\d+", k): continue
        for t in (v or "").split(","):
            t = t.strip()
            if not t: continue
            if "-" in t:
                a, b = t.split("-", 1)
                try: a, b = int(a), int(b)
                except ValueError: continue
                lo, hi = (a, b) if a <= b else (b, a); out.update(range(lo, hi + 1))
            else:
                try: out.add(int(t))
                except ValueError: pass
    return sorted(out)


class Layout:
    def __init__(self, show):
        show = Path(show)
        r = ET.parse(show / "xlights_rgbeffects.xml").getroot()
        self.groups = {g.get("name"): [m.strip() for m in (g.get("models") or "").split(",") if m.strip()]
                       for g in r.iter("modelGroup")}
        self._cache = {}
        self.bases = bases_from_network(show)
        self.start, self.subnodes, self.stride = {}, {}, {}
        for m in r.iter("model"):
            sc = m.get("StartChannel") or ""
            if sc.startswith("!") and ":" in sc:
                ctl, off = sc[1:].rsplit(":", 1)
                if ctl in self.bases and off.isdigit():
                    self.start[m.get("name")] = self.bases[ctl] + int(off) - 1
            elif sc.isdigit():                    # No Controller: xLights' own number
                self.start[m.get("name")] = int(sc)
            self.subnodes[m.get("name")] = {x.get("name"): _nodes(x) for x in m.findall("subModel")}
            # channels per node: an "RGBW Nodes" model is 4 per node, so a 3-stride read lands on the wrong
            # pixel from node 2 onward
            self.stride[m.get("name")] = 4 if "RGBW" in (m.get("StringType") or "") else 3

    def expand(self, name, seen=None):
        """Resolve a group (or model) to the set of concrete model names it reaches. Checking a group by NAME
        cannot tell you what it touches; only expansion can."""
        if name in self._cache: return self._cache[name]
        seen = seen or set()
        if name in seen: return set()
        seen = seen | {name}
        if name in self.groups:
            out = set()
            for m in self.groups[name]:
                out |= self.expand(m, seen)
        else:
            out = {name}
        if not seen - {name}: self._cache[name] = out
        return out
