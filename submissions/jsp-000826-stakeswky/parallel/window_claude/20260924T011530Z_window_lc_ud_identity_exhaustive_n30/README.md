# WindowLC continuation: extension identity, under-dispersion (UD), exhaustive n = 30

Independent Claude window. **ORIGINAL=NOT_CLOSED; WindowLC is not proved for n >= 31.**

- **Identity** (every graph, written proof; verified by literal enumeration on all 985 trees with
  3 <= n <= 12): mu_k = mu_{k-1} + Var_{k-1}(e)/mu_{k-1} - 1 - D_k, where e is the number of
  addable vertices. Hence LC at k <=> Var <= mu(1 + D + mu/k).
- **UD** (Var_{k-1}(e) <= mu_{k-1}) implies LC at k.
  - Coefficient form: p_k^2 >= (1+1/k) p_{k-1} p_{k+1} + (2/k^2) p_{k-1} A_k.
  - Equivalently, log g_{k-1} is concave at y = 1.
- **Evidence for UD in the window:**
  - all trees with 8 <= n <= 19: max Var/mu = 0.75, and 0.55–0.63 for n >= 13;
  - all 28 non-LC trees with n <= 29: max 0.198;
  - 4,425 hub/core trees with n <= 60: max 0.62.

  UD fails only in the deep tail (>= 0.84 alpha).
- **Refuted route:** real-rootedness of the free-count slices.
- **Exhaustive n = 30:** all 14,830,871,802 trees are unimodal, with strict window LC and 0 window
  equalities. There are 121 non-LC trees, all breaking at >= 0.9375 alpha. All 237 forests of
  order <= 30 with a non-LC component pass. The open range for WindowLC is now 31 <= n < N0.

Files: `WINDOW_LC_PROGRESS.md` (statements, proofs, evidence), `src/`, `results/wlc_strict_n30.json`,
and `logs/`, which holds the n=30 run, the forest check and the UD exhaustive log for n = 8..19.
