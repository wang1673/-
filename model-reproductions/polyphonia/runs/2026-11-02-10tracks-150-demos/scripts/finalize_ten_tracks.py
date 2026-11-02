import hashlib,json,shutil,tarfile
from pathlib import Path
ROOT=Path('/root/autodl-tmp/polyphonia_repro');D=ROOT/'demos/2026-11-02-ten-tracks';P=D/'delivery'
status=json.loads((D/'status.json').read_text());audit=json.loads((D/'final.audit.json').read_text())
assert status['state']=='completed' and status['validated_tasks']==status['evaluated_tasks']==150
assert audit['status']=='passed' and audit['generated']==audit['evaluated']==150
assert (D/'exit-code').read_text().strip()=='0'
source=json.loads((ROOT/'results/musdb_center10_htdemucs_4090d_01/protocol.json').read_text())
source['tracks']=source['tracks'][:10];source['track_count']=10;source['task_count']=150
source['scope']='10track listening demonstration selection from original750protocol; original parameters and crop manifest retained'
(P/'selected-protocol.json').write_text(json.dumps(source,ensure_ascii=False,indent=2))
shutil.copy2(D/'status.json',P/'status.json');shutil.copy2(D/'final.audit.json',P/'final.audit.json')
for name in ['environment.freeze.txt','hardware.txt','official-code-validation.json']:
 if (D/name).exists():shutil.copy2(D/name,P/name)
history=D/'history/aggregation-checkpoint-failure'
if history.exists():
 (P/'history').mkdir(exist_ok=True)
 shutil.copy2(history/'status.json',P/'history/aggregation-failed-status.json')
 shutil.copy2(history/'aggregate.log',P/'history/aggregation-failed-log.txt')
 shutil.copy2(D/'aggregate-resumed.log',P/'history/aggregation-resumed-log.txt')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={str(p.relative_to(P)):sha(p) for p in P.rglob('*') if p.is_file() and p.name!='manifest.sha256.json'}
(P/'manifest.sha256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
archive=ROOT/'archives/polyphonia-ten-tracks-150-listening-20261102.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
 tar.add(P,arcname='Polyphonia_10首150项编辑对照')
 tar.add(D/'scripts',arcname='scripts')
 tar.add(D/'controller.log',arcname='logs/controller.log')
 tar.add(D/'aggregate.log',arcname='logs/aggregate.log')
 if (D/'aggregate-resumed.log').exists():tar.add(D/'aggregate-resumed.log',arcname='logs/aggregate-resumed.log')
 for i in range(10):
  t=D/'tracks'/f'{i:02d}'
  for name in ['run.log','package.log','status.json','exit-code']:
   if (t/name).exists():tar.add(t/name,arcname=f'logs/{i:02d}/{name}')
receipt={'status':'passed','delivery_files_hashed':len(manifest),'archive':str(archive),'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive),'server_root':str(D),'main750_unchanged':True,'generated_tasks':150,'evaluated_tasks':150}
(D/'archive-receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
