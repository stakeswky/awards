"""Independent re-verification (Python, exact) of every tree printed by cma as EX_NOLEAF or
EX_NOALIGN: rebuild the tree from its parent array, recompute I(T) and, for every vertex v,
M(I(T-v)) and M(I(T-N[v])) with the deletion DP of modelib.py, and confirm
  (i) the parent array is a tree on n vertices and I(T) matches the printed sequence,
  (ii) no leaf is aligned,
  (iii) some vertex is aligned (with the reported degree for the first one found by degree order),
  (iv) every leaf v has M(I(T-v)) at or one step left of M(I(T))  (S2).
Also records the degrees and structure of the aligned vertices. usage: reverify_noleaf.py log..."""
import sys, re, json, collections
from modelib import *
out = []; problems = 0; per_n = collections.Counter(); aligned_deg = collections.Counter()
for f in sys.argv[1:]:
    for line in open(f):
        if not line.startswith('EX_'): continue
        tag = line.split()[0]
        par = [int(x) for x in re.search(r'parents=(\S+)', line).group(1).split(',')]
        p_c = [int(x) for x in re.search(r'p=(\S+)', line).group(1).split(',')]
        n = len(par); nb = neighbours(par)
        is_tree = par[0] == -1 and all(0 <= par[v] < v for v in range(1, n))
        p = indep_poly_del(par); t1, t2, uni = mode_set(p)
        rows = []; leaf_aligned = False; s2_ok = True; first = None
        for v in sorted(range(n), key=lambda v: (len(nb[v]), v)):
            d, MA, MC = split_alignment(par, v, nb)
            rows.append((v, len(nb[v]), d))
            if len(nb[v]) == 1:
                if d <= 1: leaf_aligned = True
                if sshift := (MA[0] - t2 if MA[0] > t2 else (-(t1 - MA[1]) if t1 > MA[1] else 0)):
                    if sshift not in (-1, 0): s2_ok = False
            if d <= 1 and first is None: first = (v, len(nb[v]))
        ok = is_tree and p == p_c and uni and (not leaf_aligned) and (first is not None) and s2_ok
        m = re.search(r'aligned_vertex_degree=(\d+)', line)
        if m and first and int(m.group(1)) != first[1]: ok = False
        problems += not ok; per_n[n] += 1
        if first: aligned_deg[first[1]] += 1
        supports = sorted(set(len(nb[nb_v]) for v in range(n) if len(nb[v]) == 1 for nb_v in nb[v]))
        out.append(dict(tag=tag, n=n, parents=par, ok=ok, unimodal=uni, mode=(t1, t2), first_aligned=first,
                        aligned_vertices=[(v, dg) for v, dg, d in rows if d <= 1], support_degrees=supports, min_support_degree=min(supports)))
print('examples', len(out), 'problems', problems, 'by n', dict(sorted(per_n.items())), 'first aligned vertex degree', dict(sorted(aligned_deg.items())))
print('min support degree over these trees:', min(o['min_support_degree'] for o in out) if out else None,
      '; trees with a support of degree 2:', sum(o['min_support_degree'] == 2 for o in out),
      '; of degree 3:', sum(o['min_support_degree'] == 3 for o in out))
json.dump(out, open('trees_without_aligned_leaf_n19_26.json', 'w'))
