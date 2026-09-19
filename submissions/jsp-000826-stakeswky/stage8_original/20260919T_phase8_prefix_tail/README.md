# Phase 8: prefix/tail research and position-aware forest search

Run `20260919T_phase8_prefix_tail`, based on the observed remote commit
`b71e0e5c87b7da24980af0f4cc73f2fc34593f11`.
**ORIGINAL NOT_CLOSED / NO_STRUCTURAL_ADVANCE.**
PR #1 stays Draft and unmerged; main and live prize records are not changed.

Read STATEMENT.md for accepted results, PROOF_ATTEMPT.md for complete scoped
proofs and the missing top-level connection, GAP.md for the exact remaining
domain, SOURCES.md for external theorem/dependency boundaries, and REVIEW.md
for arithmetic/coverage review. VERDICT.json separates every status.

## What changed

We verified a sharper established decreasing-tail bound and targeted negative
LC minors before that bound, always retaining a full original-valley scan.
All 91 previously omitted LC-input bank pairs were checked at every actual
root class. A separate unequal-depth grammar used whole-subtree replacement,
long-range transplant, duplication, cross-grafting, edge subdivision/cuts and
heterogeneous components. Neither lane reached an early LC failure or a true
valley. New distinct graph count is 12,586 relative only to the supplied
Phase7 inventory, not an all-order or all-history claim.

The proof attempt gives an exact pair partition, an actual six-vertex
obstruction to termwise positivity, a sharp k=2 bound and a short uniform
initial range. The remaining middle interval is unproved. No local bound or
auxiliary refutation is represented as ORIGINAL closure.

## Public native-source reproduction (standard-library Python)

The Git package stores complete source/input bytes in SOURCE_BUNDLE.part01
through part06 (base64 of a pinned tar.xz). Run:

```sh
python3 UNPACK_SOURCE.py
```

The unpacker checks the archive and every file hash, refuses unsafe paths or
unexpected members, and writes native readable files under src/, sources/
and provenance/. The bundle includes the exact Phase7 bank and prior
positional summary. It does NOT include the cached prior graph-code inventory
or large old coefficient streams. Those are available in the conversation
archives, or regenerated from Phase7's public source bundle. In a clean Git
clone, first unpack/reproduce the preceding Phase7 package as its README
specifies. Then from this directory:

```sh
python3 -S -B src/audit_baseline.py ../../stage7_original/20260919T_phase7_inverse_cut_search
for i in $(seq 0 12); do python3 -S -B src/lc_bridge.py --left "$i"; done
python3 -S -B src/morph_search.py
python3 -S -B src/pairing.py
python3 -S -B src/regressions.py
python3 -S -B src/audit.py
python3 -S -B src/replay.py --phase7 <actual-Phase7-directory>
```

The delivery ZIP already contains native sources, sources/prior_codes.jsonl.gz
and all outputs, so the two new search lanes do not need the earlier raw
streams to run. Baseline positional replay and the complete 18-command replay
do require the four fixed Phase7 coefficient streams. This requirement is
explicit, not silently replaced by a hash or a stale receipt. Do not use
Python -O: assertions are part of the checks.

## Hosted versus archived bytes

Git hosts this documentation, the source/input bundle and manifest, and
compact AUDIT_SUMMARY, BASELINE_POSITIONS, REGRESSIONS and REPLAY_SUMMARY
certificates. Full AUDIT and CLEAN_REPLAY receipts remain in the archive.
The graph streams, 29 MB compressed full-A/B material file, full pairing
controls, selected records, execution logs and cached prior inventory are in
the delivery ZIP and regenerate from source. They are NOT all Git-hosted.
REPLAY_SUMMARY lists every complete output hash and length, and identifies
the full execution receipt by hash. The clean run compared
34 outputs with no fields omitted and removed its temporary directory.

The source engine's root DP and separate vertex-deletion algorithm recount
every P. All A/B arrays are computed for all vertices; every A/B is dual
recounted only for the selected 24 materials. HEREDITARY remains UNKNOWN for
new graphs. No original counterexample, full formal proof, axiom audit,
independent peer review or prize entitlement is asserted. Existing external
census qualifications and earlier research are retained unchanged.
