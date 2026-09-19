#!/usr/bin/env python3
import argparse, itertools, json, random, sys, time
from pathlib import Path
from forest_counts import Forest, analyze, modes, valley, add, pad, interval_distance

SEED = 99320260918

def old_control():
    parent = [-1,0,1,1,3,1,5,0,7,8,7,10,7,12,7,14,0,16,17,16,19,16,21,16,23]
    e = [(parent[v],v) for v in range(1,25)]
    return {'id':'old25','n':25,'edges':e}

def bush(c,m):
    edges=[];n=1
    for _ in range(m):
        b=n;n+=1;edges.append((0,b))
        for _ in range(c):
            a=n;v=n+1;n+=2;edges.extend([(b,a),(a,v)])
    return {'id':f'bush-c{c}-m{m}','n':n,'edges':edges}

def union(name, rows):
    n=0;e=[]
    for row in rows:
        e.extend((n+u,n+v) for u,v in row['edges']);n+=row['n']
    return {'id':name,'n':n,'edges':e}

def inputs():
    old=old_control()
    new={'id':'new30','n':30,'edges':old['edges']+[(2,25),(25,26),(26,27),(26,28),(26,29)]}
    out=[old,new]
    out.extend(bush(c,m) for c in range(1,7) for m in range(1,9))
    rng=random.Random(SEED)
    for t in range(64):
        n=12+t
        e=[]
        for v in range(1,n):
            if t%3==0:p=rng.randrange(v)
            elif t%3==1:p=max(0,v-1-rng.randrange(min(v,5)))
            else:p=rng.randrange(min(v,4)) if rng.randrange(3) else rng.randrange(v)
            e.append((p,v))
        out.append({'id':f'tree-{t}','n':n,'edges':e})
        out.append({'id':f'forest-{t}','n':n,'edges':[x for x in e if rng.randrange(4)]})
    for n in [2,3,4,8,16,32]:
        out.extend([{'id':f'path-{n}','n':n,'edges':[(v-1,v) for v in range(1,n)]},
                    {'id':f'star-{n}','n':n,'edges':[(0,v) for v in range(1,n)]}])
    out.extend([union('old25+new30',[old,new]),union('new30+isolate',[new,{'n':1,'edges':[]}]),
                union('new30+path8',[new,{'n':8,'edges':[(v-1,v) for v in range(1,8)]}])])
    return out

def regressions():
    per_order=[];coefficients=0
    for n in range(6):
        possible=list(itertools.combinations(range(n),2));count=0
        for em in range(1<<len(possible)):
            edges=[e for j,e in enumerate(possible) if em>>j&1]
            try:g=Forest(n,edges)
            except ValueError:continue
            row=analyze({'id':f'regression-{n}-{em}','n':n,'edges':edges},brute=True)
            assert not row['candidates'];count+=1
            coefficients+=(n+1)*(2*n+1)
        per_order.append(count)
    assert per_order==[1,1,2,7,38,291]
    # All nonzero unimodal nonnegative integer sequences of length 4, entries 0..3.
    seqs=[p for p in itertools.product(range(4),repeat=4) if max(p)>0 and valley(p) is None]
    pair_tests=0
    for a in seqs:
        for b in seqs:
            ma,mb=modes(a),modes(b);p=add(a,b)
            u=min(ma[1],mb[1]);d=max(ma[0],mb[0])
            diff=[p[k+1]-p[k] for k in range(3)]
            assert all(diff[k]>=0 for k in range(u))
            assert all(diff[k]<=0 for k in range(d,3))
            if interval_distance(ma,mb)<=1 or d<=u+1:
                assert valley(p) is None
            pair_tests+=1
    return {'labeled_forests_per_order':per_order,'labeled_forests_total':sum(per_order),
            'all_graph_whole_and_2n_deletions_dp_recursion_and_bruteforce':True,
            'unimodal_sequence_pair_tests':pair_tests,'stored_padded_coefficient_slots':coefficients}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--inputs',type=Path,required=True);parser.add_argument('--generate',action='store_true')
    a=parser.parse_args();start=time.monotonic();summary={'python':sys.version,'seed':SEED}
    if a.generate:a.inputs.write_text(json.dumps(inputs(),indent=2)+'\n')
    records=json.loads(a.inputs.read_text());summary['regressions']=regressions()
    results=[];excluded=[]
    for idx,row in enumerate(records):
        if time.monotonic()-start>120:
            excluded.extend({'id':r['id'],'reason':'total budget exhausted'} for r in records[idx:]);break
        t0=time.monotonic()
        def check():
            if time.monotonic()-t0>10:raise TimeoutError('per-graph 10 second budget')
            if time.monotonic()-start>120:raise TimeoutError('total 120 second budget')
        try:r=analyze(row,checkpoint=check)
        except TimeoutError as e:
            excluded.append({'id':row['id'],'reason':str(e)});continue
        results.append(r)
        if r['candidates']:
            print('ORIGINAL CANDIDATE',row['id'],flush=True)
            excluded.extend({'id':x['id'],'reason':'candidate stop'} for x in records[idx+1:]);break
        if idx%20==0:print('completed',idx+1,'last',row['id'],'U,D',r.get('U'),r.get('D'),flush=True)
    summary.update({'input_records':len(records),'completed':len(results),'excluded':excluded,
                    'original_candidates':[r['id'] for r in results if r['candidates']],
                    'single_vertex_failures':[r['id'] for r in results if r['n'] and not r.get('good_vertices')],
                    'joint_failures':[r['id'] for r in results if r['n'] and not r.get('joint_condition')],
                    'max_D_minus_U':max(r['D']-r['U'] for r in results if 'D' in r),
                    'all_split_polynomials_recomputed':sum(2*r['n']+1 for r in results),
                    'elapsed_seconds':round(time.monotonic()-start,6)})
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'diagnostics.json').write_text(json.dumps(results,indent=2)+'\n')
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)
    assert len(results)>0
    byid={r['id']:r for r in results}
    if 'new30' in byid:
        p=byid['new30']['counts'];assert p[16]**2-p[15]*p[17]==-219 and byid['new30']['unimodal']
if __name__=='__main__':main()
