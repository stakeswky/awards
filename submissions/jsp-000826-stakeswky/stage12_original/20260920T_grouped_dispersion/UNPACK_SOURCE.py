#!/usr/bin/env python3
"""Verify and reconstruct this run's UTF-8 sources; refuse conflicting files."""
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import zlib

ROOT = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    manifest = json.loads((ROOT / 'SOURCE_BUNDLE_MANIFEST.json').read_text())
    chunks = []
    for part in manifest['parts']:
        name = part['path']
        if PurePosixPath(name).name != name:
            raise ValueError('Unsafe part path')
        data = (ROOT / name).read_bytes()
        if digest(data) != part['sha256']:
            raise ValueError('Part hash mismatch: ' + name)
        chunks.append(data.strip())
    compressed = base64.b64decode(b''.join(chunks), validate=True)
    if digest(compressed) != manifest['compressed_sha256']:
        raise ValueError('Compressed hash mismatch')
    raw = zlib.decompress(compressed)
    if digest(raw) != manifest['json_sha256']:
        raise ValueError('JSON hash mismatch')
    files = json.loads(raw)
    if set(files) != set(manifest['files']):
        raise ValueError('Source inventory mismatch')
    prepared = []
    for name, text in files.items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or path.parts[0] != 'src':
            raise ValueError('Unsafe source path')
        target = ROOT.joinpath(*path.parts)
        if not target.resolve().is_relative_to(ROOT):
            raise ValueError('Escaping symlink')
        data = text.encode('utf-8')
        if digest(data) != manifest['files'][name]:
            raise ValueError('Source hash mismatch: ' + name)
        if target.exists() and target.read_bytes() != data:
            raise FileExistsError('Refusing to replace different file: ' + name)
        prepared.append((target, data))
    for target, data in prepared:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    print('PASS: verified and reconstructed', len(prepared), 'source files')

if __name__ == '__main__':
    main()
