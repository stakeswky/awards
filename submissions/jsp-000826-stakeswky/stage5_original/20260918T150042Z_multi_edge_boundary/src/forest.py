"""Exact unweighted-forest counters. Standard library only.

Algorithm 1: directed rooted messages, Kronecker packed coefficients.
Algorithm 2: vertex deletion on active masks, schoolbook convolution.
Algorithm 3: rooted DP counting vertex subsets with zero or one induced edge.
No floating-point arithmetic is used to count or decide unimodality.
"""
from functools import lru_cache
from itertools import zip_longest


def validate(n, edges):
    if not isinstance(n, int) or n < 0:
        raise ValueError('invalid order')
    adj = [set() for _ in range(n)]
    parent = list(range(n))
    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for e in edges:
        if len(e) != 2:
            raise ValueError('edge must have two endpoints')
        u, v = e
        if not all(isinstance(w, int) and 0 <= w < n for w in (u, v)) or u == v:
            raise ValueError('invalid endpoint or loop')
        if v in adj[u]:
            raise ValueError('parallel/repeated edge')
        a, b = root(u), root(v)
        if a == b:
            raise ValueError('cycle')
        parent[a] = b
        adj[u].add(v); adj[v].add(u)
    return tuple(tuple(sorted(ns)) for ns in adj)


def add(a, b):
    return tuple(x+y for x,y in zip_longest(a,b,fillvalue=0))


