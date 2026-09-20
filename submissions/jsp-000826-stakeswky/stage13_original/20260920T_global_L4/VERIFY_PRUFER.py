#!/usr/bin/env python3
import itertools, json, hashlib
from collections import Counter, deque


def prufer_tree(n, seq):
    if n == 1:
        return [set()]
    if n == 2:
        return [{1},{0}]
    deg = [1]*n
    for x in seq:
        deg[x]+=1
    adj=[set() for _ in range(n)]
    for x in seq:
        leaf=next(i for i,d in enumerate(deg) if d==1)
        adj[leaf].add(x); adj[x].add(leaf)
        deg[leaf]-=1; deg[x]-=1
    leaves=[i for i,d in enumerate(deg) if d==1]
    a,b=leaves
    adj[a].add(b); adj[b].add(a)
    return adj


def bipartition_sizes(adj):
    n=len(adj)
    color=[None]*n
    color[0]=0
    q=deque([0])
    while q:
        v=q.popleft()
        for w in adj[v]:
            if color[w] is None:
                color[w]=1-color[v]; q.append(w)
            elif color[w]==color[v]:
                raise AssertionError('not bipartite')
    a=sum(c==0 for c in color); b=n-a
    return (min(a,b),max(a,b))


def induced_components_after_delete(adj, deleted):
    n=len(adj); deleted=set(deleted); seen=set(); comps=[]
    for s in range(n):
        if s in deleted or s in seen: continue
        comp=[]; stack=[s]; seen.add(s)
        while stack:
            v=stack.pop(); comp.append(v)
            for w in adj[v]:
                if w not in deleted and w not in seen:
                    seen.add(w); stack.append(w)
        comps.append(comp)
    return comps


def component_gap(adj, comp):
    S=set(comp); root=comp[0]; color={root:0}; q=deque([root])
    while q:
        v=q.popleft()
        for w in adj[v]:
            if w not in S: continue
            if w not in color:
                color[w]=1-color[v]; q.append(w)
    a=sum(c==0 for c in color.values()); b=len(comp)-a
    return abs(a-b)


def splittable(adj):
    a,b=bipartition_sizes(adj)
    if b-a<2: return False
    for w in range(len(adj)):
        if len(adj[w])!=1: continue
        v=next(iter(adj[w]))
        comps=induced_components_after_delete(adj,{v,w})
        if all(component_gap(adj,c)<=1 for c in comps):
            return True
    return False


def is_q7(adj):
    if len(adj)!=7: return False
    deg=[len(x) for x in adj]
    if sorted(deg)!=[1,1,1,1,2,3,3]: return False
    centers=[i for i,d in enumerate(deg) if d==3]
    mids=[i for i,d in enumerate(deg) if d==2]
    if len(centers)!=2 or len(mids)!=1: return False
    x=mids[0]
    if set(adj[x])!=set(centers): return False
    for c in centers:
        if sum(1 for w in adj[c] if deg[w]==1)!=2: return False
    return True


def is_q8(adj):
    if len(adj)!=8: return False
    deg=[len(x) for x in adj]
    if sorted(deg)!=[1,1,1,1,1,2,3,4]: return False
    c4=[i for i,d in enumerate(deg) if d==4]
    c3=[i for i,d in enumerate(deg) if d==3]
    mid=[i for i,d in enumerate(deg) if d==2]
    if len(c4)!=1 or len(c3)!=1 or len(mid)!=1: return False
    x=mid[0]; a=c4[0]; b=c3[0]
    if set(adj[x])!={a,b}: return False
    if sum(1 for w in adj[a] if deg[w]==1)!=3: return False
    if sum(1 for w in adj[b] if deg[w]==1)!=2: return False
    return True


def orientation_g(gaps, sizes):
    # component bipartition sizes (a_i,b_i); product (z^a+z^b)
    poly=[1]
    total=0
    for a,b in sizes:
        f=[0]*(b+1); f[a]+=1; f[b]+=1
        out=[0]*(len(poly)+len(f)-1)
        for i,x in enumerate(poly):
            for j,y in enumerate(f): out[i+j]+=x*y
        poly=out; total+=a+b
    assert total%2==0
    m=total//2
    c=lambda i: poly[i] if 0<=i<len(poly) else 0
    return c(m)-c(m-1),poly

rows=[]
pattern_counts=Counter()
for n in range(1,9):
    seqs=[()] if n<=2 else itertools.product(range(n), repeat=n-2)
    total=high=unspl=0
    for seq in seqs:
        adj=prufer_tree(n,seq); total+=1
        a,b=bipartition_sizes(adj)
        if b-a>=2:
            high+=1
            if not splittable(adj):
                unspl+=1
                if is_q7(adj): pattern_counts['Q7']+=1
                elif is_q8(adj): pattern_counts['Q8']+=1
                else:
                    raise AssertionError((n,seq,[len(x) for x in adj],(a,b)))
    rows.append({'n':n,'labeled_trees':total,'high_gap_trees':high,'unsplittable_high_trees':unspl})

# Algebra for the only two unsplittable structures.
g_q7_unit, poly_q7_unit = orientation_g(None, [(2,5),(0,1)])
g_q8, poly_q8 = orientation_g(None, [(2,6)])
assert g_q7_unit == -1
assert g_q8 == 0
# Four unit target used by the residual map.
g_u4, poly_u4 = orientation_g(None, [(0,1)]*4)
assert g_u4 == 2

result={
  'statement':'Complete labeled-tree classification needed for the j=4 residual sector',
  'rows':rows,
  'unsplittable_pattern_labeled_counts':dict(pattern_counts),
  'q7_plus_unit_orientation_poly':poly_q7_unit,
  'q7_plus_unit_g':g_q7_unit,
  'q8_orientation_poly':poly_q8,
  'q8_g':g_q8,
  'four_units_orientation_poly':poly_u4,
  'four_units_g':g_u4,
  'status':'PASS'
}
blob=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode()
result['canonical_payload_sha256']=hashlib.sha256(blob).hexdigest()
print(json.dumps(result,indent=2,sort_keys=True))
