import json
import os
from pathlib import Path
import subprocess
import soundfile as sf
root=Path(os.environ['POLYPHONIA_ROOT'])
run=root/'results/musdb_center10_htdemucs_01'
run.mkdir(parents=True,exist_ok=False)
audit=json.loads((root/'logs/musdb18hq.audit.json').read_text())
assert audit['status']=='passed' and audit['mapped_tasks']==750
tracks=[]
for row in audit['mapping']:
    info=sf.info(row['mixture'])
    assert info.samplerate==44100 and info.frames>=441000
    tasks=json.loads(Path(row['prompt_file']).read_text())
    assert len(tasks)==15
    tracks.append({'track':row['audio_track'],'mixture':row['mixture'],
                   'original_frames':info.frames,'original_samplerate':info.samplerate,
                   'start_frame':(info.frames-441000)//2, 'frames':441000,
                   'prompt_file':row['prompt_file'],'tasks':list(tasks)})
protocol={'run_id':run.name,'scope':'MUSDB18-HQ test / Polyphonia only',
          'paper':'https://arxiv.org/html/2605.10203v1',
          'repo_commit':subprocess.check_output(['git','-C',str(root/'polyphonia'),'rev-parse','HEAD'],text=True).strip(),
          'track_count':50,'task_count':750,'crop_seconds':10,
          'crop_rule':'floor((original_frames - 441000)/2) at original 44100 Hz; same timestamps for mixture and estimated stems',
          'crop_status':'User-approved reproduction assumption. Authors did not publish an exact crop manifest; not an exact replication of Table 1.',
          'separator':{'package':'demucs==4.0.1','model':'htdemucs','seed':928,'shifts':1,'overlap':0.25,
                       'input':'entire mixture, then crop estimated four stems; never oracle dataset stems',
                       'checkpoint_status':'htdemucs standard public weights; paper does not specify precise checkpoint hash'},
          'editing':{'steps':100,'cfg':3.5,'mask_bias_strength':2.5,'seed':928,'precision':'fp16',
                     'mask_type':'energy','down_layers':list(range(1,19)),
                     'implementation':'Unmodified official run_sample_exp.py; output saving instrumented for validation',
                     'known_paper_code_difference':'Official energy mask divides target Mel energy by mixture Mel energy; paper Eq 9 divides by target+non-target energy. Code baseline retained.'},
          'prepared_root':'/home/featurize/data/polyphonia/prepared/center10_htdemucs_01',
          'live_logs':'/home/featurize/data/polyphonia/runtime/logs/musdb_center10_htdemucs_01',
          'results':str(run/'audio'), 'tracks':tracks}
(run/'protocol.json').write_text(json.dumps(protocol,indent=2))
Path(protocol['live_logs']).mkdir(parents=True,exist_ok=True)
print(json.dumps({k:v for k,v in protocol.items() if k!='tracks'},indent=2))
