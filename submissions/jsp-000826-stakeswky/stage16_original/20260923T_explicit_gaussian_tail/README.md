# Stage 16 — explicit Gaussian-tail radius

This package records one bounded effectiveness result for the pinned external
large-forest proof.

Result:

\[
\int_{|t|>R} t^2e^{-ct^2}\,dt \le 4/(c^2R)
\]

for `c>0`, `R>0`. Therefore for target error `eta>0` the source-level existential
tail radius can be replaced by

\[
R = \left\lceil 4/(c^2\eta)\right\rceil.
\]

For the actual `curvature_limit` call this is

\[
R = \left\lceil 12/(\pi\varepsilon c_0^2)\right\rceil,
\]

and at the `mean_lc` value of `epsilon` it is

\[
R = \left\lceil 48/(\sqrt{2\pi}\,c_0^2)\right\rceil.
\]

Files:

- `PROOF.md`: complete written derivation and scope boundaries.
- `verify_effective_tail.py`: standard-library sanity checks only.
- `run.log`: actual output from that script in this run.
- `result.json`: machine-readable status and hashes.

The mathematical proof does not depend on the numerical controls. No new Lean build
or axiom audit was run for this lemma. ORIGINAL remains `NOT_CLOSED`.
