#!/usr/bin/env python3
"""Exact algebra for the 24-branch LC stability argument; not a Lean proof.
Only standard-library arithmetic and the frozen palette checker are used.
"""
import argparse
import json
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial, lcm
from pathlib import Path
from branch_study import palette


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def convolution(a, b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out


def five_polynomial(t):
    """Coefficients in k of the first five terms of F_t(k-1)-k."""
    require(type(t) is int and t>=5, 't must be at least five')
    out=[F(0)]*5
    falling=[F(1)]
    for j in range(1,6):
        weight=F(comb(t,j)*3**j,4**j*(18*t)**(j-1))
        for r,v in enumerate(falling):
            out[r]+=weight*v
        falling=convolution(falling,[-j-1,1])
    out[1]-=1
    den=lcm(*(x.denominator for x in out))
    return [int(x*den) for x in out],den


def direct_five(t, index):
    """Independent scalar evaluation, via successive rational summands."""
    require(t>=5 and index>=1, 'invalid scalar range')
    term=F(3*t,4)
    value=term
    for j in range(1,min(5,t,index)):
        term*=F(3*(t-j)*(index-j),72*t*(j+1))
        value+=term
    return value


def evaluate(c, x):
    answer=0
    for v in reversed(c):
        answer=answer*x+v
    return answer


def shift(c, offset):
    return [sum(c[j]*comb(j,i)*offset**(j-i) for j in range(i,len(c)))
            for i in range(len(c))]


def build_certificate():
    pal=palette()  # Reconstruct every permitted branch and its four hypotheses.
    c,d=five_polynomial(24)
    expected=[105841916328,-4051151998,25810301,230230,1771]
    require(c==expected and d==6115295232,'quartic derivation changed')
    tail=shift(c,43)
    require(tail==[3725220144,8847286,75157445,534842,1771], 'tail identity changed')
    require(all(v>0 for v in tail),'tail is not coefficientwise positive')
    rows=[]
    for k in range(2,43):
        n=evaluate(c,k)
        require(n>0,'small-index positivity failed')
        require(F(n,d)==direct_five(24,k-1)-k,'scalar/algebra disagreement')
        rows.append({'k':k,'numerator':n})
    # These checks test implementation and boundary handling; the tail proof
    # follows from the polynomial identity, not these finitely many values.
    regressions=[]
    for t in (24,25,44,45,70,100):
        ct,dt=five_polynomial(t)
        for k in (2,3,4,5,6,42,43,44,100,1000):
            value=direct_five(t,k-1)
            require(F(evaluate(ct,k),dt)==value-k,'scalar identity regression failed')
            require(value>=direct_five(24,k-1),'monotonicity regression failed')
            regressions.append([t,k,value.numerator,value.denominator])
    return {'status':'PASS_EXACT_ALGEBRA_NOT_LEAN', 'palette':pal,
            'theorem':'E and P log-concave for every permitted mixture with integer t>=24',
            'proof_note':'LC_STABILITY.md', 'quartic_coefficients_ascending':c,
            'denominator':d,'tail_shift':43,'shifted_coefficients_ascending':tail,
            'finite_indices':[2,42],'finite_rows':rows,
            'finite_positive_indices':len(rows),'positive_tail_coefficients':len(tail),
            'scalar_regression_checks':len(regressions),
            'scalar_regressions_sha256':sha256(encode(regressions)).hexdigest(),
            'infinite_parameter_step':'For j<=5, binom(t,j)/t^(j-1) = t/j! times product_(i=1)^(j-1)(1-i/t), nondecreasing for real t>=24. Falling factors are nonnegative at integer k>=2.',
            'limits':'Written argument plus exact algebra. No original Erdos 993 solution, optimal-threshold claim, Lean run, external review or global novelty claim.'}


def main(out):
    p=Path(out)
    p.parent.mkdir(parents=True,exist_ok=True)
    data=build_certificate()
    with p.open('xb') as f:
        f.write(json.dumps(data,indent=2,sort_keys=True).encode()+b'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ['finite_rows','palette']},indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    main(ap.parse_args().out)
