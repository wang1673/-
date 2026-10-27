"""Restore original WAV bytes from the same pinned mirror used in the old run."""
import hashlib,json,time,urllib.request,zlib
from pathlib import Path,PurePosixPath
import pyarrow.parquet as pq
from download_file import download
ROOT=Path('/root/autodl-tmp/polyphonia_repro');DATA=Path('/root/autodl-tmp/polyphonia')
REV='7950781147516a3b1411310274175ff98ab8f062'
opener=urllib.request.build_opener();opener.addheaders=[('User-Agent','curl/8.5.0')];urllib.request.install_opener(opener)
meta=json.loads((ROOT/'logs/data.api.json').read_text())
original=json.loads((ROOT/'logs/original.musdb18hq.manifest.json').read_text())['files']
expected={k:v for k,v in original.items() if k.endswith('/mixture.wav')}
plan=json.loads((ROOT/'scripts/musdb_test_plan.json').read_text())
crcs={e['path']:e['crc32'] for e in plan['entries']}
work=DATA/'mirror-shards';work.mkdir(exist_ok=True)
done_path=ROOT/'logs/mirror-shards.completed.json'
done=json.loads(done_path.read_text()) if done_path.exists() else []
for f in sorted(meta['siblings'],key=lambda x:x['rfilename']):
    name=f['rfilename']
    if not name.startswith('data/validation-') or name in done:continue
    path=work/Path(name).name
    url='https://hf-mirror.com/datasets/danjacobellis/musdb18HQ/resolve/'+REV+'/'+name+'?download=true'
    for attempt in range(8):
        try:
            download(url,path,'sha256:'+f['lfs']['sha256'],workers=16)
            break
        except Exception as exc:
            print('MIRROR RETRY',name,attempt,repr(exc),flush=True)
            if attempt==7:raise
            time.sleep(30)
    for batch in pq.ParquetFile(path).iter_batches(batch_size=1,columns=['audio','path','instrument']):
        for row in batch.to_pylist():
            parts=PurePosixPath(row['path']).parts
            assert 'test' in parts,row['path']
            key='/'.join(parts[parts.index('test'):])
            if key not in expected:continue
            body=row['audio']['bytes'];wanted=expected[key]
            assert len(body)==wanted['size'] and zlib.crc32(body)==crcs[key],key
            sha=hashlib.sha256(body).hexdigest();assert sha==wanted['sha256'],key
            target=DATA/'musdb18hq'/key;target.parent.mkdir(parents=True,exist_ok=True)
            tmp=target.with_suffix('.mirror.download');tmp.write_bytes(body);tmp.replace(target)
            print('MIRROR MIXTURE VERIFIED',key,sha,flush=True)
    done.append(name);done_path.write_text(json.dumps(done,indent=2))
    path.unlink()
    if all((DATA/'musdb18hq'/key).exists() for key in expected):break
records=[]
for key,wanted in expected.items():
    p=DATA/'musdb18hq'/key
    assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==wanted['sha256'],key
    records.append({'path':key,**wanted})
(ROOT/'logs/all-data.manifest.json').write_text(json.dumps({'status':'verified','files':records,'mirror_revision':REV},indent=2))
print('ALL 50 ORIGINAL MIXTURES VERIFIED',flush=True)
