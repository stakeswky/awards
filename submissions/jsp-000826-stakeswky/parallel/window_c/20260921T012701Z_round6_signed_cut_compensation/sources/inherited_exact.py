"""Exact, self-contained reconstruction; no inherited code bytes are claimed."""
from fractions import Fraction as Q
from math import comb
from itertools import combinations

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    while len(c)>1 and c[-1]==0:c.pop()
    return c

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):c[i+j]+=x*y
    return c

def prod(ps):
    a=[1]
    for p in ps:a=mul(a,p)
    return a

def binom(n,c=1):return [comb(n,j)*c**j for j in range(n+1)]

def bush(arms,leaves=None):
    leaves=[0]*len(arms) if leaves is None else leaves
    assert len(arms)==len(leaves) and all(a>=0 for a in arms+leaves)
    edges=[];v=1+len(arms)
    for j,(a,l) in enumerate(zip(arms,leaves),1):
        edges.append((0,j))
        for _ in range(l):edges.append((j,v));v+=1
        for _ in range(a):edges.extend(((j,v),(v,v+1)));v+=2
    return v,sorted(edges)

def bush_formula(arms,leaves=None):
    leaves=[0]*len(arms) if leaves is None else leaves
    # Hub states enumerated in each factor; central-root-selected term is separate.
    a=prod([add(mul(binom(s,2),binom(l)),[0]+binom(s)) for s,l in zip(arms,leaves)])
    return add(a,[0]+mul(binom(sum(arms),2),binom(sum(leaves))))

def graph_dp(n,edges):
    adj=[[] for _ in range(n)]
    for u,v in edges:
        if not 0<=u<n or not 0<=v<n or u==v:raise ValueError('invalid edge')
        adj[u].append(v);adj[v].append(u)
    if len(set(tuple(sorted(e)) for e in edges))!=len(edges):raise ValueError('duplicate edge')
    seen=set(); roots=[]; order=[];par={}
    for r in range(n):
        if r in seen:continue
        roots.append(r);par[r]=-1;seen.add(r);stack=[r]
        while stack:
            v=stack.pop();order.append(v)
            for u in adj[v]:
                if u==par[v]:continue
                if u in seen:raise ValueError('cycle')
                seen.add(u);par[u]=v;stack.append(u)
    absent={};present={}
    for v in reversed(order):
        a=[1];b=[0,1]
        for u in adj[v]:
            if par.get(u)==v:
                a=mul(a,add(absent[u],present[u]));b=mul(b,absent[u])
        absent[v]=a;present[v]=b
    return prod([add(absent[r],present[r]) for r in roots])

def union(gs):
    n=0;e=[]
    for m,f in gs:e.extend((u+n,v+n) for u,v in f);n+=m
    return n,e

def lc_bad(p):return [j for j in range(1,len(p)-1) if p[j]**2<p[j-1]*p[j+1]]

def valleys(p):
    first=None;out=[]
    for j in range(len(p)-1):
        if p[j+1]<p[j] and first is None:first=j
        elif p[j+1]>p[j] and first is not None:out.append((first,j))
    return out

def mu(p,k):
    if not 0<=k<len(p):raise ValueError('mu outside positive support')
    return Q((k+1)*p[k+1],p[k]) if k+1<len(p) else Q(0)

def sig(p,k):
    a=mu(p,k)
    return a*(1+a-mu(p,k+1)) if k+1<len(p) else Q(0)

def direct_G(p,k):
    def at(j):return p[j] if j<len(p) else 0
    return Q((k+1)*(k+2)*(at(k+1)-at(k+2)),p[k])

def split(a,b,k,full=True):
    p=mul(a,b);lo=max(0,k-len(b)+1);hi=min(k,len(a)-1)
    inds=list(range(lo,hi+1));w=[Q(a[i]*b[k-i],p[k]) for i in inds]
    mx=[mu(a,i) for i in inds];my=[mu(b,k-i) for i in inds]
    m=[x+y for x,y in zip(mx,my)]
    local=[sig(a,i)+sig(b,k-i) for i in inds]
    mf=mu(p,k);d=k+1-mf
    V=sum((z*(v-mf)**2 for z,v in zip(w,m)),Q(0))
    R=sum((z*s for z,s in zip(w,local)),Q(0))+mf*d
    assert sum(w)==1 and sum((z*x for z,x in zip(w,m)),Q(0))==mf
    assert R-V==direct_G(p,k)
    if not full:return R,V
    ds=[m[i+1]-m[i] for i in range(len(m)-1)]
    cum=[];s=Q(0)
    for z in w[:-1]:s+=z;cum.append(s)
    # Linear-time exact covariance-kernel sums, with no floating-point screening.
    Vkernel=Q(0);Vabs=Q(0);pref=Q(0);pabs=Q(0)
    for t,(dt,ft) in enumerate(zip(ds,cum)):
        Vkernel+=dt*dt*ft*(1-ft)+2*dt*(1-ft)*pref
        Vabs+=dt*dt*ft*(1-ft)+2*abs(dt)*(1-ft)*pabs
        pref+=dt*ft;pabs+=abs(dt)*ft
    assert Vkernel==V and Vabs>=V
    Ea=sum((z*i for z,i in zip(w,inds)),Q(0));prefa=Q(0);U=Q(0)
    for t in range(len(ds)):
        prefa+=w[t]*inds[t]
        U+=(cum[t]*Ea-prefa)*ds[t]**2
    assert U>=V
    neg=sum((z for z,i in zip(w,inds) if sig(a,i)<0 or sig(b,k-i)<0),Q(0))
    neg_signed=sum((z*min(sig(a,i),0)+z*min(sig(b,k-i),0) for z,i in zip(w,inds)),Q(0))
    return dict(k=k,lo=lo,hi=hi,mu=mf,d=d,e=mu(p,k+1)-mf-1 if k+1<len(p) else None,
                V=V,V_abs=Vabs,U_var=U,R_budget=R,G=R-V,negative_mass=neg,negative_budget=neg_signed,
                positive_delta=sum(x>0 for x in ds),negative_delta=sum(x<0 for x in ds),
                cancellation_error=Vabs-V)
