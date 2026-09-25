"""Kadrawi-Levit-type core trees (centre, t hubs, hub i carrying arms[i] pendant P2,
optional centre leaves; n<=90): D* at every History position. These are the
structures behind the known non-log-concave trees (T26 = core_tree((3,4,4))).

Usage: python check_core_family.py --out DIR [--procs 9]
"""
import argparse
import itertools
import json
import os
import sys
from fractions import Fraction as Fr
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402
from families import core_tree  # noqa: E402


def keys(nmax=90):
    out = []
    for t in range(2, 6):
        for arms in itertools.combinations_with_replacement(range(1, 10), t):
            for x in range(0, 3):
                if 1 + sum(1 + 2 * s for s in arms) + x <= nmax:
                    out.append((arms, x))
    return out


def one(key):
    arms, x = key
    par = core_tree(arms, x)
    n = len(par)
    ch = L.children_of(par)
    col = L.colours(par)
    p = L.uni_poly(par, ch)
    alpha, h, beta = L.params(p, n, n)
    first = next((k for k in range(len(p) - 1) if p[k] > p[k + 1]), None)
    nonlc = [i for i in range(1, len(p) - 1) if p[i] * p[i] < p[i - 1] * p[i + 1]]
    rows = L.biv_rows(par, ch, col)
    out = []
    for j in range(first + 1, len(p)):
        if any(p[k] < p[k + 1] for k in range(first, j)):
            break
        b, a = p[j - 1], p[j]
        S = a * (b - a)
        N, P = L.mass_arrays(rows, j)
        dm = sum(max(x1 - y1, 0) for x1, y1 in zip(N, P))
        out.append(dict(arms=list(arms), centre_leaves=x, n=n, j=j, beta=beta, in_middle=(h + 1 <= j < beta),
                        tree_nonLC_positions=nonlc, unimodal=L.is_unimodal(p), S=S, Dmass=dm,
                        ratio=(f'{Fr(dm, S).numerator}/{Fr(dm, S).denominator}' if S else None),
                        ratio_float=(float(Fr(dm, S)) if S else None)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--procs', type=int, default=9)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    ks = keys()
    with Pool(args.procs) as pool:
        res = [r for rr in pool.imap(one, ks, chunksize=20) for r in rr]
    viol = [r for r in res if (r['S'] == 0 and r['Dmass'] > 0) or (r['S'] and r['Dmass'] > r['S'])]
    order = lambda r: (Fr(r['Dmass'], r['S']), r['n'], r['j'], r['arms'], r['centre_leaves'])  # noqa: E731
    withS = [r for r in res if r['S']]
    top = sorted(withS, key=order, reverse=True)[:10]
    mid = [r for r in withS if r['in_middle']]
    nonlc_trees = sorted({(tuple(r['arms']), r['centre_leaves']) for r in res if r['tree_nonLC_positions']})
    t26 = [dict(j=r['j'], ratio=r['ratio'], Dmass=r['Dmass'], S=r['S']) for r in res if r['arms'] == [3, 4, 4] and r['centre_leaves'] == 0]
    summ = dict(trees=len(ks), history_positions=len(res), violations=len(viol), nonLC_trees=len(nonlc_trees),
                nonunimodal_positions=sum(1 for r in res if not r['unimodal']),
                max_ratio=top[0], max_middle_ratio=(max(mid, key=order) if mid else None),
                middle_positions=len(mid), middle_positive_Dmass=sum(1 for r in mid if r['Dmass'] > 0))
    print('core trees', summ['trees'], 'History positions', summ['history_positions'], 'violations', summ['violations'],
          'non-LC trees', summ['nonLC_trees'])
    print('max ratio %.6f arms=%s centre_leaves=%d n=%d j=%d' % (top[0]['ratio_float'], top[0]['arms'], top[0]['centre_leaves'], top[0]['n'], top[0]['j']))
    print('middle-range positions', summ['middle_positions'], 'with Dmass>0:', summ['middle_positive_Dmass'])
    print('T26 History positions:', t26)
    with open(os.path.join(args.out, 'core_family.json'), 'w') as fh:
        json.dump(dict(summary=summ, violations=viol[:50], top=top, T26=t26, nonLC_trees=[[list(a), x] for a, x in nonlc_trees]),
                  fh, sort_keys=True, separators=(',', ':'), default=str)
        fh.write('\n')


if __name__ == '__main__':
    main()
