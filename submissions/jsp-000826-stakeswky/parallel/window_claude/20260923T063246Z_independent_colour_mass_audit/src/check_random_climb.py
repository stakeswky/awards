"""Negative control: unstructured adversarial search. Simulated annealing on random
trees (n in {30,36,42,50,60}; three start styles; 3 seeds each; 1500 subtree
prune-and-regraft steps) maximising max_j log(Dmass/S) over the middle range.
Fixed seeds; deterministic. Documents that blind search is far weaker than the
structured hub constructions.

Usage: python check_random_climb.py --out DIR [--procs 9]
"""
import argparse
import json
import math
import os
import random
import sys
from collections import deque
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402


def bfs_par(adj):
    order = [0]
    par0 = {0: -1}
    q = deque([0])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in par0:
                par0[y] = x
                order.append(y)
                q.append(y)
    idx = {v: i for i, v in enumerate(order)}
    return [(-1 if par0[v] < 0 else idx[par0[v]]) for v in order]


def score(adj):
    par = bfs_par(adj)
    n = len(par)
    ch = L.children_of(par)
    col = L.colours(par)
    p = L.uni_poly(par, ch)
    if not L.is_unimodal(p):
        return (1e9, dict(NONUNIMODAL=True, p=p, parents=par))
    js, _ = L.domain(p, n, n)
    if not js:
        return (-1e9, None)
    rows = L.biv_rows(par, ch, col)
    best = (-1e9, None)
    for j in js:
        b, a = p[j - 1], p[j]
        S = a * (b - a)
        N, P = L.mass_arrays(rows, j)
        dm = sum(max(x - y, 0) for x, y in zip(N, P))
        if S == 0:
            val = 1e6 if dm > 0 else -1e9
        elif dm == 0:
            val = -60.0
        else:
            val = math.log(dm / S)
        if val > best[0]:
            best = (val, dict(j=j, S=S, Dmass=dm, n=n, parents=par))
    return best


def random_tree(n, rng, style):
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        if style == 'recursive':
            u = rng.randrange(v)
        elif style == 'bushy':
            u = rng.randrange(max(1, v // 6))
        else:
            u = max(0, v - 1 - int(rng.expovariate(0.3)))
        adj[u].append(v)
        adj[v].append(u)
    return adj


def mutate(adj, rng):
    n = len(adj)
    new = [list(a) for a in adj]
    x = rng.randrange(n)
    if not new[x]:
        return new
    y = rng.choice(new[x])
    side = {y}
    st = [y]
    while st:
        z = st.pop()
        for w in new[z]:
            if w != x and w not in side:
                side.add(w)
                st.append(w)
    if len(side) > n // 2 and rng.random() < 0.5:
        return new
    outside = [v for v in range(n) if v not in side]
    t = rng.choice(outside)
    if t == x:
        return new
    new[x].remove(y)
    new[y].remove(x)
    new[t].append(y)
    new[y].append(t)
    return new


def chain(job):
    seed, n, style, steps = job
    rng = random.Random(seed)
    adj = random_tree(n, rng, style)
    cur = score(adj)
    best = (cur[0], cur[1])
    temp = 1.0
    for _ in range(steps):
        cand = mutate(adj, rng)
        if rng.random() < 0.3:
            cand = mutate(cand, rng)
        sc = score(cand)
        if sc[0] >= cur[0] or rng.random() < math.exp((sc[0] - cur[0]) / max(temp, 1e-3)):
            adj, cur = cand, sc
            if cur[0] > best[0]:
                best = (cur[0], cur[1])
        temp *= 0.998
    rec = best[1]
    return dict(seed=seed, n=n, style=style, steps=steps, best_log_Dmass_over_S=best[0],
                best=None if rec is None else dict((k, rec[k]) for k in rec if k != 'parents'),
                best_parents=None if rec is None else rec.get('parents'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--procs', type=int, default=9)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    jobs = []
    s = 0
    for n in (30, 36, 42, 50, 60):
        for style in ('recursive', 'bushy', 'pathlike'):
            for _ in range(3):
                jobs.append((1000 + s, n, style, 1500))
                s += 1
    with Pool(args.procs) as pool:
        res = pool.map(chain, jobs, chunksize=1)
    nonuni = [r for r in res if r['best'] and r['best'].get('NONUNIMODAL')]
    finite = [r['best_log_Dmass_over_S'] for r in res if -1e8 < r['best_log_Dmass_over_S'] < 1e5]
    top = max(finite) if finite else None
    print('chains', len(res), 'nonunimodal found', len(nonuni), 'max Dmass/S found', math.exp(top) if top is not None else None)
    with open(os.path.join(args.out, 'random_climb.json'), 'w') as fh:
        json.dump(dict(chains=res, max_Dmass_over_S=(math.exp(top) if top is not None else None), nonunimodal_found=len(nonuni)),
                  fh, sort_keys=True, separators=(',', ':'), default=str)
        fh.write('\n')


if __name__ == '__main__':
    main()
