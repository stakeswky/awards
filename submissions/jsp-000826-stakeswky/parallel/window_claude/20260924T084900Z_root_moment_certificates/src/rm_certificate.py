"""Rigorous interval certificate for large root moments (refuting any polylogarithmic bound).
Tree: spherically symmetric, child counts per level given bottom-up (hub/gather levels of the adaptive construction,
counts fixed in advance).  n is computed exactly with integers.  The recursion
   R_i = l exp(-c_i ln(1+R_{i-1})),  q = R/(1+R),  D_i = 1 - c_i q_{i-1} D_{i-1},   M = q(1-q) D^2
is evaluated in interval arithmetic with Decimal at PREC digits; every ln/exp/division result (correctly rounded,
error <= 1/2 ulp) is widened outward by a relative 10^-(PREC-5)."""
import sys, math
from decimal import Decimal as Dec, getcontext
PREC = int(sys.argv[1]) if len(sys.argv) > 1 else 80
getcontext().prec = PREC
EPS = Dec(10) ** (-(PREC - 5))
def lo(x): return x - abs(x)*EPS
def hi(x): return x + abs(x)*EPS
def imul(a, b):
    ps = [a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]]
    return (lo(min(ps)), hi(max(ps)))

def certify(l, counts):
    L = Dec(l)
    R = (L, L); D = (Dec(1), Dec(1)); n = 1
    for c in counts:
        q = (lo(R[0]/(1 + R[0])), hi(R[1]/(1 + R[1])))            # q increasing in R
        cq = (q[0]*c, q[1]*c)
        t = imul(cq, D)
        D = (1 - t[1], 1 - t[0])
        # R_new = l exp(-c ln(1+R)) decreasing in R
        R = (lo(L*lo((-c*hi((1 + R[1]).ln())).exp())), hi(L*hi((-c*lo((1 + R[0]).ln())).exp())))
        n = 1 + c*n
    q = (lo(R[0]/(1 + R[0])), hi(R[1]/(1 + R[1])))
    qq = imul(q, (1 - q[1], 1 - q[0]))
    D2 = (min(abs(D[0]), abs(D[1]))**2 if D[0]*D[1] > 0 else Dec(0), max(abs(D[0]), abs(D[1]))**2)
    M = imul(qq, D2)
    return n, M, q

def adaptive_counts(l, k, yt, levels, prec=250):
    from decimal import localcontext
    with localcontext() as ctx:
        ctx.prec = prec; L = Dec(l); R = L; Y = Dec(yt); counts = []
        for _ in range(levels):
            counts.append(k); R = L*(-(k*(1 + R).ln())).exp()
            lg = (1 + R).ln(); d = max(1, int((Y/lg).to_integral_value())); counts.append(d); R = L*(-(d*lg)).exp()
        return counts

if __name__ == '__main__':
    from nested_hubs import nested
    for (l, name, counts) in ((1.0, 'l=1, k=14, 6 double levels (nested_hubs.py)', nested(1.0, 14, 6)),
                              (3.0, 'l=3, k=18, y_t=2.814, 24 double levels (rm_hp_adaptive.py)', adaptive_counts(3.0, 18, 2.814, 24))):
        n, M, q = certify(l, counts)
        lnn = math.log(n)
        print('%s\n   n = %d digits (log10 n = %.3f); certified M in [%.6E, %.6E]; q_root in [%.4f, %.4f]' % (name, len(str(n)), math.log10(n), M[0], M[1], q[0], q[1]))
        print('   (ln n)^2 = %.4g, (ln n)^3 = %.4g, certified M / (ln n)^2 >= %.4g, log M / log n >= %.4f' % (lnn**2, lnn**3, float(M[0])/lnn**2, math.log(float(M[0]))/lnn))
