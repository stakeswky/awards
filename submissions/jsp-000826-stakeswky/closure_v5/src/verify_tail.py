#!/usr/bin/env python3
"""Exact finite part and polynomial identity for the all-t>=24 tail proof."""
import argparse,json
from fractions import Fraction as F
from math import comb,prod
from pathlib import Path

def f_direct(t,j):
    return sum((F(comb(t,r)*3**r*prod(range(j-r+1,j)),4**r*(18*t)**(r-1))
                for r in range(1,min(t,j)+1)),F(0))
def f_recurrence(t,j):
    x=F(3*t,4);answer=x
    for r in range(2,min(t,j)+1):
        x*=F(3*(t-r+1)*(j-r+1),4*r*18*t);answer+=x
    return answer

def main(out):
    rows=[]
    for k in range(2,111):
        v=f_direct(24,k-1);w=f_recurrence(24,k-1)
        if v!=w or v<=k:raise AssertionError(('tail prefix',k,v,w))
        rows.append({'k':k,'F24_k_minus_1':[v.numerator,v.denominator],
                     'margin':[ (v-k).numerator,(v-k).denominator]})
    # Expand 110592 * [18 +23(k-2)/64+506(k-2)(k-3)/110592 -k].
    # Substitution k=u+111 is an identity of degree <=2; explicit arithmetic below.
    raw=[110592*18-110592*23*2//64+506*6,
         110592*23//64-506*5-110592,506]
    translated=[raw[0]+111*raw[1]+111**2*raw[2],raw[1]+222*raw[2],raw[2]]
    if translated!=[3672,38954,506] or not all(x>0 for x in translated):
        raise AssertionError(('polynomial',raw,translated))
    result={'status':'EXACT_ALL_PASS','t_base':24,'k_prefix':[2,110],
            'prefix_checks':109,'two_algorithms_equal':True,'finite_prefix':rows,
            'tail_translation':'k=111+u, u>=0','scale':110592,
            'raw_coefficients_ascending':raw,'translated_coefficients_ascending':translated,
            'infinite_steps':'Proved in MAIN_PROOF: termwise monotonicity in t and j; positive polynomial for u>=0.'}
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='finite_prefix'}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);main(p.parse_args().out)
