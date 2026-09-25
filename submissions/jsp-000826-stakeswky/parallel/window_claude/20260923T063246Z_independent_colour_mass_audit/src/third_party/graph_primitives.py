"""Independent coordinator reconstruction; not an author-program replay.
All inputs below were transcribed from the read R9 original-graph definitions.
Two graph recurrences share polynomial primitives, not graph recurrences.
"""
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import argparse,json
ONE={(0,0):1}
def add(a,b):
 r=a.copy()
 for k,v in b.items():r[k]=r.get(k,0)+v
 return {k:v for k,v in r.items() if v}
def mul(a,b):
 if a==ONE:return b.copy()
 if b==ONE:return a.copy()
 r=defaultdict(int)
 for (i,j),x in a.items():
  for (k,l),y in b.items():r[i+k,j+l]+=x*y
 return dict(r)
def sh(a,c):return {(i+(c==0),j+(c==1)):v for (i,j),v in a.items()}
def graph(n,es):
 adj=[0]*n;pa=list(range(n))
 def root(x):
  while pa[x]!=x:x=pa[x]
  return x
 for u,v in es:
  assert 0<=u<n and 0<=v<n and u!=v and not(adj[u]>>v&1)
  x,y=root(u),root(v);assert x!=y;pa[x]=y;adj[u]|=1<<v;adj[v]|=1<<u
 return adj
def bits(m):
 while m:
  b=m&-m;m^=b;yield b.bit_length()-1
def comps(mask,adj):
 out=[]
 while mask:
  q=mask&-mask;mask^=q;cm=0
  while q:
   bit=q&-q;q^=bit;v=bit.bit_length()-1;cm|=bit;nb=adj[v]&mask;mask^=nb;q|=nb
  out.append(cm)
 return out
def colors(adj):
 n=len(adj);cs=[-1]*n;cms=comps((1<<n)-1,adj)
 for cm in cms:
  v=next(bits(cm));cs[v]=0;q=[v]
  while q:
   v=q.pop()
   for w in bits(adj[v]):
    if cs[w]<0:cs[w]=1-cs[v];q.append(w)
    else:assert cs[w]!=cs[v]
 for flips in product((0,1),repeat=len(cms)):
  c=cs.copy()
  for cm,f in zip(cms,flips):
   for v in bits(cm):c[v]^=f
  yield c
def rooted(mask,adj,c):
 def rec(v,p):
  a=ONE.copy();b=sh(ONE,c[v])
  for w in bits(adj[v]&mask):
   if w==p:continue
   aa,bb=rec(w,v);a=mul(a,add(aa,bb));b=mul(b,aa)
  return a,b
 ans=ONE.copy()
 for cm in comps(mask,adj):
  a,b=rec(next(bits(cm)),-1);ans=mul(ans,add(a,b))
 return ans
def counter(adj,c):
 @lru_cache(None)
 def rec(mask):
  if not mask:return ONE.copy()
  cms=comps(mask,adj)
  if len(cms)>1:
   ans=ONE.copy()
   for cm in cms:ans=mul(ans,rec(cm))
   return ans
  v=max(bits(mask),key=lambda w:((adj[w]&mask).bit_count(),-w))
  return add(rec(mask&~(1<<v)),sh(rec(mask&~((1<<v)|adj[v])),c[v]))
 return rec
def uni(p):
 a=[0]*(max((i+j for i,j in p),default=0)+1)
 for (i,j),v in p.items():a[i+j]+=v
 return a
