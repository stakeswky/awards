"""Canonical-witness tests for STEP (c = 3/2).
P(F) = pendant-star centres: support vertices v with at most one non-leaf neighbour (e.g. the penultimate
vertex of a longest path; the centre of a star component; both ends of a K2 component).
For every forest F with an edge and every k in [1, min(top, alpha-1)] record whether
  S3: some support vertex is a witness;  S1: some v in P(F) is a witness;  S1u: one v in P(F) works for all k;
  S1max: the v in P(F) with the most leaf neighbours (ties: all such) contains a witness for every k."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from quant_scheme_lm import lower_surplus, g, top
from step_forests import forests
C = Fr(3, 2)

def witnesses(par, cand, ks, p, nbr, ch):
    n = len(par); W = {k: set() for k in ks}
    for v in cand:
        A = L.uni_poly(par, ch, removed=frozenset([v])); Cp = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        for k in ks:
            X = g(A, k-1)*g(Cp, k) + g(A, k+1)*g(Cp, k-2) - 2*g(A, k)*g(Cp, k-1)
            if lower_surplus(A, k, n - 1, C) + lower_surplus(Cp, k - 1, n - 1 - len(nbr[v]), C) - X >= C/n*p[k]**2: W[k].add(v)
    return W

def test(par):
    n = len(par); ch = L.children_of(par); p = L.uni_poly(par, ch); a = len(p) - 1
    ks = list(range(1, min(top(a), a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    deg = [len(x) for x in nbr]
    if max(deg) == 0 or not ks: return None
    leaves = {v for v in range(n) if deg[v] == 1}
    support = [v for v in range(n) if nbr[v] & leaves]
    P = [v for v in support if sum(1 for w in nbr[v] if w not in leaves) <= 1]
    mx = max(len(nbr[v] & leaves) for v in P); Pmax = [v for v in P if len(nbr[v] & leaves) == mx]
    W = witnesses(par, support, ks, p, nbr, ch)
    S3 = all(W[k] for k in ks); S1 = all(W[k] & set(P) for k in ks); S1max = all(W[k] & set(Pmax) for k in ks)
    S1u = any(all(v in W[k] for k in ks) for v in P)
    star_forest = all(sum(1 for w in nbr[v] if w not in leaves) == 0 for v in support) and all(deg[v] <= 1 or v in support for v in range(n))
    return S3, S1, S1u, S1max, star_forest, par

if __name__ == '__main__':
    which = sys.argv[1]
    for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        items = [L.parents_from_levels(lv) for lv in L.free_trees(n)] if which == 'trees' else list(forests(n))
        with Pool(2) as pool: res = [r for r in pool.imap_unordered(test, items, chunksize=50) if r]
        def ex(i):
            bad = [r for r in res if not r[i]]
            return '%d fail (star forests among them: %d)%s' % (len(bad), sum(1 for r in bad if r[4]), (' e.g. ' + str(next((r[5] for r in bad if not r[4]), ''))) if any(not r[4] for r in bad) else '')
        print('%s n=%d: %d | S3 support: %s | S1 pendant-star centre: %s | S1u uniform: %s | S1max: %s' % (which, n, len(res), ex(0), ex(1), ex(2), ex(3)), flush=True)
