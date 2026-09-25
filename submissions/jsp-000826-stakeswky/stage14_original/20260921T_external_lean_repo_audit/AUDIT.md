# External Lean formalization availability and statement audit

Run date: 2026-09-21 UTC.

## Scope

This is a bounded source/interface audit of the public formalization accompanying Fang--Lu--Nevo--Yao--Zheng, *Unimodality of Independence Polynomials for Sufficiently Large Forests* (arXiv:2609.20961v1). It is not a fresh Lean build, not an independent peer review, and not a proof of the all-order Erdős #993 conjecture.

The project branch was read at `a50dca327a1f6e44e98beb21d7c6b5e796088923` before this write. PR #1 was Draft and unmerged. No main/catalog/candidate/award records are touched.

## Pinned external source

Repository: `junwei-lu/Erdos_993_Tree_Independent_Set_Unimodality`

Pinned commit: `b2a1d3ede8aef259b1de6e319e7fd6cb56481ac1`

Pinned tree: `1e08c8d267130280e307257626c609418c89628b`

The repository is public and readable at this run. This supersedes only the earlier C8 availability observation that the repository returned 404 at that earlier time; it does not retroactively turn the earlier run into a Lean execution.

Selected Git blob identities at the pinned commit:

- `ErdosProblem993/Main.lean`: `109ec849c2b23c9a5d35e95ad629f993a92b9793`
- `ErdosProblem993/Central.lean`: `3da5eec63721ef3f063969cae39f3de052533c4a`
- `ErdosProblem993/Transfer.lean`: `6019a08fe595922f609ecf246b520a6771bf7ced`
- `ErdosProblem993/Basic.lean`: `3a6f9cd529b96a6792128ff0d07075ded350db54`
- `ErdosProblem993/AxiomCheck.lean`: `fd8c9761d21433ddb1faf2e578187ecdfc1b3db6`
- `lean-toolchain`: `33e0c088939ad08c9f2b1befa3118a423b06ad7d`
- `lake-manifest.json`: `d53580702dd90a22ee46e3a5152d1534dc9060c7`

Pinned toolchain metadata states Lean `v4.29.1`; the manifest pins mathlib to `5e932f97dd25535344f80f9dd8da3aab83df0fe6`.

## Statement audit

The formal headline theorem in `Main.lean` is

```lean
theorem main_fin :
    ∃ N₀ : ℕ, ∀ (n : ℕ), N₀ ≤ n → ∀ (G : SimpleGraph (Fin n)), G.IsAcyclic →
      IsUnimodal (icoeff G Finset.univ)
```

`Transfer.lean` proves the corresponding statement for an arbitrary finite vertex type:

```lean
theorem unimodal_of_isAcyclic :
    ∃ N₀ : ℕ, ∀ {V : Type u} [Fintype V] [DecidableEq V] (G : SimpleGraph V),
      G.IsAcyclic → N₀ ≤ Fintype.card V → IsUnimodal (icoeff G univ)
```

The primitive semantics match the intended sufficiently-large forest theorem:

- `icoeff G S k` is the cardinality of independent `k`-subsets of `S`.
- `IsUnimodal f` means there is a mode `m` such that the sequence is weakly nondecreasing up to `m` and weakly nonincreasing thereafter.
- `G.IsAcyclic` is the graph-side forest condition.
- `icoeff_congr` and `isAcyclic_congr` transport the statement from `Fin n` to arbitrary finite vertex types.

Therefore the displayed formal theorem is a faithful formulation of the paper's Theorem 1.1: every sufficiently large finite forest has a unimodal independence sequence.

## Exact threshold boundary

The formal source does **not** expose a numeral for the absolute threshold. `main_fin` chooses

```lean
max 1000 N₁
```

where `N₁` is obtained existentially from `central`. `central` obtains its threshold from `mean_lc`. Thus this audit does not extract a computable finite cutoff from the formal theorem.

Consequently, the theorem gives a genuine all-shape asymptotic exclusion but does not by itself reduce the remaining project work to an explicitly enumerable finite range. In particular, the project's all-order ORIGINAL remains unresolved.

## Axiom/source audit boundary

`AxiomCheck.lean` contains `#print axioms` commands for `main_fin`, `unimodal_of_isAcyclic`, `central`, the analytic core, endpoint monotonicity, and the finite-sequence correspondence theorem. The repository README reports the expected footprint as only `propext`, `Classical.choice`, and `Quot.sound`.

This run did **not** execute those commands. The runtime available to this run had no `lean` or `lake` executable on `PATH`, and no toolchain was installed. Therefore:

- fresh external Lean build: **NOT RUN**;
- fresh axiom audit: **NOT RUN**;
- external README build claim: recorded as an external claim, not reclassified as our execution evidence.

A GitHub code-index search for the token `sorry` at the pinned source returned documentation/comment occurrences; no indexed executable `sorry` occurrence was identified in that search. This is only a source-search observation and is not a substitute for `lake build` or `#print axioms`.

## Mathematical consequence for this project

At the evidence level available here, the external paper plus the now-readable formal source establish a pinned, inspectable statement of the following asymptotic fact:

> There exists an absolute `N₀` such that every forest with at least `N₀` vertices has a unimodal independence sequence.

This is stronger in shape scope than the project's restricted-family results, but it still leaves all orders below the unknown threshold. Combining it with the project's component-order-30 exclusion yields only the qualitative statement that any remaining original counterexample must have order `< N₀` and contain at least one tree component of order at least 31. No explicit value of `N₀` is supplied by this audit.

The external result is attributed to its authors and is not claimed as project novelty.

## Verdict

- `external_large_forest_statement_interface = MATCHED`
- `external_source_now_readable = YES`
- `fresh_external_lean_build = NOT_RUN`
- `fresh_external_axiom_audit = NOT_RUN`
- `explicit_N0_extracted = NO`
- `original_math = NOT_CLOSED`
- `original_formal = NOT_ESTABLISHED`

## Next precise targets

1. Effectivize the external `mean_lc`/`central` chain enough to obtain an explicit numerical threshold, or prove that a particular proof step still hides an untracked constant.
2. Independently continue the exact all-order structural route for the middle interval; do not replace it by the asymptotic theorem while `N₀` is unknown.
3. Keep direct ordinary unweighted forest counterexample checks focused outside already excluded component-order-30 and restricted-family ranges.
