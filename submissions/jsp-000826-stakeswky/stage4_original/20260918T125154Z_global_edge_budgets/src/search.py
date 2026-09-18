"""Deterministic actual-tree branch grafting, not a random-tree sweep."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from forest import *
from check import OLD23, edge_checks


def key(g):
    return (g['n'],tuple(tuple(e) for e in g['edges']))


def score(g):
    if not g['LOCAL']:return (10,Fraction(0),Fraction(0),-g['n'])
    sep=[max(a[0]-b[1],b[0]-a[1],0) for a,b in g['mode_intervals']]
    return (g['D']-g['U'],Fraction(len(g['bad_vertices']),g['n']),Fraction(sum(sep),g['n']),-g['n'])


def hubs(a,b,r,s,length):
    n=2+length;edges=[(v,v+1) for v in range(n-1)]
    for hub,cnt,leaves in [(0,a,r),(n-1,b,s)]:
        edges.append((hub,n));n+=1
        for _ in range(cnt):
            z=n;n+=1;edges.append((hub,z))
            for _ in range(leaves):edges.append((z,n));n+=1
    return n,edges


def graft(n,edges,v,shape):
    # Add a new rooted branch through an edge; no identifications or weights.
    if shape==0:branch=[];size=1
    elif shape==1:branch=[(0,1)];size=2
    elif shape==2:branch=[(0,1),(0,2),(0,3)];size=4
    elif shape==3:branch=[(0,1),(1,2),(0,3),(3,4)];size=5
    else:raise ValueError('unknown fixed attachment')
    return n+size,list(edges)+[(v,n)]+[(n+a,n+b) for a,b in branch]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    records=[];cache={};full={};incident=[];stopped=False
    def accept(n,edges,origin):
        nonlocal stopped
        if n>128:return
        edges=sorted(tuple(sorted(e)) for e in edges);ident=(n,tuple(edges))
        if ident in cache:return
        g=describe(n,edges);g['id']='g%04d'%len(records);g['origin']=origin
        assert g['P']==deletion_counter(n,edges)()
        # Every whole sequence is stored, not only maxima or hashes.
        brief={k:v for k,v in g.items() if k not in ['A','B']}
        brief['score']=[str(z) for z in score(g)]
        records.append(brief);cache[ident]=g
        if g['valleys'] or g['residual_pairs'] or not g['LOCAL']:
            checked=edge_checks(n,edges,do_brute=n<=11)
            checked['id']=g['id'];checked['origin']=origin
            incident.append(checked);stopped=True
    for a,b in [(1,1),(1,2),(2,4),(4,1)]:
        for r,s in [(1,3),(3,1),(3,5),(5,3),(5,7),(7,5)]:
            for length in (0,1,2):
                accept(*hubs(a,b,r,s,length),dict(kind='paired_hubs',a=a,b=b,r=r,s=s,length=length))
                if stopped:break
            if stopped:break
        if stopped:break
    if not stopped:
        for u in (0,2,4):
            for v in (0,2,4):
                es=OLD23+[(a+23,b+23) for a,b in OLD23]+[(u,v+23)]
                accept(46,es,dict(kind='join_old23',left_root=u,right_root=v))
                if stopped:break
            if stopped:break
    if not stopped:
        accept(46,OLD23+[(a+23,b+23) for a,b in OLD23],dict(kind='disjoint_old23_pair'))
        accept(23,OLD23,dict(kind='inherited_seed'))
    rounds=[]
    for round_id in range(2):
        if stopped:break
        seeds=sorted(cache.values(),key=score,reverse=True)[:4]
        rounds.append([g['id'] for g in seeds])
        for g in seeds:
            # Farthest separated good vertices first, then vertex id.
            good=[v for v in range(g['n']) if v not in g['bad_vertices']]
            def sep(v):
                a,b=g['mode_intervals'][v];return max(a[0]-b[1],b[0]-a[1],0)
            good=sorted(good,key=lambda v:(-sep(v),v))[:10]
            for v in good:
                for shape in range(4):
                    n,edges=graft(g['n'],g['edges'],v,shape)
                    accept(n,edges,dict(kind='targeted_graft',round=round_id,seed=g['id'],vertex=v,shape=shape))
                    if stopped:break
                if stopped:break
            if stopped:break
    best=sorted(cache.values(),key=score,reverse=True)[:4]
    for g in best:
        checked=edge_checks(g['n'],g['edges'],do_brute=g['n']<=11)
        checked['id']=g['id'];checked['origin']=g['origin'];full[g['id']]=checked
    for g in incident:full[g['id']]=g
    summary=dict(records=len(records),maximum_order=max(g['n'] for g in records),
                 LOCAL_records=sum(g['LOCAL'] for g in records),
                 max_D_minus_U=max(g['D']-g['U'] for g in records if g['LOCAL']),
                 residual_graphs=sum(bool(g['residual_pairs']) for g in records),
                 residual_pairs=sum(len(g['residual_pairs']) for g in records),
                 original_candidates=[g['id'] for g in records if g['valleys']],
                 not_LOCAL=[g['id'] for g in records if not g['LOCAL']],
                 HEREDITARY='UNKNOWN except any small fully checked incident/material records',
                 stopped_on_candidate=stopped,round_seeds=rounds,
                 best=[{k:g[k] for k in ('id','n','U','D','bad_vertices','origin')} for g in best],
                 full_two_algorithm_material=list(full),
                 each_complete_P_recounted=True,exact_edge_list_deduplication=True,
                 unlabeled_isomorphism_deduplication=False,no_random_trees=True,
                 scope='Fixed structural discovery; not a theorem or additional support from vacuous residual tests')
    for name,obj in [('search_records.json',records),('search_material.json',list(full.values())),('search_summary.json',summary)]:
        (out/name).write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
