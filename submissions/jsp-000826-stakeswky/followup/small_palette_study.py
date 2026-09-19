#!/usr/bin/env python3
"""Complete palette multiset checks at t=1..4, plus bounded direct probes.
Every main graph is reconstructed and checked by three counting routes.
No statement about unrestricted trees or higher unenumerated multisets.
"""
import argparse
import json
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
from branch_study import add, mul, product, branch, graph, packed, palette, lc, valley, modes, canonical
from audit_study import checker, unimodal
from stability_certificate import require, encode


@lru_cache(None)
def branch_polynomials(leaves):
    return branch(list(leaves))


def cases():
    pal=palette()
    for t in range(1,5):
        for ids in combinations_with_replacement(range(21),t):
            arms=[[pal[i][1]]*pal[i][0] for i in ids]
            yield 'palette-complete',list(ids),arms,True
    allowed={tuple([s]*d) for d,s in pal}
    accepted=0
    for attempt in range(100000):
        h=sha256(('erdos993-stability-direct-v1-'+str(attempt)).encode()).digest()
        t=2+h[0]%9
        arms=[[1+h[(3+5*j+k)%32]%12 for k in range(1+h[(2+4*j)%32]%6)]
              for j in range(t)]
        if len(graph(arms))>256 or all(tuple(a) in allowed for a in arms):
            continue
        yield 'outside-palette-probe',attempt,arms,bool(h[1]%2)
        accepted+=1
        if accepted==256:
            break
    require(accepted==256,'probe generator exhausted')
    yield 'known-non-LC-control',0,[[1]*3,[1]*4,[1]*4],False
    for t in (23,24,25):
        arms=[[pal[(7*i+3)%21][1]]*pal[(7*i+3)%21][0] for i in range(t)]
        yield 'threshold-control',t,arms,True


def formulas(arms, leaf):
    polys=[branch_polynomials(tuple(x)) for x in arms]
    a=product(z[1] for z in polys);q=product(z[0] for z in polys)
    b=[0]+q;E=add(a,b);C=mul([1,1],a)
    P=add(C,b) if leaf else E
    p=graph(arms)
    if not leaf:
        p=[-1]+[v-1 for v in p[2:]]
    return p,P,[(E,[0]+a),(C,b)] if leaf else [(a,b)]


def audit_graph(p, expected, pairs):
    # Both root states of the expanded-tree DP are checked, not just totals.
    actual,absent,present=packed(p)
    require(actual==expected,'formula / packed DP disagree')
    require((absent,present)==pairs[0],'root state formula disagrees')
    rec,adj=checker(p);mask=(1<<len(p))-1
    direct=list(rec(mask))
    require(direct==expected,'deletion recurrence disagrees')
    require(unimodal(direct)==(valley(expected) is None),'valley check disagrees')
    conditional_witnesses=[];counts=0
    for v,(A,B) in enumerate(pairs):
        A2=list(rec(mask&~(1<<v)))
        B2=[0]+list(rec(mask&~((1<<v)|adj[v])))
        require(A2==A and B2==B,'independent split coefficient mismatch')
        require(add(A2,B2)==expected,'split identity failed')
        counts+=len(A2)+len(B2)
        for name,poly,deleted in [('absent',A2,[v]),('present',B2,[v]+[w for w in range(len(p)) if adj[v]>>w&1])]:
            if not unimodal(poly):
                conditional_witnesses.append({'vertex':v,'state':name,
                    'deleted_vertices':deleted,'coefficients':poly,'valley':valley(poly)})
    good=[(A,B) for A,B in pairs if unimodal(A) and unimodal(B)]
    U=max((min(modes(A)[1],modes(B)[1]) for A,B in good),default=None)
    D=min((max(modes(A)[0],modes(B)[0]) for A,B in good),default=None)
    return counts,conditional_witnesses,U,D


