#!/usr/bin/env python3
"""Proved symmetry compression for ALL induced subforests of H(10,10,10).
The coverage proof is in PROOF_ATTEMPT.md, not inferred from this program.
"""
from pathlib import Path
from itertools import combinations_with_replacement
from math import comb
import hashlib,json
from forest_exact import *
BASE=Path(__file__).resolve().parents[1]

def binom_poly(k,c=1): return tuple(comb(k,j)*c**j for j in range(k+1))

def main():
    K=10
    types=[]
    for a in range(K+1):
        for b in range(K+1-a):
            x=conv(binom_poly(b),binom_poly(a,2))
            y=shift(binom_poly(a))
            # Independently graph-recount every branch type.
            ed=[]; n=1
            for _ in range(a): ed += [(0,n),(n,n+1)]; n+=2
            for _ in range(b): ed.append((0,n)); n+=1
            adj=graph(n,ed); cnt=deletion_counter(adj)
            assert cnt((1<<n)-1)==add(x,y)
            assert independence_dp(adj,set(range(1,n)))==x
            types.append((a,b,x,add(x,y)))
    assert len(types)==66
    cacheA={():((1,),(1,))}; cacheB={():((1,),(1,))}
    sha=hashlib.sha256(); counts={}; nonLC={}; failed=[]
    for r in range(4):
        counts[str(r)]=0; nonLC[str(r)]={'root_absent':0,'root_present':0}
        for t in combinations_with_replacement(range(len(types)),r):
            if t:
                px,pm=cacheA[t[:-1]]; qx,qm=cacheB[t[:-1]]; _,_,x,m=types[t[-1]]
                pX,pM=conv(px,x),conv(pm,m)
                qX,qM=packed_conv(qx,x),packed_conv(qm,m)
                assert pX==qX and pM==qM, ('multiplication mismatch',t)
            else: pX=pM=qX=qM=(1,)
            if r<3:
                cacheA[t]=(pX,pM); cacheB[t]=(qX,qM)
            present=add(pM,shift(pX)); absent=pM
            assert present==add(qM,shift(qX))
            if not unimodal(present) or not unimodal(absent): failed.append({'types':t,'present':present,'absent':absent})
            nonLC[str(r)]['root_present']+=not logconcave(present)
            nonLC[str(r)]['root_absent']+=not logconcave(absent)
            row=json.dumps([t,absent,present],separators=(',',':')).encode()+b'\n'; sha.update(row)
            counts[str(r)]+=1
    adj=hub_tree([10]*3); record=profile(adj); cnt=deletion_counter(adj); mask=(1<<len(adj))-1
    assert tuple(record['P'])==cnt(mask)
    for rec in record['vertices']:
        v=rec['v']; rest=mask&~(1<<v); closed=rest
        for w in adj[v]: closed &=~(1<<w)
        assert tuple(rec['A'])==cnt(rest)
        assert tuple(rec['B'])==shift(cnt(closed))
    ts=terminal_spiders(adj)
    assert [t['center'] for t in ts]==[1,2,3]
    assert all(record['vertices'][t['center']]['local_gap']==2 for t in ts)
    assert not failed
    record['HEREDITARY']='PROVED_BY_COMPLETE_INDUCED_SUBFOREST_COMPRESSION_AND_EXACT_CHECKS'
    record['terminal_spiders']=ts
    record['role']='COUNTEREXAMPLE_TO_UNLOCALIZED_TERMINAL_CENTER_MODE_ALIGNMENT_ONLY'
    summary={
        'status':'PASS','graph':'H(10,10,10)','n':64,'branch_types':len(types),
        'multiset_states_by_retained_hubs':counts,'total_multiset_states':sum(counts.values()),
        'root_state_polynomials_checked':2*sum(counts.values()),
        'all_compressed_polynomials_unimodal':not failed,'non_log_concave_counts':nonLC,
        'stream_sha256':sha.hexdigest(),
        'graph_polynomials_dual_recounted':1,'all_vertex_A_B_dual_recounted':len(adj)*2,
        'unimodal_original':record['unimodal'],'original_valleys':record['valleys'],
        'U':record['U'],'D':record['D'],'residual_pairs':len(record['residual_pairs']),
        'scope':'One fixed 64-vertex tree and ALL its induced subforests, via proved compression. NOT all forests on <=64 vertices.',
        'algorithms':'Nested-integer convolution versus carry-free integer packing on every compressed state; vertex-deletion recount for original and all vertex conditionals.'
    }
    (BASE/'certificates/hereditary64_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (BASE/'certificates/terminal64_witness.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
