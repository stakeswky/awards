"""(MA) on forests: every forest F of order n (multiset of trees) has a vertex v with
dist(M(I(F-v)), M(I(F-N[v]))+1) <= 1?  Trees from level sequences (WROM via e993lib-free generator:
we use the parents_from_levels of all trees produced by ./modes-like enumeration in Python).
Since I(F-v) = I(T-v) I(R) and I(F-N[v]) = I(T-N[v]) I(R) for v in component T, we enumerate
(tree T, vertex v) pairs and forest polynomials I(R) of the remaining order."""
import sys, itertools
from modelib import *
from ip import mul
sys.setrecursionlimit(10000)
# free trees by WROM (Python port from earlier runs' e993lib)
def free_trees(n):
    if n == 1: yield [0]; return
    if n == 2: yield [0, 1]; return
    L = list(range(n // 2 + 1)) + list(range(1, (n + 1) // 2))
    def next_rooted(L, p):
        if p < 0:
            p = n - 1
            while L[p] == 1: p -= 1
        if p == 0: return False
        q = p - 1
        while L[q] != L[p] - 1: q -= 1
        for i in range(p, n): L[i] = L[i - p + q]
        return True
    def split_info(L):
        ones = [i for i in range(n) if L[i] == 1]
        m = ones[1] if len(ones) > 1 else n
        lh = max([L[i] - 1 for i in range(1, m)] + [0]); rh = max([L[i] for i in range(m, n)] + [0])
        return m, lh, rh, m - 1, 1 + n - m
    def next_tree(L):
        m, lh, rh, ll, rl = split_info(L)
        valid = rh >= lh
        if valid and rh == lh:
            if ll > rl: valid = False
            elif ll == rl:
                left = [L[1 + i] - 1 for i in range(ll)]; rest = [0] + [L[m + i] for i in range(ll - 1)]
                if left > rest: valid = False
        if valid: return
        p = ll; oldp = L[p]
        next_rooted(L, p)
        if oldp > 2:
            m2, lh2, rh2, a2, b2 = split_info(L)
            slen = lh2 + 1
            for i in range(slen): L[n - slen + i] = 1 + i
    while True:
        next_tree(L)
        yield list(L)
        if not next_rooted(L, -1): break
if __name__ == '__main__':
    NMAX = int(sys.argv[1])
    # forest polynomials by order (distinct), from all trees
    tree_polys = {}
    for m in range(1, NMAX):
        tree_polys[m] = set()
        for lv in free_trees(m):
            tree_polys[m].add(tuple(indep_poly_del(parents_from_levels(lv))))
    def forest_polys(m):
        res = set()
        def rec(rem, maxm, cur):
            if rem == 0: res.add(tuple(cur)); return
            for s in range(min(rem, maxm), 0, -1):
                for tp in tree_polys[s]: rec(rem - s, s, mul(cur, list(tp)))
        rec(m, m, [1]); return res
    FP = {m: forest_polys(m) for m in range(0, NMAX)}
    print('forest polynomial counts', {m: len(v) for m, v in FP.items()})
    # for each tree T of order t and vertex v: pieces (I(T-v), I(T-N[v])); for each forest poly R of order n - t
    bad = 0; total = 0; worst = []
    for n in range(3, NMAX + 1):
        n_forests = 0; n_bad = 0
        for t in range(2, n + 1):
            for lv in free_trees(t):
                par = parents_from_levels(lv); nb = neighbours(par)
                pieces = [(indep_poly_del(par, frozenset([v])), indep_poly_del(par, frozenset(nb[v] | {v})), len(nb[v])) for v in range(t)]
                for R in FP[n - t]:
                    # this forest = T + R ; we only consider splitting inside T (other components handled when they are 'T')
                    # so aggregate per (T,R): record best alignment over v in T
                    best = 99; bestdeg = None
                    for pa, pc, d in pieces:
                        A = mul(pa, list(R)); C = mul(pc, list(R))
                        a1, a2, ua = mode_set(A); c1, c2, uc = mode_set(C)
                        if not (ua and uc): print('NONUNIMODAL PIECE'); continue
                        dd = dist(a1, a2, c1 + 1, c2 + 1)
                        if dd < best: best, bestdeg = dd, d
                    n_forests += 1
                    if best > 1: n_bad += 1; worst.append((n, t, best, lv, R))
        print(f'n={n}: (tree component T, rest R) pairs={n_forests}, pairs with no aligned vertex in T: {n_bad}', flush=True)
        bad += n_bad; total += n_forests
    print('TOTAL pairs', total, 'without aligned vertex inside the chosen component', bad)
    for w in worst[:10]: print('  ', w)
