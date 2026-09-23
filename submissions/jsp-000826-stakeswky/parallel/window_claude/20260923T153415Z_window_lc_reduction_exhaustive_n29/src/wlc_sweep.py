"""Exhaustive: unimodality + log-concavity positions + window-LC for all free trees of order n (univariate only)."""
import sys, os, json
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def work(chunk):
    out = dict(trees=0, nonuni=0, nonlc_trees=0, win_LM=0, win_beta=0, cases=[], minrel=None)
    for lv in chunk:
        par = L.parents_from_levels(lv); p = L.uni_poly(par, L.children_of(par)); n = len(par)
        out['trees'] += 1
        if not L.is_unimodal(p): out['nonuni'] += 1; out['cases'].append(('NONUNIMODAL', list(lv), p)); continue
        bad = [k for k in range(1, len(p)-1) if p[k]*p[k] < p[k-1]*p[k+1]]
        if bad:
            out['nonlc_trees'] += 1
            alpha, h, beta = L.params(p, n, n); LM = -(-(2*alpha-1)//3); q = -(-n//4)
            inLM = [k for k in bad if q <= k <= LM]; inB = [k for k in bad if q <= k <= beta]
            out['win_LM'] += bool(inLM); out['win_beta'] += bool(inB)
            rel = min(bad) / alpha
            out['minrel'] = rel if out['minrel'] is None else min(out['minrel'], rel)
            if len(out['cases']) < 200: out['cases'].append((list(lv), bad, alpha))
    return out

def chunker(n, size=20000):
    buf = []
    for lv in L.free_trees(n):
        buf.append(tuple(lv))
        if len(buf) == size: yield buf; buf = []
    if buf: yield buf

if __name__ == '__main__':
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        tot = dict(trees=0, nonuni=0, nonlc_trees=0, win_LM=0, win_beta=0, cases=[], minrel=None)
        with Pool(int(os.environ.get("PROCS","9"))) as pool:
            gen = chunker(n); done = False
            while not done:
                batch = []
                for _ in range(45):
                    try: batch.append(next(gen))
                    except StopIteration: done = True; break
                for r in pool.imap(work, batch):
                    for k in ('trees', 'nonuni', 'nonlc_trees', 'win_LM', 'win_beta'): tot[k] += r[k]
                    tot['cases'] = (tot['cases'] + r['cases'])[:300]
                    if r['minrel'] is not None: tot['minrel'] = r['minrel'] if tot['minrel'] is None else min(tot['minrel'], r['minrel'])
        json.dump(tot, open('/tmp/e993/research/wlc_n%d.json' % n, 'w'))
        print('WLC n=%d trees=%d nonunimodal=%d nonLC_trees=%d nonLC_in_window[ceil(n/4),LM]=%d in_window[ceil(n/4),beta]=%d min(first nonLC index/alpha)=%s' % (
            n, tot['trees'], tot['nonuni'], tot['nonlc_trees'], tot['win_LM'], tot['win_beta'], tot['minrel']), flush=True)
