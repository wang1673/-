"""Full-mixture HT-Demucs separation, then deterministic center crop. No oracle stems."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import time
import numpy as np
import soundfile as sf
import torch
from demucs.apply import apply_model
from demucs.pretrained import get_model

parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, required=True)
args = parser.parse_args()
root = Path(os.environ['POLYPHONIA_ROOT'])
run = root / 'results/musdb_center10_htdemucs_01'
protocol = json.loads((run/'protocol.json').read_text())
track = protocol['tracks'][args.index]
out = Path(protocol['prepared_root']) / track['track']
meta = out / 'preparation.json'
if meta.exists():
    record = json.loads(meta.read_text())
    for name, digest in record['sha256'].items():
        assert hashlib.sha256((out/name).read_bytes()).hexdigest() == digest
    print('Verified prepared track:', track['track'], flush=True)
    raise SystemExit(0)
out.mkdir(parents=True, exist_ok=True)
random.seed(928)
np.random.seed(928)
torch.manual_seed(928)
torch.cuda.manual_seed_all(928)
start_time = time.monotonic()
model = get_model('htdemucs')
model.eval()
audio, sr = sf.read(track['mixture'], dtype='float32', always_2d=True)
assert sr == model.samplerate == 44100 and audio.shape[1] == model.audio_channels == 2
wav = torch.from_numpy(audio.T.copy())
ref = wav.mean(0)
mean, std = ref.mean(), ref.std()
assert std > 1e-8
with torch.inference_mode():
    sources = apply_model(model, ((wav-mean)/std)[None], device='cuda', shifts=1,
                          split=True, overlap=0.25, progress=True, num_workers=0)[0]
    sources = sources * std + mean
start = track['start_frame']
stop = start + track['frames']
assert stop <= audio.shape[0]
sf.write(str(out/'mixture.wav'), audio[start:stop], sr, subtype='PCM_16')
for name, source in zip(model.sources, sources):
    crop = source[:, start:stop].cpu().numpy().T
    assert crop.shape == (441000, 2) and np.isfinite(crop).all()
    sf.write(str(out/(name+'.wav')), crop, sr, subtype='FLOAT')
shutil.copyfile(track['prompt_file'], out/'prompt_multi.json')
record = {'track': track['track'], 'model': 'htdemucs', 'demucs_version': '4.0.1',
          'input': track['mixture'], 'source': 'estimated from full mixture; not dataset ground-truth stems',
          'shifts': 1, 'overlap': 0.25, 'seed': 928, 'samplerate': sr,
          'start_frame': start, 'frames': track['frames'], 'seconds': 10,
          'elapsed_seconds': time.monotonic()-start_time,
          'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in out.iterdir() if p.suffix in ('.wav', '.json')}}
meta.write_text(json.dumps(record, indent=2))
print(json.dumps(record, indent=2), flush=True)
