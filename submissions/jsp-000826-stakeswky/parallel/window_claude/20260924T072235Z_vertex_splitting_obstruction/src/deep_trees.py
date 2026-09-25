"""Adversarial WindowLC tests on large structured / random trees (exact integers).
Spherically symmetric trees use the rooted recursion A' = (A+B)^b, B' = x A^b with big-integer
polynomial arithmetic; random trees use Pruefer sequences + the Kronecker DP of e993lib."""
import sys, os, random
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def pmul(a, b):
    # Kronecker substitution with base 2^W, all coefficients nonnegative
    W = max(max(a).bit_length(), 1) + max(max(b).bit_length(), 1) + (min(len(a), len(b))).bit_length() + 2
    ia = sum(c << (W * i) for i, c in enumerate(a)); ib = sum(c << (W * i) for i, c in enumerate(b))
    prod = ia * ib; mask = (1 << W) - 1; out = []
    for _ in range(len(a) + len(b) - 1):
        out.append(prod & mask); prod >>= W
    return out
def ppow(a, e):
    r = [1]
    while e:
        if e & 1: r = pmul(r, a)
        a = pmul(a, a) if e > 1 else a; e >>= 1
    return r
def padd(a, b):
    m = max(len(a), len(b)); return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(m)]

def spherical(branching):
    """branching[i] = number of children of every vertex at depth i (root depth 0). Returns (n, p)."""
    A, B = [1], [0, 1]; n_sub = 1
    for b in reversed(branching):
        A, B = ppow(padd(A, B), b), [0] + ppow(A, b)
        n_sub = 1 + b * n_sub
    p = padd(A, B)
    while p[-1] == 0: p.pop()
    return n_sub, p

def check(n, p):
    a = len(p) - 1; lo = (n + 3) // 4; hi = (2 * a + 1) // 3
    nonlc = [k for k in range(1, a) if p[k] * p[k] < p[k - 1] * p[k + 1]]
    strict_fail = [k for k in range(max(lo, 1), min(hi, a - 1) + 1) if p[k] * p[k] <= p[k - 1] * p[k + 1]]
    k = 0
    while k < a and p[k] <= p[k + 1]: k += 1
    uni = all(p[t] >= p[t + 1] for t in range(k, a))
    # normalised window LC margin: min over window of 1 - p_{k-1}p_{k+1}/p_k^2, times n
    marg = min(((p[k] * p[k] - p[k - 1] * p[k + 1]) * n / (p[k] * p[k]) for k in range(max(lo, 1), min(hi, a - 1) + 1)), default=None)
    return dict(n=n, alpha=a, window=(lo, hi), unimodal=uni, window_strict_failures=strict_fail,
                nonLC=nonlc, first_nonLC_rel=(min(nonlc) / a if nonlc else None), min_window_margin_times_n=marg)

def pruefer_tree(n, rng):
    seq = [rng.randrange(n) for _ in range(n - 2)]
    deg = [1] * n
    for x in seq: deg[x] += 1
    import heapq
    leaves = [i for i in range(n) if deg[i] == 1]; heapq.heapify(leaves); edges = []
    for x in seq:
        leaf = heapq.heappop(leaves); edges.append((leaf, x)); deg[x] -= 1
        if deg[x] == 1: heapq.heappush(leaves, x)
    u, v = heapq.heappop(leaves), heapq.heappop(leaves); edges.append((u, v))
    adj = [[] for _ in range(n)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    order = [0]; par0 = {0: -1}; q = deque([0])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in par0: par0[y] = x; order.append(y); q.append(y)
    idx = {v: i for i, v in enumerate(order)}
    return [(-1 if par0[v] < 0 else idx[par0[v]]) for v in order]

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'regular':
        worst = None; fails = 0; count = 0; nonlc_seen = []
        for b in range(2, 7):
            d = 1
            while True:
                n = (b ** (d + 1) - 1) // (b - 1)
                if n > 4100: break
                n2, p = spherical([b] * d); assert n2 == n
                r = check(n, p); count += 1
                fails += bool(r['window_strict_failures']) or not r['unimodal']
                if r['nonLC']: nonlc_seen.append((b, d, n, r['first_nonLC_rel']))
                if worst is None or r['min_window_margin_times_n'] < worst[0]: worst = (r['min_window_margin_times_n'], b, d, n)
                print('complete %d-ary depth %d: n=%d alpha=%d unimodal=%s window strict failures=%s nonLC=%s first_nonLC/alpha=%s min window margin*n=%.3f' % (
                    b, d, n, r['alpha'], r['unimodal'], r['window_strict_failures'][:5], r['nonLC'][:6], None if r['first_nonLC_rel'] is None else round(r['first_nonLC_rel'], 4), r['min_window_margin_times_n']), flush=True)
                d += 1
        print('SUMMARY complete trees:', count, 'window/unimodality failures:', fails, 'worst margin*n:', worst)
    elif which == 'mixed':
        rng = random.Random(11); count = fails = 0; worst = None; nonlc = 0
        patterns = [[1, 2], [2, 1], [1, 3], [3, 1], [1, 1, 3], [3, 1, 1], [2, 3], [3, 2], [4, 1], [1, 4], [2, 2, 1], [5, 1, 1], [1, 5]]
        for pat in patterns:
            for reps in range(1, 12):
                br = (pat * reps)[:]
                for extra_root in (1, 2, 3, 4):
                    brr = [extra_root] + br
                    # size check
                    n = 1; m = 1
                    for b in brr: m *= b; n += m
                    if n > 3000: continue
                    n2, p = spherical(brr); r = check(n2, p); count += 1
                    fails += bool(r['window_strict_failures']) or not r['unimodal']; nonlc += bool(r['nonLC'])
                    if worst is None or r['min_window_margin_times_n'] < worst[0]: worst = (r['min_window_margin_times_n'], brr, n2)
                    if r['window_strict_failures'] or not r['unimodal']: print('FAIL', brr, r)
        print('SUMMARY spherically symmetric (mixed branching):', count, 'failures:', fails, 'non-LC trees:', nonlc, 'worst margin*n:', worst)
    elif which == 'random':
        rng = random.Random(2026); count = fails = nonlc = 0; worst = None
        for n in list(range(40, 201, 10)) + [250, 300, 400]:
            for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 200):
                par = pruefer_tree(n, rng); p = L.uni_poly(par, L.children_of(par)); r = check(n, p); count += 1
                fails += bool(r['window_strict_failures']) or not r['unimodal']; nonlc += bool(r['nonLC'])
                if worst is None or r['min_window_margin_times_n'] < worst[0]: worst = (r['min_window_margin_times_n'], n)
                if r['window_strict_failures'] or not r['unimodal']: print('FAIL', n, r)
        print('SUMMARY uniform random labelled trees:', count, 'failures:', fails, 'non-LC trees:', nonlc, 'worst margin*n:', worst)
