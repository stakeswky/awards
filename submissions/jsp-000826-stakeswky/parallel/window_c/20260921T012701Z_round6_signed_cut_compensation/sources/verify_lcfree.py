"""Exact graph controls for the uniform written LC-free-subunion proof.
Finite checks are regression only; the all-r argument is in PROOF.md.
"""
import argparse,json,sys
from pathlib import Path
from math import comb
from fractions import Fraction
from inherited_exact import bush,bush_formula,graph_dp,union,lc_bad,valleys
from deletion_balanced import deletion,multiply
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
def run():
    rows=[];tasks=entries=0
    for s,r in [(6,2),(8,4),(12,6),(18,8)]:
        assert 2**s>24*r
        X=bush([s]*3);A=bush_formula([s]*3);D=len(A)-1
        assert D==3*s+3
        u=2**s+s;v=s*2**(s-1)+comb(s,2)
        assert A[-3:]==[3*u*u+3*v+2**(3*s),3*u,1]
        P=[1]
        for t in range(1,r+1):
            P=multiply(P,A);g=union([X]*t);one=graph_dp(*g);two,stats=deletion(*g)
            assert P==one==two;tasks+=1;entries+=len(P)
            minor=P[-2]**2-P[-3]*P[-1]
            expected=Fraction(t*(9*t+3)*u*u,2)-3*t*v-t*2**(3*s)
            assert minor==expected<0
            rows.append(dict(s=s,r=r,t=t,n=g[0],edges=g[1],P=P,negative_LC_indices=lc_bad(P),
              penultimate_minor=minor,formula_integer=int(expected),valleys=valleys(P),
              HEREDITARY='UNKNOWN',deletion_cache=stats))
    return dict(status='PASS',actual_graph_count_tasks=tasks,coefficient_entries_three_way=entries,
        scope='four parameter panels, not fixed-palette closure',rows=rows)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();r=run();p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'],r['actual_graph_count_tasks'],r['coefficient_entries_three_way'])
