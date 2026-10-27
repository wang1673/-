"""Verify all source mixtures and stop redundant download processes afterwards."""
import hashlib,json,os,signal,time
from pathlib import Path
ROOT=Path('/root/autodl-tmp/polyphonia_repro');DATA=Path('/root/autodl-tmp/polyphonia/musdb18hq')
original=json.loads((ROOT/'logs/original.musdb18hq.manifest.json').read_text())['files']
expected={k:v for k,v in original.items() if k.endswith('/mixture.wav')}
checked={}
while len(checked)<50:
    for key,wanted in expected.items():
        p=DATA/key
        if key in checked or not p.exists():continue
        sha=hashlib.sha256(p.read_bytes()).hexdigest()
        assert sha==wanted['sha256'],key
        checked[key]={'path':key,'sha256':sha,'bytes':p.stat().st_size}
        print('Verified source',len(checked),key,flush=True)
    if len(checked)<50:time.sleep(15)
(ROOT/'logs/all-data.manifest.json').write_text(json.dumps({'status':'verified','track_count':50,'files':list(checked.values()),'validation':'All original full-length mixture WAV SHA256 match the old experiment'},indent=2))
names={'download_stage_data.py','download_remaining_data.py','download_data_mirror.py','run_data_mirror.sh'}
stopped=[]
for p in Path('/proc').iterdir():
    if not p.name.isdigit():continue
    try:args=(p/'cmdline').read_bytes().split(b'\0')
    except OSError:continue
    if any(b'/root/autodl-tmp/polyphonia_repro/scripts/' in a and Path(a.decode(errors='replace')).name in names for a in args):
        try:os.kill(int(p.name),signal.SIGTERM);stopped.append(int(p.name))
        except ProcessLookupError:pass
(ROOT/'logs/data-downloads.finalized.json').write_text(json.dumps({'verified_mixtures':50,'stopped_redundant_download_pids':stopped},indent=2))
print('ALL 50 SOURCE MIXTURES VERIFIED; redundant downloads stopped',flush=True)
