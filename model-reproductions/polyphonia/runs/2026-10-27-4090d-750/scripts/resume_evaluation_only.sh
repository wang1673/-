#!/usr/bin/env bash
set -euo pipefail
source /root/autodl-tmp/polyphonia_repro/scripts/env.sh
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_ENDPOINT=https://hf-mirror.com
export XDG_CACHE_HOME="$POLYPHONIA_RUNTIME/xdg-cache" CUDA_CACHE_PATH="$POLYPHONIA_RUNTIME/cuda-cache"
run="$POLYPHONIA_ROOT/results/musdb_center10_htdemucs_4090d_01"
mkdir -p "$run/history/evaluation-tokenizer-repair"
for file in pipeline.json full-pipeline.exit; do
 if test -f "$run/$file"; then cp -n "$run/$file" "$run/history/evaluation-tokenizer-repair/$file"; fi
done
rm -f "$run/full-pipeline.exit"
trap 'rc=$?; echo "$rc" > "$run/full-pipeline.exit"' EXIT
cd "$POLYPHONIA_ROOT/polyphonia"
python -c 'import laion_clap; print("Offline CLAP import passed",flush=True)'
python "$POLYPHONIA_ROOT/scripts/run_evaluation_after_generation.py"
python "$POLYPHONIA_ROOT/scripts/verify_full_run.py"
echo 'EVALUATION AND FINAL AUDIT COMPLETE'
