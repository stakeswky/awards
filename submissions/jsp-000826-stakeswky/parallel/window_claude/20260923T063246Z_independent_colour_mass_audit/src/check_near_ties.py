"""Targeted near-tie search in the middle range: hub_tree(groups,s,q) trees (n<=95);
for every middle-range History position compute rho=(b-a)n/a; the 400 smallest-rho
positions (most dangerous for Dmass<=S, since S=a(b-a)) get Dmass and delta_e for
one representative leaf of every automorphism leaf type.

Usage: python check_near_ties.py --out DIR [--procs 9]
"""
import argparse
import json
import os
import sys
from fractions import Fraction as Fr
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402
from families import hub_tree  # noqa: E402


def keys():
    out = []
    for t1 in range(1, 8):
        for l1 in range(2, 17):
            for t2 in range(0, 7):
                for l2 in ([None] if t2 == 0 else range(l1 + 1, 17)):
                    groups = ((t1, l1),) if t2 == 0 else ((t1, l1), (t2, l2))
                    if t1 + t2 < 2:
                        continue
                    for s in range(0, 5):
                        for q in range(0, 4):
                            n = 1 + t1 * (1 + l1) + (t2 * (1 + l2) if t2 else 0) + s + 2 * q
                            if n <= 95:
                                out.append((groups, s, q))
    return out


def scan_one(key):
    groups, s, q = key
    par, _ = hub_tree(groups, s, q)
    n = len(par)
    p = L.uni_poly(par, L.children_of(par))
    js, _ = L.domain(p, n, n)
    return [(Fr((p[j - 1] - p[j]) * n, p[j]), key, j) for j in js]


def detail(args):
    key, j = args
    groups, s, q = key
    par, types = hub_tree(groups, s, q)
    n = len(par)
    ch = L.children_of(par)
    col = L.colours(par)
    p = L.uni_poly(par, ch)
    rows = L.biv_rows(par, ch, col)
    b, a, c = p[j - 1], p[j], p[j + 1]
    S = a * (b - a)
    N, P = L.mass_arrays(rows, j)
    dm = sum(max(x - y, 0) for x, y in zip(N, P))
    deg = [len(ch[v]) + (par[v] >= 0) for v in range(n)]
    by_type = {}
    for u in range(n):
        if deg[u] == 1 and types[u] not in by_type:
            cp, cm = L.leaf_caps(par, ch, col, rows, j, u, par[u], len(N))
            by_type[types[u]] = L.cut_deficit(N, P, cp, cm)
    md = min(by_type.values())
    return dict(groups=[list(g) for g in groups], s=s, q=q, n=n, j=j, b=b, a=a, c=c, S=S, Dmass=dm,
                rho=float(Fr((b - a) * n, a)), delta_by_leaf_type=by_type, min_delta=md,
                Dmass_over_S=float(Fr(dm, S)) if S else None, min_delta_over_S=float(Fr(md, S)) if S else None,
                unimodal=L.is_unimodal(p), LC_at_j=(a * a - b * c >= 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--procs', type=int, default=9)
    ap.add_argument('--detail', type=int, default=400)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    ks = keys()
    with Pool(args.procs) as pool:
        scans = pool.map(scan_one, ks, chunksize=200)
    cand = sorted((c for sc in scans for c in sc), key=lambda c: (c[0], str(c[1]), c[2]))
    todo = [(k, j) for r, k, j in cand[:args.detail]]
    with Pool(args.procs) as pool:
        dets = pool.map(detail, todo, chunksize=4)
    dv = [d for d in dets if (d['S'] and d['Dmass'] > d['S']) or (not d['S'] and d['Dmass'] > 0)]
    mv = [d for d in dets if (d['S'] and d['min_delta'] > d['S']) or (not d['S'] and d['min_delta'] > 0)]
    worst = max(dets, key=lambda d: (Fr(d['Dmass'], d['S']) if d['S'] else Fr(10**9), d['n'], d['j']))
    summ = dict(trees=len(ks), middle_history_positions=len(cand), detailed=len(dets),
                smallest_rho=dets[0]['rho'], smallest_b_minus_a=min(d['b'] - d['a'] for d in dets),
                Dmass_gt_S=len(dv), min_delta_gt_S=len(mv), exact_zero_Dmass=sum(1 for d in dets if d['Dmass'] == 0),
                max_Dmass_over_S=worst['Dmass_over_S'], max_case=dict((k, worst[k]) for k in ('groups', 's', 'q', 'n', 'j', 'rho')))
    print('trees', summ['trees'], 'middle History positions', summ['middle_history_positions'], 'detailed', summ['detailed'])
    print('smallest rho=(b-a)n/a %.3e ; smallest b-a among detailed = %d' % (summ['smallest_rho'], summ['smallest_b_minus_a']))
    print('Dmass>S:', summ['Dmass_gt_S'], ' min_delta>S:', summ['min_delta_gt_S'], ' Dmass==0 exactly:', summ['exact_zero_Dmass'],
          ' max Dmass/S=%.6f' % summ['max_Dmass_over_S'], summ['max_case'])
    with open(os.path.join(args.out, 'near_ties.json'), 'w') as fh:
        json.dump(dict(summary=summ, detailed=dets), fh, sort_keys=True, separators=(',', ':'), default=str)
        fh.write('\n')


if __name__ == '__main__':
    main()
