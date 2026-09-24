"""Stress test of STEP_nested (nested witnesses, IH-only bounds, c = 3/2) on large non-unique-MIS forests:
(a) s P3 + m K1 + K2 (component level; nested vertices = the K2 endpoints and any others);
(b) R(s,1): root with one pendant leaf joined to the centres of s cherries;
(c) random trees (Pruefer), n = 40..70, non-unique MIS only."""
import sys, os, random
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from comp_step import pmul, ppow, g, top
C = Fr(3, 2)

def ih(P, i, nP):
    a = len(P) - 1
    if i <= 0: return Fr(P[0]**2)
    if i > a: return Fr(0)
    if i == a: return Fr(P[i]**2)
    assert i <= top(a), (i, a)
    return C/nP*P[i]**2

def nested_step_pieces(p, n, pieces):
    """pieces: list of (A, C, deg) for candidate vertices; returns (Q_ok, failing ks, min best slack)"""
    a = len(p) - 1; ks = list(range(1, min(top(a), a - 1) + 1)) if a >= 2 else []
    Qok = all((p[k]**2 - p[k-1]*p[k+1]) * n >= C * p[k]**2 for k in ks)
    nested = [(A, Cp, d) for A, Cp, d in pieces if len(A) - 1 == a and len(Cp) - 1 == a - 1]
    if not nested: return Qok, None, None
    best = {}
    for k in ks:
        for A, Cp, d in nested:
            X = g(A, k-1)*g(Cp, k) + g(A, k+1)*g(Cp, k-2) - 2*g(A, k)*g(Cp, k-1)
            val = (ih(A, k, n - 1) + ih(Cp, k - 1, n - 1 - d) - X - C/n*p[k]**2) * n / p[k]**2
            if k not in best or val > best[k]: best[k] = val
    return Qok, [k for k in ks if best[k] < 0], (min(best.values()) if best else None)

def job_a(args):
    s, m = args
    P3 = [1, 3, 1]; B = [1, 1]; K2 = [1, 2]
    base = pmul(ppow(P3, s), ppow(B, m))
    p = pmul(base, K2); n = 3*s + m + 2
    pieces = [(pmul(base, B), base, 1)]                                  # K2 endpoint
    if m: pieces.append((pmul(pmul(ppow(P3, s), ppow(B, m-1)), K2), pmul(pmul(ppow(P3, s), ppow(B, m-1)), K2), 0))   # K1
    if s:
        rest = pmul(pmul(ppow(P3, s-1), ppow(B, m)), K2)
        pieces.append((pmul(rest, ppow(B, 2)), rest, 2))                 # P3 centre
        pieces.append((pmul(rest, [1, 2]), pmul(rest, B), 1))            # P3 leaf
    return ('a', s, m, n) + nested_step_pieces(p, n, pieces)

def vertex_level(par):
    n = len(par); ch = L.children_of(par); p = L.uni_poly(par, ch)
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    pieces = [(L.uni_poly(par, ch, removed=frozenset([v])), L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v})), len(nbr[v])) for v in range(n)]
    return nested_step_pieces(p, n, pieces)

def job_b(s):
    par = [-1, 0]
    for i in range(s):
        par.append(0); c = len(par) - 1; par += [c, c]
    return ('b', s, 1, len(par)) + vertex_level(par)

def pruefer_tree(n, rng):
    seq = [rng.randrange(n) for _ in range(n - 2)]
    deg = [1]*n
    for x in seq: deg[x] += 1
    edges = []
    import heapq
    leaves = [i for i in range(n) if deg[i] == 1]; heapq.heapify(leaves)
    for x in seq:
        l = heapq.heappop(leaves); edges.append((l, x)); deg[x] -= 1
        if deg[x] == 1: heapq.heappush(leaves, x)
    u = heapq.heappop(leaves); w = heapq.heappop(leaves); edges.append((u, w))
    adj = [[] for _ in range(n)]
    for u, w in edges: adj[u].append(w); adj[w].append(u)
    order = [0]; par = {0: -1}; i = 0
    while i < len(order):
        u = order[i]; i += 1
        for w in adj[u]:
            if w not in par: par[w] = u; order.append(w)
    idx = {v: j for j, v in enumerate(order)}
    return [(-1 if par[v] < 0 else idx[par[v]]) for v in order]

def job_c(args):
    n, seed = args
    return ('c', n, seed, n) + vertex_level(pruefer_tree(n, random.Random(seed)))

if __name__ == '__main__':
    with Pool(3) as pool:
        ra = list(pool.imap_unordered(job_a, [(s, m) for s in range(0, 40) for m in range(0, 60) if 3*s + m + 2 <= 140], chunksize=10))
        rb = list(pool.imap_unordered(job_b, range(1, 30), chunksize=1))
        rc = list(pool.imap_unordered(job_c, [(n, 1000*n + j) for n in range(40, 71, 5) for j in range(30)], chunksize=2))
    for name, rs in (('(a) sP3+mK1+K2, n<=140', ra), ('(b) R(s,1), n<=88', rb), ('(c) random trees n=40..70', rc)):
        withn = [r for r in rs if r[5] is not None]
        bad = [r for r in withn if r[5]]
        print('%s: %d cases | Q fails %d | with nested vertex %d | STEP_nested fails %d %s | min slack %.4f' % (
            name, len(rs), sum(1 for r in rs if not r[4]), len(withn), len(bad), [(r[1], r[2], r[3], r[5]) for r in sorted(bad, key=lambda r: r[3])[:4]],
            float(min(r[6] for r in withn if r[6] is not None)) if any(r[6] is not None for r in withn) else float("nan")), flush=True)
