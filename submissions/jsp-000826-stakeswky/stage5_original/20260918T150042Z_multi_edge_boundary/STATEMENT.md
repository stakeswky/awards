# Phase 5: exact statements and status

**ORIGINAL: NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** No legal original
counterexample, no strict reduction of the first original-problem gap.

## Original target and inherited hypotheses
For every finite simple undirected unweighted forest F=(V,E), including the
empty forest, isolated vertices and disconnected forests, let P_k count
independent k-subsets. P=I(F;x) has P_0=1 and coefficients through n=|V|,
with zeros outside. ORIGINAL asks for m with
P_0<=...<=P_m>=...>=P_n. Equivalently, no i<j has
Delta P_i<0<Delta P_j, where Delta Q_k=Q_(k+1)-Q_k.

A_v=I(F-v), B_v=x I(F-N[v]), P=A_v+B_v.
LOCAL means all these A_v/B_v are unimodal. HEREDITARY means every proper
induced subforest is unimodal. GLOBAL-MINIMAL means a counterexample of least
order among all forests. LEX-MINIMAL additionally minimizes the number of
edges at that order. Only
LEX-MINIMAL => GLOBAL-MINIMAL => HEREDITARY => LOCAL is used.
A hypothetical minimal counterexample is not assumed connected.

For a nonempty LOCAL forest let [ell_Av,r_Av], [ell_Bv,r_Bv] be full mode
intervals and define U=max_v min(r_Av,r_Bv), D=min_v max(ell_Av,ell_Bv).
Inherited proofs give nonnegative differences below U, nonpositive differences
at/after D, and unimodality if D<=U+1. A minimum counterexample has no isolated
vertex or K2 component and a valley U<=i<j<D. None of these inherited results
is counted as Phase-5 progress.

## Scoped results proved here
1. For A subset E, defect[A] counts vertex sets inducing EXACTLY A. With
   W=V(A), it is zero when E(F[W])!=A and otherwise equals
   x^|W| I(F-N[W]). This includes A empty. Consequently
   I(F-S)=sum_{A subset S} defect[A]. All nonzero nonempty defects are shifts
   of proper induced-forest polynomials and are unimodal under HEREDITARY.
2. The mixed finite difference at two edge deletions e,f outside S equals
   sum_{A subset S} defect[A union {e,f}], coefficientwise nonnegative.
   For S empty it is defect[{e,f}], not Z_e Z_f.
3. At an actual vertex v, with actual rooted branches M_w=I(T_w),
   X_w=I(T_w-w) and outside factor R, the partial-cut selected polynomial is
   B_J=xR product_{w in J} M_w product_{w not in J} X_w
      =xI(F-({v} union (N(v)\J))). The whole cut is A_v+B_J.
   Every B_J is unimodal under HEREDITARY; whole nonempty cuts are unimodal
   under LEX-MINIMAL. These are different premises.
4. For two further incident releases a,b, write M_w=X_w+Y_w and
   T=xR product_{w in J}M_w product_{w outside J,a,b}X_w. Then the mixed
   B increment is T Y_a Y_b, and
   B_(J+a) B_(J+b)=B_J B_(J+a+b),
   P_(J+a) P_(J+b)+A_v T Y_a Y_b=P_J P_(J+a+b).
   These are full convolution identities, not inequalities between
   same-index coefficient products or their differences.
5. Four root/vertex occupancy polynomials per internal vertex give a lossless
   actual-boundary recurrence and exact completion formula. This is an
   unbounded semantic state, NOT a finite-state unimodality induction.

## Diagnoses, not original counterexamples
The old 23-vertex tree, at v=1 and J={0,15} subset K={0,2,15}, has
B_J<=B_K coefficientwise but unique modes 9 and 8. Both partial cuts are
proper intermediate cuts, and their whole sequences are unimodal.
This refutes an UNLOCALIZED mode-monotonicity shortcut only. U=D=8;
there is no residual pair. It does not refute a residual-restricted claim,
J_H, RSM, or ORIGINAL.

Two distinct rooted 9-vertex trees have the same (X,Y) but different internal
conditional-polynomial multisets. Six actual completions preserve their equal
whole P and retain different internal profiles. No difference in U,D was
found in those completions. Thus we do NOT claim to have refuted a theorem
that U,D alone are determined by root messages. We only establish the stated
loss of full internal information.

## Unresolved claims and classification
J_H remains the inherited claim: every nonempty, isolate-free and K2-free
HEREDITARY forest has D<=U+1. RSM retains Stage-2 quantifiers: every nonempty
isolate-free HEREDITARY forest and every residual pair has a leaf blocking
that pair by the original polarization/signed-minor criterion; there is no
added K2 premise. Both remain UNRESOLVED.

The direct route still needs a proof that the actual residual slopes cannot
coexist with all vertex, edge-set and boundary constraints. In particular,
constructing a nonempty S with Delta Q_S(i)<s and Delta Q_S(j)>-t from a true
valley Delta P_i=-s<0<Delta P_j=t remains UNPROVED. No nonempty part of the old
actual-forest domain has been excluded. The final classification is E:
NOT_CLOSED / NO_STRUCTURAL_ADVANCE, not GAP_REDUCED or primary-route refutation.

## Execution boundaries
Final discovery: 146 proposals, 142 distinct labeled edge lists, 122 accepted
nonisomorphic forests (6 initial controls + 116 others within this run),
9 distinct expanded seeds and 140 distinct seed/position/operations.
There are 4 repeated edge-list proposals and 20 additional isomorphic edge
lists. Three rounds add 47,34,35 accepted forests. No global novelty claim.
All 122 whole polynomials were independently recounted; all are LOCAL and
unimodal, maximum order 53, maximum D-U=1. Residual graphs, residual pairs and
eligible nonvacuous RSM tests are all ZERO. Discovery HEREDITARY is UNKNOWN.

The 13 fixed interaction materials cover 1,337 edge pairs, 1,341 partial-cut
states and 4,425 square identities. Eight small controls have fresh full
proper-induced-subset verification (695 subsets); five larger controls remain
UNKNOWN in this run. Earlier old23 hereditary evidence is retained, not
rescinded or represented as freshly replayed. Large raw arrays accompany the
archive and are regenerated by native sources; hosted coverage is explicit
in README. Review is SAME_MODEL_SELF_REVIEW, not external peer review.

ORIGINAL formal: NOT_ESTABLISHED; no top-level source, build or axiom audit.
FAMILY is inherited unchanged, with no fresh full replay or formal build.
