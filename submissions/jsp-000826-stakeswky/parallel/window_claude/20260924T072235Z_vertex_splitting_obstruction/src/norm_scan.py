"""Scan normalisations of the LC margin on [1, min(top, alpha-1)] over all forests of order n.
Reports the minimum over forests and k of:  n*m,  (k+1)*m,  k*m,  where m = 1 - p_{k-1}p_{k+1}/p_k^2."""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from step_forests import forests, top

def scan(par):
    n = len(par); p = L.uni_poly(par, L.children_of(par)); a = len(p) - 1
    out = [None, None, None]; arg = [None, None, None]
    for k in range(1, min(top(a), a - 1) + 1):
        m = Fr(p[k]**2 - p[k-1]*p[k+1], p[k]**2)
        for j, w in enumerate((n, k + 1, k)):
            v = w * m
            if out[j] is None or v < out[j]: out[j] = v; arg[j] = (k, a)
    return out, arg, par

if __name__ == '__main__':
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        with Pool(8) as pool: res = list(pool.imap_unordered(scan, forests(n), chunksize=200))
        for j, name in enumerate(('n*m', '(k+1)*m', 'k*m')):
            vals = [(r[0][j], r[1][j], r[2]) for r in res if r[0][j] is not None]
            best = min(vals, key=lambda t: t[0])
            print('n=%d %-8s min=%.4f at (k,alpha)=%s forest=%s' % (n, name, float(best[0]), best[1], best[2] if n <= 12 else '...'), flush=True)
