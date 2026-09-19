# Phase 7: direct counterexample search by inverse cuts

**ORIGINAL NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** No counterexample found.

Baseline: `stakeswky/awards`, branch `jsp-000826-research-snapshot`, observed HEAD `f9f2d5bccd6e514e293749046f3488bf5c179524`. PR #1 stays Draft and unmerged. All earlier research is retained.

Read `STATEMENT.md`, `GAP.md`, `REVIEW.md`, `VERDICT.json` and `certificates/AUDIT.json`. This is a bounded executed search on actual unweighted forests, not a complete proof or an order census.

The four lanes check one-bridge joins, vertex-count-preserving wedge slides, disconnected component products, and all-vertex corridor-targeted slides. There are 8,882 distinct graph records, maximum order 525, all unimodal, with no residual pair. Five repeat supplied Phase-6 controls and two more are small-component-only controls. Every P is independently recounted; all vertex A/B conditions are computed. See the audit for the smaller scope of independent A/B recounts. No new HEREDITARY claim is made.

## Reproduce

The Git package includes the complete Python source and fixed JSON inputs as three binary archive parts, `SOURCE_BUNDLE.part01` through `part03`, with a SHA-256 manifest. Run `python3 UNPACK_SOURCE.py` to validate and unpack them. This uses only the Python standard library. Then run, without Python's `-O` option:

```sh
python3 -S -B src/build_bank.py
python3 -S -B src/bridge_search.py
python3 -S -B src/slide_search.py
python3 -S -B src/forest_search.py
python3 -S -B src/corridor_search.py
python3 -S -B src/audit.py
python3 -S -B src/replay.py
```

The delivery archive already contains source and all generated files. Source/input hashes, complete output hashes, actual exit codes and clean-replay observations are in `certificates/CLEAN_REPLAY.json`. The replay compares all bytes of 12 mathematical outputs; elapsed times occur only in logs/receipts. The gzip research record streams use fixed metadata for determinism.

## Availability and attribution

Git hosts the source/input bundle, compact documentation and verification receipts. The four full graph streams and `materials_full.json` are in the conversation delivery archive; they are source-regenerable and identified by hashes, not claimed Git-hosted. Every record stores its actual edge list, complete P, every vertex's mode intervals, U/D, real valleys, origins and full-conditional hash. The 25 material graphs additionally store all complete A/B arrays.

The unchanged `forest_exact.py` comes from the previous Phase-6 package; its SHA-256 remains `897199820b50cf1750fa7a5d3934e4fcf8d7921a1fb8dacba0d1d875e7cba172`. Input metadata are derived from that delivery, pinned to the baseline commit. Deeper spherical-tree motivations: D. Galvin, *Trees with non log-concave independent set sequences*, arXiv:2502.10654v2, 23 January 2026. The original problem is Alavi--Malde--Schwenk--Erdős (1987), catalogued as Erdős Problem #993. No global novelty is asserted for families, formulas or searched graphs. Existing repository licensing applies. OpenAI ChatGPT assisted the research and same-model review.

No full external census, all-forest finite UNSAT, fresh Lean build, axiom audit, outside peer review, solver status or award claim is made. Finite zero counterexamples is not a theorem of universal absence.
