"""Reproducible exact checks for global identities; no universal search claim."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from forest import *

OLD23=[(0,1),(0,17),(0,22),(1,2),(1,3),(1,15),(1,16),(2,4),(2,5),(2,6),(2,10),(2,14),(2,18),(3,8),(3,9),(3,20),(3,21),(6,7),(8,13),(9,11),(9,12),(18,19)]
OLD25=[(0,1),(0,7),(0,16),(1,2),(1,3),(1,5),(3,4),(5,6),(7,8),(7,10),(7,12),(7,14),(8,9),(10,11),(12,13),(14,15),(16,17),(16,19),(16,21),(16,23),(17,18),(19,20),(21,22),(23,24)]
CONTROLS=[('old23',23,OLD23),('old25',25,OLD25),('new30',30,OLD25+[(2,25),(25,26),(26,27),(26,28),(26,29)]),('star7',7,[(0,v) for v in range(1,7)]),('ratio_positive',5,[(2,0),(3,0),(0,1),(1,4)]),('ratio_negative',6,[(2,0),(3,0),(4,0),(0,1),(1,5)]),('disconnected_control',11,[(2,0),(3,0),(0,1),(1,4)]+[(u+5,v+5) for u,v in [(2,0),(3,0),(4,0),(0,1),(1,5)]])]


def brute(n,edges):
    f=PackedForest(n,edges); p=[0]*(n+1); w=[0]*(n+1)
    K=[0]*(n+1); availpairs=[0]*(n+1); edgeres=[0]*(n+1)
    slack=[0]*(n+1); stars=[0]*(n+1); hereditary=True
    for mask in range(1<<n):
        internal=sum(bool(mask>>u&1 and mask>>v&1) for u,v in edges)
        k=mask.bit_count()
        if internal==1:w[k]+=1
        if internal>=2 and any(sum(bool(mask>>z&1) for z in f.adj[v])==internal for v in range(n) if mask>>v&1):
            stars[k]+=1
        if internal:continue
        p[k]+=1
        remaining=f.full
        for v in range(n):
            if mask>>v&1: remaining &= ~f.closed[v]
        q=remaining.bit_count(); K[k]+=len(components(f.adj,remaining))
        availpairs[k]+=q*(q-1)//2
        edgeres[k]+=sum(bool(remaining>>u&1 and remaining>>v&1) for u,v in edges)
        slack[k]+=sum(not(mask>>u&1 or mask>>v&1) for u,v in edges)
    count=deletion_counter(n,edges)
    # Full premise verification, not only LOCAL.
    for mask in range((1<<n)-1):
        p_mask=f.count(mask); assert p_mask==count(mask)
        hereditary &= unimodal(p_mask)
    return dict(P=p,W=w,K=K,available_pairs=availpairs,edge_residual_sum=edgeres,
                endpoint_slack=slack,star_two_or_more=stars,HEREDITARY=hereditary,proper_masks=(1<<n)-1)


def product(qs):
    z=(1,)
    for q in qs:z=mul(z,q)
    return z


def edge_checks(n,edges,do_brute=False):
    g=describe(n,edges,second=True); f=PackedForest(n,edges)
    P,A,B=map(tuple,(g['P'],g['A'],g['B']))
    assert P[0]==1
    if n:assert P[1]==n
    if n>=2:assert P[2]==n*(n-1)//2-len(edges)
    count=deletion_counter(n,edges); rows=[]; Csum=[0]*(n+1); W=[0]*(n+1)
    ratio=[]
    for u,v in f.edges:
        cmask=f.full&~((1<<u)|(1<<v)); hmask=f.full&~(f.closed[u]|f.closed[v])
        C=f.count(cmask); H=f.count(hmask); Z=pad((0,0)+H,n)
        assert C==count(cmask) and H==count(hmask)
        deleted=[e for e in f.edges if e!=(u,v)]
        Pd=PackedForest(n,deleted).count(); assert Pd==deletion_counter(n,deleted)()
        assert Pd==add(P,Z)
        for leaf in (u,v):
            if len(f.adj[leaf])==1:
                assert Pd==pad(mul((1,1),A[leaf]),n)
        # Actual contraction, retaining all other components and deleting v.
        labels=[z for z in range(n) if z!=v]; index={z:i for i,z in enumerate(labels)}
        ce=[(index[u if a==v else a],index[u if b==v else b]) for a,b in deleted]
        Q=PackedForest(n-1,ce).count(); assert Q==deletion_counter(n-1,ce)()
        assert pad(Q,n)==add(C,pad((0,)+H,n))
        assert P==add(C,add(B[u],B[v]))
        assert mul(C,Z)==mul(B[u],B[v])
        assert mul(A[u],A[v])==mul(C,Pd)
        assert all(B[u][k]+B[v][k]<=P[k] for k in range(n+1))
        for k in range(n+1):Csum[k]+=C[k];W[k]+=Z[k]
        for k in range(n):
            if min(B[u][k],B[v][k],C[k],Z[k])>0:
                q=B[u][k+1]*B[v][k+1]*C[k]*Z[k]-B[u][k]*B[v][k]*C[k+1]*Z[k+1]
                if q:ratio.append(dict(edge=[u,v],k=k,signed_cross_product=q))
        rows.append(dict(edge=[u,v],C=C,H=H,Z=Z,edge_deleted_P=Pd,
                         contracted_n=n-1,contracted_edges=ce,contracted_P=Q))
    for v in range(n):
        incident=[q for q in rows if v in q['edge']]
        d=len(f.adj[v])
        if d:
            assert mul((0,1),product([q['C'] for q in incident]))==mul(B[v],product([A[v]]*(d-1)))
        for k in range(n+1):
            Tv=(A[v][k-1] if k else 0)-B[v][k]
            assert sum(q['Z'][k] for q in incident)<=Tv
    star_excess=[(n-k+1)*(P[k-1] if k else 0)-k*P[k]-2*W[k] for k in range(n+1)]
    assert min(star_excess)>=0
    for k in range(n+1):
        assert sum(B[v][k] for v in range(n))==k*P[k]
        weighted=sum(len(f.adj[v])*B[v][k] for v in range(n))
        assert weighted==len(edges)*P[k]-Csum[k]
        assert sum((2-len(f.adj[v]))*B[v][k] for v in range(n))==(2*k-len(edges))*P[k]+Csum[k]
    P0,P1=one_edge_dp(n,edges); assert P0==P and P1==tuple(W)
    # This K table is derived by the identity; independent brute verification is below.
    K=[(r+1)*(P[r+1] if r+1<=n else 0)-(W[r+2] if r+2<=n else 0) for r in range(n+1)]
    assert min(K)>=0
    pc=False
    if n and all(f.adj):
        c=len(components(f.adj,f.full))
        lhs=product([q['C'] for q in rows])
        rhs=product([P]*(c-1)+[A[v] for v in range(n) for _ in range(len(f.adj[v])-1)])
        assert lhs==rhs
        assert mul(rhs,product([q['Z'] for q in rows]))==product([B[v] for v in range(n) for _ in f.adj[v]])
        pc=True
    g.update(edge_data=rows,W=W,K_from_identity=K,endpoint_slack=Csum,
             product_identity_checked=pc,star_excess=star_excess,ratio_nonzero=ratio)
    if do_brute:
        b=brute(n,edges)
        assert tuple(b['P'])==P and b['W']==W and b['K']==K and b['endpoint_slack']==Csum
        assert b['star_two_or_more']==star_excess
        for r in range(n+1):
            wk=W[r+2] if r+2<=n else 0
            assert wk==b['edge_residual_sum'][r]
            assert wk==b['available_pairs'][r]-((r+2)*(r+1)//2)*(P[r+2] if r+2<=n else 0)
        g['HEREDITARY']='VERIFIED' if b['HEREDITARY'] else 'FAILED'
        g['brute_certificate']=b
    return g


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    invalid=[(-1,[]),(2,[(0,0)]),(2,[(0,1),(1,0)]),(2,[(0,2)]),(3,[(0,1),(1,2),(2,0)])]
    for n,edges in invalid:
        try:validate(n,edges)
        except ValueError:pass
        else:raise AssertionError('invalid forest accepted')
    assert modes((0,1,2,2,1,0))==(2,3)
    assert modes((1,1))==(0,1)
    assert unimodal((1,)) and unimodal((0,1,1,0)) and not unimodal((1,3,2,3))
    regression=[];per_order=[]
    for n in range(6):
        e=list(itertools.combinations(range(n),2));total=0
        for bits in range(1<<len(e)):
            edges=[q for j,q in enumerate(e) if bits>>j&1]
            try:validate(n,edges)
            except ValueError:continue
            g=edge_checks(n,edges,do_brute=True)
            assert g['unimodal'] and g['LOCAL'] and g['HEREDITARY']=='VERIFIED'
            total+=1
        per_order.append(total)
    material=[]
    for name,n,edges in CONTROLS:
        g=edge_checks(n,edges,do_brute=n<=11);g['id']=name;material.append(g)
    assert material[0]['P']==(1,23,231,1359,5287,14516,29219,44068,50306,43483,28198,13441,4542,1022,136,8,0,0,0,0,0,0,0,0)
    new=material[2]['P'];assert new[16]*new[16]-new[15]*new[17]==-219 and unimodal(new)
    ratio_graph=material[6]
    def positive_coefficients(r):
        u,v=r['edge'];k=r['k'];e=next(z for z in ratio_graph['edge_data'] if z['edge']==[u,v])
        return min(ratio_graph['B'][u][k:k+2]+ratio_graph['B'][v][k:k+2]+e['C'][k:k+2]+e['Z'][k:k+2])>0
    plus=next(x for x in ratio_graph['ratio_nonzero'] if x['signed_cross_product']>0 and positive_coefficients(x))
    minus=next(x for x in ratio_graph['ratio_nonzero'] if x['signed_cross_product']<0 and positive_coefficients(x))
    summary=dict(regression_labeled_forests_per_order=per_order,regression_total=sum(per_order),invalid_graphs_rejected=len(invalid),plateau_controls=5,
                 material_records=len(material),material_hereditary_verified=sum(g['HEREDITARY']=='VERIFIED' for g in material),
                 material_hereditary_unknown=sum(g['HEREDITARY']=='UNKNOWN' for g in material),
                 original_candidates=[g['id'] for g in material if g['valleys']],
                 residual_graphs=sum(bool(g['residual_pairs']) for g in material),
                 residual_pairs=sum(len(g['residual_pairs']) for g in material),
                 eligible_RSM_tests=0,non_LC_control=-219,
                 ratio_shortcut=dict(positive_graph=ratio_graph['id'],positive=plus,negative_graph=ratio_graph['id'],negative=minus,
                                    all_eight_coefficients_positive=True,HEREDITARY='VERIFIED',scope='UNLOCALIZED_ONLY; neither residual J_H nor RSM refuted'),
                 material_all_P_A_B_C_H_edge_delete_contract_two_algorithms=True,
                 all_W_recomputed_by_independent_one_edge_DP=True,
                 brute_component_double_count_scope='All 340 labeled forests on 0..5 vertices and four material controls of orders 5,6,7,11',
                 universal_math_verification=False)
    for name,obj in [('material.json',material),('checks_summary.json',summary)]:
        (out/name).write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
