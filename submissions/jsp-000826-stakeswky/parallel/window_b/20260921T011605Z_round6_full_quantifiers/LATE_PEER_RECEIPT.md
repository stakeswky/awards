# Late peer interfaces and E6-ONE full-relation supplement

This is a SEPARATE phase after the completed 16-command base replay. The
base proof, interface v2, source manifest, verdict and replay receipt retain
their original scope and hashes. ORIGINAL remains NOT_CLOSED.

## Newly read immutable interfaces

At parent c60c687ae9bccd849c5385432c6a0a3e6c3d421b, the three additions
since a7e610b6 were read in full:

- A6 root/long-path interface: blob80225d1ba5bfffec7b3caeda24570ac7f1fcafd7.
  A6-R-audit has the SAME A4-R quantifiers already tested. No new graph count
  is added for this alias. A6-PATH's large-length structural gate was NOT
  tested; its full final proof is not asserted to have been read.
- C6 signed-cut/LC-free interface: blob3012df9168d9ca756c1e088123c9b169cc93727a.
  Both new claims were read, but their finite tests were NOT run in B6.
- E6 exterior interface: blob9a1ef87ea0290fc9ada57a851755362f5d8ee3f6.
  E6-ONE-v1 DROPS C-growth, allowing EVERY actual source/target pair with
  at most one new union vertex after its pinned old reservations. E6-EXIT
  is a different proposed scoped theorem; no complete EXIT test is claimed.

The publication preserves all three peer additions, without editing them.

## E6-ONE-v1: full widened relation, independently enumerated

The two existing16-point HEREDITARY whole-graph instances have now been
checked under this ACTUAL new relation. All source groups, positive targets,
old loads and graph coefficients are retained from the already independently
verified full group ledgers. Neither connected16-point tree is a published
exact Q13 extra-flow input. Known old reservations coincide with their JC
ledger. Every permitted edge is enumerated twice, using vectorized integer
bit counts and a separate Python scalar scan. No C condition is imposed.

| Graph | Sources | Demand | Targets | ALL E6-ONE arcs | Validated flow |
|---|---:|---:|---:|---:|---:|
| network16_0 | 1236 | 1513 | 114807 | 19289220 | 1513 |
| network16_2 | 694 | 820 | 135150 | 10008291 | 820 |

There are respectively6525088 and2609727 additional arcs beyond the former
C-growing relation. Full adjacency is stored as compressed little-endian
uint32 rows, with source/target ordering and format in each network JSON.
Zero remaining-capacity positive targets are retained.

Both previously computed Dinic and Edmonds-Karp assignments were freshly
validated edge-by-edge under E6 and against ALL source demands and remaining
target capacities. They saturate all demand, so the full-network optimum is
certified by that feasible flow and the trivial demand upper bound. No NEW
optimizer call on the wider adjacency is claimed. These are the SAME two
graph instances, not two additional graphs, and there is no deficient cut.

The late script was copied to the clean base-replay directory and executed
again: one command exited0 and all five complete outputs,62328167 bytes,
matched byte-for-byte. See LATE_E6_REPLAY_RECEIPT.json. This is separate from
16 commands/64 outputs/687624863 bytes in the base receipt, not a retroactive
change to it. The full narrowed and widened networks are separate files.

## Reproduction and limitation

First reconstruct and run the base package as in README.md, then run:

    python LATE_E6_ONE_AUDIT.py --base ../B6_fresh_replay --output ../B6_E6_ONE

Use a new output directory. LATE_E6_ONE_SUMMARY.json fixes all expected output
hashes; the separate late replay receipt fixes the full five-file comparison.
Raw large adjacency/network files accompany the conversation archive and are
regenerable, not claimed to be Git-hosted raw data.

No all-forest Hall bound, ADMC proof, compensating-root existence theorem or
ORIGINAL closure follows from these two complete successful instances. The
new fixed-T26-fiber theorem in PROOF.md remains pinned to its stated old
ledger; it does not reserve capacity for the new proposed E6-EXIT rule or
for arbitrary future matchings.
