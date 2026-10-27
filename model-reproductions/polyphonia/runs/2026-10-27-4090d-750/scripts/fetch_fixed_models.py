"""Restore pinned model snapshots, checking every weight hash against HF metadata."""
import concurrent.futures,hashlib,json,time,urllib.request
from pathlib import Path
from download_file import download
ROOT=Path('/root/autodl-tmp/polyphonia_repro')
RUNTIME=Path('/root/autodl-tmp/polyphonia/runtime')
ENDPOINT='https://hf-mirror.com'
opener=urllib.request.build_opener();opener.addheaders=[('User-Agent','curl/8.5.0')];urllib.request.install_opener(opener)
def fetch_repo(repo,revision,allow):
    url=ENDPOINT+'/api/models/'+repo+'/revision/'+revision+'?blobs=true'
    with urllib.request.urlopen(url,timeout=60) as r:meta=json.load(r)
    assert meta['sha']==revision
    base=RUNTIME/'huggingface/hub'/('models--'+repo.replace('/','--'))
    snapshot=base/'snapshots'/revision
    files=[s for s in meta['siblings'] if allow(s['rfilename'])]
    def get(s):
        name=s['rfilename'];path=snapshot/name;path.parent.mkdir(parents=True,exist_ok=True)
        url=ENDPOINT+'/'+repo+'/resolve/'+revision+'/'+name+'?download=true'
        sha=s.get('lfs',{}).get('sha256')
        for attempt in range(10):
            try:
                if sha:
                    download(url,path,'sha256:'+sha,workers=8)
                else:
                    if not path.exists():
                        with urllib.request.urlopen(url,timeout=90) as r:body=r.read()
                        path.write_bytes(body)
                    body=path.read_bytes()
                    assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==s['blobId'],name
                assert path.stat().st_size==s['size'],name
                return name
            except Exception as exc:
                print('MODEL RETRY',repo,name,attempt,repr(exc),flush=True)
                if attempt==9:raise
                time.sleep(min(60, max(10, int(getattr(exc,'headers',{}).get('Retry-After','15')))))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(get,files))
    (base/'refs').mkdir(exist_ok=True);(base/'refs/main').write_text(revision)
    (ROOT/'logs'/('download-'+repo.replace('/','--')+'.json')).write_text(json.dumps(meta,indent=2))
    return snapshot

demucs=json.loads((ROOT/'logs/original.demucs-model.json').read_text())
path=RUNTIME/'torch/hub/checkpoints'/Path(demucs['path']).name
download(demucs['source'],path,'sha256:'+demucs['sha256'],workers=8)
demucs['path']=str(path);(ROOT/'logs/demucs-model.json').write_text(json.dumps(demucs,indent=2))

snapshot=fetch_repo('cvssp/audioldm2','c8e7e189d324425c05c4c2f81214041ef4107983',lambda n:not n.endswith(('.bin','.md')) and n!='.gitattributes')
(ROOT/'logs/model.snapshot.json').write_text(json.dumps({'repo_id':'cvssp/audioldm2','revision':snapshot.name,'snapshot':str(snapshot)},indent=2))
(ROOT/'logs/inference.ready').write_text('AudioLDM2 and Demucs verified\n')
original=json.loads((ROOT/'logs/original.evaluation-model.json').read_text())
clap=fetch_repo(original['repo'],original['revision'],lambda n:n==original['filename'])
roberta=fetch_repo(original['roberta_repo'],original['roberta_revision'],lambda n:n in ['config.json','merges.txt','vocab.json','tokenizer.json','tokenizer_config.json','model.safetensors'])
original['checkpoint']=str(clap/original['filename']);original['roberta_snapshot']=str(roberta)
assert hashlib.sha256(Path(original['checkpoint']).read_bytes()).hexdigest()==original['sha256']
(ROOT/'logs/evaluation-model.json').write_text(json.dumps(original,indent=2))
(ROOT/'logs/models.ready').write_text('All model snapshots and weight hashes verified\n')
print('ALL MODELS VERIFIED',flush=True)
