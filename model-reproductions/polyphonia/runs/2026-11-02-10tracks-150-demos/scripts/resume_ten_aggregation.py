import json,shutil,subprocess,sys,time
from pathlib import Path
D=Path('/root/autodl-tmp/polyphonia_repro/demos/2026-11-02-ten-tracks')
status=json.loads((D/'status.json').read_text());assert status['state']=='failed' and status['validated_tasks']==150
assert all(t['state']=='completed' for t in status['tracks'])
H=D/'history/aggregation-checkpoint-failure';H.mkdir(parents=True,exist_ok=False)
for name in ['status.json','exit-code','aggregate.log']:shutil.copy2(D/name,H/name)
(D/'delivery').rename(H/'delivery-failed')
with (D/'aggregate-resumed.log').open('w') as log:
 code=subprocess.call([sys.executable,str(D/'scripts/aggregate_ten_tracks.py')],stdout=log,stderr=subprocess.STDOUT)
assert code==0,code
status.update(state='completed',evaluated_tasks=150,resume_note='Generation/evaluation already complete. Original first demo had Jupyter auto-created .ipynb_checkpoints HTML snapshot without nearby audio. Aggregation now excludes checkpoint and AppleDouble metadata copies; no actual task audio or scores changed. Prior failure status/log retained under history.',completed_after_resume_at=time.time())
status.pop('error',None);status.pop('traceback',None)
(D/'status.json').write_text(json.dumps(status,indent=2));(D/'exit-code').write_text('0')
P=D/'delivery';f=P/'EXPERIMENT_RECORD.json';r=json.loads(f.read_text());r['observations_and_deviations'].append(status['resume_note']);f.write_text(json.dumps(r,ensure_ascii=False,indent=2))
f=P/'实验记录.md';f.write_text(f.read_text()+'\n## 打包异常与恢复\n\n'+status['resume_note']+'\n')
print('Aggregation-only recovery completed; audio and scores retained unchanged.')
