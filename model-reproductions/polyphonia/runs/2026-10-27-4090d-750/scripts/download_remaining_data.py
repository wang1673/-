"""Download only the remaining official mixture WAVs needed by the 750-task run."""
import concurrent.futures, hashlib, json, struct, time, urllib.request, zlib
from pathlib import Path
ROOT=Path('/root/autodl-tmp/polyphonia_repro')
DATA=Path('/root/autodl-tmp/polyphonia')
protocol=json.loads((ROOT/'results/musdb_center10_htdemucs_4090d_01/protocol.json').read_text())
plan=json.loads((ROOT/'scripts/musdb_test_plan.json').read_text())
original=json.loads((ROOT/'logs/original.musdb18hq.manifest.json').read_text())['files']
names={t['track'] for t in protocol['tracks'][14:]}
entries=[e for e in plan['entries'] if e['path'].endswith('/mixture.wav') and e['path'].split('/')[1] in names]
assert len(entries)==36

def fetch(e):
    name=e['path']; target=DATA/'musdb18hq'/name
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==original[name]['sha256']:
        return {'path':name,'sha256':original[name]['sha256'],'bytes':target.stat().st_size}
    for attempt in range(6):
        try:
            start=e['offset']; end=start+e['compressed_size']+65565
            def piece(bounds):
                lo,hi=bounds
                for retry in range(6):
                    try:
                        req=urllib.request.Request(plan['url'],headers={'User-Agent':'curl/8.5.0','Range':'bytes=%d-%d'%(lo,hi)})
                        with urllib.request.urlopen(req,timeout=90) as response:
                            assert response.status==206,response.status
                            assert response.headers['Content-Range']=='bytes %d-%d/%d'%(lo,hi,plan['archive_size'])
                            chunk=response.read()
                        assert len(chunk)==hi-lo+1
                        return chunk
                    except Exception:
                        if retry==5:raise
                        time.sleep(5)
            chunk_size=2*1024**2
            spans=[(lo,min(lo+chunk_size-1,end)) for lo in range(start,end+1,chunk_size)]
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as chunks:
                body=b''.join(chunks.map(piece,spans))
            assert len(body)==end-start+1
            assert body[:4]==b'PK\x03\x04'
            filename_len,extra_len=struct.unpack_from('<HH',body,26)
            offset=30+filename_len+extra_len
            encoded=body[30:30+filename_len].decode('utf-8')
            assert encoded==name,(encoded,name)
            compressed=body[offset:offset+e['compressed_size']]
            raw=zlib.decompress(compressed,-15) if e['method']==8 else compressed
            assert len(raw)==e['size'] and zlib.crc32(raw)==e['crc32']
            sha=hashlib.sha256(raw).hexdigest()
            assert sha==original[name]['sha256'],name
            target.parent.mkdir(parents=True,exist_ok=True)
            tmp=target.with_suffix('.download'); tmp.write_bytes(raw);tmp.replace(target)
            record={'path':name,'bytes':len(raw),'sha256':sha,'crc32':e['crc32']}
            print(json.dumps(record),flush=True)
            return record
        except Exception as exc:
            print('retry',attempt+1,name,repr(exc),flush=True)
            if attempt==5:raise
            time.sleep(min(2**attempt,20))

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records=list(pool.map(fetch,entries))
(ROOT/'logs/remaining-data.manifest.json').write_text(json.dumps({'status':'verified','source':plan['url'],'tracks':36,'files':records,'note':'All 36 mixture WAV SHA256 match original experiment'},indent=2))
print('ALL 36 MIXTURES VERIFIED',flush=True)
