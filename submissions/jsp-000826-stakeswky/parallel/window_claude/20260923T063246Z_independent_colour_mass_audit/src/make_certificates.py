"""Key certificates: complete exact arrays for the decisive positions, so each number
can be rechecked by hand or by any independent program (no search needed).

Includes: hubs(2,l) extremal positions (Lemma 2), the largest middle-range ratio in
the hubs(t,l) scan, the exact near-plateau with b-a=1, published regressions F56/G25,
and the per-order maximal middle-range witnesses read from the sweep outputs.

Usage: python make_certificates.py --out DIR   (run after check_sweep.py wrote DIR)
"""
import argparse
import glob
import json
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402
from families import hubs, hub_tree  # noqa: E402


def cert(label, construction, par, j, leaves=False):
    n = len(par)
    ch = L.children_of(par)
    col = L.colours(par)
    p = L.uni_poly(par, ch)
    rows = L.biv_rows(par, ch, col)
    N, P = L.mass_arrays(rows, j)
    dm = sum(max(x - y, 0) for x, y in zip(N, P))
    b, a = p[j - 1], p[j]
    c = p[j + 1] if j + 1 < len(p) else 0
    S = a * (b - a)
    alpha, h, beta = L.params(p, n, n)
    out = dict(label=label, construction=construction, n=n, parents=par,
               L_colour_class=[v for v in range(n) if col[v] == 0],
               p=p, alpha=alpha, h=h, beta=beta, j=j, in_middle_range=(h + 1 <= j < beta),
               b=b, a=a, c=c, S=S, N=N, P=P, Dmass=Dmass_check(N, P, dm),
               Dmass_over_S=(f'{Fr(dm, S).numerator}/{Fr(dm, S).denominator}' if S else None),
               checks=dict(sum_N_equals_bc=(sum(N) == b * c), sum_P_equals_a2=(sum(P) == a * a),
                           row_sums_equal_p=([sum(r) for r in rows] == p), unimodal=L.is_unimodal(p)))
    if leaves:
        deg = [len(ch[v]) + (par[v] >= 0) for v in range(n)]
        ds = {}
        for u in range(n):
            if deg[u] == 1:
                v = par[u] if par[u] >= 0 else ch[u][0]
                cp, cm = L.leaf_caps(par, ch, col, rows, j, u, v, len(N))
                ds[u] = L.cut_deficit(N, P, cp, cm)
        out['delta_by_leaf'] = ds
        out['min_delta'] = min(ds.values())
    assert all(out['checks'][k] for k in ('sum_N_equals_bc', 'sum_P_equals_a2', 'row_sums_equal_p'))
    return out


def Dmass_check(N, P, dm):
    assert dm == sum(max(x - y, 0) for x, y in zip(N, P))
    return dm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    certs = []
    for l in (4, 8, 20, 40):
        certs.append(cert(f'hubs(2,{l}) extremal tail position', f'hubs(2,{l}): centre-2 hubs-{l} leaves each', hubs(2, l), l + 1, leaves=(l <= 8)))
    certs.append(cert('largest middle-range ratio in hubs(t,l) scan', 'hubs(5,40)', hubs(5, 40), 101))
    par, _ = hub_tree(((5, 2), (1, 15)), 2, 0)
    certs.append(cert('exact near-plateau b-a=1 with Dmass=0', 'hub_tree(((5,2),(1,15)), s=2, q=0)', par, 14, leaves=True))
    certs.append(cert('published regression F56', 'hubs(5,10)', hubs(5, 10), 26))
    for c in certs:
        print(c['label'], '| n=%d j=%d middle=%s Dmass/S=%s' % (c['n'], c['j'], c['in_middle_range'], c['Dmass_over_S']))
    with open(os.path.join(args.out, 'KEY_CERTIFICATES.json'), 'w') as fh:
        json.dump(dict(certificates=certs), fh, sort_keys=True, separators=(',', ':'), default=str)
        fh.write('\n')
    # one file per swept order, so partial replays compare file by file
    for path in sorted(glob.glob(os.path.join(args.out, 'sweep_n*.json'))):
        with open(path) as fh:
            d = json.load(fh)
        if not d.get('maxD'):
            continue
        case = d['maxD']['case']
        par = L.parents_from_levels(case['levels'])
        c = cert(f"sweep n={d['n']}: maximal middle-range Dmass/S", f"level sequence {case['levels']}", par, case['j'], leaves=True)
        print(c['label'], '| n=%d j=%d middle=%s Dmass/S=%s min_delta=%d' % (c['n'], c['j'], c['in_middle_range'], c['Dmass_over_S'], c['min_delta']))
        with open(os.path.join(args.out, 'sweep_witness_n%02d.json' % d['n']), 'w') as fh:
            json.dump(c, fh, sort_keys=True, separators=(',', ':'), default=str)
            fh.write('\n')


if __name__ == '__main__':
    main()
