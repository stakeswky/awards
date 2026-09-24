"""Which deterministic rule picks a uniform STEP witness (c = 3/2)?  Rules (candidate sets; rule passes if some
candidate works for ALL k):  Pmin = pendant-star centres with the fewest leaf neighbours;  P2 = degree-2 vertices
adjacent to a leaf (middle of a pendant P2);  Pall = all pendant-star centres."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from quant_scheme_lm import top
from step_forests import forests
from step_canonical import witnesses

def rules(par):
    n = len(par); ch = L.children_of(par); p = L.uni_poly(par, ch); a = len(p) - 1
    ks = list(range(1, min(top(a), a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    deg = [len(x) for x in nbr]
    if max(deg) == 0 or not ks: return None
    leaves = {v for v in range(n) if deg[v] == 1}
    P = [v for v in range(n) if (nbr[v] & leaves) and sum(1 for w in nbr[v] if w not in leaves) <= 1]
    star_forest = all(sum(1 for w in nbr[v] if w not in leaves) == 0 for v in P) and all(deg[v] <= 1 or v in P for v in range(n))
    mn = min(len(nbr[v] & leaves) for v in P); Pmin = [v for v in P if len(nbr[v] & leaves) == mn]
    P2 = [v for v in P if deg[v] == 2 and len(nbr[v] & leaves) == 1]
    W = witnesses(par, P, ks, p, nbr, ch)
    uni = lambda S: any(all(v in W[k] for k in ks) for v in S)
    return uni(Pmin), (uni(P2) if P2 else None), uni(P), star_forest, par

if __name__ == '__main__':
    which = sys.argv[1]
    for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        items = [L.parents_from_levels(lv) for lv in L.free_trees(n)] if which == 'trees' else list(forests(n))
        with Pool(2) as pool: res = [r for r in pool.imap_unordered(rules, items, chunksize=50) if r]
        ns = [r for r in res if not r[3]]
        print('%s n=%d: non-star-forest cases %d | Pmin uniform fails: %d %s | P2 exists: %d, P2 uniform fails: %d %s | Pall uniform fails: %d' % (
            which, n, len(ns), sum(1 for r in ns if not r[0]), [r[4] for r in ns if not r[0]][:1],
            sum(1 for r in ns if r[1] is not None), sum(1 for r in ns if r[1] is False), [r[4] for r in ns if r[1] is False][:1],
            sum(1 for r in ns if not r[2])), flush=True)
