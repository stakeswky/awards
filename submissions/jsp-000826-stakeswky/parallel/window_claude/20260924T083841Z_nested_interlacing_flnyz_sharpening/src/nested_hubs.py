"""Spherically symmetric trees with prescribed child counts per level (bottom-up): exact level recursion
   R_i = l (1+R_{i-1})^{-c_i},  q_i = R_i/(1+R_i),  delta_i = 1 - c_i q_{i-1} delta_{i-1},  leaves: R_0 = l, delta_0 = 1,
root moment M = q(1-q) delta^2 at the root; n = number of vertices.  'Nested hubs': alternate hub levels (k children)
and gather levels (d children, d ~ 1/q_hub so that y ~ 1).  Reports log M / log n (the effective root-moment exponent)."""
import math, sys
from fractions import Fraction as Fr

def sym(counts, l):
    R, D, n = l, 1.0, 1                         # leaf
    logn = 0.0
    for c in counts:
        q = R/(1 + R)
        D = 1 - c*q*D
        R = l*math.exp(-c*math.log1p(R))
        n_log = math.log(c) + logn if logn else math.log(c)
        logn = math.log(1 + math.exp(n_log)) if n_log < 700 else n_log   # n_new = 1 + c*n_old (log-space)
    q = R/(1 + R)
    return q*(1 - q)*D*D, logn, q, D

def sym_exact(counts, l):
    """exact rational version (small instances)"""
    R, D, n = Fr(l), Fr(1), 1
    for c in counts:
        q = R/(1 + R); D = 1 - c*q*D; R = Fr(l)/(1 + R)**c; n = 1 + c*n
    q = R/(1 + R); return q*(1 - q)*D*D, n

def nested(l, k, levels):
    counts = []; R = l
    for _ in range(levels):
        counts.append(k)                        # hub level: k children
        R = l*math.exp(-k*math.log1p(R))
        d = max(1, round(1/(R/(1 + R))))        # gather level: ~1/q_hub children
        counts.append(d)
        R = l*math.exp(-d*math.log1p(R))
    return counts

if __name__ == '__main__':
    # exact cross-check of the float recursion on a small instance
    c = [3, 5, 3, 5]
    Mf, lnf, _, _ = sym(c, 1.0); Me, ne = sym_exact(c, 1)
    print('check small instance: float M=%.12f exact M=%.12f, n=%d (log n float %.6f exact %.6f)' % (Mf, float(Me), ne, lnf, math.log(ne)))
    for l in (0.25, 1.0, 2.0, 2.6, 3.0, 12.0):
        best = None
        for k in range(2, 40):
            for levels in (1, 2, 3, 4, 6):
                counts = nested(l, k, levels)
                M, logn, q, D = sym(counts, l)
                if logn <= 0: continue
                expo = math.log(M)/logn if M > 1 else 0.0
                rec = (expo, k, levels, M, logn/math.log(10))
                if levels >= 2 and (best is None or rec > best): best = rec
        print('l=%-5s best nested-hub pattern: k=%d, %d double levels: M=%.4g at n~10^%.1f, log M/log n = %.3f' % (l, best[1], best[2], best[3], best[4], best[0]))
    print('growth along one pattern (l=1, k=14):')
    for levels in range(1, 7):
        M, logn, q, D = sym(nested(1.0, 14, levels), 1.0)
        print('   double levels=%d: n~10^%.1f  M=%.4g  log M/log n=%.3f  (0.13 ln n would be %.2f)' % (levels, logn/math.log(10), M, math.log(M)/logn, 0.13*logn))
