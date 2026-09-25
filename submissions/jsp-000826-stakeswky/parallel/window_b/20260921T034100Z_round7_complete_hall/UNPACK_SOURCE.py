"""Verify all payload bytes and paths before writing; do not overwrite differing files."""
from pathlib import Path
import base64,hashlib,json,lzma
root=Path(__file__).resolve().parent
m=json.loads((root/'SOURCE_MANIFEST.json').read_text());chunks=[]
for item in m['parts']:
 p=root/item['path'];b=p.read_bytes()
 if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256']:raise SystemExit('Payload part mismatch: '+item['path'])
 chunks.append(b.decode().strip())
raw=base64.b64decode(''.join(chunks),validate=True)
if len(raw)!=m['compressed_bytes'] or hashlib.sha256(raw).hexdigest()!=m['compressed_sha256']:raise SystemExit('Compressed payload mismatch')
entries=json.loads(lzma.decompress(raw));expected={x['path']:x for x in m['files']}
if len(entries)!=len(expected) or {x['path'] for x in entries}!=set(expected):raise SystemExit('Unexpected payload entries')
ready=[]
for item in entries:
 name=item['path'];p=(root/name).resolve();b=item['text'].encode();e=expected[name]
 if root not in p.parents:raise SystemExit('Unsafe output path')
 if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise SystemExit('Payload file mismatch: '+name)
 if p.exists() and p.read_bytes()!=b:raise SystemExit('Refusing different existing file: '+name)
 ready.append((p,b))
for p,b in ready:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
print('Verified and reconstructed',len(ready),'files.')
