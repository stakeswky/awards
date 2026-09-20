"""Reconstruct verified source bytes; never overwrite a differing existing file."""
import base64,hashlib,io,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text())
raw=base64.b64decode((root/'SOURCE_BUNDLE.b64').read_text().strip(),validate=True)
if hashlib.sha256(raw).hexdigest()!=manifest['archive_sha256']:
    raise SystemExit('Source archive SHA-256 mismatch.')
expected={x['path']:x for x in manifest['files']}
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    if set(z.namelist())!=set(expected):raise SystemExit('Unexpected source entries.')
    recovered=[]
    for name,item in expected.items():
        target=(root/name).resolve()
        if root not in target.parents:raise SystemExit('Unsafe archive path.')
        data=z.read(name)
        if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise SystemExit('Source file mismatch: '+name)
        if target.exists() and target.read_bytes()!=data:
            raise SystemExit('Refusing to replace differing file: '+name)
        recovered.append((target,data))
    for target,data in recovered:
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
print('Verified and reconstructed',len(expected),'source files.')
