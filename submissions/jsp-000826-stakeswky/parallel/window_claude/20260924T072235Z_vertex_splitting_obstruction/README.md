# Vertex-splitting induction for WindowLC: the constant 3/2, exhaustive checks, and an exact obstruction

Independent Claude window. **ORIGINAL=NOT_CLOSED. WindowLC is not proved for n >= 31. This run
refutes one proof strategy and locates why it fails.**

This run continues `20260924T011530Z_window_lc_ud_identity_exhaustive_n30`. The attached
`WINDOW_LC_PROGRESS.md` repeats Sections 1–6 of that run unchanged and adds Sections 7–9.

## Results

### Hypothesis Q(F)

Q(F) states: for 1 <= k <= min(top(alpha), alpha-1),

    2n (p_k^2 - p_{k-1} p_{k+1}) >= 3 p_k^2,   with top(alpha) = ceil((2 alpha - 1)/3).

- Q implies strict WindowLC, and with the formalised tail monotonicity it implies unimodality.
- 3/2 is the largest constant valid for all forests: 2K1 attains equality.
- Q holds for **all 23,522,619,472 trees with 4 <= n <= 30** and **all forests of order <= 22**.
  Both checks are exhaustive, in exact `__int128` arithmetic. Forests are enumerated as T - r:
  535.9 million instances.

### One-step vertex splitting (Section 9)

The step uses p = p(F-v) + x p(F-N[v]) with exact surplus bookkeeping. The pieces get the induction
hypothesis on [1, top] and, in the gap zone, one of three bounds:

- LM (Levit–Mandrescu monotonicity);
- TR (`tail_ratio`, formalised);
- TRnu (a König-type improvement).

The step holds for all trees with n <= 30 and all forests of order <= 19, but it is **false in
general**. Counterexamples, each confirmed by a second independent computation:

| counterexample | order | fails with |
|---|---|---|
| S(2,2,2,2) + 11 K1 | 20 | LM; exact minimum, by exhaustion |
| P5 + 16 K1 | 21 | LM |
| S(2,2,2) + 21 K1 | 28 | TR |
| 12 P3 + 13 K1 | 49 | TRnu |
| tree R(19,0) (a root joined to 19 cherry centres) | 58 | TRnu, and infinitely many R(s,0) |

In every case Q itself holds.

### Mechanism

- Every failure is at k = top(alpha) when top(alpha) = top(alpha-1)+1, in a forest with a unique
  maximum independent set.
- Every split then needs a piece just past its own top. There the extension-counting bounds
  overstate P_{i+1}/P_i by about 2x.
- A true, stronger bound (Newton, for a real-rooted piece) restores slack of about +2.

So the scheme only moves the difficulty to "approximate LC just beyond 2 alpha/3", a statement of the
same type as WindowLC.

### Nested vertices (Section 9.5)

A nested vertex lies in some but not all maximum independent sets. If one exists, the step needs no
gap-zone bound.

- There is no failure on any non-unique-MIS tree with n <= 26, any non-unique-MIS forest of order
  <= 20, or the stress families up to n = 140.
- This is not a real reduction: the cross term still encodes LC of the pieces.

### Refuted and audited

- **Weak LC fails.** "p_k/k! is LC" is false: an n = 30 tree has p_14 p_16 / p_15^2 = 1.7268.
  119 of the 149 non-LC trees (n = 26..30) have a unique maximum independent set.
- **FLNYZ effectiveness.** In the read-only audit, `central` gives strict LC on
  [ceil(n/5), floor(64 alpha/95)], which reaches past top. That is exactly the missing regularity,
  but only for n >= N0. The chain is effective in principle. However, the formalised root-moment
  exponent is a = 31998/31999, so an N0 read off from it exceeds 10^660000 (for eps <= 1, R >= 1).

## Files

- `WINDOW_LC_PROGRESS.md`: statements, proofs of the identities used, evidence, obstruction
  (Sections 7–9).
- `src/`:
  - Python: exact `Fraction` arithmetic.
  - C: `stepc.c` (trees), `stepf.c` (forests), and the nested variants `stepcn.c` and `stepfn.c`.
  - Runner scripts, including absolute paths from the original working directory.
  - Four small input JSON files: the non-LC tree lists.
- `logs/python/`: one `.log` and one `.exit` per Python check.
- `logs/c/`: every C run, including the n = 30 tree run (6418 s), the forest runs for orders 20–22,
  the nested-mode runs and the n = 12 checksum cross-check against `wlc.c` / `wlc3.c`.
- `MANIFEST.sha256`: hashes of all files.

## Reproduce

    cc -O2 -o stepc src/stepc.c -lpthread && ./stepc 24 3 2 8        # trees n = 24, c = 3/2
    cc -O2 -o stepf src/stepf.c -lpthread && ./stepf 21 3 2 8        # forests of order 20
    cc -O2 -o stepcn src/stepcn.c -lpthread && ./stepcn 20 3 2 8 nested
    cd src && python3 verify_obstruction_claims.py && python3 closed_form_checks.py
