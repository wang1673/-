"""Resumable 50-track/750-task controller; all artifacts are under data/work."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root=Path(os.environ['POLYPHONIA_ROOT'])
run=root/'results/musdb_center10_htdemucs_01'
protocol=json.loads((run/'protocol.json').read_text())
status={'state':'running','protocol':str(run/'protocol.json'),'tracks':[], 'total_tasks':750,
        'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
started=time.monotonic()

def persist():
    status['elapsed_seconds']=time.monotonic()-started
    status['validated_tasks']=sum(x.get('validated_tasks',0) for x in status['tracks'])
    tmp=run/'status.json.tmp'
    tmp.write_text(json.dumps(status,indent=2))
    tmp.replace(run/'status.json')

try:
    persist()
    for i,track in enumerate(protocol['tracks']):
        name=track['track']
        item={'index':i,'track':name,'state':'preparing','validated_tasks':0}
        status['tracks'].append(item)
        persist()
        for script,stage in [('prepare_benchmark.py','separating'),('benchmark_worker.py','editing')]:
            validation=run/'audio'/name/'validation.json'
            if script=='benchmark_worker.py' and validation.exists():
                old=json.loads(validation.read_text())
                if old.get('state')=='completed' and old.get('validated_tasks')==15:
                    # Worker revalidates existing files before accepting them on a resume.
                    pass
            item['state']=stage
            persist()
            log=Path(protocol['live_logs'])/('{:02d}-{}.log'.format(i,stage))
            log.parent.mkdir(parents=True,exist_ok=True)
            print('START',i,name,stage,flush=True)
            with log.open('a') as stream:
                child=subprocess.Popen([sys.executable,str(root/'scripts'/script),'--index',str(i)],
                                       stdout=stream,stderr=subprocess.STDOUT,env=os.environ.copy())
                while child.poll() is None:
                    if stage=='editing' and validation.exists():
                        try:
                            item['validated_tasks']=json.loads(validation.read_text())['validated_tasks']
                        except (ValueError,KeyError):
                            pass
                    persist()
                    time.sleep(5)
                item[stage+'_exit']=child.returncode
                persist()
                if child.returncode!=0:
                    raise RuntimeError('{} failed for track {}: see {}'.format(stage,name,log))
            # Small completed logs persist in work as well.
            saved=run/'logs'/log.name
            saved.parent.mkdir(exist_ok=True)
            saved.write_bytes(log.read_bytes())
        record=json.loads((run/'audio'/name/'validation.json').read_text())
        assert record['state']=='completed' and record['validated_tasks']==15
        item.update(state='completed',validated_tasks=15,
                    elapsed_seconds=record['elapsed_seconds'],
                    peak_cuda_allocated_gib=record['peak_cuda_allocated_gib'])
        persist()
        print('COMPLETED',i,name,'total validated',status['validated_tasks'],flush=True)
    assert status['validated_tasks']==750
    status['state']='generation_completed'
except BaseException as exc:
    status['state']='failed'
    status['error']=repr(exc)
    raise
finally:
    persist()
    print(json.dumps(status,indent=2),flush=True)
