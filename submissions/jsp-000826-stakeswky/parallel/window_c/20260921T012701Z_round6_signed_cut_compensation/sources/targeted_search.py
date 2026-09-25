"""Fixed-order/fixed-index actual graft search for failure of the C6 payment gate.
No HEREDITARY inference for ordinary graphs. Every full polynomial is valley-scanned.
"""
import argparse,json,random,sys
from pathlib import Path
from fractions import Fraction as Q
from inherited_exact import bush,graph_dp,union,lc_bad,valleys
from signed_cut import cut_record,convolution,jsonable
from graph_controls import history,invariants,graft,c5_windows,graph_record
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)

def run(seed,steps):
    rng=random.Random(seed)
    X=bush([8]*14);Y=bush([6,7,7,7]+[8]*9)
    A=graph_dp(*X);B=graph_dp(*Y);F=union([X,Y]);p=convolution(A,B)
    k=next(k for k in range(len(p)-1) if p[k]>p[k+1])
    first=cut_record(A,B,k+1)
    def score(rec):
        den=rec['N_next']*rec['present_loss']+rec['birth']+rec['donor_budget']
        return Q(rec['negative_cut_upper_budget'],den) if den>0 else Q(0)
    best=score(first);bestX=X;bestY=Y;bestA=A;bestB=B
    rows=[];saved=[];counts=dict(proposals=0,identity=0,nonLC_rejections=0,history_rejections=0,mode_rejections=0,
          original_valleys=0,component_valleys=0,valid_gate_tests=0,gate_failures=0,accepted=0)
    for step in range(steps):
        side=rng.randrange(2);xx,yy=X,Y
        if side==0:xx=graft(X,rng)
        else:yy=graft(Y,rng)
        counts['proposals']+=1
        if xx==X and yy==Y:counts['identity']+=1;continue
        aa=graph_dp(*xx) if side==0 else A;bb=graph_dp(*yy) if side==1 else B
        pp=convolution(aa,bb);vs=valleys(pp)
        if vs:
            counts['original_valleys']+=1;saved.append(dict(kind='original_candidate',X=graph_record(xx),Y=graph_record(yy),P=pp,valleys=vs))
        av,bv=valleys(aa),valleys(bb)
        if av or bv:
            counts['component_valleys']+=bool(av)+bool(bv)
            saved.append(dict(kind='component_original_candidate',X=graph_record(xx),Y=graph_record(yy),A=aa,B=bb,X_valleys=av,Y_valleys=bv))
        if not lc_bad(aa) or not lc_bad(bb) or av or bv:
            counts['nonLC_rejections']+=1;continue
        inv=invariants(union([xx,yy]),pp)
        if history(pp,k) is None or not inv['h']<=k or not k+1<inv['beta']:
            counts['history_rejections']+=1;continue
        try:r=cut_record(aa,bb,k+1)
        except ValueError:counts['mode_rejections']+=1;continue
        counts['valid_gate_tests']+=1;s=score(r)
        if not r['gate']:
            counts['gate_failures']+=1;saved.append(dict(kind='payment_gate_failure',X=graph_record(xx),Y=graph_record(yy),k=k,cut=r))
        accepted=s>=best
        rows.append(dict(step=step,score=s,gate=r['gate'],accepted=accepted,k=k,
                         current_loss=pp[k]-pp[k+1],next_loss=pp[k+1]-pp[k+2]))
        if accepted:
            counts['accepted']+=1;X,Y,A,B=xx,yy,aa,bb;best=s;bestX,bestY,bestA,bestB=X,Y,A,B
    P=convolution(bestA,bestB)
    return dict(seed=seed,steps=steps,k=k,counts=counts,rows=rows,saved=saved,
       best=dict(X=graph_record(bestX),Y=graph_record(bestY),A=bestA,B=bestB,P=P,
          score=best,cut=cut_record(bestA,bestB,k+1,pair_audit=True),
          windows_X=c5_windows(bestA,bestB,P),windows_Y=c5_windows(bestB,bestA,P)),
       HEREDITARY='UNKNOWN',deduplication='labelled proposals only; no unlabeled novelty claim')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--steps',type=int,default=250);ap.add_argument('--seed',type=int,default=20260921);a=ap.parse_args()
    r=run(a.seed,a.steps);p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(jsonable(r),sort_keys=True,indent=2)+'\n');print(r['counts']);print('best score',float(r['best']['score']),'windows',r['best']['windows_X']['qualifying'],r['best']['windows_Y']['qualifying'])
