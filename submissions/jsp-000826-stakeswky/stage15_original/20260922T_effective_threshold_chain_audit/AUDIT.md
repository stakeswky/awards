# Stage 15: effective-threshold dependency audit

Date: 2026-09-22

## Scope

This is a bounded source audit of the pinned external Lean development
`junwei-lu/Erdos_993_Tree_Independent_Set_Unimodality` at commit
`b2a1d3ede8aef259b1de6e319e7fd6cb56481ac1`.

The task was to follow the threshold witness used by `main_fin` and either obtain
an explicit numerical `N₀` or identify the first precise source step whose witness
is still non-numerical. This run does **not** claim a fresh Lean build, a fresh
axiom audit, independent peer review, or a solution of Erdős #993.

## Result

No numerical `N₀` is extracted in this run. The threshold chain can, however, be
sharpened substantially.

The first confirmed non-numerical witness in the inspected `main_fin` dependency
path is the radius `R` produced by `exists_tail_small` inside
`curvature_limit` in `ErdosProblem993/Curvature.lean`.

That lemma obtains `R` from abstract convergence of truncated integrals using
`tendsto_setIntegral_of_monotone` and `Metric.tendsto_atTop.1`. In the actual use,

```
f(t) = t^2 * exp(-c₀ t^2)
η    = π ε / 3
```

and the proof asks for a natural `R >= 1` such that the integral of `f` outside
`[-R,R]` is at most `η`. The source proves existence but does not give a numeral
or an arithmetic formula for this `R`.

This is a more precise obstruction than merely saying that `central` or
`mean_lc` is existential.

## Exact threshold chain

The inspected source gives the following dependency chain.

1. `main_fin` takes the witness `N₁` from `central` and returns
   `max 1000 N₁`.
2. `central` takes the witness `N` from `mean_lc` and returns `max N 1`.
3. `mean_lc` sets
   `ε = 1 / (2 * sqrt(2π))`, takes the witness from `curvature_limit ε`, and
   returns `max N 1`.
4. `curvature_limit ε` constructs all quantities explicitly until it invokes
   `exists_tail_small` and obtains `R`. Once `R` is supplied, it sets
   `ε₁ = π ε / (4 R^3)`, obtains the explicit-threshold theorem
   `stdCharFn_tendsto_gaussian R ε₁`, sets
   `X = R^2 + 5 R^5 / (12 π ε)`, and returns
   `max N₁ (ceil(X/c) + 1)`.
5. `stdCharFn_tendsto_gaussian` itself returns the explicit threshold
   `ceil(Λ^2/c) + 1`, where its `b`, `η`, and `Λ` are explicitly defined from
   `R`, `ε`, and the constants supplied by `linear_variance` and `root_moments`.

Thus the compact-characteristic-function convergence used by
`curvature_limit` is not the source of an unspecified size threshold in this
pinned proof: its size witness is written as a concrete ceiling expression.

## Constants checked before the obstruction

The source also makes the earlier constants constructive enough to trace.

- `charFn_bound` uses the exact constant `1/114244`.
- `linear_variance` uses the exact lower constant
  `1/(8*13^4) = 1/228488`.
- `exists_scalar_two` uses `b = 999/1000`.
- `exists_scalar_p` sets
  `theta = 1 - (1-b)/8`, `p = 3/2 + theta/2`, and then derives `rho`.
  Exact rational reduction gives
  `theta = 7999/8000` and `p = 31999/16000`.
- The later root-moment construction sets `u = p/(2-p)` and
  `a = 1 - 1/u`, hence exactly
  `u = 31999` and `a = 31998/31999`.
- `potL(a)` is explicitly `1/(2^(1-a)-1)`.
- `exists_poly_mul_exp_le` gives the explicit witness
  `M = (1+c*n)^n` with `n = ceil(k)+1`.

The accompanying standard-library Python check recomputes the exact rational
reductions above. It does not validate transcendental inequalities or Lean
proof terms.

## Why this does not yet give a numeral

Replacing the existential tail-radius step requires an explicit upper bound for

```
∫_{|t| > R} t^2 exp(-c₀ t^2) dt.
```

After that, a fully numerical `N₀` would still require certified numerical upper
and lower bounds for the explicit real constants occurring downstream, including
those built from `rho`, real powers, `potL(a)`, and the root-moment constant.
The present source gives formulas for those quantities, but this run did not
turn all of them into rational interval certificates.

Therefore the correct status is:

- external large-forest theorem: preserved;
- threshold dependency: narrowed to a precise source obstruction;
- explicit integer `N₀`: **not established**;
- original Erdős #993: **not closed**.

## Source pins

External commit:
`b2a1d3ede8aef259b1de6e319e7fd6cb56481ac1`

Inspected source blob SHAs:

- `ErdosProblem993/Main.lean`: `109ec849c2b23c9a5d35e95ad629f993a92b9793`
- `ErdosProblem993/Central.lean`: `3da5eec63721ef3f063969cae39f3de052533c4a`
- `ErdosProblem993/Curvature.lean`: `9213aa4f6dcc862190828d0c5d3943b8533024a9`
- `ErdosProblem993/CLT.lean`: `3def743fd721791b3e2ad6da1e144dea1f2198e7`
- `ErdosProblem993/RootMoments.lean`: `048972cbbf38ca33e0944f907e99a6f2565721ff`
- `ErdosProblem993/Fourier.lean`: `a0fd4e517b059a503d104d92758e40a59acd9270`

## Execution record

`verify_constants.py` was run with Python 3.13.5 and returned
`PASS_EXACT_RATIONAL_REDUCTION` for the rational reductions listed above.

No `lean` or `lake` executable was present in this runtime, so no fresh external
Lean build or axiom audit was run. The pinned external repository's own claims
remain external evidence, not a fresh project execution result.

## Next bounded task

A useful next task is to replace the `exists_tail_small` call, for this specific
Gaussian-type function, with a proved explicit tail inequality and propagate a
symbolic radius through `curvature_limit`. Only after that should a run attempt
certified rational interval evaluation of the remaining explicit real constants.
