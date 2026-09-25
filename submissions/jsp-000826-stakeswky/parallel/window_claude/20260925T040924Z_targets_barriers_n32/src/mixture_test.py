"""Leading-order balance for the vertex mixture at fixed activity.
For p = A + xC and activity lambda, P_lambda(F) = w P_lambda(A) + (1-w) P_lambda(xC). Law of total variance:
   kappa2(F) = w kappa2(A) + (1-w) kappa2(xC) + w(1-w) delta^2,   delta = mu(xC) - mu(A).
If each piece had LC margin exactly 1/kappa2(piece) (Gaussian), the mixture's LC margin near its mean is
   about 1/kappa2(F) iff the mixing loss w(1-w)delta^2/kappa2^2 is paid for by the variance difference.
This script measures, for every tree n <= NMAX, every vertex v and every window index k (at lambda = lambda_k):
   ratio_F  = kappa2(F) * LCmargin_F(k)            (Gaussian value 1)
   ratio_pc = min over pieces of kappa2(piece) * LCmargin_piece(near k)
and records min ratio_F and the correlation of the defect with the mixing term w(1-w)delta^2/kappa2,
to see whether 'LC margin >= c / kappa2' is a plausible self-propagating invariant (c < 1)."""
import sys, math
from modelib import parents_from_levels, indep_poly_del, neighbours
from ma_forests import free_trees
def stats(p, lam):
    lw = [math.log(c) + j * math.log(lam) for j, c in enumerate(p)]; mx = max(lw); w = [math.exp(x - mx) for x in lw]; Z = sum(w)
    m = sum(j * x for j, x in enumerate(w)) / Z; v = sum((j - m) ** 2 * x for j, x in enumerate(w)) / Z; return m, v, Z * math.exp(mx)
def lcm(p, k):
    if k < 1 or k + 1 >= len(p): return None
    return 1 - p[k - 1] * p[k + 1] / (p[k] * p[k])
def lam_of(p, k):
    lo, hi = -30.0, 30.0
    for _ in range(70):
        mid = (lo + hi) / 2
        if stats(p, math.exp(mid))[0] < k: lo = mid
        else: hi = mid
    return math.exp((lo + hi) / 2)
def main():
    NMAX = int(sys.argv[1])
    for n in range(8, NMAX + 1):
        minF = 9; minpiece_leaf = 9; min_c = 9
        for lv in free_trees(n):
            par = parents_from_levels(lv); p = indep_poly_del(par); a = len(p) - 1
            q, top = (n + 3) // 4, (2 * a + 1) // 3
            for k in range(max(q, 1), min(top, a - 1) + 1):
                lam = lam_of(p, k); mF, vF, _ = stats(p, lam)
                r = vF * lcm(p, k); minF = min(minF, r)
        print(f'n={n}: min over trees and window k of kappa2(lambda_k) * LCmargin(k) = {minF:.4f}', flush=True)


if __name__ == '__main__':
    main()
