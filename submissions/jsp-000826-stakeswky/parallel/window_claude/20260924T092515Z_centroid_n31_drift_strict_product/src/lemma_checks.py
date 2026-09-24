"""Exact sanity checks of the written lemmas (not proofs):
 (1) adjacent-term Cauchy-Binet bound  c_k^2 - c_{k-1}c_{k+1} >= sum_j Da_{k-j} Db_j  for LC a,b (c=a*b),
     with Da_t = a_t^2 - a_{t-1}a_{t+1} (zero padding), on random positive LC integer sequences;
 (2) the plateau example showing the lemma needs strictness: (1+x+x^2+x^3+x^4)(1+x);
 (3) the drift identity  m_{r+1}-m_r = E_r|N(J)| - E_{r+1}|N(J)| - 1  by brute force on random forests."""
import random, itertools
from ip import mul
random.seed(20260924)
def D(a, t):
    g = lambda i: a[i] if 0 <= i < len(a) else 0
    return g(t) ** 2 - g(t - 1) * g(t + 1)
def rand_lc(L):
    # positive integer LC sequence: products of ratios nonincreasing, built from a real-rooted-ish start then perturbed down
    while True:
        a = [random.randint(1, 50)]
        r = random.uniform(0.5, 6.0)
        for i in range(L - 1):
            r *= random.uniform(0.3, 1.0)
            a.append(max(1, int(a[-1] * r)))
        if all(a[t] ** 2 >= a[t - 1] * a[t + 1] for t in range(1, L - 1)): return a
bad = 0; tests = 0
for _ in range(20000):
    a = rand_lc(random.randint(2, 9)); b = rand_lc(random.randint(2, 9)); c = mul(a, b)
    for k in range(len(c)):
        tests += 1
        lhs = D(c, k); rhs = sum(D(a, k - j) * D(b, j) for j in range(len(b)))
        if lhs < rhs: bad += 1
print('(1) adjacent-term bound: tests', tests, 'violations', bad)
c = mul([1, 1, 1, 1, 1], [1, 1]); print('(2) plateau example', c, 'D_2 =', D(c, 2))
# (3) drift identity by brute force
def forest_rand(n):
    par = [-1] + [random.randrange(v) if random.random() < 0.9 else -1 for v in range(1, n)]
    return [(v, p) for v, p in enumerate(par) if p >= 0]
viol = 0; cnt = 0
from fractions import Fraction as Fr
for _ in range(300):
    n = random.randint(3, 13); E = forest_rand(n)
    adj = [set() for _ in range(n)]
    for u, v in E: adj[u].add(v); adj[v].add(u)
    sets = [[] for _ in range(n + 1)]
    for mask in range(1 << n):
        S = [v for v in range(n) if mask >> v & 1]
        if all(not (adj[u] & set(S)) for u in S): sets[len(S)].append(S)
    p = [len(s) for s in sets]
    while p[-1] == 0: p.pop()
    a = len(p) - 1
    EN = [Fr(sum(len(set().union(*[adj[v] for v in S])) if S else 0 for S in sets[r]), p[r]) for r in range(a + 1)]
    m = [Fr((r + 1) * p[r + 1], p[r]) for r in range(a)]
    for r in range(a - 1):
        cnt += 1
        if m[r + 1] - m[r] != EN[r] - EN[r + 1] - 1: viol += 1
print('(3) drift identity checks', cnt, 'violations', viol)
