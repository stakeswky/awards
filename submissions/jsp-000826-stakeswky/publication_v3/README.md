# Pending v3 progress: reconstructible source publication

Publication date: 2026-09-18. This commit publishes the previously conversation-only source, generators and archived receipts. It does not solve Erdos #993 and does not claim a fresh Lean run or external review.

## What is now available from Git

The five text parts and the standard-library restorer reconstruct a pinned, source-only tar.xz packet (42,292 bytes, SHA-256 in SOURCE_PACKET.json). Its 67 files include the 59-type branch checker, complete v3 study/replay code, archived summaries and Lean receipts, four fixed historical Lean templates and two deterministic historical generators, and the v3 algebra source/generator. Reconstruction checks all **176 historical modules plus six v3 modules** against their archived individual source hashes. No project .olean, compiler binary or runtime library is shipped. This closes the source-availability gap by fully reconstructible source, not by merely publishing hashes.

One explicit single-character transport edit is recorded in the manifest; the restorer checks the transported parts before that edit and the complete original archive after it. The extracted mathematical source bytes are unchanged.

## Reproduce

From this directory, with Python 3.10+ and a new destination:

```bash
python3 restore_source_packet.py --out /tmp/erdos993-v3-source
cd /tmp/erdos993-v3-source/continuation_v3
python3 restore_sources.py
bash run.sh --test
LEAN_BIN=/path/to/lean-4.31.0 bash run.sh --lean
LEAN_BIN=/path/to/lean-4.31.0 bash run.sh --lean-historical
```

The two Lean commands are separate, fresh source builds. Running a restorer, reading a saved log or passing program tests is not a Lean build. The local publication rehearsal successfully restored every source hash and passed 12 program tests; it did not execute Lean. Archived Lean results cover the finite 14-vertex auxiliary tree, generic corridor lemmas and the integer local stability lemma, not the full forest problem. The explicit successor-natural-number interface is not presented as an already-proved Mathlib interface bridge.

## Pending mathematical results now recorded

The expanded palette has 59 nonuniform branch types satisfying the common coefficient hypotheses. Its written E/P log-concavity bound applies for t>=24, and the distinguished r/h corridor for t>=47. The v3 finite prefix independently checked all 35,990 expanded-palette triples and all 53,130 original-palette five-branch multisets. All remain unimodal; these are bounded palette results, not exhaustive all-tree results. Remaining finite gaps before the large-t theorem are original-palette t=6..23 and expanded-palette t=4..23.

The archived 89,120 raw graph records are not encoded here. The included sources regenerate them; the archived summaries specify their hashes and exact audit scope. The conversation full-data archive remains the raw-byte delivery. In particular no new mathematical replay of all those records is claimed in this publication step. Older CHECKPOINT/README files inside the packet retain their historical publication-blocked wording; this publication note supersedes only that availability statement, not their validation dates or proof scope.

All prior remote work is retained. PR #1 stays Draft and unmerged. Main and live prize records are untouched. AI assistance: OpenAI ChatGPT. No novelty, priority or award entitlement is claimed.
