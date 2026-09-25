import sys, os, itertools
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comp_step import star, forest_step
C = Fr(3, 2)
def job(spec):
    comps = []
    for t, mult in spec: comps += [star(t)]*mult
    q, fl, s = forest_step(comps, C)
    return spec, q, fl, s
if __name__ == '__main__':
    NMAX = int(sys.argv[1]); specs = []
    for t in range(1, 13):
        for s in range(1, 40):
            for m in range(0, 80):
                if s*(t+1) + m <= NMAX: specs.append(((t, s), (0, m)))
    for t1, t2 in itertools.combinations(range(1, 9), 2):
        for s1 in range(1, 12):
            for s2 in range(1, 12):
                for m in range(0, 40, 3):
                    if s1*(t1+1) + s2*(t2+1) + m <= NMAX: specs.append(((t1, s1), (t2, s2), (0, m)))
    with Pool(3) as pool: res = list(pool.imap_unordered(job, specs, chunksize=20))
    bad = [r for r in res if r[2] or not r[1]]
    res.sort(key=lambda r: r[3] if r[3] is not None else 99)
    print('star forests (families, n<=%d): %d specs | failures: %d %s' % (NMAX, len(res), len(bad), [(b[0], b[2]) for b in bad[:5]]))
    print('smallest slacks:', [(r[0], round(float(r[3]), 4)) for r in res[:8]])
