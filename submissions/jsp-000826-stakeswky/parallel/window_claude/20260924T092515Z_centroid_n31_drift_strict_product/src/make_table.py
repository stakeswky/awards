"""Markdown table of results/cwlc_summary.json (plus wlc2 checksum comparison if given)."""
import json, sys, re, glob
rows = json.load(open(sys.argv[1]))['rows']
wlc2 = {}
for f in sys.argv[2:]:
    txt = open(f).read()
    for m in re.finditer(r'RESULT n=(\d+) K=\d+ id=\d+ trees=(\d+).*checksum=(\d+)', txt):
        n = int(m.group(1)); t, c = wlc2.get(n, (0, 0)); wlc2[n] = (t + int(m.group(2)), (c + int(m.group(3))) % 2 ** 64)
def f(x, d=3): return '–' if x is None else (f'{x:.{d}f}' if isinstance(x, float) else str(x))
print('| n | trees (= A000055) | non-LC | min first non-LC / alpha | window LC failures / equalities | trees with an interior LC equality | drift condition failures (any r / window) | max window drift | min n * LC margin on window | min mode/n | max mode/alpha | checksum = wlc2 |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in rows:
    n = r['n']
    ck = ('yes' if wlc2[n] == (r['trees'], r['checksum']) else 'NO') if n in wlc2 else 'not run'
    print(f"| {n} | {r['trees']:,}{'' if r['count_ok'] else ' (MISMATCH)'} | {r['nonLC']} | {f(r['min_first_nonLC_over_alpha'], 4)} | "
          f"{r['nonLC_in_window']} / {r['window_equality_positions']} | {r['interior_equality_trees']} | {r['M1_fail_trees_any_r']} / {r['M1_fail_trees_window']} | "
          f"{f(r['max_window_drift'], 4)} | {f(r['min_n_times_LC_margin_window'], 3)} | {f(r['min_mode_over_n'], 3)} | {f(r['max_mode_over_alpha'], 3)} | {ck} |")
