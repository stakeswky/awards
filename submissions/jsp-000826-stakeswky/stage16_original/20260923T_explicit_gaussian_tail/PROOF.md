# Stage 16: explicit Gaussian-tail witness for `curvature_limit`

Date: 2026-09-23

## Scope

This run addresses one bounded gap from Stage 15: replace the non-effective call to
`exists_tail_small` used by `curvature_limit` in the pinned external development

`junwei-lu/Erdos_993_Tree_Independent_Set_Unimodality@b2a1d3ede8aef259b1de6e319e7fd6cb56481ac1`

for the specific function

\[
f(t)=t^2 e^{-c t^2}, \qquad c>0.
\]

This is a written mathematical proof plus small reproducibility controls. It is not a
fresh Lean build, is not external peer review, and does not solve Erdős #993.

## The explicit tail lemma

**Lemma.** Let `c > 0` and `R > 0`. Then

\[
\int_{\mathbb R\setminus[-R,R]} t^2 e^{-c t^2}\,dt
\le \frac{4}{c^2 R}.
\]

### Proof

For every `x >= 0`, the exponential power series gives

\[
e^x \ge \frac{x^2}{2}.
\]

For `|t| > R > 0`, put `x = c t^2`. Then `x > 0`, so

\[
e^{-c t^2}\le \frac{2}{c^2 t^4}
\]

and hence

\[
t^2e^{-c t^2}\le \frac{2}{c^2t^2}.
\]

Both sides are nonnegative and even. Therefore

\[
\begin{aligned}
\int_{\mathbb R\setminus[-R,R]} t^2 e^{-c t^2}\,dt
&=2\int_R^\infty t^2e^{-ct^2}\,dt\\
&\le \frac{4}{c^2}\int_R^\infty t^{-2}\,dt\\
&=\frac{4}{c^2R}.
\end{aligned}
\]

This proves the lemma.

## An explicit natural-number witness

Let `eta > 0` and define

\[
R_{\rm eff}=\left\lceil \frac{4}{c^2\eta}\right\rceil.
\]

Because the quantity inside the ceiling is positive, `R_eff >= 1`, and

\[
R_{\rm eff}\ge \frac{4}{c^2\eta}.
\]

Consequently

\[
\frac{4}{c^2R_{\rm eff}}\le\eta,
\]

so the preceding lemma gives

\[
\int_{\mathbb R\setminus[-R_{\rm eff},R_{\rm eff}]}
t^2e^{-ct^2}\,dt\le\eta.
\]

Thus the existential radius required by `exists_tail_small` is replaced by a closed
formula.

## Substitution into the pinned `curvature_limit`

The pinned source sets

\[
c_0=\min(c',1/2),\qquad
\eta=\pi\varepsilon/3.
\]

Hence one may take

\[
\boxed{
R_{\rm eff}
=
\left\lceil\frac{12}{\pi\varepsilon c_0^2}\right\rceil
}.
\]

At the later `mean_lc` call,

\[
\varepsilon=\frac{1}{2\sqrt{2\pi}},
\]

so this simplifies to

\[
\boxed{
R_{\rm mean}
=
\left\lceil\frac{48}{\sqrt{2\pi}\,c_0^2}\right\rceil
}.
\]

Once this `R` is substituted, the rest of the Stage-15 threshold chain keeps the
same explicit formulas already present in the pinned source:

- `epsilon_1 = pi * epsilon / (4 * R^3)`;
- `stdCharFn_tendsto_gaussian R epsilon_1` supplies its explicit ceiling threshold;
- `X = R^2 + 5 R^5 / (12 pi epsilon)`;
- `curvature_limit` returns the maximum of that threshold and `ceil(X/c)+1`.

Therefore the Gaussian-tail radius is no longer an existential obstruction at the
mathematical level.

## What remains non-numerical

This run does **not** produce a numerical `N0`. A numeral still requires certified
upper/lower bounds for the explicit real constants entering `c0`, the characteristic
function threshold, and the root-moment/variance constants. Those quantities are
formula-defined in the pinned source, but Stage 15 did not yet turn all of them into
rational interval certificates.

The next effective-threshold task should start from these explicit real constants,
not from `exists_tail_small`.

## Formalization status

The proof is designed to be Lean-friendly:

1. `Real.sum_le_exp_of_nonneg x hx 3` already appears elsewhere in the pinned
   development and yields a finite Taylor lower bound strong enough to derive
   `x^2 / 2 <= exp x`.
2. The remaining work is a standard comparison of nonnegative integrals against
   `2/(c^2 t^2)` on the two tails and evaluation of the improper integral of `t^-2`.

No Lean source for this new lemma was compiled in this run. Accordingly its formal
status is `WRITTEN_PROOF_ONLY`, not `LEAN_PASS`.

## Consequence for the project

This closes one specific effectiveness gap from Stage 15:

`Gaussian tail radius R in curvature_limit: existential -> explicit formula`.

It does not close the finite range below the external large-order theorem, does not
prove the remaining window log-concavity statement, and does not provide an original
counterexample.
