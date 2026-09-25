# D6-ADMC-v1: actual leaf-edge existence (UNPROVED)

This is the unchanged mathematical ADMC target of D4-J/D5-J, not a new theorem.
Run: 20260921T011340Z_round6_actual_leaf_edges. Initial observed HEAD:
e9d5986c1c3216465f4cc8608db2ddad08e31d9c. ORIGINAL remains NOT_CLOSED.

## Complete quantifiers
For EVERY nonempty finite simple undirected unweighted forest F with no
isolated vertex and no K2 connected component, assume HEREDITARY(F): the
independence polynomial of EVERY proper induced subforest is unimodal.
The empty subset and disconnected induced subforests are included.
Then there EXISTS a degree-one vertex l and its unique neighbor w such that

    dist(M(I(F-l)), M(I(F-w))) <= 1.

M(Q)=[ell_Q,r_Q] is the entire interval of maximum coefficients, with zero
padding; dist([a,b],[c,d])=max(0,c-b,a-d). There is no assumed History,
valley, graph-order bound, connectedness or log-concavity hypothesis.

For this SAME actual leaf edge, retain all other components and put
C=I(F-{l,w}), J=I(F-N[w]). The required four real counting polynomials are

    A_l=C+xJ, B_l=xC, A_w=(1+x)C, B_w=xJ.

## Proven implication, not existence
LOCAL means all A_v=I(F-v), B_v=xI(F-N[v]) are unimodal. Under LOCAL define
U=max_v min(r_Av,r_Bv), D=min_v max(ell_Av,ell_Bv). The inherited proof gives
D>=U+2 => every leaf-pair distance>=2. Thus ADMC => D<=U+1 => unimodality.
A least-order original counterexample satisfies the domain and HEREDITARY,
so a proof of this universal assertion would complete ORIGINAL. No converse
from all bad leaf pairs to D>=U+2 or an actual valley is assumed.

## Exact negative-certificate contract
Return an actual graph in the domain, ALL leaves (including a root of degree
one), their supports, complete A_l/A_w mode intervals and distance>=2 for
EVERY pair. Prove HEREDITARY separately; 2n conditional arrays prove only
LOCAL. Keep full P and all A_v/B_v arrays, U,D, and all whole-sequence valley
pairs. A single bad leaf, or one old good edge lost under an edit, is not a
refutation of this existential claim. A unimodal all-bad graph would refute
ADMC only. Check every decisive graph with a second exact counting algorithm.

## Unchanged alternatives and already received feedback
J_H retains the same nonempty isolate/K2-free HEREDITARY domain and D<=U+1.
RSM retains the nonempty isolate-free HEREDITARY domain with NO extra K2
exclusion. For EACH U<=i<j<D, SOME leaf/support split X=(1+x)C,Y=xJ must be
unpolarized, or its polarized ordering (E,L) must have
Q=Delta L_i*(-Delta E_j)-Delta L_j*(-Delta E_i)>=0. Polarized means
Delta E_i<0, Delta E_j<=0, Delta L_i>=0, Delta L_j>0. The leaf may depend on
the pair; negative Q alone is not a valley.
B5's full-leaf positive tests were read; this is not a first-ever D test.
A5 TO_D/EDGE_INTERFACE was read, including its far-from-middle positive sum;
it is not a proved mode theorem. Generic LC cofactor mode-adjacency is false
(D5 P12/S12/P4), and is not used here. Weighted transfer is not this run's goal.

## Provenance and publication
Source D5-J-v1_CLAIMS_FOR_PEERS.md is retained verbatim in inputs/; its hash
is in SOURCE_AUDIT.json. The early Library D5-J-v1.md has the same quantifiers
but different prose, and is recorded separately. Later findings are appended
under new result IDs, not silently substituted into this release.
Certificates: certificates/KEY_CERTIFICATE.json (not yet produced at release).
Publication is recorded only in the actual receipt; no B6 receipt is presumed.
