"""Retrieve a raw-WAV mirror and verify all bytes against official ZIP CRCs."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import time
import zlib
from huggingface_hub import hf_hub_download, snapshot_download
import pyarrow.parquet as pq

root = Path('/home/featurize/work/polyphonia_repro')
data = Path('/home/featurize/data/polyphonia')
plan = json.loads((root / 'scripts/musdb_test_plan.json').read_text())
expected = {e['path']: e for e in plan['entries']}
repo_id = 'danjacobellis/musdb18HQ'
revision = '7950781147516a3b1411310274175ff98ab8f062'
cache = data / 'hf-cache'
destination = data / 'musdb18hq'
records = {}
started = time.monotonic()

def extract(shard):
    for batch in pq.ParquetFile(shard).iter_batches(batch_size=1, columns=['audio', 'path', 'instrument']):
        for row in batch.to_pylist():
            parts = PurePosixPath(row['path']).parts
            assert 'test' in parts, row['path']
            name = '/'.join(parts[parts.index('test'):])
            assert name in expected and name not in records, name
            info = expected[name]
            body = row['audio']['bytes']
            assert body is not None
            assert len(body) == info['size'], ('File size differs from official WAV', name, len(body), info['size'])
            crc = zlib.crc32(body)
            assert crc == info['crc32'], ('CRC differs from official WAV', name, crc, info['crc32'])
            assert body[:4] == b'RIFF' and body[8:12] == b'WAVE'
            target = destination.joinpath(*PurePosixPath(name).parts)
            assert destination.resolve() in target.resolve().parents
            target.parent.mkdir(parents=True, exist_ok=True)
            tmp = target.with_suffix('.wav.download')
            tmp.write_bytes(body)
            tmp.replace(target)
            record = {'path': name, 'size': len(body), 'crc32': crc,
                      'sha256': hashlib.sha256(body).hexdigest()}
            records[name] = record
    print('Verified shard:', Path(shard).name, 'files:', len(records), flush=True)

# Validate one shard before committing to downloading the remainder.
first = hf_hub_download(repo_id, 'data/validation-00000-of-00022.parquet',
                        repo_type='dataset', revision=revision, cache_dir=str(cache))
extract(first)
for attempt in range(8):
    try:
        snapshot = snapshot_download(repo_id, repo_type='dataset', revision=revision,
                                     allow_patterns=['data/validation-*.parquet'],
                                     cache_dir=str(cache), max_workers=3)
        break
    except Exception as exc:
        print('Download attempt failed:', attempt + 1, type(exc).__name__, flush=True)
        if attempt == 7:
            raise
        time.sleep(10)
for shard in sorted((Path(snapshot) / 'data').glob('validation-*.parquet')):
    if shard.name != Path(first).name:
        extract(shard)
assert set(records) == set(expected), (len(records), len(expected))
assert len({n.split('/')[1] for n in records}) == 50
manifest = {'status': 'verified', 'official_source': plan['url'],
            'official_archive_size': plan['archive_size'],
            'validation': 'Every WAV size and CRC32 matches official ZIP central directory; WAV SHA256 recorded',
            'mirror': repo_id, 'mirror_revision': revision,
            'root': str(destination), 'track_count': 50, 'file_count': len(records),
            'total_bytes': sum(r['size'] for r in records.values()),
            'elapsed_seconds': time.monotonic()-started, 'files': records}
(root / 'logs/musdb18hq.manifest.json').write_text(json.dumps(manifest, indent=2))
(data / 'musdb18hq.manifest.json').write_text(json.dumps(manifest, indent=2))
print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}, indent=2), flush=True)
