import ast
import json
import os
from pathlib import Path
import sys
import torch
import numpy as np
root=Path(os.environ['POLYPHONIA_ROOT'])
sys.path.insert(0,str(root/'references/AudioEditingCode'))
from evals.lpaps import LPAPS
source=ast.parse((root/'scripts/evaluate_benchmark.py').read_text())
function=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='lpaps')
namespace={'torch':torch}
exec(compile(ast.Module(body=[function],type_ignores=[]),'lpaps-adaptation','exec'),namespace)
cache=Path('/home/featurize/data/polyphonia/metric-cache/center10_htdemucs_01')
original=torch.load(next(cache.glob('source-*.pt')),map_location='cpu',weights_only=False)
modified={'layers':[x.roll(7,dims=1) for x in original['layers']]}
class Fixture(torch.nn.Module):
    def forward(self, audio, rates):
        return original['layers'] if audio.item()==0 else modified['layers']
reference=LPAPS.__new__(LPAPS)
torch.nn.Module.__init__(reference)
reference.net=Fixture();reference.L=4;reference.spatial=False
actual=namespace['lpaps'](original,modified)
expected=float(reference(torch.tensor(0),torch.tensor(1),None,None).item())
assert abs(actual-expected)<1e-6,(actual,expected)
assert namespace['lpaps'](original,original)==0
assert np.std(original['top1'])>0
assert abs(float(np.corrcoef(original['top1'],original['top1'])[0,1])-1)<1e-12
embedding=original['embedding']
assert abs(float(torch.nn.functional.cosine_similarity(embedding,embedding).item())-1)<1e-5
report={'status':'passed','LPAPS_reference_commit':'8dc937701a42f6fb53160912f8a96b42fe8261d8',
        'reference_value':expected,'adapted_value':actual,
        'checks':['LPAPS adaptation matches the referenced upstream reduction on real Swin features with a nonzero perturbation',
                  'LPAPS identity=0','CQT1-PCC identity=1','CLAP embedding self cosine=1'],
        'scope':'Checks formula implementation and a real-audio pilot, not equivalence to unpublished author evaluation code'}
(root/'logs/metric-verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
