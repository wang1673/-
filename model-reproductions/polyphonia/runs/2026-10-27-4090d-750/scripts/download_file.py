"""Resumable range download with curl transport and complete file hash validation."""
import argparse,concurrent.futures,hashlib,re,subprocess,time,urllib.request
from pathlib import Path

def download(url,output,checksum=None,workers=6,chunk_size=8*1024**2,parts_suffix='.parts'):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    def digest(path,algo='sha256'):
        h=hashlib.new(algo)
        with path.open('rb') as stream:
            for block in iter(lambda:stream.read(8*1024**2),b''):h.update(block)
        return h.hexdigest()
    algo,expected=checksum.split(':',1) if checksum else ('sha256',None)
    if output.exists() and expected and digest(output,algo)==expected:
        print('Already verified:',output,flush=True);return
    probe=output.with_name(output.name+'.probe.headers')
    result=subprocess.run(['curl','-sS','-L','--fail','--connect-timeout','10','--max-time','90','--range','0-0','-D',str(probe),'-o','/dev/null',url],capture_output=True)
    headers=probe.read_text(errors='replace') if probe.exists() else ''
    probe.unlink(missing_ok=True)
    if result.returncode:raise RuntimeError('Range probe failed: '+result.stderr.decode(errors='replace')[-200:])
    sizes=re.findall(r'content-range:\s*bytes 0-0/(\d+)',headers,re.I)
    assert sizes,headers[-300:]
    size=int(sizes[-1]);parts=output.with_name(output.name+parts_suffix);parts.mkdir(exist_ok=True)
    count=(size+chunk_size-1)//chunk_size
    print('Downloading %s: %.1f MB, %d chunks (curl)'%(output.name,size/1e6,count),flush=True)
    def fetch(index):
        start=index*chunk_size;end=min(size,start+chunk_size)-1
        part=parts/('%06d'%index)
        if part.exists() and part.stat().st_size==end-start+1:return
        tmp=part.with_suffix('.tmp');head=part.with_suffix('.headers')
        for attempt in range(8):
            try:
                result=subprocess.run(['curl','-sS','-L','--fail','--connect-timeout','10','--max-time','180','--range','%d-%d'%(start,end),'-D',str(head),'-o',str(tmp),url],capture_output=True)
                headers=head.read_text(errors='replace') if head.exists() else ''
                if result.returncode:raise RuntimeError(result.stderr.decode(errors='replace')[-200:])
                values=re.findall(r'content-range:\s*(bytes [^\r\n]+)',headers,re.I)
                assert values and values[-1]=='bytes %d-%d/%d'%(start,end,size),values
                assert tmp.stat().st_size==end-start+1
                tmp.replace(part);head.unlink(missing_ok=True);return
            except Exception as exc:
                if attempt==7:raise
                delays=re.findall(r'retry-after:\s*(\d+)',headers,re.I)
                time.sleep(min(60,int(delays[-1])) if delays else min(20,2**attempt))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for k,_ in enumerate(pool.map(fetch,range(count)),1):
            if k%16==0 or k==count:print('Chunks complete: %d/%d'%(k,count),flush=True)
    tmp=output.with_name(output.name+'.tmp');h=hashlib.new(algo)
    with tmp.open('wb') as dst:
        for i in range(count):
            with (parts/('%06d'%i)).open('rb') as src:
                for block in iter(lambda:src.read(1024**2),b''):dst.write(block);h.update(block)
    actual=h.hexdigest();assert not expected or actual==expected,('Checksum mismatch',actual,expected)
    tmp.replace(output)
    for p in parts.iterdir():p.unlink()
    parts.rmdir()
    print('Verified %s:%s %s'%(algo,actual,output),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('output');p.add_argument('--checksum');p.add_argument('--workers',type=int,default=6);a=p.parse_args();download(a.url,a.output,a.checksum,a.workers)
