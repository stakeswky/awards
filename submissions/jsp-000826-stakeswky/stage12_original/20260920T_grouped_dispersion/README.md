# General grouped-dispersion audit and an all-length LC theorem

**ORIGINAL NOT_CLOSED; general exact BARRIER unresolved.**
The selected-branch-count grouped upper-bound certificate from the user-facing Phase-10 artifact is **false**, including on a connected 1122-vertex tree. A separate written all-parameter proof establishes LC for that tree's entire alternating-backbone family, so it is not an original counterexample.

Read `PROOF.md`, `GAP.md`, `REVIEW.md`, `VERDICT.json` and the exact native certificates. Definitions, birth terms, the precise stronger statement refuted, and every quantifier are in the proof. The connected witness preserves all backbone constraints and all external leaves/arms. No external tree census is needed by these new claims.

## Reproduction

Python 3.10 or newer, standard library only; do not use `-O` because assertions are checks.

```sh
python3 -S -B UNPACK_SOURCE.py
python3 -S -B src/verify_fixed.py
python3 -S -B src/verify_family.py
python3 -S -B src/regressions.py
python3 -S -B src/replay.py
```

`certificates/CONNECTED_WITNESS.json` and `DISCONNECTED_WITNESS.json` include full graphs and complete P arrays, every compressed sector triple/multiplicity, all-vertex mode rows, selected independently recounted full A/B arrays, rational enclosures and exact sign checks. The code recreates them without network or external data. These larger raw files are in the delivery archive, not claimed Git-hosted unless explicitly included in the repository tree.

The connected 5356-class compression covers every independent selection of its 204 backbone vertices. The disconnected 3481-class compression covers all 2^116 root selections. This is proved equality of full sector polynomials within a class, with exact multiplicity retained, not sampled sector selection. It does not generalize to arbitrary graphs as a bounded state count.

`FAMILY_CERTIFICATE.json` lists all 39 positive Bernstein coefficients establishing LC of every real-parameter factor. `PROOF.md` supplies the transfer/factorization connection to every integer backbone length; no finite list of lengths is extrapolated. `HEREDITARY_BASE_CERTIFICATE.json` checks every induced subset of the two small component trees, which certifies only the disconnected witness's HEREDITARY property. The connected witness remains UNKNOWN for HEREDITARY.

Only compact summaries, the finite coefficient certificate, notes and self-contained source are necessary in Git. All full outputs and logs accompany the conversation archive. No external peer review, Lean execution, global minimum, all-forest search bound, novelty or prize eligibility is claimed.

## Recovery and concurrency

Observed remote starting HEAD was b7e76b0737428c08e549ffd2b274122d67772b1a, not the earlier Phase-9 head. It includes concurrent Phase-10 core-cover and Phase-11 global-L3 work, distinct from the user-facing Phase-10 separator artifact. Preserve both. Updates are confined to submissions/jsp-000826-stakeswky/, with PR #1 Draft and unmerged. A publication receipt is written only after real update/readback operations.
