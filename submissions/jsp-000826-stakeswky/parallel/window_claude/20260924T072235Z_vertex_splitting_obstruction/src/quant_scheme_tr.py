"""c/n vertex-splitting scheme with the formalised ratio bounds (ErdosProblem993/Ends.lean) in place of plain
monotonicity.  For a piece P (forest, order n_P, independence number a_P) at index i:
  i <= 0: exact P_0^2;  i > a_P: 0;  i == a_P: P_i^2;  otherwise the max of
   IH : (c/n_P) P_i^2                                 if i <= top(a_P)            [induction hypothesis Q_c(P)]
   TR : P_i^2 - P_{i-1} * (2(a_P - i)/(i+1)) * P_i                                 [tail_ratio: (i+1)P_{i+1} <= 2(a_P-i)P_i]
   PTR: P_i^2 * (1 - 2 i (a_P - i) / ((i+1)(n_P - 3i + 3)))   if n_P > 3(i-1)     [prefix_ratio at i-1 and tail_ratio at i]
STEP(F,k): some v with LB_A(k) + LB_C(k-1) - X_k(v) >= (c/n) p_k^2.  (tail_ratio needs P bipartite: forests are.)"""
import sys, os, json
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(alpha): return (2*alpha + 1)//3
MODE = {'ptr': True, 'nu': False}

def LB(P, i, nP, c):
    ap = len(P) - 1
    if i <= 0: return Fr(g(P, 0)**2)
    if i > ap: return Fr(0)
    if i == ap: return Fr(P[i]**2)
    mult = (ap - i + min(ap - i, nP - ap)) if MODE['nu'] else 2*(ap - i)
    cands = [Fr(P[i]**2) - Fr(P[i-1]*P[i]*mult, i + 1)]
    if i <= top(ap): cands.append(Fr(c, max(nP, 1)) * P[i]**2)
    if MODE['ptr'] and nP > 3*(i - 1): cands.append(Fr(P[i]**2) * (1 - Fr(i*mult, (i + 1)*(nP - 3*i + 3))))
    return max(cands)

def step_info(par, c, want_slack=False):
    n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1; T = top(a)
    ks = list(range(1, min(T, a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    base_ok = all((p[k]**2 - p[k-1]*p[k+1]) * n >= c * p[k]**2 for k in ks)
    best = {k: None for k in ks}
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); C = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        for k in ks:
            if not want_slack and best[k] is not None and best[k] >= 0: continue
            X = g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1)
            val = (LB(A, k, n - 1, c) + LB(C, k - 1, n - 1 - len(nbr[v]), c) - X - Fr(c, n)*p[k]**2) * n / p[k]**2
            if best[k] is None or val > best[k]: best[k] = val
        if not want_slack and all(b is not None and b >= 0 for b in best.values()): break
    failing = [k for k in ks if best[k] < 0]
    return (base_ok, failing, (min(best.values()) if ks else None)) if want_slack else (base_ok, failing)

def job(args):
    par, c, ws = args
    r = step_info(par, c, ws)
    return r, par

if __name__ == '__main__':
    c = Fr(sys.argv[1]); which = sys.argv[2]
    if 'noptr' in sys.argv[5:]: MODE['ptr'] = False
    if 'nu' in sys.argv[5:]: MODE['nu'] = True
    ws = True
    if which in ('forests', 'trees'):
        from step_forests import forests
        for n in range(int(sys.argv[3]), int(sys.argv[4]) + 1):
            items = list(forests(n)) if which == 'forests' else [L.parents_from_levels(lv) for lv in L.free_trees(n)]
            with Pool(3) as pool: res = list(pool.imap_unordered(job, [(f, c, ws) for f in items], chunksize=50))
            fails = [(par, r[1]) for r, par in res if r[1]]
            sl = [r[2] for r, par in res if r[2] is not None]
            mn = min(sl) if sl else None
            arg = [par for r, par in res if r[2] == mn][:1]
            print('c=%s %s n=%d: %d | Q_c holds: %d | STEP fails: %d %s | min slack (units p_k^2/n): %.4f at %s' % (
                c, which, n, len(res), sum(1 for r, _ in res if r[0]), len(fails), fails[:2], float(mn) if mn is not None else float('nan'), arg if n <= 12 else '..'), flush=True)
