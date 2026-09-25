#!/usr/bin/env python3
import itertools, json, hashlib
from collections import Counter, deque


def connected_tree(n, edges):
    parent=list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        a=find(a); b=find(b)
        if a==b: return False
        parent[b]=a; return True
    for a,b in edges:
        if not union(a,b): return None
    r=find(0)
    if any(find(i)!=r for i in range(n)): return None
    adj=[set() for _ in range(n)]
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    return adj


def bip(adj):
    n=len(adj); col=[-1]*n; col[0]=0; q=deque([0])
    while q:
        v=q.popleft()
        for w in adj[v]:
            if col[w]<0: col[w]=1-col[v]; q.append(w)
    a=sum(c==0 for c in col); b=n-a
    return min(a,b),max(a,b)


def comp_gap(adj, verts):
    S=set(verts); root=next(iter(S)); col={root:0}; q=deque([root])
    while q:
        v=q.popleft()
        for w in adj[v]:
            if w in S and w not in col:
                col[w]=1-col[v]; q.append(w)
    a=sum(c==0 for c in col.values()); return abs(2*a-len(S))


def splittable(adj):
    a,b=bip(adj)
    if b-a<2: return False
    n=len(adj)
    for w in range(n):
        if len(adj[w])!=1: continue
        v=next(iter(adj[w])); deleted={v,w}; seen=set(); ok=True
        for s in range(n):
            if s in deleted or s in seen: continue
            stack=[s]; seen.add(s); cc=[]
            while stack:
                x=stack.pop(); cc.append(x)
                for y in adj[x]:
                    if y not in deleted and y not in seen:
                        seen.add(y); stack.append(y)
            if comp_gap(adj,cc)>1: ok=False; break
        if ok: return True
    return False


def kind(adj):
    n=len(adj); deg=[len(x) for x in adj]
    if n==7 and sorted(deg)==[1,1,1,1,2,3,3]:
        mids=[i for i,d in enumerate(deg) if d==2]; cs=[i for i,d in enumerate(deg) if d==3]
        if len(mids)==1 and set(adj[mids[0]])==set(cs): return 'Q7'
    if n==8 and sorted(deg)==[1,1,1,1,1,2,3,4]:
        mids=[i for i,d in enumerate(deg) if d==2]; cs=[i for i,d in enumerate(deg) if d in (3,4)]
        if len(mids)==1 and len(cs)==2 and set(adj[mids[0]])==set(cs): return 'Q8'
    return None

rows=[]; pats=Counter()
for n in range(1,9):
    if n==1:
        edge_sets=[()]
    else:
        all_edges=list(itertools.combinations(range(n),2))
        edge_sets=itertools.combinations(all_edges,n-1)
    total=high=unspl=0
    for edges in edge_sets:
        adj=[set()] if n==1 else connected_tree(n,edges)
        if adj is None: continue
        total+=1
        a,b=bip(adj)
        if b-a>=2:
            high+=1
            if not splittable(adj):
                unspl+=1; k=kind(adj)
                if k is None: raise AssertionError((n,edges,[len(x) for x in adj],(a,b)))
                pats[k]+=1
    rows.append({'n':n,'labeled_trees':total,'high_gap_trees':high,'unsplittable_high_trees':unspl})
res={'statement':'Independent edge-subset enumeration for the j=4 residual classification','rows':rows,'unsplittable_pattern_labeled_counts':dict(pats),'status':'PASS'}
canon=(json.dumps(res,sort_keys=True,separators=(',',':'))+'\n').encode();res['canonical_payload_sha256']=hashlib.sha256(canon).hexdigest()
print(json.dumps(res,indent=2,sort_keys=True))
