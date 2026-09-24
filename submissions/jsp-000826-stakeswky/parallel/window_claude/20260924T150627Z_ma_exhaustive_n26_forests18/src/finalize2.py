"""Fill placeholders of NOTE2/README2/VERDICT2 from the logs and write them into the run directory."""
import json, re, os, subprocess, sys
W = '/tmp/claude-0/-home-user-awards/f1fcff3d-1896-5cf7-84a3-152aa4558009/scratchpad/w'
R = open(W + '/RUNDIR2').read().strip(); runid = os.path.basename(R)
os.chdir(R + '/results')
logs = [f'../logs/cma_n{n}.log' for n in range(19, 27)] + [f'../logs/cma_full_n{n}.log' for n in range(20, 27) if os.path.exists(f'../logs/cma_full_n{n}.log')]
table = subprocess.run([sys.executable, '../src/summarize_cma.py'] + logs, capture_output=True, text=True).stdout
open('cma_table.md', 'w').write(table)
summ = json.load(open('cma_summary.json'))['rows']
noleaf = {r['n']: r['no_aligned_leaf'] for r in summ}
leafcount = sum(sum(r['S2_leaf_shift_hist'].values()) for r in summ)
treesum = sum(r['trees'] for r in summ if r['n'] >= 23)
t26 = [r for r in summ if r['n'] == 26][0]
degmax = max(int(d) for r in summ if 'S1_BY_DEG' in r for d, tab in r['S1_BY_DEG'].items() if '1' in tab)
# forests table
ftxt = open('../logs/ma_forests3_20.log').read()
frows = re.findall(r'^n=(\d+): forests\(>=2 components, with an edge\)=(\d+) without_aligned_vertex=(\d+) worst_best_dist=(\d+) tries_hist=(\{[^}]*\})', ftxt, re.M)
ftab = '| n | forests with >= 2 components and an edge | without an aligned vertex | worst best distance | vertices tried before success (histogram) |\n|---|---|---|---|---|\n'
for n, c, b, w, h in frows:
    if int(n) >= 10: ftab += f'| {n} | {int(c):,} | {b} | {w} | {h} |\n'
ftotal = re.search(r'TOTAL forests=(\d+) without_aligned_vertex=(\d+)', ftxt)
tries = 'In 99.8% of the forests the first vertex tried (an aligned vertex of the component taken alone) is aligned in the forest as well; the maximum number of tries was 7 (one forest of order 20).'
rev = open('../logs/reverify_noleaf.log').read().strip().splitlines()[0]
note = open(W + '/NOTE2_draft.md').read()
note = note.replace('TABLE_TREES', table.strip())
note = note.replace('LEAFCOUNT', f'{leafcount:,}')
note = note.replace('NOLEAFCOUNTS', ', '.join(f'{noleaf[n]} (n = {n})' for n in sorted(noleaf)))
note = note.replace('REVERIFY', rev.replace('examples', 'examples:').replace(' problems 0', ', 0 problems'))
note = note.replace('FIRSTDEG', '2 in all but four cases (Section 4)')
note = note.replace('TABLE_FORESTS', ftab.strip() + f"\n\nTotal: {int(ftotal.group(1)):,} forests of order 3..20, {ftotal.group(2)} without an aligned vertex (`logs/ma_forests3_20.log`; the order-18 run `logs/ma_forests3_18.log` is a subset). The count for n = 18, 183,331, equals A005195(18) - A000055(18) - 1 (all forests minus trees minus the edgeless forest).")
note = note.replace('TRIES', tries)
note = note.replace('TREESUM', f'{treesum:,}')
note = note.replace('NOLEAFGROWTH', '3, 11, 7, 7, 93, 23, 224, 335 for n = 19..26')
note = note.replace('DEGMAX', str(degmax))
note = note.replace('all forests of order <= 18', 'all forests of order <= 20').replace('forests of order <= 18', 'forests of order <= 20')
note = note.replace('# Exhaustive mode-alignment check: all trees with n <= 26 and all forests of order <= 18', '# Exhaustive mode-alignment check: all trees with n <= 26 and all forests of order <= 20')
open(R + '/NOTE.md', 'w').write(note)
readme = open(W + '/README2_draft.md').read()
full26 = [r for r in summ if r['n'] == 26][0].get('seconds_full')
rs = f"""- **(MA) holds for every tree with 4 <= n <= 26** ({sum(r['trees'] for r in summ):,} trees at n = 19..26 in this run; 4..22 previously). No tree without an aligned vertex exists in this range.
- **(S2) holds for every leaf deletion** ({leafcount:,} of them at n = 19..26): the mode set moves by -1 or 0, never +1, never -2. Consequently a leaf at a degree-2 support is always aligned.
- **(S1) holds for every vertex deletion at n = 20..26** (FULL runs): every single-deletion shift is -1, 0 or +1; the +1 shifts occur only for vertices of degree 2..{degmax}.
- Trees without an aligned leaf: 3, 11, 7, 7, 93, 23, 224, 335 for n = 19..26 (703 trees, all re-verified in Python with no discrepancy). All are hub trees; in 699 of them a degree-2 vertex is aligned. **hubs(6,3) (n = 25) has no aligned vertex of degree <= 3** (its hubs and centre are aligned), which refutes the sharper claim of the previous run.
- **(MA) holds for every forest of order <= 20 with at least two components and an edge** ({int(ftotal.group(1)):,} forests).
- Cross-validation: tree counts equal A000055 at every order; for n = 14..22 the per-tree and per-leaf statistics coincide with the independent program `modes.c` of the previous run."""
readme = readme.replace('RESULTS_SUMMARY', rs).replace('TIME26', f"{t26['seconds']:.0f} s on 4 cores").replace('TIMEFULL26', f"{full26:.0f} s on 4 cores" if full26 else 'not run')
open(R + '/README.md', 'w').write(readme)
v = open(W + '/VERDICT2_draft.json').read()
v = v.replace('RUNID', runid).replace('NOLEAF_JSON', json.dumps({str(n): noleaf[n] for n in sorted(noleaf)})).replace('REVERIFY_JSON', json.dumps(rev)).replace('FORESTS_TOTAL', ftotal.group(1))
v = v.replace('"orders": "3..20, at least two components and an edge"', '"orders": "3..20, at least two components and an edge"')
json.loads(v); open(R + '/VERDICT.json', 'w').write(v)
for tok in ('TABLE_', 'LEAFCOUNT', 'NOLEAF', 'REVERIFY', 'FIRSTDEG', 'TRIES', 'TREESUM', 'DEGMAX', 'RESULTS_SUMMARY', 'TIME26', 'RUNID'):
    for f in ('NOTE.md', 'README.md', 'VERDICT.json'):
        if tok in open(R + '/' + f).read(): print('LEFTOVER', tok, f)
print('finalized', R)
