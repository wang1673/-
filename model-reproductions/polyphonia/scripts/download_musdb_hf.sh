#!/usr/bin/env bash
set -euo pipefail
source /home/featurize/work/polyphonia_repro/scripts/env.sh
export HF_HUB_DOWNLOAD_TIMEOUT=120
export HF_HUB_ETAG_TIMEOUT=30
trap 'rc=$?; echo "$rc" > "$POLYPHONIA_ROOT/logs/musdb-hf.exit"; cp "$POLYPHONIA_RUNTIME/logs/musdb-hf.log" "$POLYPHONIA_ROOT/logs/musdb-hf.log"' EXIT
python -m pip install pyarrow==15.0.2
python "$POLYPHONIA_ROOT/scripts/download_musdb_hf.py"
python -m pip check
python -m pip freeze > "$POLYPHONIA_ROOT/logs/environment.freeze.txt"
