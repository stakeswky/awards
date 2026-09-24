"""(MA) on all forests of order n <= NMAX, as multisets of trees: does every forest with an edge have
a vertex v (in some component) with dist(M(I(F-v)), M(I(F-N[v]))+1) <= 1?  Exact arithmetic."""
import sys, itertools
from modelib import *
from ma_forests import free_trees
from ip import mul
NMAX = int(sys.argv[1])
trees = {m: [parents_from_levels(lv) for lv in free_trees(m)] for m in range(1, NMAX + 1)}
polys = {m: [indep_poly_del(par) for par in trees[m]] for m in trees}
# per tree: list over vertices of (I(T-v), I(T-N[v]), deg v)
pieces = {}
for m in trees:
    for i, par in enumerate(trees[m]):
        nb = neighbours(par)
        pieces[(m, i)] = [(indep_poly_del(par, frozenset([v])), indep_poly_del(par, frozenset(nb[v] | {v})), len(nb[v])) for v in range(m)]
def forests(n):
    """multisets of (order, index) with total order n, nonincreasing"""
    def rec(rem, maxkey, cur):
        if rem == 0: yield list(cur); return
        for m in range(min(rem, maxkey[0]), 0, -1):
            imax = len(trees[m]) - 1 if m < maxkey[0] else maxkey[1]
            for i in range(imax, -1, -1):
                cur.append((m, i)); yield from rec(rem - m, (m, i), cur); cur.pop()
    yield from rec(n, (n, len(trees[n]) - 1), [])
tot_bad = 0
for n in range(2, NMAX + 1):
    cnt = 0; bad = []
    for F in forests(n):
        if all(m == 1 for m, _ in F): continue   # edgeless: trivially unimodal
        cnt += 1
        best = 99
        for j, (m, i) in enumerate(F):
            if m == 1: continue
            if j > 0 and F[j - 1] == (m, i): continue   # same component type already tried
            R = [1]
            for jj, (m2, i2) in enumerate(F):
                if jj != j: R = mul(R, polys[m2][i2])
            for pa, pc, d in pieces[(m, i)]:
                A = mul(pa, R); C = mul(pc, R)
                a1, a2, ua = mode_set(A); c1, c2, uc = mode_set(C)
                if not (ua and uc): print('NONUNIMODAL PIECE', F)
                dd = dist(a1, a2, c1 + 1, c2 + 1)
                if dd < best: best = dd
                if best <= 1: break
            if best <= 1: break
        if best > 1: bad.append(F)
    tot_bad += len(bad)
    print(f'n={n}: forests with an edge={cnt}, without an aligned vertex={len(bad)}', bad[:3], flush=True)
print('TOTAL forests without aligned vertex:', tot_bad)
