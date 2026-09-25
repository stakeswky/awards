# Phase 10: arbitrary cores and real exterior/multicomponent exploration

Run `20260919T_phase10_core_cover`. Observed starting head:
`86f0c47070ae80dbd5316c44ec766e8f3c72ffd8`.

**ORIGINAL NOT_CLOSED.** The new scoped arbitrary-core/private-arm theorem is
proved with its stated sufficient conditions. The general BARRIER and
minimum-counterexample elimination remain unproved. No priority claim.

Read `STATEMENT.md`, `PROOF.md`, `GAP.md`, `REVIEW.md`, and `VERDICT.json`.
The theorem allows arbitrary core shape and component count, not arbitrary
forests with no arm condition. It includes an unbounded region of products
of actually non-LC tree components. Real exterior vertices are retained.

## Reproduce from the public source bundle

```sh
python3 UNPACK_SOURCE.py
python3 -S -B src/core_cover.py
python3 -S -B src/explore.py
python3 -S -B src/mixture_audit.py
python3 -S -B src/regressions.py
python3 -S -B src/compact.py
```

Use Python 3.11+ without `-O`: assertions are verification checks. No packages,
network, paid APIs, user computer or continuing worker are required. The source
bundle contains the native Python programs. The unpacker validates hashes
and permits only `src/*.py` members. New mathematical outputs need no old graph
inventory. Source/native checks are not Lean formalization or peer review.

`history_audit.py` is a separate optional exact comparison with the supplied
Phase7/8/9 inventory (21,756 canonical types). Its raw input
`inputs/prior_codes.jsonl.gz` is included in the delivery ZIP, not Git-hosted.
The public `certificates/HISTORY_CHECK.json` records the actual comparison,
not a fresh rerun by a future reader. The search itself does not use this
history filter. With the ZIP input present, rerun that audit and the full
fresh-copy verification with:

```sh
python3 -S -B src/history_audit.py
python3 -S -B src/replay.py
```

Our fresh replay ran six programs and compared ten complete deterministic
outputs with all bytes. The actual receipt is `certificates/CLEAN_REPLAY.json`.
The source copy and temporary directory were created and removed in this run.

## Data availability and scope

Git hosts the proof, notes, source bundle, compact native certificate, history
comparison, and replay receipt. Full P arrays for every search graph, all
vertex mode rows, selected full A/B arrays, exact moment arrays, core-control
polynomials, logs and the old comparison inventory are in the delivery ZIP.
The native source regenerates all new mathematical outputs. Omitted large
arrays are identified by exact hashes/byte counts in NATIVE_CERTIFICATE;
hashes are not represented as public raw-array availability.

Search: 233 actual types, max order 535, 2..7 non-LC-component products included;
zero original valleys. Separately, four theorem controls reach order 4,616,
with full polynomial recounts but no all-vertex recount claim. Neither number
is an exhaustive verification bound. HEREDITARY remains UNKNOWN for new graphs.

PR #1 remains Draft and unmerged. Publication is confined to the existing
submission subtree. Earlier work and external census qualifications are
preserved. Repository CI is not a mathematical certificate. OpenAI ChatGPT
assisted the work. Same-model self-review is not external review.
