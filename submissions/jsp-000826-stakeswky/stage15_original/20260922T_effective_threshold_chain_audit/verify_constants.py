#!/usr/bin/env python3
from fractions import Fraction
import json, hashlib

b = Fraction(999, 1000)
theta = 1 - (1 - b) / 8
p = Fraction(3, 2) + theta / 2
u = p / (2 - p)
a = 1 - 1 / u
variance_lower_c = Fraction(1, 8 * 13**4)
charfn_c = Fraction(1, 114244)
expected = {
    "b": "999/1000",
    "theta": "7999/8000",
    "p": "31999/16000",
    "u": "31999",
    "a": "31998/31999",
    "variance_lower_c": "1/228488",
    "charfn_bound_c": "1/114244",
}
actual = {
    "b": str(b),
    "theta": str(theta),
    "p": str(p),
    "u": str(u),
    "a": str(a),
    "variance_lower_c": str(variance_lower_c),
    "charfn_bound_c": str(charfn_c),
}
assert actual == expected, (actual, expected)
print(json.dumps({"status":"PASS_EXACT_RATIONAL_REDUCTION", **actual}, sort_keys=True, indent=2))
