"""Append distribution/composite metrics without changing generated data or old metrics."""
import hashlib,json,os,time
from pathlib import Path
import numpy as np
import torch
from fadtk_distance_reference import calc_embd_statistics,calc_frechet_distance
ROOT=Path('/root/autodl-tmp/polyphonia_repro')
RUN=ROOT/'results/musdb_center10_htdemucs_4090d_01'
OUT=RUN/'metrics-supplement-v1';OUT.mkdir(exist_ok=True)
CODE=Path(__file__).parent
CACHE=Path('/root/autodl-tmp/polyphonia/metric-cache/center10_htdemucs_01')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old_paths=[RUN/'metrics/summary.json',RUN/'metrics/per_task.csv',RUN/'full750.audit.json']
before={str(p):sha(p) for p in old_paths}
protocol=json.loads((RUN/'protocol.json').read_text());summary=json.loads((RUN/'metrics/summary.json').read_text());assert summary['evaluated_tasks']==750
x=[];y=[];inputs=[];tasks=[]
for track in protocol['tracks']:
    source=Path(protocol['prepared_root'])/track['track']/'mixture.wav';source_sha=sha(source)
    cache=CACHE/('source-'+source_sha+'-'+summary['specification_sha256'][:12]+'.pt')
    original=torch.load(cache,map_location='cpu',weights_only=False)
    assert original['sha256']==source_sha
    x.append(original['embedding'].numpy().reshape(512).astype(np.float64))
    inputs.append({'track':track['track'],'source_sha256':source_sha,'cache_sha256':sha(cache)})
    for task in track['tasks']:
        path=RUN/'audio'/track['track']/(task+'.wav');rec=RUN/'metrics'/track['track']/(task+'.json');r=json.loads(rec.read_text())
        assert r['audio_sha256']==sha(path) and r['source_sha256']==source_sha and r['specification_sha256']==summary['specification_sha256']
        y.append(np.asarray(r['audio_embedding'],dtype=np.float64));tasks.append({'track':track['track'],'task':task,'audio_sha256':r['audio_sha256'],'record_sha256':sha(rec)})
x=np.stack(x);y=np.stack(y);assert x.shape==(50,512) and y.shape==(750,512)
assert np.isfinite(x).all() and np.isfinite(y).all()
assert np.max(abs(np.linalg.norm(x,axis=1)-1))<1e-5 and np.max(abs(np.linalg.norm(y,axis=1)-1))<1e-5
np.savez(OUT/'clap_embeddings.npz',reference=x,generated=y)
mu_x,cov_x=calc_embd_statistics(x);mu_y,cov_y=calc_embd_statistics(y)
fad=float(calc_frechet_distance(mu_x,cov_x,mu_y,cov_y))
# Independent PSD implementation checks the copied toolkit distance on rank-deficient covariances.
def stable_fad(a,b):
    ma,ca=calc_embd_statistics(a);mb,cb=calc_embd_statistics(b)
    w,v=np.linalg.eigh(ca);root=(v*np.sqrt(np.maximum(w,0)))@v.T;p=root@cb@root
    trace=np.sqrt(np.maximum(np.linalg.eigvalsh((p+p.T)/2),0)).sum()
    return float(np.sum((ma-mb)**2)+np.trace(ca)+np.trace(cb)-2*trace)
independent=stable_fad(x,y);assert abs(fad-independent)<1e-5,(fad,independent)
assert abs(stable_fad(x,x))<1e-6
n,m=len(x),len(y)
def ustat(kxx,kyy,kxy):return float((kxx.sum()-np.trace(kxx))/(n*(n-1))+(kyy.sum()-np.trace(kyy))/(m*(m-1))-2*kxy.mean())
def poly(gamma,degree=3):return ustat((gamma*(x@x.T)+1)**degree,(gamma*(y@y.T)+1)**degree,(gamma*(x@y.T)+1)**degree)
# Author says polynomial MMD but does not disclose degree/gamma/coef0/scaling. Never label assumptions author-exact.
poly_unit=poly(1.0);poly_dimension=poly(1/512)
# Separate diagnostic: cited original KAD toolkit uses Gaussian, unlike Polyphonia's polynomial description.
x32=torch.tensor(x,dtype=torch.float32);bandwidth=float(torch.pdist(x32).median())
def d2(a,b):return np.maximum((a*a).sum(1)[:,None]+(b*b).sum(1)[None,:]-2*a@b.T,0)
gamma=1/(2*bandwidth**2+1e-8)
kad_gaussian=100*ustat(np.exp(-gamma*d2(x,x)),np.exp(-gamma*d2(y,y)),np.exp(-gamma*d2(x,y)))
table=json.loads((CODE/'paper_table1_musdb.json').read_text())
rows=table['rows']
def balances(cohort):
    vals=np.array([[r[1],-r[3],r[2]] for r in cohort],dtype=np.float64)
    z=(vals-vals.mean(0))/vals.std(0);norm=(z-z.min(0))/(z.max(0)-z.min(0))
    direct=(vals-vals.min(0))/(vals.max(0)-vals.min(0));assert np.max(abs(norm-direct))<1e-12
    h=lambda a,b:2*a*b/(a+b) if a+b else 0.0
    return [{'method':r[0],'CLAP_norm':float(a),'structure_norm':float(b),'melody_norm':float(c),'ASB':h(a,b),'AMB':h(a,c)} for r,(a,b,c) in zip(cohort,norm)]
