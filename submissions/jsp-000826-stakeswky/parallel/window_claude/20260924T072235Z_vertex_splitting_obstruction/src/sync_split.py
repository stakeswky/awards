"""Synchronising split test. For a tree T, a vertex v and an index k in the window:
  A = I(T - v), C = I(T - N[v]),  p = A + x C.
  LC(p at k) = surplus_A(k) + surplus_C(k-1) - X_k(v), where
  X_k(v) = a_{k-1} c_k + a_{k+1} c_{k-2} - 2 a_k c_{k-1}.
If X_k(v) <= 0, LC of p at k follows from LC of the two smaller forests.
Questions: does some v give X_k(v) <= 0 for each window k? Does one v work for the whole window?
Also record whether that v can be chosen with alpha(T-v) = alpha(T) and alpha(T-N[v]) = alpha(T)-1,
the condition under which the windows of the pieces cover the needed indices."""
import sys, os
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def g(a, i): return a[i] if 0 <= i < len(a) else 0

def analyse(lv):
    par = L.parents_from_levels(lv); n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1; lo = (n + 3)//4; hi = (2*a + 1)//3
    ks = [k for k in range(max(lo, 1), min(hi, a - 1) + 1)]
    if not ks: return None
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    per_k_ok = {k: False for k in ks}; whole = []; whole_nest = []
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); C = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        good = all(g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1) <= 0 for k in ks)
        for k in ks:
            if g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1) <= 0: per_k_ok[k] = True
        if good:
            whole.append(v)
            if len(A) - 1 == a and len(C) - 1 == a - 1: whole_nest.append(v)
    return (all(per_k_ok.values()), bool(whole), bool(whole_nest), len(ks))

if __name__ == '__main__':
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        trees = [tuple(lv) for lv in L.free_trees(n)]
        with Pool(int(sys.argv[3]) if len(sys.argv) > 3 else 6) as pool:
            res = [r for r in pool.imap_unordered(analyse, trees, chunksize=500) if r]
        print('n=%d trees with window=%d | each window k has a synchronising v: %d | one v for whole window: %d | ... with alpha(T-v)=alpha, alpha(T-N[v])=alpha-1: %d' % (
            n, len(res), sum(r[0] for r in res), sum(r[1] for r in res), sum(r[2] for r in res)), flush=True)
