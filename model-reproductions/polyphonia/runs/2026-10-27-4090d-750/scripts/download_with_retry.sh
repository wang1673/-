#!/usr/bin/env bash
set -u
root=/root/autodl-tmp/polyphonia_repro
python=/root/autodl-tmp/polyphonia/runtime/env/bin/python
script="$1"
for attempt in $(seq 1 8); do
  echo "Attempt $attempt: $script"
  "$python" "$root/scripts/$script"
  rc=$?
  if test "$rc" -eq 0; then echo 0 > "$root/logs/$script.exit"; exit 0; fi
  echo "Download exited $rc; retaining verified files and retrying"
  sleep 45
done
echo "$rc" > "$root/logs/$script.exit"
exit "$rc"
