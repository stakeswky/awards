#!/usr/bin/env python3
from fractions import Fraction
from math import ceil, pi, sqrt, exp, erfc

def ceil_fraction(q: Fraction) -> int:
    return (q.numerator + q.denominator - 1) // q.denominator

def main() -> None:
    rational_cases = [
        (Fraction(1, 2), Fraction(1, 10)),
        (Fraction(1, 100), Fraction(1, 1000)),
        (Fraction(3, 7), Fraction(2, 13)),
        (Fraction(1, 114244), Fraction(1, 100)),
    ]
    for c, eta in rational_cases:
        a = Fraction(4, 1) / (c * c * eta)
        R = ceil_fraction(a)
        bound = Fraction(4, 1) / (c * c * R)
        assert R >= 1
        assert Fraction(R, 1) >= a
        assert bound <= eta
        print(f"c={c} eta={eta} R={R} algebraic_bound={bound} ok=True")

    eps = 1 / (2 * sqrt(2 * pi))
    for c in [0.5, 0.1, 0.01]:
        r1 = ceil(12 / (pi * eps * c * c))
        r2 = ceil(48 / (sqrt(2 * pi) * c * c))
        assert r1 == r2
        print(f"mean_lc c={c} R_formula1={r1} R_formula2={r2} equal=True")

    # Numerical controls only; the mathematical proof does not depend on them.
    for c, R in [(0.5, 10), (0.1, 100), (0.01, 10000)]:
        exact_tail = (
            R * exp(-c * R * R) / c
            + sqrt(pi) / (2 * c ** 1.5) * erfc(sqrt(c) * R)
        )
        coarse = 4 / (c * c * R)
        assert exact_tail <= coarse
        print(
            f"numeric_tail c={c} R={R} exact={exact_tail:.17g} "
            f"coarse={coarse:.17g} ok=True"
        )

    print("PASS_EFFECTIVE_GAUSSIAN_TAIL_SANITY")

if __name__ == "__main__":
    main()
