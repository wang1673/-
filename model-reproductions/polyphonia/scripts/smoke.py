import json
import os
from pathlib import Path
import runpy
import sys
import time
import numpy as np
import soundfile as sf
import torch

root = Path(os.environ['POLYPHONIA_ROOT'])
repo = root / 'polyphonia'
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=False)
sys.path.insert(0, str(repo))
sys.argv = [str(repo / 'run_sample_exp.py'), '--sample_dir', str(repo / 'sample'),
            '--output_dir', str(out), '--task_key', 'vocals2violin',
            '--device', 'cuda', '--precision', 'fp16', '--seed', '928',
            '--mask_type', 'energy', '--visualize']
torch.cuda.reset_peak_memory_stats()
start = time.monotonic()
status = {'success': False, 'command_argv': list(sys.argv)}
try:
    runpy.run_path(str(repo / 'run_sample_exp.py'), run_name='__main__')
    audio, sr = sf.read(str(out / 'vocals2violin.wav'))
    assert sr == 16000, sr
    assert len(audio) > 0 and np.isfinite(audio).all()
    assert np.sqrt(np.mean(audio**2)) > 1e-6, 'Silent output'
    assert (out / 'vocals2violin.png').stat().st_size > 1000
    original, _ = sf.read(str(repo / 'sample/mixture.wav'))
    status.update(success=True, sample_rate=sr, frames=len(audio),
                  duration_seconds=len(audio)/sr, peak=float(np.max(np.abs(audio))),
                  rms=float(np.sqrt(np.mean(audio**2))))
finally:
    status['elapsed_seconds'] = time.monotonic() - start
    status['peak_cuda_allocated_gib'] = torch.cuda.max_memory_allocated()/1024**3
    status['peak_cuda_reserved_gib'] = torch.cuda.max_memory_reserved()/1024**3
    (out / 'validation.json').write_text(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2), flush=True)
