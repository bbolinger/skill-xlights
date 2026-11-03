"""Drive the running xLights through its automation API: open a sequence, render it, save it (the save is what
writes the .fseq), close it. Then read the render back with snap.py instead of asking the user what it looked like.
Read reference/pipeline.md, "Render, save, read back", before using this.

usage:  ./run xl.py status                        which show folder xLights has loaded, and what is open
        ./run xl.py open ../seqs/<song>/<name>.xsq
        ./run xl.py render                        ONE renderAll; nothing may touch the sequence while it runs
        ./run xl.py save                          saveSequence (xLights 2026.17+), then wait for the .fseq to settle
        ./run xl.py close [--discard]             refuses while <name>.xbkp is newer than the .xsq (unsaved edits)

One-time setup in xLights: Preferences -> Output -> API Port -> Port A (49913). Or start xLights with -a.
xLights binds that port on every interface (its wxIPV4address is left at INADDR_ANY), so an agent on another machine
can reach it over the LAN if the xLights machine's firewall lets the connection in: set XLIGHTS_HOST=<that machine>
(default 127.0.0.1), and XLIGHTS_PORT=49914 if you picked Port B. Paths sent to xLights are rewritten from the show
folder here (SHOW) to the show folder as xLights sees it (MEDIA_ROOT in show_config.py), the same mapping the media
paths already use, and paths xLights reports are mapped back. The .fseq and .xbkp checks read THIS machine's copy of
the show folder, so a synced folder has to have caught up first.

Rules, each paid for with a crash or a lost evening on the show this was built on. xl.py enforces them:
- GPU rendering OFF in xLights (Preferences; the setting is `xLightsGPURendering`). Metal shader effects (Fire)
  hung the machine under automation: nine GPU resets in one morning.
- ONE render at a time, and nothing touches the sequence while it runs. A close, open or checkSequence queued under
  a live render is what took the GPU down (four resets in 90 s); a lone renderAll on a warm cache is fine. The lock
  file enforces it: open, close and save refuse while a render is in flight, and a second render refuses to start.
- A render does not write the .fseq; a SAVE does, and the API returns while xLights is still writing the file. save
  waits until the file stops growing (2 s stable) before it reports; a read before that sees a black show.
- xLights holds the sequence, and the user's unsaved edits, in memory. A close discards them; autosave writes
  <name>.xbkp, never the .xsq. close refuses while the .xbkp is newer than the .xsq unless you pass --discard.
- The loaded show folder is part of a sequence's identity. Models and groups are per show folder, so open, render or
  save against another loaded show can write every model that layout lacks out of the file. Every write checks
  getShowFolder against MEDIA_ROOT first and refuses on a mismatch.
"""
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path
from seqlib import SHOW, MEDIA_ROOT, cli_args

HOST = os.environ.get('XLIGHTS_HOST', '127.0.0.1')
PORT = int(os.environ.get('XLIGHTS_PORT', '49913'))
URL = f'http://{HOST}:{PORT}/xlDoAutomation'
CACHE = Path(os.environ.get('XLIGHTS_TOOLING_CACHE', Path.home() / '.cache' / 'xlights-tooling'))
LOCK = CACHE / 'render.lock'           # exists while a renderAll is in flight
STALE_LOCK_S = 1200                    # a crash leaves a lock behind; one older than this is ignored


def mmss(seconds):
    m, s = divmod(max(0.0, float(seconds)), 60)
    return f'{int(m)}:{s:04.1f}'


# ---------------------------------------------------------------- paths: this machine <-> the xLights machine
def _norm(p):
    return str(p).replace('\\', '/').rstrip('/')


def there(p):
    """A path on this machine -> the same file as xLights sees it (SHOW -> MEDIA_ROOT)."""
    p = Path(p).resolve()
    try:
        rel = p.relative_to(SHOW.resolve())
    except ValueError:
        return str(p)                                   # outside the show folder: both machines must see it alike
    root = str(MEDIA_ROOT).rstrip('/\\')
    sep = '\\' if '\\' in root else '/'
    return root + sep + sep.join(rel.parts)


