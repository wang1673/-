"""Execute the unmodified official script, instrumenting output validation only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import time
import numpy as np
import soundfile as sf
import torch

parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, required=True)
args = parser.parse_args()
root = Path(os.environ['POLYPHONIA_ROOT'])
run = root/'results/musdb_center10_htdemucs_01'
protocol = json.loads((run/'protocol.json').read_text())
track = protocol['tracks'][args.index]
sample = Path(protocol['prepared_root']) / track['track']
out = run/'audio'/track['track']
out.mkdir(parents=True, exist_ok=True)
repo = root/'polyphonia'
sys.path.insert(0, str(repo))
import run_sample_exp as official

def validate(path):
    audio, sr = sf.read(str(path), dtype='float32')
    assert sr == 16000 and audio.ndim == 1 and len(audio) == 160000, (str(path), sr, audio.shape)
    assert np.isfinite(audio).all()
    rms = float(np.sqrt(np.mean(audio.astype('float64')**2)))
    assert rms > 1e-6, ('Silent output', str(path))
    return {'frames': len(audio), 'sample_rate': sr, 'rms': rms,
            'peak': float(np.max(np.abs(audio))),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

# Avoid the official file-size-only skip accepting corrupt interrupted files.
for task in track['tasks']:
    path = out/(task+'.wav')
    if path.exists():
        try:
            validate(path)
        except Exception:
            rejected = out/'rejected'
            rejected.mkdir(exist_ok=True)
            path.rename(rejected/(task+'.'+str(time.time_ns())+'.wav'))

original_save = official.save_audio_safe
start_time = time.monotonic()
status_path = out/'validation.json'
status = {'track': track['track'], 'state': 'running', 'files': {}, 'seed': 928}
for task in track['tasks']:
    path = out/(task+'.wav')
    if path.exists():
        status['files'][task] = validate(path)

def save_status():
    status['elapsed_seconds'] = time.monotonic()-start_time
    status['validated_tasks'] = len(status['files'])
    status['peak_cuda_allocated_gib'] = torch.cuda.max_memory_allocated()/1024**3
    status['peak_cuda_reserved_gib'] = torch.cuda.max_memory_reserved()/1024**3
    tmp = status_path.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(status, indent=2))
    tmp.replace(status_path)

def checked_save(path, audio_np, sr=16000):
    original_save(path, audio_np, sr)
    status['files'][path.stem] = validate(path)
    save_status()

official.save_audio_safe = checked_save
torch.cuda.reset_peak_memory_stats()
sys.argv = ['run_sample_exp.py', '--sample_dir', str(sample), '--output_dir', str(out),
            '--device', 'cuda', '--precision', 'fp16', '--seed', '928', '--mask_type', 'energy']
status['argv'] = list(sys.argv)
save_status()
try:
    official.main()
    status['files'] = {task: validate(out/(task+'.wav')) for task in track['tasks']}
    assert len(status['files']) == 15
    status['state'] = 'completed'
except BaseException as exc:
    status['state'] = 'failed'
    status['error'] = repr(exc)
    raise
finally:
    save_status()
    print(json.dumps({k:v for k,v in status.items() if k!='files'}, indent=2), flush=True)
