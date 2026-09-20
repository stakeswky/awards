"""Recover verified source, refusing to overwrite differing existing files."""
from pathlib import Path
import hashlib,base64,zipfile,io,json
root=Path(__file__).resolve().parent
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
text=''.join((root/p['path']).read_text().strip() for p in m['parts'])
b=base64.b64decode(text,validate=True)
if len(b)!=m['archive_bytes'] or hashlib.sha256(b).hexdigest()!=m['archive_sha256']:raise SystemExit('Source archive mismatch')
with zipfile.ZipFile(io.BytesIO(b)) as z:
    if set(z.namelist())!={f['path'] for f in m['files']}:raise SystemExit('Unexpected source entries')
    pending=[]
    for f in m['files']:
        p=(root/f['path']).resolve();d=z.read(f['path'])
        if root not in p.parents:raise SystemExit('Unsafe path')
        if len(d)!=f['bytes'] or hashlib.sha256(d).hexdigest()!=f['sha256']:raise SystemExit('Source hash mismatch')
        if p.exists() and p.read_bytes()!=d:raise SystemExit('Refusing differing existing file: '+str(p))
        pending.append((p,d))
    for p,d in pending:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(d)
print('Verified',len(pending),'source files')
