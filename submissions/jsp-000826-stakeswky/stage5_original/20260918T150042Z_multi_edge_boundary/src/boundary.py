"""Actual rooted-message equivalence and a partial-cut mode countercheck."""
import argparse,json
from pathlib import Path
from forest import *
from multi_edge import product
from checks import dump
from profiles import verify_profiles,complete_profile


def canonical_forest(n,edges):
    """Exact unrooted forest type, not independence-polynomial compression."""
    f=PackedForest(n,edges)
    def rooted(v,parent):
        return '('+''.join(sorted(rooted(w,v) for w in f.adj[v] if w!=parent))+')'
    parts=[]
    for mask in components(f.adj,f.full):
        parts.append(min(rooted(v,-1) for v in range(n) if mask>>v&1))
    return tuple(sorted(parts))


def rooted_shapes(limit):
    shapes=[];by_size=[]
    for n in range(1,limit+1):
        old=len(shapes);made=[]
        def combos(start,rem,chosen):
            if rem==0:
                yield chosen;return
            for j in range(start,old):
                size=shapes[j]['n']
                if size>rem:break
                yield from combos(j,rem-size,chosen+(j,))
        for children in combos(0,n-1,()):
            X=product([add(shapes[j]['X'],shapes[j]['Y']) for j in children])
            Y=(0,)+product([shapes[j]['X'] for j in children])
            made.append(dict(n=n,children=children,X=X,Y=Y))
        shapes.extend(made);by_size.append(len(made))
        yield n,shapes,range(old,len(shapes)),list(by_size)


def graph_of(shapes,index):
    edges=[];next_vertex=0
    def walk(j):
        nonlocal next_vertex
        v=next_vertex;next_vertex+=1
        for child in shapes[j]['children']:
            w=walk(child);edges.append((v,w))
        return v
    assert walk(index)==0
    return next_vertex,edges


def profile(g):return tuple(sorted((tuple(a),tuple(b)) for a,b in zip(g['A'],g['B'])))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);materials=json.loads((out/'interaction_material.json').read_text())
    candidates=[]
    for g in materials:
        for b in g['partial_cuts']:
            states={tuple(s['J']):s for s in b['states']};neighbors=[z['root'] for z in b['branches']]
            for J,before in states.items():
                if len(J)<2:continue
                for w in neighbors:
                    K=tuple(sorted(J+(w,)))
                    if w in J or len(K)>=len(neighbors):continue
                    after=states[K];m0=modes(before['B']);m1=modes(after['B'])
                    if m1[1]<m0[0]:
                        candidates.append(dict(id=g['id'],n=g['n'],edges=g['edges'],v=b['v'],
                             J=J,K=K,A=b['A'],B_before=before['B'],B_after=after['B'],
                             P_cut_before=before['P_cut'],P_cut_after=after['P_cut'],
                             original_P=g['P'],U=g['U'],D=g['D'],mode_before=m0,mode_after=m1,
                             full_coefficient_containment=all(u<=v for u,v in zip(before['B'],after['B'])),
                             scope='REFUTES_UNLOCALIZED_MODE_MONOTONICITY_ONLY'))
    witness=candidates[0] if candidates else None
    if witness:
        assert witness['full_coefficient_containment']
        assert all(unimodal(witness[k]) for k in ['A','B_before','B_after','P_cut_before','P_cut_after','original_P'])
    seen={};collisions=0;result=None;visited=0
    for size,shapes,indices,per_order in rooted_shapes(12):
        for j in indices:
            visited+=1;s=shapes[j];key=(s['X'],s['Y'])
            if key not in seen:seen[key]=j;continue
            collisions+=1;old=seen[key]
            n,e=graph_of(shapes,old);n2,e2=graph_of(shapes,j);assert n==n2
            one=describe(n,e,second=True);two=describe(n,e2,second=True)
            assert one['A'][0]==two['A'][0] and one['B'][0]==two['B'][0]
            if profile(one)==profile(two):continue
            contexts=[]
            specs=[('none',0,[],False),('leaf',1,[],False),('path3',3,[(0,1),(1,2)],False),
                   ('star3',4,[(0,1),(0,2),(0,3)],False),('leaf_plus_external_edge',1,[],True)]
            seed=next(z for z in materials if z['id']=='new30')
            specs.append(('new30_root0_plus_external_edge',seed['n'],seed['edges'],True))
            for name,m,ext,extra in specs:
                n0=n+m;ea=list(e)+[(u+n,v+n) for u,v in ext]+([(0,n)] if m else [])
                eb=list(e2)+[(u+n,v+n) for u,v in ext]+([(0,n)] if m else [])
                R=(1,)
                if extra:
                    ea.append((n0,n0+1));eb.append((n0,n0+1));n0+=2;R=(1,2)
                ga=describe(n0,ea,second=True);gb=describe(n0,eb,second=True)
                assert ga['P']==gb['P']
                if m:
                    ex=describe(m,ext,second=True);extX,extY=ex['A'][0],ex['B'][0]
                else:extX,extY=(1,),(0,)
                expected=pad(product([R,add(mul(add(s['X'],s['Y']),extX),mul(s['X'],extY))]),n0)
                assert ga['P']==expected
                contexts.append(dict(name=name,left=ga,right=gb,R=R,external_X=extX,external_Y=extY,
                     U_D_equal=(ga['U'],ga['D'])==(gb['U'],gb['D']),internal_profiles_equal=profile(ga)==profile(gb)))
            joint_left=verify_profiles(n,e);joint_right=verify_profiles(n,e2)
            completion_checks=0
            for context in contexts:
                for side,joint in [('left',joint_left),('right',joint_right)]:
                    whole=context[side]
                    for v,qs in joint['vertices'].items():
                        A,B=complete_profile(qs,context['external_X'],context['external_Y'],context['R'],whole['n'])
                        assert A==whole['A'][int(v)] and B==whole['B'][int(v)]
                        completion_checks+=1
            result=dict(n=n,left=one,right=two,X=s['X'],Y=s['Y'],contexts=contexts,joint_left=joint_left,joint_right=joint_right,completion_checks=completion_checks,
                     rooted_type_indices=(old,j),underlying_unrooted_isomorphic=canonical_forest(n,e)==canonical_forest(n,e2),
                     claim='Equal root boundary messages do not determine the full multiset of internal conditional polynomials.')
            break
        if result:break
    summary=dict(rooted_size_limit=12,completed_generation_counts=per_order,
                 examined_shapes=visited,collision_comparisons=collisions,
                 stopped_at_first_distinct_profile=result is not None,
                 collision_order=result['n'] if result else None,
                 exact_internal_completion_checks=result['completion_checks'] if result else 0,
                 U_D_difference_in_tested_completions=bool(result and any(not c['U_D_equal'] for c in result['contexts'])),
                 strict_mode_decrease_found=witness is not None,
                 strict_mode_decrease_count_in_fixed_materials=len(candidates),
                 root_compression_theorem=False,original_counterexample=False,
                 residual_graphs=sum(bool(g['residual_pairs']) for c in (result['contexts'] if result else []) for g in (c['left'],c['right'])),
                 residual_pairs=sum(len(g['residual_pairs']) for c in (result['contexts'] if result else []) for g in (c['left'],c['right'])))
    dump(out/'mode_witness.json',witness);dump(out/'boundary_witness.json',result)
    dump(out/'boundary_summary.json',summary);print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
