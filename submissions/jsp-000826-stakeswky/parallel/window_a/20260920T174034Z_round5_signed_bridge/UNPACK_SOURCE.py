"""Extract authenticated source bytes without overwriting differing files."""
import base64, hashlib, io, json, zipfile
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text())
chunks=[]
for part in manifest['parts']:
    raw=(root/part['path']).read_bytes()
    if len(raw)!=part['bytes'] or hashlib.sha256(raw).hexdigest()!=part['sha256']:
        raise SystemExit('Source part mismatch: '+part['path'])
    chunks.append(raw.strip())
archive=base64.b64decode(b''.join(chunks),validate=True)
if hashlib.sha256(archive).hexdigest()!=manifest['archive_sha256']:
    raise SystemExit('Source archive hash mismatch')
expected={f['path']:f for f in manifest['files']}
ready=[]
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    if len(z.namelist())!=len(expected) or set(z.namelist())!=set(expected):
        raise SystemExit('Unexpected source entries')
    for name,item in expected.items():
        dest=(root/name).resolve()
        if root not in dest.parents:raise SystemExit('Unsafe source path')
        raw=z.read(name)
        if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
            raise SystemExit('Source content mismatch: '+name)
        raw.decode('utf-8')
        if dest.exists() and dest.read_bytes()!=raw:
            raise SystemExit('Refusing to replace differing file: '+name)
        ready.append((dest,raw))
for dest,raw in ready:
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
print('Verified and extracted',len(ready),'source files')
