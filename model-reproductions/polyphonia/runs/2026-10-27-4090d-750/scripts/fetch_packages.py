"""Fetch the exact frozen packages concurrently with hash validation."""
import concurrent.futures,hashlib,json,re,time,urllib.request
from pathlib import Path
from pip._vendor.packaging.tags import sys_tags
from pip._vendor.packaging.utils import parse_wheel_filename
from download_file_small import download
ROOT=Path('/root/autodl-tmp/polyphonia_repro')
OUT=Path('/root/autodl-tmp/polyphonia/runtime/wheelhouse');OUT.mkdir(exist_ok=True)
opener=urllib.request.build_opener();opener.addheaders=[('User-Agent','curl/8.5.0')];urllib.request.install_opener(opener)
tags={tag:i for i,tag in enumerate(sys_tags())}
def fetch(line):
    package,version=line.split('==')
    if package in ['torch','torchaudio','torchvision']:
        name=package+'-'+version+'-cp38-cp38-linux_x86_64.whl'
        sha={'torch':'28a1a7500b8ba7a61d958b89434b1bedb64b4ead1391b469b366d739d9eb0e72','torchaudio':'7446df9665bdcda4b2348c794303e5c67afb95f11c759acf2fcebcc0bb0ec066','torchvision':'5736922eabdbdf18443a360b9ce7a7d08de87f34f7a5bec04eefd8085ae095d6'}[package]
        download('https://download.pytorch.org/whl/cu124/'+name.replace('+','%2B'),OUT/name,'sha256:'+sha,workers=6)
        return name
    with urllib.request.urlopen('https://pypi.org/pypi/'+package+'/'+version+'/json',timeout=60) as r:meta=json.load(r)
    candidates=[]
    for f in meta['urls']:
        if f['filename'].endswith('.whl'):
            try:
                file_tags=parse_wheel_filename(f['filename'])[3]
                rank=min((tags[t] for t in file_tags if t in tags),default=10**9)
                if rank<10**9:candidates.append((rank,f))
            except Exception:pass
    if candidates:f=min(candidates,key=lambda x:x[0])[1]
    else:
        files=[f for f in meta['urls'] if f['packagetype']=='sdist'];assert files,line
        f=files[0]
    f['url']=f['url'].replace('https://files.pythonhosted.org/packages/','https://mirrors.aliyun.com/pypi/packages/')
    path=OUT/f['filename'];sha=f['digests']['sha256']
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==sha:return path.name
    if f['size']>8*1024**2:
        download(f['url'],path,'sha256:'+sha,workers=4)
    else:
        with urllib.request.urlopen(f['url'],timeout=90) as r:body=r.read()
        assert hashlib.sha256(body).hexdigest()==sha
        path.write_bytes(body)
    print('PACKAGE VERIFIED',path.name,flush=True)
    return path.name
lines=[l.strip() for l in (ROOT/'scripts/full.freeze.txt').read_text().splitlines() if l.strip()]
def retry(line):
    for n in range(5):
        try:return fetch(line)
        except Exception as exc:
            print('PACKAGE RETRY',line,n,repr(exc),flush=True)
            if n==4:raise
            time.sleep(10)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:files=list(pool.map(retry,lines))
(ROOT/'logs/packages.ready').write_text(json.dumps(files,indent=2))
print('ALL PACKAGES VERIFIED',flush=True)