def row(p,r):return [p.get((l,r-l),0) for l in range(r+1)]
def conv(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def fine(p,j):
 ws=[]
 for u in range(max(i for i,k in p)+1):
  m=max([k for i,k in p if i==u],default=0)
  for v in range(m+1):
   w=sum((-1)**(r-v)*comb(r,v)*p.get((u,r),0) for r in range(v,m+1));assert w>=0
   if w:ws.append((u,v,w,*[comb(v,r-u) if 0<=r-u<=v else 0 for r in (j-1,j,j+1)]))
 total=0
 for k,(_,_,w,b,a,c) in enumerate(ws):
  for _,_,z,bb,aa,cc in ws[k+1:]:total+=w*z*max(b*cc+bb*c-2*a*aa,0)
 return total,ws
def core(arms):
 n=1;es=[]
 for s in arms:
  h=n;n+=1;es.append((0,h))
  for _ in range(s):es.extend([(h,n),(n,n+1)]);n+=2
 return n,es
def hubs(t,l):
 n=1;es=[]
 for _ in range(t):
  h=n;n+=1;es.append((0,h))
  for _ in range(l):es.append((h,n));n+=1
 return n,es
def union(g,h):
 n,es=g;m,fs=h;return n+m,es+[(a+n,b+n) for a,b in fs]
A61=[(0,1),(0,12),(0,21),(1,2),(1,4),(1,6),(1,8),(1,10),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13),(12,15),(12,17),(12,19),(13,14),(15,16),(17,18),(19,20),(21,22),(21,24),(21,26),(21,28),(22,23),(24,25),(26,27),(28,29)]
B61=[(30,31),(30,42),(30,51),(31,32),(31,36),(31,38),(31,40),(32,33),(33,34),(34,35),(36,37),(36,60),(38,39),(40,41),(42,43),(42,47),(42,49),(43,44),(44,45),(45,46),(47,48),(49,50),(51,52),(51,56),(51,58),(52,53),(53,54),(54,55),(56,57),(58,59)]
F14=(14,[(0,1),(0,2),(1,3),(2,4),(3,5),(4,6),(4,12),(4,13),(5,7),(6,8),(6,10),(6,11),(7,9)])
F17=(17,[(0,1),(0,9),(0,15),(0,16),(1,2),(1,5),(1,8),(2,3),(2,4),(5,6),(5,7),(9,10),(9,13),(10,11),(10,12),(13,14)])
def materials():
 h=core([10,10,10]);f=union(h,(23,[(0,l) for l in range(1,23)]));g=(87,f[1]+[(0,65)])
 return [('F14',F14,5,[0,0]),('F17',F17,6,[0,0]),('T26',core([3,4,4]),13,[1472]*2),('F61',(61,A61+B61),19,[0]*4),('F56',hubs(5,10),26,[1181067781056125771069280]*2),('F87',f,33,[0,0,263461814,263461814]),('G87',g,33,[235203150]*2)]
def metadata(p,n,M,j):
 first=next((k for k in range(len(p)-1) if p[k]>p[k+1]),None);alpha=len(p)-1;h=M*(n-1)//(4*M-2)+1;beta=(alpha*(n-1)+n+alpha-1)//(n+alpha)
 valley=[] if first is None else [k for k in range(first+1,len(p)-1) if p[k]<p[k+1]]
 return dict(n=n,M=M,alpha=alpha,h=h,beta=beta,j=j,first_descent=first,history=first is not None and first<=j-1 and not any(k<j for k in valley),middle=h<=j-1 and j<beta,valley_rises=valley,nonLC=[i for i in range(1,len(p)-1) if p[i]**2<p[i-1]*p[i+1]])
def get(p,i):return p[i] if 0<=i<len(p) else 0
def strip(A,B,k):
 z=k+1;u=max(i for i,x in enumerate(A) if x==max(A));m=max(i for i,x in enumerate(B) if x==max(B));q=z-m-1;ds=[get(B,t)-get(B,t-1) for t in range(len(B)+1)]
 P=lambda zz:sum(max(d,0)*get(A,zz-t) for t,d in enumerate(ds));N=lambda zz:sum(max(-d,0)*get(A,zz-t) for t,d in enumerate(ds))
 ws=[]
 for i in range(len(A)-1):
  uu=sum(max(d,0)*get(A,z-t) for t,d in enumerate(ds) if z-t>i);vv=sum(max(-d,0)*get(A,z-t) for t,d in enumerate(ds) if 0<=z-t<=i);ws.append(uu*vv)
 ws.append(0);prior=0;terms=[]
 for i,x in enumerate(A):
  t=(Q(get(A,i+1),x)-1)*(ws[i]-prior);assert t.denominator==1;terms.append(t.numerator);prior=ws[i]
 loss=sum(-x for x in terms if x<0);outside=sum(x for x in terms if x>0);p=conv(A,B);ell=p[z-1]-p[z];c0=P(z)*A[0]*max(0,-get(ds,z+1));pay=N(z+1)*ell+c0+outside-loss
 assert pay==N(z)*(p[z]-p[z+1])
 return dict(k=k,z=z,u=u,m=m,q=q,loss=loss,outside=outside,C0=c0,N=N(z),N_next=N(z+1),ell=ell,descent_only=N(z+1)*ell-loss,full_pay=pay,terms=terms)
def dump(out,name,obj):
 (out/name).write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n')
