"""Exact coefficient arithmetic and the two graph-count polynomials.
Coefficients are stored in increasing degree order.
"""
from math import comb

def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def add(a,b):
 return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]

def binom(n):return [comb(n,k) for k in range(n+1)]
def branch(s):
 q=[1]
 for n in s:q=mul(q,add(binom(n),[0,1]))
 r=binom(sum(s));h=add(q,[0]+r)
 return h,q,r
B=[(s,) for s in range(3,18)]+[(2,b) for b in range(6,15)]+[(3,b) for b in range(5,14)]+[(4,b) for b in range(4,13)]+[(5,b) for b in range(5,12)]+[(6,b) for b in range(6,11)]+[(7,b) for b in range(7,10)]+[(8,8),(5,5,5)]

def family(sigma):
 a=q=[1]
 for s in sigma:
  h,g,_=branch(s);a=mul(a,h);q=mul(q,g)
 return a,q,add(a,[0]+q),add(mul(a,[1,1]),[0]+q)

