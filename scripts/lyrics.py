"""Transcribe the isolated vocal stem with Whisper and keep a timestamp for every word.

usage: lyrics.py <song> [--model=small.en] [--prompt="words, phrases, from the song"] [--no-vad]
  --prompt   vocabulary hint (a few phrases you know are sung); recovers lines Whisper otherwise drops
  --no-vad   keep quiet or heavily processed singing that the voice filter throws away
Writes tooling/songs/<song>/lyrics.json ([{word, start, end, p}]) and lyrics.txt (one line per segment).
The model downloads once into the tooling cache.
"""
import json, os, sys
from faster_whisper import WhisperModel
from seqlib import song_dir, cli_args

opts = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
SONG = cli_args()[0]
CACHE = os.environ.get('XLIGHTS_TOOLING_CACHE', os.path.expanduser('~/.cache/xlights-tooling'))
model = WhisperModel(opts.get('model', 'small.en'), device='cpu', compute_type='int8',
                     download_root=f'{CACHE}/whisper', cpu_threads=os.cpu_count())
segments, _ = model.transcribe(f'{CACHE}/stems/{SONG}/vocals.wav', word_timestamps=True,
                               vad_filter='--no-vad' not in sys.argv, condition_on_previous_text=False, beam_size=5,
                               initial_prompt=opts.get('prompt'), no_speech_threshold=0.9 if 'prompt' in opts else 0.6)
words, lines = [], []
for seg in segments:
    lines.append(f'{seg.start:7.2f}  {seg.text.strip()}')
    for w in seg.words or []:
        words.append(dict(word=w.word.strip(), start=round(w.start, 3), end=round(w.end, 3), p=round(w.probability, 2)))
    print(lines[-1], flush=True)
HERE = song_dir(SONG)
json.dump(words, open(HERE / 'lyrics.json', 'w'), indent=0)
(HERE / 'lyrics.txt').write_text('\n'.join(lines) + '\n')
print(f'{len(words)} words -> {HERE / "lyrics.json"}')
