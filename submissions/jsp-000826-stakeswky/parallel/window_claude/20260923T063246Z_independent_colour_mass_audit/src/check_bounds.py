"""Boundary claims of the hand-off, checked on all free trees n<=NMAX:
  (i)  strict increase p_0<...<p_h with h=floor(n(n-1)/(4n-2))+1 (trees: M=n);
  (ii) strict increase through ceil(n/4);
  (iii) no rise p_{k+1}>p_k for k>=beta=ceil(alpha(n-1)/(n+alpha)).
Also the deletion identity sum_v T_v - ba = (n-2j) b (a-c) on random GENERAL graphs
(cycles allowed, fixed seed), by literal enumeration.

Usage: python check_bounds.py --nmax 20 --out DIR [--procs 9]
"""
import argparse
import itertools
import json
import os
import random
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402


def chk(n):
    bad_h = bad_q = bad_beta = tot = 0
    min_first = None
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv)
        p = L.uni_poly(par, L.children_of(par))
        tot += 1
        alpha, h, beta = L.params(p, n, n)
        first = next((k for k in range(len(p) - 1) if p[k] >= p[k + 1]), len(p) - 1)  # first non-strict step
        if first < h:
            bad_h += 1
        if first < -(-n // 4):
            bad_q += 1
        if min_first is None or first * 10**6 // n < min_first[0]:
            min_first = (first * 10**6 // n, first, list(lv))
        if any(p[k + 1] > p[k] for k in range(beta, len(p) - 1)):
            bad_beta += 1
    return dict(n=n, trees=tot, strict_increase_through_h_violations=bad_h,
                strict_increase_through_ceil_n_over_4_violations=bad_q,
                rise_at_or_after_beta_violations=bad_beta,
                min_first_nonincrease_index=min_first[1], min_first_nonincrease_levels=min_first[2])


def indep_counts(n, adj, mask):
    cnt = [0] * (n + 1)
    verts = [v for v in range(n) if mask >> v & 1]

    def rec(i, chosen, sz):
        if i == len(verts):
            cnt[sz] += 1
            return
        v = verts[i]
        rec(i + 1, chosen, sz)
        if not (adj[v] & chosen):
            rec(i + 1, chosen | (1 << v), sz + 1)
    rec(0, 0, 0)
    return cnt


def deletion_identity(trials=60, seed=7):
    rng = random.Random(seed)
    checked = 0
    graphs = []
    for _ in range(trials):
        n = rng.randint(6, 13)
        adj = [0] * n
        m = 0
        for u, v in itertools.combinations(range(n), 2):
            if rng.random() < 0.35:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
                m += 1
        full = (1 << n) - 1
        p = indep_counts(n, adj, full)
        g = lambda arr, i: arr[i] if 0 <= i < len(arr) else 0  # noqa: E731
        A = [indep_counts(n, adj, full & ~(1 << v)) for v in range(n)]
        B = [indep_counts(n, adj, full & ~((1 << v) | adj[v])) for v in range(n)]
        for j in range(1, n):
            b, a, c = g(p, j - 1), g(p, j), g(p, j + 1)
            T = sum(g(A[v], j - 1) * (g(A[v], j) - g(A[v], j + 1)) - g(B[v], j - 2) * (g(B[v], j - 1) - g(B[v], j))
                    for v in range(n))
            assert T - b * a == (n - 2 * j) * b * (a - c), (n, j)
            checked += 1
        graphs.append(dict(n=n, edges=m, cyclomatic=m - n + 1))
    return dict(seed=seed, graphs=len(graphs), positions_checked=checked,
                graphs_with_cycles=sum(1 for x in graphs if x['cyclomatic'] > 0), graph_sizes=graphs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nmax', type=int, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--procs', type=int, default=9)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    res = []
    with Pool(args.procs) as pool:
        for r in pool.imap(chk, range(4, args.nmax + 1)):
            res.append(r)
            print('n=%d trees=%d h_viol=%d ceil(n/4)_viol=%d beta_viol=%d min_first_index=%d' % (
                r['n'], r['trees'], r['strict_increase_through_h_violations'],
                r['strict_increase_through_ceil_n_over_4_violations'], r['rise_at_or_after_beta_violations'],
                r['min_first_nonincrease_index']), flush=True)
    ident = deletion_identity()
    print('deletion identity verified on', ident['graphs'], 'random general graphs (', ident['graphs_with_cycles'],
          'with cycles ),', ident['positions_checked'], 'positions')
    with open(os.path.join(args.out, 'bounds.json'), 'w') as fh:
        json.dump(dict(per_n=res, deletion_identity=ident), fh, sort_keys=True, separators=(',', ':'))
        fh.write('\n')


if __name__ == '__main__':
    main()
