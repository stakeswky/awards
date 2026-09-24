"""Window drift max_{q<=r<=top-2} (m_{r+1}-m_r) on large trees: uniform random labelled trees (Pruefer),
random recursive trees, deep complete b-ary trees and spherically symmetric trees; exact integers,
drift evaluated from exact ratios. Low priority companion to the exhaustive run."""
import random, sys, time, json
from fractions import Fraction as Fr
from ip import indep_poly
random.seed(31)
def wdrift(p, n):
    a = len(p) - 1; q, top = (n + 3) // 4, (2 * a + 1) // 3
    best = None
    for r in range(q, top - 1):
        d = Fr((r + 2) * p[r + 2], p[r + 1]) - Fr((r + 1) * p[r + 1], p[r])
        if best is None or d > best: best = d
    return best
def relabel(par):
    n = len(par); ch = [[] for _ in range(n)]
    for v in range(1, n): ch[par[v]].append(v)
    order = []; st = [0]
    while st:
        u = st.pop(); order.append(u); st.extend(reversed(ch[u]))
    pos = {u: i for i, u in enumerate(order)}
    return [-1] + [pos[par[u]] for u in order[1:]]
def pruefer(n):
    code = [random.randrange(n) for _ in range(n - 2)]
    deg = [1] * n
    for x in code: deg[x] += 1
    import heapq
    leaves = [v for v in range(n) if deg[v] == 1]; heapq.heapify(leaves)
    adj = [[] for _ in range(n)]
    for x in code:
        l = heapq.heappop(leaves); adj[l].append(x); adj[x].append(l)
        deg[x] -= 1
        if deg[x] == 1: heapq.heappush(leaves, x)
    u, v = heapq.heappop(leaves), heapq.heappop(leaves); adj[u].append(v); adj[v].append(u)
    par = [-2] * n; par[0] = -1; st = [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if par[w] == -2: par[w] = u; st.append(w)
    return relabel(par)
def sph(branch):
    par = [-1]; frontier = [0]
    for b in branch:
        nf = []
        for u in frontier:
            for _ in range(b): par.append(u); nf.append(len(par) - 1)
        frontier = nf
    return par
res = []
t0 = time.time()
for n in (100, 200, 400, 800):
    for _ in range({100: 60, 200: 30, 400: 12, 800: 4}[n]):
        par = pruefer(n); res.append(('pruefer', n, float(wdrift(indep_poly(par), n))))
    for _ in range({100: 30, 200: 15, 400: 6, 800: 2}[n]):
        par = [-1] + [random.randrange(v) for v in range(1, n)]; par = relabel(par)
        res.append(('recursive', n, float(wdrift(indep_poly(par), n))))
for br in ([2] * 9, [3] * 6, [4] * 5, [5] * 4, [1, 3] * 4, [3, 1] * 4, [1, 4] * 3, [4, 1] * 3, [2, 1] * 6, [1, 2] * 6, [6, 1, 1] * 2):
    par = sph(br); res.append(('sph' + str(br[:3]), len(par), float(wdrift(indep_poly(par), len(par)))))
res.sort(key=lambda x: -x[2])
print('trees', len(res), 'max window drift', res[0], 'min', res[-1][2], 'failures(>1)', sum(r[2] > 1 for r in res), 'secs', round(time.time() - t0))
by = {}
for kind, n, d in res: by.setdefault(kind.split('[')[0], []).append(d)
print({k: (len(v), round(max(v), 4)) for k, v in by.items()})
json.dump(res, open('big_drift.json', 'w'))
