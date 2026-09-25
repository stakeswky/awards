"""Research experiments for G1/G2/G3 (exploratory; exact integers)."""
import sys, os, json, itertools
from math import comb
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L

def rows_of(par):
    ch = L.children_of(par); col = L.colours(par)
    return L.biv_rows(par, ch, col)

def flip(rows):  # swap colour classes: f_r(l) -> f_r(r-l)
    return [list(reversed(r)) for r in rows]

def mul_rows(A, B):
    n = len(A) + len(B) - 1
    out = [[0]*(r+1) for r in range(n)]
    for r1, ra in enumerate(A):
        for r2, rb in enumerate(B):
            o = out[r1+r2]
            for l1, x in enumerate(ra):
                if x:
                    for l2, y in enumerate(rb):
                        if y: o[l1+l2] += x*y
    return out

def dmass_pair(rows, i, j):
    """long-range: N=f_i*f_{j+1}, P=f_{i+1}*f_j ; returns Dmass, sumN, sumP"""
    g = lambda r: rows[r] if 0 <= r < len(rows) else [0]
    N = L.conv(g(i), g(j+1)); P = L.conv(g(i+1), g(j))
    m = max(len(N), len(P)); N += [0]*(m-len(N)); P += [0]*(m-len(P))
    return sum(max(x-y, 0) for x, y in zip(N, P)), sum(N), sum(P)

def history_positions(p):
    first = next((k for k in range(len(p)-1) if p[k] > p[k+1]), None)
    out = []
    if first is None: return out
    for j in range(first+1, len(p)):
        if any(p[k] < p[k+1] for k in range(first, j)): break
        out.append(j)
    return out

# ---------- E1: forests with two components, colour flips ----------
def e1_chunk(args):
    trees_small, trees_big_list = args
    res = dict(forests=0, positions=0, best_viol=0, worst_viol=0, max_best=Fr(0), max_worst=Fr(0), best_case=None, worst_case=None, mid_positions=0, mid_best_viol=0, max_best_mid=Fr(0))
    for (n1, lv1, R1) in trees_small:
        for (n2, lv2, R2) in trees_big_list:
            if (n1, lv1) > (n2, lv2): continue
            res['forests'] += 1
            options = [mul_rows(R1, R2), mul_rows(R1, flip(R2))]
            p = [sum(r) for r in options[0]]
            n = n1 + n2; M = max(n1, n2)
            alpha, h, beta = L.params(p, n, M)
            for j in history_positions(p):
                b, a = p[j-1], p[j]; S = a*(b-a)
                vals = [dmass_pair(rows, j-1, j)[0] for rows in options]
                best, worst = min(vals), max(vals)
                res['positions'] += 1
                mid = (h+1 <= j < beta)
                if mid: res['mid_positions'] += 1
                if S == 0:
                    if best > 0: res['best_viol'] += 1; res['mid_best_viol'] += mid
                    if worst > 0: res['worst_viol'] += 1
                    continue
                if best > S: res['best_viol'] += 1; res['mid_best_viol'] += mid
                if worst > S: res['worst_viol'] += 1
                if Fr(best, S) > res['max_best']: res['max_best'] = Fr(best, S); res['best_case'] = (n1, lv1, n2, lv2, j, mid)
                if Fr(worst, S) > res['max_worst']: res['max_worst'] = Fr(worst, S); res['worst_case'] = (n1, lv1, n2, lv2, j, mid)
                if mid and Fr(best, S) > res['max_best_mid']: res['max_best_mid'] = Fr(best, S)
    return res

# ---------- E2: long-range anchors on trees ----------
def e2(n):
    res = dict(n=n, pairs=0, anchors_lt=0, viol=0, max_ratio=Fr(0), case=None, plateaus=0)
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv); rows = rows_of(par); p = [sum(r) for r in rows]
        hp = history_positions(p)
        for j in hp:
            a = p[j]
            if p[j-1] == p[j]: res['plateaus'] += 1
            for i in range(j):
                if not (p[i] > p[i+1] and all(p[k] >= p[k+1] for k in range(i+1, j))): continue
                dm, sN, sP = dmass_pair(rows, i, j); Si = a*(p[i]-p[i+1])
                res['pairs'] += 1; res['anchors_lt'] += (i < j-1)
                if dm > Si: res['viol'] += 1
                if Si and Fr(dm, Si) > res['max_ratio']: res['max_ratio'] = Fr(dm, Si); res['case'] = (list(lv), i, j)
    return res

