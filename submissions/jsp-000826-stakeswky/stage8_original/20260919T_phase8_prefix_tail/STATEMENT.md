# Phase 8 result and boundaries

**ORIGINAL: NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** No legal non-unimodal forest
or counterexample to the proposed prefix-LC condition was found. The full
prefix condition remains unproved. The first original-problem gap was not
reduced.

For a forest with n vertices, independence number alpha and independent-set
counts p_k, let beta=ceil(alpha(n-1)/(n+alpha)). An established theorem of
Basit--Galvin makes the tail from beta weakly decreasing. Thus LC at every
1<=k<beta would suffice for ORIGINAL. We also track the older forest tail
b0=ceil((2alpha-1)/3), with beta<=b0. These are external known theorems, not
new results.

The written work proves an exact independent-set pair partition for
p_k^2-p_(k-1)p_(k+1), with the actual exterior F-N[S] retained. The six-vertex
star K1,5 has a negative individual partition term at k=2<beta=3, disproving
termwise positivity and the union/intersection-preserving injection shortcut.
The complete minor is nevertheless 40>0. This is not a prefix-LC or ORIGINAL
counterexample.

Two uniform aggregate bounds are proved: for n>=3,

    p_2^2-n p_3 >= (n-1)(n-2)(n^2-3n+6)/12 > 0,

with equality for stars; and L_k>=0 whenever n>=2k(k-1)(k+1). These bounds do
not reach every k<beta. No claim of novelty or original-domain closure.

The old 8,882-graph coefficients were reread. Of their 6,818 non-LC cases,
none breaks before either tail; beta is earlier in 4,055 cases. This is not
new graph coverage or a fresh Phase7 independent-set recount.

New actual-forest checks:

| Lane | Distinct graphs | Non-LC | Maximum order | Prefix failures / valleys |
|---|---:|---:|---:|---:|
| All 91 omitted LC-input bank pairs, every root class | 11,628 | 43 | 216 | 0 / 0 |
| Unequal-depth grammar, whole-subtree changes, heterogeneous products | 958 | 226 | 376 | 0 / 0 |
| Combined | 12,586 | 269 | 376 | 0 / 0 |

All 12,586 are new relative to the fixed Phase7 inventory only. There are
145 disconnected records and 38 with at least two large components. No
six-component construction passed the declared order cap; this is not an
all-order census. Whole P was dual-recounted for every graph; all 3,065,560
vertex A/B arrays were computed, but only the 24 material graphs received a
second recount of every A/B array (8,452). New HEREDITARY statuses remain
UNKNOWN. All are LOCAL with D-U<=1; residual pairs and nonvacuous RSM tests
are zero.

A fresh-copy replay executed 18 commands and compared 34 complete outputs,
all bytes, with no mathematical fields omitted. This is same-model review,
not external peer review or Lean formalization. The external component-30
census/H2/H3 and the 247-small-index qualification remain unchanged. FAMILY
is unchanged. No minimum counterexample or global novelty claim is made.
