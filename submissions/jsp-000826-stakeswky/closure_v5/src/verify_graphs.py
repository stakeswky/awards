#!/usr/bin/env python3
"""Bounded original-problem checks and graph semantics controls.
Inputs stored verbatim. Replay and both counting algorithms are standard-library only.
Rooted forest DP is compared with deletion/closed-neighborhood recursion; the latter
splits disconnected induced subgraphs and uses isolated-vertex binomials.
"""
import argparse, functools, hashlib, json, random, time
from math import comb
from pathlib import Path
from polynomials import mul,add,family,B

def validate(n,edges):
    parent=list(range(n));adj=[0]*n;seen=set()
    def root(v):
        while parent[v]!=v:v=parent[v]
        return v
    for a,b in edges:
        if not (0<=a<n and 0<=b<n and a!=b):raise ValueError('bad edge')
        key=tuple(sorted((a,b)))
        if key in seen:raise ValueError('duplicate edge')
        seen.add(key);ra,rb=root(a),root(b)
        if ra==rb:raise ValueError('cycle')
        parent[ra]=rb;adj[a]|=1<<b;adj[b]|=1<<a
    return adj

def bits(mask):
    while mask:
        low=mask&-mask;yield low.bit_length()-1;mask-=low

def counter(n,edges):
    adj=validate(n,edges)
    @functools.lru_cache(None)
    def deletion(mask):
        if not mask:return (1,)
        v=max(bits(mask),key=lambda j:(adj[j]&mask).bit_count())
        if not (adj[v]&mask):return tuple(comb(mask.bit_count(),k) for k in range(mask.bit_count()+1))
        # Connected components of the induced subgraph, without assuming input connected.
        todo=mask;comps=[]
        while todo:
            frontier=todo&-todo;comp=0
            while frontier:
                comp|=frontier;nexts=0
                for u in bits(frontier):nexts|=adj[u]
                frontier=nexts&todo&~comp
            comps.append(comp);todo&=~comp
        if len(comps)>1:
            p=[1]
            for c in comps:p=mul(p,deletion(c))
            return tuple(p)
        return tuple(add(deletion(mask&~(1<<v)),[0]+list(deletion(mask&~((1<<v)|adj[v])))))
    def dp(mask):
        used=0;answer=[1]
        def visit(v,parent):
            nonlocal used
            used|=1<<v;absent=[1];present=[0,1]
            for w in bits(adj[v]&mask):
                if w==parent:continue
                no,yes=visit(w,v);absent=mul(absent,add(no,yes));present=mul(present,no)
            return absent,present
        for v in bits(mask):
            if not (used>>v&1):
                no,yes=visit(v,-1);answer=mul(answer,add(no,yes))
        return answer
    return adj,deletion,dp

def valley(p):
    first=None
    for k in range(len(p)-1):
        if p[k]>p[k+1] and first is None:first=k
        if p[k]<p[k+1] and first is not None:return [first,k]
    return None

def brute(n,edges):
    p=[0]*(n+1)
    for mask in range(1<<n):
        if all(not(mask>>a&1 and mask>>b&1) for a,b in edges):p[mask.bit_count()]+=1
    while len(p)>1 and p[-1]==0:p.pop()
    return p

def family_graph(sigma):
    edges=[(0,1)];n=2
    for s in sigma:
        u=n;n+=1;edges.append((1,u))
        for size in s:
            c=n;n+=1;edges.append((u,c))
            for _ in range(size):edges.append((c,n));n+=1
    return n,edges

def generated_inputs():
    rng=random.Random(20260918);records=[]
    # Explicit controls include the empty forest and disconnected independent vertices.
    records += [{'kind':'empty','n':0,'edges':[]},{'kind':'isolates','n':12,'edges':[]}]
    for n in range(2,17):
        records.append({'kind':'path','n':n,'edges':[(i-1,i) for i in range(1,n)]})
        records.append({'kind':'star','n':n,'edges':[(0,i) for i in range(1,n)]})
    for i in range(96):
        n=8+i%57
        # Recursive trees deliberately alternate parent-selection mechanisms.
        edges=[]
        for v in range(1,n):
            if i%3==0:p=rng.randrange(v)
            elif i%3==1:p=max(0,v-1-rng.randrange(min(v,5)))
            else:p=rng.randrange(min(v,4)) if rng.randrange(3) else rng.randrange(v)
            edges.append((p,v))
        records.append({'kind':'general_tree','n':n,'edges':edges})
        if i%2==0:
            records.append({'kind':'general_forest','n':n,
                            'edges':[e for e in edges if rng.randrange(4)]})
    return records

