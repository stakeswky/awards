"""Exact sanity checks of Theorem 1 and of the (S1-lower) configuration, over all (H, w), H a tree n <= NMAX.
 T1(c): if q1 = p2+1 =: m+1 then [G nonincreasing on [m+1, inf)] <=> [Q_m + Q'_m >= Q_{m+2} + Q'_{m+1}],
        and G is always nonincreasing on [m+2, inf).
 T1(a): if q2 >= p1-1 then G nondecreasing on [0, p1].   T1(b): if q1 <= p2 then G nonincreasing on [p2+1, inf).
 (S1-lower) configuration: q'1 = q2+1 (Q' = I(H-N[w]) starts its plateau one step after Q's ends);
        there P nonincreasing from q2+1 <=> Q_{q2+1}-Q_{q2+2} >= Q'_{q2+1}-Q'_{q2}; record min ratio.
 Also count how often q'1 >= q2+2 (would need more)."""
import sys, collections
from fractions import Fraction as Fr
from modelib import *
from ma_forests import free_trees
NMAX = int(sys.argv[1])
c = collections.Counter(); minratio = None; minratio3 = None
def noninc(s, a): return all(s[k] >= s[k + 1] for k in range(max(a, 0), len(s) - 1))
def nondec(s, b): return all(s[k] <= s[k + 1] for k in range(0, min(b, len(s) - 1)))
for n in range(4, NMAX + 1):
    for lv in free_trees(n):
        par = parents_from_levels(lv); nb = neighbours(par)
        P = indep_poly_del(par); p1, p2, _ = mode_set(P)
        for w in range(n):
            Q = indep_poly_del(par, frozenset([w])); q1, q2, _ = mode_set(Q)
            Qp = indep_poly_del(par, frozenset(nb[w] | {w})); r1, r2, _ = mode_set(Qp)
            g = lambda s, k: s[k] if 0 <= k < len(s) else 0
            G = [g(P, k) + g(Q, k - 1) for k in range(max(len(P), len(Q) + 1))]
            c['pairs'] += 1
            if q2 >= p1 - 1: c['a_hyp'] += 1; c['a_ok'] += nondec(G, p1)
            if q1 <= p2: c['b_hyp'] += 1; c['b_ok'] += noninc(G, p2 + 1)
            if q1 == p2 + 1:
                m = p2; c['c_hyp'] += 1
                lhs = noninc(G, m + 1); rhs = (Q[m] + g(Qp, m) >= g(Q, m + 2) + g(Qp, m + 1))
                c['c_iff_ok'] += (lhs == rhs); c['c_tail_ok'] += noninc(G, m + 2)
            if q1 >= p2 + 2: c['q1_ge_p2+2'] += 1
            # (S1-lower) configuration
            if r1 == q2 + 1:
                c['s1low_config'] += 1
                fall = Q[q2] - g(Q, q2 + 1) if False else g(Q, q2 + 1) - g(Q, q2 + 2); rise = g(Qp, q2 + 1) - g(Qp, q2)
                ok = (fall >= rise); c['s1low_ineq_ok'] += ok
                c['s1low_P_noninc_from_q2+1'] += noninc(P, q2 + 1)
                if rise > 0:
                    r = Fr(fall, rise)
                    if minratio is None or r < minratio[0]: minratio = (r, n, w, len(nb[w]))
            if r1 >= q2 + 2: c['r1_ge_q2+2'] += 1
            # (S1-upper) configuration: r2 <= q1-2; need Q rising at k >= Q' falling at k-1 for k in [r2+1, q1-1]
            if r2 <= q1 - 2:
                c['s1up_config'] += 1
                ok = True
                for k in range(r2 + 1, q1 - 1):   # (S1-upper) needs P nondecreasing on [0, q1-2] only
                    riseQ = g(Q, k + 1) - g(Q, k); fallQp = g(Qp, k - 1) - g(Qp, k)
                    if riseQ < fallQp: ok = False
                    if fallQp > 0:
                        r = Fr(riseQ, fallQp)
                        if minratio3 is None or r < minratio3[0]: minratio3 = (r, n, w, len(nb[w]), k - r2, q1 - k)
                c['s1up_ineq_ok'] += ok; c['s1up_P_nondec_to_q1-2'] += nondec(P, q1 - 2)
print(dict(c)); print('(S1-lower) configuration: min fall(Q at q2+1)/rise(Qp at q2) =', minratio)
print('(S1-upper) configuration: min rise(Q at k)/fall(Qp at k-1) over k in [r2+1,q1-1] =', minratio3, '(ratio, n, w, deg w, k-r2, q1-k)')
