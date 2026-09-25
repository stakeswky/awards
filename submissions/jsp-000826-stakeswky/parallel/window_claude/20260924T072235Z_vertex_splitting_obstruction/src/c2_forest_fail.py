import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from quant_scheme_lm import step_info
from step_broad import forest_from
if __name__ == '__main__':
    rng = random.Random(9); small = {1: [[-1]]}
    for m in range(2, 13): small[m] = [L.parents_from_levels(lv) for lv in L.free_trees(m)]
    for i in range(3000):
        parts = [rng.choice(small[rng.randint(1, 12)]) for _ in range(rng.randint(2, 5))]
        if i in (72, 205, 290):
            par = forest_from(parts); p = L.uni_poly(par, L.children_of(par))
            print(i, 'component orders', [len(q) for q in parts], 'n=', len(par), 'p=', p, 'Q2 at k=1:', p[1]**2 - p[0]*p[2], 'vs need', 2*p[1]**2/len(par))
