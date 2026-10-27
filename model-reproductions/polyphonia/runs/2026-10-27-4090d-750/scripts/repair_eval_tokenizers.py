import json,urllib.request
from pathlib import Path
root=Path('/root/autodl-tmp/polyphonia_repro')
namespace={}
text=(root/'scripts/fetch_fixed_models.py').read_text()
exec(text.split('demucs=json.loads')[0],namespace)
records=[]
for repo in ['bert-base-uncased','facebook/bart-base']:
    with urllib.request.urlopen('https://hf-mirror.com/api/models/'+repo+'/revision/main?blobs=true',timeout=60) as r:meta=json.load(r)
    rev=meta['sha']
    allow={'config.json','tokenizer.json','tokenizer_config.json','special_tokens_map.json','vocab.txt','vocab.json','merges.txt','added_tokens.json'}
    snapshot=namespace['fetch_repo'](repo,rev,lambda n:n in allow)
    records.append({'repo':repo,'revision':rev,'snapshot':str(snapshot),'use':'Only import-time unused BERT/BART tokenizer caches; actual metric text branch remains pinned Roberta','old_revision':'not recorded in old experiment'})
(root/'logs/evaluation-tokenizer-repair.json').write_text(json.dumps({'reason':'CLAP import initializes BERT, Roberta, and BART tokenizers; BERT/BART caches were missing on fresh server','software_or_metric_changes':False,'tokenizers':records},indent=2))
print('TOKENIZER CACHES RESTORED',flush=True)
