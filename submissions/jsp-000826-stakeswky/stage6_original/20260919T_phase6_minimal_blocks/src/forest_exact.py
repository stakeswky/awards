"""Exact, independent algorithms for ordinary finite forests (stdlib only)."""
from functools import lru_cache
from itertools import combinations
from math import comb
import hashlib, json


def trim(p):
    p = list(p)
    while len(p)>1 and p[-1]==0: p.pop()
    return tuple(p)


def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    return trim(c)


def conv(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)


def packed_conv(a,b):
    """Independent nonnegative convolution using carry-free integer packing."""
    assert min(a)>=0 and min(b)>=0
    width=max(1,(sum(a)*sum(b)).bit_length()+1)
    z=sum(x<<(width*i) for i,x in enumerate(a))*sum(y<<(width*j) for j,y in enumerate(b))
    mask=(1<<width)-1
    ans=[]
    for _ in range(len(a)+len(b)-1):
        ans.append(z&mask); z>>=width
    assert z==0
    return trim(ans)


def shift(p,k=1): return (0,)*k+tuple(p)
def diff(p,k): return (p[k+1] if k+1<len(p) else 0)-(p[k] if 0<=k<len(p) else 0)
def modes(p):
    m=max(p); ix=[i for i,x in enumerate(p) if x==m]
    return (ix[0],ix[-1])

def valleys(p):
    """All negative-then-positive difference pairs, excluding artificial tails."""
    d=[diff(p,k) for k in range(len(p)-1)]
    return [(i,j) for i in range(len(d)) if d[i]<0 for j in range(i+1,len(d)) if d[j]>0]

def unimodal(p):
    fell=False
    for a,b in zip(p,p[1:]):
        if b<a: fell=True
        elif b>a and fell: return False
    return True

def logconcave(p):
    supp=[i for i,x in enumerate(p) if x]
    return (not supp or len(supp)==supp[-1]-supp[0]+1) and all(p[i]*p[i]>=p[i-1]*p[i+1] for i in range(1,len(p)-1))


def graph(n,edges):
    assert isinstance(n,int) and n>=0
    adj=[set() for _ in range(n)]; parent=list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for a,b in edges:
        assert isinstance(a,int) and isinstance(b,int) and 0<=a<n and 0<=b<n and a!=b
        assert b not in adj[a], 'duplicate edge'
        x,y=find(a),find(b)
        assert x!=y, 'cycle'
        parent[x]=y; adj[a].add(b); adj[b].add(a)
    return tuple(tuple(sorted(s)) for s in adj)

def edges_of(adj): return [(v,w) for v,ns in enumerate(adj) for w in ns if v<w]

def components(adj,allowed=None):
    todo=set(range(len(adj))) if allowed is None else set(allowed)
    out=[]
    while todo:
        v=min(todo); todo.remove(v); stack=[v]; block=[]
        while stack:
            u=stack.pop(); block.append(u)
            for w in adj[u]:
                if w in todo: todo.remove(w); stack.append(w)
        out.append(tuple(sorted(block)))
    return tuple(out)

def induced(adj,keep):
    keep=sorted(keep); mp={v:i for i,v in enumerate(keep)}
    return graph(len(keep),[(mp[v],mp[w]) for v in keep for w in adj[v] if w in mp and v<w])

def union(*graphs):
    n=0; ed=[]
    for a in graphs:
        ed += [(v+n,w+n) for v,w in edges_of(a)]; n+=len(a)
    return graph(n,ed)

def attach_path(adj,v,length):
    assert length>=1
    n=len(adj); ed=edges_of(adj)+[(v,n)]+[(n+i-1,n+i) for i in range(1,length)]
    return graph(n+length,ed)


def independence_dp(adj,allowed=None):
    """Algorithm A: root absent/present postorder DP."""
    allow=set(range(len(adj))) if allowed is None else set(allowed)
    def visit(v,parent):
        absent=(1,); present=(0,1)
        for w in adj[v]:
            if w!=parent and w in allow:
                a,b=visit(w,v)
                absent=conv(absent,add(a,b)); present=conv(present,a)
        return absent,present
    p=(1,)
    for block in components(adj,allow): p=conv(p,add(*visit(block[0],-1)))
    return p


def deletion_counter(adj):
    """Algorithm B: bitmask vertex deletion, component splitting, packed products.
    Does not use rooted occupancy messages or Algorithm A's convolution.
    """
    n=len(adj); neighbors=[sum(1<<w for w in ns) for ns in adj]
    @lru_cache(None)
    def count(mask):
        if mask==0: return (1,)
        first=mask&-mask; seen=0; front=first
        while front:
            seen|=front; nxt=0; t=front
            while t:
                bit=t&-t; t-=bit; nxt|=neighbors[bit.bit_length()-1]
            front=nxt&mask&~seen
        if seen!=mask: return packed_conv(count(seen),count(mask^seen))
        vertices=[v for v in range(n) if mask>>v&1]
        v=max(vertices,key=lambda w:(neighbors[w]&mask).bit_count())
        rest=mask&~(1<<v)
        return add(count(rest),shift(count(rest&~neighbors[v])))
    return count


