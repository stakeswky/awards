/-
# Reduction of Erdős #993 (all orders) to window log-concavity

Independent addition (Anthropic Claude via Claude Code, 2026-09-23), built on the
external FLNYZ formalization at commit `b2a1d3e`. It proves no new mathematics
about forests; it machine-checks the *reduction*:

* for every forest on `Fin n` (any `n`), strict log-concavity of the independence
  sequence on the window `[⌈n/4⌉, ⌈(2α−1)/3⌉]` implies unimodality;
* hence window log-concavity for all forests implies Erdős #993 for all forests;
* combined with the formal large-order theorem `main_fin`, it suffices to prove
  window log-concavity below the (existential) threshold `N₀`.

It reuses `isUnimodal_of_central_logConcave`, `monotoneOn_icoeff_prefix`,
`antitoneOn_icoeff_tail`, `isBipartiteOn_of_isAcyclic` and `main_fin`.
-/
import ErdosProblem993.Main

namespace ErdosProblem993

open Finset

/-- Strict log-concavity of the independence sequence of `G` on the window
`[⌈n/4⌉, ⌈(2α−1)/3⌉]`, written division-free as in the external development. -/
def WindowLC {n : ℕ} (G : SimpleGraph (Fin n)) : Prop :=
  ∀ k, (n + 3) / 4 ≤ k → k ≤ (2 * alpha G Finset.univ + 1) / 3 →
    icoeff G Finset.univ (k - 1) * icoeff G Finset.univ (k + 1) < icoeff G Finset.univ k ^ 2

/-- **Reduction (every order).** A forest whose independence sequence is strictly
log-concave on the window is unimodal. -/
theorem isUnimodal_of_windowLC {n : ℕ} (G : SimpleGraph (Fin n)) (hG : G.IsAcyclic)
    (hW : WindowLC G) : IsUnimodal (icoeff G Finset.univ) := by
  have hcard : (Finset.univ : Finset (Fin n)).card = n := by simp
  by_cases hPm : (n + 3) / 4 < (2 * alpha G Finset.univ + 1) / 3
  · refine isUnimodal_of_central_logConcave (L := (n + 3) / 4) (P := (n + 3) / 4)
      (m := (2 * alpha G Finset.univ + 1) / 3) (U := (2 * alpha G Finset.univ + 1) / 3)
      le_rfl hPm le_rfl ?_ ?_ ?_
    · intro j k hjk hk
      exact monotoneOn_icoeff_prefix hG Finset.univ hjk (by rwa [hcard])
    · intro j k hj hjk
      exact antitoneOn_icoeff_tail (isBipartiteOn_of_isAcyclic hG Finset.univ) hj hjk
    · intro k hLk hkU
      exact hW k hLk hkU
  · rw [not_lt] at hPm
    refine ⟨(n + 3) / 4, ?_, ?_⟩
    · intro j k hjk hk
      exact monotoneOn_icoeff_prefix hG Finset.univ hjk (by rwa [hcard])
    · intro j k hj hjk
      exact antitoneOn_icoeff_tail (isBipartiteOn_of_isAcyclic hG Finset.univ)
        (le_trans hPm hj) hjk

/-- **Erdős #993 from window log-concavity.** If every forest is strictly
log-concave on its window, every forest is unimodal. -/
theorem erdos993_of_windowLC
    (hW : ∀ (n : ℕ) (G : SimpleGraph (Fin n)), G.IsAcyclic → WindowLC G) :
    ∀ (n : ℕ) (G : SimpleGraph (Fin n)), G.IsAcyclic → IsUnimodal (icoeff G Finset.univ) :=
  fun n G hG => isUnimodal_of_windowLC G hG (hW n G hG)

/-- **What remains, formally.** With the external large-order theorem, it
suffices to prove window log-concavity for forests of order below the
(existential) `N₀`. -/
theorem erdos993_of_windowLC_below :
    ∃ N₀ : ℕ, (∀ (n : ℕ), n < N₀ → ∀ (G : SimpleGraph (Fin n)), G.IsAcyclic → WindowLC G) →
      ∀ (n : ℕ) (G : SimpleGraph (Fin n)), G.IsAcyclic → IsUnimodal (icoeff G Finset.univ) := by
  obtain ⟨N₀, hN₀⟩ := main_fin
  refine ⟨N₀, fun hW n G hG => ?_⟩
  by_cases hn : N₀ ≤ n
  · exact hN₀ n hn G hG
  · exact isUnimodal_of_windowLC G hG (hW n (by omega) G hG)

end ErdosProblem993
