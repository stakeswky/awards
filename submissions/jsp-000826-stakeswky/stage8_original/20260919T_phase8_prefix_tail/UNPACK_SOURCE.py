#!/usr/bin/env python3
"""Reconstruct the exact native source/input files without unsafe extraction."""
from pathlib import Path, PurePosixPath
import base64, hashlib, io, json, lzma, tarfile
BASE=Path(__file__).resolve().parent

def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    manifest=json.loads((BASE/'SOURCE_BUNDLE_MANIFEST.json').read_text())
    chunks=[]
    for row in manifest['parts']:
        data=(BASE/row['path']).read_bytes()
        assert sha(data)==row['sha256'] and len(data)==row['bytes'],row['path']
        chunks.append(data)
    blob=base64.b64decode(b''.join(chunks),validate=True)
    assert sha(blob)==manifest['archive_sha256'] and len(blob)==manifest['archive_bytes']
    with tarfile.open(fileobj=io.BytesIO(lzma.decompress(blob)),mode='r:') as tar:
        members=tar.getmembers(); assert len(members)==len(manifest['files'])
        assert {m.name for m in members}==set(manifest['files'])
        for m in members:
            name=PurePosixPath(m.name)
            assert m.isfile() and not name.is_absolute() and '..' not in name.parts
            data=tar.extractfile(m).read(); rec=manifest['files'][m.name]
            assert len(data)==rec['bytes'] and sha(data)==rec['sha256'],m.name
            dest=BASE.joinpath(*name.parts)
            assert BASE in dest.resolve().parents
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    (BASE/'certificates').mkdir(exist_ok=True)
    print('PASS: all native source/input hashes verified and reconstructed')
if __name__=='__main__': main()
