"""Conjecture D* test: Dmass_j <= S_j at EVERY j after the first strict descent
(History holds there because every tree tested is unimodal; this is re-checked),
for ALL free trees of order n, including tail positions j >= beta.

Usage: python check_allj.py --nmin 4 --nmax 19 --out DIR [--procs 9]
"""
import argparse
import json
import os
import sys
from fractions import Fraction as Fr
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402


def chk(n):
    cases = viol = plateau = nonunimodal = 0
    best = None
    viol_cases = []
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv)
        ch = L.children_of(par)
        col = L.colours(par)
        p = L.uni_poly(par, ch)
        if not L.is_unimodal(p):
            nonunimodal += 1
        first = next((k for k in range(len(p) - 1) if p[k] > p[k + 1]), None)
        if first is None:
            continue
        rows = L.biv_rows(par, ch, col)
        for j in range(first + 1, len(p)):
            if any(p[k] < p[k + 1] for k in range(first, j)):
                break  # History(T,j-1) fails from here on
            b, a = p[j - 1], p[j]
            S = a * (b - a)
            N, P = L.mass_arrays(rows, j)
            dm = sum(max(x - y, 0) for x, y in zip(N, P))
            cases += 1
            if S == 0:
                plateau += 1
                if dm > 0:
                    viol += 1
                    viol_cases.append(dict(levels=list(lv), j=j, S=S, Dmass=dm))
                continue
            if dm > S:
                viol += 1
                viol_cases.append(dict(levels=list(lv), j=j, S=S, Dmass=dm))
            r = Fr(dm, S)
            if best is None or r > best[0]:
                best = (r, dict(levels=list(lv), j=j, b=b, a=a, c=p[j + 1] if j + 1 < len(p) else 0,
                                S=S, Dmass=dm, alpha_h_beta=list(L.params(p, n, n))))
    out = dict(n=n, cases=cases, plateaus=plateau, violations=viol, nonunimodal_trees=nonunimodal,
               violation_cases=viol_cases[:50])
    if best is not None:
        out['max_ratio'] = f'{best[0].numerator}/{best[0].denominator}'
        out['max_ratio_float'] = float(best[0])
        out['max_case'] = best[1]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nmin', type=int, default=4)
    ap.add_argument('--nmax', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--procs', type=int, default=9)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    res = []
    with Pool(args.procs) as pool:
        for r in pool.imap(chk, range(args.nmin, args.nmax + 1)):
            res.append(r)
            print(f"n={r['n']} cases={r['cases']} plateaus={r['plateaus']} Dmass>S={r['violations']} "
                  f"nonunimodal={r['nonunimodal_trees']} max_Dmass/S={r.get('max_ratio_float')} "
                  f"at j={r.get('max_case', {}).get('j')} levels={r.get('max_case', {}).get('levels')}", flush=True)
    summary = dict(scope='all free trees n in [%d,%d]; every j after the first strict descent while History holds' % (args.nmin, args.nmax),
                   total_cases=sum(r['cases'] for r in res), total_violations=sum(r['violations'] for r in res),
                   per_n=res)
    with open(os.path.join(args.out, 'allj.json'), 'w') as fh:
        json.dump(summary, fh, sort_keys=True, separators=(',', ':'), default=str)
        fh.write('\n')
    print('TOTAL cases', summary['total_cases'], 'violations', summary['total_violations'])


if __name__ == '__main__':
    main()
