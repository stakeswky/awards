"""Verify and reconstruct the complete executable payload without overwrites."""
from pathlib import Path
import base64,hashlib,json,lzma
root=Path(__file__).resolve().parent
m=json.loads((root/'SOURCE_MANIFEST.json').read_text())
chunks=[]
for item in m['parts']:
 p=root/item['path'];data=p.read_bytes()
 if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:raise SystemExit('Bad payload part: '+item['path'])
 chunks.append(data.decode().strip())
raw=base64.b64decode(''.join(chunks),validate=True)
if len(raw)!=m['compressed_bytes'] or hashlib.sha256(raw).hexdigest()!=m['compressed_sha256']:raise SystemExit('Compressed payload mismatch')
entries=json.loads(lzma.decompress(raw).decode());expected={e['path']:e for e in m['files']}
if len(entries)!=len(expected) or {e['path'] for e in entries}!=set(expected):raise SystemExit('Unexpected entries')
ready=[]
for e in entries:
 p=(root/e['path']).resolve();b=e['text'].encode();x=expected[e['path']]
 if root not in p.parents:raise SystemExit('Unsafe path')
 if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:raise SystemExit('File mismatch: '+e['path'])
 if p.exists() and p.read_bytes()!=b:raise SystemExit('Refusing differing existing file: '+e['path'])
 ready.append((p,b))
for p,b in ready:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
print('Verified and reconstructed',len(ready),'files.')
