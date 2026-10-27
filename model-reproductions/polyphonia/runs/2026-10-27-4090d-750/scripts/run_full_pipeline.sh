#!/usr/bin/env bash
set -euo pipefail
source /root/autodl-tmp/polyphonia_repro/scripts/env.sh
export HF_ENDPOINT=https://hf-mirror.com
export XDG_CACHE_HOME="$POLYPHONIA_RUNTIME/xdg-cache"
export CUDA_CACHE_PATH="$POLYPHONIA_RUNTIME/cuda-cache"
run="$POLYPHONIA_ROOT/results/musdb_center10_htdemucs_4090d_01"
mkdir -p "$run/logs" "$POLYPHONIA_RUNTIME/logs/musdb_center10_htdemucs_4090d_01"
trap 'rc=$?; echo "$rc" > "$run/full-pipeline.exit"' EXIT
echo 'Waiting for exact package downloads'
while ! test -f "$POLYPHONIA_ROOT/logs/packages.ready"; do sleep 15; done
bash "$POLYPHONIA_ROOT/scripts/setup_fresh.sh"
echo 'Waiting for pinned inference models'
while ! test -f "$POLYPHONIA_ROOT/logs/inference.ready"; do sleep 15; done
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
cd "$POLYPHONIA_ROOT/polyphonia"
python - <<'PY'
import json,os
from pathlib import Path
root=Path(os.environ['POLYPHONIA_ROOT']);run=root/'results/musdb_center10_htdemucs_4090d_01'
p=json.loads((run/'protocol.json').read_text());assert json.loads((run/'control.json').read_text())['max_tasks']==750
for t in p['tracks']:
    prompts=json.loads(Path(t['prompt_file']).read_text())
    assert list(prompts)==t['tasks'],t['track']
assert sum(len(t['tasks']) for t in p['tracks'])==750
print('Verified full task order and source paths',flush=True)
PY
python "$POLYPHONIA_ROOT/scripts/benchmark_controller.py" > "$run/logs/controller.log" 2>&1
while ! test -f "$POLYPHONIA_ROOT/logs/models.ready"; do sleep 15; done
python "$POLYPHONIA_ROOT/scripts/run_evaluation_after_generation.py" > "$run/logs/evaluation-pipeline.log" 2>&1
python "$POLYPHONIA_ROOT/scripts/verify_full_run.py" > "$run/logs/final-audit.log" 2>&1
echo 'ALL 750 TASKS AND THREE-METRIC EVALUATION COMPLETE'
