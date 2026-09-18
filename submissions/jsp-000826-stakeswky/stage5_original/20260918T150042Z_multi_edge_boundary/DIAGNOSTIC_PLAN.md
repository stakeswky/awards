# Fixed Phase-5 diagnosis, written before execution

Target: actual joint multi-edge cut compatibility, not a new sample bound.
The original problem remains unresolved at entry. All array comparisons use
integers; ranking uses fractions. No claim of exhaustive forest coverage.

1. Prove the defect-set partition and root partial-cut formula; test each by
   independent subset enumeration on empty, isolated, path, star, internal
   branch and disconnected controls of order at most 9. Include the missing
   middle edge between the endpoints of two disjoint edges. Test all cuts
   only for these expressly small interaction controls.
2. For five pinned historical material graphs, test every incident partial
   cut and each pair of edges, retaining all branch and external factors.
   These test identities, not the still-empty hard residual case.
3. Directed discovery: use old23, new30, g0013, g0063. Add their disjoint
   old23/new30 and g0013/new30 combinations to retain an external factor.
   Three rounds select three not-yet-expanded seeds: the highest two scores
   and a smallest-order alternative. At each seed use the first four
   conditional bottleneck vertices (smallest conditional mode distance),
   attach either a leaf or a rooted 3-leaf star; also move each of the first
   four internal incident branches one step across its support, and test
   two-edge cuts at degree>=3 supports. Maximum 24 proposals per expanded
   seed, maximum order 100, at most 222 proposals including six initial
   seeds. Rank first D-U, then exact whole-sequence valley score nu, not the
   fraction of bad leaves. Each seed/position/operation is attempted once;
   log duplicate edge lists separately. Freeze after these operations even
   if no residual graph is reached. This is heuristic discovery only.
4. On a true valley, LOCAL failure, or D>=U+2, stop ordinary discovery and
   compute all conditional/edge data with two algorithms. HEREDITARY is
   UNKNOWN unless every proper vertex subset is covered. RSM is checked
   only under its exact premises; off-residual values are not counted.
5. Check the proposed boundary-only compression on actual rooted trees,
   enumerated by child multisets up to order 12, stopping at the first
   equal-message pair with distinct internal conditional profiles. This is
   a diagnostic of information loss, not a compression theorem or original
   counterexample. Compare the pair in actual leaf, path, star, and
   disconnected external completions; retain both underlying graphs.
6. Re-run final sources from a new directory. Compare all deterministic
   output bytes and full parsed arrays. Record failures and repairs, then
   publish a bounded record. No background computation or external service.

## Recorded pre-final repair
The first implementation already used distinct exact seed/operation states, but
symmetric reattachments could repeat an unrooted forest. Before final replay,
an exact whole-forest canonical-type key was added. The three-round/222-proposal
cap was not increased. Initial source and complete outputs are retained under
provenance/pre_repair; final counts are separate, not added to old counts.
This is graph-isomorphism deduplication, not boundary-message compression.