def main(out,start,end):
    target=Path(out);target.mkdir(parents=True,exist_ok=False)
    stats={};shapes=set();witnesses=[];coefs=0;splitcoefs=0;splitcount=0;nrows=0
    with (target/'trials.jsonl').open('wb') as f:
        for index,(kind,identity,arms,leaf) in enumerate(cases(),1):
            if index<start:continue
            if end is not None and index>end:break
            p,P,pairs=formulas(arms,leaf)
            count,conditional,U,D=audit_graph(p,P,pairs)
            row={'index':index,'kind':kind,'case_identity':identity,'branches':arms,
                 'root_leaf':leaf,'parents':p,'coefficients':P,
                 'valley':valley(P),'log_concave':lc(P),
                 'E_log_concave':lc(pairs[0][0]) if leaf else lc(P),
                 'split_scope':'root-and-hub' if leaf else 'hub-only',
                 'all_selected_parts_unimodal':not conditional,'U':U,'D':D}
            f.write(encode(row));nrows+=1;coefs+=len(P);splitcoefs+=count;splitcount+=len(pairs)
            shapes.add(canonical(p))
            key='palette-t'+str(len(arms)) if kind=='palette-complete' else kind
            st=stats.setdefault(key,{'records':0,'min_n':10**9,'max_n':0,'not_LC':0,
                                    'E_not_LC':0,'original_valleys':0,'conditional_witness_records':0,
                                    'max_root_hub_corridor':-10})
            st['records']+=1;st['min_n']=min(st['min_n'],len(p));st['max_n']=max(st['max_n'],len(p))
            st['not_LC']+=not row['log_concave'];st['E_not_LC']+=not row['E_log_concave']
            st['original_valleys']+=row['valley'] is not None
            st['conditional_witness_records']+=bool(conditional)
            if U is not None:st['max_root_hub_corridor']=max(st['max_root_hub_corridor'],D-U)
            if row['valley'] is not None or conditional:
                witnesses.append({'record':row,'conditional_witnesses':conditional})
            if nrows%500==0:print('verified',index,flush=True)
    require(nrows>0,'empty study is not a passing study')
    summary={'status':'PASS_THREE_COUNTING_ROUTES' if not witnesses else 'WITNESS_REQUIRES_REVIEW',
             'requested_range':[start,end],'actual_records':nrows,'by_stage':stats,
             'within_batch_unlabelled_shapes':len(shapes),'full_coefficients_compared':coefs,
             'independently_rebuilt_splits':splitcount,'split_coefficients_compared':splitcoefs,
             'witness_records':len(witnesses),'raw_log_sha256':sha256((target/'trials.jsonl').read_bytes()).hexdigest(),
             'independence':'Formula list convolution versus expanded-tree packed DP versus general-graph deletion recurrence; same research process, not external review or Lean.',
             'scope':'Palette t=1..4 is an explicit complete finite parameter range only if all indices 1..12649 are present. 256 outside probes and four controls are separate. No global-new-shape or whole-tree-size coverage claim.'}
    for name,data in [('summary',summary),('witnesses',witnesses)]:
        (target/(name+'.json')).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))


def recursive_ids(t,lower=0):
    """Independent coverage enumerator, not itertools.combinations."""
    if t==0:
        yield []
    else:
        for value in range(lower,21):
            for rest in recursive_ids(t-1,value):yield [value]+rest


def audit_coverage(log):
    expected=(ids for t in range(1,5) for ids in recursive_ids(t))
    tallies=Counter();total=0
    with Path(log).open() as f:
        for index,line in enumerate(f,1):
            row=json.loads(line);require(row['index']==index,'missing or repeated index')
            if row['kind']=='palette-complete':
                require(row['case_identity']==next(expected,None),'palette coverage mismatch')
                tallies[len(row['case_identity'])]+=1
            total=index
    require(next(expected,None) is None,'palette incomplete')
    require(dict(tallies)=={t:comb(20+t,t) for t in range(1,5)},'wrong palette counts')
    require(total==12909,'not the complete frozen study')
    return {'status':'PASS_COMPLETE_PARAMETER_COVERAGE','palette_counts':dict(tallies),
            'palette_total':sum(tallies.values()),'records':total,
            'rechecked_prior_t2_t3_parameter_choices':2002,
            't1_and_t4_parameter_choices':10647}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--out');ap.add_argument('--start',type=int,default=1);ap.add_argument('--end',type=int)
    ap.add_argument('--coverage')
    args=ap.parse_args()
    if args.coverage:
        print(json.dumps(audit_coverage(args.coverage),indent=2,sort_keys=True))
    else:
        require(args.out and args.start>=1 and (args.end is None or args.end>=args.start),'invalid range')
        main(args.out,args.start,args.end)
