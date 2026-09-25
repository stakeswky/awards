"""Hub-variant family stress test of D*: trees hub_tree(groups,s,q) with up to two hub
groups (t1 hubs with l1 leaves, t2 hubs with l2 leaves), s centre leaves and q
pendant P2 on the centre, n<=80. Every j after the first strict descent while
History holds; middle-range positions flagged separately.

Usage: python check_hub_variants.py --out DIR [--procs 9]
"""
import argparse
import json
import os
import sys
from fractions import Fraction as Fr
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e993lib as L  # noqa: E402
from families import hub_tree  # noqa: E402


def keys(nmax=80):
    out = []
    for t1 in range(1, 8):
        for l1 in range(1, 21):
            for t2 in range(0, 5):
                for l2 in ([None] if t2 == 0 else range(l1 + 1, 26)):
                    groups = ((t1, l1),) if t2 == 0 else ((t1, l1), (t2, l2))
                    if t1 + t2 < 2:
                        continue
                    for s in range(0, 4):
                        for q in range(0, 3):
                            n = 1 + t1 * (1 + l1) + (t2 * (1 + l2) if t2 else 0) + s + 2 * q
                            if n <= nmax:
                                out.append((groups, s, q))
    return out


def one(key):
    groups, s, q = key
    par, _ = hub_tree(groups, s, q)
    n = len(par)
    ch = L.children_of(par)
    col = L.colours(par)
    p = L.uni_poly(par, ch)
    alpha, h, beta = L.params(p, n, n)
    unimodal = L.is_unimodal(p)
    first = next((k for k in range(len(p) - 1) if p[k] > p[k + 1]), None)
    if first is None:
        return []
    rows = L.biv_rows(par, ch, col)
    out = []
    for j in range(first + 1, len(p)):
        if any(p[k] < p[k + 1] for k in range(first, j)):
            break
        b, a = p[j - 1], p[j]
        S = a * (b - a)
        N, P = L.mass_arrays(rows, j)
        dm = sum(max(x - y, 0) for x, y in zip(N, P))
        out.append(dict(groups=[list(g) for g in groups], s=s, q=q, n=n, j=j, beta=beta,
                        in_middle=(h + 1 <= j < beta), unimodal=unimodal, S=S, Dmass=dm,
                        ratio=(f'{Fr(dm, S).numerator}/{Fr(dm, S).denominator}' if S else None),
                        ratio_float=(float(Fr(dm, S)) if S else None)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--procs', type=int, default=9)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    ks = keys()
    with Pool(args.procs) as pool:
        res = [r for rr in pool.imap(one, ks, chunksize=50) for r in rr]
    viol = [r for r in res if (r['S'] == 0 and r['Dmass'] > 0) or (r['S'] and r['Dmass'] > r['S'])]
    ins = [r for r in res if r['in_middle'] and r['S']]
    outs = [r for r in res if not r['in_middle'] and r['S']]
    order = lambda r: (Fr(r['Dmass'], r['S']), r['n'], r['j'], str(r['groups']), r['s'], r['q'])  # noqa: E731
    top_all = sorted([r for r in res if r['S']], key=order, reverse=True)[:12]
    top_in = sorted(ins, key=order, reverse=True)[:12]
    summ = dict(trees=len(ks), history_positions=len(res), nonunimodal_positions=sum(1 for r in res if not r['unimodal']),
                violations=len(viol), middle_positions=len(ins), plateaus=sum(1 for r in res if r['S'] == 0),
                max_in_middle=top_in[0] if top_in else None, max_overall=top_all[0])
    print('trees', summ['trees'], 'History positions', summ['history_positions'], 'violations', summ['violations'],
          'nonunimodal positions', summ['nonunimodal_positions'])
    print('max overall ratio %.6f groups=%s s=%d q=%d n=%d j=%d beta=%d' % (
        top_all[0]['ratio_float'], top_all[0]['groups'], top_all[0]['s'], top_all[0]['q'], top_all[0]['n'], top_all[0]['j'], top_all[0]['beta']))
    print('max middle-range ratio %.6f groups=%s s=%d q=%d n=%d j=%d beta=%d' % (
        top_in[0]['ratio_float'], top_in[0]['groups'], top_in[0]['s'], top_in[0]['q'], top_in[0]['n'], top_in[0]['j'], top_in[0]['beta']))
    with open(os.path.join(args.out, 'hub_variants.json'), 'w') as fh:
        json.dump(dict(summary=summ, violations=viol[:50], top_overall=top_all, top_middle=top_in),
                  fh, sort_keys=True, separators=(',', ':'), default=str)
        fh.write('\n')


if __name__ == '__main__':
    main()
