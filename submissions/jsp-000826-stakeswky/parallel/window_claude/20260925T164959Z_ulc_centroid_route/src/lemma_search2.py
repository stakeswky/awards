"""Candidate one-step lemma: for branch pairs with g_i, h_i LC (positive, no internal zeros, constant
term 1), h_i <= g_i coefficientwise, f_i = g_i + x h_i LC, is p = prod f_i + x prod g_i unimodal?
Random search (branch data random, not from trees)."""
import random, math
random.seed(11)
def lc(a): return all(x > 0 for x in a) and all(a[i]*a[i] >= a[i-1]*a[i+1]*(1-1e-12) for i in range(1, len(a)-1))
def conv(a, b):
    o = [0.0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): o[i+j] += x*y
    return o
def rand_lc(L, spread=3.0):
    inc = sorted([random.uniform(-spread, spread) for _ in range(L-1)], reverse=True)
    s=[0.0]
    for x in inc: s.append(s[-1]+x)
    return [math.exp(v) for v in s]
def dip(p):
    n=len(p); pre=[0]*n; m=0
    for i in range(n): m=max(m,p[i]); pre[i]=m
    suf=[0]*n; m=0
    for i in range(n-1,-1,-1): m=max(m,p[i]); suf[i]=m
    return max([ (min(pre[j-1],suf[j+1])-p[j])/p[j] for j in range(1,n-1) if min(pre[j-1],suf[j+1])>p[j]] + [0.0])
def rand_branch():
    while True:
        Lg = random.randint(1, 6); Lh = random.randint(1, Lg)
        g = rand_lc(Lg) if Lg > 1 else [1.0]
        h = rand_lc(Lh) if Lh > 1 else [1.0]
        if any(h[k] > g[k] for k in range(Lh)): continue
        f = [ (g[k] if k < Lg else 0.0) + (h[k-1] if 1 <= k <= Lh else 0.0) for k in range(max(Lg, Lh+1))]
        if lc(f): return f, g
best=(0,None); tried=0
for it in range(100000):
    d = random.randint(1, 10)
    br = [rand_branch() for _ in range(d)]
    F=[1.0]; B=[1.0]
    for f,g in br: F=conv(F,f); B=conv(B,g)
    p=[(F[k] if k<len(F) else 0.0)+(B[k-1] if 1<=k<=len(B) else 0.0) for k in range(max(len(F),len(B)+1))]
    tried+=1
    s=dip(p)
    if s>best[0]: best=(s,(br,F,B,p))
print('tried',tried,'max relative dip',best[0])
if best[1]:
    br,F,B,p=best[1]
    for f,g in br: print(' f',[round(x,3) for x in f],' g',[round(x,3) for x in g])
    print('p',[round(x,3) for x in p])
