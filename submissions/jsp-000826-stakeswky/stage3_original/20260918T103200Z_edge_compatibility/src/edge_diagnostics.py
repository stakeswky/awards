#!/usr/bin/env python3
"""Exact, bounded, real-forest diagnostics. No universal claim from sampling."""
import argparse
import itertools
import json
import time
from pathlib import Path
from forest_counts import Forest, add, convolution, pad, modes, valley, vertices


class Table:
    def __init__(self):
        self.values = []
        self.ids = {}

    def put(self, seq):
        seq = tuple(seq)
        if seq not in self.ids:
            self.ids[seq] = len(self.values)
            self.values.append(seq)
        return self.ids[seq]


def union(identifier, rows):
    n, edges = 0, []
    for row in rows:
        edges.extend((n+u, n+v) for u, v in row['edges'])
        n += row['n']
    return {'id': identifier, 'n': n, 'edges': edges, 'origin': 'new'}


def side(c, m):
    n, edges = 1, []
    for _ in range(m):
        root = n
        n += 1
        edges.append((0, root))
        for _ in range(c):
            edges.append((root, n))
            n += 1
    return {'n': n, 'edges': edges}


def generate(controls):
    types = [(1,2),(2,2),(2,4),(3,3),(4,4),(6,6)]
    new = []
    new30 = next(r for r in controls if r['id'] == 'new30')
    p3 = {'n': 3, 'edges': [(0,1),(1,2)]}
    for a in range(len(types)):
        for b in range(a, len(types)):
            left, right = side(*types[a]), side(*types[b])
            for length in [1,3]:
                row = union(f'join-{a}-{b}-length{length}', [left, right])
                path = [0] + list(range(row['n'], row['n']+length-1)) + [left['n']]
                row['edges'].extend(zip(path, path[1:]))
                row['n'] += length-1
                row['construction'] = {'left': types[a], 'right': types[b],
                                       'joining_path': path}
                new.append(row)
                if a == b and length == 1:
                    new.extend([union(row['id']+'+P3', [row,p3]),
                                union(row['id']+'+new30', [row,new30])])
    new.extend([{'id':'P4','n':4,'edges':[(0,1),(1,2),(2,3)],'origin':'new'},
                {'id':'double-star22','n':6,'edges':[(0,1),(0,2),(0,3),(1,4),(1,5)],'origin':'new'}])
    assert len(new) == 56
    return controls + new


def component(g, start, blocked_edge=None):
    found, stack = 0, [start]
    while stack:
        v = stack.pop()
        if found >> v & 1:
            continue
        found |= 1 << v
        for w in vertices(g.adj[v]):
            if blocked_edge is not None and {v,w} == set(blocked_edge):
                continue
            if not (found >> w & 1):
                stack.append(w)
    return found


def describe(seq, table):
    ok = valley(seq) is None
    return {'poly': table.put(seq), 'unimodal': ok,
            'mode': list(modes(seq)) if ok else None}


def delta(seq, k):
    return (seq[k+1] if k+1 < len(seq) else 0) - (seq[k] if k < len(seq) else 0)


def leaf_test(x, y, i, j):
    for e, l, order in [(x,y,'X_early'),(y,x,'Y_early')]:
        di, dj, li, lj = delta(e,i), delta(e,j), delta(l,i), delta(l,j)
        if di < 0 and dj <= 0 and li >= 0 and lj > 0:
            q = li*(-dj)-lj*(-di)
            return {'polarized': True, 'order': order, 'Q': q,
                    'dE_i':di, 'dE_j':dj, 'dL_i':li, 'dL_j':lj,
                    'blocks_valley': q >= 0}
    return {'polarized': False, 'blocks_valley': True}