replay=balances(rows);deltas=[max(abs(r['ASB']-p[4]),abs(r['AMB']-p[5])) for r,p in zip(replay,rows)]
assert max(deltas)<0.005
cohort=rows[:-1]+[['Polyphonia_reproduction',summary['CLAP']['mean'],summary['CQT1_PCC']['mean'],summary['LPAPS']['mean'],None,None]]
balance=balances(cohort)[-1]
assert {str(p):sha(p) for p in old_paths}==before
result={'state':'completed_with_explicit_reproduction_limits','source_code_commit':'26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc','counts':{'reference_clips':50,'generated_clips':750,'dimensions':512},'feature_protocol':'Reuse this run hash-verified CLAP music checkpoint embeddings; one full10s embedding per clip; original preprocessing unchanged; float32 values promoted tofloat64; not latest fadtk default trailing-padding multiwindow or fp16-storage extraction','FAD':{'value':fad,'implementation':'Unmodified calc_embd_statistics/calc_frechet_distance function bodies from microsoft/fadtk ec74b1f96d5576ec04e721985fa0f0d14d965d9b; standalone imports for original Python3.8 environment','independent_psd_check':independent,'infinite_sample_extrapolation':False,'uncertainty':'Not estimated; not a per-task standard deviation'},'KAD':{'status':'polynomial_family_matches_paper_but_exact_author_parameters_unpublished','value':poly_dimension,'variant':'unbiased polynomial MMD2; degree3; gamma1/512; coef0=1; scale1; normalized CLAP features; matches original declared evaluation convention','author_exact':False,'sensitivity_gamma_1':poly_unit,'diagnostic_cited_kadtk_gaussian_x100':kad_gaussian,'diagnostic_bandwidth':bandwidth,'warning':'Gaussian diagnostic is original kadtk convention, not paper-polynomial result; do not substitute one for the other or compare unverified scales to the paper table'},'ASB':{'value':balance['ASB'],'status':'paper_baseline_reference_approximation_user_authorized'},'AMB':{'value':balance['AMB'],'status':'paper_baseline_reference_approximation_user_authorized'},'composite_reference':{'source':table['source'],'baseline_count':7,'cohort_count':8,'operation':'Replace published Polyphonia row by this reproduction; use7 published rounded baseline means; Zscore thenMinMax within each metric across8 methods; harmonic mean; CQT1_PCC forAMB','normalized_reproduction':balance,'paper_table_replay_max_abs_error':max(deltas),'replay_limitation':'Published rounded inputs and unpublished normalization details prevent exact table replay; not newly reproduced baseline runs or same-crop causal comparison'},'validation':{'old_metrics_and_audit_unchanged':True,'all750_audio_hashes_checked':True,'all50_source_hashes_checked':True,'fad_reference_vs_psd_abs_difference':abs(fad-independent)},'old_file_hashes':before}
(OUT/'summary.json').write_text(json.dumps(result,indent=2))
(OUT/'input-manifest.json').write_text(json.dumps({'sources':inputs,'tasks':tasks,'embeddings_sha256':sha(OUT/'clap_embeddings.npz')},indent=2))
(OUT/'paper-baseline-normalization.json').write_text(json.dumps({'paper_inputs':table,'paper_replay':replay,'paper_replay_abs_errors':deltas,'reproduction_cohort':cohort,'reproduction_scores':balances(cohort)},indent=2))
print(json.dumps(result,indent=2),flush=True)
