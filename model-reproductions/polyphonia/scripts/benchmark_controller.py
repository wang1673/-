"""Resumable controller with an explicit global task limit (control.json)."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root=Path(os.environ['POLYPHONIA_ROOT'])
run=root/'results/musdb_center10_htdemucs_01'
protocol=json.loads((run/'protocol.json').read_text())
previous=json.loads((run/'status.json').read_text()) if (run/'status.json').exists() else {}
started=time.monotonic()
status={'state':'handoff_wait','protocol':str(run/'protocol.json'),'tracks':[],'total_tasks':750,
        'started_utc':previous.get('started_utc',datetime.datetime.now(datetime.timezone.utc).isoformat()),
        'resumed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'previous_elapsed_seconds':previous.get('elapsed_seconds',0),'validated_tasks':0}

def persist():
    status['elapsed_seconds']=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(status['started_utc'])).total_seconds()
    status['validated_tasks']=sum(x.get('validated_tasks',0) for x in status['tracks'])
    tmp=run/'status.json.tmp';tmp.write_text(json.dumps(status,indent=2));tmp.replace(run/'status.json')

def limit():
    value=json.loads((run/'control.json').read_text()).get('max_tasks',750)
    assert isinstance(value,int) and 1<=value<=750
    return value

def handoff():
    pid=json.loads((run/'control.json').read_text()).get('active_worker_pid')
    while pid:
        process=Path('/proc')/str(pid)/'stat'
        if not process.exists():break
        if b'benchmark_worker.py' not in (process.parent/'cmdline').read_bytes():break
        # A zombie is no longer writing files and may wait for init to reap it.
        state=process.read_text().rsplit(')',1)[1].strip().split()[0]
        if state=='Z':break
        time.sleep(2)
    control=json.loads((run/'control.json').read_text())
    control.pop('active_worker_pid',None)
    control['handoff_completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    temp=run/'control.json.tmp';temp.write_text(json.dumps(control,indent=2));temp.replace(run/'control.json')

def valid_existing(track,tasks):
    path=run/'audio'/track['track']/'validation.json'
    if not path.exists():return None
    old=json.loads(path.read_text())
    if old.get('state') not in ['completed','completed_subset']:return None
    for task in tasks:
        item=old.get('files',{}).get(task)
        audio=path.parent/(task+'.wav')
        if not item or not audio.exists():return None
        if hashlib.sha256(audio.read_bytes()).hexdigest()!=item['sha256']:return None
    return old

try:
    handoff()
    status['state']='running'
    persist()
    for i,track in enumerate(protocol['tracks']):
        maximum=limit();status['task_limit']=maximum
        count=max(0,min(15,maximum-i*15))
        if count==0:break
        selected=track['tasks'][:count]
        name=track['track']
        item={'index':i,'track':name,'state':'preparing','validated_tasks':0,'selected_tasks':count}
        status['tracks'].append(item)
        old=valid_existing(track,selected)
        if old:
            item.update(state='completed' if count==15 else 'completed_subset',validated_tasks=count,
                        reused_verified_outputs=True,elapsed_seconds=old['elapsed_seconds'],
                        peak_cuda_allocated_gib=old['peak_cuda_allocated_gib'])
            for stage in ['separating','editing']:
                log=Path(protocol['live_logs'])/('{:02d}-{}.log'.format(i,stage))
                if log.exists():
                    saved=run/'logs'/log.name;saved.parent.mkdir(exist_ok=True);saved.write_bytes(log.read_bytes())
            persist();continue
        persist()
        for script,stage in [('prepare_benchmark.py','separating'),('benchmark_worker.py','editing')]:
            validation=run/'audio'/name/'validation.json'
            item['state']=stage;persist()
            log=Path(protocol['live_logs'])/('{:02d}-{}.log'.format(i,stage))
            command=[sys.executable,str(root/'scripts'/script),'--index',str(i)]
            if stage=='editing':command+=['--task-limit',str(count)]
            print('START',i,name,stage,'selected tasks',count,flush=True)
            with log.open('a') as stream:
                child=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,env=os.environ.copy())
                while child.poll() is None:
                    if stage=='editing' and validation.exists():
                        try:
                            item['validated_tasks']=min(count,json.loads(validation.read_text())['validated_tasks'])
                        except (ValueError,KeyError):pass
                    persist();time.sleep(5)
                item[stage+'_exit']=child.returncode;persist()
                if child.returncode!=0:raise RuntimeError('{} failed for {}: {}'.format(stage,name,log))
            saved=run/'logs'/log.name;saved.parent.mkdir(exist_ok=True);saved.write_bytes(log.read_bytes())
        record=valid_existing(track,selected)
        assert record is not None
        item.update(state='completed' if count==15 else 'completed_subset',validated_tasks=count,
                    elapsed_seconds=record['elapsed_seconds'],peak_cuda_allocated_gib=record['peak_cuda_allocated_gib'])
        persist()
        print('COMPLETED',i,name,'total validated',status['validated_tasks'],flush=True)
    assert status['validated_tasks']==limit()
    status['state']='generation_completed' if limit()==750 else 'paused_at_task_limit'
    status['pause_reason']='User requested first {} tasks; remaining tasks require a later resume'.format(limit())
except BaseException as exc:
    status['state']='failed';status['error']=repr(exc);raise
finally:
    persist();print(json.dumps(status,indent=2),flush=True)
