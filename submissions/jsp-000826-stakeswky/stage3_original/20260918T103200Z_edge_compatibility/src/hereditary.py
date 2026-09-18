#!/usr/bin/env python3
"""Complete induced-subset coverage via rooted forest signatures, not LOCAL."""
import argparse
import json
import time
from pathlib import Path
from forest_counts import Forest, vertices, valley
from edge_diagnostics import Table, component


def merged(a,b):
    return tuple(sorted(a+b))


def all_signatures(g, checkpoint, cap=100000):
    def add(dst,key,count,mask):
        if key in dst:
            old,witness=dst[key]
            dst[key]=(old+count,witness)
        else:
            dst[key]=(count,mask)
        if len(dst)>cap:
            raise TimeoutError('100000-signature limit')

    node_stats=[]
    def visit(v,parent):
        absent={(): (1,0)}
        present={((),()): (1,1<<v)}
        subtree_size=1
        for w in vertices(g.adj[v]):
            if w==parent:
                continue
            ca,cp,cs=visit(w,v)
            subtree_size+=cs
            choices=[]
            for forest,(cnt,mask) in ca.items():
                choices.append((None,forest,cnt,mask))
            for (tree,others),(cnt,mask) in cp.items():
                choices.append((tree,others,cnt,mask))
            aa={};pp={}
            for forest,(cnt,mask) in absent.items():
                checkpoint()
                for tree,others,cnt2,mask2 in choices:
                    all_components=others if tree is None else merged((tree,),others)
                    add(aa,merged(forest,all_components),cnt*cnt2,mask|mask2)
            for (children,others),(cnt,mask) in present.items():
                checkpoint()
                for tree,others2,cnt2,mask2 in choices:
                    key=(children,merged(others,others2)) if tree is None else (merged(children,(tree,)),merged(others,others2))
                    add(pp,key,cnt*cnt2,mask|mask2)
            absent,present=aa,pp
            if len(absent)+len(present)>cap:
                raise TimeoutError('100000 combined signature limit')
        assert sum(c for c,_ in absent.values()) == 2**(subtree_size-1)
        assert sum(c for c,_ in present.values()) == 2**(subtree_size-1)
        node_stats.append({'vertex':v,'subtree_order':subtree_size,'absent_signatures':len(absent),
                           'present_signatures':len(present),
                           'absent_subsets':sum(c for c,_ in absent.values()),
                           'present_subsets':sum(c for c,_ in present.values())})
        return absent,present,subtree_size

    result={(): (1,0)};remaining=g.full
    while remaining:
        v=next(vertices(remaining))
        ca,cp,_=visit(v,-1)
        choices=[]
        for sig,(cnt,mask) in ca.items():
            choices.append((sig,cnt,mask))
        for (tree,others),(cnt,mask) in cp.items():
            choices.append((merged((tree,),others),cnt,mask))
        new={}
        for forest,(cnt,mask) in result.items():
            checkpoint()
            for sig,cnt2,mask2 in choices:
                add(new,merged(forest,sig),cnt*cnt2,mask|mask2)
        result=new
        remaining &= ~component(g,v)
    assert sum(c for c,_ in result.values()) == 2**g.n
    return result,node_stats


def realize(signature):
    edges=[];n=0
    def tree(children):
        nonlocal n
        v=n;n+=1
        for sub in children:
            w=tree(sub);edges.append((v,w))
        return v
    for root in signature:
        tree(root)
    return n,edges


def audit(row):
    start=time.monotonic()
    def check():
        if time.monotonic()-start>30:
            raise TimeoutError('30-second hereditary limit')
    g=Forest(row['n'],row['edges'],check)
    table=Table()
    signatures,stats=all_signatures(g,check)
    records=[];bad=[];proper_subsets=0;proper_signatures=0
    for idx,(sig,(multiplicity,mask)) in enumerate(sorted(signatures.items())):
        check()
        n,edges=realize(sig)
        assert n==mask.bit_count()
        # Reconstruct the canonical forest as well as counting an actual subset witness.
        h=Forest(n,edges,check)
        p=h.recount(h.full,brute=(g.n<=7))
        q=g.recount(mask,brute=(g.n<=7))
        assert p==q
        h._deletion.cache_clear()
        is_proper=n<g.n
        if is_proper:
            proper_subsets+=multiplicity
            proper_signatures+=1
            if valley(p) is not None:
                bad.append({'mask':mask,'counts':p,'valley':valley(p)})
        records.append({'signature':sig,'multiplicity':multiplicity,
                        'witness_mask':mask,'counts':table.put(p),'proper':is_proper})
    assert proper_subsets==2**g.n-1
    g._deletion.cache_clear()
    return {'id':row['id'],'n':g.n,'edges':g.edges,'status':'VERIFIED' if not bad else 'REFUTED',
            'proper_subsets_covered':proper_subsets,'proper_signatures':proper_signatures,
            'total_signatures':len(records),'node_stats':stats,'records':records,
            'polynomials':table.values,'candidates':bad,
            'coverage':'All vertex subsets, exact multiplicity-preserving rooted-signature recursion; no smaller non-induced graph claim',
            'algorithms':'DP and deletion on every canonical signature and its original-subset witness; brute also when original n<=7'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    rows=json.loads(args.inputs.read_text())
    chosen=[r for r in rows if r['n']<=12 or r['id']=='tree-11']
    results=[];excluded=[]
    for index,row in enumerate(chosen):
        try:
            r=audit(row)
        except TimeoutError as exc:
            excluded.append({'id':row['id'],'status':'UNKNOWN','reason':str(exc)})
            print('UNKNOWN',row['id'],str(exc),flush=True)
            continue
        results.append(r)
        print('HEREDITARY',r['id'],r['status'],'proper subsets',r['proper_subsets_covered'],
              'signatures',r['proper_signatures'],flush=True)
        if r['candidates']:
            excluded.extend({'id':x['id'],'status':'NOT_RUN','reason':'ORIGINAL-candidate stop'}
                            for x in chosen[index+1:])
            break
    summary={'requested_graphs':len(chosen),'completed_graphs':len(results),'excluded':excluded,
             'HEREDITARY_verified_graphs':[r['id'] for r in results if r['status']=='VERIFIED'],
             'proper_subset_occurrences':sum(r['proper_subsets_covered'] for r in results),
             'proper_signature_occurrences':sum(r['proper_signatures'] for r in results),
             'candidates':[r['id'] for r in results if r['candidates']],
             'global_minimality_verified':False,'finite_coverage_only':True}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'hereditary_material.json').write_text(json.dumps(results,separators=(',',':'))+'\n')
    (args.out/'hereditary_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
    main()
