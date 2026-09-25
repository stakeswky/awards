"""Run every check of this audit with fixed configuration and write a receipt.

Usage: python run_all.py --out NEW_EMPTY_DIR [--maxn 23] [--procs 9]

All outputs except RUN_RECEIPT.json are deterministic (ordered aggregation, fixed
seeds, no timings), so a clean re-run can be compared byte for byte.
Standard library only; Python >= 3.10; no network access.
"""
import argparse
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OEIS_A000055 = [1, 1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159, 7741, 19320, 48629, 123867, 317955,
                823065, 2144505, 5623756, 14828074, 39299897]


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--maxn', type=int, default=23)
    ap.add_argument('--procs', type=int, default=9)
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    if os.path.exists(out) and os.listdir(out):
        sys.exit('output directory must be new or empty')
    os.makedirs(os.path.join(out, 'logs'), exist_ok=True)
    P = str(args.procs)
    steps = [
        ('crossvalidation', ['check_crossvalidation.py']),
        ('bounds', ['check_bounds.py', '--nmax', '20', '--procs', P]),
        ('sweep', ['check_sweep.py', '--nmin', '5', '--nmax', str(args.maxn), '--procs', P]),
        ('allj', ['check_allj.py', '--nmin', '4', '--nmax', '19', '--procs', P]),
        ('hubs_closed_form', ['check_hubs_closed_form.py']),
        ('hub_variants', ['check_hub_variants.py', '--procs', P]),
        ('core_family', ['check_core_family.py', '--procs', P]),
        ('near_ties', ['check_near_ties.py', '--procs', P]),
        ('random_climb', ['check_random_climb.py', '--procs', P]),
        ('certificates', ['make_certificates.py']),
    ]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records = []
    status = 'PASS'
    for name, cmd in steps:
        full = [sys.executable, os.path.join(HERE, cmd[0])] + cmd[1:] + ['--out', out]
        t0 = time.time()
        with open(os.path.join(out, 'logs', name + '.stdout.txt'), 'w') as so, open(os.path.join(out, 'logs', name + '.stderr.txt'), 'w') as se:
            rc = subprocess.run(full, stdout=so, stderr=se, cwd=HERE).returncode
        records.append(dict(step=name, command='python src/' + ' '.join(cmd + ['--out', '<OUT>']), exit_code=rc,
                            wall_seconds=round(time.time() - t0, 1),
                            stderr_bytes=os.path.getsize(os.path.join(out, 'logs', name + '.stderr.txt'))))
        print(f'{name}: exit {rc} ({records[-1]["wall_seconds"]}s)', flush=True)
        if rc != 0:
            status = 'FAIL'
    oeis = []
    for n in range(5, args.maxn + 1):
        path = os.path.join(out, 'sweep_n%02d.json' % n)
        if os.path.exists(path):
            with open(path) as fh:
                trees = json.load(fh)['trees']
            oeis.append(dict(n=n, trees=trees, OEIS_A000055=OEIS_A000055[n], equal=(trees == OEIS_A000055[n])))
            if trees != OEIS_A000055[n]:
                status = 'FAIL'
    files = []
    for root, _, names in os.walk(out):
        for nm in sorted(names):
            path = os.path.join(root, nm)
            rel = os.path.relpath(path, out)
            if rel == 'RUN_RECEIPT.json':
                continue
            files.append(dict(file=rel, bytes=os.path.getsize(path), sha256=sha(path)))
    files.sort(key=lambda f: f['file'])
    sources = []
    for root, _, names in os.walk(HERE):
        if '__pycache__' in root:
            continue
        for nm in sorted(names):
            if nm.endswith('.py'):
                path = os.path.join(root, nm)
                sources.append(dict(file=os.path.relpath(path, HERE), bytes=os.path.getsize(path), sha256=sha(path)))
    sources.sort(key=lambda f: f['file'])
    receipt = dict(status=status, started_utc=started, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   python=sys.version.split()[0], platform=platform.platform(), maxn=args.maxn, procs=args.procs,
                   steps=records, sweep_tree_counts_vs_OEIS=oeis, outputs=files, sources=sources,
                   kind='NEW_INDEPENDENT_IMPLEMENTATION_NOT_AUTHOR_REPLAY', lean='NOT_RUN', external_peer_review='NOT_PERFORMED')
    with open(os.path.join(out, 'RUN_RECEIPT.json'), 'w') as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('STATUS', status, '| output files', len(files))
    sys.exit(0 if status == 'PASS' else 1)


if __name__ == '__main__':
    main()
