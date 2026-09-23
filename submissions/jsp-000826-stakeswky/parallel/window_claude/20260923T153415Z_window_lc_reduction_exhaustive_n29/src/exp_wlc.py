import sys, os, itertools
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L
from families import hub_tree, core_tree

def window_report(par):
    n = len(par); ch = L.children_of(par); p = L.uni_poly(par, ch)
    alpha, h, beta = L.params(p, n, n); LM = -(-(2*alpha-1)//3); q = -(-n//4)
    nonlc = [k for k in range(1, len(p)-1) if p[k]*p[k] < p[k-1]*p[k+1]]
    in_window_LM = [k for k in nonlc if q <= k <= LM]
    in_window_beta = [k for k in nonlc if q <= k <= beta]
    return n, alpha, q, beta, LM, nonlc, in_window_beta, in_window_LM, L.is_unimodal(p)

def core_job(key):
    arms, x = key
    return ('core', key) + window_report(core_tree(arms, x))

def hub_job(key):
    groups, s, q = key
    return ('hub', key) + window_report(hub_tree(groups, s, q)[0])

if __name__ == '__main__':
    keys_core = [(arms, x) for t in range(2, 7) for arms in itertools.combinations_with_replacement(range(1, 12), t) for x in range(0, 3) if 1 + sum(1 + 2*s for s in arms) + x <= 130]
    keys_hub = []
    for t1 in range(1, 8):
        for l1 in range(1, 21):
            for t2 in range(0, 5):
                for l2 in ([None] if t2 == 0 else range(l1+1, 26)):
                    groups = ((t1, l1),) if t2 == 0 else ((t1, l1), (t2, l2))
                    if t1 + t2 < 2: continue
                    for s in range(0, 4):
                        for q in range(0, 3):
                            n = 1 + t1*(1+l1) + (t2*(1+l2) if t2 else 0) + s + 2*q
                            if n <= 90: keys_hub.append((groups, s, q))
    with Pool(9) as pool:
        res = pool.map(core_job, keys_core, chunksize=50) + pool.map(hub_job, keys_hub, chunksize=200)
    nonlc = [r for r in res if r[7]]
    print('trees tested:', len(res), '(core %d, hub %d); non-LC trees: %d; non-unimodal: %d' % (len(keys_core), len(keys_hub), len(nonlc), sum(1 for r in res if not r[10])))
    inb = [r for r in res if r[8]]; inlm = [r for r in res if r[9]]
    print('non-LC positions inside [ceil(n/4), beta]:', len(inb), ' inside [ceil(n/4), ceil((2a-1)/3)]:', len(inlm))
    for r in inlm[:8]: print('  ', r[0], r[1], 'n=%d alpha=%d window=[%d,%d] (beta=%d) nonLC=%s' % (r[2], r[3], r[4], r[6], r[5], r[7]))
    # where do non-LC positions sit relative to alpha?
    rel = sorted(set(round((min(r[7]))/r[3], 3) for r in nonlc))[:10]
    print('smallest (first non-LC index)/alpha among non-LC trees:', rel)