def analyze(row, table, checkpoint):
    g = Forest(row['n'], row['edges'], checkpoint)
    cache = {}
    candidates = []

    def count(mask):
        checkpoint()
        if mask not in cache:
            p = g.recount(mask, brute=(g.n <= 7))
            cache[mask] = p
            if valley(p) is not None:
                candidates.append({'mask': mask, 'counts': table.put(p),
                                   'valley': valley(p)})
        return cache[mask]

    n, full = g.n, g.full
    p = count(full)
    splits, arrays = [], []
    for v in range(n):
        a = pad(count(full & ~(1<<v)), n)
        b = pad((0,)+count(full & ~((1<<v)|g.adj[v])), n)
        assert add(a,b) == p
        ra, rb = describe(a,table), describe(b,table)
        item = {'v':v, 'A':ra, 'B':rb, 'degree':g.adj[v].bit_count()}
        if ra['unimodal'] and rb['unimodal']:
            am,bm = ra['mode'],rb['mode']
            item.update(u=min(am[1],bm[1]), d=max(am[0],bm[0]))
        splits.append(item)
        arrays.append((a,b))
    for k in range(n+1):
        assert sum(ab[1][k] for ab in arrays) == k*p[k]
        assert sum(ab[0][k] for ab in arrays) == (n-k)*p[k]
    comps = []
    remaining = full
    while remaining:
        mask = component(g, next(vertices(remaining)))
        comps.append(list(vertices(mask)))
        remaining &= ~mask
    edges = []
    for u,v in g.edges:
        c = count(full & ~((1<<u)|(1<<v)))
        cp = pad(c,n)
        bu,bv = arrays[u][1], arrays[v][1]
        assert add(add(cp,bu),bv) == p
        assert add(cp,bv) == arrays[u][0]
        assert add(cp,bu) == arrays[v][0]
        mu,mv = component(g,u,(u,v)), component(g,v,(u,v))
        assert not mu & mv
        mr = full & ~(mu|mv)
        xu = count(mu & ~(1<<u))
        yu = (0,)+count(mu & ~((1<<u)|g.adj[u]))
        xv = count(mv & ~(1<<v))
        yv = (0,)+count(mv & ~((1<<v)|g.adj[v]))
        r = count(mr)
        prod = lambda aa,bb: pad(convolution(r,convolution(aa,bb)),n)
        assert prod(xu,xv) == cp
        assert prod(yu,xv) == bu
        assert prod(xu,yv) == bv
        # Unit-weight endpoint removal injections, never a coefficient cancellation.
        xcp = pad((0,)+c, n)
        assert all(bu[k] <= xcp[k] and bv[k] <= xcp[k] for k in range(n+1))
        edges.append({'u':u,'v':v,'C':describe(cp,table),
                      'Tu':list(vertices(mu)),'Tv':list(vertices(mv)),
                      'R_mask':mr,'R':table.put(r),'Xu':table.put(xu),'Yu':table.put(yu),
                      'Xv':table.put(xv),'Yv':table.put(yv)})
    local = all(s['A']['unimodal'] and s['B']['unimodal'] for s in splits)
    result = dict(row)
    result.update(edges=g.edges, components=comps, P=describe(p,table), vertices=splits,
                  edge_splits=edges, LOCAL=local, HEREDITARY='UNKNOWN',
                  counted_masks=[{'mask':m,'poly':table.put(q)} for m,q in sorted(cache.items())],
                  distinct_counted_masks=len(cache), candidates=candidates,
                  delta=[delta(p,k) for k in range(n)], residual_pairs=[])
    if n and local:
        U,D = max(s['u'] for s in splits), min(s['d'] for s in splits)
        result.update(U=U,D=D,D_minus_U=D-U)
        assert all(delta(p,k) >= 0 for k in range(U))
        assert all(delta(p,k) <= 0 for k in range(D,n))
        if D <= U+1:
            assert valley(p) is None
        for i,j in itertools.combinations(range(U,D),2):
            leaves=[]
            for leaf in range(n):
                if g.adj[leaf].bit_count() != 1:
                    continue
                w=next(vertices(g.adj[leaf]))
                x,y=arrays[w]
                leaves.append({'leaf':leaf,'support':w,**leaf_test(x,y,i,j)})
            result['residual_pairs'].append({'i':i,'j':j,'leaves':leaves,
                           'all_leaves_fail': bool(leaves) and not any(a['blocks_valley'] for a in leaves),
                           'original_RSM_premises':'HEREDITARY_UNKNOWN'})
    g._deletion.cache_clear()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--controls',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    controls=json.loads(args.controls.read_text())
    rows=generate(controls)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'inputs.json').write_text(json.dumps(rows,indent=2)+'\n')
    table=Table();results=[];excluded=[];start=time.monotonic()
    for idx,row in enumerate(rows):
        before=time.monotonic()
        def checkpoint():
            if time.monotonic()-before > 10:
                raise TimeoutError('per-graph 10-second limit')
            if time.monotonic()-start > 120:
                raise TimeoutError('batch 120-second limit')
        try:
            r=analyze(row,table,checkpoint)
        except TimeoutError as exc:
            excluded.append({'id':row['id'],'reason':str(exc)})
            continue
        results.append(r)
        print('completed',r['id'],'n',r['n'],'U,D',r.get('U'),r.get('D'),flush=True)
        if r['candidates']:
            excluded.extend({'id':rr['id'],'reason':'ORIGINAL-candidate stop'} for rr in rows[idx+1:])
            break
    summary={'status':'COMPLETED_WITH_SCOPE','input_graphs':len(rows),
             'completed_graphs':len(results),'inherited_controls':sum(r['origin']=='inherited_control' for r in results),
             'new_graphs':sum(r['origin']=='new' for r in results),'LOCAL_graphs':sum(r['LOCAL'] for r in results),
             'HEREDITARY_graphs':0,'HEREDITARY_note':'Separate complete-subset certificate required',
             'residual_graphs':sum(r.get('D_minus_U',0)>=2 for r in results),
             'residual_pairs':sum(len(r['residual_pairs']) for r in results),
             'eligible_RSM_tests':0,'max_D_minus_U':max(r.get('D_minus_U',0) for r in results),
             'all_edge_factorizations':sum(len(r['edge_splits']) for r in results),
             'distinct_graph_mask_recounts':sum(r['distinct_counted_masks'] for r in results),
             'whole_or_induced_candidates':[r['id'] for r in results if r['candidates']],
             'excluded':excluded,'universal_claim':False}
    (args.out/'edge_material.json').write_text(json.dumps({'polynomials':table.values,'graphs':results},separators=(',',':'))+'\n')
    (args.out/'edge_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)
    print('elapsed_seconds',round(time.monotonic()-start,6),flush=True)

if __name__=='__main__':
    main()
