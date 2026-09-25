"""Round-5 independent vertex-deletion count with balanced component products.
No import of the rooted-DP or graph-construction implementations.
Each recursive state is an actual labelled vertex subset. Polynomial products
use carry-free byte-limb packing (not the DP's nested integer convolution).
"""
from functools import lru_cache
from heapq import heappush,heappop

def multiply(a,b):
    if min(a)<0 or min(b)<0:raise ValueError('nonnegative coefficients required')
    if a==[1] or a==(1,):return list(b)
    if b==[1] or b==(1,):return list(a)
    width=max(1,((sum(a)*sum(b)).bit_length()+7)//8)
    u=int.from_bytes(b''.join(x.to_bytes(width,'little') for x in a),'little')
    v=int.from_bytes(b''.join(x.to_bytes(width,'little') for x in b),'little')
    # Every coefficient is strictly below 256**width, so no inter-limb carry.
    raw=(u*v).to_bytes(width*(len(a)+len(b)-1),'little')
    return [int.from_bytes(raw[i:i+width],'little') for i in range(0,len(raw),width)]

def product(ps):
    heap=[];serial=0
    for p in ps:heappush(heap,(len(p),serial,p));serial+=1
    if not heap:return [1]
    while len(heap)>1:
        _,_,a=heappop(heap);_,_,b=heappop(heap);c=multiply(a,b)
        heappush(heap,(len(c),serial,c));serial+=1
    return list(heap[0][2])

def deletion(n,edges):
    adj=[0]*n;seen=set()
    for u,v in edges:
        if not (0<=u<n and 0<=v<n) or u==v:raise ValueError('invalid edge')
        e=tuple(sorted((u,v)))
        if e in seen:raise ValueError('duplicate edge')
        seen.add(e);adj[u]|=1<<v;adj[v]|=1<<u
    @lru_cache(None)
    def rec(mask):
        if mask==0:return (1,)
        if mask&(mask-1)==0:return (1,1)
        unseen=mask;comps=[]
        while unseen:
            start=unseen&-unseen;visited=start;front=start
            while front:
                bit=front&-front;front-=bit;v=bit.bit_length()-1
                new=adj[v]&mask&~visited;visited|=new;front|=new
            unseen&=~visited;comps.append(visited)
        if len(comps)>1:return tuple(product(rec(c) for c in comps))
        bits=mask;vertices=[]
        while bits:
            bit=bits&-bits;bits-=bit;vertices.append(bit.bit_length()-1)
        v=max(vertices,key=lambda v:((adj[v]&mask).bit_count(),-v))
        a=rec(mask&~(1<<v));b=rec(mask&~((1<<v)|adj[v]))
        ans=[0]*max(len(a),len(b)+1)
        for j,c in enumerate(a):ans[j]+=c
        for j,c in enumerate(b):ans[j+1]+=c
        return tuple(ans)
    p=list(rec((1<<n)-1))
    return p,rec.cache_info()._asdict()
