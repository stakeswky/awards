"""A9 small, explicit graph regressions for root/centroid/endpoint identities.
Two exact graph recurrences, plus literal subsets on small inputs. No claim
that these graphs are beyond the analytic cutoff or an exhaustive census.
This source is newly written for A9 using standard library only.
"""
from __future__ import annotations
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import argparse,json


def add(a:tuple[int,...],b:tuple[int,...])->tuple[int,...]:
    z=[0]*max(len(a),len(b))
    for i,v in enumerate(a):z[i]+=v
    for i,v in enumerate(b):z[i]+=v
    while len(z)>1 and z[-1]==0:z.pop()
    return tuple(z)

def scale(a:tuple[int,...],c:int)->tuple[int,...]: return tuple(c*v for v in a)
def mul(a:tuple[int,...],b:tuple[int,...])->tuple[int,...]:
    z=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    while len(z)>1 and z[-1]==0:z.pop()
    return tuple(z)

def product(xs)->tuple[int,...]:
    z=(1,)
    for x in xs:z=mul(z,x)
    return z

def shift(a:tuple[int,...])->tuple[int,...]:return (0,)+a

def bits(mask:int):
    while mask:
        b=mask&-mask;mask-=b;yield b.bit_length()-1


class Forest:
    def __init__(self,n:int,edges:list[tuple[int,int]]):
        self.n=n;self.edges=sorted(tuple(sorted(e)) for e in edges);self.adj=[0]*n
        assert len(set(self.edges))==len(self.edges)
        parent=list(range(n))
        def root(x):
            while parent[x]!=x:x=parent[x]
            return x
        for v,w in self.edges:
            assert 0<=v<w<n
            rv,rw=root(v),root(w);assert rv!=rw;parent[rv]=rw
            self.adj[v]|=1<<w;self.adj[w]|=1<<v
        self.full=(1<<n)-1
        self.dp=lru_cache(None)(self._dp)
        self.delete=lru_cache(None)(self._delete)
    def components(self,mask:int)->list[int]:
        answer=[]
        while mask:
            frontier=mask&-mask;component=0
            while frontier:
                b=frontier&-frontier;frontier-=b
                if component&b:continue
                v=b.bit_length()-1;component|=b
                frontier|=self.adj[v]&mask&~component
            answer.append(component);mask&=~component
        return answer
    def _dp(self,mask:int)->tuple[int,...]:
        def walk(v:int,parent:int)->tuple[tuple[int,...],tuple[int,...]]:
            zero,one=(1,),(0,1)
            for w in bits(self.adj[v]&mask):
                if w==parent:continue
                x,y=walk(w,v);zero=mul(zero,add(x,y));one=mul(one,x)
            return zero,one
        total=(1,)
        for c in self.components(mask):
            v=(c&-c).bit_length()-1;x,y=walk(v,-1);total=mul(total,add(x,y))
        return total
    def _delete(self,mask:int)->tuple[int,...]:
        if mask==0:return (1,)
        cs=self.components(mask)
        if len(cs)>1:return product(self.delete(c) for c in cs)
        v=max(bits(mask),key=lambda x:((self.adj[x]&mask).bit_count(),-x))
        return add(self.delete(mask&~(1<<v)),shift(self.delete(mask&~((1<<v)|self.adj[v]))))
    def literal(self,mask:int)->tuple[int,...]:
        assert mask.bit_count()<=10
        result=[0]*(mask.bit_count()+1);s=mask
        while True:
            if all(self.adj[v]&s==0 for v in bits(s)): result[s.bit_count()]+=1
            if s==0:break
            s=(s-1)&mask
        while len(result)>1 and result[-1]==0:result.pop()
        return tuple(result)
    def rooted(self,v:int,parent:int,mask:int,lam:Q)->tuple[Q,Q,Q,Q]:
        r=lam;delta=Q(1);gamma=Q(0)
        for w in bits(self.adj[v]&mask):
            if w==parent:continue
            ri,qi,di,gi=self.rooted(w,v,mask,lam)
            r/=1+ri;delta-=qi*di;gamma-=qi*gi+qi*(1-qi)*di*di
        return r,r/(1+r),delta,gamma
    def prefix_recurrences(self,mask:int,r:int)->tuple[tuple[int,...],tuple[int,...]]:
        assert len(self.components(mask))==1
        sub=mask&~(1<<r);cs=self.components(sub)
        roots=[next(bits(self.adj[r]&c)) for c in cs]
        A=[self.dp(c) for c in cs];B=[self.dp(c&~(1<<v)) for c,v in zip(cs,roots)]
        U=[add(x,scale(y,-1)) for x,y in zip(A,B)]
        DE=[self.prefix_recurrences(c,v) for c,v in zip(cs,roots)]
        common=(0,)
        for i in range(len(cs)):
            common=add(common,mul(DE[i][0],product(A[j] for j in range(len(cs)) if j!=i)))
        D=common
        for i in range(len(cs)):
            diff=add(product(A[j] for j in range(len(cs)) if j!=i),scale(product(B[j] for j in range(len(cs)) if j!=i),-1))
            D=add(D,mul(U[i],diff))
            D=add(D,shift(mul(DE[i][1],product(B[j] for j in range(len(cs)) if j!=i))))
        E=common
        for selected in range(1<<len(cs)):
            c=selected.bit_count()
            if c>=2:E=add(E,scale(product(U[i] if selected&(1<<i) else B[i] for i in range(len(cs))),c-1))
        assert all(x>=0 for x in D+E)
        return D,E
    def prefix_literal(self,mask:int,r:int)->tuple[tuple[int,...],tuple[int,...]]:
        D=[0]*(mask.bit_count()+1);E=[0]*len(D);s=mask
        while True:
            if all(self.adj[v]&s==0 for v in bits(s)):
                k=s.bit_count();score=2*k-sum((self.adj[v]&mask).bit_count() for v in bits(s))
                D[k]+=score-2*bool(s&(1<<r))
                if s&(1<<r)==0:E[k]+=score-1
            if s==0:break
            s=(s-1)&mask
        j=self.dp(mask&~((1<<r)|self.adj[r]))
        return add(tuple(D),(0,)),add(tuple(E),j)


