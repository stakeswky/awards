"""Algebra-only controls. These arrays are NOT forest counterexamples or coverage."""
import random,json,argparse,sys
from pathlib import Path
from signed_cut import cut_record,convolution,last_mode,jsonable,at
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
def run():
    rng=random.Random(99306);positions=0;backwards=0;birth=0;flat=0;gates=0;negative_total=0
    for case in range(2000):
        a=[rng.randrange(1,22) for _ in range(rng.randrange(2,10))]
        left=sorted(rng.randrange(1,21) for _ in range(rng.randrange(0,5)))
        right=sorted((rng.randrange(1,21) for _ in range(rng.randrange(0,5))),reverse=True)
        b=left+[21]+right;m=last_mode(b);p=convolution(a,b)
        for z in range(m+1,m+len(a)):
            r=cut_record(a,b,z,pair_audit=True);positions+=1
            assert at(p,z-1)-at(p,z)==r['present_loss'] and at(p,z)-at(p,z+1)==r['next_loss']
            backwards+=r['negative_pairs']>0;birth+=r['birth']>0;flat+=r['present_loss']==0
            gates+=r['gate'];negative_total+=r['H']<0
    # Explicit last-mode plateaus and support endpoints, including B of degree zero.
    controls=[]
    for a,b in [([1,2,2,1],[1,1]),([1,1],[1]),([1,4,1],[1,2,2,2,1]),([1,1,1],[1,1,1])]:
        m=last_mode(b)
        for z in range(m+1,m+len(a)):
            controls.append(cut_record(a,b,z,pair_audit=True))
    abstract_a=[1,2,2,2,2,3,5,10,10,10,10,20,20,20,100]
    abstract_b=[1,2,3,5,5,10,10,100,100]
    abstract_p=convolution(abstract_a,abstract_b)
    guard=cut_record(abstract_a,abstract_b,20,pair_audit=True)
    assert abstract_p[19:22]==[5200,5000,12000] and guard['payment']<0
    assert len(abstract_a)-1>abstract_a[1]  # impossible for any graph count
    return dict(abstract_nonforest_guard=dict(A=abstract_a,B=abstract_b,P=abstract_p,cut=guard),status='PASS',seed=99306,array_pairs=2000,random_positions=positions,
        positions_with_inverse_pairs=backwards,positive_birth_positions=birth,
        current_plateaus=flat,payment_gates_pass=gates,negative_total_H_positions=negative_total,
        explicit_boundary_positions=len(controls),controls=controls,
        scope='arbitrary positive arrays; NOT forest coverage, NOT a forest theorem proof')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    r=run();p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(jsonable(r),sort_keys=True,indent=2)+'\n')
    print({k:v for k,v in r.items() if k not in ('controls','abstract_nonforest_guard')})
