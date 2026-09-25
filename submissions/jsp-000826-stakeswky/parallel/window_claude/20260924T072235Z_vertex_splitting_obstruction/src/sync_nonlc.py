import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from sync_exists import sync_info
H = os.path.dirname(os.path.abspath(__file__))
trees = []
for n, f in ((26, 'wlc_c_n26.json'), (28, 'wlc_c_n28.json'), (29, 'wlc_c_n29.json'), (30, 'wlc_strict_n30.json')):
    for e in json.load(open(os.path.join(H, f)))['examples']:
        trees.append((n, [int(x) for x in e.split('levels=')[1].split()[0].split(',')]))
tot = ok = okn = 0; bad = []
for n, lv in trees:
    r = sync_info(L.parents_from_levels(lv)); tot += 1; ok += bool(r['good']); okn += bool(r['good_nest'])
    if not r['good']: bad.append((n, lv))
print('non-LC trees n=26..30: %d | sync v on [1,top]: %d | sync+nesting: %d | failures (no sync v): %d' % (tot, ok, okn, len(bad)))
for b in bad[:3]: print('  no-sync:', b)
