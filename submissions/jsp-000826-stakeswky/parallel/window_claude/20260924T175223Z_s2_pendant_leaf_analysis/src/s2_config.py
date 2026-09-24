"""All '+1 configurations' (H, w): H a tree with n <= NMAX, w a vertex, with
    min M(I(H-w)) = max M(I(H)) + 1.
For each, with P = I(H), Q = I(H-w), Q' = I(H-N[w]), m = max M(P):
   (*)  margin  = (Q'_m - Q'_{m+1}) - (Q_{m+2} - Q_m)     [ (S2) at this (H,w) <=> margin >= 0 ]
   left-heavy   = Q_m >= Q_{m+2}                            [ makes (*) automatic ]
   dagger       = (Q'_{m-1} - Q'_m) - (Q_{m+1} - Q_m) > 0   [ the configuration itself ]
   fall ratio   = (Q'_m - Q'_{m+1}) / (Q'_{m-1} - Q'_m)
   concave Q'@m = Q'_{m-1} - 2Q'_m + Q'_{m+1} <= 0
   LC Q'@m      = Q'_m^2 >= Q'_{m-1} Q'_{m+1}
Exact rationals."""
import sys, collections
from fractions import Fraction as Fr
from modelib import *
from ma_forests import free_trees
NMAX = int(sys.argv[1])
stats = collections.Counter(); worst_margin = None; minratio = None; examples = []
for n in range(4, NMAX + 1):
    for lv in free_trees(n):
        par = parents_from_levels(lv); nb = neighbours(par)
        P = indep_poly_del(par); p1, p2, _ = mode_set(P)
        for w in range(n):
            Q = indep_poly_del(par, frozenset([w])); q1, q2, _ = mode_set(Q)
            if q1 != p2 + 1: continue
            Qp = indep_poly_del(par, frozenset(nb[w] | {w}))
            g = lambda s, k: s[k] if 0 <= k < len(s) else 0
            m = p2
            fall_prev = g(Qp, m - 1) - g(Qp, m); fall = g(Qp, m) - g(Qp, m + 1)
            rise = Q[m + 1] - Q[m]; rhs = g(Q, m + 2) - Q[m]
            margin = fall - rhs
            stats['configs'] += 1
            stats['deg%d' % len(nb[w])] += 1
            stats['left_heavy'] += (Q[m] >= g(Q, m + 2))
            stats['margin_ge_0'] += (margin >= 0)
            stats['dagger_ok'] += (fall_prev > rise)
            stats['concave'] += (g(Qp, m - 1) - 2 * g(Qp, m) + g(Qp, m + 1) <= 0)
            stats['LC_Qp_at_m'] += (g(Qp, m) ** 2 >= g(Qp, m - 1) * g(Qp, m + 1))
            stats['fall_ge_rise'] += (fall >= rise)
            stats['Q_plateau'] += (q2 > q1)
            stats['Qp_mode_le_m-1'] += (mode_set(Qp)[1] <= m - 1)
            r = Fr(fall, fall_prev) if fall_prev > 0 else None
            if r is not None and (minratio is None or r < minratio[0]): minratio = (r, n, w, par)
            rel = Fr(margin, g(Qp, m)) if g(Qp, m) else None
            if rel is not None and (worst_margin is None or rel < worst_margin[0]): worst_margin = (rel, n, w, par, margin, fall, rhs, rise, fall_prev)
            if not (Q[m] >= g(Q, m + 2)): examples.append((n, w, par, m, Q[m:m+3], Qp[m-1:m+2], margin))
print(dict(stats))
print('min relative margin (margin/Q\'_m):', worst_margin[0], 'at n=%d w=%d' % (worst_margin[1], worst_margin[2]), 'margin/fall/rhs/rise/fall_prev', worst_margin[4:])
print('min fall ratio Q\' (fall at m)/(fall at m-1):', minratio[0], float(minratio[0]), 'n=%d w=%d' % (minratio[1], minratio[2]))
print('right-skewed examples (Q_m < Q_{m+2}):', len(examples))
for e in examples[:8]: print('  ', e)
