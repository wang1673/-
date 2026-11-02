import json,os,sys,time,hashlib,shutil
from pathlib import Path
import numpy as np,soundfile as sf,torch
ROOT=Path('/root/autodl-tmp/polyphonia_repro')
RUN=ROOT/'results/musdb_center10_htdemucs_4090d_01'
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--index',type=int,required=True);parser.add_argument('--dir',required=True);args=parser.parse_args()
D=Path(args.dir)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((RUN/'protocol.json').read_text());track=p['tracks'][args.index]
source=Path(p['prepared_root'])/track['track'];inp=D/'input';out=D/'output'
inp.mkdir(parents=True,exist_ok=True);out.mkdir(exist_ok=True)
for name in ['mixture','vocals','bass','drums','other']:
    q=inp/(name+'.wav')
    if not q.exists():q.symlink_to(source/q.name)
assert not list(out.glob('*.wav')),'Do not overwrite/restart an existing demo run'
shutil.copy2(source/'prompt_multi.json',inp/'prompt_multi.json')
prompts=json.loads((inp/'prompt_multi.json').read_text())
assert len(prompts)==15 and list(prompts)==list(track['tasks'])
oldfiles=[RUN/'metrics/summary.json',RUN/'metrics/per_task.csv',RUN/'full750.audit.json']
before={str(f):sha(f) for f in oldfiles}
status={'state':'running','track':track['track'],'task_count':15,'track_index':args.index,'selected_tasks':list(prompts),'original_protocol':str(RUN/'protocol.json'),'input_sha256':{str(f):sha(f) for f in inp.iterdir()},'original_records_sha256':before,'configuration':p['editing'],'OPENBLAS_CORETYPE':os.environ.get('OPENBLAS_CORETYPE'),'OPENBLAS_NUM_THREADS':os.environ.get('OPENBLAS_NUM_THREADS'),'note':'Fresh official inference on same dataset clip and all15published prompts. No old output/RNG reused; independent demo, not appended to750benchmark.'}
(D/'status.json').write_text(json.dumps(status,indent=2))
start=time.monotonic();sys.path.insert(0,str(ROOT/'polyphonia'))
import run_sample_exp as official
sys.argv=['run_sample_exp.py','--sample_dir',str(inp),'--output_dir',str(out),'--device','cuda','--precision','fp16','--seed','928','--mask_type','energy']
status['argv']=sys.argv.copy();torch.cuda.reset_peak_memory_stats()
try:
    official.main()
    validated={}
    for task in prompts:
        f=out/(task+'.wav');a,sr=sf.read(str(f),dtype='float32')
        assert sr==16000 and a.ndim==1 and len(a)==160000 and np.isfinite(a).all()
        rms=float(np.sqrt(np.mean(a.astype('float64')**2)));assert rms>1e-6
        validated[task]={'sha256':sha(f),'sample_rate':sr,'frames':len(a),'rms':rms,'peak':float(abs(a).max())}
    assert {str(f):sha(f) for f in oldfiles}==before
    status.update(state='completed',validated_tasks=len(validated),files=validated,original_records_unchanged=True)
except BaseException as e:
    status.update(state='failed',error=repr(e));raise
finally:
    status.update(elapsed_seconds=time.monotonic()-start,peak_cuda_allocated_GiB=torch.cuda.max_memory_allocated()/1024**3)
    (D/'status.json').write_text(json.dumps(status,indent=2));print(json.dumps(status,indent=2),flush=True)
