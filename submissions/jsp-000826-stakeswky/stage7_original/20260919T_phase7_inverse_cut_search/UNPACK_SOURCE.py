"""Validate and extract the complete source/input archive from committed parts."""
from pathlib import Path
import hashlib,io,json,tarfile
BASE=Path(__file__).resolve().parent
manifest=json.loads((BASE/'SOURCE_BUNDLE_MANIFEST.json').read_text())
chunks=[]
for part in manifest['parts']:
    data=(BASE/part['path']).read_bytes()
    if len(data)!=part['bytes'] or hashlib.sha256(data).hexdigest()!=part['sha256']:
        raise ValueError('Archive part mismatch: '+part['path'])
    chunks.append(data)
raw=b''.join(chunks)
if len(raw)!=manifest['archive_bytes'] or hashlib.sha256(raw).hexdigest()!=manifest['archive_sha256']:
    raise ValueError('Full archive mismatch')
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:xz') as archive:
    for member in archive.getmembers():
        relative=Path(member.name)
        if not member.isfile() or relative.is_absolute() or '..' in relative.parts or relative.parts[0] not in ('src','sources'):
            raise ValueError('Unexpected archive path')
        target=BASE/relative
        data=archive.extractfile(member).read()
        if target.exists() and target.read_bytes()!=data:
            raise ValueError('Refusing to overwrite a modified file: '+member.name)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
for name in ['certificates','logs']:
    (BASE/name).mkdir(exist_ok=True)
print('PASS: source and inputs unpacked; existing modifications were not overwritten.')
