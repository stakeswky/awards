"""hubs(t,l) family: Dmass/S at every History position, and the exact closed form
for the subdivided double star hubs(2,l) at j=l+1 (Lemma 2 of PROOF.md):

    Dmass/S = A (l^2-2l-4) / ((A+2)(l^2+l-2)),   A = C(2l+1, l+1),   l >= 4,
    Dmass = 0 for l = 3.

Usage: python check_hubs_closed_form.py --out DIR
"""
import argparse
import json
import os
import sys
from fractions import Fraction as Fr
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402
from families import hubs  # noqa: E402


def dm_at(par, j):
    ch = L.children_of(par)
    col = L.colours(par)
    p = L.uni_poly(par, ch)
    rows = L.biv_rows(par, ch, col)
    N, P = L.mass_arrays(rows, j)
    return p, sum(max(x - y, 0) for x, y in zip(N, P)), N, P


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--lmax_scan', type=int, default=40)
    ap.add_argument('--lmax_exact', type=int, default=80)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    scan = []
    for t in range(2, 7):
        for l in range(2, args.lmax_scan + 1):
            par = hubs(t, l)
            n = len(par)
            ch = L.children_of(par)
            col = L.colours(par)
            p = L.uni_poly(par, ch)
            alpha, h, beta = L.params(p, n, n)
            first = next((k for k in range(len(p) - 1) if p[k] > p[k + 1]), None)
            rows = L.biv_rows(par, ch, col)
            for j in range(first + 1, len(p)):
                if any(p[k] < p[k + 1] for k in range(first, j)):
                    break
                b, a = p[j - 1], p[j]
                S = a * (b - a)
                N, P = L.mass_arrays(rows, j)
                dm = sum(max(x - y, 0) for x, y in zip(N, P))
                r = Fr(dm, S) if S else None
                scan.append(dict(t=t, l=l, n=n, j=j, beta=beta, in_middle=(h + 1 <= j < beta),
                                 ratio_float=None if r is None else float(r), S_zero=(S == 0),
                                 _exact=r, _Dmass=dm, _S=S))
    viol = [x for x in scan if (x['S_zero'] and x['_Dmass'] > 0) or (x['_exact'] is not None and x['_exact'] > 1)]
    ins = [x for x in scan if x['in_middle'] and x['_exact'] is not None]
    outs = [x for x in scan if not x['in_middle'] and x['_exact'] is not None]
    best_in = dict(max(ins, key=lambda x: (x['_exact'], x['t'], x['l'], x['j'])))
    best_out = dict(max(outs, key=lambda x: (x['_exact'], x['t'], x['l'], x['j'])))
    for bst in (best_in, best_out):
        bst['ratio'] = f"{bst['_exact'].numerator}/{bst['_exact'].denominator}"
        bst['Dmass'], bst['S'] = bst['_Dmass'], bst['_S']
    for x in scan + [best_in, best_out]:
        for k in ('_exact', '_Dmass', '_S'):
            x.pop(k, None)
    print('hubs(t,l) t=2..6 l=2..%d: History positions=%d violations=%d' % (args.lmax_scan, len(scan), len(viol)))
    print('  max in-middle ratio %.6f at t=%d l=%d n=%d j=%d beta=%d' % (best_in['ratio_float'], best_in['t'], best_in['l'], best_in['n'], best_in['j'], best_in['beta']))
    print('  max out-of-middle ratio %.6f at t=%d l=%d n=%d j=%d beta=%d' % (best_out['ratio_float'], best_out['t'], best_out['l'], best_out['n'], best_out['j'], best_out['beta']))
    exact = []
    for l in range(3, args.lmax_exact + 1):
        par = hubs(2, l)
        n = len(par)
        p, dm, N, P = dm_at(par, l + 1)
        alpha, h, beta = L.params(p, n, n)
        first = next((k for k in range(len(p) - 1) if p[k] > p[k + 1]), None)
        assert first == l, (l, first)                      # History at j-1=l: first strict descent is at l
        assert beta == l + 1                               # j=l+1=beta: tail boundary, outside the middle range
        A = comb(2 * l + 1, l + 1)
        assert p[l + 1] == A + 2 and p[l] == A + 2 * l     # a=A+2, b=A+2l
        S = p[l + 1] * (p[l] - p[l + 1])
        if l == 3:
            assert dm == 0
            exact.append(dict(l=l, Dmass=0, S=S))
            continue
        assert dm == A * (2 * l * l - 4 * l - 8) // (l + 2) and A * (2 * l * l - 4 * l - 8) % (l + 2) == 0
        assert Fr(dm, S) == Fr(A * (l * l - 2 * l - 4), (A + 2) * (l * l + l - 2))
        assert Fr(dm, S) < 1
        exact.append(dict(l=l, n=n, j=l + 1, A=A, Dmass=dm, S=S, ratio_float=float(Fr(dm, S))))
    print('closed form verified exactly for hubs(2,l), l=3..%d; ratio at l=%d is %.10f' % (args.lmax_exact, args.lmax_exact, exact[-1]['ratio_float']))
    per_tl = {}
    for x in scan:
        rec = per_tl.setdefault((x['t'], x['l']), dict(t=x['t'], l=x['l'], n=x['n'], beta=x['beta'], positions=0,
                                                         middle_positions=0, max_ratio=0.0, max_middle_ratio=None))
        rec['positions'] += 1
        if x['ratio_float'] is not None:
            rec['max_ratio'] = max(rec['max_ratio'], x['ratio_float'])
            if x['in_middle']:
                rec['middle_positions'] += 1
                rec['max_middle_ratio'] = x['ratio_float'] if rec['max_middle_ratio'] is None else max(rec['max_middle_ratio'], x['ratio_float'])
    with open(os.path.join(args.out, 'hubs_closed_form.json'), 'w') as fh:
        json.dump(dict(scan_summary=dict(positions=len(scan), violations=len(viol), max_in_middle=best_in, max_out_of_middle=best_out),
                       closed_form_exact=exact, per_t_l=[per_tl[k] for k in sorted(per_tl)]),
                  fh, sort_keys=True, separators=(',', ':'), default=str)
        fh.write('\n')


if __name__ == '__main__':
    main()
