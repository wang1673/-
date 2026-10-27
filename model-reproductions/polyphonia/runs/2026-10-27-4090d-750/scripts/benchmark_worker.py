"""Execute the unmodified official script, instrumenting output validation only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import random
import sys
import time
import numpy as np
import soundfile as sf
import torch

parser = argparse.ArgumentParser()
parser.add_argument('--index', type=int, required=True)
parser.add_argument('--task-limit', type=int, default=15)
parser.add_argument('--plan-only', action='store_true')
args = parser.parse_args()
root = Path(os.environ['POLYPHONIA_ROOT'])
run = root/'results/musdb_center10_htdemucs_4090d_01'
protocol = json.loads((run/'protocol.json').read_text())
track = protocol['tracks'][args.index]
assert 1 <= args.task_limit <= 15
all_tasks = list(track['tasks'])
track['tasks'] = all_tasks[:args.task_limit]
if args.plan_only:
    print(json.dumps({'track': track['track'], 'selected_tasks': track['tasks'],
                      'selected_count': len(track['tasks']), 'track_total_tasks': len(all_tasks)}))
    raise SystemExit(0)
sample = Path(protocol['prepared_root']) / track['track']
out = run/'audio'/track['track']
out.mkdir(parents=True, exist_ok=True)
repo = root/'polyphonia'
sys.path.insert(0, str(repo))
import run_sample_exp as official
original_parse = official.parse_prompt_file
def selected_parse(*positional, **keyword):
    tasks = original_parse(*positional, **keyword)
    return {name: tasks[name] for name in track['tasks']}
official.parse_prompt_file = selected_parse

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
status['selected_tasks'] = track['tasks']
status['track_total_tasks'] = len(all_tasks)
rng_path = Path(os.environ['POLYPHONIA_RUNTIME'])/'rng-musdb_center10_htdemucs_4090d_01'/track['track']/'last.pt'
rng_path.parent.mkdir(parents=True, exist_ok=True)
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
    checkpoint = {'last_task': path.stem, 'audio_sha256': status['files'][path.stem]['sha256'],
                  'python': random.getstate(), 'numpy': np.random.get_state(),
                  'torch': torch.get_rng_state(), 'cuda': torch.cuda.get_rng_state_all()}
    temp = rng_path.with_suffix('.tmp')
    torch.save(checkpoint, temp)
    temp.replace(rng_path)
    save_status()

# Restore the random stream immediately before the first missing task. Re-inversion
# still uses the original seed; completed outputs are never regenerated on resume.
original_prepare = official.prepare_editor
def resumable_prepare(*positional, **keyword):
    editor = original_prepare(*positional, **keyword)
    reverse = editor.reverse_pipeline
    first_call = True
    def resumable_reverse(*args, **kwargs):
        nonlocal first_call
        if first_call:
            first_call = False
            pending = [name for name in track['tasks'] if name not in status['files']]
            if pending and rng_path.exists():
                checkpoint = torch.load(rng_path, map_location='cpu', weights_only=False)
                index = all_tasks.index(pending[0])
                previous = all_tasks[index-1] if index else None
                if previous and checkpoint['last_task'] == previous and status['files'].get(previous, {}).get('sha256') == checkpoint['audio_sha256']:
                    random.setstate(checkpoint['python'])
                    np.random.set_state(checkpoint['numpy'])
                    torch.set_rng_state(checkpoint['torch'])
                    torch.cuda.set_rng_state_all(checkpoint['cuda'])
                    status['rng_restored_after'] = previous
        return reverse(*args, **kwargs)
    editor.reverse_pipeline = resumable_reverse
    return editor
official.prepare_editor = resumable_prepare

official.save_audio_safe = checked_save
torch.cuda.reset_peak_memory_stats()
sys.argv = ['run_sample_exp.py', '--sample_dir', str(sample), '--output_dir', str(out),
            '--device', 'cuda', '--precision', 'fp16', '--seed', '928', '--mask_type', 'energy']
status['argv'] = list(sys.argv)
save_status()
try:
    official.main()
    status['files'] = {task: validate(out/(task+'.wav')) for task in track['tasks']}
    assert len(status['files']) == args.task_limit
    status['state'] = 'completed' if args.task_limit == 15 else 'completed_subset'
except BaseException as exc:
    status['state'] = 'failed'
    status['error'] = repr(exc)
    raise
finally:
    save_status()
    print(json.dumps({k:v for k,v in status.items() if k!='files'}, indent=2), flush=True)
