"""Direction 1 experiments.
(1) Verify the exact U + K2 identity  s_F(k) = (1 + 2Q_{k-1}/Q_k) s_Q(k) + (4 + 2Q_{k+1}/Q_k) s_Q(k-1),  F = U + K2, Q = I(U).
(2) Ratio interlacing for a vertex v: A = I(F-v), B = x I(F-N[v]) (b_k = c_{k-1}).  Interlacing at k means
      b_{k+1} a_{k-1} <= a_k b_k   (I1)   and   a_{k+1} b_{k-1} <= a_k b_k   (I2),
    which gives X_k(v) = a_{k-1}b_{k+1} + a_{k+1}b_{k-1} - 2 a_k b_k <= 0.  Test on [1, top] and on [1, alpha-1],
    for nested v, for all trees of order n."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
def g(a, i): return a[i] if 0 <= i < len(a) else 0
def top(al): return (2*al + 1)//3

def identity_check(nmax):
    bad = 0; tot = 0
    for n in range(2, nmax + 1):
        for lv in L.free_trees(n):
            par = L.parents_from_levels(lv); Q = L.uni_poly(par, L.children_of(par))
            P = [0]*(len(Q) + 1)
            for i, q in enumerate(Q): P[i] += q; P[i+1] += 2*q
            for k in range(1, len(Q)):
                lhs = g(P, k)**2 - g(P, k-1)*g(P, k+1)
                sQk = g(Q, k)**2 - g(Q, k-1)*g(Q, k+1); sQk1 = g(Q, k-1)**2 - g(Q, k-2)*g(Q, k)
                rhs = (1 + Fr(2*g(Q, k-1), g(Q, k)))*sQk + (4 + Fr(2*g(Q, k+1), g(Q, k)))*sQk1
                tot += 1; bad += (lhs != rhs)
    return tot, bad

def job(lv):
    par = L.parents_from_levels(lv); n = len(par); ch = L.children_of(par)
    p = L.uni_poly(par, ch); a = len(p) - 1; T = min(top(a), a - 1)
    nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
    res = {'nested': 0, 'top_all': 0, 'full_all': 0, 'X_top_nonpos': 0}
    any_top = any_full = any_x = False
    for v in range(n):
        A = L.uni_poly(par, ch, removed=frozenset([v])); C = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
        if not (len(A) - 1 == a and len(C) - 1 == a - 1): continue
        res['nested'] += 1
        B = [0] + C
        ok_top = all(g(B, k+1)*g(A, k-1) <= g(A, k)*g(B, k) and g(A, k+1)*g(B, k-1) <= g(A, k)*g(B, k) for k in range(1, T + 1))
        ok_full = all(g(B, k+1)*g(A, k-1) <= g(A, k)*g(B, k) and g(A, k+1)*g(B, k-1) <= g(A, k)*g(B, k) for k in range(1, a))
        ok_x = all(g(A, k-1)*g(B, k+1) + g(A, k+1)*g(B, k-1) - 2*g(A, k)*g(B, k) <= 0 for k in range(1, T + 1))
        any_top |= ok_top; any_full |= ok_full; any_x |= ok_x
    return res['nested'] > 0, any_top, any_full, any_x, (lv if (res['nested'] > 0 and not any_top) else None)

if __name__ == '__main__':
    tot, bad = identity_check(14)
    print('(1) U+K2 identity checked on all trees U with n <= 14: %d (U,k) pairs, mismatches %d' % (tot, bad), flush=True)
    for n in range(5, int(sys.argv[1]) + 1):
        with Pool(3) as pool: res = list(pool.imap_unordered(job, [tuple(lv) for lv in L.free_trees(n)], chunksize=100))
        withn = [r for r in res if r[0]]
        print('(2) n=%d: trees with a nested vertex %d | some nested v interlaces on [1,top]: %d | on [1,alpha-1]: %d | X<=0 on [1,top]: %d | first non-interlacing: %s' % (
            n, len(withn), sum(r[1] for r in withn), sum(r[2] for r in withn), sum(r[3] for r in withn), next((r[4] for r in withn if r[4]), None)), flush=True)
