"""Independent saved-data arithmetic audit, with unnormalized pair sums.
Graph DP is not imported. Stored full polynomials are checked via vertex deletion.
"""
import argparse,json,sys
from pathlib import Path
from fractions import Fraction as Q
from deletion_balanced import deletion,multiply
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
def cv(x):
    if isinstance(x,dict):
        if set(x)=={'num','den'}:return Q(int(x['num']),int(x['den']))
        return {k:cv(v) for k,v in x.items()}
    if isinstance(x,list):return [cv(v) for v in x]
    return x

def at(p,j):return p[j] if 0<=j<len(p) else 0

def audit(p):
    full=cv(json.loads((p/'MATERIAL_FULL.json').read_text()));tasks=coeffs=positions=allocs=negpairs=0
    for g in full['records']:
        for key,array in [('X','A'),('Y','B'),('F','P')]:
            actual,_=deletion(g[key]['n'],g[key]['edges']);assert actual==g[array];tasks+=1;coeffs+=len(actual)
        A,B,C=g['A'],g['B'],g['P'];assert multiply(A,B)==C
        for row in g['positions']:
            k=row['k'];z=k+1;r=row['cut'];m=max(i for i,x in enumerate(B) if x==max(B))
            plus=[(j,at(B,j)-at(B,j-1)) for j in range(m+1)]
            minus=[(t,at(B,t-1)-at(B,t)) for t in range(m+1,len(B)+1)]
            P=sum(u*at(A,z-j) for j,u in plus);N=sum(v*at(A,z-t) for t,v in minus)
            P1=sum(u*at(A,z+1-j) for j,u in plus);N1=sum(v*at(A,z+1-t) for t,v in minus)
            assert (P,N,P1,N1)==(r['P'],r['N'],r['P_next'],r['N_next'])
            Hp=Hn=0
            for j,u in plus:
                for t,v in minus:
                    val=u*v*(at(A,z-j)*at(A,z+1-t)-at(A,z+1-j)*at(A,z-t))
                    Hp+=max(val,0);Hn+=max(-val,0)
            assert Hp==r['pair_positive'] and Hn==r['pair_negative'] and Hp-Hn==r['H']
            assert r['payment']==N1*(C[k]-C[k+1])+r['lower_H']
            assert r['next_loss_lower_bound']==r['payment']/N<=C[k+1]-C[k+2]
            mf=Q((k+1)*C[k+1],C[k]);var=Q(0);es=Q(0);neg=Q(0)
            for ar in row['all_allocations']:
                i,j=ar['a'],ar['b'];w=Q(A[i]*B[j],C[k]);mux=Q((i+1)*at(A,i+1),A[i]);muy=Q((j+1)*at(B,j+1),B[j])
                sx=mux+mux*mux-Q((i+1)*(i+2)*at(A,i+2),A[i]);sy=muy+muy*muy-Q((j+1)*(j+2)*at(B,j+2),B[j])
                assert ar['w']==w and ar['sigma_X']==sx and ar['sigma_Y']==sy
                assert ar['signed_local_budget']==w*(sx+sy)
                var+=w*(mux+muy-mf)**2;es+=w*(sx+sy);neg+=w*(min(sx,0)+min(sy,0));allocs+=1
            R=es+mf*(k+1-mf);G=Q((k+1)*(k+2)*(C[k+1]-C[k+2]),C[k])
            assert R-var==G==row['allocation_budget']['G'] and var==row['allocation_budget']['V']
            assert neg==row['allocation_budget']['negative_budget']
            assert row['G_lower_bound']==Q((k+1)*(k+2),C[k])*r['payment']/N<=G
            md=row['fixed_modal_donor'];u=md['A_mode'];ell=u-1
            assert A[u]==max(A) and u==max(i for i,v in enumerate(A) if v==max(A))
            curv=Q(A[u],A[u-1])-Q(at(A,u+1),A[u])
            assert curv>=0 and md['donor']==curv*r['cut_weights'][ell]
            assert md['payment']==N1*(C[k]-C[k+1])+r['birth']+md['donor']-r['negative_cut_upper_budget']
            assert md['G_lower_bound']==Q((k+1)*(k+2),C[k])*md['payment']/N<=G
            positions+=1;negpairs+=Hn>0
    lc=json.loads((p/'LCFREE_REGRESSION.json').read_text())
    for g in lc['rows']:
        s,t=g['s'],g['t'];u=2**s+s;v=s*2**(s-1)+s*(s-1)//2
        assert g['P'][-1]==1
        assert 2*(g['P'][-2]**2-g['P'][-3])==t*((9*t+3)*u*u-6*v-2*2**(3*s))<0
    search=json.loads((p/'TARGETED_SEARCH.json').read_text())
    assert search['counts']['original_valleys']==search['counts']['component_valleys']==0
    return dict(status='PASS',array_tasks_independently_reaudited=tasks,coefficient_entries=coeffs,
                material_positions=positions,all_allocation_rows_reaudited=allocs,
                positions_with_inverse_pair_mass=negpairs,LC_free_tail_identities=len(lc['rows']),
                review='SAME_MODEL_SELF_REVIEW with independent arithmetic routes; not external review')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--outdir',required=True);a=ap.parse_args();p=Path(a.outdir);r=audit(p)
    (p/'AUDIT.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r)
