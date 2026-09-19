#!/usr/bin/env python3
"""One fixed, structure-directed round after terminal-center alignment fails.
No random growth; no exhaustive all-forest claim; full outside components retained.
"""
from pathlib import Path
from math import comb
import json, hashlib
from forest_exact import *
BASE=Path(__file__).resolve().parents[1]

def path_poly(n):
    assert n>=0
    return tuple(comb(n-k+1,k) for k in range((n+1)//2+1))

def subtract(a,b):
    return trim([(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def main():
    inp=json.loads((BASE/'sources/selected_external_trees.json').read_text())
    ts={t['index']:parent_graph(t['par']) for t in inp['trees']}
    h=hub_tree([10,10,10]); hc=canonical(h)
    seeds=[
        ('balanced_terminal_obstruction',h),
        ('asymmetric_same_order',hub_tree([4,10,16])),
        ('larger_exterior_hub',hub_tree([10,10,16])),
        ('path_core_three',hub_tree([10,10,10],'path')),
        ('path_core_four',hub_tree([4,10,16,22],'path')),
        ('four_hub_exterior',hub_tree([4,4,10,16])),
        ('two_large_components',union(h,hub_tree([8,8,8]))),
        ('one_large_two_H2_small',union(h,ts[1],ts[145])),
        ('two_large_one_small',union(h,hub_tree([12,12,12]),ts[0]))
    ]
    records=[]; seen={}; proposals=[]; ops_seen=set(); duplicate_types=0; comparisons=0; formulas=0
    def accept(adj,origin,hereditary='UNKNOWN'):
        nonlocal duplicate_types,comparisons,formulas
        code=canonical(adj); key=hashlib.sha256(code.encode()).hexdigest()
        proposals.append({'canonical_sha256':key,'origin':origin})
        if key in seen:
            duplicate_types+=1; return seen[key]
        rec=profile(adj); count=deletion_counter(adj); full=(1<<len(adj))-1
        assert tuple(rec['P'])==count(full)
        for vr in rec['vertices']:
            v=vr['v']; rest=full&~(1<<v); closed=rest
            for w in adj[v]: closed&=~(1<<w)
            assert tuple(vr['A'])==count(rest)
            assert tuple(vr['B'])==shift(count(closed))
            comparisons+=2
        rec.update(id='t%03d'%len(records),canonical_sha256=key,origin=origin,HEREDITARY=hereditary)
        rec['terminal_spiders']=terminal_spiders(adj)
        checks=[]
        for t in rec['terminal_spiders']:
            v=t['center']; w=t['exterior_neighbor']; arms=t['arms']
            occupied={v}|{u for a in arms for u in a}; keep=full
            for u in occupied: keep&=~(1<<u)
            M=count(keep); B=count(keep&~(1<<w)) if w is not None else M
            a=M; b=shift(B)
            for arm in arms:
                a=conv(a,path_poly(len(arm))); b=conv(b,path_poly(len(arm)-1))
            assert a==tuple(rec['vertices'][v]['A']) and b==tuple(rec['vertices'][v]['B'])
            assert add(a,b)==tuple(rec['P']); formulas+=1
            # Exact whole-arm deletion/cut relation for one representative arm.
            arm=min(arms,key=lambda x:(len(x),x)); E=M; L=shift(B)
            for other in arms:
                if other is arm: continue
                E=conv(E,path_poly(len(other))); L=conv(L,path_poly(len(other)-1))
            arm_mask=sum(1<<u for u in arm)
            deleted=count(full&~arm_mask)
            assert deleted==add(E,L)
            al,bl=path_poly(len(arm)),path_poly(len(arm)-1)
            cut=conv(al,deleted); corr=conv(subtract(al,bl),L)
            assert subtract(cut,rec['P'])==corr and min(corr)>=0
            checks.append({'center':v,'arm':arm,'arm_deleted_P':deleted,'detached_cut_P':cut,
                           'correction':corr,'arm_deleted_valleys':valleys(deleted),'cut_valleys':valleys(cut)})
        rec['exact_arm_checks']=checks
        records.append(rec); seen[key]=rec
        if rec['valleys'] or not rec['LOCAL']:
            (BASE/'certificates/direct_incident.json').write_text(json.dumps(rec,indent=2)+'\n')
            raise RuntimeError('Material original/conditional candidate: stop ordinary expansion for diagnosis')
        return rec
    for name,adj in seeds:
        accept(adj,{'kind':'fixed_seed','name':name},'PROVED_BY_H64_COMPRESSION' if canonical(adj)==hc else 'UNKNOWN')
    # Expand each fixed seed once at one marked terminal center/arm.
    for name,adj in seeds:
        base=seen[hashlib.sha256(canonical(adj).encode()).hexdigest()]
        candidates=terminal_spiders(adj)
        max_comp=max(components(adj),key=len); candidates=[t for t in candidates if t['center'] in max_comp]
        t=max(candidates,key=lambda z:(base['vertices'][z['center']]['local_gap'],-z['center']))
        v=t['center']; arm=min(t['arms'],key=lambda a:(len(a),a)); first,last=arm[0],arm[-1]
        keep=set(range(len(adj))); ed=edges_of(adj)
        variants=[
          ('delete_whole_arm',induced(adj,keep-set(arm)),True),
          ('delete_arm_leaf',induced(adj,keep-{last}),True),
          ('extend_arm_by_one',attach_path(adj,last,1),False),
          ('detach_arm',graph(len(adj),[(a,b) for a,b in ed if {a,b}!={v,first}]),False)
        ]
        w=t['exterior_neighbor']
        if w is not None:
            variants.append(('move_arm_to_exterior_neighbor',graph(len(adj),[(a,b) for a,b in ed if {a,b}!={v,first}]+[(w,first)]),False))
        for op,new,is_induced in variants:
            opkey=(base['canonical_sha256'],v,tuple(arm),op)
            assert opkey not in ops_seen; ops_seen.add(opkey)
            hered='PROVED_AS_INDUCED_SUBFOREST_OF_H64' if canonical(adj)==hc and is_induced else 'UNKNOWN'
            accept(new,{'kind':'one_marked_operation','seed':base['id'],'name':name,'center':v,'arm':arm,'operation':op},hered)
    summary={
      'status':'FIXED_STRUCTURAL_ROUND_COMPLETE_NO_ORIGINAL_COUNTEREXAMPLE',
      'fixed_seeds':len(seeds),'distinct_expanded_seed_position_operations':len(ops_seen),
      'proposals':len(proposals),'accepted_nonisomorphic_forests':len(records),'duplicate_canonical_types':duplicate_types,
      'maximum_order':max(r['n'] for r in records),
      'all_P_dual_recounted':len(records),'all_vertex_A_B_dual_recounted':comparisons,
      'terminal_spider_exact_boundary_checks':formulas,
      'unimodal_forests':sum(r['unimodal'] for r in records),
      'non_log_concave_forests':sum(not r['log_concave'] for r in records),
      'disconnected_forests':sum(len(r['component_orders'])>1 for r in records),
      'forests_with_at_least_two_large_components':sum(sum(n>=31 for n in r['component_orders'])>=2 for r in records),
      'HEREDITARY_proved':sum(r['HEREDITARY']!='UNKNOWN' for r in records),
      'HEREDITARY_unknown':sum(r['HEREDITARY']=='UNKNOWN' for r in records),
      'max_D_minus_U':max(r['D']-r['U'] for r in records),
      'residual_graphs':sum(bool(r['residual_pairs']) for r in records),
      'residual_pairs':sum(len(r['residual_pairs']) for r in records),
      'eligible_RSM_tests':0,'original_counterexamples':0,
      'global_minimality':'NOT_CLAIMED','universal_absence':'NOT_CLAIMED',
      'core_gap_reduced':False,
      'scope':'One fixed round around an explicitly failed terminal elimination shortcut; not an order census or all-boundary coverage.'
    }
    (BASE/'certificates/directed_search_full.json').write_text(json.dumps({'summary':summary,'proposals':proposals,'records':records},indent=2)+'\n')
    (BASE/'certificates/directed_search_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
