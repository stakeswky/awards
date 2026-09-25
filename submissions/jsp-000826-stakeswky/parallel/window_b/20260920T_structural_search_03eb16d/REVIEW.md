# Internal review and repairs

Review type: same-model self-review with independent algorithms and exact
reproduction, NOT independent external peer review. ORIGINAL NOT_CLOSED.

1. Input recovery. Actual remote head/state/protocol and PR metadata were read.
   The requested Window-B markdown file was not accessible; this limitation is
   recorded rather than inventing its contents. The latest visible baseline
   did not contain a new parallel-A claim. Tests target inherited exact claims.
2. Graph legality. Every accepted graph is reconstructed through the original
   DSU validator, rejecting loops, duplicate edges, cycles and invalid labels.
   Disjoint union and grafting preserve actual vertices and edges. Full edge
   lists are archived; no coefficient-only or weighted surrogate is accepted.
3. Complete original statement. Two scans use the whole sequence with plateaus.
   The definition-based independent scan tries valid peak locations and includes
   zero padding through n. No non-LC failure is mislabeled non-unimodality.
4. Counting. Unchanged Phase-6 rooted occupancy DP uses explicit convolution.
   The second implementation uses vertex deletion at centroids, component
   splitting, exact AHU shape memoization and carry-free integer products.
   The pivot changes runtime, not the deletion identity. Small forests also
   agree with exhaustive subset enumeration and the original max-degree
   deletion counter. Shared graph/parsing and addition helpers remain a
   dependency; this is not a fully independent software stack or Lean proof.
5. Arithmetic. Counts, minors, graph validity, alpha and beta are exact.
   Ranking floats never determine failure. p0, p1, p2 and alpha were checked
   separately. The nearest prefix minor is strictly positive, not rounded zero.
6. Product semantics. Each of 23 bank trees is connected, larger than 30 and
   genuinely non-LC; every combination uses distinct bank members. Products
   retain all components. Their 881 occurrences were re-audited, and product
   coefficients were checked again in reversed factor order.
7. Actual scope. 1567 proposals yielded 1546 unique accepted forests after 11
   duplicates and 10 cap exclusions. Deduplication is exact AHU within this
   run, not all history. Selected roots do not mean all rooted isomorphism
   classes. Non-LC members and theorem controls are not universal new coverage.
8. Candidate triage. ORIGINAL/PREFIX/BARRIER failure candidates are all zero.
   Thus original reductions are zero; reducing a merely non-LC graph would
   answer a different problem. No minimal counterexample claim is made.
9. Material conditional counts. Six graphs receive every A/B array by two
   methods; four larger graphs receive five selected roles only. The total
   1150 arrays excludes uncomputed vertices. LOCAL on six examples does not
   imply HEREDITARY. Residual-pair and new nonvacuous RSM counts are zero.
10. Runtime repairs. A 200-second first structure run using the original
    max-degree deletion counter interrupted after 129 recoverable rows. These
    are excluded. A separate centroid verifier was added without modifying
    forest_exact.py, then the complete lane was rerun. A 30-second first
    product call interrupted after 296 recoverable rows; those are also
    excluded and the complete lane was rerun. Both partial logs/bytes are
    preserved in the conversation archive. Bounded in-session workers were
    monitored and completed; no continuing/background service is claimed.
11. Reproduction. Four fresh search commands matched nine entire deterministic
    files byte for byte, including all graph/coefficient records. The material
    audit and regression replay have separate receipts. Timing fields/logs are
    not claimed deterministic. No mathematical fields were silently omitted
    from files that were compared.
12. Publication. Only a new Window-B subtree may be added. Publication must use
    the freshly reread head as parent, retain other windows, use non-force
    fast-forward, then verify the diff, unchanged top-level state and Draft PR.
    The local publication receipt records actual resulting IDs. Passing CI
    would check repository integrity, not settle the mathematical problem.

No fresh Lean run, axiom audit, external component census or novelty review
was executed. Finite successful tests establish no universal theorem.
