#!/usr/bin/env python3
"""Restore the exact five source files from the compact Git transport.
All payload/source hashes are checked before any file is written.
Existing different files and symlink paths are never overwritten.
"""
from pathlib import Path
import base64
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PAYLOAD_SHA = '81c11cbcc1e9d6639a51b7191662d729ae064f4a7f832655d5c48ad29cd4f81e'
PARTS = ['SOURCE_BUNDLE.part00.b64', 'SOURCE_BUNDLE.part01.b64', 'SOURCE_BUNDLE.part02.b64']
ALLOWED = {'RUN_ALL.py', 'EXPECTED_OUTPUTS.json', 'src/hereditary_core.cpp', 'src/verify_cut.py', 'src/regression.py'}


def main():
    manifest = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    text = ''.join((ROOT/name).read_text().strip() for name in PARTS)
    raw = base64.b64decode(text, validate=True)
    if hashlib.sha256(raw).hexdigest() != PAYLOAD_SHA:
        raise ValueError('Transport hash mismatch')
    source = json.loads(gzip.decompress(raw))
    if set(source) != ALLOWED or set(manifest['source_files']) != ALLOWED:
        raise ValueError('Unexpected source paths')
    pending = []
    for name in sorted(ALLOWED):
        data = source[name].encode('utf-8')
        expected = manifest['source_files'][name]
        if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
            raise ValueError('Source hash mismatch: '+name)
        path = ROOT/name
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError('Refusing symlink target')
        if path.exists() and path.read_bytes() != data:
            raise ValueError('Refusing to replace a different existing file: '+name)
        pending.append((path, data))
    for path, data in pending:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print('PASS: restored five exact source files')


if __name__ == '__main__':
    main()
