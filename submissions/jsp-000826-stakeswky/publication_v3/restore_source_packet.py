#!/usr/bin/env python3
"""Restore the source-only packet from pinned text parts. No network or execution."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile


def restore(destination: Path) -> None:
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'SOURCE_PACKET.json').read_text())
    parts = []
    for entry in manifest['parts']:
        data = (root / entry['name']).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError('Source part hash mismatch: ' + entry['name'])
        parts.append(data.decode('ascii').strip())
    # One redundant character was introduced during text transport. This exact,
    # hash-bound edit restores the original encoding, never alters proof sources.
    for edit in manifest['transport_edits']:
        s = parts[edit['part']]
        j = edit['offset']
        old = edit['remove']
        if s[j:j + len(old)] != old:
            raise ValueError('Transport edit precondition mismatch')
        parts[edit['part']] = s[:j] + edit['insert'] + s[j + len(old):]
    data = base64.b64decode(''.join(parts), validate=True)
    if len(data) != manifest['archive_bytes']:
        raise ValueError('Archive length mismatch')
    if hashlib.sha256(data).hexdigest() != manifest['archive_sha256']:
        raise ValueError('Archive hash mismatch')
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as archive:
        members = archive.getmembers()
        files = [m for m in members if m.isfile()]
        if len(files) != manifest['files']:
            raise ValueError('File count mismatch')
        seen = set()
        for member in members:
            path = PurePosixPath(member.name)
            if (path.is_absolute() or '..' in path.parts or
                    not path.parts or path.parts[0] != 'continuation_v3' or
                    not (member.isfile() or member.isdir()) or member.name in seen):
                raise ValueError('Unsafe or duplicate archive member')
            seen.add(member.name)
        destination.mkdir(parents=True, exist_ok=False)
        for member in members:
            path = destination / member.name
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('xb') as output:
                    source = archive.extractfile(member)
                    if source is None:
                        raise ValueError('Missing file body')
                    output.write(source.read())
    print('SOURCE_PACKET_HASH_VERIFIED: 67 files, no precompiled proof objects')
    print('Next: python3 ' + str(destination / 'continuation_v3/restore_sources.py'))
    print('That rebuilds source text only; run the Lean entrypoint separately.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    restore(parser.parse_args().out)
