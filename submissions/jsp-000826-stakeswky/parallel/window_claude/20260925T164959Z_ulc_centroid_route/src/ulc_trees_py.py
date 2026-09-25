"""Independent Python check of ULC(infinity), k p_k^2 >= (k+1) p_{k-1} p_{k+1}, for every tree of order
4..NMAX (free trees from the WROM level-sequence generator of ma_forests.py; polynomials from modelib.py)."""
import sys, collections
from ma_forests import free_trees
from modelib import parents_from_levels, indep_poly_del
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
for n in range(4, NMAX + 1):
    cnt = 0; fails = 0; where = collections.Counter()
    for lv in free_trees(n):
        p = indep_poly_del(parents_from_levels(lv)); cnt += 1; a = len(p) - 1
        bad = [k for k in range(1, a) if k * p[k] * p[k] < (k + 1) * p[k - 1] * p[k + 1]]
        if bad:
            fails += 1
            for k in bad: where[a - k] += 1
    print(n, 'trees', cnt, 'ULC-failing trees', fails, 'failure positions (alpha - k):', dict(sorted(where.items())), flush=True)
