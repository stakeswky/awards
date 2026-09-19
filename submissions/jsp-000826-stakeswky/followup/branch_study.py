#!/usr/bin/env python3
"""Exact, deterministic heterogeneous-branch study; standard library only.
No general-tree proof is claimed. Run without -O and use a fresh output directory.
"""
import argparse, json
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
if not __debug__: raise SystemExit('Assertions must remain enabled: do not use -O.')

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return c

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def product(items):
    p=[1]
    for x in items:p=mul(p,x)
    return p

def lc(a):return all(a[k]**2>=a[k-1]*a[k+1] for k in range(1,len(a)-1))
def olc(a):return all(k*a[k]**2>=(k+1)*a[k-1]*a[k+1] for k in range(1,len(a)-1))
def valley(a):
    first=None
    for j in range(len(a)-1):
        if a[j]>a[j+1] and first is None:first=j
        if a[j]<a[j+1] and first is not None:return [first,j]
    return None

def modes(a):
    m=max(a);ix=[i for i,x in enumerate(a) if x==m];return [ix[0],ix[-1]]

def branch(leaves):
    assert leaves and all(type(s) is int and s>=1 for s in leaves)
    q=product(add([comb(s,k) for k in range(s+1)],[0,1]) for s in leaves)
    r=[comb(sum(leaves),k) for k in range(sum(leaves)+1)]
    return q,add(q,[0]+r),r

def graph(arms):
    p=[-1,0]
    for leaves in arms:
        u=len(p);p.append(1)
        for s in leaves:w=len(p);p.append(u);p.extend([w]*s)
    return p

def packed(p):
    """Full expanded graph DP; independent of the branch product formula."""
    assert p and p[0]==-1
    if any(type(p[i]) is not int or not 0<=p[i]<i for i in range(1,len(p))):raise ValueError('invalid parent')
    width=len(p)+1;X=1<<width;mask=X-1;A=[1]*len(p);B=[X]*len(p)
    for v in range(len(p)-1,0,-1):
        u=p[v];A[u]*=A[v]+B[v];B[u]*=A[v]
    def decode(z):
        c=[]
        while z:c.append(z&mask);z>>=width
        return c or [0]
    return decode(A[0]+B[0]),decode(A[0]),decode(B[0])

def splits(p):
    """All conditional counts; same packed representation, not a third checker."""
    width=len(p)+1;X=1<<width;mask=X-1;adj=[[] for _ in p]
    for v in range(1,len(p)):adj[v].append(p[v]);adj[p[v]].append(v)
    @lru_cache(None)
    def message(v,parent):
        a,b=1,X
        for w in adj[v]:
            if w!=parent:c,d=message(w,v);a*=c+d;b*=c
        return a,b
    def decode(z):
        c=[]
        while z:c.append(z&mask);z>>=width
        return c or [0]
    return [(decode(a),decode(b)) for a,b in (message(v,-1) for v in range(len(p)))]

def canonical(p):
    adj=[set() for _ in p]
    for v in range(1,len(p)):adj[v].add(p[v]);adj[p[v]].add(v)
    deg=[len(x) for x in adj];front=[v for v,d in enumerate(deg) if d<=1];remaining=len(p)
    while remaining>2:
        remaining-=len(front);new=[]
        for v in front:
            for w in adj[v]:
                deg[w]-=1
                if deg[w]==1:new.append(w)
        front=new
    def code(v,parent):return '('+''.join(sorted(code(w,v) for w in adj[v] if w!=parent))+')'
    return min(code(v,-1) for v in front)

# Exact polynomial arithmetic in variables t,k; no symbolic package needed.
def plus(a,b):
    c=dict(a)
    for q,v in b.items():c[q]=c.get(q,0)+v
    return {q:v for q,v in c.items() if v}
def times(a,b):
    c={}
    for (i,j),x in a.items():
        for (u,v),y in b.items():c[i+u,j+v]=c.get((i+u,j+v),0)+x*y
    return {q:v for q,v in c.items() if v}
def scale(a,s):return {q:s*v for q,v in a.items() if s*v}
def con(v):return {(0,0):v} if v else {}
def minus(a,b):return plus(a,scale(b,-1))
def translate(a,dt,dk):
    c={}
    for (i,j),x in a.items():
        for u in range(i+1):
            for v in range(j+1):
                key=u,v;c[key]=c.get(key,0)+x*comb(i,u)*comb(j,v)*dt**(i-u)*dk**(j-v)
    return {q:v for q,v in c.items() if v}

def bounds():
    t,k={(1,0):1},{(0,1):1}
    def M(shift):
        z=plus(k,con(shift))
        return plus(plus(scale(times(t,t),3456),scale(times(times(t,minus(z,con(1))),minus(t,con(1))),72)),times(times(minus(z,con(1)),minus(z,con(2))),times(minus(t,con(1)),minus(t,con(2)))))
    den=scale(t,4608);lo,hi=M(-1),M(1)
    polys=[minus(times(lo,hi),times(times(k,den),plus(plus(lo,hi),den))),minus(times(lo,lo),times(times(k,den),plus(scale(lo,2),den)))]
    result=[]
    for p in polys:
        shifted=translate(p,70,2)
        assert len(shifted)==25 and all(v>0 for v in shifted.values())
        result.append([[list(k),v] for k,v in sorted(shifted.items())])
    return result

