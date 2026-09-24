import sys, os, random, itertools
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from quant_scheme_lm import step_info
from families import hub_tree, core_tree

def forest_from(parts):
    par = []; off = 0
    for q in parts:
        par += [(-1 if x < 0 else x + off) for x in q]; off += len(q)
    return par

def run(args):
    label, par, c = args
    b, fl = step_info(par, c)
    return label, b, fl

def complete(b, d):
    par = [-1]; frontier = [0]
    for _ in range(d):
        nf = []
        for u in frontier:
            for _ in range(b): par.append(u); nf.append(len(par) - 1)
        frontier = nf
    return par

if __name__ == '__main__':
    c = Fr(sys.argv[1]); which = sys.argv[2]; jobs = []
    if which == 'forests':
        rng = random.Random(9); small = {1: [[-1]]}
        for m in range(2, 13): small[m] = [L.parents_from_levels(lv) for lv in L.free_trees(m)]
        for i in range(int(sys.argv[3])):
            parts = [rng.choice(small[rng.randint(1, 12)]) for _ in range(rng.randint(2, 5))]
            jobs.append(('forest%d' % i, forest_from(parts), c))
    elif which == 'families':
        for t in range(2, 5):
            for arms in itertools.combinations_with_replacement(range(1, 6), t):
                par = core_tree(arms)
                if len(par) <= 40: jobs.append(('core%s' % (arms,), par, c))
        for t1 in range(1, 5):
            for l1 in range(1, 9):
                for s in range(0, 3):
                    par, _ = hub_tree(((t1, l1),), s, 0)
                    if 4 <= len(par) <= 40: jobs.append(('hub(%d,%d)+%d' % (t1, l1, s), par, c))
        for (b, d) in ((2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3), (4, 2), (5, 2)):
            jobs.append(('complete%d^%d' % (b, d), complete(b, d), c))
    elif which == 'trees':
        n = int(sys.argv[3])
        jobs = [('tree', L.parents_from_levels(lv), c) for lv in L.free_trees(n)]
    with Pool(8) as pool:
        res = list(pool.imap_unordered(run, jobs, chunksize=max(1, len(jobs)//200)))
    fails = [(lab, fl) for lab, b, fl in res if fl]
    print('c=%s %s: cases=%d | Q_c holds: %d | STEP at every k: %d | failures: %s' % (c, which + (' n=' + sys.argv[3] if which == 'trees' else ''), len(res), sum(b for _, b, _ in res), sum(1 for _, _, fl in res if not fl), fails[:3]), flush=True)
