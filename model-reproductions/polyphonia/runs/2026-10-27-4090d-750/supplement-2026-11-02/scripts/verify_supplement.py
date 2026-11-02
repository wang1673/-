import json,hashlib,os
from pathlib import Path
import numpy as np,scipy,torch
R=Path('/root/autodl-tmp/polyphonia_repro/results/musdb_center10_htdemucs_4090d_01');O=R/'metrics-supplement-v1'
s=json.loads((O/'summary.json').read_text());a=np.load(O/'clap_embeddings.npz');x=a['reference'];y=a['generated']
c=np.cov(x,rowvar=False);w,v=np.linalg.eigh(c)
residual=float(np.linalg.norm(c@v-v*w));orthogonal=float(np.linalg.norm(v.T@v-np.eye(512)))
assert residual<1e-10 and orthogonal<1e-10
x=torch.tensor(x,dtype=torch.float64,device='cuda');y=torch.tensor(y,dtype=torch.float64,device='cuda')
cx=torch.cov(x.T);cy=torch.cov(y.T);w,v=torch.linalg.eigh(cx);root=(v*w.clamp_min(0).sqrt())@v.T;p=root@cy@root
fad=float(((x.mean(0)-y.mean(0)).square().sum()+cx.trace()+cy.trace()-2*torch.linalg.eigvalsh((p+p.T)/2).clamp_min(0).sqrt().sum()).item())
n,m=len(x),len(y)
kxx=(x@x.T/512+1)**3;kyy=(y@y.T/512+1)**3;kxy=(x@y.T/512+1)**3
kad=float(((kxx.sum()-kxx.trace())/(n*(n-1))+(kyy.sum()-kyy.trace())/(m*(m-1))-2*kxy.mean()).item())
assert abs(fad-s['FAD']['value'])<1e-5
assert abs(kad-s['KAD']['value'])<1e-10
for path,h in s['old_file_hashes'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h
record={'status':'passed','numpy':np.__version__,'scipy':scipy.__version__,'torch':torch.__version__,'OPENBLAS_CORETYPE':os.environ.get('OPENBLAS_CORETYPE'),'OPENBLAS_NUM_THREADS':os.environ.get('OPENBLAS_NUM_THREADS'),'numpy_eigen_residual':residual,'numpy_eigen_orthogonality_error':orthogonal,'independent_torch_cuda_float64_fad':fad,'independent_torch_cuda_float64_polynomial_kad':kad,'old_files_unchanged':True,'runtime_anomaly':'Default OpenBLAS CPU dispatch produced invalid eigenvectors (orthogonality error3596.56), causing previous negative FAD and failed assertions. Haswell dispatch restored eigenvector checks without changing packages, source embeddings or main750data. Default-dispatch attempted values are invalid and excluded; original failure log retained. Applied only to new supplement and demo processes.'}
(O/'independent-validation.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
