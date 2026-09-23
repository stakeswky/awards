"""Second implementations / algorithms for the material computations.

(a) tree generator: counts vs OEIS A000055 (n<=18) and pairwise non-isomorphism
    (AHU canonical forms rooted at the centre(s)) for n<=12;
(b) bivariate independence counts: Kronecker DP vs literal enumeration of all
    independent sets, every tree n<=12 (all rows, hence all Dmass values);
(c) leaf-exchange capacities c_t^+/c_t^-: formula (K=F-{u,v}, J=F-N[v]) vs literal
    enumeration of source pairs, with validity and injectivity of every image, every
    tree n<=10, every j, every leaf;
(d) cut-DP delta_e vs Edmonds-Karp max-flow on the aggregated mass network, for all
    cases of (c) and a deterministic middle-range sample for n=14..20;
(e) the vendored project coordinator polynomial code (third_party/graph_primitives.py,
    dict-based rooted recursion and vertex-deletion recursion) vs the Kronecker DP on
    the same sample;
(f) regression against published project values for F14, G25, T26, F56.

Usage: python check_crossvalidation.py --out DIR
"""
import argparse
import json
import os
import sys
from collections import defaultdict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'third_party'))
import e993lib as L  # noqa: E402
import graph_primitives as G  # noqa: E402
from families import hubs, core_tree, edges  # noqa: E402

OEIS_A000055 = [1, 1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159, 7741, 19320, 48629, 123867, 317955,
                823065, 2144505, 5623756, 14828074, 39299897]


def adjacency(par):
    n = len(par)
    adj = [[] for _ in range(n)]
    for v, p in enumerate(par):
        if p >= 0:
            adj[v].append(p)
            adj[p].append(v)
    return adj


def canonical(par):
    adj = adjacency(par)
    n = len(adj)
    deg = [len(a) for a in adj]
    layer = [v for v in range(n) if deg[v] <= 1]
    left = n
    removed = [False] * n
    while left > 2:
        left -= len(layer)
        nxt = []
        for v in layer:
            removed[v] = True
            for w in adj[v]:
                if not removed[w]:
                    deg[w] -= 1
                    if deg[w] == 1:
                        nxt.append(w)
        layer = nxt
    centres = [v for v in range(n) if not removed[v]]

    def enc(v, p):
        return '(' + ''.join(sorted(enc(w, v) for w in adj[v] if w != p)) + ')'
    return min(enc(c, -1) for c in centres)


def literal_rows(par):
    n = len(par)
    adj = [0] * n
    for v, p in enumerate(par):
        if p >= 0:
            adj[v] |= 1 << p
            adj[p] |= 1 << v
    col = L.colours(par)
    Lmask = sum(1 << v for v in range(n) if col[v] == 0)
    sets = []

    def rec(i, chosen):
        if i == n:
            sets.append(chosen)
            return
        rec(i + 1, chosen)
        if not (adj[i] & chosen):
            rec(i + 1, chosen | (1 << i))
    rec(0, 0)
    rows = defaultdict(lambda: defaultdict(int))
    for s in sets:
        rows[bin(s).count('1')][bin(s & Lmask).count('1')] += 1
    return sets, adj, Lmask, rows


def literal_caps(par, j, u, v, sets, adj, Lmask, length):
    by = defaultdict(list)
    for s in sets:
        by[bin(s).count('1')].append(s)
    targets = set(by[j])
    cp = [0] * length
    cm = [0] * length
    images = set()
    mass = lambda x: bin(x & Lmask).count('1')  # noqa: E731
    for a in by.get(j - 1, []):
        for b in by.get(j + 1, []):
            img = None
            if (b >> v) & 1 and not ((a | b) >> u & 1) and not (a >> v & 1):
                img = (a | (1 << u), b & ~(1 << v))
            elif (b >> u) & 1 and not ((a | b) >> v & 1) and not (a & adj[v]):
                img = (a | (1 << v), b & ~(1 << u))
            if img is None:
                continue
            assert img[0] in targets and img[1] in targets
            assert img not in images
            images.add(img)
            t0 = mass(a) + mass(b)
            t1 = mass(img[0]) + mass(img[1])
            assert abs(t1 - t0) == 1
            (cp if t1 == t0 + 1 else cm)[t0] += 1
    return cp, cm


