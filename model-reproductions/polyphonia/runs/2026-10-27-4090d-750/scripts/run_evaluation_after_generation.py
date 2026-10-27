"""Evaluate the current user-selected stage after generation pauses or completes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root=Path(os.environ['POLYPHONIA_ROOT'])
run=root/'results/musdb_center10_htdemucs_4090d_01'
state_path=run/'pipeline.json'
started=time.monotonic()

def state(value,**extra):
    record={'state':value,'elapsed_seconds':time.monotonic()-started,**extra}
    tmp=state_path.with_suffix('.json.tmp');tmp.write_text(json.dumps(record,indent=2));tmp.replace(state_path)

state('waiting_for_generation',requested_tasks=json.loads((run/'control.json').read_text())['max_tasks'])
try:
    while True:
        generation=json.loads((run/'status.json').read_text())
        if generation['state']=='failed':raise RuntimeError('Generation failed: '+generation.get('error',''))
        if generation['state'] in ['generation_completed','paused_at_task_limit']:
            count=generation['validated_tasks']
            assert count==json.loads((run/'control.json').read_text())['max_tasks']
            break
        time.sleep(10)
    state('evaluating',generated_tasks=count)
    live=Path('/root/autodl-tmp/polyphonia/runtime/logs/musdb_center10_htdemucs_4090d_01/evaluation-first{}.log'.format(count))
    command=[sys.executable,str(root/'scripts/evaluate_benchmark.py'),'--device','cuda']
    if count<750:command+=['--available-only','--limit',str(count)]
    with live.open('a') as log:
        subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    summary_path=run/'metrics'/('summary.json' if count==750 else 'summary.partial.json')
    summary=json.loads(summary_path.read_text())
    assert summary['evaluated_tasks']==count
    (run/'logs'/live.name).write_bytes(live.read_bytes())
    if count<750:
        (run/'metrics'/('summary.first{}.json'.format(count))).write_bytes(summary_path.read_bytes())
        subprocess.run([sys.executable,str(root/'scripts/export_stage_review.py'),'--limit',str(count)],check=True)
        state('stage_completed_remaining_paused',generated_tasks=count,evaluated_tasks=count,
              remaining_tasks=750-count,summary=str(run/'metrics'/('summary.first{}.json'.format(count))))
    else:
        subprocess.run([sys.executable,str(root/'scripts/export_benchmark.py')],check=True)
        state('completed',generated_tasks=750,evaluated_tasks=750,summary=str(summary_path))
except BaseException as exc:
    state('failed',error=repr(exc));raise
