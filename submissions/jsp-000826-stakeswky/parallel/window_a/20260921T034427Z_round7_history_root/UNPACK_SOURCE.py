"""Authenticate and extract the exact A7 source without replacing other bytes."""
import base64, hashlib, io, json, zipfile
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
b=(root/'SOURCE_BUNDLE.b64').read_bytes()
if hashlib.sha256(b).hexdigest()!=m['bundle_sha256']:raise SystemExit('bundle hash mismatch')
a=base64.b64decode(b.strip(),validate=True)
if len(a)!=m['archive_bytes'] or hashlib.sha256(a).hexdigest()!=m['archive_sha256']:raise SystemExit('archive mismatch')
expected={x['path']:x for x in m['files']};ready=[]
with zipfile.ZipFile(io.BytesIO(a)) as z:
    if len(z.namelist())!=len(expected) or set(z.namelist())!=set(expected):raise SystemExit('unexpected source names')
    for name,e in expected.items():
        raw=z.read(name);p=(root/name).resolve()
        if root not in p.parents:raise SystemExit('unsafe path')
        if len(raw)!=e['bytes'] or hashlib.sha256(raw).hexdigest()!=e['sha256']:raise SystemExit('source mismatch')
        raw.decode('utf-8')
        if p.exists() and p.read_bytes()!=raw:raise SystemExit('refuse overwrite of differing source')
        ready.append((p,raw))
for p,raw in ready:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
print('Verified',len(ready),'source files')
