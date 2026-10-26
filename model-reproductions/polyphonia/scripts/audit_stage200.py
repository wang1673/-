import csv
import datetime
import hashlib
import json
from pathlib import Path
import numpy as np
import soundfile as sf
root=Path('/home/featurize/work/polyphonia_repro');run=root/'results/musdb_center10_htdemucs_01'
protocol=json.loads((run/'protocol.json').read_text());status=json.loads((run/'status.json').read_text())
pipeline=json.loads((run/'pipeline.json').read_text());control=json.loads((run/'control.json').read_text())
assert status['state']=='paused_at_task_limit' and status['validated_tasks']==200
assert control['max_tasks']==200
assert pipeline['state']=='stage_completed_remaining_paused' and pipeline['evaluated_tasks']==200 and pipeline['remaining_tasks']==550
for name in ['metrics/summary.first200.json','metrics/per_task.first200.csv','RESULTS_first200_zh.md','review_first200/listening-manifest.json']:
    assert (run/name).is_file(),name
summary=json.loads((run/'metrics/summary.first200.json').read_text())
expected=[(t,task) for t in protocol['tracks'] for task in t['tasks']][:200]
assert len(expected)==200
csv_rows=list(csv.DictReader((run/'metrics/per_task.first200.csv').open()))
assert len(csv_rows)==200
assert [(r['track'],r['task']) for r in csv_rows]==[(t['track'],task) for t,task in expected]
actual=set(p.relative_to(run/'audio').as_posix() for p in (run/'audio').glob('*/*.wav'))
assert actual==set(t['track']+'/'+task+'.wav' for t,task in expected)
source_hashes={};checked=[];records=[]
for (track,task),row in zip(expected,csv_rows):
    name=track['track'];wave=run/'audio'/name/(task+'.wav')
    body=wave.read_bytes();sha=hashlib.sha256(body).hexdigest()
    validation=json.loads((wave.parent/'validation.json').read_text())
    assert validation['state'] in ['completed','completed_subset']
    assert validation['files'][task]['sha256']==sha==row['audio_sha256']
    audio,sr=sf.read(str(wave),dtype='float32')
    assert sr==16000 and audio.ndim==1 and len(audio)==160000
    assert np.isfinite(audio).all() and np.sqrt(np.mean(audio.astype('float64')**2))>1e-6
    metric=json.loads((run/'metrics'/name/(task+'.json')).read_text())
    assert metric['audio_sha256']==sha
    if name not in source_hashes:
        source_hashes[name]=hashlib.sha256((Path(protocol['prepared_root'])/name/'mixture.wav').read_bytes()).hexdigest()
    assert metric['source_sha256']==source_hashes[name]==row['source_sha256']
    for key in ['CLAP','LPAPS','CQT1_PCC']:
        assert metric[key] is not None and np.isfinite(metric[key])
        assert abs(float(row[key])-metric[key])<1e-12
    checked.append({'track':name,'task':task,'sha256':sha});records.append(metric)
for key in ['CLAP','LPAPS','CQT1_PCC']:
    values=np.array([r[key] for r in records],dtype='float64')
    assert abs(float(values.mean())-summary[key]['mean'])<1e-12
    assert abs(float(values.std())-summary[key]['std_population'])<1e-12
    assert summary[key]['valid']==200 and summary[key]['undefined']==0
examples=json.loads((run/'review_first200/listening-manifest.json').read_text())
assert len(examples)==8
for row in examples:
    assert hashlib.sha256(Path(row['edited']).read_bytes()).hexdigest()==row['audio_sha256']
    assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['source_sha256']
report={'status':'passed','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'generated_wav_count':200,'evaluated_rows':200,'full_tracks':13,'partial_tracks':1,
        'listening_pairs':8,'final_failed_tasks':0,'undefined_metrics':{key:0 for key in ['CLAP','LPAPS','CQT1_PCC']},
        'remaining_tasks_paused':550,'no_outputs_beyond_task200':True,
        'checks':['All 200 WAV hashes match validation and metric records','16k mono, 10 seconds, finite non-silent audio',
                  'CSV order exactly matches first 200 protocol tasks','CSV and JSON values match; means/std independently recomputed',
                  'All 8 listening pairs match source/edited hashes','Generation paused and evaluation completed with limit=200'],
        'known_interruption':'One unsaved generation was interrupted during controller handoff. 70 valid outputs retained; missing tasks resumed. Random-stream difference documented in limit200-change.json.',
        'files':checked}
(run/'stage200.audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
