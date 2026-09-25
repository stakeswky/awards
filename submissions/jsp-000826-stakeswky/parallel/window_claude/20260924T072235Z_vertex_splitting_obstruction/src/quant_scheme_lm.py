"""Quantitative vertex-splitting scheme.
Q_c(F): for every k in [1, top(alpha(F))]:  p_k^2 - p_{k-1}p_{k+1} >= (c/n) p_k^2   (n = |V(F)|).
Identity: p_k^2 - p_{k-1}p_{k+1} = sA(k) + sC(k-1) - X_k(v) with A = p(F-v), C = p(F-N[v]).
Guaranteed lower bounds from the induction hypothesis on the smaller forests:
  sA(k) >= gA * a_k^2 with gA = c/(n-1) if 1 <= k <= top(alpha_A); = 1 if k == alpha_A; a_k = 0 if k > alpha_A;
  unusable if top(alpha_A) < k < alpha_A (gap zone).  Same for C at k-1 with n_C = n-1-deg(v);
  k-1 == 0 gives sC(0) = c_0^2 (factor 1).
STEP(F,k): some v with  gA a_k^2 + gC c_{k-1}^2 - X_k(v) >= (c/n) p_k^2  (exact rational arithmetic).
If STEP holds for every forest of order > n0 and every k in [1, top], and Q_c holds for all forests
of order <= n0, then Q_c holds for all forests; Q_c implies WindowLC, hence unimodality."""
import sys, os, json, random
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(alpha): return (2*alpha + 1)//3

def lower_surplus(poly, idx, n_piece, c):
    """proved lower bound for s(idx) = poly_idx^2 - poly_{idx-1} poly_{idx+1}:
    inductive margin (c/n_piece) poly_idx^2 on [1, top]; Levit-Mandrescu monotonicity poly_{idx+1} <= poly_idx
    (formalized for every bipartite graph from top(alpha) on) gives s >= poly_idx^2 - poly_{idx-1} poly_idx there."""
    ap = len(poly) - 1
    if idx <= 0: return Fr(g(poly, 0)**2)
    if idx > ap: return Fr(0)
    if idx == ap: return Fr(poly[idx]**2)
    best = None
    if idx <= top(ap): best = Fr(c, max(n_piece, 1)) * poly[idx]**2
    if idx >= top(ap):
        lm = Fr(poly[idx]**2 - poly[idx-1]*poly[idx])
        best = lm if best is None else max(best, lm)
    return best

def step_info(par, c):
    n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1; T = top(a)
    ks = list(range(1, min(T, a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    pieces = []
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); C = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        pieces.append((v, A, C, n - 1, n - 1 - len(nbr[v])))
    base_ok = all((p[k]**2 - p[k-1]*p[k+1]) * n >= c * p[k]**2 for k in ks)
    failing = []
    for k in ks:
        need = Fr(c, n) * p[k]**2; ok = False
        for (v, A, C, nA, nC) in pieces:
            LA = lower_surplus(A, k, nA, c); LC_ = lower_surplus(C, k - 1, nC, c)
            X = g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1)
            if LA + LC_ - X >= need: ok = True; break
        if not ok: failing.append(k)
    return base_ok, failing

def job(args):
    lv, c = args
    base_ok, failing = step_info(L.parents_from_levels(lv), c)
    return base_ok, not failing, None if not failing else (list(lv), failing)

if __name__ == '__main__':
    c = Fr(sys.argv[1]); which = sys.argv[2]
    if which == 'trees':
        for n in range(int(sys.argv[3]), int(sys.argv[4]) + 1):
            trees = [(tuple(lv), c) for lv in L.free_trees(n)]
            with Pool(8) as pool: res = list(pool.imap_unordered(job, trees, chunksize=200))
            fails = [r[2] for r in res if not r[1]]
            print('c=%s trees n=%d: %d | Q_c holds: %d | STEP holds at every k: %d | first STEP failure: %s' % (
                c, n, len(res), sum(r[0] for r in res), sum(r[1] for r in res), fails[:1]), flush=True)
    elif which == 'nonlc':
        H = os.path.dirname(os.path.abspath(__file__)); tot = qb = st = 0; bad = []
        for n, f in ((26, 'wlc_c_n26.json'), (28, 'wlc_c_n28.json'), (29, 'wlc_c_n29.json'), (30, 'wlc_strict_n30.json')):
            for e in json.load(open(os.path.join(H, f)))['examples']:
                lv = [int(x) for x in e.split('levels=')[1].split()[0].split(',')]
                b, fl = step_info(L.parents_from_levels(lv), c); tot += 1; qb += b; st += not fl
                if fl: bad.append((n, fl))
        print('c=%s non-LC trees n=26..30: %d | Q_c holds: %d | STEP at every k: %d | failures: %s' % (c, tot, qb, st, bad[:4]))
