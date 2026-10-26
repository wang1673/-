#!/usr/bin/env bash
set -euo pipefail
source /home/featurize/work/polyphonia_repro/scripts/env.sh
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
cd "$POLYPHONIA_ROOT/polyphonia"
run_id="${1:-smoke_official_01}"
trap 'rc=$?; echo "$rc" > "$POLYPHONIA_ROOT/logs/$run_id.exit"' EXIT
/usr/bin/time -v python "$POLYPHONIA_ROOT/scripts/smoke.py" "$POLYPHONIA_ROOT/results/$run_id"
