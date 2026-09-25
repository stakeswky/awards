#!/usr/bin/env python3
"""Semantic and independent small-subset checks; not an all-order census."""
from pathlib import Path
from math import comb
import json
from forest_exact import *
BASE=Path(__file__).resolve().parents[1]

def power(p,k):
    out=(1,)
    for _ in range(k): out=conv(out,p)
    return out

def main():
    controls=[((1,),True),((1,2,2,1),True),((0,1,1,0),True),((1,3,2,2,3),False),((1,3,2,3,1),False)]
    for p,u in controls: assert unimodal(p)==u and bool(valleys(p))==(not u)
    assert valleys((1,3,2,2,3))==[(1,3)]
    illegal=[(2,[(0,0)]),(2,[(0,1),(1,0)]),(3,[(0,1),(1,2),(2,0)]),(2,[(0,2)])]
    for n,ed in illegal:
        try: graph(n,ed)
        except AssertionError: pass
        else: raise AssertionError('accepted invalid forest')
    for n in range(26):
        p=tuple(comb(n-k+1,k) for k in range((n+1)//2+1))
        adj=graph(n,[(i,i+1) for i in range(n-1)])
        assert p==independence_dp(adj)==deletion_counter(adj)((1<<n)-1) and logconcave(p)
    for p in [(1,),(1,2,2,1),(0,1,1),(1,3,7,6,2),(1,5,3,3,3)]:
        for c in [1,2,7]: assert unimodal(conv(p,(1,c)))
    # Every induced subset of the 10-vertex H_1 is independently counted by
    # direct subset enumeration and checked against the exact reduction mapping.
    h=hub_tree([1,1,1]); n=len(h); assert n==10
    es=edges_of(h)
    independent=[all(not ((m>>u&1) and (m>>v&1)) for u,v in es) for m in range(1<<n)]
    counter=deletion_counter(h); checked=0
    for mask in range(1<<n):
        brute=[0]*(n+1); sub=mask
        while True:
            if independent[sub]: brute[sub.bit_count()]+=1
            if sub==0: break
            sub=(sub-1)&mask
        brute=trim(brute)
        pm=px=(1,); iso=edges=0
        for hub in [1,2,3]:
            mid=4+2*(hub-1); end=mid+1
            m=bool(mask>>mid&1); f=bool(mask>>end&1)
            if mask>>hub&1:
                a=int(m and f); b=int(m and not f); iso+=int(f and not m)
                x=conv(power((1,1),b),power((1,2),a))
                M=add(x,shift(power((1,1),a)))
                pm=conv(pm,M); px=conv(px,x)
            elif m and f: edges+=1
            elif m or f: iso+=1
        reduced=add(pm,shift(px)) if mask&1 else pm
        reduced=conv(reduced,conv(power((1,1),iso),power((1,2),edges)))
        assert brute==counter(mask)==reduced==independence_dp(h,[v for v in range(n) if mask>>v&1])
        assert unimodal(brute)
        checked+=1
    # Canonical encodings must distinguish forests, not just root polynomials.
    trees=[graph(5,[(0,1),(1,2),(2,3),(3,4)]),graph(5,[(0,i) for i in range(1,5)])]
    assert canonical(trees[0])!=canonical(trees[1])
    for adj in [h,*trees,union(*trees),graph(0,[])]:
        perm=list(reversed(range(len(adj))))
        relabeled=graph(len(adj),[(perm[u],perm[v]) for u,v in edges_of(adj)])
        assert canonical(adj)==canonical(relabeled)
        assert independence_dp(adj)==independence_dp(relabeled)
    out={'status':'PASS','sequence_controls':len(controls),'invalid_graph_rejections':len(illegal),
         'path_formula_orders_checked':[0,25], 'compression_mapping_all_subsets_H1':checked,
         'compression_mapping_algorithms':'Explicit independent-subset enumeration, deletion recurrence, rooted DP, and mapped reduced polynomial',
         'original_forest_census':False,'finite_UNSAT_used':False}
    (BASE/'certificates/regressions.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
