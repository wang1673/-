#!/usr/bin/env bash
set -euo pipefail
source /root/autodl-tmp/polyphonia_repro/scripts/env.sh
while ! test -f "$POLYPHONIA_RUNTIME/wheelhouse/numpy-1.23.5-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl" || ! test -f "$POLYPHONIA_RUNTIME/wheelhouse/pyarrow-15.0.2-cp38-cp38-manylinux_2_28_x86_64.whl"; do sleep 10; done
python -m pip install --no-index --no-deps "$POLYPHONIA_RUNTIME/wheelhouse/numpy-1.23.5-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl" "$POLYPHONIA_RUNTIME/wheelhouse/pyarrow-15.0.2-cp38-cp38-manylinux_2_28_x86_64.whl"
python "$POLYPHONIA_ROOT/scripts/download_data_mirror.py"
