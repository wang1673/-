"""Part of the current one-off benchmark job; evaluate after generation completes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root=Path(os.environ['POLYPHONIA_ROOT'])
run=root/'results/musdb_center10_htdemucs_01'
state_path=run/'pipeline.json'
started=time.monotonic()

def state(value,**extra):
    record={'state':value,'elapsed_seconds':time.monotonic()-started,**extra}
    tmp=state_path.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(record,indent=2))
    tmp.replace(state_path)

state('waiting_for_generation')
try:
    while True:
        generation=json.loads((run/'status.json').read_text())
        if generation['state']=='failed':
            raise RuntimeError('Generation failed: '+generation.get('error',''))
        if generation['state']=='generation_completed':
            assert generation['validated_tasks']==750
            break
        time.sleep(10)
    state('evaluating',generated_tasks=750)
    live=Path('/home/featurize/data/polyphonia/runtime/logs/musdb_center10_htdemucs_01/evaluation.log')
    with live.open('a') as log:
        subprocess.run([sys.executable,str(root/'scripts/evaluate_benchmark.py'),'--device','cuda'],
                       stdout=log,stderr=subprocess.STDOUT,check=True)
    summary=json.loads((run/'metrics/summary.json').read_text())
    assert summary['state']=='completed' and summary['evaluated_tasks']==750
    (run/'logs/evaluation.log').write_bytes(live.read_bytes())
    subprocess.run([sys.executable,str(root/'scripts/export_benchmark.py')],check=True)
    state('completed',generated_tasks=750,evaluated_tasks=750,summary=str(run/'metrics/summary.json'))
except BaseException as exc:
    state('failed',error=repr(exc))
    raise
