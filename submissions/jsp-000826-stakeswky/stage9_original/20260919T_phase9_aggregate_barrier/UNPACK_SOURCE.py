"""Verify and reconstruct the compact source bundle without executing it."""
from pathlib import Path
import base64,hashlib,json,lzma
B=Path(__file__).resolve().parent
m=json.loads((B/'SOURCE_BUNDLE_MANIFEST.json').read_text())
encoded=''.join((B/name).read_text().strip() for name in m['parts'])
raw=base64.b64decode(encoded,validate=True)
assert hashlib.sha256(raw).hexdigest()==m['compressed_sha256']
files=json.loads(lzma.decompress(raw))
assert set(files)==set(m['files'])
for name,text in files.items():
    rel=Path(name)
    assert not rel.is_absolute() and '..' not in rel.parts
    data=text.encode();assert hashlib.sha256(data).hexdigest()==m['files'][name]
    p=B/rel;p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():assert p.read_bytes()==data,('refuse overwrite',name)
    else:p.write_bytes(data)
(B/'certificates').mkdir(exist_ok=True)
print('PASS: verified and reconstructed',len(files),'source/input files')
