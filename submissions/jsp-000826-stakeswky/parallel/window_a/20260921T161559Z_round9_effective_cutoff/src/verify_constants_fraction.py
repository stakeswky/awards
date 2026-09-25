"""Exact-rational A9 constant audit; no floating arithmetic or network access.

The infinite inequalities are proved in PROOF.md. This program checks the
finite rational premises, log/sqrt enclosures, and all-n exponent certificate.
Run: python verify_constants_fraction.py --output NEW_DIRECTORY
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from math import isqrt, factorial
from pathlib import Path
import json
import sys
sys.set_int_max_str_digits(0)


def log_bounds(x: F, terms: int = 128) -> tuple[F, F]:
    if x < 1:
        low, high = log_bounds(1 / x, terms)
        return -high, -low
    z = (x - 1) / (x + 1)
    z2 = z * z
    term, total = z, F(0)
    for r in range(terms):
        total += 2 * term / (2*r + 1)
        term *= z2
    remainder = 2 * term / ((2*terms + 1) * (1-z2))
    return total, total + remainder


def sqrt_bounds(x: F, scale: int = 10**18) -> tuple[F, F]:
    assert x >= 0
    q = isqrt((x.numerator * scale**2) // x.denominator)
    low, high = F(q, scale), F(q+1, scale)
    assert low * low <= x < high * high
    return low, high


def outward(interval: tuple[F, F], places: int = 18) -> dict:
    low, high = interval
    assert low <= high
    scale = 10**places
    lower = (low.numerator * scale) // low.denominator
    upper = -((-high.numerator * scale) // high.denominator)
    return {"lower_numerator": lower, "upper_numerator": upper,
            "denominator": scale, "rounding": "outward"}


def pair(x: F) -> list[int]:
    return [x.numerator, x.denominator]


def run() -> dict:
    tests: list[dict] = []
    def lt(name: str, left: F | int, right: F | int) -> None:
        left, right = F(left), F(right)
        assert left < right, name
        tests.append({"id": name, "left": pair(left), "right": pair(right),
                      "strict": True, "pass": True})
    p, u, a, rho = F(1999, 1000), 1999, F(1998,1999), F(999,1000)
    assert a == 2-2/p and 1/(1-a) == u and 1+1000*rho == 1000
    lt("exponent_a_below_one", a, 1)
    lt("exponent_a_above_two_thirds", F(2,3), a)
    exp_lower = sum((F(997,400)**h / factorial(h) for h in range(21)), F(0))
    lt("continuous_p2_contraction_exp_Taylor20", 12, F(199,200)*exp_lower)
    lt("p_interpolation_integer_power", 3*F(199,200)**499, rho**500)
    lt("e_lower_Taylor4", F(8,3), sum((F(1,factorial(h)) for h in range(5)),F(0)))
    lt("qstar_power26", F(12,13)**26, F(1,4))
    lt("u_minus_p_at_least26", 26, u-p)
    lt("u_minus_one_at_least26", 26, u-1)
    lt("1000_power_one_over1999_below2", 1000, 2**1999)
    lt("weighted_delta_square_constant", 12*10**6*4, 2**26)
    lt("gamma_induction_constant", 4*u*384000, 2**32)
    lt("weighted_gamma_square_constant", 12*2**64, 2**68)
    lt("centroid_mean_constant", 4*u*2**26, 2**39)
    lt("centroid_squared_exponent", F(1,2), 2*a-1)
    lt("sqrt_half_below_three_quarters_squared", F(1,2), F(9,16))
    lt("variance_lower_lambda_quarter", F(1,2**13), F(32,625))
    lt("variance_lower_lambda_twelve", F(1,2**13), F(6,28561))
    lt("variance_upper", F(1,4)+2**39, 2**40)
    for label, value in [("p_quarter",F(1,5)),("bernoulli_quarter",F(8,25)),("bernoulli_twelve",F(24,169))]:
        lt("frequency_beta_"+label, F(1,8), value)
    lt("frequency_unscaled", F(1,2**12), F(1,2704))
    # Compact CF constants, clearing squares when a square root is present.
    lt("block_cf_constant_squared", 2**13, (2**7)**2)
    assert (2**26)**2 == 2**39 * 2**13
    assert 2**47 == 2**35 * 2**13 // 2
    assert 2**51 == 2**39 * 2**13 // 2
    assert 8*u == 15992 and 4*u == 7996
    assert 7+6*32 == 199 and 26+4*32 == 154
    assert 47+5*32 == 207 and 51+5*32 == 211
    assert -56+2*32 == 8 and 1+32+56 == 89 and 89-256 == -167
    assert 77-13 == 2*32
    assert F(2**13,4) == 2**11  # Gaussian moment integral; sqrt(2*pi)>1 in proof.
    lt("prefix_central_tail_join_at1000", F(1000,4)+1, F(999,3))
    lt("paper_upper_join_linear_margin_at500", F(1002,3), F(17*500,25))
    lt("formal_upper_join_linear_margin_at500", F(1002,3), F(64*500,95))
    cutoff_log2 = 2600000
    exponent_specs = [(199,4),(154,15992),(207,1999),(211,7996),(11,1)]
    exponents = [F(c)-F(cutoff_log2,d) for c,d in exponent_specs]
    for idx, exponent in enumerate(exponents):
        lt("cutoff_term_exponent_"+str(idx), exponent, -8 if idx==1 else -12)
    lt("constant_tail_exponent", -167, -12)
    lt("sum_error_bound", F(1,256)+5*F(1,4096), F(1,128))
    assert F(1,3)-F(1,128) == F(125,384)

    l2 = log_bounds(F(2))
    l13 = log_bounds(F(13))
    l10 = log_bounds(F(10))
    s2 = sqrt_bounds(F(2))
    s12 = sqrt_bounds(F(12))
    s13 = sqrt_bounds(F(13))
    s13over12 = sqrt_bounds(F(13,12))
    xlow = (s12[0]+s13[0])/(1+s2[1])
    xhigh = (s12[1]+s13[1])/(1+s2[0])
    lratio = (log_bounds(xlow)[0], log_bounds(xhigh)[1])
    qstar = (s13over12[0]*(3*l2[0]/s2[1]+2*lratio[0]),
             s13over12[1]*(3*l2[1]/s2[0]+2*lratio[1]))
    mean_factor = (l13[0]/qstar[1], l13[1]/qstar[0])
    target_lo, target_hi = F(680891044148,10**12), F(680891044149,10**12)
    assert target_lo < mean_factor[0] <= mean_factor[1] < target_hi
    lt("paper_mean_endpoint", F(17,25), target_lo)
    lt("formal_endpoint_narrower_than_paper", F(64,95), F(17,25))
    lt("formal_endpoint_above_two_thirds", F(2,3), F(64,95))
    assert l2[0] > F(1,2) and l2[1] < 1
    log10_cutoff = (cutoff_log2*l2[0]/l10[1], cutoff_log2*l2[1]/l10[0])
    digits = log10_cutoff[0].numerator // log10_cutoff[0].denominator + 1
    assert digits == log10_cutoff[1].numerator // log10_cutoff[1].denominator + 1 == 782678
    return {"status":"PASS_EXACT_RATIONAL_PREMISES", "uniform_scope":"Analytic proofs in PROOF.md; no continuum grid or graph-size census",
            "method":"Fraction, integer isqrt, positive Taylor sums, atanh logarithm with geometric remainder",
            "sqrt_scale":10**18, "log_terms":128,
            "parameters":{"p":pair(p),"a":pair(a),"u":u,"rho":pair(rho),"C0":1000},
            "finite_checks":tests,"finite_check_count":len(tests),
            "intervals":{"log2":outward(l2),"log13":outward(l13),"log10":outward(l10),
                         "Qstar12":outward(qstar),"mean_factor12":outward(mean_factor),
                         "log10_cutoff":outward(log10_cutoff)},
            "cutoff":{"exact":"2^2600000","binary_exponent":cutoff_log2,
                      "decimal_digits":digits,"term_exponents":[pair(v) for v in exponents],
                      "error_strict_upper":pair(F(21,4096)),"error_target":pair(F(1,128)),
                      "second_difference_strict_lower":pair(F(125,384))},
            "all_smaller_forests_covered":False,"Lean":"NOT_RUN"}


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    target=args.output/'CONSTANTS_FRACTION.json'
    if target.exists(): raise SystemExit('Refusing to overwrite output')
    result=run();target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS',result['finite_check_count'],'finite exact checks; cutoff has',result['cutoff']['decimal_digits'],'digits')
if __name__=='__main__': main()