# ---------- E3: population structure at middle-range positions ----------
def populations(rows, side):
    """side 1: S subset of colour-1 (R), free count k of colour-0 (L); side 0: roles swapped."""
    if side == 0: rows = flip(rows)
    # f[l][m] with l = #colour-0 (free side), m = #colour-1 (S side)
    f = {}
    for r, row in enumerate(rows):
        for l, v in enumerate(row):
            if v: f[(l, r-l)] = v
    ms = sorted({m for (_, m) in f}); pops = {}
    for m in ms:
        lmax = max(l for (l, mm) in f if mm == m)
        for k in range(lmax+1):
            g = sum((-1)**(l-k) * comb(l, k) * f.get((l, m), 0) for l in range(k, lmax+1))
            assert g >= 0
            if g: pops[(m, k)] = g
    return pops

def e3(n):
    res = dict(n=n, positions=0, allDEC_some_side=0, inc_share_max=Fr(0))
    for lv in L.free_trees(n):
        par = L.parents_from_levels(lv); rows = rows_of(par); p = [sum(r) for r in rows]
        js, meta = L.domain(p, n, n)
        if not js: continue
        pops = [populations(rows, s) for s in (0, 1)]
        for j in js:
            res['positions'] += 1
            ok = False; shares = []
            for side in (0, 1):
                inc = 0; tot = 0; bad = False
                for (m, k), g in pops[side].items():
                    x = comb(k, j-1-m) if 0 <= j-1-m <= k else 0
                    y = comb(k, j-m) if 0 <= j-m <= k else 0
                    z = comb(k, j+1-m) if 0 <= j+1-m <= k else 0
                    tot += g*y
                    if y > x or (x == 0 and y == 0 and z > 0): bad = True; inc += g*max(y, z)
                shares.append(Fr(inc, tot) if tot else Fr(0))
                if not bad: ok = True
            if ok: res['allDEC_some_side'] += 1
            s = min(shares)
            if s > res['inc_share_max']: res['inc_share_max'] = s
    return res

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'e1':
        NMAX = int(sys.argv[2])
        trees = []
        for n in range(1, NMAX):
            if n == 1: trees.append((1, (0,), [[1], [1, 0]])); continue   # K1: rows r0=[1], r1: l=1 -> [0,1]? fixed below
            for lv in L.free_trees(n):
                par = L.parents_from_levels(lv); trees.append((n, tuple(lv), rows_of(par)))
        # correct K1 rows: one vertex in colour 0 -> r=1 row [0,1] (l=1)
        trees[0] = (1, (0,), [[1], [0, 1]])
        small = [t for t in trees if 2*t[0] <= NMAX]
        chunks = []
        for t in small:
            big = [u for u in trees if u[0] >= t[0] and t[0] + u[0] <= NMAX]
            chunks.append(([t], big))
        tot = None
        with Pool(9) as pool:
            for r in pool.imap_unordered(e1_chunk, chunks):
                if tot is None: tot = r; continue
                for k in ('forests','positions','best_viol','worst_viol','mid_positions','mid_best_viol'): tot[k] += r[k]
                for k, c in (('max_best','best_case'), ('max_worst','worst_case')):
                    if r[k] > tot[k]: tot[k] = r[k]; tot[c] = r[c]
                if r['max_best_mid'] > tot['max_best_mid']: tot['max_best_mid'] = r['max_best_mid']
        print('E1 two-component forests, total n <=', NMAX, {k: (float(v) if isinstance(v, Fr) else v) for k, v in tot.items()})
    elif which == 'e2':
        with Pool(9) as pool:
            for r in pool.imap(e2, range(4, int(sys.argv[2])+1)):
                print('E2 n=%d anchor-pairs=%d (i<j-1: %d) violations=%d plateaus=%d max Dmass^(i)/S_i=%.5f case=%s' % (r['n'], r['pairs'], r['anchors_lt'], r['viol'], r['plateaus'], float(r['max_ratio']), r['case']), flush=True)
    elif which == 'e3':
        with Pool(9) as pool:
            for r in pool.imap(e3, range(14, int(sys.argv[2])+1)):
                print('E3 n=%d middle positions=%d with an all-DEC side=%d  max over positions of min-side INC share=%.4f' % (r['n'], r['positions'], r['allDEC_some_side'], float(r['inc_share_max'])), flush=True)
