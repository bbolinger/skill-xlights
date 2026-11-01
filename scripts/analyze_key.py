"""Estimate a song's key, and where it changes, from the separated stems (Krumhansl key profiles on chroma).

usage: analyze_key.py <song> [window_s=16]
Prints the best key per window and for the whole song. A run of windows in a new key = a modulation (a "lift" -
in practice the biggest emotional moment of a pop song); a minor-key stretch in a major song is usually the
darkest lyric (the pre-chorus "searching in the dark"). Drums are left out of the chroma.
"""
import os, sys
import librosa, numpy as np
from seqlib import cli_args

SONG = cli_args()[0]
WIN = float(cli_args()[1]) if len(cli_args()) > 1 else 16.0
CACHE = os.environ.get('XLIGHTS_TOOLING_CACHE', os.path.expanduser('~/.cache/xlights-tooling'))
D = f'{CACHE}/stems/{SONG}'
y = sum(librosa.load(f'{D}/{s}.wav', sr=22050)[0] for s in ('bass', 'guitar', 'piano', 'other', 'vocals'))
ch = librosa.feature.chroma_cqt(y=y, sr=22050, hop_length=2048)
t = librosa.times_like(ch, sr=22050, hop_length=2048)
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
N = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def key(a, b):
    v = ch[:, (t >= a) & (t < b)].mean(1)
    return max((np.corrcoef(np.roll(m, k), v)[0, 1], N[k] + q) for m, q in ((MAJ, ' major'), (MIN, ' minor'))
               for k in range(12))


print(f'{SONG}: whole song {key(0, t[-1])[1]}  ({key(0, t[-1])[0]:.2f})')
prev = None
for a in np.arange(0, t[-1], WIN):
    r, k = key(a, a + WIN)
    print(f'  {a:6.0f}s  {k:9} {r:.2f}' + ('   <- change' if prev and k != prev else ''))
    prev = k
