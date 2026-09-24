"""Adversarial search for large root moments M(v) = q_v(1-q_v) delta_v^2 over trees of order n.
O(n) rerooting: for every directed edge (w|u) (subtree of w hanging away from u) compute odds R and meanDiff delta:
   R_{w|u} = l * prod_{x in N(w)-u} 1/(1+R_{x|w}),  delta_{w|u} = 1 - sum_{x in N(w)-u} q_{x|w} delta_{x|w}.
For the whole tree rooted at v: R_v = l prod_{x in N(v)} 1/(1+R_{x|v}), delta_v = 1 - sum q_{x|v} delta_{x|v}.
Local search: prune a random leaf and regraft it at a random vertex; accept if max_v max_l M does not decrease."""
import sys, os, math, random
from fractions import Fraction

def all_M(adj, l):
    n = len(adj); order = [0]; par = [-1]*n; seen = [False]*n; seen[0] = True
    for u in order:
        for w in adj[u]:
            if not seen[w]: seen[w] = True; par[w] = u; order.append(w)
    down_R = [0.0]*n; down_D = [0.0]*n   # (v | par[v])
    for v in reversed(order):
        prodinv = 1.0; s = 0.0
        for x in adj[v]:
            if x != par[v]:
                prodinv /= (1 + down_R[x]); s += down_R[x]/(1 + down_R[x]) * down_D[x]
        down_R[v] = l*prodinv; down_D[v] = 1 - s
    up_R = [0.0]*n; up_D = [0.0]*n       # (par[v] | v): subtree of par[v] away from v
    best = 0.0
    for v in order:
        nb = adj[v]
        vals = []
        for x in nb:
            if x == par[v]: vals.append((up_R[v], up_D[v]))
            else: vals.append((down_R[x], down_D[x]))
        # total product and sum
        logprod = sum(math.log1p(r) for r, d in vals); ssum = sum(r/(1 + r)*d for r, d in vals)
        Rv = l*math.exp(-logprod); qv = Rv/(1 + Rv); Dv = 1 - ssum
        M = qv*(1 - qv)*Dv*Dv
        if M > best: best = M
        for i, x in enumerate(nb):
            if x == par[v]: continue
            r, d = vals[i]
            Rx = l*math.exp(-(logprod - math.log1p(r))); Dx = 1 - (ssum - r/(1 + r)*d)
            up_R[x] = Rx; up_D[x] = Dx
    return best

def score(adj, lams): return max(all_M(adj, l) for l in lams)

def random_tree(n, rng):
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        u = rng.randrange(v); adj[u].append(v); adj[v].append(u)
    return adj

def climb(n, steps, seed, lams):
    rng = random.Random(seed); adj = random_tree(n, rng); cur = score(adj, lams)
    for _ in range(steps):
        leaves = [v for v in range(n) if len(adj[v]) == 1]
        v = rng.choice(leaves); u = adj[v][0]; w = rng.randrange(n)
        if w == v or w == u: continue
        adj[u].remove(v); adj[v] = [w]; adj[w].append(v)
        s = score(adj, lams)
        if s >= cur: cur = s
        else: adj[w].remove(v); adj[v] = [u]; adj[u].append(v)
    degs = sorted((len(a) for a in adj), reverse=True)
    return cur, degs[:6]

if __name__ == '__main__':
    lams = [0.25, 0.5, 1.0, 1.5, 2.0, 2.6, 3.0]
    # sanity: compare with the O(n^2) routine on a few random trees
    from root_moment_growth import all_roots_M
    rng = random.Random(1)
    for _ in range(5):
        adj = random_tree(40, rng)
        for l in (0.5, 2.6):
            a = all_M(adj, l); b = all_roots_M(adj, l)[0]
            assert abs(a - b) < 1e-9*max(1, b), (a, b)
    print('rerooting check vs direct computation: ok', flush=True)
    for n, steps in ((50, 3000), (100, 3000), (200, 2500), (400, 2000)):
        results = [climb(n, steps, s, lams) for s in range(3)]
        best = max(results, key=lambda r: r[0])
        print('n=%d: best max_v max_{l in [1/4,3]} q(1-q)delta^2 after local search = %.4f (top degrees %s); runs: %s' % (
            n, best[0], best[1], ', '.join('%.3f' % r[0] for r in results)), flush=True)
