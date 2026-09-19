#!/usr/bin/env python3
"""Exact checks for the uniform large-component LC-block obstruction.
The all-parameter proof is in PROOF_ATTEMPT.md; these are checks, not its basis.
"""
from pathlib import Path
from math import comb
import json
from forest_exact import *
BASE=Path(__file__).resolve().parents[1]

def power(p,r):
    q=(1,)
    for _ in range(r): q=conv(q,p)
    return q

def main():
    out=[]; conditional_checks=0
    for k,rmax in [(6,1),(7,3),(8,7),(10,3)]:
        a=2**k+k; b=k*2**(k-1)+comb(k,2)
        s=add(tuple(comb(k,j)*2**j for j in range(k+1)),shift(tuple(comb(k,j) for j in range(k+1))))
        p=add(power(s,3),shift(tuple(comb(3*k,j)*2**j for j in range(3*k+1))))
        h=hub_tree([k,k,k]); assert p==independence_dp(h)==deletion_counter(h)((1<<len(h))-1)
        for r in range(1,rmax+1):
            q=power(p,r); deg=r*(3*k+3)
            exact=q[-2]**2-q[-3]*q[-1]
            numerator=r*((9*r+3)*a*a-2*2**(3*k)-6*b)
            assert numerator%2==0 and exact==numerator//2
            assert 2**k>18*r+6 and exact<0
            # An independent packed-product recomputation of every full coefficient.
            other=(1,)
            for _ in range(r): other=packed_conv(other,p)
            assert q==other
            actual=union(*([h]*r)); pr=profile(actual); count=deletion_counter(actual); mask=(1<<len(actual))-1
            assert q==tuple(pr['P'])==count(mask)
            for vr in pr['vertices']:
                v=vr['v']; rest=mask&~(1<<v); closed=rest
                for w in actual[v]: closed&=~(1<<w)
                assert tuple(vr['A'])==count(rest) and tuple(vr['B'])==shift(count(closed))
                conditional_checks+=2
            assert pr['LOCAL']
            out.append({'U':pr['U'],'D':pr['D'],'residual_pairs':pr['residual_pairs'],
                        'HEREDITARY':'PROVED_BY_H64_COMPRESSION' if k==10 and r==1 else 'UNKNOWN',
                        'all_vertex_modes':[{'v':v['v'],'A':v['A_modes'],'B':v['B_modes']} for v in pr['vertices']],
                        'P':q,'k':k,'r':r,'component_order':len(h),'degree':deg,'top_minor':exact,
                        'full_sequence_unimodal':unimodal(q),'valleys':valleys(q)})
    result={'status':'PASS','checked_parameter_pairs':len(out),'all_vertex_conditionals_dual_recounted':conditional_checks,'checks':out,
      'proved_uniform_claim':'For every r>=1 choose 2^k>=32(r+1). Every nonempty component block of r disjoint H_k trees is non-log-concave.',
      'all_parameter_unimodality':'NOT_CLAIMED','all_parameter_HEREDITARY':'UNKNOWN',
      'original_counterexample_from_non_log_concavity':False,
      'scope':'Obstruction to bounding the number of large components using only non-log-concavity of component blocks; not a counterexample or an obstruction to stronger full-minimality arguments.'}
    (BASE/'certificates/large_block_obstruction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
if __name__=='__main__': main()
