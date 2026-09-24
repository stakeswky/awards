# Exhaustive mode-alignment check: all trees with n <= 26 and all forests of order <= 20

Independent Claude window, 2026-09-24. It continues `20260924T143534Z_mode_alignment_route` and
executes the two computations recommended there (trees to n = 26, forests to order 18), taking the
forests two orders further.

**ORIGINAL=NOT_CLOSED.** Erdős #993 is neither proved nor refuted here. This run only extends the
range on which the empirical statements (MA), (S1) and (S2) of the previous run are verified.

Recall (previous run, Theorem 3): if every forest with an edge has an **aligned** vertex v, i.e.

    dist( M(I(F - v)),  M(I(F - N[v])) + 1 ) <= 1,

then every forest is unimodal. (S2) is the pendant-leaf statement: for a leaf v, M(I(F - v)) is at
or one step to the left of M(I(F)). (S1): for any vertex w, M(I(F - w)) is within one step of M(I(F)).

## 1. Method

**Trees (`src/cma.c`).** Free trees are generated once each by the centroid decomposition of run
`20260924T092515Z` (rooted-tree tables, centroid + multiset of branches, bicentroid pairs); the
counts are checked against OEIS A000055. For each tree with sequence p:

- for a vertex v, one deletion DP gives C = I(T - N[v]); then I(T - v) = p - xC needs no second DP
  (from I(T) = I(T - v) + x I(T - N[v]));
- for a leaf v with support u, I(T - u) = (1+x) I(T - u - v), so C = I(T - u)/(1+x) (exact division)
  and all leaves of the same support share one DP;
- leaves are scanned first (grouped by support), then the remaining vertices by increasing
  degree; without `-DFULL` the scan stops at the first aligned vertex. With `-DFULL` every vertex
  is scanned, which gives the complete (S1) and alignment histograms by degree.

Every tree without an aligned leaf is printed with its parent array (`EX_NOLEAF`), and every tree
without any aligned vertex would be printed as `EX_NOALIGN`. `src/reverify_noleaf.py` rebuilds all
printed trees from their parent arrays and recomputes everything with the Python DP of the previous
run.

**Cross-validation.** For n = 14..22 the per-tree counts (trees with an aligned leaf) and the
complete (S2) histograms equal those of `modes.c` (WROM generation, two DPs per vertex) of run
`20260924T143534Z`; with `-DFULL` the (S1) row for leaves and the alignment histogram also agree.
For n = 20: 2,843,452 / 5,027,798 leaf shifts of -1 / 0 in both programs.

**Forests (`src/ma_forests3.py`).** Every forest of order n <= 20 with at least two components and
at least one edge is enumerated once as a multiset of free trees (components of order <= 19). For v
in component T_j, I(F - v) = I(T_j - v) prod_{i != j} I(T_i) and I(F - N[v]) = I(T_j - N[v]) prod_{i != j} I(T_i).
Vertices are tried in a heuristic order (vertices aligned in the component alone first; vertices
equivalent under automorphism are tried once) and the search stops at the first aligned vertex.
Single-component forests are the trees of the exhaustive tree run.

## 2. Results: trees

| n | trees (= A000055) | no aligned vertex | no aligned leaf | trees with a degree-2 support | of which a leaf there is aligned | S2 leaf shifts {-1, 0} | other S2 shifts | S1 range (all vertices) | first aligned vertex degrees |
|---|---|---|---|---|---|---|---|---|---|
| 19 | 317,955 | 0 | 3 | 299,089 | 299,089 | 685,545 / 2,217,054 | 0 | – | {'1': 317952, '2': 3} |
| 20 | 823,065 | 0 | 11 | 780,036 | 780,036 | 2,843,452 / 5,027,798 | 0 | [-1, 1] | {'1': 823054, '2': 11} |
| 21 | 2,144,505 | 0 | 7 | 2,045,924 | 2,045,924 | 10,634,064 / 10,806,578 | 0 | [-1, 1] | {'1': 2144498, '2': 7} |
| 22 | 5,623,756 | 0 | 7 | 5,396,078 | 5,396,078 | 17,727,827 / 40,944,762 | 0 | [-1, 1] | {'1': 5623749, '2': 7} |
| 23 | 14,828,074 | 0 | 93 | 14,299,878 | 14,299,878 | 52,859,117 / 108,296,520 | 0 | [-1, 1] | {'1': 14827981, '2': 92, '3': 1} |
| 24 | 39,299,897 | 0 | 23 | 38,067,356 | 38,067,356 | 207,599,097 / 236,641,530 | 0 | [-1, 1] | {'1': 39299874, '2': 23} |
| 25 | 104,636,890 | 0 | 224 | 101,748,748 | 101,748,748 | 437,660,235 / 790,740,509 | 0 | [-1, 1] | {'1': 104636666, '2': 221, '3': 2, '4': 1} |
| 26 | 279,793,450 | 0 | 335 | 272,995,157 | 272,995,157 | 1,053,650,250 / 2,353,018,615 | 0 | [-1, 1] | {'1': 279793115, '2': 335} |

