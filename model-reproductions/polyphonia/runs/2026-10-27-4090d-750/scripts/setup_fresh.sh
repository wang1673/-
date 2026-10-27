#!/usr/bin/env bash
set -euo pipefail
source /root/autodl-tmp/polyphonia_repro/scripts/env.sh
mkdir -p "$POLYPHONIA_RUNTIME"/{tmp,pip-cache,huggingface,torch,matplotlib,numba,xdg-cache,cuda-cache}
export XDG_CACHE_HOME="$POLYPHONIA_RUNTIME/xdg-cache"
export CUDA_CACHE_PATH="$POLYPHONIA_RUNTIME/cuda-cache"
trap 'rc=$?; echo "$rc" > "$POLYPHONIA_ROOT/logs/setup.exit"' EXIT
python --version
python -m pip install --disable-pip-version-check --no-index --find-links "$POLYPHONIA_RUNTIME/wheelhouse" --no-build-isolation -r "$POLYPHONIA_ROOT/scripts/full.freeze.txt"
python -m pip check
python -m pip freeze > "$POLYPHONIA_ROOT/logs/environment.freeze.txt"
python - <<'PY'
import torch,torchaudio,torchvision,diffusers,transformers,sys,json
from pathlib import Path
import importlib.metadata as metadata
root=Path('/root/autodl-tmp/polyphonia_repro')
comparison=[]
for line in (root/'scripts/full.freeze.txt').read_text().splitlines():
    if not line.strip():continue
    name,wanted=line.strip().split('==')
    got=metadata.version(name)
    comparison.append({'package':name,'expected':wanted,'actual':got})
    assert got==wanted,(name,wanted,got)
(root/'logs/environment-comparison.json').write_text(json.dumps(comparison,indent=2))
expected={'torch':'2.4.1+cu124','torchaudio':'2.4.1+cu124','torchvision':'0.19.1+cu124','diffusers':'0.32.0','transformers':'4.46.3'}
actual={k:globals()[k].__version__ for k in expected}
assert actual==expected,(actual,expected)
assert sys.version_info[:3]==(3,8,20)
assert torch.cuda.is_available()
x=torch.ones(256,256,device='cuda',dtype=torch.float16)
y=x@x
assert y[0,0].item()==256
info={'python':sys.version,'versions':actual,'gpu':torch.cuda.get_device_name(),'cuda':torch.version.cuda,'fp16_matrix_test':y[0,0].item()}
Path('/root/autodl-tmp/polyphonia_repro/logs/cuda-validation.json').write_text(json.dumps(info,indent=2))
print(info,flush=True)
PY
