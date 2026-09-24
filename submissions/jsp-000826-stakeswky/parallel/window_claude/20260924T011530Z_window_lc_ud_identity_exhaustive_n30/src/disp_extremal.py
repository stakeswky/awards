import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from ext_identity import size_free_poly, moments
from fractions import Fraction as Fr
def deg_seq(par):
    n=len(par); d=[0]*n
    for v,p in enumerate(par):
        if p>=0: d[v]+=1; d[p]+=1
    return sorted(d, reverse=True)
for n in range(10, int(sys.argv[1])+1):
    best = []
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv); G = size_free_poly(par)
        p = [sum(v for (s,f),v in G.items() if s==k) for k in range(n+1)]
        while p and p[-1]==0: p.pop()
        a=len(p)-1; lo=(n+3)//4; hi=(2*a+1)//3
        for k in range(max(lo,1), min(hi,a-1)+1):
            c,mu,var = moments(G,k-1)
            if mu: best.append((float(var/mu), k, a, deg_seq(par)[:5], list(lv)))
    best.sort(reverse=True)
    print('n=%d top window Var/mu:' % n)
    for b in best[:3]: print('   %.4f k=%d alpha=%d top degrees=%s levels=%s' % b)
