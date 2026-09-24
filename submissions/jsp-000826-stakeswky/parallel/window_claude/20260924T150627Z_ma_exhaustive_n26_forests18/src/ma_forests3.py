"""(MA) on all forests of order n <= NMAX with at least two components and at least one edge
(single trees are covered by the exhaustive tree runs). A forest is a multiset of free trees.
For each forest F = T_1 + ... + T_c and a vertex v in component T_j:
    I(F - v)   = I(T_j - v)    * prod_{i != j} I(T_i),
    I(F - N[v])= I(T_j - N[v]) * prod_{i != j} I(T_i).
v is aligned if dist(M(I(F-v)), M(I(F-N[v])) + 1) <= 1. We try vertices in a heuristic order
(standalone-aligned vertices of each component first) and stop at the first aligned one; a forest
with no aligned vertex at all is printed. Exact integer arithmetic."""
import sys, time
from modelib import *
from ma_forests import free_trees
from ip import mul
NMAX = int(sys.argv[1])
trees = {m: [parents_from_levels(lv) for lv in free_trees(m)] for m in range(1, NMAX)}   # components have order <= NMAX-1
polys = {m: [indep_poly_del(par) for par in trees[m]] for m in trees}
# per tree: distinct (I(T-v), I(T-N[v]), deg) triples (vertices equivalent under automorphism give equal pairs), standalone-aligned first
pieces = {}
for m in trees:
    for i, par in enumerate(trees[m]):
        nb = neighbours(par); seen = set(); lst = []
        for v in range(m):
            pa = tuple(indep_poly_del(par, frozenset([v]))); pc = tuple(indep_poly_del(par, frozenset(nb[v] | {v})))
            if (pa, pc) in seen: continue
            seen.add((pa, pc))
            a1, a2, _ = mode_set(list(pa)); c1, c2, _ = mode_set(list(pc))
            lst.append((dist(a1, a2, c1 + 1, c2 + 1), len(nb[v]), list(pa), list(pc)))
        lst.sort(key=lambda t: (t[0], t[1]))
        pieces[(m, i)] = lst
print('trees per order:', {m: len(trees[m]) for m in trees}, flush=True)
def forests(n):
    def rec(rem, maxkey, cur):
        if rem == 0: yield list(cur); return
        for m in range(min(rem, maxkey[0]), 0, -1):
            imax = len(trees[m]) - 1 if m < maxkey[0] else maxkey[1]
            for i in range(imax, -1, -1):
                cur.append((m, i)); yield from rec(rem - m, (m, i), cur); cur.pop()
    yield from rec(n, (n - 1, len(trees[n - 1]) - 1), [])   # largest component <= n-1: at least two components
t00 = time.time(); grand = 0; grand_bad = 0
for n in range(3, NMAX + 1):
    t0 = time.time(); cnt = 0; bad = []; tries_hist = {}; used_nonfirst = 0; worst = 0
    for F in forests(n):
        if all(m == 1 for m, _ in F): continue
        cnt += 1
        best = 99; tries = 0
        # products of all components, then divide out by re-multiplying the others (n small: recompute)
        total_poly_by_index = [polys[m][i] for (m, i) in F]
        done = False
        for j, (m, i) in enumerate(F):
            if m == 1: continue
            if j > 0 and F[j - 1] == (m, i): continue
            R = [1]
            for jj in range(len(F)):
                if jj != j: R = mul(R, total_poly_by_index[jj])
            for d0, dg, pa, pc in pieces[(m, i)]:
                tries += 1
                A = mul(pa, R); C = mul(pc, R)
                a1, a2, ua = mode_set(A); c1, c2, uc = mode_set(C)
                if not (ua and uc): print('NONUNIMODAL PIECE', F, flush=True)
                dd = dist(a1, a2, c1 + 1, c2 + 1)
                if dd < best: best = dd
                if dd <= 1:
                    done = True; break
            if done: break
            used_nonfirst += 1
        tries_hist[tries] = tries_hist.get(tries, 0) + 1
        if best > worst: worst = best
        if best > 1: bad.append(F)
    grand += cnt; grand_bad += len(bad)
    print(f'n={n}: forests(>=2 components, with an edge)={cnt} without_aligned_vertex={len(bad)} worst_best_dist={worst} tries_hist={dict(sorted(tries_hist.items()))} secs={time.time()-t0:.0f}', bad[:3], flush=True)
print(f'TOTAL forests={grand} without_aligned_vertex={grand_bad} secs={time.time()-t00:.0f}')
