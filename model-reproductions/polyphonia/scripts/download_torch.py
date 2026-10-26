import html
import re
import urllib.parse
import urllib.request
from pathlib import Path
from download_file import download

wheelhouse = Path('/home/featurize/data/polyphonia/runtime/wheelhouse')
for package, version in [('torch', '2.4.1'), ('torchaudio', '2.4.1'), ('torchvision', '0.19.1')]:
    index = 'https://download.pytorch.org/whl/cu124/' + package + '/'
    page = urllib.request.urlopen(index, timeout=60).read().decode()
    target = '%s-%s+cu124-cp38-cp38-linux_x86_64.whl' % (package, version)
    matches = [html.unescape(u) for u in re.findall(r'href="([^"]+)"', page)
               if urllib.parse.unquote(u).split('#')[0].endswith('/' + target)]
    assert len(matches) == 1, (target, matches)
    u = urllib.parse.urljoin(index, matches[0])
    split = urllib.parse.urlsplit(u)
    checksum = split.fragment.replace('=', ':', 1)
    assert checksum.startswith('sha256:')
    # Both hosts are official; the legacy CDN is faster from this server.
    u = urllib.parse.urlunsplit(('https', 'download.pytorch.org', split.path, split.query, ''))
    download(u, wheelhouse / target, checksum)
