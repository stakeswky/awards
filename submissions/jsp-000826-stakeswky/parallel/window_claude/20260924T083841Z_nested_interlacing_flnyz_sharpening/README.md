# Nested splits, disjoint unions, and how far the FLNYZ analytic argument can be sharpened

Independent Claude window. **ORIGINAL=NOT_CLOSED. WindowLC is not proved for n >= 31.** This run
continues `..._vertex_splitting_obstruction` and adds Section 10 of `WINDOW_LC_PROGRESS.md`.

## Direction 1: nested splits

A nested vertex lies in some but not all maximum independent sets.

- **Ratio interlacing.** For every tree with n <= 16 that has a nested vertex, some nested v makes
  p(F-v) and x p(F-N[v]) ratio-interlacing on the whole range [1, alpha-1]. Hence X_k(v) <= 0.
- **Exact identity** (checked on 45,115 pairs): for F = U + K2 and Q = p(U),

      s_F(k) = (1 + 2Q_{k-1}/Q_k) s_Q(k) + (4 + 2Q_{k+1}/Q_k) s_Q(k-1).

  So nested splits need LC of U just past its own top. The nested case is therefore a
  disjoint-union (G3) problem, not a genuine reduction.
- **G3 stress test.** 149 non-LC trees x 5,763 partner forests, plus 7,152 unions with the
  slowest-saturating trees. No window-LC failure; the minimal normalised margin is 5.23.

## Direction 2: sharpening FLNYZ

All Lean constants below were checked in the source (commit b2a1d3e); the paper constants were
checked in the arXiv v1 PDF.

- **Activities actually needed for the window:** at most 2.581 over all trees with n <= 20.
  Long-leg spiders tend to 1 + sqrt 2. FLNYZ use [1/4, 12].
- **Root moments are polynomial, and the FLNYZ exponent is sharp.** q(1-q)delta^2 = Cov(1_v,|I|)^2/Var(1_v)
  looks logarithmic on small trees (at most 0.47 for n <= 18; about 0.13 ln n up to n = 400). Adaptive
  nested-hub trees nevertheless make it grow like n^{a*(l)}, with a*(l) = 2 - 2/p*(l), where p*(l) is
  the single-activity threshold of FLNYZ Lemma 4.2.
  - Examples: a* = 0.52 at l = 1, 0.672 at l = 3 and about 0.94 at l = 12.
  - The construction and the Hoelder upper bound agree to about 3 decimals. States are kept at
    250-digit precision and cross-checked at 400 digits.
  - So no polylog root-moment bound exists, and the Hoelder induction cannot be improved in the
    exponent.
- **Free improvements** (no new mathematics):
  - the true scalar sup is 0.9103, not 999/1000;
  - the direct optimal Hoelder exponent p = 1.8915 gives u = 17.4 instead of 31999;
  - bounding beta and (1+l)^2 jointly makes the Fourier constant about 1/2380 instead of 1/114244.
- **Paid improvements** (new lemmas needed):
  - A sharper mean-range lemma mu(3) >= top(alpha) would allow K = [1/4, 3]. Then u = 3.05 and the
    Fourier constant is about 1/85. The paper's own mean bound gives only 0.513 alpha at l = 3.
  - A polylog root-moment lemma cannot exist (see above).
  - Even with all of these, a CLT-based threshold stays of order 10^30 or more.
- **Literature** (web; key items verified):
  - No explicit LCLT is known for all trees.
  - The zero-free (Michelen–Sahasrabudhe) route fails for trees: zeros accumulate at
    lambda_c(Delta), inside the needed activity range.
  - CYYZ (arXiv:2404.04668) give degree-free spectral independence on all trees for fugacity below
    e^2. This controls root moments only on average; the per-vertex bound is genuinely polynomial.

## Files

- `WINDOW_LC_PROGRESS.md`: Sections 1–10.
- `src/`: `interlace_test.py`, `g3_stress.py`, `slow_saturation.py`, `mean_range_scan.py`,
  `root_moment_growth.py`, `rm_climb.py`, `scalar_sup.py`, `nested_hubs.py`, `rm_exponent.py`,
  `rm_adaptive.py`, `rm_sharpness.py`, `rm_highprec_check.py`, `rm_hp_adaptive.py`, `e993lib.py`, and the
  non-LC tree inputs.
- `logs/python/`: one `.log` and one `.exit` per run.
- `MANIFEST.sha256`: hashes of all files.
