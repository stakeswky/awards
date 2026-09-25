"""List every STEP failure of the c/n scheme (quant_scheme_lm.step_info) over all forests of order n,
for rational c given as a/b. Failures are summarised by component structure."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from quant_scheme_lm import step_info
from step_forests import forests

def comps(par):
    n = len(par); root = list(range(n))
    for v in range(n):
        r = v
        while par[r] >= 0: r = par[r]
        root[v] = r
    sizes = {}
    for v in range(n): sizes[root[v]] = sizes.get(root[v], 0) + 1
    return sorted(sizes.values(), reverse=True)

def job(args):
    par, c = args
    b, fl = step_info(par, c)
    return b, fl, par

if __name__ == '__main__':
    c = Fr(sys.argv[1])
    for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
        with Pool(8) as pool: res = list(pool.imap_unordered(job, [(f, c) for f in forests(n)], chunksize=100))
        bad = [(r[2], r[1]) for r in res if r[1]]
        qfail = sum(1 for r in res if not r[0])
        desc = []
        for par, fl in bad:
            cs = comps(par)
            desc.append('%dK1' % n if cs == [1]*n else ('comp%s k=%s par=%s' % (cs, fl, par if n <= 13 else '')))
        print('c=%s n=%d: forests=%d Q_c-fail=%d STEP-fail=%d: %s' % (c, n, len(res), qfail, len(bad), desc), flush=True)