def maxflow_deficit(N, P, cp, cm):
    m = len(N)
    S, T = 2 * m, 2 * m + 1
    cap = defaultdict(int)
    nbr = defaultdict(set)

    def arc(x, y, c):
        cap[(x, y)] += c
        nbr[x].add(y)
        nbr[y].add(x)
    big = sum(N) + 1
    for t in range(m):
        arc(S, t, N[t])
        arc(t, m + t, big)
        arc(m + t, T, P[t])
        if t + 1 < m:
            arc(t, m + t + 1, cp[t])
        if t > 0:
            arc(t, m + t - 1, cm[t])
    flow = 0
    while True:
        prev = {S: None}
        q = deque([S])
        while q and T not in prev:
            x = q.popleft()
            for y in nbr[x]:
                if y not in prev and cap[(x, y)] > 0:
                    prev[y] = x
                    q.append(y)
        if T not in prev:
            break
        path = []
        y = T
        while prev[y] is not None:
            path.append((prev[y], y))
            y = prev[y]
        aug = min(cap[e] for e in path)
        for x, y in path:
            cap[(x, y)] -= aug
            cap[(y, x)] += aug
        flow += aug
    return sum(N) - flow


def coordinator_rows(par):
    n = len(par)
    adj = G.graph(n, edges(par))
    col = L.colours(par)
    mask = (1 << n) - 1
    poly = G.rooted(mask, adj, col)
    return poly, adj, col, mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rep = {}
    # (a) generator
    counts = {}
    for n in range(2, 19):
        c = 0
        forms = set() if n <= 12 else None
        for lv in L.free_trees(n):
            c += 1
            if forms is not None:
                forms.add(canonical(L.parents_from_levels(lv)))
        assert c == OEIS_A000055[n], (n, c)
        if forms is not None:
            assert len(forms) == c, (n, len(forms), c)
        counts[n] = c
    rep['a_generator'] = dict(counts_match_OEIS_A000055_for_n='2..18', pairwise_nonisomorphic_verified_for_n='2..12', counts=counts)
    print('(a) generator counts n=2..18 match OEIS A000055; n<=12 pairwise non-isomorphic', flush=True)
    # (b) bivariate DP vs literal enumeration
    trees_b = rows_b = 0
    for n in range(2, 13):
        for lv in L.free_trees(n):
            par = L.parents_from_levels(lv)
            ch = L.children_of(par)
            rows = L.biv_rows(par, ch, L.colours(par))
            _, _, _, lit = literal_rows(par)
            assert len(rows) == max(lit) + 1
            for r in range(len(rows)):
                assert rows[r] == [lit[r].get(l, 0) for l in range(r + 1)], (lv, r)
                rows_b += 1
            assert [sum(x) for x in rows] == L.uni_poly(par, ch)
            trees_b += 1
    rep['b_bivariate_vs_literal'] = dict(trees=trees_b, rows_compared=rows_b, orders='2..12')
    print('(b) bivariate rows equal literal enumeration:', trees_b, 'trees,', rows_b, 'rows', flush=True)
    # (c)+(d) literal capacities and max-flow, small trees
    cases_c = 0
    for n in range(3, 11):
        for lv in L.free_trees(n):
            par = L.parents_from_levels(lv)
            ch = L.children_of(par)
            col = L.colours(par)
            rows = L.biv_rows(par, ch, col)
            sets, adj, Lmask, _ = literal_rows(par)
            deg = [len(ch[v]) + (par[v] >= 0) for v in range(n)]
            for j in range(1, len(rows) - 1):
                N, P = L.mass_arrays(rows, j)
                for u in range(n):
                    if deg[u] != 1:
                        continue
                    v = par[u] if par[u] >= 0 else ch[u][0]
                    cp, cm = L.leaf_caps(par, ch, col, rows, j, u, v, len(N))
                    lcp, lcm = literal_caps(par, j, u, v, sets, adj, Lmask, len(N))
                    assert (cp, cm) == (lcp, lcm), (lv, j, u)
                    d1 = L.cut_deficit(N, P, cp, cm)
                    d2 = maxflow_deficit(N, P, cp, cm)
                    assert d1 == d2, (lv, j, u, d1, d2)
                    cases_c += 1
    rep['c_d_small'] = dict(orders='3..10', tree_j_leaf_cases=cases_c,
                            checks='literal capacities equal K/J formula; every image valid, injective, mass step +-1; cut DP equals Edmonds-Karp')
    print('(c,d) literal capacities and cut-DP = max-flow on', cases_c, '(tree,j,leaf) cases, n=3..10', flush=True)
    # (d)+(e) middle-range sample n=14..20
    samp = dict(trees=0, positions=0, leaf_checks=0, coordinator_poly_entries=0, deletion_recursion_trees=0)
    for n in range(14, 21):
        k = 0
        taken = 0
        for lv in L.free_trees(n):
            par = L.parents_from_levels(lv)
            p, meta, recs = L.analyse(par, want_leaves=False)
            if not recs:
                continue
            k += 1
            if k % 97 != 1 or taken >= 120:
                continue
            taken += 1
            ch = L.children_of(par)
            col = L.colours(par)
            rows = L.biv_rows(par, ch, col)
            poly, adj, colc, mask = coordinator_rows(par)
            for r in range(len(rows)):
                for l in range(r + 1):
                    assert rows[r][l] == poly.get((l, r - l), 0)
            samp['coordinator_poly_entries'] += len(poly)
            if n <= 16:
                assert G.counter(adj, colc)(mask) == poly
                samp['deletion_recursion_trees'] += 1
            deg = [len(ch[v]) + (par[v] >= 0) for v in range(n)]
            for rec in recs:
                j = rec['j']
                N, P = L.mass_arrays(rows, j)
                Nc = G.conv(G.row(poly, j - 1), G.row(poly, j + 1))
                Pc = G.conv(G.row(poly, j), G.row(poly, j))
                assert sum(max(x - y, 0) for x, y in zip(Nc, Pc)) == rec['Dmass']
                for u in range(n):
                    if deg[u] != 1:
                        continue
                    v = par[u] if par[u] >= 0 else ch[u][0]
                    cp, cm = L.leaf_caps(par, ch, col, rows, j, u, v, len(N))
                    assert L.cut_deficit(N, P, cp, cm) == maxflow_deficit(N, P, cp, cm)
                    samp['leaf_checks'] += 1
                samp['positions'] += 1
            samp['trees'] += 1
    rep['d_e_middle_sample'] = dict(samp, rule='for each n in 14..20: the 1st, 98th, 195th, ... middle-range tree in generation order, at most 120 per n')
    print('(d,e) middle-range sample:', samp, flush=True)
    # (f) published project values
    G25 = (25, [(1, 0), (2, 1), (3, 1), (5, 1), (6, 0), (7, 6), (8, 3), (0, 10), (2, 11), (3, 12), (5, 13), (5, 14), (5, 15), (5, 16),
                (5, 17), (9, 18), (9, 19), (9, 20), (9, 21), (9, 22), (9, 23), (9, 24), (4, 2), (19, 5)])

    def to_par(n, es):
        adj = [[] for _ in range(n)]
        for a, b in es:
            adj[a].append(b)
            adj[b].append(a)
        order = []
        parent = {}
        seen = [False] * n
        for s in range(n):
            if seen[s]:
                continue
            seen[s] = True
            parent[s] = -1
            q = deque([s])
            while q:
                x = q.popleft()
                order.append(x)
                for y in adj[x]:
                    if not seen[y]:
                        seen[y] = True
                        parent[y] = x
                        q.append(y)
        idx = {v: i for i, v in enumerate(order)}
        return [(-1 if parent[v] < 0 else idx[parent[v]]) for v in order]
    expected = [('F14', to_par(*G.F14), 5, 375, 0, {0}),
                ('G25', to_par(*G25), 10, 19283724, 3158, None),
                ('T26', core_tree((3, 4, 4)), 13, 149328, 1472, {1472}),
                ('F56', hubs(5, 10), 26, 28078903272718866773804040, 1181067781056125771069280, {298125284806617840})]
    regress = []
    for name, par, j, S0, D0, deltas in expected:
        n = len(par)
        ch = L.children_of(par)
        col = L.colours(par)
        p = L.uni_poly(par, ch)
        rows = L.biv_rows(par, ch, col)
        N, P = L.mass_arrays(rows, j)
        dm = sum(max(x - y, 0) for x, y in zip(N, P))
        S = p[j] * (p[j - 1] - p[j])
        deg = [len(ch[v]) + (par[v] >= 0) for v in range(n)]
        ds = []
        for u in range(n):
            if deg[u] == 1:
                v = par[u] if par[u] >= 0 else ch[u][0]
                cp, cm = L.leaf_caps(par, ch, col, rows, j, u, v, len(N))
                ds.append(L.cut_deficit(N, P, cp, cm))
        assert S == S0 and dm == D0, (name, S, dm)
        if deltas is not None:
            assert set(ds) == deltas, (name, set(ds))
        if name == 'G25':
            assert min(ds) == 2666 and p == [1, 25, 276, 1807, 7966, 25460, 61894, 118051, 180007, 221739, 221652, 179772, 117831,
                                             61925, 25763, 8316, 2016, 347, 38, 2]
        regress.append(dict(name=name, n=n, j=j, S=S, Dmass=dm, min_delta=min(ds), leaves=len(ds)))
    rep['f_published_regressions'] = regress
    print('(f) published values reproduced:', [(r['name'], r['Dmass'], r['min_delta']) for r in regress], flush=True)
    with open(os.path.join(args.out, 'crossvalidation.json'), 'w') as fh:
        json.dump(rep, fh, sort_keys=True, separators=(',', ':'), default=str)
        fh.write('\n')


if __name__ == '__main__':
    main()
