"""Quantitative form of the remaining hypothesis in all +1 configurations (trees n <= NMAX):
   rise = Q_{m+1}-Q_m, phi = Q'_{m-1}-Q'_m (> rise by the configuration), gamma = 2Q_{m+1}-Q_m-Q_{m+2}.
   (LH) <=> gamma >= 2 rise, and gamma >= 2 phi suffices. Report max n*rise/Q_{m+1}, max n*phi/Q_{m+1},
   min n*gamma/Q_{m+1}, min gamma/(2 phi), by order and by deg w."""
import sys, collections
from fractions import Fraction as Fr
from modelib import *
from ma_forests import free_trees
NMAX = int(sys.argv[1])
for n in range(10, NMAX + 1):
    mx_rise = Fr(0); mx_phi = Fr(0); mn_gamma = None; mn_ratio = None; cnt = 0; bydeg = collections.defaultdict(lambda: [0, None])
    for lv in free_trees(n):
        par = parents_from_levels(lv); nb = neighbours(par)
        P = indep_poly_del(par); p1, p2, _ = mode_set(P)
        for w in range(n):
            Q = indep_poly_del(par, frozenset([w])); q1, q2, _ = mode_set(Q)
            if q1 != p2 + 1: continue
            Qp = indep_poly_del(par, frozenset(nb[w] | {w})); g = lambda s, k: s[k] if 0 <= k < len(s) else 0
            m = p2; rise = Q[m + 1] - Q[m]; phi = g(Qp, m - 1) - g(Qp, m); gamma = 2 * Q[m + 1] - Q[m] - g(Q, m + 2)
            cnt += 1
            mx_rise = max(mx_rise, Fr(n * rise, Q[m + 1])); mx_phi = max(mx_phi, Fr(n * phi, Q[m + 1]))
            gq = Fr(n * gamma, Q[m + 1]); mn_gamma = gq if mn_gamma is None else min(mn_gamma, gq)
            rt = Fr(gamma, 2 * phi); mn_ratio = rt if mn_ratio is None else min(mn_ratio, rt)
            d = len(nb[w]); bydeg[d][0] += 1; bydeg[d][1] = rt if bydeg[d][1] is None else min(bydeg[d][1], rt)
    print(f'n={n}: configs={cnt} max n*rise/Q={float(mx_rise):.3f} max n*phi/Q={float(mx_phi):.3f} min n*gamma/Q={float(mn_gamma) if mn_gamma is not None else None} min gamma/(2phi)={float(mn_ratio) if mn_ratio is not None else None} by_deg={ {d: (c, round(float(r),2)) for d, (c, r) in sorted(bydeg.items())} }', flush=True)
