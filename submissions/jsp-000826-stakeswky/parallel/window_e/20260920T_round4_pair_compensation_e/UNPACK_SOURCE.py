"""Reconstruct and hash-check both exact source files before writing.
The archived payload has one documented transport-byte correction.
Unexpected payloads and different existing source files are rejected.
"""
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent
WIRE_SHA = '5041a4f8eaf11c61d1b03e272608da22a1010b4b15c5fbeec1ea76fe4ab65d90'
GZIP_SHA = 'bb456a946a8e8e351181eb24942200bb8524d43cd54e111ccd71b8b0b79b0181'
EXPECTED = {
    'src/forest_counts.py': '59eb6612f0ceffb5cf3d974296746c3b4800d9915e832a096f93bd7ee0e43618',
    'src/verify.py': '43399d9d8181453fcc7f5b519209bd32379fa3490c5dcebc3d36e9423aba9452',
}

def main():
    wire = (ROOT / 'SOURCE_PAYLOAD.bin').read_bytes()
    if hashlib.sha256(wire).hexdigest() != WIRE_SHA:
        raise ValueError('Unexpected archived payload')
    data = bytearray(wire)
    if len(data) != 9618 or data[6756] != 20:
        raise ValueError('Transport correction precondition failed')
    data[6756] = 124
    if hashlib.sha256(data).hexdigest() != GZIP_SHA:
        raise ValueError('Corrected payload hash mismatch')
    files = json.loads(gzip.decompress(data))
    if set(files) != set(EXPECTED):
        raise ValueError('Unexpected source paths')
    prepared = []
    for name, expected in EXPECTED.items():
        raw = files[name].encode('utf-8')
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Source hash mismatch: ' + name)
        path = ROOT / name
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError('Refusing symlink target')
        if path.exists() and path.read_bytes() != raw:
            raise ValueError('Refusing to overwrite different source: ' + name)
        prepared.append((path, raw))
    for path, raw in prepared:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    print('PASS: both exact source files reconstructed and verified')

if __name__ == '__main__':
    main()
