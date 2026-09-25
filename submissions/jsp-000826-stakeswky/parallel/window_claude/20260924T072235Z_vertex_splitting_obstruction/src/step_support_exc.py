import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from step_anatomy import anatomy
from multiprocessing import Pool
if __name__ == '__main__':
    for n in range(7, 15):
        items = [L.parents_from_levels(lv) for lv in L.free_trees(n)]
        with Pool(2) as pool: res = [r for r in pool.imap_unordered(anatomy, items, chunksize=50) if r]
        exc_s = [r['par'] for r in res if not r['all_k_support']]
        exc_u = [r['par'] for r in res if not r['uniform']]
        def shape(par):
            ch = L.children_of(par); deg = [len(ch[v]) + (par[v] >= 0) for v in range(len(par))]
            return 'path' if max(deg) <= 2 else 'degs=%s' % sorted(deg, reverse=True)
        print(n, 'no support witness at some k:', [shape(p) for p in exc_s], '| no uniform witness:', [shape(p) for p in exc_u], flush=True)
