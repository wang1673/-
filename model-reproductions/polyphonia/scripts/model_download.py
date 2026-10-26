import json
import os
from pathlib import Path
from huggingface_hub import snapshot_download

root = Path(os.environ['POLYPHONIA_ROOT'])
metadata = json.loads((root / 'logs/model.api.json').read_text())
snapshot = snapshot_download(
    repo_id='cvssp/audioldm2', revision='main',
    ignore_patterns=['*.bin', '*.md', '.gitattributes'], max_workers=4,
)
assert Path(snapshot).name == metadata['sha'], 'Upstream revision changed; stop for review'
record = {'repo_id': 'cvssp/audioldm2', 'revision': Path(snapshot).name, 'snapshot': snapshot}
(root / 'logs/model.snapshot.json').write_text(json.dumps(record, indent=2))
print(json.dumps(record, indent=2), flush=True)
