import json
from pathlib import Path
import re
import hashlib
import zlib
import soundfile as sf

root = Path('/home/featurize/work/polyphonia_repro')
manifest = json.loads((root / 'logs/musdb18hq.manifest.json').read_text())
assert manifest['status'] == 'verified' and manifest['file_count'] == 250
base = Path(manifest['root'])
info = []
for name, expected in manifest['files'].items():
    p = base / name
    assert p.stat().st_size == expected['size'], name
    digest = hashlib.sha256()
    crc = 0
    with p.open('rb') as source:
        for block in iter(lambda: source.read(4 * 1024 * 1024), b''):
            digest.update(block)
            crc = zlib.crc32(block, crc)
    assert crc == expected['crc32'] and digest.hexdigest() == expected['sha256'], name
    s = sf.info(str(p))
    assert s.samplerate == 44100 and s.channels == 2, (name, str(s))
    info.append({'path': name, 'frames': s.frames, 'samplerate': s.samplerate,
                 'channels': s.channels, 'subtype': s.subtype,
                 'duration_seconds': s.duration})
    partial = p.with_suffix('.wav.part')
    if partial.exists():
        partial.unlink()
tracks = sorted({x['path'].split('/')[1] for x in info})
assert len(tracks) == 50
for track in tracks:
    entries = [x for x in info if x['path'].split('/')[1] == track]
    assert len(entries) == 5 and len({x['frames'] for x in entries}) == 1, track
prompts = root / 'polyphonia/PolyEvalPrompts/musdb18_test'
normalize = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
mapping, missing = [], []
for prompt in sorted(prompts.glob('*/prompt_multi.json')):
    candidates = [t for t in tracks if t == prompt.parent.name]
    match_type = 'exact'
    if not candidates:
        candidates = [t for t in tracks if normalize(t) == normalize(prompt.parent.name)]
        match_type = 'normalized_unique'
    if len(candidates) != 1:
        missing.append({'prompt': str(prompt), 'candidates': candidates})
        continue
    tasks = json.loads(prompt.read_text())
    mapping.append({'prompt_track': prompt.parent.name, 'audio_track': candidates[0],
                    'match_type': match_type, 'task_count': len(tasks),
                    'prompt_file': str(prompt),
                    'mixture': str(base / 'test' / candidates[0] / 'mixture.wav')})
report = {'status': 'passed' if not missing else 'mapping_review_required',
          'root': str(base), 'track_count': len(tracks), 'file_count': len(info),
          'sample_rate': 44100, 'channels': 2,
          'total_mixture_hours': sum(x['duration_seconds'] for x in info
                                     if x['path'].endswith('/mixture.wav'))/3600,
          'mapped_prompt_tracks': len(mapping),
          'mapped_tasks': sum(x['task_count'] for x in mapping),
          'missing_or_ambiguous': missing, 'mapping': mapping, 'audio_info': info}
(root / 'logs/musdb18hq.audit.json').write_text(json.dumps(report, indent=2))
print(json.dumps({k: v for k, v in report.items() if k not in ['mapping','audio_info']}, indent=2))
assert not missing, 'Track mapping requires review'
assert len(mapping) == 50 and report['mapped_tasks'] == 750, 'Incomplete prompt mapping'
