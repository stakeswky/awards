import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from sync_cover import g, top
lv = [0, 1, 2, 2, 2, 1, 2, 2, 2]          # hubs(2,3): centre 0, hubs 1 and 5, leaves
par = L.parents_from_levels(lv); n = len(par); ch = L.children_of(par)
p = L.uni_poly(par, ch); a = len(p) - 1; k = top(a)
print('p =', p, ' alpha =', a, ' top =', k)
nbr = [set(ch[v]) | ({par[v]} if par[v] >= 0 else set()) for v in range(n)]
deg = [len(nbr[v]) for v in range(n)]
for v in range(n):
    A = L.uni_poly(par, ch, removed=frozenset([v])); C = L.uni_poly(par, ch, removed=frozenset(nbr[v] | {v}))
    aA, aC = len(A) - 1, len(C) - 1
    X = g(A, k-1)*g(C, k) + g(A, k+1)*g(C, k-2) - 2*g(A, k)*g(C, k-1)
    sA = g(A, k)**2 - g(A, k-1)*g(A, k+1); sC = g(C, k-1)**2 - g(C, k-2)*g(C, k)
    covA = (k <= top(aA)) or (k >= aA); covC = (k-1 == 0) or (k-1 <= top(aC)) or (k-1 >= aC)
    print('v=%d deg=%d alpha(F-v)=%d alpha(F-N[v])=%d  X_k=%d  sA(k)=%d sC(k-1)=%d  sync=%s coverA=%s coverC=%s' % (v, deg[v], aA, aC, X, sA, sC, X <= 0, covA, covC))
