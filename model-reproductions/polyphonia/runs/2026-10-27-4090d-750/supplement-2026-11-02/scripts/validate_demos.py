import hashlib,json,os
from pathlib import Path
import numpy as np
import soundfile as sf
import torch,julius,laion_clap
from laion_clap.clap_module.factory import load_state_dict

ROOT=Path('/root/autodl-tmp/polyphonia_repro')
D=ROOT/'demos/2026-11-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    a,sr=sf.read(str(p),dtype='float32',always_2d=True)
    a=torch.tensor(a.mean(1)).unsqueeze(0)
    return julius.resample_frac(a,sr,16000).numpy()[0]
paths={
 'music_original':D/'music/input/mixture.wav',
 'music_violin':D/'music/output/vocals2violin.wav',
 'music_saxophone':D/'music/output/vocals2saxophone.wav',
 'cat_original':D/'cat-to-dog/input/mixture.wav',
 'cat_to_dog':D/'cat-to-dog/output/cat2dog.wav',
 'cat_to_dog_deep':D/'cat-to-dog/output/cat2dog_deep.wav'}
arrays={};validation={}
for name,p in paths.items():
    a=read(p);assert len(a)==160000 and np.isfinite(a).all()
    rms=float(np.sqrt(np.mean(a.astype('float64')**2)));assert rms>1e-6
    arrays[name]=a;validation[name]={'path':str(p),'sha256':sha(p),'sample_rate_after_audition_resample':16000,'frames':len(a),'rms':rms,'peak':float(abs(a).max())}
aud=D/'listening';aud.mkdir(exist_ok=True)
def audition(a):
    gain=min(0.1/np.sqrt(np.mean(a.astype('float64')**2)),0.95/max(abs(a).max(),1e-8))
    return a*gain
for name,a in arrays.items():sf.write(str(aud/(name+'.wav')),audition(a),16000)
for name,src in [('music_violin','music_original'),('music_saxophone','music_original'),('cat_to_dog','cat_original'),('cat_to_dog_deep','cat_original')]:
    before,after=arrays[src],arrays[name]
    assert not np.array_equal(before,after)
    sf.write(str(aud/(name+'_before_after.wav')),np.concatenate([audition(before),np.zeros(8000),audition(after)]),16000)

weights=json.loads((ROOT/'logs/evaluation-model.json').read_text())
model=laion_clap.CLAP_Module(enable_fusion=False,amodel='HTSAT-base',device='cuda')
state=load_state_dict(weights['checkpoint'],skip_params=True);state.pop('text_branch.embeddings.position_ids',None)
model.model.load_state_dict(state,strict=True);model.eval()
texts=['The sound of a cat meowing.','The sound of a dog barking.']
scores={}
with torch.inference_mode():
    t=model.get_text_embedding(texts,use_tensor=True)
    for name in ['cat_original','cat_to_dog','cat_to_dog_deep']:
        a=julius.resample_frac(torch.tensor(arrays[name]).unsqueeze(0),16000,48000).cuda()
        e=model.get_audio_embedding_from_data(a,use_tensor=True)
        s=(torch.nn.functional.normalize(e,dim=1)@torch.nn.functional.normalize(t,dim=1).T).cpu().numpy()[0]
        scores[name]={'cat_prompt_cosine':float(s[0]),'dog_prompt_cosine':float(s[1]),'dog_minus_cat':float(s[1]-s[0])}
record={'state':'completed','files':validation,'cat_dog_CLAP_diagnostic':scores,'diagnostic_note':'Two-prompt similarity is an auxiliary semantic check, not human listening or proof of convincing dog sound; no selection or exclusion of either prompt variant.','audition_note':'Separate listening copies only: mono mean, resample16k, targetRMS0.1 limited topeak0.95. Raw model outputs unchanged. Before-after files have10s source,0.5s silence,10s edited.','settings':{'official_commit':'26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc','steps':100,'cfg':3.5,'maskbias':2.5,'seed':928,'precision':'fp16','mask_type':'energy','OPENBLAS_CORETYPE':'Haswell','OPENBLAS_NUM_THREADS':'1'},'failures_and_retries':'Second cat prompt failed in shared process with CPU/CUDA attention tensor mismatch; preserved run.log. Retried only deep task in fresh process with unchanged official code/parameters and new seed928 stream. Official script exits0 even on task failure; output existence and content are checked here.'}
record['failures_and_retries']='Initial deep prompt and fresh-process retry failed with CPU/CUDA attention mismatch. The softmask phrase a dog barking was absent from baseline a large dog barking, triggering official fallback. Kept failed-v1 prompt and both logs; changed only mask phrase to exact a large dog barking per official mirror rule, reran only deep task in fresh process with same code/parameters/seed928. No model code changes. Official exits0 on task failure; validated outputs independently.'
(D/'validation.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
