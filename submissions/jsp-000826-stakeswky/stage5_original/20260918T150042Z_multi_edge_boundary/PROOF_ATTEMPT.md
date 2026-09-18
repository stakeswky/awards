# Multi-edge and actual-boundary attempt

**NOT_CLOSED / NO_STRUCTURAL_ADVANCE.** This is not a proof of ORIGINAL.
The chain below reaches an explicitly unproved last implication. Equations
are derived from actual sets; no arbitrary arrays replace forest messages.

## 1. Original target, minimality and residual location
Use STATEMENT.md's precise definitions. A finite sequence is unimodal iff it
has no strict negative difference followed later by a strict positive one:
one implication follows from monotonicity on each side of a peak; conversely,
once the first negative difference occurs, absence of a later positive one
makes the remaining sequence nonincreasing. Zeros between signs cause no
exception. Thus the definition includes peak plateaus and separated valleys.

If ORIGINAL is false, choose a counterexample with lexicographically least
(n,m)=(|V|,|E|). Every forest of smaller order is unimodal; every forest of this
order and fewer edges is unimodal. In particular, proper induced subforests
and every F-S with nonempty S subset E are unimodal. HEREDITARY alone would
not justify the second assertion.

For every v, partitioning independent sets according to membership of v gives
P=A_v+B_v. Under minimality both summands are unimodal. If k<min(r_A,r_B),
both differences are nonnegative, because each sequence is nondecreasing up
to its rightmost mode. If k>=max(ell_A,ell_B), both are nonpositive. Taking
maxima/minima over the finitely many vertices gives the U,D sign bounds.
For D<=U, all differences between the bounds are zero. For D=U+1, at most
one difference lies between the initial nonnegative and final nonpositive
ranges. Either sign at that one position is compatible with unimodality.
A valley must therefore have U<=i<j<D and D>=U+2.

The empty forest has P=1. A linear kernel 1+c x, c>0, preserves unimodality:
if q has a peak at m, Delta((1+cx)q)_k=Delta q_k+c Delta q_(k-1) is
nonnegative for k<m and nonpositive for k>m; only k=m is undecided. Treat
q_-1=0, so the initial difference has the same sign convention. This also
handles leading/trailing zeros. An isolated or K2 component has polynomial
1+x or 1+2x. Removing such a component leaves a smaller forest, so it cannot
occur in a minimum counterexample. Nothing here makes F connected.

Fix a hypothetical actual valley Delta P_i=-s<0, Delta P_j=t>0. Hence s,t
are positive integers and U<=i<j<D. This hypothetical valley is never
substituted by an off-residual or purely scalar example in the proof.

## 2. Exact defect sets: all shared cut coefficients
For A subset E let W be its endpoint set. Suppose T induces exactly A. Every
endpoint of A belongs to T, so W subset T. Consequently E(F[W])=A is
necessary. If W already induces an extra edge, no such T exists.

Assume E(F[W])=A. Write T=W disjoint union Z. There can be no edge from Z to
W, nor an edge within Z, since either would enlarge the induced edge set.
Thus Z is an independent subset of F-N[W]. Conversely, every such Z gives a
set T inducing exactly A. These operations are inverse and |T|=|W|+|Z|.
They prove

    defect[A] = 0                                  if E(F[W]) != A,
    defect[A] = x^|W| I(F-N[W])                    otherwise.       (2.1)

For A empty, W and N[W] are empty and this is P. The formula is valid for any
finite simple graph; our applications are forests. For nonempty A, the
remaining induced forest has fewer vertices. Under HEREDITARY every nonzero
defect is therefore unimodal after its displayed shift. The zero polynomial
is also unimodal, but no mode interval for it is used.

A set T is independent in F-S exactly when its original induced edge set is
contained in S. Its unique induced edge set partitions all these sets, giving

    P_S := I(F-S) = sum_{A subset S} defect[A],
    Q_S := P_S-P = sum_{empty != A subset S} defect[A].             (2.2)

