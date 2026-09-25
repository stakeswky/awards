# Stage 18: analytic nested-hub infinite family

This bounded task addresses the precise Stage-17 gap: finite root-moment certificates did not prove asymptotic growth.

Result: an explicit recursively defined family of ordinary finite unweighted trees at hard-core activity `lambda=1` satisfies

`M_root(T_m) >= C |T_m|^alpha`

with the proved coarse exponent

`alpha = log(4761/400)/log(1936) = 0.327249517292562...`.

Therefore `M/(log n)^d` is unbounded for every fixed `d`. This rules out every fixed-degree polylogarithmic universal root-moment upper bound of that form. It does not prove the sharper numerical exponent reported by the parallel window, and it does not solve Erdős #993.

Files:

- `PROOF.md`: complete written derivation;
- `verify_bounds.py`: exact rational/integer side-condition checks;
- `run.log`: completed script output;
- `result.json`: machine-readable scope and verdict;
- `verify_numeric_family.py`: independent high-precision recurrence check of the first 12 family members;
- `numeric_prefix.log`: completed output of that finite sanity check.

No Lean build or axiom audit was run in this stage.

One local development run of the Decimal sanity script initially demanded exact Decimal equality for the identity `D_1=7` and failed only at the `1e-99` rounding level. The final script uses a `1e-90` tolerance; the exact identity itself is proved algebraically in `PROOF.md`.
