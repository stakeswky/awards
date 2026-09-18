#!/usr/bin/env python3
"""Require complete fresh arithmetic certificates; never mark formal verification."""
import argparse,hashlib,json,platform
from math import comb
from pathlib import Path

def main(root,out):
    def read(name):return json.loads((root/name).read_text())
    totals=[0,0,0]
    for t in range(4,24):
        p=read(f'envelope-primary-{t:02}.json');r=read(f'envelope-replay-{t:02}.json')
        for x in (p,r):
            if x['t']!=t or x['status']!='EXACT_ALL_PASS':raise AssertionError('envelope status')
            expected=sum(2*(S+t)-3 for S in range(3*t,17*t+1))
            if x['interior_cases']!=expected:raise AssertionError('domain count')
        for key in ['canonical_L_sha256','condition_domain_sha256','interior_cases',
                    'nonzero_neighbor_conditions','zero_neighbor_cases','S_min','S_max','epsilon']:
            if p[key]!=r[key]:raise AssertionError(('replay mismatch',t,key))
        for i,k in enumerate(['interior_cases','nonzero_neighbor_conditions','zero_neighbor_cases']):totals[i]+=p[k]
    a=read('blocks-primary.json');b=read('blocks-replay.json')
    for v in (a,b):
        if v['status']!='EXACT_ALL_PASS' or v['palette_size']!=59 or v['total_multisets']!=37819:
            raise AssertionError('block completeness')
        if v['multisets']!={str(t):comb(58+t,t) for t in (1,2,3)}:raise AssertionError('prefix domain')
    for key in ('canonical_branch_sha256','canonical_multiset_sha256','block_ULC_inequalities','prefix_LC_inequalities'):
        if a[key]!=b[key]:raise AssertionError(('block replay',key))
    tail=read('tail.json');graphs=read('graphs.json')
    if tail['status']!='EXACT_ALL_PASS' or tail['prefix_checks']!=109 or tail['translated_coefficients_ascending']!=[3672,38954,506]:
        raise AssertionError('tail completeness')
    if graphs['original_counterexamples'] or graphs['v4']['LC_margin']!=-219 or not graphs['v4']['unimodal']:
        raise AssertionError('unexpected graph finding; review before delivery')
    result={'status':'COMPLETE_EXACT_CERTIFICATES_PASS','python':platform.python_version(),
            'envelope_interior_cases':totals[0],'envelope_nonzero_neighbor_conditions':totals[1],
            'envelope_zero_neighbor_cases':totals[2],'all_20_parameter_slices_replayed':True,
            'prefix_multisets':37819,'block_multisets':37760,
            'prefix_LC_inequalities':a['prefix_LC_inequalities'],'block_ULC_inequalities':a['block_ULC_inequalities'],
            'tail_prefix_checks':109,'graph_records':graphs['input_records'],
            'whole_and_conditional_counts':graphs['whole_and_conditional_forests_checked'],
            'original_counterexamples_found':0,'formal_verification':'NOT_ESTABLISHED',
            'certificate_files_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest()
                    for f in sorted(root.glob('*.json')) if f.resolve()!=out.resolve()}}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='certificate_files_sha256'}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificates',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();main(a.certificates,a.out)
