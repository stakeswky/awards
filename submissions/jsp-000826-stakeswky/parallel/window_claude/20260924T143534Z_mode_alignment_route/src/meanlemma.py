"""First-order comparison of the mean number of addable vertices m_k = (k+1) p_{k+1}/p_k
between a forest G and G - u, over all trees n <= NMAX and all vertices u, for k in the LC window
[ceil(n/4), ceil((2a-1)/3)] of G (and also over all k). Also the two-sided curvature:
max over the window of n(1 - p_{k-1}p_{k+1}/p_k^2)."""
import sys
from fractions import Fraction as Fr
from modelib import *
from ma_forests import free_trees   # noqa (import triggers nothing: guarded below)
NMAX = int(sys.argv[1])
stats = []
for n in range(6, NMAX + 1):
    up_win = Fr(-100); dn_win = Fr(-100); up_all = Fr(-100); dn_all = Fr(-100); curv_max = Fr(0); curv_min = Fr(100)
    up_leaf = Fr(-100); dn_leaf = Fr(-100)
    for lv in free_trees(n):
        par = parents_from_levels(lv); nb = neighbours(par)
        p = indep_poly_del(par); a = len(p) - 1
        q, top = (n + 3) // 4, (2 * a + 1) // 3
        m = [Fr((k + 1) * p[k + 1], p[k]) for k in range(a)]
        for k in range(max(q, 1), min(top, a - 1) + 1):
            c = n * (1 - Fr(p[k - 1] * p[k + 1], p[k] * p[k]))
            curv_max = max(curv_max, c); curv_min = min(curv_min, c)
        for u in range(n):
            pu = indep_poly_del(par, frozenset([u])); au = len(pu) - 1
            mu = [Fr((k + 1) * pu[k + 1], pu[k]) for k in range(au)]
            for k in range(min(a, au)):
                d = mu[k] - m[k]          # m_k(G-u) - m_k(G)
                up_all = max(up_all, d); dn_all = max(dn_all, -d)
                if q <= k <= top:
                    up_win = max(up_win, d); dn_win = max(dn_win, -d)
                    if len(nb[u]) == 1: up_leaf = max(up_leaf, d); dn_leaf = max(dn_leaf, -d)
    print(f'n={n}: window: max[m_k(G-u)-m_k(G)]={float(up_win):.4f} max[m_k(G)-m_k(G-u)]={float(dn_win):.4f} | leaves: {float(up_leaf):.4f} {float(dn_leaf):.4f} | all k: {float(up_all):.4f} {float(dn_all):.4f} | n*LCmargin window min={float(curv_min):.3f} max={float(curv_max):.3f}', flush=True)
