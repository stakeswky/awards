"""Bounded targeted actual-forest operations; distinct expanded frontiers."""
import argparse,json
from pathlib import Path
from fractions import Fraction
from itertools import combinations
from forest import *
from checks import dump,material
from boundary import canonical_forest


def nu(p):
    alpha=max(k for k,x in enumerate(p) if x)
    values=[]
    for i in range(alpha):
        for j in range(i+1,alpha):
            assert p[i]+p[i+1]>0 and p[j]+p[j+1]>0
            z=min(Fraction(p[i]-p[i+1],p[i]+p[i+1]),
                  Fraction(p[j+1]-p[j],p[j]+p[j+1]))
            values.append((z,i,j))
    if not values:return None,None
    score,i,j=max(values,key=lambda z:(z[0],-z[1],-z[2]))
    return score,(i,j)


def rank(g):
    q=Fraction(g['nu']) if g['nu'] is not None else Fraction(-2)
    return (g['D']-g['U'] if g['LOCAL'] and g['n'] else -100,q,-g['n'])


def operations(g):
    f=PackedForest(g['n'],g['edges']);n=f.n; es=list(f.edges)
    def sep(v):
        a,b=g['mode_intervals'][v];return max(a[0]-b[1],b[0]-a[1],0)
    targets=sorted(range(n),key=lambda v:(sep(v),v))[:4]
    ops=[]
    for v in targets:
        for shape in (1,4):
            extra=[(v,n)]+([(n,n+k) for k in (1,2,3)] if shape==4 else [])
            ops.append((('graft',v,shape),n+shape,es+extra))
    # At most four oriented internal branches per support, transplanted to
    # its least other neighbor. Tree acyclicity supplies disjoint sides.
    for v in targets:
        internal=[w for w in f.adj[v] if len(f.adj[w])>=2][:4]
        for w in internal:
            other=[z for z in f.adj[v] if z!=w]
            if not other:continue
            z=other[0]; edge=tuple(sorted((v,w)))
            relocated=[e for e in es if e!=edge]+[(z,w)]
            ops.append((('move_internal',v,w,z),n,relocated))
        if len(f.adj[v])>=3:
            # Prefer two internal branches; if unavailable include a leaf.
            ns=sorted(f.adj[v],key=lambda w:(len(f.adj[w])==1,w))[:2]
            removed={tuple(sorted((v,w))) for w in ns}
            ops.append((('two_cut',v,*ns),n,[e for e in es if e not in removed]))
    return ops[:24]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    pinned={g['id']:g for g in json.loads(Path(__file__).with_name('seeds.json').read_text())}
    initial=[pinned[k] for k in ('old23','new30','g0013','g0063')]
    for left,right in [('old23','new30'),('g0013','new30')]:
        l,r=pinned[left],pinned[right]
        initial.append(dict(id='union_'+left+'_'+right,n=l['n']+r['n'],
                        edges=l['edges']+[[u+l['n'],v+l['n']] for u,v in r['edges']]))
    records=[];cache={};types={};attempts=[];expanded=set();expanded_ops=set();rounds=[];incidents=[]
    stop=False
    def accept(n,edges,origin):
        nonlocal stop
        ident=(n,tuple(sorted(tuple(sorted(e)) for e in edges)))
        if n>100:
            attempts.append(dict(origin=origin,status='ORDER_LIMIT',n=n));return
        if ident in cache:
            attempts.append(dict(origin=origin,status='DUPLICATE_EDGE_LIST',existing=cache[ident]['id']));return
        ctype=canonical_forest(n,ident[1])
        if ctype in types:
            cache[ident]=types[ctype]
            attempts.append(dict(origin=origin,status='ISOMORPHIC_NEW_EDGE_LIST',existing=types[ctype]['id'],n=n,edges=ident[1]))
            return
        g=describe(n,ident[1]);g['id']='d%03d'%len(records);g['origin']=origin
        g['canonical_forest_type']=ctype
        assert tuple(g['P'])==deletion_counter(n,ident[1])()
        score,pair=nu(g['P']);g['nu']=str(score) if score is not None else None;g['nu_pair']=pair
        assert (score is not None and score>0)==bool(g['valleys'])
        cache[ident]=g;types[ctype]=g;records.append(g)
        attempts.append(dict(origin=origin,status='NEW_EDGE_LIST',id=g['id']))
        if g['valleys'] or not g['LOCAL'] or g['residual_pairs']:
            incident=material(n,ident[1],g['id'],small=n<=12)
            # A failing local conditional is an actual smaller induced forest.
            incident['extracted_local_failures']=[]
            f=PackedForest(n,ident[1])
            for v in range(n):
                for kind,p,mask in [('A',g['A'][v],f.full&~(1<<v)),('B',g['B'][v],f.full&~f.closed[v])]:
                    if unimodal(p):continue
                    verts=[w for w in range(n) if mask>>w&1];lab={w:k for k,w in enumerate(verts)}
                    subedges=[(lab[u],lab[w]) for u,w in ident[1] if u in lab and w in lab]
                    sub=describe(len(verts),subedges,second=True);assert sub['valleys']
                    incident['extracted_local_failures'].append(dict(vertex=v,kind=kind,graph=sub))
            incidents.append(incident);stop=True
    for g in initial:
        accept(g['n'],g['edges'],dict(kind='initial',source=g['id']))
        if stop:break
    for round_id in range(3):
        if stop:break
        available=sorted([g for g in records if g['id'] not in expanded],key=rank,reverse=True)
        chosen=available[:2]
        others=[g for g in available if g not in chosen]
        if others:chosen.append(min(others,key=lambda g:(g['n'],g['id'])))
        round_record=dict(round=round_id,seeds=[g['id'] for g in chosen],new_records=0,proposals=0)
        before=len(records);before_proposals=len(attempts)
        for g in chosen:
            assert g['id'] not in expanded;expanded.add(g['id'])
            for op,n,edges in operations(g):
                key=(g['id'],op);assert key not in expanded_ops;expanded_ops.add(key)
                accept(n,edges,dict(kind='operation',round=round_id,seed=g['id'],operation=op))
                if stop:break
            if stop:break
        round_record['new_records']=len(records)-before
        round_record['proposals']=len(attempts)-before_proposals;rounds.append(round_record)
    best=sorted(records,key=rank,reverse=True)[:3]
    mats=[material(g['n'],g['edges'],g['id'],small=g['n']<=12) for g in best]
    assert len(attempts)<=222 and len(expanded_ops)==len(set(expanded_ops))
    summary=dict(proposals=len(attempts),distinct_proposed_edge_lists=len(cache),accepted_nonisomorphic_forests=len(records),initial_controls=len(initial),
        new_nonisomorphic_forests=len(records)-min(len(initial),len(records)),
        isomorphic_new_edge_list_proposals=sum(a['status']=='ISOMORPHIC_NEW_EDGE_LIST' for a in attempts),
        duplicate_proposals=sum(a['status']=='DUPLICATE_EDGE_LIST' for a in attempts),
        order_limit_exclusions=sum(a['status']=='ORDER_LIMIT' for a in attempts),
        expanded_seeds=len(expanded),expanded_seed_position_operations=len(expanded_ops),rounds=rounds,
        max_order=max(g['n'] for g in records),max_D_minus_U=max(g['D']-g['U'] for g in records if g['LOCAL']),
        max_nu=str(max(Fraction(g['nu']) for g in records if g['nu'] is not None)),
        whole_P_independently_recounted=len(records),
        all_vertex_material_independently_recounted=len(mats),
        LOCAL_records=sum(g['LOCAL'] for g in records),
        residual_graphs=sum(bool(g['residual_pairs']) for g in records),
        residual_pairs=sum(len(g['residual_pairs']) for g in records),
        eligible_RSM_tests=sum(r['eligible'] for g in mats+incidents for r in g['residual_diagnostics']),
        original_candidates=[g['id'] for g in records if g['valleys']],
        LOCAL_failures=[g['id'] for g in records if not g['LOCAL']],
        stopped_on_incident=stop,stop_reason='INCIDENT' if stop else 'FIXED_THREE_ROUNDS_COMPLETE',
        HEREDITARY='UNKNOWN for discovery except any separately complete small certificates',
        best=[{k:g[k] for k in ['id','n','U','D','nu','nu_pair','origin']} for g in best],
        deduplication='EXACT_FOREST_CANONICAL_TYPE_WITH_SEPARATE_EDGE_LIST_ACCOUNTING',exhaustive=False)
    dump(out/'discovery_records.json',records);dump(out/'discovery_attempts.json',attempts)
    dump(out/'discovery_material.json',mats);dump(out/'incidents.json',incidents)
    dump(out/'search_summary.json',summary);print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
