import sys, os
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp_more import e2
if __name__ == '__main__':
    with Pool(3) as pool:
        rs = pool.map(e2, range(4, 12))
    small = sum(r['pairs'] for r in rs); viol = sum(r['viol'] for r in rs)
    big = [4415, 12971, 34630, 90726, 270231, 751687, 2020385, 5949964]
    print('anchor pairs n=4..11:', small, 'violations', viol, '| total n=4..19:', small + sum(big))
