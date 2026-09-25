"""Exhaustive middle-range sweep over ALL free trees of each order n.

For every tree T and every j with h+1<=j<beta and History(T,j-1) (the project's
remaining middle range), record S=a(b-a), Dmass, and min over leaf edges e of the
exact C10 deficit delta_e. Count violations of Dmass<=S and of exists-e delta_e<=S
(plateaus S=0 are reported separately and count as violations if Dmass>0 or all
delta_e>0). Aggregation is ordered, so outputs are deterministic; no timings are
written to the JSON files.

Usage: python check_sweep.py --nmin 5 --nmax 23 --out DIR [--procs 9]
"""
import argparse
import json
import os
import sys
from fractions import Fraction as Fr
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402

KEEP = 50


def work(chunk):
    st = dict(trees=0, dom_trees=0, cases=0, plateau=0, nonunimodal=0, nonLC_in_domain=0,
              D_viol=0, delta_viol=0, maxD=None, maxDelta=None,
              plateau_cases=[], D_viol_cases=[], delta_viol_cases=[], nonunimodal_trees=[])
    for lv in chunk:
        par = L.parents_from_levels(lv)
        st['trees'] += 1
        p, meta, recs = L.analyse(par)
        if not L.is_unimodal(p):
            st['nonunimodal'] += 1
            if len(st['nonunimodal_trees']) < KEEP:
                st['nonunimodal_trees'].append(dict(levels=list(lv), p=p))
        if not recs:
            continue
        st['dom_trees'] += 1
        for r in recs:
            st['cases'] += 1
            if r['LC'] < 0:
                st['nonLC_in_domain'] += 1
            info = dict(levels=list(lv), j=r['j'], b=r['b'], a=r['a'], c=r['c'], S=r['S'],
                        Dmass=r['Dmass'], min_delta=r['min_delta'], alpha_h_beta_first=list(meta))
            if r['S'] == 0:
                st['plateau'] += 1
                if len(st['plateau_cases']) < KEEP:
                    st['plateau_cases'].append(info)
                if r['Dmass'] > 0:
                    st['D_viol'] += 1
                    if len(st['D_viol_cases']) < KEEP:
                        st['D_viol_cases'].append(info)
                if r['min_delta'] > 0:
                    st['delta_viol'] += 1
                    if len(st['delta_viol_cases']) < KEEP:
                        st['delta_viol_cases'].append(info)
                continue
            rd = Fr(r['Dmass'], r['S'])
            rm = Fr(r['min_delta'], r['S'])
            if st['maxD'] is None or rd > st['maxD'][0]:
                st['maxD'] = (rd, info)
            if st['maxDelta'] is None or rm > st['maxDelta'][0]:
                st['maxDelta'] = (rm, info)
            if r['Dmass'] > r['S']:
                st['D_viol'] += 1
                if len(st['D_viol_cases']) < KEEP:
                    st['D_viol_cases'].append(info)
            if r['min_delta'] > r['S']:
                st['delta_viol'] += 1
                if len(st['delta_viol_cases']) < KEEP:
                    st['delta_viol_cases'].append(info)
    return st


def merge(a, b):
    for k in ('trees', 'dom_trees', 'cases', 'plateau', 'nonunimodal', 'nonLC_in_domain', 'D_viol', 'delta_viol'):
        a[k] += b[k]
    for k in ('maxD', 'maxDelta'):
        if b[k] is not None and (a[k] is None or b[k][0] > a[k][0]):
            a[k] = b[k]
    for k in ('plateau_cases', 'D_viol_cases', 'delta_viol_cases', 'nonunimodal_trees'):
        a[k] = (a[k] + b[k])[:KEEP]
    return a


def chunker(n, size):
    buf = []
    for lv in L.free_trees(n):
        buf.append(tuple(lv))
        if len(buf) == size:
            yield buf
            buf = []
    if buf:
        yield buf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nmin', type=int, required=True)
    ap.add_argument('--nmax', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--procs', type=int, default=9)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for n in range(args.nmin, args.nmax + 1):
        tot = None
        with Pool(args.procs) as pool:
            gen = chunker(n, 5000)
            done = False
            while not done:
                batch = []
                for _ in range(90):
                    try:
                        batch.append(next(gen))
                    except StopIteration:
                        done = True
                        break
                for st in pool.imap(work, batch):  # ordered => deterministic witnesses
                    tot = st if tot is None else merge(tot, st)
        for k in ('maxD', 'maxDelta'):
            if tot[k] is not None:
                fr, case = tot[k]
                tot[k] = dict(ratio=f'{fr.numerator}/{fr.denominator}', ratio_float=float(fr), case=case)
        tot['n'] = n
        tot['scope'] = ('all free trees of order n; j with h+1<=j<beta and History(T,j-1); '
                        'Dmass with the root colour class as L (global swap invariant for trees); '
                        'min_delta = min over all leaf edges of the C10 cut deficit')
        with open(os.path.join(args.out, f'sweep_n{n:02d}.json'), 'w') as fh:
            json.dump(tot, fh, sort_keys=True, separators=(',', ':'), default=str)
            fh.write('\n')
        md = tot['maxD']['ratio_float'] if tot['maxD'] else None
        mm = tot['maxDelta']['ratio_float'] if tot['maxDelta'] else None
        print(f"n={n} trees={tot['trees']} domain_trees={tot['dom_trees']} domain_cases={tot['cases']} "
              f"plateaus={tot['plateau']} nonunimodal_trees={tot['nonunimodal']} nonLC_in_domain={tot['nonLC_in_domain']} "
              f"Dmass>S={tot['D_viol']} min_delta>S={tot['delta_viol']} max_Dmass/S={md} max_min_delta/S={mm}", flush=True)


if __name__ == '__main__':
    main()
