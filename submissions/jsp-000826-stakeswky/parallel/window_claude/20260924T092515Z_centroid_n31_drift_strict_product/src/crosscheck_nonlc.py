"""Compare the non-log-concave trees found by cwlc (centroid enumeration, this run) with those
recorded by the WROM checkers of runs 20260923T153415Z (n=26..29) and 20260924T011530Z (n=30).
Trees are compared by their full independence sequences (as multisets) and by counts."""
import json, re, sys, glob, collections
BASE = sys.argv[1]  # path to parallel/window_claude
old = collections.defaultdict(list)
for f in sorted(glob.glob(BASE + '/20260923T153415Z_window_lc_reduction_exhaustive_n29/results/wlc_strict_n2[6-9].json')) + \
         [BASE + '/20260924T011530Z_window_lc_ud_identity_exhaustive_n30/results/wlc_strict_n30.json']:
    d = json.load(open(f)); n = d['summary']['n']
    for ex in d['examples']:
        old[n].append(tuple(int(x) for x in re.search(r'p=(\S+)', ex).group(1).split(',')))
    assert len(old[n]) == d['summary']['nonLC'], (n, len(old[n]), d['summary']['nonLC'])
new = collections.defaultdict(list)
for f in sys.argv[2:]:
    n = None
    for line in open(f):
        if line.startswith('RESULT'): n = int(re.search(r' n=(\d+)', line).group(1))
    for line in open(f):
        if line.startswith('EX') and 'first_bad=-1' not in line:
            new[n].append(tuple(int(x) for x in re.search(r'p=(\S+)', line).group(1).split(',')))
out = {}
for n in sorted(set(old) | set(new)):
    same = collections.Counter(old[n]) == collections.Counter(new[n]) if n in old else None
    out[n] = dict(old_count=len(old[n]) if n in old else None, new_count=len(new[n]), identical_multisets=same)
    print(n, out[n])
json.dump(out, open('crosscheck_nonlc.json', 'w'), indent=1)
