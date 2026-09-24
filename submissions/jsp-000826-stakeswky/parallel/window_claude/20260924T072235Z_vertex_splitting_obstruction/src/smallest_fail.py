import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
import quant_scheme_lm as QL
import quant_scheme_tr as QT
from step_forests import forest_from
C = Fr(3, 2)
def job(args):
    label, par, mode = args
    if mode == 'LM':
        b, fl = QL.step_info(par, C)
    else:
        QT.MODE['nu'] = (mode == 'TRnu'); QT.MODE['ptr'] = False
        b, fl = QT.step_info(par, C)
    return label, len(par), mode, b, fl
if __name__ == '__main__':
    jobs = []
    for t in range(2, 8):
        for lv in (L.free_trees(t) if t >= 3 else [None]):
            T = L.parents_from_levels(lv) if lv is not None else [-1, 0]
            for m in range(0, 46):
                for mode in ('LM', 'TR', 'TRnu'):
                    jobs.append(('T%s+%dK1' % (T, m), forest_from([T] + [[-1]]*m), mode))
    with Pool(3) as pool: res = list(pool.imap_unordered(job, jobs, chunksize=10))
    for mode in ('LM', 'TR', 'TRnu'):
        bad = sorted([r for r in res if r[2] == mode and r[4]], key=lambda r: r[1])
        qb = [r for r in res if r[2] == mode and not r[3]]
        print('%-4s: T + mK1 (|T|<=7, m<=45): %d forests | Q fails %d | STEP fails %d | smallest failing: %s' % (
            mode, sum(1 for r in res if r[2] == mode), len(qb), len(bad), [(r[0], r[1], r[4]) for r in bad[:3]]))
