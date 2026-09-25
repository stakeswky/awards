"""Extension-count identity for independent sets (any graph):
    mu_k = mu_{k-1} + Var_{k-1}(e)/mu_{k-1} - 1 - D_k
where e(J) = #vertices addable to J, mu_r = E_{J~Unif(I_r)} e(J) = (r+1)p_{r+1}/p_r,
and D_k = average over uniform extension pairs (J,v), |J|=k-1, v addable, of #addable neighbours of v.
Hence  LC at k  <=>  Var_{k-1}(e) <= mu_{k-1} (1 + D_k + mu_{k-1}/k),
and under-dispersion Var_{k-1}(e) <= mu_{k-1} is a sufficient condition for LC at k.
Tree DP tracks the joint law of (|J|, e(J)) exactly."""
import sys, os
from fractions import Fraction as Fr
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def padd(a, b):
    r = defaultdict(int)
    for k, v in a.items(): r[k] += v
    for k, v in b.items(): r[k] += v
    return {k: v for k, v in r.items() if v}
def pmul(a, b):
    r = defaultdict(int)
    for (i, j), v in a.items():
        for (k, l), w in b.items(): r[(i+k, j+l)] += v*w
    return dict(r)
def shift(a, di, dj): return {(i+di, j+dj): v for (i, j), v in a.items()}
def psub(a, b):
    r = dict(a)
    for k, v in b.items(): r[k] = r.get(k, 0) - v
    return {k: v for k, v in r.items() if v}

def size_free_poly(par):
    """G[(size, free)] = number of independent sets J with |J|=size and e(J)=free."""
    n = len(par); ch = L.children_of(par)
    In = [None]*n; Blk = [None]*n; Fr_ = [None]*n
    ONE = {(0, 0): 1}
    for v in range(n-1, -1, -1):
        inv = ONE; allv = ONE; nochild = ONE
        for c in ch[v]:
            inv = pmul(inv, padd(Blk[c], Fr_[c]))                       # c blocked by v, c not free
            allv = pmul(allv, padd(padd(In[c], Blk[c]), shift(Fr_[c], 0, 1)))
            nochild = pmul(nochild, padd(Blk[c], shift(Fr_[c], 0, 1)))  # c free iff unblocked & v not in J
        In[v] = shift(inv, 1, 0); Blk[v] = psub(allv, nochild); Fr_[v] = nochild
    r = 0
    return padd(padd(In[r], Blk[r]), shift(Fr_[r], 0, 1))

def moments(G, k):
    """count, mean, variance of e over independent k-sets."""
    tot = sum(v for (s, f), v in G.items() if s == k)
    if tot == 0: return 0, None, None
    m1 = Fr(sum(v*f for (s, f), v in G.items() if s == k), tot)
    m2 = Fr(sum(v*f*f for (s, f), v in G.items() if s == k), tot)
    return tot, m1, m2 - m1*m1

def brute_check(par):
    """verify the identity by literal enumeration (small trees)."""
    n = len(par); adj = [0]*n
    for v, p in enumerate(par):
        if p >= 0: adj[v] |= 1 << p; adj[p] |= 1 << v
    sets = []
    def rec(i, J):
        if i == n: sets.append(J); return
        rec(i+1, J)
        if not (adj[i] & J): rec(i+1, J | (1 << i))
    rec(0, 0)
    by = defaultdict(list)
    for J in sets: by[bin(J).count('1')].append(J)
    def ext(J):
        blocked = J
        for v in range(n):
            if J >> v & 1: blocked |= adj[v]
        return ((1 << n) - 1) & ~blocked
    ok = True
    for k in range(1, max(by)):
        Js = by[k-1]; es = [ext(J) for J in Js]; e = [bin(x).count('1') for x in es]
        pk1 = len(Js); mu_prev = Fr(sum(e), pk1); var = Fr(sum(x*x for x in e), pk1) - mu_prev**2
        pairs = sum(e); Dnum = 0
        for x in es:
            for v in range(n):
                if x >> v & 1: Dnum += bin(adj[v] & x).count('1')
        D = Fr(Dnum, pairs) if pairs else Fr(0)
        pk = len(by[k]); pk_1 = len(by.get(k+1, []))
        mu_k = Fr((k+1)*pk_1, pk)
        if pairs and mu_k != mu_prev + var/mu_prev - 1 - D: ok = False
    return ok

if __name__ == '__main__':
    import itertools
    # (a) identity by brute force on all trees n<=12
    cnt = 0
    for n in range(3, 13):
        for lv in L.free_trees(n):
            par = L.parents_from_levels(lv); assert brute_check(par), lv; cnt += 1
    print('identity verified by literal enumeration on all', cnt, 'trees with 3<=n<=12')
    # (b) DP consistency: marginal of G equals the independence polynomial
    for n in (10, 14):
        for lv in list(L.free_trees(n))[:200]:
            par = L.parents_from_levels(lv); G = size_free_poly(par); p = L.uni_poly(par, L.children_of(par))
            assert [sum(v for (s, f), v in G.items() if s == k) for k in range(len(p))] == p
    print('DP marginals equal independence polynomials (sampled n=10,14)')