def moments(poly:tuple[int,...],lam:Q)->tuple[Q,Q,Q]:
    weights=[Q(x)*lam**k for k,x in enumerate(poly)];z=sum(weights,Q(0))
    mu=sum((k*w for k,w in enumerate(weights)),Q(0))/z
    second=sum((k*k*w for k,w in enumerate(weights)),Q(0))/z
    return z,mu,second-mu*mu

def enc(x:Q)->list[int]:return [x.numerator,x.denominator]


def centroid_audit(g:Forest,lam:Q,b:int)->dict:
    _,mu,var=moments(g.dp(g.full),lam)
    leaves=[];transitions=0
    def visit(mask:int,offset:int,weight:Q,history:list)->None:
        nonlocal transitions
        large=next((c for c in g.components(mask) if c.bit_count()>b),None)
        if large is None:
            _,localmean,localvar=moments(g.dp(mask),lam)
            leaves.append({'mask':mask,'offset':offset,'weight':enc(weight),'mean':enc(offset+localmean),'variance':enc(localvar),'history':history})
            return
        v=next(v for v in bits(large) if max((c.bit_count() for c in g.components(large&~(1<<v))),default=0)*2<=large.bit_count())
        a=mask&~(1<<v);j=mask&~((1<<v)|g.adj[v])
        za,ma,va=moments(g.dp(a),lam);zj,mj,vj=moments(g.dp(j),lam)
        q=lam*zj/(za+lam*zj);delta=1+mj-ma;gamma=vj-va
        _,mp,vp=moments(g.dp(mask),lam)
        for xi,newmask,newmean,newvar,prob in [(0,a,ma,va,1-q),(1,j,1+mj,vj,q)]:
            assert newmean-mp==delta*(xi-q)
            assert newvar-vp==gamma*(xi-q)-q*(1-q)*delta*delta
            transitions+=1
            visit(newmask,offset+xi,weight*prob,history+[[v,xi]])
    visit(g.full,0,Q(1),[])
    weight=lambda row:Q(*row['weight'])
    mean=lambda row:Q(*row['mean'])
    variance=lambda row:Q(*row['variance'])
    assert sum((weight(x) for x in leaves),Q(0))==1
    assert sum((weight(x)*mean(x) for x in leaves),Q(0))==mu
    mixed=sum((weight(x)*(mean(x)-mu)**2 for x in leaves),Q(0))
    expected_var=sum((weight(x)*variance(x) for x in leaves),Q(0))
    assert mixed+expected_var==var
    return {'block_limit':b,'activity':enc(lam),'terminal_histories':leaves,'transition_checks':transitions,
            'mean_mixture_variance':enc(mixed),'expected_terminal_variance':enc(expected_var),'whole_variance':enc(var),
            'absolute_variance_drift':enc(sum((weight(x)*abs(variance(x)-var) for x in leaves),Q(0))),
            'zero_terminal_variance_histories':sum(variance(x)==0 for x in leaves)}


