#!/usr/bin/env python3
"""Independent all-subset signature distribution and three-algorithm regression."""
import argparse
from collections import Counter
import json
from pathlib import Path
from forest_counts import Forest, vertices, valley, modes
from hereditary import all_signatures
from edge_diagnostics import Table


def explicit_signature(g, mask, parent):
    """Construct each induced component directly; no aggregation recursion."""
    children=[[] for _ in range(g.n)]
    roots=[]
    for v in vertices(mask):
        if parent[v] < 0 or not (mask >> parent[v] & 1):
            roots.append(v)
        else:
            children[parent[v]].append(v)
    def visit(v):
        return tuple(sorted(visit(w) for w in children[v]))
    return tuple(sorted(visit(v) for v in roots))


def original_parents(g):
    parent=[-2]*g.n
    for v in range(g.n):
        if parent[v] != -2:
            continue
        parent[v]=-1
        stack=[v]
        while stack:
            w=stack.pop()
            for u in vertices(g.adj[w]):
                if parent[u] == -2:
                    parent[u]=w
                    stack.append(u)
    return parent


def run(row):
    g=Forest(row['n'],row['edges'])
    compressed,_=all_signatures(g,lambda:None)
    parent=original_parents(g)
    direct=Counter();by_signature={};masks=[];table=Table()
    for mask in range(1<<g.n):
        sig=explicit_signature(g,mask,parent)
        direct[sig]+=1
        p=g.recount(mask,brute=True)
        if sig in by_signature:
            assert by_signature[sig]==p
        else:
            by_signature[sig]=p
        masks.append({'mask':mask,'poly':table.put(p)})
    assert direct==Counter({sig:cnt for sig,(cnt,_) in compressed.items()})
    for sig,(_,witness) in compressed.items():
        assert explicit_signature(g,witness,parent)==sig
    g._deletion.cache_clear()
    return {**row,'status':'PASS','subsets':1<<g.n,'signatures':len(direct),
            'polynomials':table.values,'masks':masks,
            'algorithms':'Explicit enumeration of EVERY vertex subset; DP, independent vertex-deletion, and independent-set enumeration for every mask'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    rows=[r for r in json.loads(args.inputs.read_text()) if r['n']<=12]
    regressions=[{'id':'regression-empty','n':0,'edges':[]},
      {'id':'regression-isolates3','n':3,'edges':[]},
      {'id':'regression-K2','n':2,'edges':[(0,1)]},
      {'id':'regression-P3','n':3,'edges':[(0,1),(1,2)]},
      {'id':'regression-P4+P3','n':7,'edges':[(0,1),(1,2),(2,3),(4,5),(5,6)]}]
    results=[run(r) for r in rows+regressions]
    invalid=[(2,[(0,0)]),(2,[(0,1),(1,0)]),(3,[(0,1),(1,2),(2,0)]),(2,[(0,2)]),(-1,[])]
    for n,edges in invalid:
        try:
            Forest(n,edges)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid graph accepted')
    seqs=[((1,),None,(0,0)),((1,2,2,1,0),None,(1,2)),
          ((0,1,1,0),None,(1,2)),((1,3,2,2,3,0),(1,3),None)]
    for p,witness,mode in seqs:
        assert valley(p)==witness
        if mode is not None:
            assert modes(p)==mode
    summary={'status':'PASS','original_batch_graphs':len(rows),
      'extra_regression_graphs':len(regressions),'all_subsets_checked':sum(r['subsets'] for r in results),
      'entire_signature_distributions_equal':True,'entire_coefficients_equal_three_algorithms':True,
      'invalid_graphs_rejected':len(invalid),'plateau_and_shift_controls':len(seqs),
      'global_minimality_claim':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'coverage_regression_material.json').write_text(json.dumps(results,separators=(',',':'))+'\n')
    (args.out/'coverage_regression_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
