import sys, os, itertools
from fractions import Fraction as Fr
from multiprocessing import Pool
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comp_step import star, forest_step
C = Fr(3, 2)
def job(spec):
    comps = []
    for t, mult in spec: comps += [star(t)]*mult
    q, fl, s = forest_step(comps, C)
    n = sum((t + 1)*m for t, m in spec)
    return spec, n, q, fl, s
if __name__ == '__main__':
    NMAX = int(sys.argv[1]); specs = []
    for t in range(1, 13):
        for s in range(1, 60):
            for m in range(0, 100):
                if s*(t+1) + m <= NMAX: specs.append(((t, s), (0, m)))
    with Pool(3) as pool: res = list(pool.imap_unordered(job, specs, chunksize=20))
    bad = [r for r in res if r[3] or not r[2]]
    print('single-size star forests s*K_{1,t} + m*K1, n<=%d: %d specs | Q_{3/2} failures: %d | STEP failures: %d' % (NMAX, len(res), sum(1 for r in res if not r[2]), sum(1 for r in res if r[3])))
    byt = Counter(r[0][0][0] for r in bad); print('STEP failures by star size t:', dict(sorted(byt.items())))
    for t in sorted(byt):
        bt = [r for r in bad if r[0][0][0] == t]
        mn = min(bt, key=lambda r: r[1])
        print('  t=%d: smallest failing order n=%d spec=%s k=%s ; failing (s,m) sample: %s' % (t, mn[1], mn[0], mn[3], sorted((r[0][0][1], r[0][1][1]) for r in bt)[:12]))
