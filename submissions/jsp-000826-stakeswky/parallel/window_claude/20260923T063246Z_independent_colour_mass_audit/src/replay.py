"""Clean-source replay: copy ONLY the source files into a new directory, run
run_all.py there, and compare every output with a reference run byte for byte.

Usage: python replay.py --reference REF_OUT_DIR --workdir NEW_DIR [--maxn 21] [--procs 9]

With --maxn smaller than the reference run, per-order sweep files above maxn are
simply not produced; the sweep and certificate logs are then compared as prefixes.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PREFIX_LOGS = {'logs/sweep.stdout.txt', 'logs/certificates.stdout.txt'}


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reference', required=True)
    ap.add_argument('--workdir', required=True)
    ap.add_argument('--maxn', type=int, default=21)
    ap.add_argument('--procs', type=int, default=9)
    args = ap.parse_args()
    work = os.path.abspath(args.workdir)
    if os.path.exists(work):
        sys.exit('workdir must not exist')
    src = os.path.join(work, 'src')
    for root, _, names in os.walk(HERE):
        if '__pycache__' in root:
            continue
        for nm in names:
            if nm.endswith('.py'):
                rel = os.path.relpath(os.path.join(root, nm), HERE)
                os.makedirs(os.path.dirname(os.path.join(src, rel)), exist_ok=True)
                shutil.copy2(os.path.join(root, nm), os.path.join(src, rel))
    out = os.path.join(work, 'out')
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rc = subprocess.run([sys.executable, os.path.join(src, 'run_all.py'), '--out', out, '--maxn', str(args.maxn),
                         '--procs', str(args.procs)], cwd=src).returncode
    ref = os.path.abspath(args.reference)
    rows = []
    ok = rc == 0
    for root, _, names in os.walk(out):
        for nm in sorted(names):
            rel = os.path.relpath(os.path.join(root, nm), out)
            if rel == 'RUN_RECEIPT.json':
                continue
            a = os.path.join(out, rel)
            b = os.path.join(ref, rel)
            if not os.path.exists(b):
                rows.append(dict(file=rel, result='MISSING_IN_REFERENCE'))
                ok = False
                continue
            ab, bb = open(a, 'rb').read(), open(b, 'rb').read()
            if ab == bb:
                res = 'BYTE_EQUAL'
            elif rel in PREFIX_LOGS and bb.startswith(ab):
                res = 'PREFIX_OF_REFERENCE'
            else:
                res = 'DIFFERENT'
                ok = False
            rows.append(dict(file=rel, result=res, bytes=len(ab), sha256=sha(a)))
    rows.sort(key=lambda r: r['file'])
    not_replayed = sorted(os.path.relpath(os.path.join(r, n), ref) for r, _, ns in os.walk(ref) for n in ns
                          if not os.path.exists(os.path.join(out, os.path.relpath(os.path.join(r, n), ref)))
                          and n != 'RUN_RECEIPT.json')
    rec = dict(status='PASS' if ok else 'FAIL', started_utc=started, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               run_all_exit_code=rc, maxn=args.maxn, source_only_clean_copy=True, compared=rows,
               byte_equal=sum(r['result'] == 'BYTE_EQUAL' for r in rows),
               prefix_equal=sum(r['result'] == 'PREFIX_OF_REFERENCE' for r in rows),
               different=sum(r['result'] == 'DIFFERENT' for r in rows), reference_files_not_replayed=not_replayed)
    with open(os.path.join(work, 'REPLAY.json'), 'w') as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('REPLAY', rec['status'], 'byte_equal', rec['byte_equal'], 'prefix_equal', rec['prefix_equal'], 'different', rec['different'],
          'not_replayed', len(not_replayed))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
