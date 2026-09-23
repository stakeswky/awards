# Fresh local build and audit of the external FLNYZ Lean formalization

Run: `20260923T074907Z_external_flnyz_lean_build` (window `claude`, independent of windows A–E).

**ORIGINAL=NOT_CLOSED.** This run builds and audits the external authors' formalization
(Fang, Lu, Nevo, Yao, Zheng; arXiv:2609.20961). It proves nothing new and claims no novelty,
priority or award status. PR #1 stays Draft. The shared `RESEARCH_STATE.json` is not modified.

## What was built

| Item | Value |
|---|---|
| Repository | https://github.com/junwei-lu/Erdos_993_Tree_Independent_Set_Unimodality |
| Commit | `b2a1d3ede8aef259b1de6e319e7fd6cb56481ac1` (clean worktree; the project's pinned commit, also the current HEAD) |
| Toolchain | `leanprover/lean4:v4.29.1` via elan 4.2.4; Lake 5.0.0 |
| Mathlib | `5e932f97dd25535344f80f9dd8da3aab83df0fe6` (from `lake-manifest.json`) |
| Commands | `lake exe cache get`, then `lake build`, then `lake env lean ErdosProblem993/AxiomCheck.lean` |

## Results

- **Build.** `Build completed successfully (8267 jobs)`, exit 0. All 19 project modules were
  compiled in this run. There were 0 errors and 0 `declaration uses 'sorry'` warnings; the 32
  warnings are all linter or deprecation messages.
- **Axiom audit.** All 14 headline declarations depend only on `propext`,
  `Classical.choice` and `Quot.sound`. No `sorryAx` appears, and no `Lean.ofReduceBool`
  (so no `native_decide`).
- **Statement correspondence** (`audit/StatementAudit.lean` prints the elaborated
  statements). `main_fin` states: there exists N0 such that for every n >= N0, every
  `G : SimpleGraph (Fin n)` with `G.IsAcyclic` has `IsUnimodal (icoeff G univ)`. The
  definitions match the original problem:
  - `icoeff` counts independent k-subsets, using Mathlib `IsIndepSet` (pairwise
    non-adjacent);
  - `IsAcyclic` means no cycle walk, so forests may be disconnected;
  - `IsUnimodal` allows plateaus, and `isUnimodal_iff_finite` proves it equivalent to the
    finite definition on 0..alpha.
- **Lemmas valid at every order** (`audit/EndsAudit.lean`):
  - `monotoneOn_icoeff_prefix`: every forest is nondecreasing through ceil(n/4);
  - `antitoneOn_icoeff_tail`: every bipartite graph is nonincreasing from ceil((2 alpha - 1)/3).

## Boundaries

- N0 is **existential**. The formal `main_fin` uses `max 1000 N1` with N1 from the
  existential `central`. The project's explicit A9 cutoff 2^2600000 is **not** formalized.
- **Residual trust:**
  - the Lean 4.29.1 kernel and the three standard axioms;
  - Mathlib `.olean` files from the official cache (not rebuilt from source; `lean4checker`
    not run);
  - statement correspondence, which was checked by reading the elaborated statements, not by a
    second formalization.
- This is not external peer review. The remaining original-problem gap (the middle window for
  orders below N0) is untouched by this run.

## Files

- `LEAN_BUILD_RECEIPT.json`: versions, exit codes, per-module compile times, axiom lines,
  statement and ends audit outputs, and SHA256 of every source file built.
- `audit/StatementAudit.lean`, `audit/EndsAudit.lean`: independent audit inputs, run with
  `lake env lean <file>` from the external repository root.
- `logs/`: complete logs and exit codes. One home-directory path is redacted; see
  `REDACTION.json`.
- `VERDICT.json`: machine-readable status.
