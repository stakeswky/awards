# All-edge attempt: no top-level closure

**NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** The universal joint bound and the
residual obstruction remain unresolved. The following arguments do not infer
unimodality from a general sum or product of unimodal sequences.

## 1. Definitions and inherited dependencies
Use the exact definitions in STATEMENT.md. For the independent-set partition,
mode sign bounds, D<=U+1 criterion, minimal-counterexample exclusions,
valley polarization and RSM=>ORIGINAL, the dependency is Stage-2
PROOF_ATTEMPT.md sections 1-9 at commit
5169aa045816af5a87f5cf17341592ecb3ec8139, under
submissions/jsp-000826-stakeswky/stage2_original/20260918T_original_joint_modes/.
Those arguments were read and checked where used, not assumed from state
labels. Their frozen archive bytes were matched to live Git blob identities.
No inherited proof error was identified in the portions used here.

## 2. Actual all-edge identities (E1)
Let uv be an edge. An independent subset cannot contain both u and v. The
three disjoint cases, neither endpoint, only u, and only v, give

    C=I(F-{u,v}), P=C+B_u+B_v,
    A_u=C+B_v, A_v=C+B_u.

For instance, deleting u from a set containing u bijects that class with the
independent subsets of F-N[u], and contributes exactly one factor x. This
proves the identities from actual subsets rather than defining arrays to
make them hold.

Delete the edge uv. In its original component the sides T_u and T_v are trees,
rooted at u and v. Let R be the independent-set polynomial of all OTHER
components. Put X_u=I(T_u-u), Y_u=xI(T_u-N_Tu[u]) and likewise at v. Choosing
independent subsets on disjoint sides and on the other components gives

    C=R X_u X_v, B_u=R Y_u X_v, B_v=R X_u Y_v,
    P=R(X_u X_v+Y_u X_v+X_u Y_v).

There is no Y_u Y_v term, since uv is an edge. Empty sides after deletion have
polynomial 1. The x in each Y is already included. R is retained in every
coefficient and difference comparison below, never canceled.

For each k>=1, removal of u sends independent k-sets containing u injectively
into independent (k-1)-sets of F-{u,v}. Thus (B_u)_k<=C_(k-1), and similarly
(B_v)_k<=C_(k-1); at k=0 both left sides are zero. These are **coefficientwise**
inequalities. Taking their differences need not preserve the inequality.
No stronger difference estimate was obtained from this injection.

## 3. What compatibility actually forces
### 3.1 Global bands under a separated joint bound (E2)
Assume LOCAL and D>=U+2. For a fixed v, min(r_A,r_B)<=U and
max(ell_A,ell_B)>=D. The interval ending at or before U cannot be the interval
beginning at or after D, since ell<=r for each interval. Therefore each split
has a unique early interval with r_E<=U and a unique late interval with
ell_L>=D. There is no gap in the argument for peak plateaus.

Call v selected-early or selected-late according to the band of B_v. At a
leaf l with neighbor w set C=I(F-{l,w}), H=I(F-N[w]). Actual counts give

    B_l=xC, A_l=C+xH, A_w=(1+x)C, B_w=xH.

C is unimodal because xC=B_l is unimodal. The inherited adjacent-mode lemma
says the mode intervals of xC and (1+x)C are at distance at most one. They
cannot occupy opposite global bands, whose distance is at least two. Thus
B_l and A_w share a band, while B_w has the other band. This proves opposite
selected roles for a leaf and its support under band separation, even without
assuming P already has a valley. It does NOT extend opposition to every
edge, and opposition itself is consistent on a tree.

### 3.2 Edge slopes under an actual valley (E3)
Now assume HEREDITARY and Delta P_i=-s<0, Delta P_j=t>0, with i<j. Here s,t
are strictly positive integers. In every vertex split the early member has
negative difference at i and nonpositive difference at j; the late member
has nonnegative difference at i and positive difference at j. This follows
from the inherited polarization lemma, not merely from the mode labels.
For each selected-early vertex v write

    Delta B_v_i=-a_v, Delta B_v_j=-b_v, a_v>=s>0, b_v>=0.

For each selected-late vertex w write

    Delta B_w_i=c_w, Delta B_w_j=d_w, c_w>=0, d_w>=t>0.

These inequalities follow by subtracting the other member of the split from
Delta P. For the actual edge polynomial C=P-B_u-B_v:

* If u,v are both selected-early, Delta C_i=a_u+a_v-s>=s>0 and
  Delta C_j=t+b_u+b_v>=t>0. C has a late mode: ell_C>=j+1.
