"""Verify and extract the exact compact C8 source/inputs. No network needed."""
from pathlib import Path
import base64,zlib,json,hashlib
R=Path(__file__).resolve().parent
manifest=json.loads((R/'SOURCE_MANIFEST.json').read_text());chunks=[]
for item in manifest['parts']:
 raw=(R/item['path']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=item['sha256']:raise RuntimeError('Bundle part hash mismatch')
 chunks.append(b''.join(raw.split()))
obj=json.loads(zlib.decompress(base64.b85decode(b''.join(chunks))))
if obj['schema']!=1:raise RuntimeError('Unsupported schema')
for name,rec in obj['files'].items():
 rel=Path(name)
 if rel.is_absolute() or '..' in rel.parts:raise RuntimeError('Unsafe source member')
 data=rec['text'].encode();h=hashlib.sha256(data).hexdigest()
 if h!=rec['sha256'] or h!=manifest['files'][name]:raise RuntimeError('Member hash mismatch')
 dest=R/rel
 if dest.exists() and dest.read_bytes()!=data:raise RuntimeError('Refusing to overwrite differing file '+name)
 dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():dest.write_bytes(data)
 print(name,h)
