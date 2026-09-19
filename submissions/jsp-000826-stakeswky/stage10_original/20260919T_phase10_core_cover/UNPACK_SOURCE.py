"""Reconstruct hash-verified native source. Stdlib only; no commands executed."""
from pathlib import Path,PurePosixPath
import base64,gzip,hashlib,json
B=Path(__file__).resolve().parent
m=json.loads((B/'SOURCE_BUNDLE_MANIFEST.json').read_text())
encoded=''.join((B/name).read_text().strip() for name in m['parts'])
compressed=base64.b64decode(encoded,validate=True)
assert hashlib.sha256(compressed).hexdigest()==m['payload_sha256']
raw=gzip.decompress(compressed)
assert hashlib.sha256(raw).hexdigest()==m['json_sha256']
files=json.loads(raw)
assert set(files)==set(m['members'])
for name,text in files.items():
    p=PurePosixPath(name)
    assert len(p.parts)==2 and p.parts[0]=='src' and p.suffix=='.py'
    assert hashlib.sha256(text.encode()).hexdigest()==m['members'][name]
    out=B/name;out.parent.mkdir(exist_ok=True);out.write_text(text)
for d in ('inputs','certificates','logs'):(B/d).mkdir(exist_ok=True)
print('PASS: reconstructed',len(files),'source files; no programs executed')
