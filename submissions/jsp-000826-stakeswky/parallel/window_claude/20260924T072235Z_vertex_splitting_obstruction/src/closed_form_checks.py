"""Closed-form (second-implementation) checks of the STEP counterexamples in WINDOW_LC_PROGRESS.md 9.4-9.5.
Each vertex orbit's pieces A = I(F-v), C = I(F-N[v]) are written explicitly and p = A + xC is asserted.
  (1) R(s,0) = root joined to the centres of s cherries: STEP fails at k = top for s = 19,21,22,24 (bounds IH + TRnu);
  (2) P5 + 16 K1: STEP with the LM bound fails at k = 13 for every orbit;
  (3) Newton diagnostic: for R(s,0), v = cherry centre, replacing the gap bound of the real-rooted piece
      C = (s-1)P3 by Newton's inequality restores positive slack;
  (4) the n = 30 non-LC tree with p_14 p_16 / p_15^2 = 1.7268 (weak LC of p_k/k! fails)."""
import sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def mul(a, b):
    r = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i+j] += x*y
    return r
def pw(a, e):
    r = [1]
    for _ in range(e): r = mul(r, a)
    return r
def add(a, b):
    m = max(len(a), len(b)); return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(m)]
def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(al): return (2*al + 1)//3
c = Fr(3, 2)
P3 = [1, 3, 1]; B = [1, 1]; X1 = [0, 1]

def LB(P, i, nP, gap='TRnu', newton=False):
    a = len(P) - 1
    if i <= 0: return Fr(P[0]**2)
    if i > a: return Fr(0)
    if i == a: return Fr(P[i]**2)
    cands = []
    if i <= top(a): cands.append(c/nP*P[i]**2)
    if gap == 'LM' and i >= top(a): cands.append(Fr(P[i]**2 - P[i-1]*P[i]))
    if gap == 'TRnu':
        mult = a - i + min(a - i, nP - a); cands.append(Fr(P[i]**2) - Fr(P[i-1]*P[i]*mult, i + 1))
    if newton: cands.append(Fr(P[i]**2 * (a + 1), (i + 1)*(a - i + 1)))
    return max(cands) if cands else None

def slack(p, n, A, C, d, k, **kw):
    X = g(A,k-1)*g(C,k) + g(A,k+1)*g(C,k-2) - 2*g(A,k)*g(C,k-1)
    la = LB(A, k, n-1, **{k2: v for k2, v in kw.items() if k2 != 'newtonC'})
    lc = LB(C, k-1, n-1-d, gap=kw.get('gap', 'TRnu'), newton=kw.get('newtonC', False))
    if la is None or lc is None: return None
    return (la + lc - X - c/n*p[k]**2) * n / p[k]**2

def pR(s): return add(pw(P3, s), mul(X1, pw(B, 2*s)))
print('(1) R(s,0), bounds IH + TRnu:')
for s in (18, 19, 20, 21, 22, 24):
    n = 3*s + 1; p = pR(s); a = len(p) - 1; T = top(a)
    orbits = {'root': (pw(P3, s), pw(B, 2*s), s), 'centre': (mul(pw(B, 2), pR(s-1)), pw(P3, s-1), 3),
              'leaf': (add(mul(pw(P3, s-1), [1, 2]), mul(X1, pw(B, 2*s-1))), mul(B, pR(s-1)), 1)}
    for nm, (A, C, d) in orbits.items(): assert add(A, mul(X1, C)) == p, nm
    fails = []
    for k in range(1, min(T, a-1)+1):
        best = max((slack(p, n, A, C, d, k), nm) for nm, (A, C, d) in orbits.items())
        if best[0] < 0: fails.append((k, round(float(best[0]), 4), best[1]))
    Qok = all(2*n*(p[k]**2 - p[k-1]*p[k+1]) >= 3*p[k]**2 for k in range(1, min(T, a-1)+1))
    print('  R(%d,0): n=%d alpha=%d top=%d | Q holds: %s | STEP failing (k, best slack, orbit): %s' % (s, n, a, T, Qok, fails))

print('(2) P5 + 16 K1 with the LM gap bound, k = 13:')
m = 16; n = 5 + m; p = mul(pw(B, m), [1, 5, 6, 1]); a = len(p) - 1
orb = {'K1': (mul(pw(B, m-1), [1, 5, 6, 1]), mul(pw(B, m-1), [1, 5, 6, 1]), 0),
       'end': (mul(pw(B, m), [1, 4, 3]), mul(pw(B, m), P3), 1),
       'second': (mul(pw(B, m), mul(B, P3)), mul(pw(B, m), [1, 2]), 2),
       'middle': (mul(pw(B, m), mul([1, 2], [1, 2])), mul(pw(B, m), pw(B, 2)), 2)}
for nm, (A, C, d) in orb.items(): assert add(A, mul(X1, C)) == p, nm
for nm, (A, C, d) in orb.items():
    print('  v=%-6s slack = %.4f' % (nm, float(slack(p, n, A, C, d, 13, gap='LM'))))
print('  alpha=%d top=%d, Q holds at k=13: %s' % (a, top(a), 2*n*(p[13]**2 - p[12]*p[14]) >= 3*p[13]**2))

print('(3) Newton diagnostic, R(s,0), v = cherry centre, k = top:')
for s in (19, 21, 22, 24, 30, 40, 60):
    n = 3*s + 1; p = pR(s); a = len(p) - 1; k = top(a)
    A = mul(pw(B, 2), pR(s-1)); C = pw(P3, s-1)
    print('  s=%d: slack with TRnu %.4f | with Newton for C %.4f' % (s, float(slack(p, n, A, C, 3, k)), float(slack(p, n, A, C, 3, k, newtonC=True))))

print('(4) weak LC (p_k/k! LC) fails:')
import e993lib as L
lv = [int(x) for x in '0,1,2,3,2,3,2,3,2,3,2,3,1,2,3,2,3,2,3,2,3,1,2,3,2,3,2,3,2,3'.split(',')]
par = L.parents_from_levels(lv); p = L.uni_poly(par, L.children_of(par)); a = len(p) - 1
r = Fr(p[a-2]*p[a], p[a-1]**2)
print('  n=%d alpha=%d tail=%s ratio p_{a-2}p_a/p_{a-1}^2 = %.6f > 1 + 1/(a-1) = %.6f' % (len(par), a, p[a-3:], float(r), 1 + 1/(a-1)))
