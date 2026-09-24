"""Margins of (LH) in all +1 configurations (H tree n<=NMAX, w any vertex):
  rise = Q_{m+1}-Q_m, fall = Q_{m+1}-Q_{m+2}  (Q = I(H-w), m = max M(I(H)))
  (LH) <=> fall >= rise.  Report min of fall/rise, and the sufficient condition
  S: (Q'_{m-1}-Q'_m)/Q_m <= (1/2)*(1 - rho_{m+1}/rho_m) with rho_k = Q_{k+1}/Q_k (LC margin of Q at m+1)."""
import sys, collections
from fractions import Fraction as Fr
from modelib import *
from ma_forests import free_trees
NMAX = int(sys.argv[1])
res = []
for n in range(4, NMAX + 1):
    cnt = 0; minr = None; S_fail = 0; deg2 = []
    for lv in free_trees(n):
        par = parents_from_levels(lv); nb = neighbours(par)
        P = indep_poly_del(par); p1, p2, _ = mode_set(P)
        for w in range(n):
            Q = indep_poly_del(par, frozenset([w])); q1, q2, _ = mode_set(Q)
            if q1 != p2 + 1: continue
            Qp = indep_poly_del(par, frozenset(nb[w] | {w})); g = lambda s, k: s[k] if 0 <= k < len(s) else 0
            m = p2; rise = Q[m + 1] - Q[m]; fall = Q[m + 1] - g(Q, m + 2); cnt += 1
            r = Fr(fall, rise)
            if minr is None or r < minr[0]: minr = (r, w, par, Q[m:m+3], Qp[max(0,m-1):m+2], len(nb[w]))
            lcm = 1 - Fr(g(Q, m + 2) * Q[m], Q[m + 1] ** 2)     # 1 - rho_{m+1}/rho_m
            lhs = Fr(g(Qp, m - 1) - g(Qp, m), Q[m])
            if lhs > lcm / 2: S_fail += 1
            if len(nb[w]) == 2: deg2.append((w, par, m, Q[m-1:m+3], Qp[max(0,m-2):m+2], P[m-1:m+3]))
    mr = ('%.3f' % float(minr[0])) if minr else 'n/a'
    print(f'n={n}: +1 configurations={cnt} min fall/rise={mr} (deg w={minr[5] if minr else None}) sufficient-condition-S failures={S_fail}', flush=True)
    if minr and float(minr[0]) < 1.05: print('   min example: w=%d deg=%d Q[m..m+2]=%s Qp[m-1..m+1]=%s par=%s' % (minr[1], minr[5], minr[3], minr[4], minr[2]))
    if deg2 and n <= 14: 
        for d in deg2[:3]: print('   deg2 example', d)
    res.append((n, cnt, minr and float(minr[0]), S_fail))
