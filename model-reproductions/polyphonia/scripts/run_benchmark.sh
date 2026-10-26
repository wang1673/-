#!/usr/bin/env bash
set -euo pipefail
source /home/featurize/work/polyphonia_repro/scripts/env.sh
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export XDG_CACHE_HOME=/home/featurize/data/polyphonia/runtime/xdg-cache
export CUDA_CACHE_PATH=/home/featurize/data/polyphonia/runtime/cuda-cache
run_dir="$POLYPHONIA_ROOT/results/musdb_center10_htdemucs_01"
trap 'rc=$?; echo "$rc" > "$run_dir/controller.exit"; cp "$POLYPHONIA_RUNTIME/logs/musdb_center10_htdemucs_01/controller.log" "$run_dir/controller.log"' EXIT
cd "$POLYPHONIA_ROOT/polyphonia"
python "$POLYPHONIA_ROOT/scripts/benchmark_controller.py"
