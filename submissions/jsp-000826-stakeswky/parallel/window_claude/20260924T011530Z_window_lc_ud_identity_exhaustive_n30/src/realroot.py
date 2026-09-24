"""Exact real-rootedness test (Sturm) of g_r(y) = sum_{J in I_r} y^{e(J)}, e(J) = #addable vertices.
Real-rooted g_r (nonnegative coefficients) => e is a sum of independent Bernoullis under Unif(I_r)
=> Var <= mean (under-dispersion) => log-concavity of p at r+1."""
import sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from ext_identity import size_free_poly

def trim(p):
    while p and p[-1] == 0: p.pop()
    return p
def deriv(p): return [i*p[i] for i in range(1, len(p))]
def prem(a, b):
    a = [Fr(x) for x in a]
    while len(a) >= len(b) and any(a):
        c = a[-1] / b[-1]; sh = len(a) - len(b)
        for i in range(len(b)): a[sh+i] -= c*b[i]
        a.pop(); a = trim(a)
    return a
def sign_changes(vals):
    s = [v for v in vals if v != 0]
    return sum(1 for x, y in zip(s, s[1:]) if (x > 0) != (y > 0))
def count_real_roots(p):
    """number of distinct real roots via Sturm; p has rational coeffs, p[i] coeff of y^i"""
    p = trim(list(p))
    if len(p) <= 1: return 0
    seq = [[Fr(x) for x in p], [Fr(x) for x in deriv(p)]]
    while len(seq[-1]) > 1 or (len(seq[-1]) == 1 and False):
        r = prem(seq[-2], seq[-1])
        if not r: break
        seq.append([-x for x in r])
    # values at -inf and +inf: sign of leading coeff times (-1)^deg
    at_pinf = [q[-1] for q in seq]
    at_minf = [q[-1] * (1 if (len(q)-1) % 2 == 0 else -1) for q in seq]
    return sign_changes(at_minf) - sign_changes(at_pinf)
def distinct_part(p):
    """p / gcd(p, p') to count roots without multiplicity issues: degree of squarefree part"""
    a = [Fr(x) for x in trim(list(p))]; b = [Fr(x) for x in deriv(a)]
    while b:
        a, b = b, prem(a, b)
    g = a  # gcd (up to scalar)
    return len(trim(list(p))) - 1 - (len(g) - 1)
def real_rooted(p):
    """all roots real (counting multiplicity): #distinct real roots == degree of squarefree part"""
    p = trim(list(p))
    # strip factor y^m (roots at 0 are real)
    while p and p[0] == 0: p = p[1:]
    if len(p) <= 2: return True
    return count_real_roots(p) == distinct_part(p)

def check_tree(par, window_only=True):
    n = len(par); G = size_free_poly(par)
    pmax = max(s for (s, f) in G)
    res = []
    for r in range(0, pmax):
        g = [0]*(n+1)
        for (s, f), v in G.items():
            if s == r: g[f] += v
        k = r + 1
        a = pmax; lo = (n + 3)//4; hi = (2*a + 1)//3
        inw = lo <= k <= hi
        if window_only and not inw: continue
        res.append((k, inw, real_rooted(g)))
    return res

if __name__ == '__main__':
    # sanity: known real-rooted and non-real-rooted polys
    assert real_rooted([1, 3, 3, 1]) and real_rooted([2, 3, 1]) and not real_rooted([1, 0, 1]) and not real_rooted([1, 4, 3, 1][::-1][:0] + [1, 1, 1])
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        pos = rr = 0; allpos = allrr = 0; bad = None
        for lv in L.free_trees(n):
            par = L.parents_from_levels(lv)
            for (k, inw, ok) in check_tree(par, window_only=False):
                allpos += 1; allrr += ok
                if inw:
                    pos += 1; rr += ok
                    if not ok and bad is None: bad = (list(lv), k)
        print('n=%d window positions=%d real-rooted=%d | all positions=%d real-rooted=%d | first window failure=%s' % (n, pos, rr, allpos, allrr, bad), flush=True)