def run()->dict:
    cases=[('empty',0,[]),('singleton',1,[]),('P2',2,[(0,1)]),('P7',7,[(i,i+1) for i in range(6)]),
           ('star9',9,[(0,i) for i in range(1,9)]),
           ('branched9',9,[(0,1),(0,2),(1,3),(1,4),(2,5),(5,6),(5,7),(5,8)]),
           ('P5_union_star5',10,[(i,i+1) for i in range(4)]+[(5,i) for i in range(6,10)])]
    edges=[(0,1),(0,2),(0,3)];n=4
    for hub,s in enumerate([3,4,4],1):
        for _ in range(s):edges.extend([(hub,n),(n,n+1)]);n+=2
    cases.append(('T26_nonLC',n,edges))
    records=[];arrays=0;coefficients=0;literal_arrays=0;root_tests=0;prefix_tests=0;centroids=0;negative_delta=0;negative_gamma=0
    for name,n,edges in cases:
        g=Forest(n,edges);masks=[g.full]+[g.full&~(1<<r) for r in range(n)]+[g.full&~((1<<r)|g.adj[r]) for r in range(n)]
        polynomials=[]
        for mask in masks:
            x,y=g.dp(mask),g.delete(mask);assert x==y
            arrays+=1;coefficients+=len(x)
            if n<=10:assert x==g.literal(mask);literal_arrays+=1
            polynomials.append({'mask':mask,'coefficients':x})
        P=g.dp(g.full);alpha=len(P)-1;rows=[]
        for lam in [Q(1,4),Q(1),Q(12)]:
            zp,mp,vp=moments(P,lam)
            if n:assert Q(n,2**13)<=vp<=2**40*n
            for r in range(n):
                za,ma,va=moments(g.dp(g.full&~(1<<r)),lam)
                zj,mj,vj=moments(g.dp(g.full&~((1<<r)|g.adj[r])),lam)
                q=lam*zj/zp;delta=1+mj-ma;gamma=vj-va
                assert zp==za+lam*zj
                assert mp==ma+q*delta and vp==va+q*gamma+q*(1-q)*delta**2
                if len(g.components(g.full))==1:
                    rr,qr,dr,gr=g.rooted(r,-1,g.full,lam)
                    assert (qr,dr,gr)==(q,delta,gamma)
                rows.append({'activity':enc(lam),'root':r,'q':enc(q),'delta':enc(delta),'gamma':enc(gamma),
                             'weighted_mean_square':enc(q*(1-q)*delta**2),'weighted_variance_square':enc(q*(1-q)*gamma**2)})
                root_tests+=1;negative_delta+=delta<0;negative_gamma+=gamma<0
        prefix=[]
        if 0<n<=10:
            for c in g.components(g.full):
                for r in bits(c):
                    de=g.prefix_recurrences(c,r);assert de==g.prefix_literal(c,r)
                    prefix.append({'mask':c,'root':r,'D':de[0],'E':de[1]});prefix_tests+=1
        assert all(P[k+1]>=P[k] for k in range(min((n+3)//4,alpha)))
        assert all(P[k+1]<=P[k] for k in range(max(0,(2*alpha+1)//3),alpha))
        ca=[]
        if 0<n<=10:
            for lam in [Q(1,4),Q(12)]:ca.append(centroid_audit(g,lam,2));centroids+=1
        records.append({'name':name,'n':n,'edges':g.edges,'polynomial_tasks':polynomials,
                        'root_moments':rows,'prefix_root_recurrences':prefix,'centroid_audits':ca,
                        'negative_LC_indices':[k for k in range(1,alpha) if P[k]*P[k]<P[k-1]*P[k+1]]})
    return {'status':'PASS_EXACT_GRAPH_REGRESSION_NOT_THRESHOLD_CERTIFICATION','graphs':records,
            'counts':{'named_graphs':len(cases),'full_array_tasks':arrays,'coefficient_comparisons':coefficients,
                      'literal_array_tasks':literal_arrays,'root_activity_checks':root_tests,
                      'negative_delta_occurrences':negative_delta,'negative_gamma_occurrences':negative_gamma,
                      'prefix_recurrence_literal_checks':prefix_tests,'complete_centroid_law_checks':centroids,
                      'centroid_transition_checks':sum(c['transition_checks'] for g in records for c in g['centroid_audits']),
                      'centroid_terminal_histories':sum(len(c['terminal_histories']) for g in records for c in g['centroid_audits'])},
            'shared_helpers':'The two counters share graph validation, connected-component finder, and integer polynomial arithmetic, but not counting recurrence. Literal enumeration is a third small-graph check.',
            'cutoff_scale_graphs_tested':0,'old_author_programs_rerun':False,'external_review':False,'Lean':'NOT_RUN'}


def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True);out=a.output/'GRAPH_IDENTITIES.json'
    if out.exists():raise SystemExit('Refusing to overwrite output')
    result=run();out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result['counts'],sort_keys=True))
if __name__=='__main__':main()
