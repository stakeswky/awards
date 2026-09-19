"""Exact graph-semantic multi-edge and partial-star identities. No shape claim."""
from itertools import combinations
from forest import PackedForest, deletion_counter, components, add, mul, pad, unimodal


def shift(p, k, n):
    return pad((0,) * k + tuple(p), n)


def difference(a, b):
    assert len(a) == len(b)
    return tuple(x-y for x,y in zip(a,b))


def sum_arrays(arrays, n):
    r=(0,)*(n+1)
    for a in arrays:r=add(r,a)
    return r


def product(arrays):
    r=(1,)
    for a in arrays:r=mul(r,a)
    return r


def normalized_cut(f, edge_indices):
    ids=tuple(sorted(set(edge_indices)))
    if any(type(j) is not int or not 0<=j<len(f.edges) for j in ids):
        raise ValueError('edge index out of range')
    return ids


def defect(f, edge_indices, second=None):
    """Count T with E(F[T]) EXACTLY the requested edge set."""
    ids=normalized_cut(f,edge_indices)
    endpoints=0
    for j in ids:
        u,v=f.edges[j]; endpoints|=(1<<u)|(1<<v)
    actual=tuple(j for j,(u,v) in enumerate(f.edges)
                 if endpoints>>u&1 and endpoints>>v&1)
    if ids!=actual:return (0,)*(f.n+1)
    allowed=f.full
    for v in range(f.n):
        if endpoints>>v&1:allowed &= ~f.closed[v]
    p=f.count(allowed)
    if second is not None:assert p==second(allowed)
    return shift(p,endpoints.bit_count(),f.n)


def cut_polynomial(f, ids, independent=True):
    ids=set(normalized_cut(f,ids))
    edges=[e for j,e in enumerate(f.edges) if j not in ids]
    p=PackedForest(f.n,edges).count()
    if independent:assert p==deletion_counter(f.n,edges)()
    return p


def all_subsets(items):
    items=tuple(items)
    for k in range(len(items)+1):yield from combinations(items,k)


def root_bundle(f,v,second=None):
    if not 0<=v<f.n:raise ValueError('vertex out of range')
    masks=components(f.adj,f.full&~(1<<v)); branches=[]; outside=0
    for mask in masks:
        roots=[w for w in f.adj[v] if mask>>w&1]
        assert len(roots)<=1
        if not roots:outside|=mask;continue
        w=roots[0]; M=f.count(mask); X=f.count(mask&~(1<<w))
        if second is not None:
            assert M==second(mask) and X==second(mask&~(1<<w))
        branches.append(dict(root=w,mask=mask,M=M,X=X,Y=difference(M,X)))
    R=f.count(outside)
    if second is not None:assert R==second(outside)
    branches.sort(key=lambda b:b['root'])
    A=pad(product([R]+[b['M'] for b in branches]),f.n)
    assert A==f.count(f.full&~(1<<v))
    return dict(v=v,R=R,outside_mask=outside,branches=branches,A=A)


def partial_cut(f,bundle,J,second=None):
    v=bundle['v']; J=set(J)
    if not J<=set(f.adj[v]):raise ValueError('non-neighbor cut')
    B=shift(product([bundle['R']]+[b['M'] if b['root'] in J else b['X']
                                   for b in bundle['branches']]),1,f.n)
    mask=f.full&~(1<<v)
    for w in f.adj[v]:
        if w not in J:mask &= ~(1<<w)
    direct=f.count(mask)
    if second is not None:assert direct==second(mask)
    assert B==shift(direct,1,f.n)
    ids=[j for j,e in enumerate(f.edges) if v in e and (e[0] if e[1]==v else e[1]) in J]
    whole=add(bundle['A'],B)
    assert whole==cut_polynomial(f,ids,independent=second is not None)
    return dict(J=sorted(J),B=B,P_cut=whole,proper_vertex_mask=mask,
                B_unimodal=unimodal(B),P_cut_unimodal=unimodal(whole))


def brute_defects(f):
    """Independent direct vertex subset classification, only small controls."""
    data={}
    for mask in range(1<<f.n):
        ids=tuple(j for j,(u,v) in enumerate(f.edges) if mask>>u&1 and mask>>v&1)
        a=data.setdefault(ids,[0]*(f.n+1)); a[mask.bit_count()]+=1
    return {ids:tuple(a) for ids,a in data.items()}
