"""CLAP, CLAP-Swin LPAPS, and CQT1-PCC for the recorded center-10s protocol.
LPAPS tensor normalization/reduction follows HilaManor/AudioEditingCode/evals/lpaps.py
(reference checkout and licenses retained under references/AudioEditingCode).
Distribution metrics use explicit supplementary conventions, not claimed exact paper code.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import numpy as np
import soundfile as sf
import torch
import torch.nn.functional as F
import julius
import laion_clap
from laion_clap.clap_module.factory import load_state_dict
from nnAudio.features import CQT2010

parser=argparse.ArgumentParser()
parser.add_argument('--device',default='cpu')
parser.add_argument('--available-only',action='store_true')
parser.add_argument('--limit',type=int,default=0)
args=parser.parse_args()
root=Path(os.environ['POLYPHONIA_ROOT'])
run=root/'results/musdb_center10_htdemucs_01'
protocol=json.loads((run/'protocol.json').read_text())
weights=json.loads((root/'logs/evaluation-model.json').read_text())
metrics_dir=run/'metrics'
metrics_dir.mkdir(exist_ok=True)
cache=Path('/home/featurize/data/polyphonia/metric-cache/center10_htdemucs_01')
cache.mkdir(parents=True,exist_ok=True)
metric_spec={'version':1,'checkpoint_sha256':weights['sha256'],
    'CLAP':'cosine of HTSAT-base music_audioset_epoch_15_esc_90.14 embeddings; 48k mono, julius resampling, float input, max 77 text tokens',
    'LPAPS':'four Swin layer outputs; normalize over token axis dim=1; squared difference, sum token axis, mean remaining axes, sum four layers; matches referenced DDPM LPAPS reduction',
    'CQT1_PCC':{'library':'nnAudio==0.3.3','class':'CQT2010','sr':16000,'n_bins':128,'bins_per_octave':24,
                'hop_length':512,'fmin':32.7,'definition':'Pearson correlation of argmax-frequency-bin trajectories; constant trajectories undefined'},
    'reference_audio':'the raw center crop, stereo averaged; no per-clip peak normalization',
    'inference_source_note':'upstream wav_to_fbank reads first channel and normalizes; source evaluation downmix follows referenced evaluation code',
    'crop_assumption':protocol['crop_status'],
    'LPAPS_reference_commit':'8dc937701a42f6fb53160912f8a96b42fe8261d8',
    'distributional_conventions':'CLAP 512-d normalized embeddings; source set 50 tracks, generated 750 tasks. FAD uses empirical Gaussian moments; polynomial MMD2 uses (dot/d+1)^3 and unbiased U-statistic. These details are supplementary assumptions, not published exact paper settings.',
    'omitted':'ASB and AMB require all-method normalization; MOS requires human raters; neither is fabricated.'}
spec_hash=hashlib.sha256(json.dumps(metric_spec,sort_keys=True).encode()).hexdigest()
(metrics_dir/'specification.json').write_text(json.dumps(metric_spec,indent=2))
np.random.seed(928)
torch.manual_seed(928)
model=laion_clap.CLAP_Module(enable_fusion=False,amodel='HTSAT-base',device=args.device)
state=load_state_dict(weights['checkpoint'],skip_params=True)
state.pop('text_branch.embeddings.position_ids',None)
model.model.load_state_dict(state,strict=True)
model.eval()
for param in model.parameters():param.requires_grad=False
captured={}
for index,layer in enumerate(model.model.audio_branch.layers):
    def hook(module,inputs,output,key=index):
        captured[key]=output[0].detach().cpu()
    layer.register_forward_hook(hook)
cqt=CQT2010(sr=16000,n_bins=128,bins_per_octave=24,hop_length=512,fmin=32.7,verbose=False).to(args.device).eval()

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    data,sr=sf.read(str(path),dtype='float32',always_2d=True)
    assert np.isfinite(data).all() and abs(len(data)/sr-10)<1e-4
    return torch.from_numpy(data.mean(axis=1).copy()).unsqueeze(0),sr

@torch.inference_mode()
def features(path):
    audio,sr=read(path)
    wave48=julius.resample_frac(audio,sr,48000).to(args.device)
    captured.clear()
    embedding=model.get_audio_embedding_from_data(wave48,use_tensor=True).detach().cpu()
    assert set(captured)==set(range(4))
    layers=[captured[i].clone() for i in range(4)]
    wave16=julius.resample_frac(audio,sr,16000).to(args.device)
    top1=cqt(wave16).argmax(dim=1).squeeze(0).cpu().numpy().astype('float64')
    return {'embedding':embedding,'layers':layers,'top1':top1}

def lpaps(first,second):
    value=0.0
    for a,b in zip(first['layers'],second['layers']):
        na=a/(torch.sqrt(torch.sum(a*a,dim=1,keepdim=True))+1e-10)
        nb=b/(torch.sqrt(torch.sum(b*b,dim=1,keepdim=True))+1e-10)
        value+=float(((na-nb)**2).sum(dim=1,keepdim=True).mean([1,2]).item())
    return value

def pcc(a,b):
    assert a.shape==b.shape
    if np.std(a)==0 or np.std(b)==0:return None
    return float(np.corrcoef(a,b)[0,1])

rows=[]
sources=[]
outputs=[]
started=time.monotonic()
for track in protocol['tracks']:
    sample=Path(protocol['prepared_root'])/track['track']
    source=sample/'mixture.wav'
    available=[task for task in track['tasks'] if (run/'audio'/track['track']/(task+'.wav')).exists()]
    if not available:
        if args.available_only:continue
        raise FileNotFoundError('No outputs for '+track['track'])
    if not args.available_only:assert len(available)==15
    source_sha=digest(source)
    source_cache=cache/('source-'+source_sha+'-'+spec_hash[:12]+'.pt')
    if source_cache.exists():
        original=torch.load(source_cache,map_location='cpu',weights_only=False)
    else:
        original=features(source)
        assert lpaps(original,original)==0
        original['sha256']=source_sha
        torch.save(original,source_cache)
    sources.append(original['embedding'].numpy()[0])
    prompts=json.loads((sample/'prompt_multi.json').read_text())
    for task in available:
        path=run/'audio'/track['track']/(task+'.wav')
        out_sha=digest(path)
        record_path=metrics_dir/track['track']/(task+'.json')
        record_path.parent.mkdir(exist_ok=True)
        if record_path.exists():
            old=json.loads(record_path.read_text())
        else:old={}
        if old.get('audio_sha256')==out_sha and old.get('source_sha256')==source_sha and old.get('specification_sha256')==spec_hash:
            row=old
        else:
            edited=features(path)
            with torch.inference_mode():
                text=model.get_text_embedding([prompts[task]['Baseline Prompt']],use_tensor=True).detach().cpu()
            clap=float(F.cosine_similarity(edited['embedding'],text,dim=1).item())
            row={'track':track['track'],'task':task,'audio_sha256':out_sha,'source_sha256':source_sha,
                 'specification_sha256':spec_hash,'CLAP':clap,'LPAPS':lpaps(original,edited),
                 'CQT1_PCC':pcc(original['top1'],edited['top1']),
                 'target_prompt':prompts[task]['Baseline Prompt'],
                 'audio_embedding':edited['embedding'].numpy()[0].tolist()}
            assert np.isfinite(row['CLAP']) and np.isfinite(row['LPAPS'])
            record_path.write_text(json.dumps(row,indent=2))
        rows.append(row)
        outputs.append(np.asarray(row['audio_embedding']))
        print('Evaluated',len(rows),track['track'],task,'CLAP',row['CLAP'],'LPAPS',row['LPAPS'],'CQT1_PCC',row['CQT1_PCC'],flush=True)
        if args.limit and len(rows)>=args.limit:break
    if args.limit and len(rows)>=args.limit:break

summary={'state':'partial' if len(rows)!=750 else 'completed','evaluated_tasks':len(rows),
         'expected_tasks':750,'elapsed_seconds':time.monotonic()-started,'specification_sha256':spec_hash,
         'paper_comparison':'Center-crop protocol differs from unpublished author crop manifest. Quantitative results are not exact Table 1 replication.'}
for key in ['CLAP','LPAPS','CQT1_PCC']:
    values=np.array([r[key] for r in rows if r[key] is not None],dtype='float64')
    summary[key]={'mean':float(values.mean()) if len(values) else None,
                  'std_population':float(values.std()) if len(values) else None,'valid':len(values),
                  'undefined':len(rows)-len(values)}
if len(rows)==750:
    x=np.array(sources,dtype='float64');y=np.array(outputs,dtype='float64')
    assert len(x)==50 and len(y)==750
    def fad(a,b):
        ca=np.cov(a,rowvar=False);cb=np.cov(b,rowvar=False)
        eig,vec=np.linalg.eigh(ca)
        square=(vec*np.sqrt(np.maximum(eig,0)))@vec.T
        product=(square@cb@square)
        trace_root=np.sqrt(np.maximum(np.linalg.eigvalsh((product+product.T)/2),0)).sum()
        return float(max(np.sum((a.mean(0)-b.mean(0))**2)+np.trace(ca)+np.trace(cb)-2*trace_root,0))
    def mmd(a,b):
        dim=a.shape[1]
        xx=(a@a.T/dim+1)**3;yy=(b@b.T/dim+1)**3;xy=(a@b.T/dim+1)**3
        return float((xx.sum()-np.trace(xx))/(len(a)*(len(a)-1))+(yy.sum()-np.trace(yy))/(len(b)*(len(b)-1))-2*xy.mean())
    assert fad(x,x)<1e-6
    summary['supplementary_CLAP_FAD_empirical']=fad(x,y)
    summary['supplementary_polynomial_MMD2_unbiased']=mmd(x,y)
    np.savez(cache/'distribution_embeddings.npz',source=x,generated=y)
filename='summary.json' if len(rows)==750 else 'summary.partial.json'
(metrics_dir/filename).write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2),flush=True)
if not args.available_only:assert len(rows)==750
