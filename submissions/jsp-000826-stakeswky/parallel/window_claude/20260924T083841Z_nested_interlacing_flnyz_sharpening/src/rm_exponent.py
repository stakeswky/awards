"""Lower bounds for the true root-moment exponent a*(l) = limsup log M / log n, M = q(1-q) delta^2 at the root,
from spherically symmetric trees whose child counts repeat a period (c_1, ..., c_P) (bottom-up).
On the periodic orbit of R, delta grows per period by G = prod_i (c_i q_{i-1}) (affine recursion delta_i = 1 - c_i q_{i-1} delta_{i-1}),
and n grows by prod_i c_i; hence M ~ n^{a} with a = 2 log|G| / log prod c_i, provided |G| > 1 and the root level has q bounded
below.  We optimise period-2 and period-3 patterns by grid search, then confirm on explicit finite trees (level recursion)."""
import math, itertools
from nested_hubs import sym

def orbit_rate(counts, l, iters=4000):
    R = l
    for _ in range(iters):
        for c in counts: R = l*math.exp(-c*math.log1p(R))
    G = 1.0; logN = 0.0
    for c in counts:
        q = R/(1 + R); G *= c*q; R = l*math.exp(-c*math.log1p(R)); logN += math.log(c)
    R2 = R
    for c in counts: R2 = l*math.exp(-c*math.log1p(R2))
    stable = abs(R2 - R) < 1e-9*max(1.0, R)
    if not stable:                                   # P-step map on a 2-cycle: use the doubled period
        R = R2; G = 1.0; logN = 0.0
        for c in list(counts)*2:
            q = R/(1 + R); G *= c*q; R = l*math.exp(-c*math.log1p(R)); logN += math.log(c)
        stable = True
    return (2*math.log(abs(G))/logN if abs(G) > 1 else 0.0), G, stable

for l in (0.25, 0.5, 1.0, 2.0, 2.6, 3.0, 7.0, 12.0):
    best = (0, None, None)
    for k in list(range(2, 60)) + [70, 90, 120, 160, 220, 300, 400]:
        for d in list(range(1, 60)) + [70, 90, 120, 160, 220, 300, 500, 800, 1200, 2000, 4000, 8000]:
            a, G, st = orbit_rate((k, d), l)
            if st and a > best[0]: best = (a, (k, d), G)
    b3 = (0, None)
    for k in range(2, 40, 2):
        for d in (1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987):
            for e in (1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233):
                a, G, st = orbit_rate((k, d, e), l)
                if st and a > b3[0]: b3 = (a, (k, d, e))
    # confirm on explicit finite trees: repeat the best period-2 pattern, root at the end of a period
    if best[1] is None:
        print('l=%-5s no growing period-2 pattern found' % l, flush=True); continue
    k, d = best[1]; confirm = []
    for per in (4, 8, 16):
        M, logn, q, D = sym([k, d]*per, l)
        confirm.append('%d periods: log M/log n=%.3f (n~10^%.0f, q_root=%.3f)' % (per, math.log(M)/logn if M > 1 else 0, logn/math.log(10), q))
    print('l=%-5s period-2 best (k,d)=%s: a=%.3f (growth/period %.3g) | period-3 best %s: a=%.3f | finite check: %s' % (l, best[1], best[0], best[2], b3[1], b3[0], '; '.join(confirm)), flush=True)