* If u,v are both selected-late, Delta C_i=-s-c_u-c_v<=-s<0 and
  Delta C_j=t-d_u-d_v<=-t<0. C has an early mode: r_C<=i.
* If u is selected-early and v selected-late, with a=a_u,b=b_u,c=c_v,d=d_v,

      Delta C_i=a-c-s, Delta C_j=t+b-d.

  C counts a proper induced forest, so is unimodal under HEREDITARY. It cannot
  have a negative difference at i followed by a positive difference at j.
  Consequently every such mixed edge must obey the exact disjunction

      a>=c+s  OR  d>=b+t.                           (E3-mixed)

Equality is allowed in either alternative. No division, limit or real-valued
approximation is used. The same-role mode conclusions require unimodality of
C; their strict signs follow from s,t>0, not a heuristic choice of modes.

### 3.3 The first missing step is not supplied by these restrictions
E3-mixed does not specify one common alternative on all mixed edges. Summing
arbitrarily chosen alternatives, or using separate vertex averages at i and
j to obtain one common vertex, is invalid. Same-role edges are not eliminated:
they force C into the opposite band, but C really is a different proper
induced forest and such a mode is not itself forbidden. The endpoint
injections in section 2 bound coefficients, not the needed differences.

The actual product formulas were retained in an attempt to strengthen this
restriction. They did not yield an inequality that excludes every surviving
assignment. In particular, multiplication by R cannot be removed from the
problem, and the rooted X/Y arrays cannot be replaced by arbitrary unimodal
arrays. Leaf-support alternation provides no numerical contradiction. Deleting
or contracting an edge does not preserve U,D,i,j without a new proof;
contraction also is not generally an induced-subgraph operation and so cannot
silently be justified by HEREDITARY alone. These attempted continuations did
not establish J_H or a direct minimal-counterexample contradiction.

## 4. Finite diagnosis and its actual logical contribution
The prewritten DIAGNOSTIC_PLAN fixes two rooted sides, internal edge/path
joining, and disconnected factors, rather than optimizing one bad root. It
was not extended after the empty residual result. Every whole polynomial,
A_v/B_v and counted cut-edge factor was computed by rooted forest DP and
independent vertex deletion, with complete integer-array comparison. There
were 2,099 full-edge factorizations and 6,999 graph/mask recounts in 60 records.
All 60 were LOCAL, and all had D-U<=1. Hence no actual two-position residual
configuration tested E3 or RSM nonvacuously. Testing algebraic identities on
these graphs is not evidence that the unobserved residual case is impossible.

A separate induced-subset coverage proof and exact computation establish
HEREDITARY for seven selected graphs. This includes the old 23-vertex bad-leaf
control, which previously had only LOCAL verification. Its 8,388,607 proper
subsets are represented by 22,174 rooted-signature entries, each with a
multiplicity and an actual subset witness. Every representative and witness
was recounted in two algorithms. The original graph has

    P=(1,23,231,1359,5287,14516,29219,44068,50306,43483,
       28198,13441,4542,1022,136,8,0,0,0,0,0,0,0,0).

Its peak is 8. At leaf 4, A has peak 7 and B peak 9, but at vertex 0 both peaks
are 8. Thus U=D=8. The stronger every-leaf assertion is false even under full
HEREDITARY; the already-known bad leaf is not new as an underlying graph.
This premise audit does not refute the existential or joint route. All edge
and vertex arrays are retained in the archive; the full 23-vertex vertex
splits are also in the archive bad-leaf certificate, reconstructible by the published source.

The star control still has Q=-5 at (1,2) with U=D=3, outside the residual band.
The 30-vertex control still has 54^2-3135*1=-219 at index 16 and remains
unimodal. Neither is an ORIGINAL refutation. No new RSM estimate from actual
branch products was obtained, so RSM was not promoted to a purported solution.

## 5. Conditional route back to ORIGINAL, with the gap visible
Suppose ORIGINAL fails and choose a least-order counterexample. By the
inherited reductions it satisfies HEREDITARY, has no isolated or K2 component,
and any valley lies in U<=i<j<D. **The next step would be J_H, but J_H is
UNRESOLVED.** If it were proved, D<=U+1 would contradict the valley and close
ORIGINAL. Alternatively, the unchanged RSM would prohibit the valley through
its inherited signed-minor implication, but RSM is also UNRESOLVED.

The direct route using section 3 stops at the same substantive obstacle:
no proof excludes the simultaneous real-forest residual slopes. Calling that
obstacle a new lemma would not prove it. The remaining domain is not shown
smaller than in Phase 2. No full ORIGINAL proof, counterexample, or formal
verification is claimed.
