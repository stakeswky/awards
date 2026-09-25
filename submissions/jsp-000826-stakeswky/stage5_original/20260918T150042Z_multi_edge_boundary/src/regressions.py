"""Targeted regression and exact replay preconditions; no finite-range theorem."""
import argparse,json
from pathlib import Path
from fractions import Fraction
from forest import validate,modes,unimodal,PackedForest
from multi_edge import defect,cut_polynomial,root_bundle,partial_cut
from boundary import canonical_forest
from search import nu
from checks import dump


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out)
    invalid=[(-1,[]),(2,[(0,0)]),(2,[(0,1),(1,0)]),(2,[(0,2)]),(3,[(0,1),(1,2),(2,0)])]
    for n,e in invalid:
        try:validate(n,e)
        except ValueError:pass
        else:raise AssertionError('invalid graph accepted')
    assert nu((1,))[0] is None and nu((1,1))[0] is None
    assert nu((1,3,2,2,3,0,0))[0]==Fraction(1,5)
    assert nu((1,2,2,1,0,0))[0]==Fraction(-1,3)
    assert nu((1,2,2,2,1,0,0))[0]==0
    assert modes((0,1,2,2,1,0))==(2,3)
    assert not unimodal((1,3,2,2,3,0))
    mats=json.loads((out/'interaction_material.json').read_text());ncanon=0
    for g in mats:
        n=g['n'];rev=[(n-1-u,n-1-v) for u,v in g['edges']]
        assert canonical_forest(n,g['edges'])==canonical_forest(n,rev);ncanon+=1
    bw=json.loads((out/'boundary_witness.json').read_text())
    assert canonical_forest(bw['n'],bw['left']['edges'])!=canonical_forest(bw['n'],bw['right']['edges'])
    sw=json.loads((out/'search_summary.json').read_text());records=json.loads((out/'discovery_records.json').read_text())
    codes=[canonical_forest(g['n'],g['edges']) for g in records]
    assert len(codes)==len(set(codes))==sw['accepted_nonisomorphic_forests']
    attempts=json.loads((out/'discovery_attempts.json').read_text());by_id={g['id']:g for g in records}
    for r in attempts:
        if r['status']=='ISOMORPHIC_NEW_EDGE_LIST':
            old=by_id[r['existing']]
            assert canonical_forest(r['n'],r['edges'])==canonical_forest(old['n'],old['edges'])
    assert len(attempts)==sw['proposals']
    assert sw['proposals']==sw['distinct_proposed_edge_lists']+sw['duplicate_proposals']
    assert sw['distinct_proposed_edge_lists']==len(records)+sw['isomorphic_new_edge_list_proposals']
    assert len({s for row in sw['rounds'] for s in row['seeds']})==sw['expanded_seeds']
    # Independently recompute the selected nu witness by direct pair fractions.
    for g in records:
        p=g['P'];alpha=max(k for k,z in enumerate(p) if z)
        vals=[min(Fraction(p[i]-p[i+1],p[i]+p[i+1]),Fraction(p[j+1]-p[j],p[j]+p[j+1]))
              for i in range(alpha) for j in range(i+1,alpha)]
        assert (str(max(vals)) if vals else None)==g['nu']
    derived={'edge_pair_whole':0,'partial_whole':0,'partial_selected':0,'C_H':0}
    for filename in ['interaction_material.json','discovery_material.json']:
        for g in json.loads((out/filename).read_text()):
            for row in g['edge_pairs']:
                derived['edge_pair_whole']+=1;assert unimodal(row['P_cut']), ('DERIVED_COUNTEREXAMPLE',g['id'],row['edge_indices'])
            for bundle in g['partial_cuts']:
                for row in bundle['states']:
                    derived['partial_whole']+=1;derived['partial_selected']+=1
                    assert unimodal(row['P_cut']) and unimodal(row['B']), ('DERIVED_COUNTEREXAMPLE',g['id'],bundle['v'],row['J'])
            for row in g['edge_data']:
                for k in ['C','H']:
                    derived['C_H']+=1;assert unimodal(row[k]), ('DERIVED_COUNTEREXAMPLE',g['id'],row['edge'],k)
    summary=dict(derived_forest_arrays_checked=derived,derived_counterexamples=[],invalid_graphs_rejected=5,plateau_score_controls=7,
        relabeling_controls=ncanon,nonisomorphic_collision_pair_checked=True,
        discovery_canonical_types_checked=len(records),proposal_accounting_pass=True,
        nu_full_pair_recounts=len(records),status='PASS')
    dump(out/'regression_summary.json',summary);print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
