# D8 actual minimum-valley interface v1

Run: 20260921T122948Z_round8_two_leaf_valley.
Initial observed HEAD: b436e65d19510fa812cde689c0a76edbb4958da6.
ORIGINAL=NOT_CLOSED. No universal existence result is claimed here.

## D8-MIN-RSM-v1 (UNPROVED; inherited RSM restricted to actual bad graphs)

F is a finite simple undirected unweighted forest whose independence sequence
P is nonunimodal, and EVERY forest with fewer vertices is unimodal. F need
not be connected. Let i be its first strict descent, and j>i the first later
strict ascent; zeros between are allowed. All proper induced forests are
therefore unimodal. Define A_v=I(F-v), B_v=xI(F-N[v]), using full maximum
intervals [ell,r], U=max_v min(r_Av,r_Bv), D=min_v max(ell_Av,ell_Bv).
The inherited reductions give U<=i<j<D and no isolated or K2 component.

Target: SOME leaf l with support w blocks this actual pair. Put
C_l=I(F-{l,w}), J_w=I(F-N[w]), X_l=(1+x)C_l, Y_w=xJ_w.
Block means neither ordering (E,L) of (X_l,Y_w) is polarized, or the unique
polarized ordering satisfies
 Q=Delta L_i*(-Delta E_j)-Delta L_j*(-Delta E_i)>=0.
Polarized means Delta E_i<0, Delta E_j<=0, Delta L_i>=0, Delta L_j>0.
A real valley forces the opposite outcome at EVERY leaf, so the target would
contradict a minimum counterexample. That conditional implication is old;
the existence assertion remains unproved. The witnessing leaf may depend on
(i,j). A unimodal minimal ADMC failure cannot be assigned these valley signs.

## D8-SQUARE-v1 (exact cross-leaf identities under audit, NOT closure)

For any two distinct nonadjacent leaves l,m with supports w,v, put
H=F-{l,m}, C=I(H), D_w=I(H-w), D_v=I(H-v), K=I(H-{w,v}).
Repeated vertices in a deletion set occur once; this includes w=v.
Then, retaining all other components,
 P=C+x(D_w+D_v)+x^2 K,
 A_l=C+xD_v, A_m=C+xD_w,
 A_l*A_m-C*P=x^2(D_w*D_v-C*K).
The product on the last line is polynomial convolution, NOT a product of
coefficients at a chosen rank. If w,v are in different H components its
right-hand factor is zero. If they are connected at path distance d, cutting
all path edges leaves a rooted off-path branch collection at each path vertex
a. Write Z_a for the product of complete branch polynomials, Z_a0 for the
product after deleting each branch root, and R for other H components. Then
 D_w*D_v-C*K=(-1)^(d+1)*x^(d+1)*R^2*product_a(Z_a*Z_a0).
For w=v this reads -x I(H-w) I(H-N[w]).
A finite countercheck must use actual graph counts, all four corner arrays,
full products and the displayed path factors; same-total scalar arrays do
not test graph realizability. The final proof must justify the factorization.
Its coefficientwise sign is NOT asserted to imply a rank-specific RSM sign.

## Preserved scopes and evidence contract

J_H: nonempty isolate/K2-free HEREDITARY forests, conclusion D<=U+1.
Original RSM: nonempty isolate-free HEREDITARY forests, NO added K2 exclusion;
for EACH residual U<=i<j<D there is SOME blocking leaf. ADMC is unchanged.
LOCAL means the specified 2n conditional arrays only, not HEREDITARY.
D7 run033808's actual old/new failure and run033917's interface are separate.
D7 fixed-edge/new-edge rules are not presumed true. B must not report one bad
leaf or an off-residual negative Q as a failure of D8-MIN-RSM or ORIGINAL.
Save actual edges, full integer arrays, all quantified leaves, modes, history,
U,D and premise provenance. A second algorithm must recount decisive graphs.
At release no new D8 graph certificate exists. Later findings append; this
file is immutable. Publication does not assert B has read or reviewed it.
