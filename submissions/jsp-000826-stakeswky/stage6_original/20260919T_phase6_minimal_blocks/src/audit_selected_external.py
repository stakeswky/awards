#!/usr/bin/env python3
from pathlib import Path
from math import comb
import json
from forest_exact import *
BASE=Path(__file__).resolve().parents[1]

def main():
    data=json.loads((BASE/'sources/selected_external_trees.json').read_text()); ts={}
    for t in data['trees']:
        adj=parent_graph(t['par']); a=independence_dp(adj); b=deletion_counter(adj)((1<<len(adj))-1)
        assert a==b==tuple(t['seq'])
        assert unimodal(a) and not logconcave(a)
        ts[t['index']]=(adj,a)
    for t in data['selected_H2_pairs']:
        i,j=t['indices']; p=conv(ts[i][1],ts[j][1]); adj=union(ts[i][0],ts[j][0])
        assert p==packed_conv(ts[i][1],ts[j][1])==tuple(t['seq'])
        assert p==deletion_counter(adj)((1<<len(adj))-1)
        assert unimodal(p) and not logconcave(p)
    # These arithmetic equalities check transcription only, not census truth.
    assert 2+19+7+121==149 and comb(150,2)==11175
    assert 1+149+97==247 and 11175+10823==21998
    result={'status':'PASS_SELECTED_RECORDS_AND_TRANSCRIPTION_ONLY',
      'fresh_tree_full_coefficients_recounted':3,'fresh_H2_full_products_recounted':2,
      'external_census_completeness':'ASSUMED_PINNED_EXTERNAL_INPUT_NOT_RERUN',
      'external_full_H2_H3_computation':'ASSUMED_PINNED_EXTERNAL_INPUT_NOT_RERUN',
      'H1_external':149,'H2_external':97,'H3_external':0,
      'small_component_index_bound_conditional':247,
      'small_index_classes':['empty tuple','149 singleton bank indices','97 H2 pairs with repetitions allowed'],
      'large_component_count_bound':None,'large_component_order_bound':None,
      'scope':'Small-component submultiset only; NOT a finite enumeration of external boundaries or all remaining forests.'}
    (BASE/'certificates/external_selected_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
