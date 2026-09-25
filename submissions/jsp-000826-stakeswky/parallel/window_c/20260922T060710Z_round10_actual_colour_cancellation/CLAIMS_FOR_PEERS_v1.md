# C10 v1: actual two-colour root compatibility

Run: 20260922T060710Z_round10_actual_colour_cancellation.
ORIGINAL=NOT_CLOSED. No new unrestricted colour-mass entrance is claimed.
The C9 deletion identity and its nonzero p_(j-1)*p_j baseline are retained.
C4/C5, both C6 batches, and C8/C9 maintain their original scopes.

## Shared actual definitions

F is a finite simple undirected unweighted forest with a fixed proper vertex
bipartition L,R. Let f_r(x)=sum_{I independent, |I|=r} x^{|I intersect L|},
with zero padding. Define g=f_j^2-f_(j-1)f_(j+1), D=sum_t max(-[x^t]g,0),
and S=p_j*(p_(j-1)-p_j). An intersection vertex is counted twice in a pair's
colour mass. Under current nonincrease S>=0; no division by S is performed.
The middle is h+1<=j<beta, h=floor(M_max(n-1)/(4M_max-2))+1,
beta=ceil(alpha(n-1)/(n+alpha)); History(F,j-1) retains an actual earlier
strict drop. HEREDITARY means all proper induced forests are whole-unimodal.

At an ORIGINAL root v, put A=Z_(F-v) and C=z_v Z_(F-N[v]), with the root's
weight restored in C. Both polynomials retain every other actual component
and all inherited colours. On rank rows, set
 g00=A_j^2-A_(j-1)A_(j+1),
 g11=C_j^2-C_(j-1)C_(j+1),
 g01=2 A_j C_j-A_(j-1)C_(j+1)-C_(j-1)A_(j+1).
Thus g=g00+g11+g01. These are not independent coefficient inputs.
Define U_v=sum_t ([-g00_t]_+ +[-g11_t]_+ +[-g01_t]_+).
The triangle bound D<=U_v is valid, but U_v<=S is a STRONGER gate.

## C10-ROOT-PREMERGE-v1: an EVERY-root surrogate is refuted

The actual 25-vertex tree below, at j=10 and original root v=9, satisfies
HEREDITARY, connectedness, the project middle and a first strict drop at k=9.
Indeed every induced forest is LC, by the finite complete connected-induced
subtree classification supplied with the final package. No <=30 external
census completeness is used. The tree has alpha=19, h=7, beta=11.

Edges (zero based):
 (1,0),(2,1),(3,1),(5,1),(6,0),(7,6),(8,3),(0,10),(2,11),(3,12),
 (5,13),(5,14),(5,15),(5,16),(5,17),(9,18),(9,19),(9,20),(9,21),
 (9,22),(9,23),(9,24),(4,2),(19,5).

Its full coefficients are
 1,25,276,1807,7966,25460,61894,118051,180007,221739,221652,
 179772,117831,61925,25763,8316,2016,347,38,2.
Choose v=9 in L, so |L|=6 and |R|=19. Exact quantities:
 S=19283724; D=3158;
 ||g00_-||=1210, ||g11_-||=0, ||g01_-||=22792700;
 U_9=22793910>S by3510186.
The full g has just one negative colour sector, t=9 with value-3158.
Its next scalar drop is41880. Merging the actual state blocks recovers
22790752 units of same-colour cancellation. The independent graph deletion
algorithm agrees with the rooted bivariate count; a complete H certificate
has2854 rooted connected-induced types, all LC.

This refutes the asserted EVERY-v U_v<=S even under H and history. It does
NOT refute the raw D<=S gate, an EXISTS-root gate, or ORIGINAL. All25 root
choices were checked: only v9 fails this surrogate. It is not a minimum-bad
forest and is not claimed to lack a proper LC subunion (it is connected).
Refutation of this stated counterexample requires a wrong edge/count/sign,
a missing connected-induced type, or a failure in the hereditary argument.

## C10-TRUE-MASS-v1: unchanged main entrance, UNPROVED

For EVERY actual forest satisfying HEREDITARY and EVERY project-middle
History position, does SOME proper complete-component bipartition satisfy
D<=S? For a connected tree the two choices are global complements and give
identical D. A proposed failure needs all component flips, full original
edges and count arrays, and the exact H status. A good graph with H unknown
cannot refute the H version. A failed U_v never refutes this weaker question.

For a fixed colouring, the exact same-sector cancellation is
 C_v=sum_t min(sum_{s in{00,11,01}}[g_s,t]_+,
               sum_{s in{00,11,01}}[-g_s,t]_+).
Then D=U_v-C_v independently of the chosen root. This is accounting, not a
new structural lower bound on C_v. The missing estimate C_v>=U_v-S is not
claimed merely by restating it. The actual25 counterexample requires keeping
pure-state and mixed-state contributions together before charging the deficit.

Full proof, source and final execution receipts will be added to this run's
own directory. This interface does not assert a peer receipt, formal build,
external review or novelty. E9-012308Z colour-mass relay is retained as a
proved conditional mechanism, not assumed to make its entrance automatic.
