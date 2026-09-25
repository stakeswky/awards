"""Fast STEP evaluation for forests given by components (new LB: IH c/n_P, matching tail bound TRnu).
A component is described by (poly, order, alpha, vertex_types) where each vertex type is (A_comp, C_comp, deg):
A_comp = I(Q - v), C_comp = I(Q - N[v]) for the component Q. For F = union of components, the pieces are
A = A_comp * prod(other components), C = C_comp * prod(other components)."""
import sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def pmul(a, b):
    r = [0]*(len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i+j] += x*y
    return r
def ppow(a, e):
    r = [1]
    for _ in range(e): r = pmul(r, a)
    return r
def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(alpha): return (2*alpha + 1)//3

def LB(P, i, nP, c):
    ap = len(P) - 1
    if i <= 0: return Fr(g(P, 0)**2)
    if i > ap: return Fr(0)
    if i == ap: return Fr(P[i]**2)
    mult = ap - i + min(ap - i, nP - ap)
    best = Fr(P[i]**2) - Fr(P[i-1]*P[i]*mult, i + 1)
    if i <= top(ap): best = max(best, Fr(c, max(nP, 1)) * P[i]**2)
    return best

def star(t):
    """K_{1,t} (t>=0; t=0 is K1). vertex types: centre, leaf."""
    if t == 0: return ([1, 1], 1, [([1], [1], 0)])
    poly = ppow([1, 1], t); poly[1] += 1
    centre = (ppow([1, 1], t), [1], t)
    leaf = (ppow([1, 1], t - 1)[:] if t >= 1 else [1], None, 1)
    # leaf v: Q - v = K_{1,t-1} ; Q - N[v] = t-1 isolated leaves
    Km = ppow([1, 1], t - 1); Km = Km + [0] if len(Km) < 2 else Km
    qv = ppow([1, 1], t - 1); qv = qv + [0]*(2 - len(qv)); qv[1] += 1   # I(K_{1,t-1}) = (1+x)^{t-1} + x
    leaf = (qv, ppow([1, 1], t - 1), 1)
    return (poly, t + 1, [centre, leaf])

def forest_step(comps, c, want=False):
    """comps: list of (poly, order, types). Returns (Q_ok, failing ks, min slack in units p_k^2/n)."""
    polys = [q[0] for q in comps]; n = sum(q[1] for q in comps)
    p = [1]
    for q in polys: p = pmul(p, q)
    while len(p) > 1 and p[-1] == 0: p.pop()
    a = len(p) - 1; ks = list(range(1, min(top(a), a - 1) + 1)) if a >= 2 else []
    Qok = all((p[k]**2 - p[k-1]*p[k+1]) * n >= c * p[k]**2 for k in ks)
    best = {k: None for k in ks}
    seen = set()
    for j, (poly, order, types) in enumerate(comps):
        key = (tuple(poly), order)
        if key in seen: continue
        seen.add(key)
        rest = [1]
        for i, q in enumerate(polys):
            if i != j: rest = pmul(rest, q)
        for (Ac, Cc, d) in types:
            A = pmul(Ac, rest); C = pmul(Cc, rest)
            while len(A) > 1 and A[-1] == 0: A.pop()
            while len(C) > 1 and C[-1] == 0: C.pop()
            for k in ks:
                X = g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1)
                val = (LB(A, k, n - 1, c) + LB(C, k - 1, n - 1 - d, c) - X - Fr(c, n)*p[k]**2) * n / p[k]**2
                if best[k] is None or val > best[k]: best[k] = val
    fl = [k for k in ks if best[k] < 0]
    return Qok, fl, (min(best.values()) if ks else None)
