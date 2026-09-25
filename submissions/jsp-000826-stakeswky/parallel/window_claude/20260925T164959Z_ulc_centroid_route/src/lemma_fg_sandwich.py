"""Candidate (sandwich variant): F, G ULC(infinity), F_0 = G_0 = 1, G <= F <= (1+x)^d G coefficientwise
  with d = F_1 - G_1 a positive integer, d <= deg F (as for centroid data prod f_i, prod g_i)
  ==> F + xG unimodal.   Adversarial hill-climbing on log-increments of k! F_k and k! G_k."""
import random, math, sys
seed = int(sys.argv[1]); random.seed(seed)
def seq(inc):
    s=[0.0]
    for x in sorted(inc, reverse=True): s.append(s[-1]+x)
    return [math.exp(v - math.lgamma(k+1)) for k, v in enumerate(s)]
def build(P):
    fi, gi, D = P
    G = seq(gi)
    if len(G) < 2: return None
    F = seq(fi)
    if len(F) < 2: return None
    # force F_1 = G_1 + D by scaling F's higher coefficients: F_k -> F_k * t^k keeps ULC
    t = (G[1] + D) / F[1]
    F = [F[k] * t ** k for k in range(len(F))]
    if len(G) > len(F) or any(G[k] > F[k] for k in range(len(G))): return None
    # d = F_1 - G_1 must be a positive integer <= deg F: rescale nothing, just snap by rejecting
    if len(F) < 2: return None
    d = F[1] - (G[1] if len(G) > 1 else 0.0)
    D = round(d)
    if D < 1 or abs(d - D) > 1e-9 * max(1.0, F[1]) or D > len(F) - 1: return None
    U = [0.0] * (len(G) + D)
    for i, x in enumerate(G):
        for j in range(D + 1): U[i + j] += x * math.comb(D, j)
    if len(F) > len(U) or any(F[k] > U[k] * (1 + 1e-12) for k in range(len(F))): return None
    return [(F[k] if k < len(F) else 0.0) + (G[k-1] if 1 <= k <= len(G) else 0.0) for k in range(max(len(F), len(G)+1))]
def score(p):
    n=len(p); best=-1e9; pre=[0]*n; m=0
    for i in range(n): m=max(m,p[i]); pre[i]=m
    suf=[0]*n; m=0
    for i in range(n-1,-1,-1): m=max(m,p[i]); suf[i]=m
    for j in range(1,n-1): best=max(best,(min(pre[j-1],suf[j+1])-p[j])/p[j])
    return best
overall=(-1e9,None)
for restart in range(300):
    LF=random.randint(2,30); LG=random.randint(1,LF)
    P=([random.uniform(-1,6) for _ in range(LF)],[random.uniform(-1,6) for _ in range(LG)], random.randint(1, 12))
    p=build(P)
    if p is None: continue
    cur=score(p); T=0.05
    for step in range(3000):
        Q=[list(P[0]),list(P[1]),P[2]]
        if random.random() < 0.1: Q[2] = max(1, Q[2] + random.choice([-1, 1]))
        w=random.randrange(2); arr=Q[w]; r=random.random()
        if r<0.75 and arr: k=random.randrange(len(arr)); arr[k]+=random.gauss(0,0.3)
        elif r<0.87 and len(arr)<35: arr.append(random.uniform(-1,5))
        elif len(arr)>1: arr.pop(random.randrange(len(arr)))
        q=build(Q)
        if q is None: continue
        s=score(q)
        if s>cur or random.random()<math.exp((s-cur)/T): P,cur=Q,s
        T*=0.999
        if cur>overall[0]: overall=(cur,(list(P[0]),list(P[1]),P[2]))
    if overall[0]>0: break
print('seed',seed,'best',overall[0])
if overall[0] > -0.02:
    print(' d', overall[1][2]); print(' p',[round(x,4) for x in build(overall[1])])
