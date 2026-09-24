import sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from ext_identity import size_free_poly, moments

def window_stats(par):
    n = len(par); G = size_free_poly(par)
    p = [sum(v for (s, f), v in G.items() if s == k) for k in range(n + 1)]
    while p and p[-1] == 0: p.pop()
    a = len(p) - 1; lo = (n + 3)//4; hi = (2*a + 1)//3
    out = []
    for k in range(max(lo, 1), min(hi, a - 1) + 1):
        cnt, mu, var = moments(G, k - 1)
        if not mu: continue
        Q = var / mu
        mu_k = Fr((k + 1)*p[k + 1], p[k])
        D = mu + var/mu - 1 - mu_k            # from the identity
        R = var / (mu * (1 + D + mu / k))      # LC at k  <=>  R <= 1
        out.append((k, Q, R, D, mu))
    return out

if __name__ == '__main__':
    NMAX = int(sys.argv[1])
    for n in range(8, NMAX + 1):
        pos = under = 0; maxQ = Fr(0); maxR = Fr(0); argQ = argR = None; minD = None
        for lv in L.free_trees(n):
            par = L.parents_from_levels(lv)
            for (k, Q, R, D, mu) in window_stats(par):
                pos += 1; under += (Q <= 1)
                if Q > maxQ: maxQ, argQ = Q, (list(lv), k)
                if R > maxR: maxR, argR = R, (list(lv), k)
                minD = D if minD is None else min(minD, D)
        print('n=%d window positions=%d  under-dispersed (Var<=mu)=%d (%.1f%%)  max Var/mu=%.4f  max R(LC iff <=1)=%.4f  min D=%s  argmax R=%s' % (
            n, pos, under, 100.0*under/max(pos, 1), float(maxQ), float(maxR), None if minD is None else round(float(minD), 3), argR), flush=True)
