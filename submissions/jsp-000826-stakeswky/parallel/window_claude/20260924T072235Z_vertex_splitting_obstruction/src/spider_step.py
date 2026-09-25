"""STEP (c = 3/2, LB = IH + matching tail bound TRnu) on spider-like trees, one representative vertex per orbit.
Families: S(2^s, 1^m) = centre with s legs of length 2 and m pendant leaves;
          R(s, m)     = root adjacent to the centres of s cherries (K_{1,2}) and to m leaves."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from comp_step import LB, g, top
C = Fr(3, 2)

def spider(s, m):
    par = [-1]; reps = [0]
    for i in range(s):
        par.append(0); mid = len(par) - 1; par.append(mid)
        if i == 0: reps += [mid, mid + 1]
    for i in range(m):
        par.append(0)
        if i == 0: reps.append(len(par) - 1)
    return par, reps

def cherries(s, m):
    par = [-1]; reps = [0]
    for i in range(s):
        par.append(0); c = len(par) - 1; par.append(c); par.append(c)
        if i == 0: reps += [c, c + 1]
    for i in range(m):
        par.append(0)
        if i == 0: reps.append(len(par) - 1)
    return par, reps

def step(args):
    fam, s, m = args
    par, reps = (spider if fam == 'S' else cherries)(s, m)
    n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1
    ks = list(range(1, min(top(a), a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    Qok = all((p[k]**2 - p[k-1]*p[k+1]) * n >= C * p[k]**2 for k in ks)
    best = {k: None for k in ks}
    for v in reps:
        A = L.uni_poly(par, ch, removed=frozenset([v])); Cp = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        for k in ks:
            X = g(A, k-1)*g(Cp, k) + g(A, k+1)*g(Cp, k-2) - 2*g(A, k)*g(Cp, k-1)
            val = (LB(A, k, n - 1, C) + LB(Cp, k - 1, n - 1 - len(nbr[v]), C) - X - C/n*p[k]**2) * n / p[k]**2
            if best[k] is None or val > best[k]: best[k] = val
    fl = [k for k in ks if best[k] < 0]
    return fam, s, m, n, a, Qok, fl, (min(best.values()) if ks else None)

if __name__ == '__main__':
    NMAX = int(sys.argv[1]); jobs = []
    for s in range(1, NMAX):
        for m in range(0, NMAX):
            if 1 + 2*s + m <= NMAX and (m % 2 == 0 or s % 3 == 0): jobs.append(('S', s, m))
            if 1 + 3*s + m <= NMAX and (m % 2 == 0 or s % 3 == 0): jobs.append(('R', s, m))
    with Pool(3) as pool: res = list(pool.imap_unordered(step, jobs, chunksize=4))
    for fam in ('S', 'R'):
        rs = [r for r in res if r[0] == fam]
        bad = sorted([r for r in rs if r[6] or not r[5]], key=lambda r: r[3])
        print('%s family (n<=%d): %d trees | Q_{3/2} fails: %d | STEP fails: %d | smallest failing: %s | min slack: %.4f' % (
            fam, NMAX, len(rs), sum(1 for r in rs if not r[5]), len(bad), [(r[1], r[2], r[3], r[6]) for r in bad[:4]], float(min(r[7] for r in rs if r[7] is not None))), flush=True)
