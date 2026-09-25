"""Tilted concavity at the mean (TC): for integer k in the window [ceil(n/4), ceil((2a-1)/3)], let
lambda_k solve E_lambda|I| = k. (TC) says P_lambda(k) >= (P_lambda(k-1) + P_lambda(k+1))/2, i.e.
2 p_k >= p_{k-1}/lambda + lambda p_{k+1}. By AM-GM, (TC) at k implies LC at k. Report failures and the
minimal normalised slack n*(2p_k - p_{k-1}/lambda - lambda p_{k+1})/(2 p_k) over all trees n <= NMAX."""
import sys
from modelib import parents_from_levels, indep_poly_del
from ma_forests import free_trees
def mean(p, lam):
    num = sum(k * c * lam ** k for k, c in enumerate(p)); den = sum(c * lam ** k for k, c in enumerate(p)); return num / den
def solve(p, k):
    lo, hi = 1e-9, 1e9
    for _ in range(200):
        mid = (lo * hi) ** 0.5
        if mean(p, mid) < k: lo = mid
        else: hi = mid
    return (lo * hi) ** 0.5
NMAX = int(sys.argv[1])
for n in range(6, NMAX + 1):
    fails = 0; minslack = 1e9; arg = None; cnt = 0; maxlam = 0
    for lv in free_trees(n):
        p = indep_poly_del(parents_from_levels(lv)); a = len(p) - 1
        q, top = (n + 3) // 4, (2 * a + 1) // 3
        for k in range(max(q, 1), min(top, a - 1) + 1):
            lam = solve(p, k); cnt += 1; maxlam = max(maxlam, lam)
            s = n * (2 * p[k] - p[k - 1] / lam - lam * p[k + 1]) / (2 * p[k])
            if s < 0: fails += 1
            if s < minslack: minslack, arg = s, (lv, k, round(lam, 3))
    print(f'n={n}: window positions={cnt} TC failures={fails} min n*slack={minslack:.4f} max lambda_k={maxlam:.3f} at {arg}', flush=True)
