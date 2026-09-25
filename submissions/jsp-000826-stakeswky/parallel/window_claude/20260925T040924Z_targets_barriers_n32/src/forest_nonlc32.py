"""Forests of order <= NMAX that contain a non-log-concave tree component.

A forest with two non-LC tree components has order >= 52 (all trees of order <= 25 are LC), so for
NMAX <= 51 such a forest is T + R with T a non-LC tree of order 26..NMAX and R an arbitrary forest of
order <= NMAX - |T| (possibly empty). I(T+R) = I(T) I(R) depends only on I(T) and I(R), so it suffices
to take every non-LC tree sequence (from the exhaustive cwlc logs) and every distinct forest
polynomial of order m <= NMAX - |T| (products of tree polynomials; all trees of order <= 5 are
enumerated from Pruefer codes). For each product: unimodality, strict LC on [ceil(n/4), ceil((2a-1)/3)],
and the window drift condition on [ceil(n/4), ceil((2a-1)/3) - 2]; exact integers.
usage: forest_nonlc.py NMAX log26 log27 ... (cwlc logs; EX lines with first_bad>=0 are the non-LC trees)"""
import sys, re, itertools, json
from ip import mul
NMAX = int(sys.argv[1])
nonlc = []
for f in sys.argv[2:]:
    for line in open(f):
        if line.startswith('EX') and 'first_bad=-1' not in line:
            p = [int(x) for x in re.search(r'p=(\S+)', line).group(1).split(',')]
            par = re.search(r'parents=(\S+)', line).group(1)
            n = par.count(',') + 1
            nonlc.append((n, tuple(p)))
by_n = {}
for n, p in set(nonlc): by_n.setdefault(n, set()).add(p)
print('non-LC tree sequences by order:', {n: len(v) for n, v in sorted(by_n.items())})
def tree_polys(m):
    """distinct independence polynomials of labelled trees on m vertices (Pruefer)."""
    out = set()
    if m == 1: return {(1, 1)}
    if m == 2: return {(1, 2)}
    for code in itertools.product(range(m), repeat=m - 2):
        deg = [1] * m
        for x in code: deg[x] += 1
        edges = []; code = list(code)
        for x in code:
            leaf = min(v for v in range(m) if deg[v] == 1)
            edges.append((leaf, x)); deg[leaf] -= 1; deg[x] -= 1
        u, v = [w for w in range(m) if deg[w] == 1]; edges.append((u, v))
        adj = [0] * m
        for a, b in edges: adj[a] |= 1 << b; adj[b] |= 1 << a
        p = [0] * (m + 1)
        for mask in range(1 << m):
            if all(not (mask >> v & 1) or not (adj[v] & mask) for v in range(m)): p[bin(mask).count('1')] += 1
        while p[-1] == 0: p.pop()
        out.add(tuple(p))
    return out
TP = {m: tree_polys(m) for m in range(1, 7)}
print('distinct tree polynomials of order 1..6:', {m: len(v) for m, v in TP.items()})
def forest_polys(m):
    """distinct polynomials of forests on exactly m vertices (multisets of trees)."""
    res = set()
    def rec(rem, maxm, cur):
        if rem == 0: res.add(tuple(cur)); return
        for s in range(min(rem, maxm), 0, -1):
            for tp in TP[s]:
                rec(rem - s, s, mul(cur, list(tp)))
    rec(m, m, [1])
    return res
FP = {m: forest_polys(m) for m in range(0, 7)}
print('distinct forest polynomials of order 0..6:', {m: len(v) for m, v in FP.items()})
def check(p, n):
    a = len(p) - 1
    q, top = (n + 3) // 4, (2 * a + 1) // 3
    k = 0
    while k < a and p[k] <= p[k + 1]: k += 1
    uni = all(p[t] >= p[t + 1] for t in range(k, a))
    wlc = all(p[t] ** 2 > p[t - 1] * p[t + 1] for t in range(max(q, 1), min(top, a - 1) + 1))
    m1 = all((r + 2) * p[r] * p[r + 2] <= (r + 1) * p[r + 1] ** 2 + p[r] * p[r + 1] for r in range(q, top - 1) if r + 2 <= a)
    return uni, wlc, m1
total = 0; fails = []
for nt, seqs in sorted(by_n.items()):
    for m in range(0, NMAX - nt + 1):
        for T in seqs:
            for R in FP[m]:
                p = mul(list(T), list(R)); total += 1
                u, w, m1 = check(p, nt + m)
                if not (u and w and m1): fails.append(dict(tree_order=nt, rest_order=m, T=T, R=R, unimodal=u, strict_wlc=w, m1=m1))
print('forests checked (distinct polynomial pairs):', total, 'failures:', len(fails))
json.dump(dict(NMAX=NMAX, nonlc_orders={n: len(v) for n, v in by_n.items()}, forest_polys={m: len(v) for m, v in FP.items()},
               checked=total, failures=fails), open(f'forest_nonlc_N{NMAX}.json', 'w'), indent=1)
