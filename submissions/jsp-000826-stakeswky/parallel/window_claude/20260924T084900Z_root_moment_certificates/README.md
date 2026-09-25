# Addendum: rigorous interval certificates for polynomial root moments

Independent Claude window. **ORIGINAL=NOT_CLOSED. WindowLC is not proved for n >= 31.**

This addendum to `20260924T083841Z_nested_interlacing_flnyz_sharpening` turns the refutation of a
polylogarithmic root-moment bound into rigorous certificates. The FLNYZ root moment is
M = q_v(1-q_v) delta_v^2 = Cov(1_v,|I|)^2 / Var(1_v).

- **Trees.** Spherically symmetric "adaptive nested-hub" trees, with the child counts fixed in
  advance: hub levels with k children alternate with gather levels with d = round(y_t / ln(1+R_hub))
  children.
- **Method.** n is computed exactly as an integer. The level recursion
  R_i = l exp(-c_i ln(1+R_{i-1})), D_i = 1 - c_i q_{i-1} D_{i-1} is evaluated in outward-rounded
  interval arithmetic: Decimal at 80 digits, with correctly rounded ln/exp widened by a relative 1e-75,
  and rechecked at 300 digits.
- **Certified results:**

| activity | tree | n | certified M | consequence |
|---|---|---|---|---|
| l = 1 | k = 14, 6 double levels | 21 digits (log10 n = 20.647) | [5.254278e6, 5.254278e6] | M/(ln n)^2 >= 2325 |
| l = 3 | k = 18, y_t = 2.814, 24 double levels | 71 digits | [4.562450e41, 4.562450e41] | M/(ln n)^2 >= 1.7e37 and log M / log n >= 0.588 |

These certify, in particular, that any bound of the form M <= C (log n)^2 fails for the
certified trees unless C is astronomically large. Together with Section 10.3 of the attached
`WINDOW_LC_PROGRESS.md` (the exponent a*(l) = 2 - 2/p*(l) matches FLNYZ's Hoelder exponent), no
polylogarithmic root-moment bound exists.

The only change to `WINDOW_LC_PROGRESS.md` relative to the previous directory is the
"Rigorous certificates" paragraph in Section 10.3.

## Files

- `src/rm_certificate.py`: certificate script.
- `src/nested_hubs.py`: construction of the l = 1 child counts.
- `logs/python/rm_certificate.log`, `logs/python/rm_certificate.exit`: run output.
- `MANIFEST.sha256`: hashes of all files.

## Reproduce

    cd src && python3 rm_certificate.py 80 && python3 rm_certificate.py 300
