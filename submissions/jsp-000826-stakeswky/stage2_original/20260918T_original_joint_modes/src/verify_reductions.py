#!/usr/bin/env python3
"""Finite regression of proved reductions; not a proof of the forest conjecture."""
import argparse
import itertools
import json
from pathlib import Path
from forest_counts import Forest,add,convolution,pad,valley,modes,interval_distance
from verify_material import minor


def delta(a,k):
    return (a[k+1] if k+1<len(a) else 0)-(a[k] if 0<=k<len(a) else 0)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--material',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    seqs=[p for p in itertools.product(range(4),repeat=4)
          if max(p)>0 and valley(p) is None]
    groups={};polarized_pairs=0;weighted=0
    for a in seqs:
        for c in [1,2,3]:
            p=convolution((1,c),a)
            assert valley(p) is None
            weighted+=1
        assert interval_distance(modes(convolution((1,1),a)),modes((0,)+a))<=1
        for b in seqs:
            p=add(a,b);am,bm=modes(a),modes(b)
            groups.setdefault(p,[]).append((min(am[1],bm[1]),max(am[0],bm[0])))
            for i in range(3):
                for j in range(i+1,3):
                    if not (delta(p,i)<0<delta(p,j)):
                        continue
                    e,l=(a,b) if delta(a,i)<0 else (b,a)
                    assert delta(e,i)<0 and delta(e,j)<=0
                    assert delta(l,i)>=0 and delta(l,j)>0
                    assert modes(e)[1]<=i and modes(l)[0]>=j+1
                    assert minor(e,l,i,j)<0
                    polarized_pairs+=1
    overlap=adjacent=unresolved=0
    for p,decompositions in groups.items():
        u=max(x[0] for x in decompositions);d=min(x[1] for x in decompositions)
        assert all(delta(p,k)>=0 for k in range(u))
        assert all(delta(p,k)<=0 for k in range(d,3))
        if d<=u+1:
            assert valley(p) is None
        if d<=u:overlap+=1
        elif d==u+1:adjacent+=1
        else:unresolved+=1
    assert polarized_pairs>0 and overlap>0 and adjacent>0
    rows=json.loads(args.material.read_text())['graph_witnesses']
    leaf_records=[]
    for row in rows:
        g=Forest(row['n'],row['edges']);n=g.n
        for leaf in range(n):
            if g.adj[leaf].bit_count()!=1:continue
            w=g.adj[leaf].bit_length()-1
            cm=g.full&~((1<<leaf)|(1<<w))
            hm=g.full&~((1<<w)|g.adj[w])
            c=g.recount(cm);h=g.recount(hm)
            av,bv=row['vertices'][leaf],row['vertices'][w]
            assert pad(add(c,(0,)+h),n)==tuple(av['A'])
            assert pad((0,)+c,n)==tuple(av['B'])
            assert pad(convolution((1,1),c),n)==tuple(bv['A'])
            assert pad((0,)+h,n)==tuple(bv['B'])
            assert interval_distance(modes(bv['A']),modes(av['B']))<=1
            leaf_records.append({'graph':row['id'],'leaf':leaf,'support':w,'C':c,'H':h})
    rejected=0
    for n,edges in [(1,[(0,0)]),(2,[(0,1),(1,0)]),(3,[(0,1),(1,2),(2,0)]),(2,[(0,2)])]:
        try:Forest(n,edges)
        except ValueError:rejected+=1
        else:raise AssertionError('invalid graph accepted')
    result={'status':'PASS_WITH_SCOPE','unimodal_sequences':len(seqs),
            'weighted_linear_factor_controls':weighted,'common_sum_groups':len(groups),
            'joint_overlap_groups':overlap,'joint_adjacent_groups':adjacent,
            'joint_unresolved_groups':unresolved,'abstract_valley_pairs_checked':polarized_pairs,
            'material_leaf_identities':len(leaf_records),'leaf_records':leaf_records,
            'invalid_graph_controls_rejected':rejected,
            'original_structural_bridge_proved':False,
            'scope':'Finite regression, with nonvacuous abstract valleys; no residual RSM forest case.'}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='leaf_records'},indent=2))

if __name__=='__main__':main()
