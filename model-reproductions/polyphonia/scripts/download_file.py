"""Resumable public-file downloader; validates byte ranges and optional checksum."""
import argparse
import concurrent.futures
import hashlib
import os
from pathlib import Path
import re
import time
import urllib.request


def download(url, output, checksum=None, workers=6):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and checksum:
        algo, expected = checksum.split(':', 1)
        h = hashlib.new(algo)
        with output.open('rb') as f:
            for block in iter(lambda: f.read(8 * 1024**2), b''):
                h.update(block)
        if h.hexdigest() == expected:
            print('Already verified:', output, flush=True)
            return
    req = urllib.request.Request(url, headers={'Range': 'bytes=0-0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        cr = r.headers.get('Content-Range', '')
        match = re.fullmatch(r'bytes 0-0/(\d+)', cr)
        if r.status != 206 or not match:
            raise RuntimeError('Server did not honor byte range: %s %s' % (r.status, cr))
        size = int(match.group(1))
        r.read()
    chunksize = 8 * 1024**2
    parts = output.with_name(output.name + '.parts')
    parts.mkdir(exist_ok=True)
    def fetch(i):
        start = i * chunksize
        end = min(size, start + chunksize) - 1
        part = parts / ('%06d' % i)
        if part.exists() and part.stat().st_size == end - start + 1:
            return i
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={'Range': 'bytes=%d-%d' % (start, end)})
                with urllib.request.urlopen(req, timeout=60) as r:
                    expected = 'bytes %d-%d/%d' % (start, end, size)
                    if r.status != 206 or r.headers.get('Content-Range') != expected:
                        raise RuntimeError('Range mismatch: ' + str(r.headers.get('Content-Range')))
                    body = r.read()
                if len(body) != end - start + 1:
                    raise RuntimeError('Truncated range')
                tmp = part.with_suffix('.tmp')
                tmp.write_bytes(body)
                tmp.replace(part)
                return i
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2**attempt)
    n = (size + chunksize - 1) // chunksize
    print('Downloading %s: %.1f MB, %d chunks' % (output.name, size / 1e6, n), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for k, _ in enumerate(pool.map(fetch, range(n)), 1):
            if k % 8 == 0 or k == n:
                print('Chunks complete: %d/%d' % (k, n), flush=True)
    tmp = output.with_name(output.name + '.tmp')
    algo, expected = checksum.split(':', 1) if checksum else ('sha256', None)
    h = hashlib.new(algo)
    with tmp.open('wb') as dst:
        for i in range(n):
            with (parts / ('%06d' % i)).open('rb') as src:
                for block in iter(lambda: src.read(1024**2), b''):
                    dst.write(block)
                    h.update(block)
    actual = h.hexdigest()
    if expected and actual != expected:
        raise RuntimeError('Checksum mismatch: ' + actual)
    tmp.replace(output)
    for part in parts.iterdir():
        part.unlink()
    parts.rmdir()
    print('Verified %s:%s %s' % (algo, actual, output), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('url')
    p.add_argument('output')
    p.add_argument('--checksum')
    p.add_argument('--workers', type=int, default=6)
    a = p.parse_args()
    download(a.url, a.output, a.checksum, a.workers)
