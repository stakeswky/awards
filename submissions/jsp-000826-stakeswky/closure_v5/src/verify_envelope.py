#!/usr/bin/env python3
"""Exhaustive rational certificate, not sampling. Python 3.10+, no third-party libraries.
Primary uses Fraction recurrence. Replay uses integer common denominators and
independently expanded square comparisons. No float enters any acceptance test.
"""
import argparse, hashlib, json, time
from fractions import Fraction as F
from math import comb, prod
from pathlib import Path

def lower_primary(t, s, d, j):
    term = F(3*t,4)
    value = F(max(0,s-t-j+1), j) + term
    for r in range(2,min(t,j)+1):
        term *= F(3*(t-r+1)*(j-r+1),4*r*(s+d-j+r))
        value += term
    return value.numerator, value.denominator

def lower_replay(t,s,d,j):
    u=min(t,j); B=s+d-j+2
    den=4**u*prod(range(B,B+u-1))
    total=0
    for r in range(1,u+1):
        falling=prod(range(j-r+1,j))
        suffix=prod(range(B+r-1,B+u-1))
        total += comb(t,r)*3**r*4**(u-r)*falling*suffix
    return j*total+max(0,s-t-j+1)*den, j*den

def primary_test(wn,wd,cn,cd,ln,ld):
    # (max(0,1-sqrt(w)))^2 <= c*L.
    if wn<0 or wd<=0 or cn<=0 or cd<=0 or ln<=0 or ld<=0:
        raise ValueError('sign premise')
    if wn>=wd:return True
    # 1+w-cL <= 2sqrt(w); square only if left hand side positive.
    a=(wd+wn)*cd*ld-cn*ln*wd
    return a<=0 or a*a<=4*wn*wd*(cd*ld)**2

def replay_test(wn,wd,cn,cd,ln,ld):
    if not (0<=wn and 0<wd and 0<cn and 0<cd and 0<ln and 0<ld):
        raise ValueError('sign premise')
    if wn>=wd:return True
    R=F(cn*ln,cd*ld); w=F(wn,wd)
    if R>=1+w:return True
    return (1-w)**2 + R**2 - 2*R*(1+w) <= 0

def run(t, method):
    start=time.monotonic(); conditions=0; interiors=0; zero_neighbors=0
    hash_l=hashlib.sha256(); digest=hashlib.sha256()
    lower=lower_primary if method=='primary' else lower_replay
    check=primary_test if method=='primary' else replay_test
    for s in range(3*t,17*t+1):
        d=min(3*t,(s+2*t)//5,18*t-s)
        if d<t:raise AssertionError(('D bound',t,s,d))
        L=[None]+[lower(t,s,d,j) for j in range(1,s+2)]
        # Canonical rational hash is equal for the two different constructions.
        for j in range(1,s+2):
            r=F(*L[j]);hash_l.update(f'{t},{s},{j},{r.numerator}/{r.denominator}\n'.encode())
        for eps in (0,1):
            M=s+t+eps; N=s+4*t+eps
            for k in range(2,M):
                interiors+=1; cn=N+1; cd=k*(N-k)
                wn=(k+1)*max(0,s-t-k+1)*max(0,s-t-k+2)
                wd=(k-1)*(M+d-k)*(M+d-k+1)
                # inverse of upper bound on r, set to zero if lower z-rate vanishes.
                if s+eps-k>0:
                    vn=(k-1)*(s+eps-k)*(s+eps-k+1)
                    vd=(k+1)*(s+d-k+1)*(s+d-k+2)
                else:vn,vd=0,1
                for side,j,a,b in ((-1,k-1,wn,wd),(1,k+1,vn,vd)):
                    if j>s+1:
                        zero_neighbors+=1
                        continue
                    ln,ld=L[j]
                    if not check(a,b,cn,cd,ln,ld):
                        raise AssertionError(('ENVELOPE',method,t,s,d,eps,k,side,a,b,cn,cd,ln,ld))
                    conditions+=1
                    # Digest of ALL admitted finite conditions, not just boundary samples.
                    digest.update(f'{t},{s},{d},{eps},{k},{side}\n'.encode())
    return {'t':t,'method':method,'S_min':3*t,'S_max':17*t,'epsilon':[0,1],
            'k_range':'2 <= k < S+t+epsilon','interior_cases':interiors,
            'nonzero_neighbor_conditions':conditions,'zero_neighbor_cases':zero_neighbors,
            'canonical_L_sha256':hash_l.hexdigest(),'condition_domain_sha256':digest.hexdigest(),
            'status':'EXACT_ALL_PASS','elapsed_seconds':round(time.monotonic()-start,6)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--method',choices=['primary','replay'],required=True)
    p.add_argument('--start',type=int,default=4);p.add_argument('--end',type=int,default=23)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if not (4<=a.start<=a.end<=23):p.error('require 4 <= start <= end <= 23')
    a.out.mkdir(parents=True,exist_ok=True)
    for t in range(a.start,a.end+1):
        result=run(t,a.method)
        (a.out/f'envelope-{a.method}-{t:02}.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)