def here(p):
    """A path xLights reported -> the same file on this machine (MEDIA_ROOT -> SHOW)."""
    root = _norm(MEDIA_ROOT)
    s = _norm(p)
    if s == root or s.startswith(root + '/'):
        return SHOW / s[len(root):].lstrip('/')
    return Path(str(p))


def same_show(folder):
    """Is the show folder xLights reports this show (MEDIA_ROOT)?"""
    a, b = Path(str(folder)), Path(str(MEDIA_ROOT))
    if a.exists() and b.exists():
        return a.resolve() == b.resolve()
    return _norm(a) == _norm(b)


# ---------------------------------------------------------------- the API
def call(cmd, timeout=600):
    req = urllib.request.Request(URL, data=json.dumps(cmd).encode(), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode()
    except urllib.error.HTTPError as e:
        # xLights answers 503 with a JSON body that says why ("Sequence not open."); report it as is
        try:
            msg = json.loads(e.read().decode()).get('msg', '')
        except Exception:
            msg = ''
        if cmd['cmd'] == 'getOpenSequence' and 'not open' in msg.lower():
            return {'res': '200', 'seq': ''}             # a normal state, not an error
        sys.exit(f"xLights answered HTTP {e.code} to {cmd['cmd']}: {msg or '(no message)'}")
    except urllib.error.URLError as e:
        sys.exit(f"xLights automation is not reachable at {HOST}:{PORT} ({e.reason}).\n"
                 "  Is xLights running there? Enable the port once: Preferences -> Output -> API Port -> Port A (49913),\n"
                 "  or start xLights with -a. From another machine set XLIGHTS_HOST and open the port in its firewall.")
    try:
        res = json.loads(body)
    except json.JSONDecodeError:
        res = {'raw': body}
    if str(res.get('res', '200')) != '200':
        hint = ' (saveSequence needs xLights 2026.17 or newer)' if cmd['cmd'] == 'saveSequence' else ''
        sys.exit(f"xLights refused {cmd['cmd']}: {res}{hint}")
    return res


def show_folder():
    return call({'cmd': 'getShowFolder'}).get('folder', '')


def assert_show(what):
    folder = show_folder()
    if not same_show(folder):
        sys.exit(f"REFUSING {what}: xLights has the show folder {folder!r} loaded, but this show is {str(MEDIA_ROOT)!r} "
                 "(MEDIA_ROOT).\n  Models and groups are per show folder; rendering or saving across layouts can drop "
                 f"every model the other layout lacks.\n  In xLights: File -> Select Show Folder -> {MEDIA_ROOT}, then re-run.")


# ---------------------------------------------------------------- the render lock
def rendering():
    if not LOCK.exists():
        return False
    if time.time() - LOCK.stat().st_mtime > STALE_LOCK_S:
        LOCK.unlink(missing_ok=True)
        return False
    return True


def guard(what):
    if rendering():
        sys.exit(f"REFUSING {what}: a render is in flight ({LOCK}). Nothing may touch the sequence while it runs; "
                 "wait for it to return.")


# ---------------------------------------------------------------- commands
def status():
    folder = show_folder()
    note = '' if same_show(folder) else f'   (NOT this show: MEDIA_ROOT is {MEDIA_ROOT})'
    print(f'show folder: {folder}{note}')
    r = call({'cmd': 'getOpenSequence'})
    if r.get('seq'):
        print(f"open: {r.get('fullseq') or r.get('seq')}   media: {Path(str(r.get('media', ''))).name}   "
              f"length {mmss(float(r.get('len', 0)) / 1000)}")
    else:
        print('no sequence open')
    return r


def open_(xsq):
    guard('loadSequence')
    assert_show('loadSequence')
    p = Path(xsq)
    if not p.exists():
        sys.exit(f'{xsq}: no such file on this machine')
    target = there(p)
    r = call({'cmd': 'loadSequence', 'seq': target, 'promptIssues': 'false'})
    print(f"opened {target}: {r.get('msg', r)}")


def render():
    if rendering():
        sys.exit('REFUSING renderAll: a render is already in flight. Two renders queued together is the failure; '
                 'wait for the first to return.')
    st = call({'cmd': 'getOpenSequence'})
    if st.get('fullseq'):
        assert_show('renderAll')
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(str(time.time()))
    try:
        t0 = time.time()
        r = call({'cmd': 'renderAll'}, timeout=1800)
        print(f"renderAll returned after {time.time() - t0:.1f} s: {r.get('msg', r)}")
    finally:
        LOCK.unlink(missing_ok=True)


def settle(fseq, before_mtime, appear_s=30.0, stable_s=2.0, cap_s=120.0, poll_s=0.5):
    """Block until the .fseq stops growing: done when its size has been unchanged for `stable_s` AFTER its mtime
    moved past `before_mtime` (so an old, untouched file is not mistaken for a finished write). Gives up if no
    write shows within `appear_s` (a synced folder may need longer), or after `cap_s`.
    Returns (size_bytes, elapsed_s, note); note is '' when it settled cleanly."""
    t0 = time.time(); last = None; since = t0
    while True:
        now = time.time()
        st = fseq.stat() if fseq.exists() else None
        if st is not None and st.st_mtime > before_mtime:
            if st.st_size != last:
                last, since = st.st_size, now
            elif now - since >= stable_s:
                return last, now - t0, ''
        elif now - t0 >= appear_s:
            return (st.st_size if st else 0), now - t0, \
                f"{fseq.name} {'never appeared' if st is None else 'was not rewritten'} within {appear_s:.0f} s"
        if now - t0 >= cap_s:
            return (last or 0), now - t0, f'still growing after {cap_s:.0f} s: do not read it yet'
        time.sleep(poll_s)


def save(timeout=180):
    guard('saveSequence')
    st = call({'cmd': 'getOpenSequence'})
    if not st.get('fullseq'):
        sys.exit('REFUSING save: xLights has no sequence open.')
    assert_show('saveSequence')
    fseq = here(st['fullseq']).with_suffix('.fseq')
    before = fseq.stat().st_mtime if fseq.exists() else 0
    t0 = time.time()
    r = call({'cmd': 'saveSequence'}, timeout=timeout)
    t_api = time.time() - t0
    size, waited, note = settle(fseq, before)
    if fseq.exists() and fseq.stat().st_mtime > before:
        print(f"saved via API in {t_api:.1f} s: {r.get('msg', r)}  -> {fseq.name} {size / 1e6:.1f} MB, "
              f"settled after {waited:.1f} s" + (f' ({note})' if note else ''))
    else:
        print(f"saveSequence returned {r.get('msg', r)} in {t_api:.1f} s but {fseq} did not change after "
              f"{waited:.1f} s ({note or 'no write seen'}). An unrendered sequence saves only the .xsq (render "
              "first), or a synced folder has not caught up. Do not read the .fseq as if it were new.")
    return r


def close(discard=False):
    guard('closeSequence')
    if not discard:
        st = call({'cmd': 'getOpenSequence'})
        if st.get('fullseq'):
            seq = here(st['fullseq']); bk = seq.with_suffix('.xbkp')
            if seq.exists() and bk.exists() and bk.stat().st_mtime > seq.stat().st_mtime + 1:
                hm = lambda p: time.strftime('%H:%M:%S', time.localtime(p.stat().st_mtime))
                sys.exit(f"REFUSING close: {bk.name} (autosave {hm(bk)}) is newer than {seq.name} (saved {hm(seq)}): "
                         "xLights holds UNSAVED edits, probably the user's. `xl.py save` first, or "
                         "`xl.py close --discard` to throw them away.")
    r = call({'cmd': 'closeSequence', 'quiet': 'true', 'force': 'true'})
    print(f"closed: {r.get('msg', r)}")


def main():
    args = cli_args()
    cmd = args[0] if args else ''
    if cmd == 'status': status()
    elif cmd == 'open' and len(args) == 2: open_(args[1])
    elif cmd == 'render': render()
    elif cmd == 'save': save()
    elif cmd == 'close': close(discard='--discard' in sys.argv)
    else: sys.exit(__doc__.split('\n\n')[1])


if __name__ == '__main__':
    main()
