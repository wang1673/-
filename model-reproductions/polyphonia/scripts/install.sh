#!/usr/bin/env bash
set -euo pipefail
source /home/featurize/work/polyphonia_repro/scripts/env.sh
mkdir -p "$POLYPHONIA_RUNTIME"/{tmp,pip-cache,huggingface,torch,matplotlib,numba}
trap 'rc=$?; echo "$rc" > "$POLYPHONIA_ROOT/logs/install.exit"' EXIT
date -Is
if ! test -x "$POLYPHONIA_RUNTIME/env/bin/python"; then
  /environment/miniconda3/bin/conda create -p "$POLYPHONIA_RUNTIME/env" python=3.8.20 pip -y
fi
cd "$POLYPHONIA_ROOT/polyphonia"
python --version
if test -d "$POLYPHONIA_RUNTIME/wheelhouse"; then
  python -m pip install "$POLYPHONIA_RUNTIME/wheelhouse/"*.whl
fi
python - <<'PY'
from pathlib import Path
import os
source = Path('requirements.txt').read_text()
target = Path(os.environ['POLYPHONIA_ROOT']) / 'scripts/requirements.pypi.txt'
target.write_text('\n'.join(line for line in source.splitlines()
                            if not line.startswith('--extra-index-url')) + '\n')
PY
python -m pip install -r "$POLYPHONIA_ROOT/scripts/requirements.pypi.txt"
python -m pip check
python - <<'PY'
import sys
import torch, torchaudio, torchvision, diffusers, transformers
from diffusers import AudioLDM2Pipeline
print('Python:', sys.version)
print('torch:', torch.__version__, 'CUDA:', torch.version.cuda)
assert torch.cuda.is_available(), 'CUDA unavailable'
print('GPU:', torch.cuda.get_device_name(0))
print('GPU calculation:', (torch.ones(4, device='cuda') * 2).tolist())
print('torchaudio:', torchaudio.__version__)
print('torchvision:', torchvision.__version__)
print('diffusers:', diffusers.__version__)
print('transformers:', transformers.__version__)
import run_sample_exp
print('Official entry point import OK')
PY
python -m pip freeze > "$POLYPHONIA_ROOT/logs/environment.freeze.txt"
git rev-parse HEAD > "$POLYPHONIA_ROOT/logs/code.commit.txt"
date -Is
