"""High-precision (60-digit Decimal) recomputation of the adaptive nested-hub root moments, compared with the
double-precision recursion, for l = 1 (k=14 pattern, 1..6 double levels) and for the sharpness table's best
parameters at l = 1 and l = 3 (40 double levels)."""
import math
from decimal import Decimal as Dec, getcontext
getcontext().prec = 60
from nested_hubs import nested, sym
from rm_sharpness import build

def hp(counts, l):
    L = Dec(l); R = L; D = Dec(1); logn = None; n_dec = Dec(1)
    for c in counts:
        q = R/(1 + R); D = 1 - c*q*D; R = L*((-c*(1 + R).ln()).exp()); n_dec = 1 + c*n_dec
    q = R/(1 + R); return q*(1 - q)*D*D, n_dec

for levels in range(1, 7):
    cts = nested(1.0, 14, levels)
    Mh, nh = hp(cts, 1); Mf, logn, _, _ = sym(cts, 1.0)
    print('l=1 k=14 levels=%d: M(60 digits)=%.10E  M(double)=%.10E  rel.diff=%.1e  n~10^%.2f' % (levels, Mh, Mf, abs(float(Mh) - Mf)/float(Mh), float(nh.log10())))
for l, k, yt in ((1.0, 70, 3.146), (3.0, 18, 2.814)):
    cts = build(l, k, yt, 40)
    Mh, nh = hp(cts, l); Mf, logn, _, _ = sym(cts, l)
    print('l=%s k=%d y_t=%s, 40 double levels: log10 M (60 digits)=%.6f  (double)=%.6f  log10 n=%.3f  log M/log n=%.4f' % (
        l, k, yt, float(Mh.log10()), math.log10(Mf), float(nh.log10()), float(Mh.ln()/nh.ln())))