def main(out):
 out.mkdir(parents=True,exist_ok=True);records=[];entries=0
 for name,(n,es),j,expected in materials():
  adj=graph(n,es);mask=(1<<n)-1;M=max(cm.bit_count() for cm in comps(mask,adj));rr=[];whole=None
  for cols in colors(adj):
   p=rooted(mask,adj,cols);dc=counter(adj,cols);assert p==dc(mask);pp=uni(p);assert whole is None or pp==whole;whole=pp;entries+=len(p)
   ns=conv(row(p,j-1),row(p,j+1));ps=conv(row(p,j),row(p,j));dm=sum(max(x-y,0) for x,y in zip(ns,ps));dl,ws=fine(p,j)
   assert dm<=dl and sum(ns)==pp[j-1]*pp[j+1] and sum(ps)==pp[j]**2
   rr.append(dict(L=[v for v,c in enumerate(cols) if c==0],bivariate=[[i,k,v] for (i,k),v in sorted(p.items())],negative=ns,positive=ps,D_mass=dm,D_fine=dl,profiles=ws))
  assert sorted(r['D_mass'] for r in rr)==sorted(expected),name
  info=metadata(whole,n,M,j);assert not info['valley_rises'];records.append(dict(name=name,edges=es,P=whole,info=info,reserve=whole[j]*(whole[j-1]-whole[j]),colors=rr));print(name,'PASS',flush=True)
 dump(out,'COLOR_MASS.json',dict(kind='INDEPENDENT_RECONSTRUCTION_NOT_AUTHOR_REPLAY',graphs=len(records),arrays=sum(len(r['colors']) for r in records),entries=entries,materials=records))
 deck=[];arrays=0;entries=0;positions=0
 for name,(n,es) in [('F14',F14),('F61',(61,A61+B61)),('H85',hubs(21,3))]:
  adj=graph(n,es);mask=(1<<n)-1;cs=[0]*n;dc=counter(adj,cs);p=uni(dc(mask));assert p==uni(rooted(mask,adj,cs));arrays+=1;entries+=len(p);aa=[];bb=[]
  for v in range(n):
   for mm,target in [(mask&~(1<<v),aa),(mask&~((1<<v)|adj[v]),bb)]:
    ar=uni(dc(mm));assert ar==uni(rooted(mm,adj,cs));target.append(ar);arrays+=1;entries+=len(ar)
  checks=[]
  for j in range(1,len(p)):
   ts=[get(a,j-1)*(get(a,j)-get(a,j+1))-get(b,j-2)*(get(b,j-1)-get(b,j)) for a,b in zip(aa,bb)];left=sum(ts)-get(p,j-1)*get(p,j);right=(n-2*j)*get(p,j-1)*(get(p,j)-get(p,j+1));assert left==right
   checks.append(dict(j=j,left=left,right=right,negative_T=sum(t<0 for t in ts)));positions+=1
  deck.append(dict(name=name,n=n,P=p,A=aa,B=bb,checks=checks));print(name,'deletion PASS',flush=True)
 adj=graph(61,A61+B61);ca=uni(rooted((1<<30)-1,adj,[0]*61));cb=uni(rooted(((1<<61)-1)^((1<<30)-1),adj,[0]*61));ss=[strip(ca,cb,18),strip(cb,ca,18)]
 assert [s['descent_only'] for s in ss]==[-1412722031309550056002,-1481523614524337983046]
 assert [s['full_pay'] for s in ss]==[279422008351100178135900,292173160577280597558300]
 halls=[]
 for name,a,j in [('H85',64,31),('H85_squared',128,62)]:
  demand=comb(a,j-1)*comb(a,j+1);cap=comb(a,j-1)*comb(a,j);assert demand>cap;f=Q(demand,cap);halls.append(dict(name=name,alpha=a,j=j,demand=demand,capacity=cap,deficit=demand-cap,ratio=[f.numerator,f.denominator]))
 dump(out,'DELETION_AND_STRIP.json',dict(kind='INDEPENDENT_RECONSTRUCTION',deck=deck,arrays=arrays,entries=entries,positions=positions,F61_strips=ss,Hall_counts=halls))
 adj=graph(*F14);n=14;size=1<<n;z=[[0]*(n+1) for _ in range(size)]
 for m in range(size):
  if all(not(adj[v]&m) for v in bits(m)):z[m][m.bit_count()]=1
 for v in range(n):
  for m in range(size):
   if m>>v&1:
    a=z[m];b=z[m^(1<<v)]
    for k in range(n+1):a[k]+=b[k]
 dp=[[1]]+[None]*(size-1);coefs=0;bad=0
 for m in range(size):
  if m:
   bit=m&-m;v=bit.bit_length()-1;a=dp[m^bit];b=dp[m&~(bit|adj[v])];r=[0]*max(len(a),len(b)+1)
   for i,x in enumerate(a):r[i]+=x
   for i,x in enumerate(b):r[i+1]+=x
   dp[m]=r
  r=dp[m];assert r+[0]*(n+1-len(r))==z[m];coefs+=len(r);bad+=any(r[i]**2<r[i-1]*r[i+1] for i in range(1,len(r)-1))
 assert bad==0;dump(out,'F14_HEREDITARY.json',dict(kind='COMPLETE_SUBSET_CHECK_ONE_GRAPH',n=n,masks=size,entries=coefs,nonLC_masks=bad,methods=['subset zeta of literal independence indicators','vertex deletion on smallest vertex'],all_coefficients=dp));print('F14 H PASS',size,coefs,flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);main(ap.parse_args().output)
