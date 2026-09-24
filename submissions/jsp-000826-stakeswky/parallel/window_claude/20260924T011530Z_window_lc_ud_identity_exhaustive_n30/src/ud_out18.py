import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from dispersion2 import profile
for lv in L.free_trees(18):
    n, a, prof = profile(L.parents_from_levels(lv))
    bad = [(k, round(q, 4)) for (k, q, inw, nlc) in prof if q > 1 and k >= 2]
    if bad:
        lo = (n + 3)//4; hi = (2*a + 1)//3
        print('levels=%s alpha=%d window=[%d,%d] over-dispersed at (k,Var/mu)=%s  k/alpha=%s' % (list(lv), a, lo, hi, bad, [round(k/a, 3) for k, _ in bad]))
