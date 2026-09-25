#!/usr/bin/env python3
"""Independent exact deletion recurrence; audits frozen study records.
Only standard library; run without -O. No third-party/Lean verification claim.
"""
import argparse,json
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
if not __debug__:raise SystemExit('Do not use -O.')

def convolution(a,b):
    c=[0]*(len(a)+len(b)-1)
    for k in range(len(c)):
        for i in range(max(0,k-len(b)+1),min(k,len(a)-1)+1):c[k]+=a[i]*b[k-i]
    return tuple(c)

def checker(p):
    if not p or p[0]!=-1 or any(type(p[v]) is not int or not 0<=p[v]<v for v in range(1,len(p))):raise ValueError('invalid tree')
    n=len(p);adj=[0]*n
    for v in range(1,n):adj[v]|=1<<p[v];adj[p[v]]|=1<<v
    def components(mask):
        out=[];left=mask
        while left:
            todo=left & -left;part=0
            while todo:
                bit=todo & -todo;todo^=bit
                if part & bit:continue
                part|=bit;todo|=adj[bit.bit_length()-1]&mask&~part
            out.append(part);left&=~part
        return out
    @lru_cache(None)
    def rec(mask):
        if not mask:return (1,)
        cs=components(mask)
        if len(cs)>1:
            r=(1,)
            for c in cs:r=convolution(r,rec(c))
            return r
        vertices=[v for v in range(n) if mask>>v&1]
        v=max(vertices,key=lambda v:(adj[v]&mask).bit_count())
        a=rec(mask&~(1<<v));b=rec(mask&~((1<<v)|adj[v]))
        result=[0]*max(len(a),len(b)+1)
        for i,x in enumerate(a):result[i]+=x
        for i,x in enumerate(b):result[i+1]+=x
        return tuple(result)
    return rec,adj

def unimodal(a):
    m=max(range(len(a)),key=a.__getitem__)
    return all(a[i]<=a[i+1] for i in range(m)) and all(a[i]>=a[i+1] for i in range(m,len(a)-1))

def main(log,out,stride,start=1,end=None):
    path=Path(log);records=0;coefficients=0;split_coefficients=0;indices=[]
    for line in path.read_text().splitlines():
        row=json.loads(line)
        if row['index']<start or (end is not None and row['index']>end):continue
        if (row['index']-1)%stride and row['kind']!='theorem-regression':continue
        p=[-1,0]
        for leaves in row['branches']:
            u=len(p);p.append(1)
            for s in leaves:
                if type(s) is not int or s<1:raise ValueError('invalid branch')
                w=len(p);p.append(u);p.extend([w]*s)
        assert p==row['parents'] and len(p)==row['n']
        rec,adj=checker(p);mask=(1<<len(p))-1;c=rec(mask)
        assert list(c)==row['coefficients']
        assert unimodal(c)==(row['valley'] is None)
        # Root and hub deletions are reconstructed, not accepted from the formula.
        pairs=[]
        for v in [0,1]:
            a=rec(mask&~(1<<v));b=(0,)+rec(mask&~((1<<v)|adj[v]))
            assert all((a[k] if k<len(a) else 0)+(b[k] if k<len(b) else 0)==c[k] for k in range(len(c)))
            assert unimodal(a) and unimodal(b);pairs.append((a,b));split_coefficients+=len(a)+len(b)
        if row['kind']=='theorem-regression':
            def mode(a):
                m=max(a);i=[k for k,x in enumerate(a) if x==m];return i[0],i[-1]
            U=max(min(mode(a)[1],mode(b)[1]) for a,b in pairs)
            D=min(max(mode(a)[0],mode(b)[0]) for a,b in pairs)
            assert U==row['U'] and D==row['D']
        records+=1;coefficients+=len(c);indices.append(row['index'])
        if records%400==0:print(records,flush=True)
    assert records>0
    result=dict(status='PASS_DELETION_RECURSION',records=records,full_coefficients_compared=coefficients,
        root_hub_splits=2*records,split_coefficients=split_coefficients,stride=stride,
        requested_range=[start,end],log_sha256=sha256(path.read_bytes()).hexdigest(),
        audited_indices=indices,scope='Different algorithm in the same session; not Lean or external peer review.')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='audited_indices'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--log',required=True);p.add_argument('--out',required=True);p.add_argument('--stride',type=int,default=1)
    p.add_argument('--start',type=int,default=1);p.add_argument('--end',type=int)
    a=p.parse_args()
    if a.stride<1:p.error('stride must be positive')
    main(a.log,a.out,a.stride,a.start,a.end)
