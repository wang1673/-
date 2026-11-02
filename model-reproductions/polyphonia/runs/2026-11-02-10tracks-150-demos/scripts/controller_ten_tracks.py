import json,os,shutil,subprocess,sys,time,traceback
from pathlib import Path
ROOT=Path('/root/autodl-tmp/polyphonia_repro');D=ROOT/'demos/2026-11-02-ten-tracks';S=D/'scripts';T=D/'tracks';T.mkdir(exist_ok=True)
first=ROOT/'demos/2026-11-02-full15';assert json.loads((first/'status.json').read_text())['validated_tasks']==15
if not (T/'00').exists():(T/'00').symlink_to(first,target_is_directory=True)
protocol=json.loads((ROOT/'results/musdb_center10_htdemucs_4090d_01/protocol.json').read_text())
assert not (D/'status.json').exists(),'Controller already initialized; inspect before any resume'
status={'state':'generating','tracks':[{ 'index':i,'track':t['track'],'tasks':15,'state':'completed_reused_prior_demo' if i==0 else 'pending'} for i,t in enumerate(protocol['tracks'][:10])],'selection':'First10tracks in original protocol order, selected before running; same center10s clips; no quality selection','expected_tasks':150,'prior_demo_tasks':15,'new_tasks':135,'completed_tracks':1,'validated_tasks':15,'started_at':time.time()}
start=time.monotonic()
def save():
 status['elapsed_seconds']=time.monotonic()-start
 tmp=D/'status.tmp';tmp.write_text(json.dumps(status,indent=2));tmp.replace(D/'status.json')
save()
try:
 for i in range(1,10):
  track=T/f'{i:02d}';track.mkdir(exist_ok=True);status.update(current_index=i,state='generating');status['tracks'][i]['state']='running';save()
  with (track/'run.log').open('w') as log:
   code=subprocess.call([sys.executable,str(S/'run_dataset15_generic.py'),'--index',str(i),'--dir',str(track)],stdout=log,stderr=subprocess.STDOUT)
  (track/'exit-code').write_text(str(code));assert code==0,('generation_exit',i,code)
  r=json.loads((track/'status.json').read_text());assert r['state']=='completed' and r['validated_tasks']==15
  status['tracks'][i]['state']='generation_completed';status['completed_tracks']=i+1;status['validated_tasks']=(i+1)*15;save()
 status['state']='packaging';save()
 for i in range(10):
  track=T/f'{i:02d}';status['current_index']=i;save()
  if i==0:
   assert (track/'delivery/EXPERIMENT_RECORD.json').exists()
  else:
   with (track/'package.log').open('w') as log:
    code=subprocess.call([sys.executable,str(S/'package_dataset15_generic.py'),'--dir',str(track)],stdout=log,stderr=subprocess.STDOUT)
   assert code==0,('packaging_exit',i,code)
  status['tracks'][i]['state']='completed';save()
 with (D/'aggregate.log').open('w') as log:
  code=subprocess.call([sys.executable,str(S/'aggregate_ten_tracks.py')],stdout=log,stderr=subprocess.STDOUT)
 assert code==0,('aggregate_exit',code)
 status.update(state='completed',evaluated_tasks=150);save();(D/'exit-code').write_text('0')
except BaseException as e:
 status.update(state='failed',error=repr(e),traceback=traceback.format_exc());save();(D/'exit-code').write_text('1');raise
