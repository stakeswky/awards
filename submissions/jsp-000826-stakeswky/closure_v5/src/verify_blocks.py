#!/usr/bin/env python3
"""All 59 branches and all 1/2/3-element multisets; two exact algorithms.
No sampling; no external dependencies. LC and finite-order ULC are distinct.
"""
import argparse, hashlib, json, time
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
from polynomials import B, add, binom, branch, mul

def require(p, label):
    if not p:raise AssertionError(label)

def palette_replay():
    ans=[]
    for d in range(1,4):
        for s in combinations_with_replacement(range(2,18),d):
            if d==1:accept=3<=s[0]<=17
            elif d==2:
                a,b=s
                accept=(a==2 and 6<=b<=14) or (a==3 and 5<=b<=13) or \
                    (4<=a<=8 and a<=b<=16-a)
            else:accept=(s==(5,5,5))
            if accept:ans.append(s)
    return ans

def branch_replay(s):
    S=sum(s);q=[0]*(S+1)
    for mask in range(1<<len(s)):
        selected=[j for j in range(len(s)) if mask>>j&1]
        shift=len(selected);free=S-sum(s[j] for j in selected)
        for k in range(free+1):q[k+shift]+=comb(free,k)
    r=[comb(S,k) for k in range(S+1)]
    return add(q,[0]+r),q,r

def packed_mul(a,b):
    # Every product coefficient <= sum(a)*sum(b), so base 2^w admits no carry.
    width=(sum(a)*sum(b)).bit_length()+1
    aa=sum(x<<(width*i) for i,x in enumerate(a))
    bb=sum(x<<(width*i) for i,x in enumerate(b))
    zz=aa*bb;mask=(1<<width)-1
    result=[(zz>>(width*i))&mask for i in range(len(a)+len(b)-1)]
    require(zz>>(width*len(result))==0,'packed degree')
    return result

def lc_margins(f):return [f[k]*f[k]-f[k-1]*f[k+1] for k in range(1,len(f)-1)]
def ulc_margins(f,N):
    return [k*(N-k)*f[k]*f[k]-(k+1)*(N-k+1)*f[k-1]*f[k+1]
            for k in range(1,len(f)-1)]

def run(method):
    start=time.monotonic(); alt=palette_replay()
    require(len(B)==59 and len(set(B))==59 and set(alt)==set(B),'two palettes')
    polynomial_multiply=mul if method=='primary' else packed_mul
    factors=[];branch_checks=0;branch_digest=hashlib.sha256()
    for s in B:
        h,q,r=(branch if method=='primary' else branch_replay)(s)
        S=sum(s);d=len(s)
        require((h,q,r)==branch_replay(s),'star formula/subset equality')
        require(3<=S<=17 and 1<=d<=3 and S>=5*d-2 and S+d<=18,('size',s))
        require(len(h)==S+2 and len(q)==S+1 and h[0]==q[0]==1,('degrees',s))
        require(all(x>0 for x in h+q),('positive support',s))
        require(all(4*r[k]>=3*q[k] for k in range(S+1)),('4R>=3Q',s))
        for name,f in [('H',h),('Q',q)]:
            m=len(f)-1
            for k in range(m+1):
                v=(k+1)*(f[k+1] if k<m else 0)
                require((m-k-1)*f[k]<=v<=(m+d-k)*f[k],('rate',s,name,k))
                branch_checks+=2
            for k in range(1,m):
                require(k*f[k]**2>=(k+1)*f[k-1]*f[k+1],('FLC',s,name,k))
                branch_checks+=1
        branch_digest.update((json.dumps([s,h,q,r],separators=(',',':'))+'\n').encode())
        factors.append((h,q))
    cases={};total_lc=total_ulc=0;dg=hashlib.sha256()
    for t in (1,2,3):
        n=0
        for ids in combinations_with_replacement(range(59),t):
            a=q=[1]
            for idx in ids:
                h,g=factors[idx];a=polynomial_multiply(a,h);q=polynomial_multiply(q,g)
            e=add(a,[0]+q);p=add(polynomial_multiply(a,[1,1]),[0]+q)
            for name,f in [('E',e),('P',p)]:
                m=lc_margins(f);require(all(x>=0 for x in m),('LC',ids,name));total_lc+=len(m)
            if t>=2:
                for name,f in [('A',a),('Q',q)]:
                    N=len(f)-1+3*t
                    m=ulc_margins(f,N);require(all(x>=0 for x in m),('ULC_'+name,ids,N));total_ulc+=len(m)
            dg.update((json.dumps([ids,a,q,e,p],separators=(',',':'))+'\n').encode())
            n+=1
        require(n==comb(58+t,t),('multiset count',t,n))
        cases[str(t)]=n
    return {'status':'EXACT_ALL_PASS','method':method,'palette_size':len(B),'multisets':cases,
            'total_multisets':sum(cases.values()),'block_multisets':cases['2']+cases['3'],
            'branch_rate_and_FLC_checks':branch_checks,'prefix_LC_inequalities':total_lc,
            'block_ULC_inequalities':total_ulc,'canonical_branch_sha256':branch_digest.hexdigest(),
            'canonical_multiset_sha256':dg.hexdigest(),'elapsed_seconds':round(time.monotonic()-start,6)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--method',choices=['primary','replay'],required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();v=run(a.method)
    a.out.write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v),flush=True)
