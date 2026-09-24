"""Exact independence polynomials of rooted trees (parent arrays, parent index < child index)."""
from fractions import Fraction as Fr
def mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r
def add(a, b):
    if len(a) < len(b): a, b = b, a
    r = list(a)
    for i, y in enumerate(b): r[i] += y
    return r
def indep_poly(par):
    n = len(par)
    A = [[1] for _ in range(n)]      # v excluded
    B = [[0, 1] for _ in range(n)]   # v included
    for v in range(n - 1, 0, -1):
        u = par[v]
        A[u] = mul(A[u], add(A[v], B[v]))
        B[u] = mul(B[u], A[v])
    p = add(A[0], B[0])
    while len(p) > 1 and p[-1] == 0: p.pop()
    return p
def drift(p):
    a = len(p) - 1
    m = [Fr((r + 1) * p[r + 1], p[r]) for r in range(a)]
    return m, [m[r + 1] - m[r] for r in range(a - 1)]
def mode(p):
    k = 0
    while k + 1 < len(p) and p[k] < p[k + 1]: k += 1
    return k