For a single edge e=uv, (2.1) is the inherited Z_e=x^2 I(F-(N[u] union N[v])).
For two adjacent edges, the endpoint count is three, so the shift is x^3.
For the path 0-1-2-3, A={01,23} has all four endpoints, which also induce 12;
its defect is zero. Even in a forest disjoint edges need not form an induced
matching. On the path of length two, defect[{01,12}]=x^3 whereas Z_01 Z_12=x^4.
This is an explicit reason not to multiply the single-edge corrections.
The entire factor from other connected components remains in F-N[W].

Let e,f be distinct edges outside S. Taking the mixed finite difference of
(2.2), each defect term survives exactly when it contains e and f and all
its other edges are in S. Thus

    P_(S+e+f)-P_(S+e)-P_(S+f)+P_S
      = sum_{A subset S} defect[A union {e,f}] >=_coeff 0.         (2.3)

The coefficientwise inequality is exact, but subtraction of adjacent
coefficients does NOT preserve it. In general this mixed polynomial is a sum
of shifted induced-forest polynomials, not a product of individual Z terms.

## 3. What all nonempty cuts require, and the unsuccessful connection
By lexicographic minimality, P_S is unimodal for every nonempty S. At the
fixed actual valley it follows that

    Delta Q_S(i) >= s  OR  Delta Q_S(j) <= -t.                    (3.1)

Indeed failure of both inequalities would leave Delta P_S(i)<0<Delta P_S(j).
Equality in either alternative is permitted. The quantifier is per S, not
one uniform choice of alternative for all cuts.

We attempted to use (2.3) to carry a common rescue direction across the cut
lattice. The uncontrolled terms are precisely the TWO differences of the
mixed increment. Its nonnegative coefficients do not bound either difference.
Even unimodality of an individual defect only forbids its own negative-then-
positive sign pattern; it does not fix its mode relative to i,j or compare
its slope magnitude to s,t. Thus sums of the constraints do not yield a
common branch of (3.1). No such common choice is used in the subsequent work.

A sufficient endpoint would be a construction, from the actual forest and
valley, of a nonempty S with

    Delta Q_S(i)<s and Delta Q_S(j)>-t.                           (3.2)

That would contradict (3.1) and close ORIGINAL. We have not proved (3.2).
Restating it is not a smaller gap. The next sections retain more shared
structure rather than treating its terms as independent slope variables.

## 4. Partial cuts at one actual vertex
Fix v and let T_w be the component of F-v containing neighbor w. No such
component contains two neighbors: together with v that would make a cycle.
Let R count all the other original components. Set M_w=I(T_w),
X_w=I(T_w-w), Y_w=M_w-X_w=xI(T_w-N_Tw[w]). These are actual root-absent and
root-present classes, with the x already included in Y_w.

If v is absent, all branches are free, so A=R product M_w. After cutting the
edges vw for w in J, selecting v forbids the roots of precisely the uncut
branches. Independent choices on disjoint branches give

    B_J=xR product_{w in J}M_w product_{w outside J}X_w,
    P_J=A+B_J.                                                   (4.1)

Equivalently, remove v and its uncut neighbors from the original F, choose
an independent set of what remains, and then adjoin v in the cut graph. This
bijection proves

    B_J=xI(F-({v} union (N(v)\J))).                              (4.2)

Equation (4.2) makes every B_J a shifted proper induced-forest polynomial,
so its unimodality follows from HEREDITARY. Unimodality of P_J for nonempty
J instead follows from LEX-MINIMAL. The two justifications are not exchanged.
At J empty, B_J=B_v. At J=N(v), B_J=xA and P_J=(1+x)A. The latter whole-cut
unimodality was already implied by smaller-order minimality and the linear
kernel argument. If J consists only of original leaves, then F-J has fewer
vertices and the cut polynomial is (1+x)^|J| I(F-J); this is also redundant.
For degree <=2, a cut involving at least two edges is the full-star case,
not a genuinely new intermediate state. Our material controls include
internal branches and proper intermediate states at degree >=3.

For further neighbors a,b outside J, put

    T=xR product_{w in J}M_w product_{w outside J,a,b}X_w.

Then the four selected-state polynomials are respectively

    T X_a X_b,   T M_a X_b,   T X_a M_b,   T M_a M_b.

