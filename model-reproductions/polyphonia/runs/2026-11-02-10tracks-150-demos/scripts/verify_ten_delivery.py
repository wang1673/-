import hashlib,json
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).resolve().parent.parent/'outputs/Polyphonia_10首150项编辑对照'
manifest=json.loads((P/'manifest.sha256.json').read_text())
for name,h in manifest.items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h,name
class Check(HTMLParser):
 def __init__(self,base):super().__init__();self.base=base;self.audio=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='audio':assert (self.base/a['src']).is_file(),a;self.audio+=1
  if tag=='a' and 'href' in a and not a['href'].startswith(('http','https','#')):assert (self.base/a['href']).exists(),a
audio=0
for f in P.rglob('*.html'):
 parser=Check(f.parent);parser.feed(f.read_text());audio+=parser.audio
summary=json.loads((P/'summary.json').read_text());audit=json.loads((P/'final.audit.json').read_text())
assert summary['generated_tasks']==summary['evaluated_tasks']==150 and audit['status']=='passed'
assert len(list((P/'tracks').glob('*/audio/*_raw.wav')))==150
print(json.dumps({'status':'passed','files_hashed':len(manifest),'audio_elements':audio,'html_pages':len(list(P.rglob('*.html'))),'raw_outputs':150,'generated_tasks':150,'evaluated_tasks':150}))
