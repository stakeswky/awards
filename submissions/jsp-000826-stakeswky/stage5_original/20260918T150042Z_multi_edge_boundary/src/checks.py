"""Full-array certificates for actual defect sets and partial cuts."""
import argparse, json
from pathlib import Path
from itertools import combinations
from forest import *
from multi_edge import *

SMALL=[('empty',0,[]),('isolated',1,[]),('edge',2,[(0,1)]),
 ('adjacent_pair',3,[(0,1),(1,2)]),
 ('missing_middle',4,[(0,1),(1,2),(2,3)]),
 ('star4',5,[(0,v) for v in range(1,5)]),
 ('internal_support',7,[(0,1),(1,2),(0,3),(3,4),(0,5),(5,6)]),
 ('disconnected',9,[(0,1),(1,2),(0,3),(3,4),(0,5),(5,6),(7,8)])]


def dump(path,obj):
    path.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')


def material(n,edges,ident,small=False):
    f=PackedForest(n,edges); second=deletion_counter(n,edges)
    g=describe(n,edges,second=True);g['id']=ident
    P=g['P'];D0=defect(f,(),second);assert tuple(P)==D0
    assert P[0]==1
    if n:assert P[1]==n
    if n>=2:assert P[2]==n*(n-1)//2-len(edges)
    g['edge_data']=[]
    for k,(u,v) in enumerate(f.edges):
        C=f.count(f.full&~((1<<u)|(1<<v)))
        H=f.count(f.full&~(f.closed[u]|f.closed[v])); Z=shift(H,2,n)
        assert C==second(f.full&~((1<<u)|(1<<v)))
        assert H==second(f.full&~(f.closed[u]|f.closed[v]))
        assert Z==defect(f,(k,),second)
        assert add(P,Z)==cut_polynomial(f,(k,))
        assert add(C,add(g['B'][u],g['B'][v]))==tuple(P)
        assert mul(C,Z)==mul(g['B'][u],g['B'][v])
        g['edge_data'].append(dict(edge=(u,v),C=C,H=H,Z=Z))
    g['edge_pairs']=[]
    for e,h in combinations(range(len(f.edges)),2):
        mixed=defect(f,(e,h),second)
        total=add(P,add(g['edge_data'][e]['Z'],add(g['edge_data'][h]['Z'],mixed)))
        assert total==cut_polynomial(f,(e,h))
        g['edge_pairs'].append(dict(edge_indices=(e,h),defect=mixed,P_cut=total))
    g['partial_cuts']=[];g['square_identities']=0
    for v in range(n):
        b=root_bundle(f,v,second); states={}
        for J in all_subsets(f.adj[v]):states[J]=partial_cut(f,b,J,second)
        assert states[()]['B']==tuple(g['B'][v])
        assert states[tuple(f.adj[v])]['B']==shift(g['A'][v],1,n)
        for J in states:
            for e,h in combinations([w for w in f.adj[v] if w not in J],2):
                Je=tuple(sorted(J+(e,))); Jh=tuple(sorted(J+(h,))); Jeh=tuple(sorted(J+(e,h)))
                a,ae,ah,aeh=[states[z] for z in (J,Je,Jh,Jeh)]
                M=difference(difference(aeh['B'],ae['B']),difference(ah['B'],a['B']))
                assert min(M)>=0
                factors=[b['R']]
                for branch in b['branches']:
                    w=branch['root'];factors.append(branch['Y'] if w in (e,h) else branch['M'] if w in J else branch['X'])
                assert M==shift(product(factors),1,n)
                assert mul(ae['B'],ah['B'])==mul(a['B'],aeh['B'])
                # This is a full polynomial identity, not a diagonal coefficient assertion.
                lhs=add(mul(ae['P_cut'],ah['P_cut']),mul(b['A'],M))
                rhs=mul(a['P_cut'],aeh['P_cut']);assert lhs==rhs
                g['square_identities']+=1
        g['partial_cuts'].append(dict(**b,states=list(states.values())))
    g['HEREDITARY']='UNKNOWN';g['proper_subset_checks']=0
    if small:
        table=brute_defects(f)
        for S in all_subsets(range(len(f.edges))):
            assert defect(f,S,second)==table.get(S,(0,)*(n+1))
            summed=sum_arrays([table.get(A,(0,)*(n+1)) for A in all_subsets(S)],n)
            assert summed==cut_polynomial(f,S)
        for mask in range((1<<n)-1):
            p=f.count(mask); assert p==second(mask) and unimodal(p)
            g['proper_subset_checks']+=1
        g['HEREDITARY']='VERIFIED'
        g['all_defect_sets']=[dict(edge_indices=S,P=table.get(S,(0,)*(n+1))) for S in all_subsets(range(len(f.edges)))]
    g['residual_diagnostics']=[]
    for i,j in g['residual_pairs']:
        rows=[]
        for l in range(n):
            if len(f.adj[l])!=1:continue
            w=f.adj[l][0];C=second(f.full&~((1<<l)|(1<<w)))
            X=pad(mul((1,1),C),n);Y=g['B'][w];pol=[]
            for early,late in [(X,Y),(Y,X)]:
                ei,ej,li,lj=delta(early,i),delta(early,j),delta(late,i),delta(late,j)
                if ei<0 and ej<=0 and li>=0 and lj>0:
                    pol.append(dict(E=early,L=late,Q=li*(-ej)-lj*(-ei)))
            rows.append(dict(leaf=l,support=w,polarized=pol))
        g['residual_diagnostics'].append(dict(i=i,j=j,leaves=rows,
              eligible=g['HEREDITARY']=='VERIFIED' and all(f.adj)))
    return g


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    controls=[material(n,e,name,True) for name,n,e in SMALL]
    seeds=json.loads(Path(__file__).with_name('seeds.json').read_text())
    controls += [material(g['n'],g['edges'],g['id']) for g in seeds]
    miss=next(g for g in controls if g['id']=='missing_middle')
    assert miss['all_defect_sets'][0]['P'][0]==1
    f=PackedForest(miss['n'],miss['edges']);assert defect(f,(0,2))==(0,)*5
    adj=next(g for g in controls if g['id']=='adjacent_pair')
    assert defect(PackedForest(3,adj['edges']),(0,1))==(0,0,0,1)
    old30=next(g for g in controls if g['id']=='new30');p=old30['P']
    assert p[16]**2-p[15]*p[17]==-219 and unimodal(p)
    assert modes((0,1,2,2,1,0))==(2,3)
    assert not unimodal((1,3,2,2,3,0))
    summary=dict(material_graphs=len(controls),small_interaction_controls=len(SMALL),
        edge_pairs=sum(len(g['edge_pairs']) for g in controls),
        partial_cut_states=sum(len(b['states']) for g in controls for b in g['partial_cuts']),
        square_identities=sum(g['square_identities'] for g in controls),
        proper_subsets=sum(g['proper_subset_checks'] for g in controls),
        HEREDITARY_verified=sum(g['HEREDITARY']=='VERIFIED' for g in controls),
        HEREDITARY_unknown=sum(g['HEREDITARY']=='UNKNOWN' for g in controls),
        all_full_arrays_two_algorithms=True,
        residual_graphs=sum(bool(g['residual_pairs']) for g in controls),
        residual_pairs=sum(len(g['residual_pairs']) for g in controls),
        eligible_RSM_tests=sum(r['eligible'] for g in controls for r in g['residual_diagnostics']),
        original_candidates=[g['id'] for g in controls if g['valleys']],
        inherited_non_LC_control=-219,universal_absence_claim=False)
    dump(out/'interaction_material.json',controls);dump(out/'checks_summary.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