Their mixed increment is T Y_a Y_b. Their opposite products agree. Adding
the common A to each gives the full polynomial identity

    P_(J+a) P_(J+b) + A T Y_a Y_b = P_J P_(J+a+b).                (4.3)

The same branch-exponent accounting proves
B_J B_K=B_(J intersection K) B_(J union K) for arbitrary J,K. All products
are full convolutions; none is replaced by same-index multiplication.
For a nonempty released set K disjoint from J, the higher mixed B increment
is xR product_J M_w product_K Y_w product_else X_w. Selecting all roots in
K and deleting their branch neighborhoods leaves an actual proper induced
forest, so this increment is itself a shifted induced-forest polynomial.
That strengthens the semantics but still does not locate its mode.

## 5. A proposed monotone-mode propagation fails on an actual graph
A tempting next step was to order the modes of B_J along J subset K. Even
all their coefficients increasing would not prove that order. Here it is
actually false, including for two proper intermediate states.

Use the historical 23-vertex tree with edges

    01, 0-17, 0-22, 12, 13, 1-15, 1-16,
    24, 25, 26, 2-10, 2-14, 2-18,
    38, 39, 3-20, 3-21, 67, 8-13, 9-11, 9-12, 18-19.

Here labels such as 01 mean the edge {0,1}, not a number; the machine
certificate gives unambiguous endpoint pairs. At v=1 choose
J={0,15}, K={0,2,15}. Degree(v)=5, so both are proper intermediate sets.
The complete nonzero ranges of their selected polynomials are

    B_J = (0,1,19,164,852,2975,7383,13423,18153,18338,
           13758,7537,2919,754,116,8),
    B_K = (0,1,20,177,925,3208,7851,14041,18696,18651,
           13871,7560,2921,754,116,8).

Every B_K coefficient is at least the corresponding B_J coefficient.
Nevertheless B_J has its unique peak at 9 and B_K at 8; in particular
Delta B_J(8)=185 whereas Delta B_K(8)=-45. A, B_J, B_K, P_J, P_K and the
original P are all unimodal, independently recounted as full integer arrays.
The original graph has U=D=8. The earlier complete HEREDITARY proof for this
graph remains historical evidence; this run does not relabel its new
finite checks as a fresh replay of all 8,388,607 proper subsets.

This rejects the unlocalized monotone-mode step, not the residual problem.
It does not test a version restricted to D>=U+2 or to actual counterexamples.
Consequently it neither proves J_H nor refutes J_H, RSM or ORIGINAL. We did
not try to rescue the argument by assuming its desired monotonicity on the
unobserved residual domain. No tree potential with a proved forbidden sink
was obtained from (4.3).

## 6. Lossless rooted profiles with actual external completion
The next attempt retains internal information explicitly. In a rooted tree
(T,r), for every vertex v and a,b in {0,1}, define C_v^(ab) to count independent
sets of T with membership of r equal to a and membership of v equal to b.
The power of x is the TOTAL set size, including all selected marked vertices.
Write its four entries in order 00,01,10,11. For v=r these are X,0,0,Y.
For every v, row sums are X=C00+C01 and Y=C10+C11. Column sums are the
ordinary conditional polynomials at v in T.

For a leaf rooted tree X=1,Y=x and its sole profile is (1,0,0,x). For an
arbitrary root with child trees h,

    X=product_h (X_h+Y_h),   Y=x product_h X_h.

For a vertex v in child j let q00,q01,q10,q11 be its child profile. Define
O_M=product_(h!=j)(X_h+Y_h), O_X=product_(h!=j)X_h. Partitioning on the new
root and the child root gives exactly

    C00=(q00+q10)O_M,   C01=(q01+q11)O_M,
    C10=x q00 O_X,      C11=x q01 O_X.                            (6.1)

This proves the profile recurrence by structural induction, retaining one
profile for EVERY internal vertex. No graph is dropped because it happens
to have the same X,Y as another graph.

