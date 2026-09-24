"""Parse cwlc logs (one per order) into results/cwlc_summary.json and check tree counts against
OEIS A000055 (free trees) and rooted counts against A000081."""
import re, sys, json
A000055 = {4: 2, 5: 3, 6: 6, 7: 11, 8: 23, 9: 47, 10: 106, 11: 235, 12: 551, 13: 1301, 14: 3159, 15: 7741, 16: 19320,
           17: 48629, 18: 123867, 19: 317955, 20: 823065, 21: 2144505, 22: 5623756, 23: 14828074, 24: 39299897,
           25: 104636890, 26: 279793450, 27: 751065460, 28: 2023443032, 29: 5469566585, 30: 14830871802,
           31: 40330829030, 32: 109972410221}
A000081 = [0, 1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766, 12486, 32973, 87811, 235381]
rows = {}
for f in sys.argv[1:]:
    txt = open(f).read()
    res = re.search(r'^RESULT (.*)$', txt, re.M)
    if not res: print('incomplete log', f); continue
    d = dict(kv.split('=', 1) for kv in res.group(1).split())
    n = int(d['n'])
    m1 = dict(kv.split('=', 1) for kv in re.search(r'^M1 (.*?) window_argmax', txt, re.M).group(1).split())
    eq = dict(kv.split('=', 1) for kv in re.search(r'^EQ (.*)$', txt, re.M).group(1).split())
    mg = dict(kv.split('=', 1) for kv in re.search(r'^MARGIN (.*)$', txt, re.M).group(1).split())
    rooted = [tuple(map(int, x.split(':'))) for x in re.search(r'^ROOTED (.*)$', txt, re.M).group(1).split()]
    am = re.search(r'window_argmax (\S+)', txt); argmax = am.group(1) if am else None  # empty window for tiny n
    rows[n] = dict(n=n, trees=int(d['trees']), OEIS_A000055=A000055[n], count_ok=int(d['trees']) == A000055[n],
                   rooted_counts_ok=all(c == A000081[s] for s, c in rooted),
                   nonunimodal=int(d['nonunimodal']), nonLC=int(d['nonLC']), nonLC_in_window=int(d['nonLC_in_window_LM']),
                   nonLC_in_beta_window=int(d['nonLC_in_window_beta']), min_first_nonLC_over_alpha=None if d['minrel'] == '9.000000' else float(d['minrel']),
                   window_equality_positions=int(eq['window_positions']), interior_equality_trees=int(eq['interior_equality_trees']),
                   consecutive_interior_equality_trees=int(eq['consecutive_interior_equality_trees']),
                   M1_fail_trees_any_r=int(m1['bad_any_trees']), M1_fail_trees_window=int(m1['bad_window_trees']),
                   max_drift_any_r=float(m1['max_drift_any']), max_window_drift=None if float(m1['max_drift_window']) < -1e17 else float(m1['max_drift_window']), max_window_drift_tree=argmax,
                   min_n_times_LC_margin_window=None if float(mg['min_n_margin_window']) > 1e17 else float(mg['min_n_margin_window']),
                   min_n_times_LC_margin_1_to_top=None if float(mg['min_n_margin_1_to_top']) > 1e17 else float(mg['min_n_margin_1_to_top']),
                   min_mode_over_n=float(mg['mode_over_n_min']), max_mode_over_alpha=float(mg['mode_over_alpha_max']),
                   checksum=int(d['checksum']), seconds=float(d['seconds']), threads=int(d['threads']))
    print(n, {k: rows[n][k] for k in ('trees', 'count_ok', 'nonunimodal', 'nonLC', 'nonLC_in_window', 'window_equality_positions',
                                      'interior_equality_trees', 'M1_fail_trees_window', 'max_window_drift', 'seconds')})
json.dump(dict(rows=[rows[n] for n in sorted(rows)]), open('cwlc_summary.json', 'w'), indent=1)
