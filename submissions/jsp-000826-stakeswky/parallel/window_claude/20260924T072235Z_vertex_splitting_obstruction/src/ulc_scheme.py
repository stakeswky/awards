"""ULC(inf)-type inductive scheme on [1, top].
H(F): for every k with 1 <= k <= min(top(alpha), alpha-1):  k p_k^2 >= (k+1) p_{k-1} p_{k+1}
      (equivalently  s(k) := p_k^2 - p_{k-1}p_{k+1} >= p_k^2/(k+1)).
Splitting identity (any vertex v): s_F(k) = sA(k) + sC(k-1) - X_k(v), A = p(F-v), C = p(F-N[v]).
Lower bounds for a piece P (forest of smaller order) at index i:
  i <= 0: exact P_0^2 = 1;  i > alpha_P: 0;  i == alpha_P: P_i^2;
  1 <= i <= top(alpha_P), i < alpha_P: P_i^2/(i+1)            (induction hypothesis H(P));
  top(alpha_P) <= i < alpha_P:        P_i^2 - P_{i-1}P_i       (Levit-Mandrescu tail: P_{i+1} <= P_i);
  (max of the two when both apply).
STEP(F,k): some v with  LB_A(k) + LB_C(k-1) - X_k(v) >= p_k^2/(k+1).
H for all forests follows from STEP for every forest and every k in the range (strong induction on order;
orders 0 and 1 have an empty range)."""
import sys, os, json
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(alpha): return (2*alpha + 1)//3

def LB(P, i):
    ap = len(P) - 1
    if i <= 0: return Fr(g(P, 0)**2)
    if i > ap: return Fr(0)
    if i == ap: return Fr(P[i]**2)
    best = None
    if i <= top(ap): best = Fr(P[i]**2, i + 1)
    if i >= top(ap):
        lm = Fr(P[i]**2 - P[i-1]*P[i]); best = lm if best is None else max(best, lm)
    return best

def info(par, want_v=False):
    n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1; T = top(a)
    ks = list(range(1, min(T, a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    H = all(k * p[k]**2 >= (k + 1) * p[k-1] * p[k+1] for k in ks)
    pieces = []
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); C = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        pieces.append((v, A, C))
    failing = []; goodv = {}
    for k in ks:
        need = Fr(p[k]**2, k + 1); good = []
        for (v, A, C) in pieces:
            X = g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1)
            if LB(A, k) + LB(C, k - 1) - X >= need:
                good.append(v)
                if not want_v: break
        if not good: failing.append(k)
        goodv[k] = good
    return (H, failing, goodv) if want_v else (H, failing)

def job(par):
    H, fl = info(par)
    return H, not fl, None if not fl else (par, fl)

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'forests':
        from step_forests import forests
        for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            with Pool(8) as pool: res = list(pool.imap_unordered(job, forests(n), chunksize=100))
            fails = [r[2] for r in res if not r[1]]
            print('forests n=%d: %d | H holds: %d | STEP at every k: %d | failures: %s' % (
                n, len(res), sum(r[0] for r in res), sum(r[1] for r in res), fails[:2]), flush=True)
    elif which == 'trees':
        for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
            trees = [L.parents_from_levels(lv) for lv in L.free_trees(n)]
            with Pool(8) as pool: res = list(pool.imap_unordered(job, trees, chunksize=200))
            fails = [r[2] for r in res if not r[1]]
            print('trees n=%d: %d | H holds: %d | STEP at every k: %d | failures: %s' % (
                n, len(res), sum(r[0] for r in res), sum(r[1] for r in res), fails[:2]), flush=True)
    elif which == 'nonlc':
        H_ = os.path.dirname(os.path.abspath(__file__)); pars = []
        for n, f in ((26, 'wlc_c_n26.json'), (28, 'wlc_c_n28.json'), (29, 'wlc_c_n29.json'), (30, 'wlc_strict_n30.json')):
            for e in json.load(open(os.path.join(H_, f)))['examples']:
                pars.append(L.parents_from_levels([int(x) for x in e.split('levels=')[1].split()[0].split(',')]))
        with Pool(8) as pool: res = list(pool.imap_unordered(job, pars, chunksize=4))
        fails = [r[2] for r in res if not r[1]]
        print('non-LC trees n=26..30: %d | H holds: %d | STEP at every k: %d | failures: %s' % (
            len(res), sum(r[0] for r in res), sum(r[1] for r in res), [(len(f[0]), f[1]) for f in fails[:4]]), flush=True)
