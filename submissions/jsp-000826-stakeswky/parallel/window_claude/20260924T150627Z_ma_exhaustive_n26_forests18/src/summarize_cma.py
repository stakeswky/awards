"""Summarise cma / cma_full logs into results/cma_summary.json and a markdown table."""
import re, sys, json
A000055 = {19: 317955, 20: 823065, 21: 2144505, 22: 5623756, 23: 14828074, 24: 39299897, 25: 104636890, 26: 279793450}
rows = {}
for f in sys.argv[1:]:
    txt = open(f).read(); m = re.search(r'^RESULT (.*)$', txt, re.M)
    if not m: print('incomplete', f); continue
    d = dict(kv.split('=', 1) for kv in m.group(1).split()); n = int(d['n']); full = 'cma_full' in f
    r = rows.setdefault(n, dict(n=n, OEIS_A000055=A000055.get(n)))
    r.update(trees=int(d['trees']), count_ok=int(d['trees']) == A000055.get(n), leaf_aligned=int(d['leaf_aligned']), no_aligned_leaf=int(d['no_aligned_leaf']),
             no_aligned_vertex=int(d['no_aligned_vertex']), trees_with_degree2_support=int(d['trees_with_degree2_support']),
             leaf_at_degree2_support_aligned=int(d['of_which_leaf_at_degree2_support_aligned']), nonunimodal_pieces=int(d['nonunimodal_pieces']),
             worst_best_dist=int(d['worst_best_dist']))
    r['seconds_full' if full else 'seconds'] = float(d['seconds'])
    s2 = [int(x) for x in re.search(r'^S2 leaf_shift_hist\(-4..4\):(.*)$', txt, re.M).group(1).split()]
    r['S2_leaf_shift_hist'] = {str(i - 4): c for i, c in enumerate(s2) if c}
    fa = re.search(r'^FIRST_ALIGNED_DEGREE(.*)$', txt, re.M).group(1).split()
    r['first_aligned_degree'] = {kv.split(':')[0]: int(kv.split(':')[1]) for kv in fa}
    for kind in ('S2_BY_SUPPDEG', 'LEAFALIGN_BY_SUPPDEG', 'S1_BY_DEG', 'ALIGN_BY_DEG'):
        tab = {}
        for mm in re.finditer(r'^' + kind + r' deg=(\d+)(.*)$', txt, re.M):
            tab[mm.group(1)] = {str(i - 4): int(c) for i, c in enumerate(mm.group(2).split()) if int(c)}
        if tab: r[kind] = tab
    ex = [l for l in txt.splitlines() if l.startswith('EX_')]
    r['EX_NOLEAF_printed'] = sum(l.startswith('EX_NOLEAF') for l in ex); r['EX_NOALIGN_printed'] = sum(l.startswith('EX_NOALIGN') for l in ex)
json.dump(dict(rows=[rows[n] for n in sorted(rows)]), open('cma_summary.json', 'w'), indent=1)
print('| n | trees (= A000055) | no aligned vertex | no aligned leaf | trees with a degree-2 support | of which a leaf there is aligned | S2 leaf shifts {-1, 0} | other S2 shifts | S1 range (all vertices) | first aligned vertex degrees |')
print('|---|---|---|---|---|---|---|---|---|---|')
for n in sorted(rows):
    r = rows[n]; s2 = r['S2_leaf_shift_hist']; other = sum(c for k, c in s2.items() if k not in ('-1', '0'))
    s1 = r.get('S1_BY_DEG'); s1r = '–'
    if s1:
        ks = sorted(int(k) for tab in s1.values() for k in tab); s1r = f'[{ks[0]}, {ks[-1]}]'
    print(f"| {n} | {r['trees']:,}{'' if r['count_ok'] else ' MISMATCH'} | {r['no_aligned_vertex']} | {r['no_aligned_leaf']} | {r['trees_with_degree2_support']:,} | {r['leaf_at_degree2_support_aligned']:,} | {s2.get('-1',0):,} / {s2.get('0',0):,} | {other} | {s1r} | {r['first_aligned_degree']} |")