def palette():
    out=[]
    for d in range(1,6):
        for s in range(1,18):
            if d*(s+1)>18:continue
            q,h,r=branch([s]*d)
            if olc(q) and olc(h) and all(4*x>=3*y for x,y in zip(r,q)) and all((k+1)*q[k+1]<=18*q[k] for k in range(len(q)-1)):out.append([d,s])
    assert out==[[1,s] for s in range(3,18)]+[[2,s] for s in range(4,9)]+[[3,5]]
    return out

def cases(pal):
    for t in [2,3]:
        for ids in combinations_with_replacement(range(len(pal)),t):yield 'palette-small',[[pal[i][1]]*pal[i][0] for i in ids]
    for i in range(1200):
        raw=sha256(('erdos993-hetero-v1-'+str(i)).encode()).digest();t=2+raw[0]%7
        yield 'irregular-probe',[[1+raw[(2+6*j+k)%32]%9 for k in range(1+raw[(1+4*j)%32]%5)] for j in range(t)]
    for t in [70,71]:
        for offset in [0,7]:yield 'theorem-regression',[[pal[(i*5+offset)%21][1]]*pal[(i*5+offset)%21][0] for i in range(t)]

def evaluate(kind,arms,index):
    base=[branch(x) for x in arms];a=product(h for q,h,r in base);q=product(q for q,h,r in base)
    b=[0]+q;E=add(a,b);C=mul([1,1],a);P=add(C,b);p=graph(arms);actual,Ar,Br=packed(p)
    assert actual==P and Ar==E and Br==[0]+a
    assert P[:3]==[1,len(p),(len(p)-1)*(len(p)-2)//2]
    pairs=splits(p) if kind!='theorem-regression' else [(E,[0]+a),(C,b)]
    for av,bv in pairs:assert add(av,bv)==P
    failures=[v for v,(av,bv) in enumerate(pairs) if valley(av) is not None or valley(bv) is not None]
    good=[(av,bv) for av,bv in pairs if valley(av) is None and valley(bv) is None]
    U=max(min(modes(av)[1],modes(bv)[1]) for av,bv in good) if good else None
    D=min(max(modes(av)[0],modes(bv)[0]) for av,bv in good) if good else None
    return dict(index=index,kind=kind,branches=arms,parents=p,n=len(p),coefficients=P,valley=valley(P),log_concave=lc(P),split_scope='r-and-h' if kind=='theorem-regression' else 'all-vertices',split_failures=failures,U=U,D=D,E_log_concave=lc(E),degree=len(P)-1)

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    pal=palette();cert=bounds();stats={};shapes=set();witnesses=[];rows=0;count_splits=0;best={};count_coefficients=0
    with (out/'trials.jsonl').open('w') as f:
        for i,(kind,arms) in enumerate(cases(pal),1):
            r=evaluate(kind,arms,i);rows+=1;f.write(json.dumps(r,separators=(',',':'))+'\n')
            s=stats.setdefault(kind,dict(records=0,max_n=0,min_n=10**9,non_lc=0,valleys=0,max_corridor=-10))
            s['records']+=1;s['max_n']=max(s['max_n'],r['n']);s['min_n']=min(s['min_n'],r['n']);s['non_lc']+=not r['log_concave'];s['valleys']+=r['valley'] is not None
            gap=r['D']-r['U'] if r['U'] is not None else 999;s['max_corridor']=max(s['max_corridor'],gap)
            count_splits+=2 if kind=='theorem-regression' else r['n'];count_coefficients+=len(r['coefficients']);shapes.add(canonical(r['parents']))
            if r['valley'] is not None or r['split_failures']:witnesses.append(r)
            if kind not in best or (gap,not r['log_concave'])>(best[kind]['D']-best[kind]['U'],not best[kind]['log_concave']):best[kind]=r
            if i%400==0:print(i,kind,flush=True)
    summary=dict(status='PASS_EXACT_BOUNDED_STUDY',records=rows,unique_shapes=len(shapes),by_stage=stats,original_counterexamples=sum(r['valley'] is not None for r in witnesses),conditional_counterexample_records=sum(bool(r['split_failures']) for r in witnesses),full_coefficients_compared=count_coefficients,directed_message_splits=count_splits,independence='List-convolution branch formula versus expanded-graph packed DP; same-session implementations.',split_scope='All-vertex counts use the main message implementation, not independent all-vertex replays.',theorem_scope='Written extension for arbitrary mixtures of 21 branch types, t>=70 only; not Lean formalized.',log_sha256=sha256((out/'trials.jsonl').read_bytes()).hexdigest(),palette=pal)
    for name,value in [('summary',summary),('symbolic',cert),('selected',best),('witnesses',witnesses)]:
        (out/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);main(ap.parse_args().out)
