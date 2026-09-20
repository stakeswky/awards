"""Verify and extract this package's exact source and compact receipts."""
from pathlib import Path
import base64,hashlib,json,zlib
EXPECTED_BUNDLE_SHA256 = "b1639a44cdc090cb5c4ca697f4bd0368a50834b72af7fd72378235edbde3c7a8"
root=Path(__file__).resolve().parent
raw=(root/'SOURCE_BUNDLE.b85').read_bytes()
if hashlib.sha256(raw).hexdigest()!=EXPECTED_BUNDLE_SHA256:
    raise RuntimeError('Source bundle hash mismatch')
obj=json.loads(zlib.decompress(base64.b85decode(b''.join(raw.split()))))
if obj['schema']!=1:raise RuntimeError('Unknown bundle schema')
for name,record in obj['files'].items():
    rel=Path(name)
    if rel.is_absolute() or '..' in rel.parts:raise RuntimeError('Unsafe member path')
    dst=root/rel;data=record['text'].encode('utf-8')
    if hashlib.sha256(data).hexdigest()!=record['sha256']:raise RuntimeError(name)
    if dst.exists() and dst.read_bytes()!=data:raise RuntimeError('Refusing to overwrite: '+name)
    dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():dst.write_bytes(data)
    print(name,record['sha256'])