def profile(adj,full=True):
    n=len(adj); blocks=components(adj)
    @lru_cache(None)
    def msg(v,parent):
        a=(1,); b=(0,1)
        for w in adj[v]:
            if w==parent: continue
            x,y=msg(w,v)
            a=conv(a,add(x,y)); b=conv(b,x)
        return a,b
    polys=[add(*msg(bl[0],-1)) for bl in blocks]
    allp=(1,)
    for p in polys: allp=conv(allp,p)
    assert allp==independence_dp(adj)
    assert allp[0]==1 and (n==0 or allp[1]==n)
    if len(allp)>2: assert allp[2]==comb(n,2)-len(edges_of(adj))
    records=[]
    for idx,bl in enumerate(blocks):
        ext=(1,)
        for j,p in enumerate(polys):
            if j!=idx: ext=conv(ext,p)
        for v in bl:
            a,b=msg(v,-1); a=conv(a,ext); b=conv(b,ext)
            assert add(a,b)==allp
            ma,mb=modes(a),modes(b)
            rec={'v':v,'A_modes':ma,'B_modes':mb,'local_gap':max(ma[0],mb[0])-min(ma[1],mb[1]),'unimodal_A':unimodal(a),'unimodal_B':unimodal(b)}
            if full: rec.update(A=a,B=b)
            records.append(rec)
    local=all(r['unimodal_A'] and r['unimodal_B'] for r in records)
    U=max((min(r['A_modes'][1],r['B_modes'][1]) for r in records),default=None)
    D=min((max(r['A_modes'][0],r['B_modes'][0]) for r in records),default=None)
    residual=list(combinations(range(max(0,U),min(D,len(allp)-1)),2)) if local and n else []
    return {'n':n,'edges':edges_of(adj),'component_orders':[len(b) for b in blocks],'P':allp,'unimodal':unimodal(allp),'log_concave':logconcave(allp),'valleys':valleys(allp),'LOCAL':local,'HEREDITARY':'UNKNOWN','U':U,'D':D,'residual_pairs':residual,'vertices':sorted(records,key=lambda r:r['v'])}


def terminal_spiders(adj):
    """Centers of degree >=3 with <=1 non-pendant-path neighbor branch."""
    records=[]
    for v,ns in enumerate(adj):
        if len(ns)<3: continue
        arms=[]; exterior=[]
        for w in ns:
            prev=v; cur=w; arm=[cur]
            while len(adj[cur])==2:
                nxt=next(t for t in adj[cur] if t!=prev)
                prev,cur=cur,nxt; arm.append(cur)
            if len(adj[cur])==1: arms.append(arm)
            else: exterior.append(w)
        if len(exterior)<=1 and len(arms)>=2:
            records.append({'center':v,'arms':arms,'exterior_neighbor':exterior[0] if exterior else None})
    return records


def canonical(adj):
    """Exact AHU encoding, independent of vertex labels; forest is a multiset."""
    @lru_cache(None)
    def rooted(v,parent): return '('+''.join(sorted(rooted(w,v) for w in adj[v] if w!=parent))+')'
    codes=[]
    for bl in components(adj):
        if len(bl)<=2: centers=bl
        else:
            deg={v:len(adj[v]) for v in bl}; leaves=[v for v in bl if deg[v]<=1]; left=len(bl)
            while left>2:
                left-=len(leaves); nxt=[]
                for v in leaves:
                    deg[v]=0
                    for w in adj[v]:
                        if deg[w]>0:
                            deg[w]-=1
                            if deg[w]==1: nxt.append(w)
                leaves=nxt
            centers=leaves
        codes.append(min(rooted(v,-1) for v in centers))
    return '|'.join(sorted(codes))


def parent_graph(par):
    assert par[0]==0 and all(1<=par[i]<=i for i in range(1,len(par)))
    return graph(len(par),[(i,p-1) for i,p in enumerate(par) if i])


def hub_tree(ks,core='star'):
    """Core vertices carry ki pendant length-two arms; optional central root."""
    m=len(ks)
    if core=='star':
        ed=[(0,i+1) for i in range(m)]; hubs=list(range(1,m+1)); n=m+1
    elif core=='path':
        ed=[(i,i+1) for i in range(m-1)]; hubs=list(range(m)); n=m
    else: raise ValueError(core)
    for h,k in zip(hubs,ks):
        for _ in range(k): ed += [(h,n),(n,n+1)]; n+=2
    return graph(n,ed)


def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
