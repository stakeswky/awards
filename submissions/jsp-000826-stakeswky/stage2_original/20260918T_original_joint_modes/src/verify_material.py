#!/usr/bin/env python3
"""Exact material controls. Abstract witnesses are explicitly not forests."""
import argparse,json,time
from pathlib import Path
from forest_counts import Forest,analyze,add,convolution,modes,valley,pad

def minor(e,l,i,j):
    de_i=e[i+1]-e[i];de_j=e[j+1]-e[j]
    dl_i=l[i+1]-l[i];dl_j=l[j+1]-l[j]
    return dl_i*(-de_j)-dl_j*(-de_i)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    t=time.monotonic()
    rows=json.loads(a.inputs.read_text());lookup={r['id']:r for r in rows}
    selected=[analyze(lookup[k]) for k in ['tree-11','old25','new30']]
    bad=selected[0]
    assert bad['n']==23 and bad['U']==bad['D']==8 and bad['unimodal']
    assert bad['vertices'][4]['M_A']==(7,7) and bad['vertices'][4]['M_B']==(9,9)
    assert bad['vertices'][4]['distance']==2 and bad['local_deletions_unimodal']
    old_a=selected[1]['vertices'][2]['A'];old_b=selected[1]['vertices'][2]['B']
    assert old_a[13]==1 and old_b[13]==4
    p=selected[2]['counts'];assert p[16]**2-p[15]*p[17]==-219
    new_a=selected[2]['vertices'][2]['A'];new_b=selected[2]['vertices'][2]['B']
    assert new_a[15:18]==(1935,50,1) and new_b[15:18]==(1200,4,0)
    assert 50*50-1935==565 and 4*4==16
    assert 2*50*4-1935*0-1*1200==-800
    star={'id':'star7-minor-control','n':7,'edges':[(0,v) for v in range(1,7)]}
    s=analyze(star);g=Forest(7,star['edges'])
    for mask in range(1<<7):
        p=g.recount(mask,brute=True);assert valley(p) is None
    x=s['vertices'][0]['A'];y=s['vertices'][0]['B']
    assert minor(y,x,1,2)==-5 and s['U']==s['D']==3 and s['unimodal']
    assert x[2]-x[1]==9 and x[3]-x[2]==5
    assert y[2]-y[1]==-1 and y[3]-y[2]==0
    c=(1,6,7,8,9,8,1);h=(1,4,1)
    aa=add(c,(0,)+h);xx=convolution((1,1),c);yy=(0,)+h
    pp=add(xx,yy)
    assert all(valley(z) is None for z in [c,h,aa,xx,yy,(0,)+c])
    assert all((h[k] if k<len(h) else 0)<=c[k] for k in range(len(c)))
    assert pp==(1,8,17,16,17,17,9,1) and valley(pp)==(2,3)
    assert len(c)-1==c[1]==6 and c[2]==7  # would imply 8 edges on 6 vertices: not a forest.
    e=(3,2,1);l=(1,4,8);p=add(e,l)
    assert minor(e,l,0,1)==-1 and valley(p) is None
    result={'graph_witnesses':selected+[s],
            'scope_of_bad_leaf':'Refutes every-leaf corridor under the checked 2n deletion premises; not existential corridor or ORIGINAL.',
            'star7':{'all_induced_masks_three_algorithm_checked':128,
                     'proper_induced_masks':127,'i':1,'j':2,'minor':-5,
                     'U':3,'D':3,'original_counterexample':False,
                     'scope':'Refutes unlocalized all-leaf slope-minor inequality; not the residual-interval blocker.'},
            'abstract_leaf_shape_control':{'C':c,'H':h,'C_plus_xH':aa,'one_plus_x_C':xx,
                 'xH':yy,'whole':pp,'valley':(2,3),'graph_realizable_as_forest':False,
                 'reason':'C_1=6, C_2=7 imply 8 edges, exceeding 5 for a 6-vertex forest.'},
            'abstract_minor_control':{'E':e,'L':l,'sum':p,'i':0,'j':1,'minor':-1,
                                      'unimodal_sum':True,'graph_claim':False}}
    a.out.parent.mkdir(exist_ok=True,parents=True)
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS_WITH_SCOPE','material_graphs':4,
        'material_whole_and_2n_counts':sum(2*r['n']+1 for r in selected+[s]),
        'star_induced_masks':128,'negative_minor':-5,
        'abstract_valley':[2,3],'original_candidate':False,
        'elapsed_seconds':round(time.monotonic()-t,6)},indent=2))
if __name__=='__main__':main()
