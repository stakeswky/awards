"""Independent integer fixed-point interval audit of the A9 endpoint and cutoff.
No Fraction, floating point, approximate transcendental library, or network.
The log identity agrees with the first verifier; the arithmetic implementation
and rounding scheme differ. This is not independent external peer review.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isqrt
from pathlib import Path
import argparse, json
S=10**24

def ceil_div(x:int,y:int)->int:
    assert y>0
    return -((-x)//y)

@dataclass(frozen=True)
class I:
    lo:int
    hi:int
    def __post_init__(self): assert self.lo<=self.hi
    @staticmethod
    def rational(n:int,d:int=1)->'I':
        assert d>0
        return I(n*S//d,ceil_div(n*S,d))
    def __add__(self,o:'I')->'I': return I(self.lo+o.lo,self.hi+o.hi)
    def __neg__(self)->'I': return I(-self.hi,-self.lo)
    def __sub__(self,o:'I')->'I': return self+-o
    def __mul__(self,o:'I')->'I':
        q=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi]
        return I(min(q)//S,ceil_div(max(q),S))
    def __truediv__(self,o:'I')->'I':
        assert o.lo>0
        inv=I(S*S//o.hi,ceil_div(S*S,o.lo))
        return self*inv
    def sqrt(self)->'I':
        assert self.lo>=0
        low=isqrt(self.lo*S); high=isqrt(self.hi*S)
        if high*high<self.hi*S: high+=1
        assert low*low<=self.lo*S and high*high>=self.hi*S
        return I(low,high)
    def log(self,m:int=256)->'I':
        assert self.lo>=S
        one=I.rational(1)
        z=(self-one)/(self+one)
        z2=z*z;term=z;total=I.rational(0)
        for h in range(m):
            total=total+I.rational(2)*term/I.rational(2*h+1)
            term=term*z2
        remainder=I.rational(2)*term/(I.rational(2*m+1)*(one-z2))
        assert remainder.lo>=0
        return I(total.lo,total.hi+remainder.hi)
    def output(self)->dict:
        return {'lower_numerator':self.lo,'upper_numerator':self.hi,'denominator':S,'rounding':'outward_fixedpoint'}

def run()->dict:
    one=I.rational(1);two=I.rational(2);three=I.rational(3)
    l2=two.log();l13=I.rational(13).log();l10=I.rational(10).log()
    qstar=I.rational(13,12).sqrt()*(three*l2/two.sqrt()+two*((I.rational(12).sqrt()+I.rational(13).sqrt())/(one+two.sqrt())).log())
    ratio=l13/qstar
    assert 680891044148*S < ratio.lo*10**12
    assert ratio.hi*10**12 < 680891044149*S
    assert ratio.lo*25 > 17*S
    logcut=I.rational(2600000)*l2/l10
    assert logcut.lo//S == logcut.hi//S == 782677
    # Integer-only polynomial/rational premises, independently arranged.
    assert 3*199**499*1000**500 < 999**500*200**499
    assert 4*12**26 < 13**26
    # exp(997/400) lower series represented by one common factorial denominator.
    factorial=1
    for k in range(1,21): factorial*=k
    exp_numerator=0;fact_h=1
    for h in range(21):
        if h:fact_h*=h
        exp_numerator += 997**h*400**(20-h)*(factorial//fact_h)
    assert 199*exp_numerator > 12*200*400**20*factorial
    assert 4*1999*384000 < (1<<32)
    assert 4*1999*(1<<26) < (1<<39)
    rows=[]
    for c,d,target in [(199,4,-12),(154,15992,-8),(207,1999,-12),(211,7996,-12),(11,1,-12)]:
        margin=target*d-(c*d-2600000)
        assert margin>0
        rows.append({'coefficient_log2':c,'n_exponent_denominator':d,'target_log2':target,'cleared_positive_margin':margin})
    assert 21*128<4096
    return {'status':'PASS_INTEGER_INTERVALS','scale':S,'log_terms':256,
            'intervals':{'log2':l2.output(),'log13':l13.output(),'log10':l10.output(),'Qstar12':qstar.output(),'mean_factor12':ratio.output(),'log10_cutoff':logcut.output()},
            'integer_power_and_Taylor_checks':True,'all_n_exponent_certificate':rows,
            'cutoff_decimal_digits':782678,'shared_with_other_auditor':'same analytic log identity; no shared interval implementation',
            'not_graph_enumeration':True,'not_formal_or_external_review':True}

def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True);f=a.output/'CONSTANTS_FIXEDPOINT.json'
    if f.exists(): raise SystemExit('Refusing to overwrite output')
    r=run();f.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print('PASS integer intervals and all-n exponents')
if __name__=='__main__': main()
