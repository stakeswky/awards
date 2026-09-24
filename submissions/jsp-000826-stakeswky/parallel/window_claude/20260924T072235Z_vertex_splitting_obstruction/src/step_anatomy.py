"""Anatomy of STEP (c = 3/2) : for every forest F (non-edgeless) and k in [1, min(top, alpha-1)]:
  slack(F,k) = max_v [LB_A(k) + LB_C(k-1) - X_k(v) - (c/n) p_k^2] / (p_k^2 / n)      (units of p_k^2/n)
and which vertex classes contain a witness v: leaf, support vertex (adjacent to a leaf), max-degree vertex,
centroid vertex; and whether ONE vertex works for all k (uniform witness), and its class."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from quant_scheme_lm import lower_surplus, g, top
from step_forests import forests

C = Fr(3, 2)

def centroids(n, nbr):
    # vertices minimising the largest component of F - v (forest version: within its own component)
    best = None; res = []
    for v in range(n):
        seen = {v}; worst = 0
        for w in nbr[v]:
            stack = [w]; seen.add(w); cnt = 0
            while stack:
                x = stack.pop(); cnt += 1
                for y in nbr[x]:
                    if y not in seen: seen.add(y); stack.append(y)
            worst = max(worst, cnt)
        if best is None or worst < best: best = worst; res = [v]
        elif worst == best: res.append(v)
    return set(res)

def anatomy(par):
    n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1; T = top(a)
    ks = list(range(1, min(T, a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    if all(len(x) == 0 for x in nbr) or not ks: return None
    deg = [len(x) for x in nbr]; maxd = max(deg)
    leaves = {v for v in range(n) if deg[v] == 1}; support = {v for v in range(n) if any(w in leaves for w in nbr[v])}
    maxdeg = {v for v in range(n) if deg[v] == maxd}; cent = centroids(n, nbr)
    wit = {k: set() for k in ks}; slack = {}
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); Cp = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        for k in ks:
            X = g(A, k-1)*g(Cp, k) + g(A, k+1)*g(Cp, k-2) - 2*g(A, k)*g(Cp, k-1)
            val = (lower_surplus(A, k, n - 1, C) + lower_surplus(Cp, k - 1, n - 1 - deg[v], C) - X - C/n*p[k]**2) * n / p[k]**2
            if k not in slack or val > slack[k]: slack[k] = val
            if val >= 0: wit[k].add(v)
    uniform = set(range(n))
    for k in ks: uniform &= wit[k]
    cls = lambda S: dict(leaf=bool(S & leaves), support=bool(S & support), maxdeg=bool(S & maxdeg), centroid=bool(S & cent))
    per_k = {k: cls(wit[k]) for k in ks}
    return dict(n=n, minslack=min(slack.values()), argk=min(slack, key=slack.get), top=T,
                all_k_leaf=all(per_k[k]['leaf'] for k in ks), all_k_support=all(per_k[k]['support'] for k in ks),
                all_k_maxdeg=all(per_k[k]['maxdeg'] for k in ks), all_k_centroid=all(per_k[k]['centroid'] for k in ks),
                uniform=bool(uniform), uniform_cls=cls(uniform), par=par)

if __name__ == '__main__':
    which = sys.argv[1]; lo, hi = int(sys.argv[2]), int(sys.argv[3])
    for n in range(lo, hi + 1):
        items = [L.parents_from_levels(lv) for lv in L.free_trees(n)] if which == 'trees' else list(forests(n))
        with Pool(2) as pool: res = [r for r in pool.imap_unordered(anatomy, items, chunksize=50) if r]
        m = min(res, key=lambda r: r['minslack'])
        cnt = lambda key: sum(1 for r in res if r[key])
        ucls = {c: sum(1 for r in res if r['uniform'] and r['uniform_cls'][c]) for c in ('leaf', 'support', 'maxdeg', 'centroid')}
        print('%s n=%d: %d | min slack (units p_k^2/n) = %.4f at k=%d (top=%d) par=%s | every k has a witness that is a leaf: %d, support: %d, max-degree: %d, centroid: %d | one v for all k: %d (classes of such v: %s)' % (
            which, n, len(res), float(m['minslack']), m['argk'], m['top'], m['par'] if n <= 12 else '..', cnt('all_k_leaf'), cnt('all_k_support'), cnt('all_k_maxdeg'), cnt('all_k_centroid'), cnt('uniform'), ucls), flush=True)
