#!/usr/bin/env python3
"""Join separate certificates without upgrading LOCAL to HEREDITARY."""
import argparse
import hashlib
import json
from pathlib import Path
from edge_diagnostics import leaf_test


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();root=args.out
    material=json.loads((root/'edge_material.json').read_text())
    hereditary=json.loads((root/'hereditary_material.json').read_text())
    hs=json.loads((root/'hereditary_summary.json').read_text())
    cs=json.loads((root/'coverage_regression_summary.json').read_text())
    graphs=material['graphs'];table=material['polynomials'];by_id={g['id']:g for g in graphs}
    assert len(by_id)==len(graphs)
    verified={}
    for h in hereditary:
        g=by_id[h['id']]
        assert h['n']==g['n'] and h['edges']==g['edges']
        if h['status']=='VERIFIED':
            assert not h['candidates'] and h['proper_subsets_covered']==2**g['n']-1
            verified[h['id']]=h
    rows=[];eligible=0;refutations=[]
    for g in graphs:
        no_isolates=all(v['degree']>0 for v in g['vertices'])
        no_k2=all(len(c)!=2 for c in g['components'])
        premise=g['n']>0 and no_isolates and g['id'] in verified
        if premise:
            eligible+=len(g['residual_pairs'])
            refutations.extend({'id':g['id'],'i':p['i'],'j':p['j']} for p in g['residual_pairs'] if p['all_leaves_fail'])
        rows.append({'id':g['id'],'n':g['n'],'origin':g['origin'],'LOCAL':g['LOCAL'],
          'HEREDITARY':'VERIFIED' if g['id'] in verified else 'UNKNOWN',
          'no_isolates':no_isolates,'no_K2_component':no_k2,
          'U':g.get('U'),'D':g.get('D'),'residual_pairs':len(g['residual_pairs']),
          'J_H_premises_verified':premise and no_k2,'RSM_premises_verified':premise})
    witness=by_id['tree-11'];h=verified['tree-11']
    vertices=[]
    for v in witness['vertices']:
        a,b=v['A']['mode'],v['B']['mode']
        vertices.append({'v':v['v'],'degree':v['degree'],'A':table[v['A']['poly']],
          'B':table[v['B']['poly']],'A_mode':a,'B_mode':b,
          'mode_distance':max(0,a[0]-b[1],b[0]-a[1])})
    compact={'id':'tree-11','n':witness['n'],'edges':witness['edges'],
      'components':witness['components'],'P':table[witness['P']['poly']],
      'P_mode':witness['P']['mode'],'vertices':vertices,
      'U':witness['U'],'D':witness['D'],'HEREDITARY':'VERIFIED',
      'proper_subsets_covered':h['proper_subsets_covered'],'proper_signatures':h['proper_signatures'],
      'bad_leaf':4,'good_vertex':0,'ORIGINAL_counterexample':False,
      'J_H_counterexample':False,'RSM_counterexample':False}
    assert vertices[4]['degree']==1 and vertices[4]['mode_distance']==2
    assert vertices[0]['mode_distance']==0 and witness['U']==witness['D']==8
    star=by_id['star7-minor-control'];s=star['vertices'][0]
    off=leaf_test(table[s['A']['poly']],table[s['B']['poly']],1,2)
    assert off['Q']==-5 and not (star['U']<=1<2<star['D'])
    lc=by_id['new30'];p=table[lc['P']['poly']]
    assert p[16]*p[16]-p[15]*p[17]==-219 and lc['P']['unimodal']
    summary={'original_math':'NOT_CLOSED','structural_progress':'NO_STRUCTURAL_ADVANCE',
      'completed_graph_records':len(graphs),'inherited_controls':sum(g['origin']=='inherited_control' for g in graphs),
      'new_graph_records':sum(g['origin']=='new' for g in graphs),'maximum_order':max(g['n'] for g in graphs),
      'LOCAL_verified_graphs':sum(g['LOCAL'] for g in graphs),'HEREDITARY_verified_graphs':len(verified),
      'HEREDITARY_unknown_graphs':len(graphs)-len(verified),
      'J_H_premises_verified_graphs':sum(r['J_H_premises_verified'] for r in rows),
      'residual_graphs':sum(g.get('D_minus_U',0)>=2 for g in graphs),
      'residual_pairs':sum(len(g['residual_pairs']) for g in graphs),
      'eligible_RSM_tests':eligible,'RSM_refutations':refutations,
      'whole_or_induced_ORIGINAL_candidates':[g['id'] for g in graphs if g['candidates']],
      'hereditary_ORIGINAL_candidates':hs['candidates'],
      'all_edge_factorizations':sum(len(g['edge_splits']) for g in graphs),
      'graph_mask_recounts':sum(g['distinct_counted_masks'] for g in graphs),
      'proper_subset_occurrences':hs['proper_subset_occurrences'],
      'proper_signature_occurrences':hs['proper_signature_occurrences'],
      'direct_coverage_regression_subset_occurrences':cs['all_subsets_checked'],
      'extra_regression_graphs_not_in_main_batch':cs['extra_regression_graphs'],
      'exclusions':json.loads((root/'edge_summary.json').read_text())['excluded']+hs['excluded'],
      'scope_note':'Counts are record/occurrence counts, not globally new or unlabelled-isomorphism counts. Zero residual tests means no nonvacuous support for J_H or RSM.',
      'off_residual_star':{'i':1,'j':2,'U':star['U'],'D':star['D'],**off},
      'new30_LC_control':{'k':16,'difference':-219,'unimodal':True}}
    for name,data in [('integrated_summary.json',summary),('graph_status.json',rows),('bad_leaf_hereditary.json',compact)]:
        (root/name).write_text(json.dumps(data,indent=2)+'\n')
    evidence={str(p.name):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
       for p in sorted(root.glob('*.json')) if p.name not in ['CLEAN_REPLAY.json','DATA_FILES.json']}
    (root/'DATA_FILES.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