def mul(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[i+j] += x*y
    while len(c)>1 and c[-1]==0:
        c.pop()
    return tuple(c)


def pad(a, n):
    if len(a)>n+1 and any(a[n+1:]):
        raise ValueError('nonzero coefficient beyond order')
    return tuple(a[:n+1])+(0,)*max(0,n+1-len(a))


def delta(a, k):
    at = lambda j: a[j] if 0 <= j < len(a) else 0
    return at(k+1)-at(k)


def unimodal(a):
    down = False
    for x, y in zip(a,a[1:]):
        if y < x:
            down = True
        elif down and y > x:
            return False
    return True


def modes(a):
    m = max(a)
    if m <= 0 or not unimodal(a):
        raise ValueError('mode interval requires nonzero unimodal sequence')
    ids = [i for i,x in enumerate(a) if x==m]
    return (ids[0],ids[-1])


def components(adj, mask):
    answer=[]
    while mask:
        bit=mask & -mask; todo=bit; part=0
        while todo:
            q=todo & -todo; todo ^= q
            if part & q:
                continue
            v=q.bit_length()-1; part |= q
            for w in adj[v]:
                t=1<<w
                if mask&t and not part&t:
                    todo |= t
        answer.append(part); mask &= ~part
    return answer


class PackedForest:
    def __init__(self,n,edges):
        self.n=n; self.edges=tuple(sorted(tuple(sorted(e)) for e in edges))
        self.adj=validate(n,edges); self.bits=n+2
        self.digit=(1<<self.bits)-1; self.full=(1<<n)-1
        self.closed=tuple((1<<v)|sum(1<<w for w in self.adj[v]) for v in range(n))

    def unpack(self,q):
        a=tuple((q>>(k*self.bits))&self.digit for k in range(self.n+1))
        assert q>>((self.n+1)*self.bits)==0
        return a

    def count(self,mask=None):
        if mask is None:
            mask=self.full
        if mask & ~self.full or mask < 0:
            raise ValueError('invalid active mask')
        seen=set()
        def visit(v,p):
            seen.add(v); z0=z1=1
            for w in self.adj[v]:
                if w!=p and mask>>w&1:
                    a,b=visit(w,v)
                    z0*=a+b; z1*=a
            return z0,z1<<self.bits
        out=1
        for v in range(self.n):
            if mask>>v&1 and v not in seen:
                a,b=visit(v,-1); out*=a+b
        return self.unpack(out)

    def all_vertices(self):
        @lru_cache(None)
        def message(v,p):
            a=b=1
            for w in self.adj[v]:
                if w != p:
                    c,d=message(w,v); a*=c+d; b*=c
            return a,b<<self.bits
        comps=components(self.adj,self.full)
        totals=[]; compof={}
        for c in comps:
            r=(c&-c).bit_length()-1
            x,y=message(r,-1); totals.append(x+y)
            for v in range(self.n):
                if c>>v&1: compof[v]=len(totals)-1
        total=1
        for q in totals: total*=q
        A=[]; B=[]
        for v in range(self.n):
            other=1
            for z,q in enumerate(totals):
                if z!=compof[v]: other*=q
            a,b=message(v,-1)
            A.append(self.unpack(a*other)); B.append(self.unpack(b*other))
        return self.unpack(total),A,B


def deletion_counter(n,edges):
    adj=validate(n,edges)
    closed=tuple((1<<v)|sum(1<<w for w in adj[v]) for v in range(n))
    @lru_cache(None)
    def raw(mask):
        if mask==0: return (1,)
        parts=components(adj,mask)
        if len(parts)>1:
            out=(1,)
            for p in parts: out=mul(out,raw(p))
            return out
        v=max((v for v in range(n) if mask>>v&1),
              key=lambda v:sum(bool(mask>>w&1) for w in adj[v]))
        return add(raw(mask&~(1<<v)),(0,)+raw(mask&~closed[v]))
    def count(mask=None):
        return pad(raw((1<<n)-1 if mask is None else mask),n)
    return count


def one_edge_dp(n,edges):
    adj=validate(n,edges); seen=set()
    # state[selected root][number of induced edges, capped at one]
    zero=(0,); unit=(1,)
    def visit(v,p):
        seen.add(v)
        out=[[unit,zero],[(0,1),zero]]
        for w in adj[v]:
            if w==p: continue
            child=visit(w,v); new=[[zero,zero],[zero,zero]]
            for s in (0,1):
                for t in (0,1):
                    for a in (0,1):
                        for b in (0,1):
                            c=a+b+s*t
                            if c<=1:
                                new[s][c]=add(new[s][c],mul(out[s][a],child[t][b]))
            out=new
        return out
    ans=[unit,zero]
    for v in range(n):
        if v not in seen:
            z=visit(v,-1); q=[add(z[0][i],z[1][i]) for i in (0,1)]
            ans=[mul(ans[0],q[0]),add(mul(ans[0],q[1]),mul(ans[1],q[0]))]
    return pad(ans[0],n),pad(ans[1],n)


def describe(n,edges,second=False):
    f=PackedForest(n,edges); P,A,B=f.all_vertices()
    if second:
        count=deletion_counter(n,edges)
        assert P==count()
        for v in range(n):
            assert A[v]==count(f.full&~(1<<v))
            assert B[v]==pad((0,)+count(f.full&~f.closed[v]),n)
    local=all(unimodal(q) for q in A+B)
    ud=None; bad=[]; m=[]
    if n and local:
        m=[(modes(a),modes(b)) for a,b in zip(A,B)]
        U=max(min(a[1],b[1]) for a,b in m)
        D=min(max(a[0],b[0]) for a,b in m)
        ud=(U,D)
        bad=[v for v,(a,b) in enumerate(m) if max(a[0]-b[1],b[0]-a[1],0)>1]
    valleys=[(i,j) for i in range(n) if delta(P,i)<0
             for j in range(i+1,n) if delta(P,j)>0]
    pairs=[] if ud is None else [(i,j) for i in range(ud[0],ud[1]) for j in range(i+1,ud[1])]
    return dict(n=n,edges=[list(e) for e in f.edges],P=P,A=A,B=B,LOCAL=local,
                HEREDITARY='UNKNOWN',U=None if ud is None else ud[0],
                D=None if ud is None else ud[1],bad_vertices=bad,mode_intervals=m,
                residual_pairs=pairs,valleys=valleys,unimodal=unimodal(P))
