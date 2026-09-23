import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
M = (1 << 64) - 1; G = 0x9E3779B97F4A7C15
for n in (5, 10, 14, 16, 18, 20):
    cs = 0; t = 0
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv); p = L.uni_poly(par, L.children_of(par)); t += 1
        for k, v in enumerate(p): cs = (cs + v * (k + 1) * G) & M
    print('PY n=%d trees=%d checksum=%d' % (n, t, cs))
