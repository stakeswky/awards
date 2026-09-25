"""Joint Darroch interlacing (JDT) for a vertex split p = A + xC, A = I(F-v), C = I(F-N[v]).
Coefficient ratios rho_j(S) = S_j/S_{j+1}; mean-activities lam_j(S) = activity with tilted mean j.
Lemma: rho_k(p) lies between rho_k(A) and rho_{k-1}(C) (mediant); lam_k(p) lies between lam_k(A)
and lam_{k-1}(C) (convex combination of increasing means). Hence DT_k(p) follows from
   max(rho_{k-1}(A), rho_{k-2}(C)) <= min(lam_k(A), lam_{k-1}(C))  and
   max(lam_k(A), lam_{k-1}(C)) <= min(rho_k(A), rho_{k-1}(C)).                         (JDT_k)
Test: for every tree n <= NMAX, does some vertex v satisfy JDT_k for all k in the window of F?"""
import sys, math
from modelib import parents_from_levels, indep_poly_del, neighbours
from ma_forests import free_trees
def mean(p, lam):
    lw = [math.log(c) + j * math.log(lam) if c > 0 else -1e300 for j, c in enumerate(p)]; mx = max(lw)
    w = [math.exp(x - mx) for x in lw]; return sum(j * x for j, x in enumerate(w)) / sum(w)
def lam_of(p, k):
    if k <= 0 or k >= len(p) - 1 + 1e-9: return None
    lo, hi = -40.0, 40.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if mean(p, math.exp(mid)) < k: lo = mid
        else: hi = mid
    return math.exp((lo + hi) / 2)
def rho(p, j): return p[j] / p[j + 1] if 0 <= j and j + 1 < len(p) and p[j + 1] > 0 else (0.0 if j < 0 else math.inf)
NMAX = int(sys.argv[1]); EPS = 1e-12
for n in range(4, NMAX + 1):
    trees = 0; ok_trees = 0; bad = []
    for lv in free_trees(n):
        par = parents_from_levels(lv); nb = neighbours(par); p = indep_poly_del(par); a = len(p) - 1
        q, top = (n + 3) // 4, (2 * a + 1) // 3; ks = [k for k in range(max(q, 1), min(top, a - 1) + 1)]
        trees += 1; found = False
        for v in sorted(range(n), key=lambda v: len(nb[v])):
            A = indep_poly_del(par, frozenset([v])); C = indep_poly_del(par, frozenset(nb[v] | {v}))
            good = True
            for k in ks:
                la = lam_of(A, k) if k < len(A) - 1 else math.inf
                lc = lam_of(C, k - 1) if 0 < k - 1 < len(C) - 1 else (0.0 if k - 1 <= 0 else math.inf)
                lo_r = max(rho(A, k - 1), rho(C, k - 2)); hi_r = min(rho(A, k), rho(C, k - 1))
                if not (lo_r <= min(la, lc) * (1 + EPS) and max(la, lc) <= hi_r * (1 + EPS)): good = False; break
            if good: found = True; break
        ok_trees += found
        if not found and len(bad) < 3: bad.append(lv)
    print(f'n={n}: trees={trees} with a JDT vertex={ok_trees} without={trees - ok_trees} examples={bad}', flush=True)
