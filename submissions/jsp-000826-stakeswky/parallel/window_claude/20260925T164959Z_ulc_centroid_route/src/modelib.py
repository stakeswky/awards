"""Mode-set utilities and vertex-split polynomials for forests given as parent arrays
(parent index < child index within each tree; roots have parent -1; forests allowed)."""
from ip import mul, add
def indep_poly_del(par, deleted=frozenset()):
    n = len(par)
    A = [[1] for _ in range(n)]
    B = [[0, 1] if v not in deleted else [0] for v in range(n)]
    for v in range(n - 1, -1, -1):
        u = par[v]
        if u < 0: continue
        A[u] = mul(A[u], add(A[v], B[v]))
        if u not in deleted: B[u] = mul(B[u], A[v])
    p = [1]
    for v in range(n):
        if par[v] < 0: p = mul(p, add(A[v], B[v]))
    while len(p) > 1 and p[-1] == 0: p.pop()
    return p
def mode_set(p):
    mx = max(p); lo = p.index(mx); hi = len(p) - 1 - p[::-1].index(mx)
    uni = all(p[k] <= p[k + 1] for k in range(lo)) and all(p[k] >= p[k + 1] for k in range(hi, len(p) - 1)) and all(p[k] == mx for k in range(lo, hi + 1))
    return lo, hi, uni
def dist(a1, a2, b1, b2):
    if b1 > a2: return b1 - a2
    if a1 > b2: return a1 - b2
    return 0
def neighbours(par):
    n = len(par); nb = [set() for _ in range(n)]
    for v in range(n):
        if par[v] >= 0: nb[v].add(par[v]); nb[par[v]].add(v)
    return nb
def split_alignment(par, v, nb=None):
    """returns (dist(M(A), M(C)+1), M(A), M(C)) for A = I(F-v), C = I(F-N[v])"""
    nb = nb or neighbours(par)
    pa = indep_poly_del(par, frozenset([v])); pc = indep_poly_del(par, frozenset(nb[v] | {v}))
    a1, a2, ua = mode_set(pa); c1, c2, uc = mode_set(pc)
    assert ua and uc
    return dist(a1, a2, c1 + 1, c2 + 1), (a1, a2), (c1, c2)
def parents_from_levels(lv):
    par = [-1]; st = [0]
    for i in range(1, len(lv)):
        while lv[st[-1]] >= lv[i]: st.pop()
        par.append(st[-1]); st.append(i)
    return par
