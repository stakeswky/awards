# Phase 3: all-edge compatibility and complete premise audit

**ORIGINAL NOT_CLOSED; NO_STRUCTURAL_ADVANCE.** This is a completed, reviewed
proof attempt, not a solution announcement. Start with STATEMENT.md,
PROOF_ATTEMPT.md and GAP.md. The first missing step remains the universal
joint bound or an actual residual-slope contradiction.

## Actual additions
The written proof records all-edge count identities, endpoint-removal
injections, a global-band leaf/support restriction, and exact edge slope
constraints under a hypothetical valley. None closes the first gap.

A finite complete induced-subset certificate upgrades the existing 23-vertex
bad-leaf witness from LOCAL to HEREDITARY. It refutes EVERY-leaf goodness even
with that stronger premise, but its whole polynomial is unimodal and U=D=8.
The main batch has 60 records (four old controls, 56 new), 60 LOCAL cases,
seven fully HEREDITARY cases, and **zero** residual graphs or eligible RSM tests.

## Reproduce from the run directory (Python standard library)

```sh
python -S -B src/edge_diagnostics.py --controls inputs/controls.json --out certificates
python -S -B src/hereditary.py --inputs certificates/inputs.json --out certificates
python -S -B src/coverage_regression.py --inputs certificates/inputs.json --out certificates
python -S -B src/integrate.py --out certificates
python -S -B src/clean_replay.py
```

Run the first four counting commands to reconstruct omitted raw material from the
compact Git publication. Then clean_replay.py makes a fresh temporary copy, repeats
those commands and compares EVERY deterministic output both as bytes and full
parsed JSON. It writes actual replay logs/receipt, not a synthetic PASS.
Do not use python -O: source assertions are part of these checks. Per-case
resource limits are explicit; a slower machine may report UNKNOWN rather
than complete coverage. A failed or incomplete run is not a verified witness.

## Evidence locations
The delivery archive retains all code, actual inputs, full edge/vertex
coefficient arrays, complete hereditary signatures/multiplicities/witnesses,
direct-enumeration material, original and repaired logs, source hashes, review,
and actual post-publication receipt. The compact Git subtree publishes the
mathematical documents, native tested source, fixed controls, summaries and
replay receipt. The full bad-leaf vertex certificate, raw arrays, signatures,
provenance and logs are in the delivery archive and reconstructible where
specified. Larger raw coefficient/signature files are
reconstructible from source but are NOT claimed to be Git-hosted; see
EVIDENCE_LIST.md. The archival source packet is not an additional computation.

Publication outcome must be read from the receipt created after the actual
ref update. The mathematical files do not assert a future commit SHA.
PR #1 remains Draft; no merge, main/catalog/award change or upstream claim is
authorized. FAMILY is inherited unchanged; there is no new Lean build.
Review is SAME_MODEL_SELF_REVIEW, not outside peer review.