Attach r by an edge to the root of an actual external tree with messages
X_e,Y_e, and retain an arbitrary actual disconnected factor R. Put
L=R(X_e+Y_e), M=R X_e. A set with r absent allows either exterior root state;
a set with r present forces the exterior root absent. Therefore

    P=L X+M Y,
    A_v=L C00+M C10,   B_v=L C01+M C11.                           (6.2)

The no-exterior case is L=M=1. Products with R are kept in full. Equations
(6.1)-(6.2) prove a lossless counting state, not a finite collection of mode
inequalities invariant under grafting. Its dimension and polynomial degrees
grow with T; no finite compression or all-parameter UNSAT result is claimed.

### Concrete information loss in a two-message-only state
The following two rooted trees (root 0) both have

    X=(1,8,23,30,18,4),   Y=(0,1,5,7,3),
    P=(1,9,28,37,21,4).

Their edge sets are

    T1: (0,1),(0,2),(0,3),(3,4),(3,5),(5,6),(6,7),(7,8),
    T2: (0,1),(0,2),(0,4),(2,3),(4,5),(5,6),(5,7),(7,8).

They are not isomorphic as unrooted trees. Their multisets of internal
(A_v,B_v) differ; for example T1 has A_3=(1,8,23,29,16,3), which no vertex
of T2 has. The complete lists and joint profiles are in the certificate.
The same X,Y guarantee the same P under EVERY same actual external completion
by (6.2), not merely the six tested completions. But these equal messages do
not determine the internal profiles. Six fixed actual completions, including
an outside edge factor and a 30-vertex external tree, were independently
recounted. All 108 internal profile completions matched full A/B arrays.
All tested U,D pairs still agree; no contrary U/D theorem is asserted.

The remaining induction step would have to constrain all these genuine
profiles, plus the lexicographic cut hypotheses, so that the two strict
valley signs cannot coexist after completion. Neither the exact recurrence
nor the equal-message witness supplies such an invariant. This route stops
at that missing inequality, not at a proved universal theorem.

## 7. Directed actual-forest checks and what they do not establish
The fixed discovery plan targets bottleneck vertices, moves internal rooted
branches across a support, performs proper two-edge cuts, and includes
explicit disconnected combinations. It does not simply increase the old
random or graft sample limit. The primary score is D-U; the secondary score
is the exact nu in DIAGNOSTIC_PLAN, with i<j<alpha and no padded-tail indices.
Nu>0 is equivalent to an actual valley; N/A is not a successful score.

Final counts are in STATEMENT and certificates/search_summary.json. Every
accepted P was recomputed by a different vertex-deletion algorithm. All
A/B/C/H/Z, pairs and partial cuts of the three selected discovery materials
were independently recounted as well. A true valley, LOCAL failure or
D>=U+2 would stop ordinary expansion for complete diagnostics. None occurred.
The 122 accepted types are distinct WITHIN this run, not a global novelty
or an exhaustive order range. Earlier initial-source results are retained
separately, not added to final coverage.

Full-defect enumeration is confined to eight small interaction controls;
it is not an attempt to enumerate all cuts of all forests. Their direct
vertex-subset classifications independently verify the exact induced-edge
semantics. The larger materials test all pairs and all incident partial
cuts. These are semantic regressions, not nonvacuous tests of (3.1) or RSM.

## 8. Final chain and the unchanged first gap
If ORIGINAL fails, Section 1 produces a lexicographically minimal forest
and a true residual pair. Sections 2,4,6 describe its exact shared defect,
partial-cut and full internal-boundary data. Minimality imposes (3.1) for
every nonempty cut. **The missing step is to prove those actual data cannot
satisfy the valley and all these conditions simultaneously.** We have not
constructed a cut satisfying (3.2), nor proved another direct contradiction.

The old remaining domain was all such real minimum-counterexample residual
configurations. The newly excluded part of that ACTUAL domain is none: one
unlocalized shortcut failed, and new necessary identities were established,
but no nonempty subclass of the old residual domain was ruled out. The new
remaining domain is unchanged. J_H and the original-quantifier RSM remain
unproved alternative bridges. No full ORIGINAL proof, counterexample, formal
build, independent external review or global novelty claim is made.
