#!/usr/bin/env python3
"""Exact certificate lowering the restricted palette thresholds to 45/47.
Standard library only; this checks algebra, not Lean or general forests.
"""
import argparse
import json
from fractions import Fraction
from hashlib import sha256
from math import comb
from pathlib import Path
from branch_study import palette, bounds


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(row):
    return (json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode()


def integer_bounds(t, limit):
    """N/D = sum_j binom(t,j)(3/4)^j (k-1)_(j-1)/(18t)^(j-1)."""
    require(type(t) is int and t >= 1 and limit >= 1, 'invalid bound range')
    denominator = 4 * (72*t)**(t-1)
    weights = [comb(t,j)*3**j*(72*t)**(t-j) for j in range(1,t+1)]
    values = [0]
    for k in range(1, limit+1):
        falling = 1
        total = weights[0]
        for j in range(2, min(t,k)+1):
            falling *= k-j+1
            total += weights[j-1]*falling
        values.append(total)
    return denominator, values


def rational_bound(t, k):
    """Second evaluation: successive summand ratios, not integer weights."""
    term = Fraction(3*t,4)
    result = term
    for j in range(1, min(t,k)):
        term *= Fraction(3*(t-j)*(k-j),72*t*(j+1))
        result += term
    return result


def check_t(t, row_stream=None):
    limit = 18*t+2
    denominator, n = integer_bounds(t, limit)
    bad = {'LC': [], 'corridor_square': [], 'mode_localization': []}
    digest = sha256()
    for k in range(1, limit+1):
        q = rational_bound(t,k)
        require(n[k]*q.denominator == q.numerator*denominator,
                'independent bound evaluations disagree')
        if n[k] <= (k+1)*denominator:
            bad['mode_localization'].append(k)
        row = {'t':t, 'k':k, 'numerator':str(n[k]), 'denominator':str(denominator)}
        data = encode(row)
        digest.update(data)
        if row_stream is not None:
            row_stream.write(data)
    for k in range(2, 18*t+2):
        lo, hi = n[k-1], n[k+1]
        if lo*hi < k*denominator*(lo+hi+denominator):
            bad['LC'].append(k)
        if lo*lo < k*denominator*(2*lo+denominator):
            bad['corridor_square'].append(k)
    return {'t':t, 'bound_values_compared':limit,
            'interior_indices_checked':18*t,
            'failed_indices':bad, 'rows_sha256':digest.hexdigest()}


def main(out):
    target = Path(out)
    target.mkdir(parents=True, exist_ok=False)
    pal = palette()
    old = bounds()
    old_digest = sha256(encode(old)).hexdigest()
    rows = []
    with (target/'bound_rows.jsonl').open('wb') as stream:
        for t in range(45,70):
            r = check_t(t, stream)
            require(not r['failed_indices']['LC'], 'LC certificate failed')
            if t >= 47:
                require(not r['failed_indices']['corridor_square'], 'corridor bound failed')
                require(not r['failed_indices']['mode_localization'], 'mode bound failed')
            rows.append(r)
            print('checked t='+str(t), flush=True)
    boundary = [check_t(44), check_t(46)]
    require(boundary[0]['failed_indices']['LC'] == list(range(34,50)), 't=44 control drift')
    require(boundary[1]['failed_indices']['corridor_square'] == [40,41], 't=46 control drift')
    summary = {
        'status':'PASS_EXACT_THRESHOLD_CERTIFICATE_NOT_LEAN',
        'palette':pal, 'new_LC_threshold':45, 'new_corridor_threshold':47,
        'finite_t_range':[45,69], 'max_degree_a':18*69,
        'bound_values_compared':sum(r['bound_values_compared'] for r in rows),
        'LC_indices_checked':sum(r['interior_indices_checked'] for r in rows),
        'corridor_indices_checked':sum(r['interior_indices_checked'] for r in rows if r['t']>=47),
        'unbounded_tail':{'t_min':70,'positive_coefficients_per_polynomial':[len(p) for p in old],
                          'certificate_sha256':old_digest},
        'rows':rows, 'method_failure_controls':boundary,
        'bound_rows_sha256':sha256((target/'bound_rows.jsonl').read_bytes()).hexdigest(),
        'scope':'Same 21-type palette. Both E and P are log-concave for every t>=45; the r/h corridor is certified for every t>=47. Written proof plus exact algebra, not a full Erdos 993 theorem, Lean proof, or external review.'
    }
    (target/'threshold_summary.json').write_bytes(json.dumps(summary,indent=2,sort_keys=True).encode()+b'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['rows','method_failure_controls','palette']},indent=2))


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    main(p.parse_args().out)
