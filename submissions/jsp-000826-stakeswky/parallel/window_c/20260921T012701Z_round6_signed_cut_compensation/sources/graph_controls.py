"""Actual graph constructions and premise checks; no symmetry quotient implied."""
from inherited_exact import bush, graph_dp, lc_bad, valleys
from signed_cut import convolution

def invariants(g, coeffs):
    n,edges=g
    adj=[[] for _ in range(n)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    seen=set();sizes=[]
    for v in range(n):
        if v in seen:continue
        stack=[v];seen.add(v);sz=0
        while stack:
            u=stack.pop();sz+=1
            for w in adj[u]:
                if w not in seen:seen.add(w);stack.append(w)
        sizes.append(sz)
    alpha=len(coeffs)-1;M=max(sizes,default=0)
    h=M*(n-1)//(4*M-2)+1 if M else 0
    beta=(alpha*(n-1)+(n+alpha)-1)//(n+alpha) if n+alpha else 0
    return dict(n=n,M_max=M,alpha=alpha,h=h,beta=beta,component_orders=sorted(sizes))

def history(p,k):
    if not 0<=k<len(p)-1 or p[k+1]>p[k]:return None
    i=k
    while i>=0 and p[i+1]==p[i]:i-=1
    if i<0 or p[i+1]>p[i]:return None
    # First strict decline since the last rise, not just the most recent decline.
    while i>0 and p[i]<=p[i-1]:i-=1
    while i<=k and p[i+1]==p[i]:i+=1
    return i if i<=k else None

def c5_windows(a,b,p=None):
    """Exhaust ALL admissible global K,T (C5-W); return count and first gate."""
    p=convolution(a,b) if p is None else p
    degree=len(p)-1;last_prefix=0
    while last_prefix<degree and p[last_prefix+1]>=p[last_prefix]:last_prefix+=1
    first_suffix=degree
    while first_suffix>0 and p[first_suffix-1]>=p[first_suffix]:first_suffix-=1
    bad=lc_bad(a);qual=0;first=None;checked=0
    for K in range(last_prefix+1):
        for T in range(max(K,first_suffix),degree+1):
            checked+=1;L=max(0,K-len(b)+1);U=min(len(a)-1,T)
            if all(not L<j<U for j in bad):
                qual+=1
                if first is None:first=dict(K=K,T=T,L=L,U=U)
    return dict(checked=checked,qualifying=qual,first=first,last_prefix=last_prefix,
                first_suffix=first_suffix,A_bad=bad)

def graft(g, rng):
    n,edges=g;edges=list(map(tuple,edges));q=rng.randrange(len(edges));u,v=edges.pop(q)
    adj=[[] for _ in range(n)]
    for x,y in edges:adj[x].append(y);adj[y].append(x)
    side={u};stack=[u]
    while stack:
        x=stack.pop()
        for y in adj[x]:
            if y not in side:side.add(y);stack.append(y)
    # Retain the cut endpoint on one side; choose an actual attachment on the other.
    if rng.randrange(2):
        left=u;right=rng.choice(sorted(set(range(n))-side))
    else:
        left=rng.choice(sorted(side));right=v
    edges.append(tuple(sorted((left,right))))
    return n,sorted(tuple(sorted(e)) for e in edges)

def graph_record(g):return dict(n=g[0],edges=[list(e) for e in g[1]])
