"""ULC variant (g_i, h_i, f_i ultra-log-concave). Adversarial hill-climbing against candidate lemma L:
  (g_i, h_i) positive LC, constant term 1, h_i <= g_i, f_i = g_i + x h_i LC  ==>  prod f_i + x prod g_i unimodal.
Parametrise each g_i, h_i by log-increments (sorted nonincreasing => LC); maximise
  score(p) = max_j (min(max p[:j], max p[j+1:]) - p_j) / p_j   (> 0 means a dip),
using a smooth surrogate when there is no dip: max_j (min(p_{j-1}, p_{j+1}) - p_j)/p_j."""
import random, math, sys
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(seed)
def conv(a, b):
    o = [0.0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): o[i+j] += x*y
    return o
def seq(inc):
    # ULC(infinity) sequence: q_k = p_k k! is LC (sorted increments), p_k = q_k / k!
    s=[0.0]
    for x in sorted(inc, reverse=True): s.append(s[-1]+x)
    return [math.exp(v - math.lgamma(k+1)) for k, v in enumerate(s)]
def lc(a): return all(a[i]*a[i] >= (1+1.0/i)*a[i-1]*a[i+1]*(1-1e-12) for i in range(1, len(a)-1))  # ULC
def build(params):
    F=[1.0]; B=[1.0]
    for gi, hi in params:
        g = seq(gi); h = seq(hi)
        if len(h) > len(g) or any(h[k] > g[k] for k in range(len(h))): return None
        f = [(g[k] if k < len(g) else 0.0) + (h[k-1] if 1 <= k <= len(h) else 0.0) for k in range(max(len(g), len(h)+1))]
        if not lc(f): return None
        F = conv(F, f); B = conv(B, g)
    return [(F[k] if k < len(F) else 0.0) + (B[k-1] if 1 <= k <= len(B) else 0.0) for k in range(max(len(F), len(B)+1))]
def score(p):
    n=len(p); best=-1e9
    pre=[0]*n; m=0
    for i in range(n): m=max(m,p[i]); pre[i]=m
    suf=[0]*n; m=0
    for i in range(n-1,-1,-1): m=max(m,p[i]); suf[i]=m
    for j in range(1,n-1):
        best=max(best,(min(pre[j-1],suf[j+1])-p[j])/p[j])
    return best
overall=(-1e9,None)
for restart in range(60):
    d = random.randint(2, 8)
    params=[]
    for _ in range(d):
        Lg=random.randint(0,6); Lh=random.randint(0,Lg)
        params.append(([random.uniform(-1,5) for _ in range(Lg)], [random.uniform(-1,4) for _ in range(Lh)]))
    p=build(params)
    if p is None: continue
    cur=score(p); T=0.05
    for step in range(4000):
        newp=[(list(a),list(b)) for a,b in params]
        i=random.randrange(len(newp)); which=random.randrange(2)
        arr=newp[i][which]
        r=random.random()
        if r<0.7 and arr: k=random.randrange(len(arr)); arr[k]+=random.gauss(0,0.3)
        elif r<0.85 and len(arr)<8: arr.append(random.uniform(-2,3))
        elif arr: arr.pop(random.randrange(len(arr)))
        q=build(newp)
        if q is None: continue
        s=score(q)
        if s>cur or random.random()<math.exp((s-cur)/T):
            params, cur = newp, s
        T*=0.999
        if cur>overall[0]: overall=(cur,[(list(a),list(b)) for a,b in params])
    if overall[0] > 0: break
print('seed',seed,'best score',overall[0])
if overall[1]:
    for gi,hi in overall[1]:
        print(' g',[round(x,3) for x in seq(gi)],' h',[round(x,3) for x in seq(hi)])
    print(' p',[round(x,3) for x in build(overall[1])])
