"""Adversarial STEP_nested tests: a large unique-MIS forest U plus one small non-unique component W,
so that the only nested vertices lie in W.  U in {R(s,0), s P3 + m K1, s K_{1,3} + m K1, hubs}, W in {K2, P4, K_{1,1}+...}."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from step_forests import forest_from
from nested_stress import vertex_level
def R(s):
    par = [-1]
    for i in range(s):
        par.append(0); c = len(par) - 1; par += [c, c]
    return par
def star(t): return [-1] + [0]*t
def job(args):
    name, parts = args
    par = forest_from(parts)
    r = vertex_level(par)
    return (name, len(par)) + r
if __name__ == '__main__':
    K2 = [-1, 0]; P4 = [-1, 0, 1, 2]
    jobs = []
    for s in range(15, 31):
        for Wn, W in (('K2', K2), ('P4', P4)):
            jobs.append(('R(%d,0)+%s' % (s, Wn), [R(s), W]))
    for s in range(8, 16):
        for m in (5, 13, 20):
            jobs.append(('%dP3+%dK1+K2' % (s, m), [star(2)]*s + [[-1]]*m + [K2]))
            jobs.append(('%dK13+%dK1+K2' % (s, m), [star(3)]*s + [[-1]]*m + [K2]))
    with Pool(3) as pool: res = list(pool.imap_unordered(job, jobs, chunksize=1))
    res.sort(key=lambda r: r[1])
    bad = [r for r in res if r[3]]
    print('adversarial U + small W: %d forests (n up to %d) | Q fails %d | STEP_nested fails %d %s | min slack %.4f at %s' % (
        len(res), max(r[1] for r in res), sum(1 for r in res if not r[2]), len(bad), [(r[0], r[3]) for r in bad[:4]],
        float(min(r[4] for r in res)), min(res, key=lambda r: r[4])[0]))