def main(inputs,out,generate):
    start=time.monotonic()
    if generate:inputs.write_text(json.dumps(generated_inputs(),indent=2)+'\n')
    records=json.loads(inputs.read_text());checked=0;counts=0;conditional=0;brutes=0
    digest=hashlib.sha256();candidates=[]
    for idx,row in enumerate(records):
        n=row['n'];edges=row['edges'];adj,rec,dp=counter(n,edges);mask=(1<<n)-1
        masks=[('whole',mask)]
        for v in range(n):masks += [(f'delete-{v}',mask&~(1<<v)),(f'closed-{v}',mask&~((1<<v)|adj[v]))]
        for label,m in masks:
            a=list(rec(m));b=dp(m)
            if a!=b:raise AssertionError(('graph counts',idx,label))
            counts+=len(a);checked+=1;conditional+=label!='whole'
            failure=valley(a)
            if failure:
                vertices=list(bits(m));index={v:j for j,v in enumerate(vertices)}
                small_edges=[[index[u],index[v]] for u,v in edges if u in index and v in index]
                candidates.append({'source':idx,'condition':label,'n':len(vertices),
                                   'edges':small_edges,'coefficients':a,'descent_ascent':failure})
            digest.update((json.dumps([idx,label,a],separators=(',',':'))+'\n').encode())
        if n<=12:
            if brute(n,edges)!=dp(mask):raise AssertionError(('brute',idx))
            brutes+=1
    # Actual graph/product correspondence controls on all 59 individual branches,
    # plus mixed cases in each parameter zone; not called exhaustive graph replay.
    controls=[[s] for s in B]+[[B[i%59] for i in range(t)] for t in (2,3,4,9,23,24,25)]
    graph_product=0
    for sigma in controls:
        n,edges=family_graph(sigma);adj,rec,dp=counter(n,edges);a,q,e,p=family(sigma)
        full=(1<<n)-1
        if dp(full)!=p or list(rec(full))!=p:raise AssertionError('P graph bridge control')
        if dp(full&~1)!=e or list(rec(full&~1))!=e:raise AssertionError('E graph bridge control')
        graph_product+=2
    # v4 negative control: not a member of the restricted product family.
    parent=[-1,0,1,1,3,1,5,0,7,8,7,10,7,12,7,14,0,16,17,16,19,16,21,16,23]
    old_edges=[(parent[v],v) for v in range(1,25)];new_edges=old_edges+[(2,25),(25,26),(26,27),(26,28),(26,29)]
    old_adj,old_rec,old_dp=counter(25,old_edges);old_mask=(1<<25)-1
    old_a=old_dp(old_mask&~(1<<2));old_q=old_dp(old_mask&~((1<<2)|old_adj[2]))
    if old_a!=list(old_rec(old_mask&~(1<<2))) or old_q!=list(old_rec(old_mask&~((1<<2)|old_adj[2]))):
        raise AssertionError('v4 input split counts')
    if old_a[13]!=1 or old_q[12]!=4 or 4*old_a[13]>=3*old_q[12]:
        raise AssertionError('v4 product-bound separation')
    aj,rec,dp=counter(30,new_edges);whole=(1<<30)-1;p=dp(whole)
    if p!=list(rec(whole)):raise AssertionError('v4 whole')
    a=dp(whole&~(1<<2));q=dp(whole&~((1<<2)|aj[2]));b=[0]+q
    if add(a,b)!=p or p[16]**2-p[15]*p[17]!=-219 or valley(p) is not None:
        raise AssertionError('v4 control')
    v4={'old_n':25,'old_edges':old_edges,'old_split_a':old_a,'old_split_q':old_q,'n':30,'edges':new_edges,'coefficients':p,'k':16,'LC_margin':-219,'unimodal':True,
        'split_a_at_15_16_17':[a[k] if k<len(a) else 0 for k in (15,16,17)],
        'split_b_at_15_16_17':[b[k] if k<len(b) else 0 for k in (15,16,17)],
        'scope':'Outside B59; disproves broad shape-only LC insertion, not FAMILY or ORIGINAL.'}
    result={'status':'EXACT_CHECKS_COMPLETED','seed':20260918,'input_records':len(records),
            'whole_and_conditional_forests_checked':checked,'conditional_checks':conditional,
            'coefficient_comparisons':counts,'bruteforce_whole_graph_controls':brutes,
            'family_graph_product_comparisons':graph_product,'family_control_mixtures':len(controls),
            'counts_sha256':digest.hexdigest(),'original_counterexamples':candidates,'v4':v4,
            'elapsed_seconds':round(time.monotonic()-start,6)}
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('v4','original_counterexamples')}),flush=True)
    print('original_counterexamples',len(candidates),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--generate',action='store_true');a=p.parse_args();main(a.inputs,a.out,a.generate)
