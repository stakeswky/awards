"""Darroch-type mean-mode slack (DT), exact rationals. For k in the window [ceil(n/4), ceil((2a-1)/3)]:
  at lambda~ = p_k/p_{k+1} (tilt with P(k) = P(k+1)):   s+ = E|I| - k        (DT+ : s+ >= 0)
  at lambda^ = p_{k-1}/p_k (tilt with P(k-1) = P(k)):   s- = k - E|I|        (DT- : s- >= 0)
Both together imply p_{k-1}/p_k <= lambda_k <= p_k/p_{k+1}, hence tilted concavity (TC) and LC at k.
A symmetric distribution gives s+ = s- = 1/2. Report min s+, min s- over all trees n <= NMAX."""
import sys
from fractions import Fraction as Fr
from modelib import parents_from_levels, indep_poly_del
from ma_forests import free_trees
def tmean(p, lam):
    num = sum(Fr(j) * c * lam ** j for j, c in enumerate(p)); den = sum(c * lam ** j for j, c in enumerate(p)); return num / den
NMAX = int(sys.argv[1])
for n in range(6, NMAX + 1):
    mp = (Fr(99), None); mm = (Fr(99), None); cnt = 0
    for lv in free_trees(n):
        p = indep_poly_del(parents_from_levels(lv)); a = len(p) - 1
        q, top = (n + 3) // 4, (2 * a + 1) // 3
        for k in range(max(q, 1), min(top, a - 1) + 1):
            cnt += 1
            sp = tmean(p, Fr(p[k], p[k + 1])) - k
            sm = k - tmean(p, Fr(p[k - 1], p[k]))
            if sp < mp[0]: mp = (sp, (lv, k))
            if sm < mm[0]: mm = (sm, (lv, k))
    print(f'n={n}: positions={cnt} min s+ = {float(mp[0]):.4f} at {mp[1]} | min s- = {float(mm[0]):.4f} at {mm[1]}', flush=True)
