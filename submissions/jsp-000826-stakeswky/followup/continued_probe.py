#!/usr/bin/env python3
"""Bounded unweighted probes outside the proven palette; exact replay only."""
import argparse
import json
from hashlib import sha256
from pathlib import Path
from branch_study import branch, graph, product, add, mul, packed, canonical, valley, lc, palette
from audit_study import checker, unimodal


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(row):
    return (json.dumps(row,sort_keys=True,separators=(',',':'))+'\n').encode()


def cases():
    pal={tuple([s]*d) for d,s in palette()}
    accepted=0
    for attempt in range(100000):
        h=sha256(('erdos993-outside-palette-v2-'+str(attempt)).encode()).digest()
        arms=[[1+h[(3+5*j+k)%32]%10 for k in range(1+h[(2+4*j)%32]%5)]
              for j in range(2+h[0]%7)]
        p=graph(arms)
        if len(p)>256 or all(tuple(a) in pal for a in arms):
            continue
        yield 'outside-palette',attempt,arms,bool(h[1]%2)
        accepted+=1
        if accepted==128:
            break
    require(accepted==128,'case generation exhausted')
    # Six samples at theorem boundaries; these are controls, not new searches.
    for t in (44,45,46,47,69,70):
        arms=[[3+(i*7)%15] for i in range(t)]
        yield 'threshold-control',t,arms,True


def main(out):
    target=Path(out)
    target.mkdir(parents=True,exist_ok=False)
    shapes=set();total=0;coefs=0;split_coefs=0;non_lc=0;failure=[];stages={}
    for_logging=[]
    with (target/'trials.jsonl').open('wb') as f:
        for index,(kind,seed,arms,leaf) in enumerate(cases(),1):
            base=[branch(a) for a in arms]
            a=product(z[1] for z in base);q=product(z[0] for z in base)
            expected=add(mul([1,1],a),[0]+q) if leaf else add(a,[0]+q)
            original=graph(arms)
            p=original if leaf else [-1]+[v-1 for v in original[2:]]
            actual,_,_=packed(p)
            require(expected==actual,'formula/graph disagreement')
            rec,adj=checker(p);mask=(1<<len(p))-1
            third=rec(mask)
            require(list(third)==actual,'deletion recurrence disagreement')
            require(unimodal(third)==(valley(actual) is None),'unimodality disagreement')
            # Keep failures instead of asserting conjectures about subforests.
            v=1 if leaf else 0
            absent=list(rec(mask&~(1<<v)))
            present=[0]+list(rec(mask&~((1<<v)|adj[v])))
            require(add(absent,present)==actual,'split disagreement')
            conditional=valley(absent) is not None or valley(present) is not None
            row={'index':index,'kind':kind,'case_seed':seed,'root_leaf':leaf,
                 'branches':arms,'parents':p,'coefficients':actual,
                 'valley':valley(actual),'log_concave':lc(actual),
                 'hub':v,'hub_absent':absent,'hub_present':present,
                 'conditional_valley':conditional}
            f.write(encode(row))
            total+=1;coefs+=len(actual);split_coefs+=len(absent)+len(present)
            non_lc+=not lc(actual);shapes.add(canonical(p))
            stats=stages.setdefault(kind,{'records':0,'max_n':0,'min_n':10**9,'counterexamples':0})
            stats['records']+=1;stats['max_n']=max(stats['max_n'],len(p));stats['min_n']=min(stats['min_n'],len(p))
            stats['counterexamples']+=row['valley'] is not None
            if row['valley'] is not None or conditional:failure.append(row)
            if index%32==0:print('verified '+str(index),flush=True)
    summary={'status':'PASS_BOUNDED_STUDY_NO_ORIGINAL_COUNTEREXAMPLE' if not failure else 'WITNESS_REQUIRES_REVIEW',
             'records':total,'within_batch_unlabelled_structures':len(shapes),'by_stage':stages,
             'full_coefficients_compared':coefs,'hub_splits':total,'split_coefficients':split_coefs,
             'non_log_concave_records':non_lc,'witness_records':len(failure),
             'raw_log_sha256':sha256((target/'trials.jsonl').read_bytes()).hexdigest(),
             'scope':'128 bounded probes plus six controls. Formula, graph DP and deletion recurrence compared for every original graph; one hub split rebuilt by deletion per graph. Same-session algorithms, no Lean or third-party review; no across-round novelty claim.'}
    (target/'probe_summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    (target/'witnesses.json').write_text(json.dumps(failure,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True)
    main(ap.parse_args().out)
