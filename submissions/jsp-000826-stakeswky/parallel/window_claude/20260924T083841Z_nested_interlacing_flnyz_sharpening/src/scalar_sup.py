"""Scalar ingredient of FLNYZ root_moments: with r = l e^{-y}, q = r/(1+r), A = log(1+r),
  F_p(l, y) = y q^p / A.  exists_scalar_two uses sup F_2 <= b = 999/1000; the Hoelder step needs sup F_p <= rho < 1.
Compute (numerically, fine grid + local refinement) sup F_p over l in K, y >= 0, for K = [1/4,12] and [1/4,3], and the
smallest p with sup F_p < 1 (then u = p/(2-p), a = 1 - 1/u = 2 - 2/p).  Also the formalised interpolation route."""
import math
def F(p, l, y):
    r = l*math.exp(-y); q = r/(1 + r); A = math.log1p(r)
    return y*q**p/A
def sup_F(p, lmin, lmax):
    best = 0.0; arg = None
    for i in range(401):
        l = lmin*(lmax/lmin)**(i/400)
        for j in range(1, 2001):
            y = 12*j/2000
            v = F(p, l, y)
            if v > best: best = v; arg = (l, y)
    l0, y0 = arg; h = 0.01
    for _ in range(60):
        for dl in (-h, 0, h):
            for dy in (-h, 0, h):
                l = min(max(l0*(1 + dl), lmin), lmax); y = max(y0 + dy, 1e-9)
                v = F(p, l, y)
                if v > best: best, l0, y0 = v, l, y
        h *= 0.8
    return best, (l0, y0)
for name, lo, hi in (('K=[1/4,12]', 0.25, 12.0), ('K=[1/4,3]', 0.25, 3.0), ('K=[1/4,2.6]', 0.25, 2.6)):
    b2, at = sup_F(2.0, lo, hi); b15, _ = sup_F(1.5, lo, hi)
    # formalised interpolation: theta = 1-(1-b)/8, p = 3/2+theta/2 with b replaced by the true sup
    th = 1 - (1 - b2)/8; p_int = 1.5 + th/2
    # optimal interpolation between exponents 3/2 and 2: need b2^theta * b15^(1-theta) < 1
    if b15 < 1: th_opt = 0.0
    else: th_opt = math.log(b15)/(math.log(b15) - math.log(b2))
    p_opt_int = 1.5 + th_opt/2
    # direct: smallest p with sup F_p < 1 (bisection)
    lo_p, hi_p = 1.0001, 2.0
    for _ in range(40):
        mid = (lo_p + hi_p)/2
        if sup_F(mid, lo, hi)[0] < 1: hi_p = mid
        else: lo_p = mid
    def ua(p): u = p/(2 - p); return u, 1 - 1/u
    print('%-12s sup F_2 = %.4f at (l,y)=(%.3g,%.3g); sup F_1.5 = %.4f' % (name, b2, at[0], at[1], b15))
    for tag, p in (('formalised interpolation with true b', p_int), ('optimal interpolation 3/2..2', p_opt_int), ('direct smallest p', hi_p)):
        u, a = ua(p); print('   %-38s p=%.5f  u=p/(2-p)=%9.2f  a=2-2/p=%.5f  1/(1-a)=%.1f' % (tag, p, u, a, 1/(1 - a)))
