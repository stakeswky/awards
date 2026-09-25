"""Exact whole-graph and full-allocation certificates for C6-SC.
Run targeted_search.py first. No ordinary large graph is assumed HEREDITARY.
"""
import argparse,json,sys,hashlib
from pathlib import Path
from fractions import Fraction as Q
from inherited_exact import bush,bush_formula,graph_dp,union,lc_bad,valleys,mu,sig,direct_G,split
from deletion_balanced import deletion
from signed_cut import cut_record,convolution,jsonable,last_mode
from graph_controls import invariants,history,c5_windows,graph_record
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)

def allocations(a,b,k):
    p=convolution(a,b);out=[]
    for i in range(max(0,k-len(b)+1),min(k,len(a)-1)+1):
        w=Q(a[i]*b[k-i],p[k]);mx=mu(a,i);my=mu(b,k-i);sx=sig(a,i);sy=sig(b,k-i)
        out.append(dict(a=i,b=k-i,w=w,mu_X=mx,mu_Y=my,sigma_X=sx,sigma_Y=sy,
                        signed_local_budget=w*(sx+sy),negative_part=w*(min(sx,0)+min(sy,0))))
    assert sum(row['w'] for row in out)==1
    return out

def run(outdir):
    T26=bush([3,4,4]);B212=bush([6,7,7,7]+[8]*9);B226=bush([0]+[8]*13,[3]+[0]*13)
    B239=bush([8]*14);T8=bush([8]*3);T10=bush([10,11,12])
    sr=json.loads((outdir/'TARGETED_SEARCH.json').read_text())
    q=sr['best'];gX=(q['X']['n'],q['X']['edges']);gY=(q['Y']['n'],q['Y']['edges'])
    specs=[
      ('T26_squared_guard',T26,T26,[16,17,20],'C5 HEREDITARY guard; C4-covered',True),
      ('comparable_unequal_bushes',T8,T10,None,'two non-LC complete components; not a palette-closure claim',False),
      ('B212_B226_control',B212,B226,[137,138,150],'distinct historical identities; C4-covered',False),
      ('fixed_graft_seed',B239,B212,[sr['k']],'fixed-size search baseline; C4-covered',False),
      ('fixed_graft_best',gX,gY,[sr['k'],sr['k']+1],'real graft changes both degree profiles; no C5 window',False),
      ('inverse_pair_middle_control',T26,B212,[78],'inverse Toeplitz pair control; another orientation has a C5 window',False),
      ('negative_total_paid_tail_control',T26,(2,[(0,1)]),[13],'actual negative total H paid by decline; tail only, LC proper component',False),
      ('plateau_boundary_control',(1,[]),(2,[]),[1],'actual plateau without history, outside middle',False),
    ]
    records=[];count_tasks=entries=0;pos=histcount=earlier=qualified=neg_sigma=inverse=outside=0
    for name,X,Y,ks,purpose,H in specs:
        A=graph_dp(*X);B=graph_dp(*Y);F=union([X,Y]);p=graph_dp(*F)
        A2,xa=deletion(*X);B2,yb=deletion(*Y);p2,fp=deletion(*F)
        assert A==A2 and B==B2 and p==p2==convolution(A,B)
        count_tasks+=3;entries+=len(A)+len(B)+len(p)
        inv=invariants(F,p)
        if ks is None:
            k0=next(k for k in range(len(p)-1) if p[k]>p[k+1]);ks=sorted(set([k0,k0+1,inv['beta']-2]))
        wrX=c5_windows(A,B,p);wrY=c5_windows(B,A,p)
        rows=[]
        for k in ks:
            r=cut_record(A,B,k+1,pair_audit=True);bud=split(A,B,k,full=True);alloc=allocations(A,B,k)
            modeA=last_mode(A);modal_cut=modeA-1
            modal_donor=r['curvature'][modal_cut]*r['cut_weights'][modal_cut]
            assert r['curvature'][modal_cut]>=0 and modal_donor>=0
            modal_payment=r['N_next']*r['present_loss']+r['birth']+modal_donor-r['negative_cut_upper_budget']
            modal_lower=Q((k+1)*(k+2),p[k])*modal_payment/r['N']
            lo=Q((k+1)*(k+2),p[k])*r['next_loss_lower_bound']
            assert lo<=bud['G']==direct_G(p,k)
            h=history(p,k);eligible=h is not None and inv['h']<=k and k+1<inv['beta']
            if r['gate']:assert p[k+1]>=p[k+2] and bud['G']>=0
            if eligible:assert r['gate'] and modal_payment>=0
            pos+=1;histcount+=h is not None;earlier+=h is not None and h<k;qualified+=eligible
            neg_sigma+=eligible and bud['negative_mass']>0;inverse+=eligible and r['negative_pairs']>0;outside+=not eligible
            rows.append(dict(k=k,history_start=h,history_before_current=h is not None and h<k,
                middle_range=inv['h']<=k and k+1<inv['beta'],qualified=eligible,
                cut=r,allocation_budget=bud,all_allocations=alloc,G_lower_bound=lo,
                fixed_modal_donor=dict(A_mode=modeA,cut=modal_cut,donor=modal_donor,payment=modal_payment,G_lower_bound=modal_lower)))
        rec=dict(name=name,purpose=purpose,X=graph_record(X),Y=graph_record(Y),F=graph_record(F),A=A,B=B,P=p,
           invariants=inv,X_nonLC=lc_bad(A),Y_nonLC=lc_bad(B),whole_nonLC=lc_bad(p),
           original_valleys=valleys(p),X_valleys=valleys(A),Y_valleys=valleys(B),
           proper_LC_component_subunion=not lc_bad(A) or not lc_bad(B) if len(inv['component_orders'])==2 else 'not tested for this control',
           HEREDITARY='CERTIFIED_BY_C5_GUARD_SEPARATE_REPLAY' if H else 'UNKNOWN',
           C5_X_window=wrX,C5_Y_window=wrY,positions=rows,
           independent_deletion_stats=dict(X=xa,Y=yb,F=fp))
        records.append(rec)
    report=dict(status='PASS',whole_graph_pairs=len(specs),array_tasks_dual_recounted=count_tasks,
        coefficient_entries_dual_recounted=entries,material_positions=pos,history_positions=histcount,
        prior_history_positions=earlier,qualified_middle_history_positions=qualified,
        qualified_negative_sigma_positions=neg_sigma,qualified_inverse_Toeplitz_positions=inverse,
        nonqualified_controls=outside,original_counterexamples=sum(bool(r['original_valleys']) for r in records),
        records=records)
    return report
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--outdir',required=True);a=ap.parse_args();p=Path(a.outdir);r=run(p)
    (p/'MATERIAL_FULL.json').write_text(json.dumps(jsonable(r),sort_keys=True,indent=2)+'\n')
    key_names={'T26_squared_guard','comparable_unequal_bushes','fixed_graft_best','inverse_pair_middle_control','negative_total_paid_tail_control'}
    key=dict(scope='selected material controls, NOT extra coverage',records=[g for g in r['records'] if g['name'] in key_names])
    (p/'KEY_CERTIFICATE.json').write_text(json.dumps(jsonable(key),sort_keys=True,indent=2)+'\n')
    summary={k:v for k,v in r.items() if k!='records'}
    summary['positions']=[dict(name=g['name'],n=g['invariants']['n'],k=v['k'],qualified=v['qualified'],
      no_C5_window=not(g['C5_X_window']['qualifying'] or g['C5_Y_window']['qualifying']),
      reverse_pairs=v['cut']['negative_pairs'],negative_cut_mass_positive=v['cut']['exact_negative_cut_mass']>0,
      gate=v['cut']['gate'],G=v['allocation_budget']['G'],G_lower_bound=v['G_lower_bound'],
      negative_sigma_mass=v['allocation_budget']['negative_mass']) for g in r['records'] for v in g['positions']]
    (p/'MATERIAL_SUMMARY.json').write_text(json.dumps(jsonable(summary),sort_keys=True,indent=2)+'\n')
    print({k:v for k,v in summary.items() if k!='positions'})
    for v in summary['positions']:
        print(v['name'],v['k'],'qual',v['qualified'],'noC5',v['no_C5_window'],'rev',v['reverse_pairs'],'G',float(v['G']),'bound',float(v['G_lower_bound']))
