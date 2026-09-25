# Stage 18: analytic nested-hub infinite family

The written derivation is split across `DERIVATION_A.md` through `DERIVATION_D.md`. It proves an explicit family of finite unweighted trees at activity 1 with `M >= C n^alpha`, where `alpha=0.327249517292562...` and one coarse `C=0.158177938799633...`.

Thus `M/(log n)^d` is unbounded for every fixed degree `d`. This does not prove WindowLC or Erdős #993.

Two local Python checks completed: exact rational side conditions and a 100-digit recurrence check for the first 12 members. Their hashes and scope are recorded in `RESEARCH_STATE.json`. No Lean build or axiom audit was run.
