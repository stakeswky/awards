"""Forests of order <= NMAX that contain a non-log-concave tree component (general NMAX <= 51).

A forest with two non-LC tree components has order >= 52 (every tree of order <= 25 is LC), so for
NMAX <= 51 such a forest is T + R with T a non-LC tree of order 26..NMAX and R an arbitrary forest of
order <= NMAX - |T| (possibly empty). I(T+R) = I(T) I(R) depends only on I(T) and I(R). So it suffices
to take every non-LC tree sequence (EX lines with first_bad >= 0 in the exhaustive checker logs) and
every distinct forest polynomial of order m <= NMAX - 26.

Tree polynomials of order m are generated from rooted trees (a root plus a multiset of smaller rooted
trees; f = I(tau), g = I(tau - root), f = prod f_c + x prod g_c, g = prod f_c). Every free tree is a
rooted tree, so the set {f} over rooted trees of order m is the set of tree polynomials of order m.
The set sizes are checked against the Pruefer-code enumeration of forest_nonlc32.py for m <= 6.

For each product: unimodality, strict LC on [ceil(n/4), ceil((2a-1)/3)], and the window drift
condition on [ceil(n/4), ceil((2a-1)/3) - 2] (as in forest_nonlc32.py); exact integers.
usage: forest_nonlc_gen.py NMAX out.json log26 log27 ...
"""
import sys, re, json


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return out


def add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def rooted_trees(mmax):
    """R[m] = list of (f, g) for all rooted trees of order m (each once, up to isomorphism)."""
    R = {1: [((1, 1), (1,))]}
    idx = [(1, 0)]  # global index list of (order, position)
    for m in range(2, mmax + 1):
        out = []
        allr = [(s, i) for s in range(1, m) for i in range(len(R[s]))]

        def rec(rem, maxk, F, G):
            if rem == 0:
                f = add(F, [0] + G)
                out.append((tuple(f), tuple(F)))
                return
            for k in range(maxk, -1, -1):
                s, i = allr[k]
                if s > rem:
                    continue
                f, g = R[s][i]
                rec(rem - s, k, mul(F, list(f)), mul(G, list(g)))
        rec(m - 1, len(allr) - 1, [1], [1])
        R[m] = out
    return R


def check(p, n):
    a = len(p) - 1
    q, top = (n + 3) // 4, (2 * a + 1) // 3
    k = 0
    while k < a and p[k] <= p[k + 1]:
        k += 1
    uni = all(p[t] >= p[t + 1] for t in range(k, a))
    wlc = all(p[t] ** 2 > p[t - 1] * p[t + 1] for t in range(max(q, 1), min(top, a - 1) + 1))
    m1 = all((r + 2) * p[r] * p[r + 2] <= (r + 1) * p[r + 1] ** 2 + p[r] * p[r + 1] for r in range(q, top - 1) if r + 2 <= a)
    return uni, wlc, m1


if __name__ == '__main__':
    NMAX = int(sys.argv[1]); out = sys.argv[2]
    nonlc = []
    for fn in sys.argv[3:]:
        for line in open(fn):
            if line.startswith('EX') and 'first_bad=-1' not in line:
                p = [int(x) for x in re.search(r'p=(\S+)', line).group(1).split(',')]
                par = re.search(r'parents=(\S+)', line).group(1)
                nonlc.append((par.count(',') + 1, tuple(p)))
    by_n = {}
    for n, p in set(nonlc):
        by_n.setdefault(n, set()).add(p)
    print('non-LC tree sequences by order:', {n: len(v) for n, v in sorted(by_n.items())})
    MR = max(1, NMAX - 26)
    R = rooted_trees(MR)
    TP = {m: sorted(set(f for f, g in R[m])) for m in range(1, MR + 1)}
    print(f'rooted trees of order 1..{MR}:', {m: len(R[m]) for m in R})
    print(f'distinct tree polynomials of order 1..{MR}:', {m: len(v) for m, v in TP.items()})
    FP = {}
    for m in range(0, MR + 1):
        res = set()

        def rec(rem, maxm, cur):
            if rem == 0:
                res.add(tuple(cur)); return
            for s in range(min(rem, maxm), 0, -1):
                for tp in TP[s]:
                    rec(rem - s, s, mul(cur, list(tp)))
        rec(m, m, [1])
        FP[m] = res
    print(f'distinct forest polynomials of order 0..{MR}:', {m: len(v) for m, v in FP.items()})
    total = 0; fails = []
    for nt, seqs in sorted(by_n.items()):
        for m in range(0, NMAX - nt + 1):
            for T in seqs:
                for Rp in FP[m]:
                    p = mul(list(T), list(Rp)); total += 1
                    u, w, m1 = check(p, nt + m)
                    if not (u and w and m1):
                        fails.append(dict(tree_order=nt, rest_order=m, T=T, R=Rp, unimodal=u, strict_wlc=w, m1=m1))
    print('forests checked (distinct polynomial pairs):', total, 'failures:', len(fails))
    json.dump(dict(NMAX=NMAX, nonlc_orders={n: len(v) for n, v in by_n.items()}, forest_polys={m: len(v) for m, v in FP.items()},
                   checked=total, failures=fails), open(out, 'w'), indent=1)