- **(MA) holds for every tree with 4 <= n <= 26.** No `EX_NOALIGN` line was printed at any order.
- **(S2) holds for every leaf of every tree with n <= 26**: the shift of M(I(T - v)) relative to
  M(I(T)) is -1 or 0 for all 5,331,352,953 leaf deletions; never +1, never -2.
- **(S1) holds for every vertex of every tree with n <= 26** (FULL runs): all single-deletion shifts
  lie in {-1, 0, +1}.
- **A leaf at a degree-2 support is always aligned** (column 6 equals column 5 at every order), as
  (S2) predicts.
- Trees without an aligned leaf: 3, 11, 7, 7, 93, 23, 224, 335 for n = 19, ..., 26 (703 trees). All were
  re-verified in Python from their parent arrays (`results/trees_without_aligned_leaf_n19_26.json`,
  `logs/reverify_noleaf.log`): 703 examples, 0 discrepancies; the aligned vertex of least degree has
  degree 2 in 699 of them, degree 3 in three, degree 4 in one. In every one of them every support
  vertex has degree >= 4 (hub trees); see Section 4.

## 3. Results: forests

| n | forests with >= 2 components and an edge | without an aligned vertex | worst best distance | vertices tried before success (histogram) |
|---|---|---|---|---|
| 10 | 222 | 0 | 1 | {1: 222} |
| 11 | 474 | 0 | 1 | {1: 469, 2: 4, 3: 1} |
| 12 | 1,049 | 0 | 1 | {1: 1049} |
| 13 | 2,356 | 0 | 1 | {1: 2348, 2: 6, 3: 2} |
| 14 | 5,439 | 0 | 1 | {1: 5413, 2: 25, 3: 1} |
| 15 | 12,772 | 0 | 1 | {1: 12756, 2: 14, 3: 2} |
| 16 | 30,584 | 0 | 1 | {1: 30459, 2: 99, 3: 22, 4: 4} |
| 17 | 74,333 | 0 | 1 | {1: 74143, 2: 167, 3: 21, 4: 2} |
| 18 | 183,331 | 0 | 1 | {1: 182919, 2: 323, 3: 59, 4: 19, 5: 8, 6: 3} |
| 19 | 457,573 | 0 | 1 | {1: 456761, 2: 677, 3: 111, 4: 22, 5: 1, 6: 1} |
| 20 | 1,154,812 | 0 | 1 | {1: 1152034, 2: 2483, 3: 232, 4: 47, 5: 10, 6: 5, 7: 1} |

Total: 1,923,150 forests of order 3..20, 0 without an aligned vertex (`logs/ma_forests3_20.log`; the order-18 run `logs/ma_forests3_18.log` is a subset). The count for n = 18, 183,331, equals A005195(18) - A000055(18) - 1 (all forests minus trees minus the edgeless forest).

**(MA) holds for every forest of order <= 20** (trees by Section 2, forests with at least two
components by this table). In 99.8% of the forests the first vertex tried (an aligned vertex of the component taken alone) is aligned in the forest as well; the maximum number of tries was 7 (one forest of order 20).

## 4. What this changes

The three empirical statements now stand on: all 6.6 million trees with n <= 22 (previous run) plus
all 438,558,311 trees with 23 <= n <= 26, all forests of order <= 20, and the sampled large trees of the
previous run. Nothing here is a proof. The obstruction analysis of the previous run (Section 5
there) is unchanged: unimodality of the pieces plus the mediant property allows the +1 shift, and
(S2)/(MA) need one quantitative inequality next to the modes.

Two structural observations from the larger range:

- The trees without an aligned leaf grow in number (3, 11, 7, 7, 93, 23, 224, 335 for n = 19..26) but remain a vanishing fraction, and
  they are all hub trees (every support vertex of degree >= 4). In all but four of them the aligned
  vertex of least degree has degree 2; in three (n = 23, 25, 25) it has degree 3; and in one it has
  degree 4. That one is hubs(6,3), the centre of degree 6 joined to six hubs each carrying three
  leaves (n = 25): its leaves have alignment distance 2, while every hub (degree 4) and the centre
  (degree 6) have distance 1. **This refutes the sharper form stated in the previous run** ("an
  aligned vertex of degree at most 3 always exists"), which held only up to n = 22. What survives:
  every tree has an aligned vertex, and in a tree with a degree-2 support vertex a leaf there is
  aligned (as (S2) predicts). For hub trees the aligned vertex can be a hub or the centre.
- The +1 deletion shifts (S1 table) stay confined to vertices of degree 2 to 13; deleting a leaf never
  raises the mode.

## 5. Boundaries

- ORIGINAL=NOT_CLOSED; no Lean was run.
- The tree computation uses one program (`cma`) at n = 23..26, cross-validated against a second
  program at n <= 22 and against the OEIS counts at every order; the printed exceptional trees were
  re-verified by a third implementation (Python). The forest computation uses one Python program;
  its tree generator and DP are those cross-validated in the previous runs.
- Vertices equivalent under an automorphism of a component give identical pieces and are tried once;
  this does not change which forests have an aligned vertex.
