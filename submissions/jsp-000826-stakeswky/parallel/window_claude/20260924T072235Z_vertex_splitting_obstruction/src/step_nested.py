"""STEP restricted to NESTED witnesses (v in some but not all maximum independent sets), using ONLY the induction
hypothesis Q_{3/2} for the pieces (no gap-zone bound is ever needed: alpha(F-v)=alpha, alpha(F-N[v])=alpha-1).
A forest has a nested vertex iff its maximum independent set is not unique.  Reports, per order, the number of
forests with a unique MIS (no nested vertex) and the number of non-unique-MIS forests where STEP_nested fails."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from step_forests import forests
C = Fr(3, 2)
def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(al): return (2*al + 1)//3

def ih(P, i, nP):
    a = len(P) - 1
    if i <= 0: return Fr(P[0]**2)
    if i > a: return Fr(0)
    if i == a: return Fr(P[i]**2)
    assert i <= top(a)
    return C/nP*P[i]**2

def job(par):
    n = len(par); ch = L.children_of(par); p = L.uni_poly(par, ch); a = len(p) - 1
    ks = list(range(1, min(top(a), a - 1) + 1)) if a >= 2 else []
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    nested = []
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); Cp = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        if len(A) - 1 == a and len(Cp) - 1 == a - 1: nested.append((v, A, Cp))
    if not nested: return 'unique', None
    if not ks: return 'ok', None
    fl = []
    for k in ks:
        ok = False
        for v, A, Cp in nested:
            X = g(A, k-1)*g(Cp, k) + g(A, k+1)*g(Cp, k-2) - 2*g(A, k)*g(Cp, k-1)
            if ih(A, k, n - 1) + ih(Cp, k - 1, n - 1 - len(nbr[v])) - X >= C/n*p[k]**2: ok = True; break
        if not ok: fl.append(k)
    return ('fail', (par, fl)) if fl else ('ok', None)

if __name__ == '__main__':
    which = sys.argv[1]
    for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        items = list(forests(n)) if which == 'forests' else [L.parents_from_levels(lv) for lv in L.free_trees(n)]
        with Pool(3) as pool: res = list(pool.imap_unordered(job, items, chunksize=50))
        cnt = {t: sum(1 for r in res if r[0] == t) for t in ('unique', 'ok', 'fail')}
        print('%s n=%d: %d | unique MIS (no nested v): %d | STEP_nested holds: %d | fails: %d %s' % (
            which, n, len(res), cnt['unique'], cnt['ok'], cnt['fail'], [r[1] for r in res if r[0] == 'fail'][:2] if n <= 13 else ''), flush=True)
