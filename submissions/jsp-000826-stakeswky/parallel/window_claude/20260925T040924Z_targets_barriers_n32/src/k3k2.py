"""Cumulant ratio r(lambda) = kappa3/kappa2 of X = |I| under the hard-core measure at activity lambda.
(Phi3) |r(lambda)| <= 1 holds for sums of independent Bernoullis (real-rooted polynomials) and is closed
under disjoint union (products). Test it for all trees n <= NMAX on a lambda grid, report
max |r| over lambda <= L for several L, and the smallest lambda at which |r| > 1 (if any)."""
import sys, math
from modelib import parents_from_levels, indep_poly_del
from ma_forests import free_trees
def cumulants(p, lam):
    # moments of X under P(j) ∝ p_j lam^j, computed stably in floating point with scaling
    lw = [math.log(c) + j * math.log(lam) for j, c in enumerate(p)]
    mx = max(lw); w = [math.exp(x - mx) for x in lw]; Z = sum(w)
    m1 = sum(j * x for j, x in enumerate(w)) / Z
    c2 = sum((j - m1) ** 2 * x for j, x in enumerate(w)) / Z
    c3 = sum((j - m1) ** 3 * x for j, x in enumerate(w)) / Z
    return m1, c2, c3
if __name__ == '__main__':
    NMAX = int(sys.argv[1]); grid = [math.exp(t / 20) for t in range(-80, 81)]   # lambda in [e^-4, e^4]
    Ls = (1, 2, 4, 8, 12, 20, 54.6)
    for n in range(6, NMAX + 1):
        worst = {L: (0, None) for L in Ls}; first_bad = (1e9, None)
        for lv in free_trees(n):
            p = indep_poly_del(parents_from_levels(lv))
            for lam in grid:
                m1, c2, c3 = cumulants(p, lam); r = abs(c3) / c2
                for L in Ls:
                    if lam <= L and r > worst[L][0]: worst[L] = (r, (lv, round(lam, 3), round(m1, 2)))
                if r > 1 and lam < first_bad[0]: first_bad = (lam, (lv, round(r, 3)))
        print(f'n={n}: ' + ' '.join(f'max|r|(lam<={L})={worst[L][0]:.3f}' for L in Ls) + f' | smallest lambda with |r|>1: {first_bad[0] if first_bad[1] else None} {first_bad[1]}', flush=True)
