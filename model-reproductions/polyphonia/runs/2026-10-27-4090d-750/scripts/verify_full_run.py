import hashlib,json,os
from pathlib import Path
import numpy as np
import soundfile as sf
root=Path(os.environ['POLYPHONIA_ROOT'])
run=root/'results/musdb_center10_htdemucs_4090d_01'
protocol=json.loads((run/'protocol.json').read_text())
expected={(t['track'],task) for t in protocol['tracks'] for task in t['tasks']}
assert len(expected)==750 and len(protocol['tracks'])==50
actual={(p.parent.name,p.stem) for p in (run/'audio').glob('*/*.wav')}
assert actual==expected,(len(actual),len(expected))
records=[]
for track in protocol['tracks']:
    sample=Path(protocol['prepared_root'])/track['track']
    prep=json.loads((sample/'preparation.json').read_text())
    for name,sha in prep['sha256'].items():assert hashlib.sha256((sample/name).read_bytes()).hexdigest()==sha
    validation=json.loads((run/'audio'/track['track']/'validation.json').read_text())
    assert validation['state']=='completed' and validation['validated_tasks']==15
    for task in track['tasks']:
        path=run/'audio'/track['track']/(task+'.wav')
        audio,sr=sf.read(path,dtype='float32');assert sr==16000 and audio.shape==(160000,) and np.isfinite(audio).all()
        sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha==validation['files'][task]['sha256']
        metric=json.loads((run/'metrics'/track['track']/(task+'.json')).read_text());assert metric['audio_sha256']==sha
        records.append({'track':track['track'],'task':task,'sha256':sha})
summary=json.loads((run/'metrics/summary.json').read_text())
assert summary['evaluated_tasks']==750
for key in ['CLAP','LPAPS','CQT1_PCC']:
    rows=[json.loads(p.read_text())[key] for p in (run/'metrics').glob('*/*.json')]
    values=np.array([v for v in rows if v is not None],dtype='float64')
    assert abs(values.mean()-summary[key]['mean'])<1e-12
    assert abs(values.std()-summary[key]['std_population'])<1e-12
audit={'status':'passed','generated':750,'evaluated':750,'tracks':50,'output_format':'16 kHz mono 10 seconds','prepared_audio':'New HT-Demucs output on RTX 4090 D; original server unavailable','records':records}
(run/'full750.audit.json').write_text(json.dumps(audit,indent=2))
print('FULL 750-TASK GENERATION AND THREE-METRIC AUDIT PASSED',flush=True)
