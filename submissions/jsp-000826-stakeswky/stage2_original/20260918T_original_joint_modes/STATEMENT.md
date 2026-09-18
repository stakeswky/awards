# ORIGINAL: exact statements and the unproved structural bridge

**Result of this run: NOT_CLOSED.** The reductions below are proved in
PROOF_ATTEMPT.md. Neither ORIGINAL nor the residual structural bridge is proved
or refuted here. The diagnostic graphs contain no ORIGINAL counterexample.
Review is SAME_MODEL_SELF_REVIEW, not independent peer review.

## 1. Graph semantics and ORIGINAL

A graph is a finite set V and a set E of unordered two-element subsets of V.
It is unweighted, undirected and simple. A forest has no cycle. Empty graphs,
isolated vertices and disconnected forests are included. For every integer k,

    a_k(F) = #{S subset V : |S|=k and no edge of F lies in S},
    I(F;x) = sum_{k=0}^{|V|} a_k(F) x^k.

Set a_k=0 outside 0..|V|; a_0=1. A nonnegative finite sequence is unimodal when
some index m has weak increase through m and weak decrease afterwards. Plateaus
are allowed. ORIGINAL asserts this for every forest F. A counterexample must
supply an actual such graph and indices 0<=i<j<|V| with

    a_i>a_(i+1) and a_j<a_(j+1).

A log-concavity failure, weighted example, abstract sequence, bad root or failed
sufficient condition is not a counterexample under this definition.

## 2. Premises that must not be confused

LOCAL(F): each of the 2|V| specified polynomials I(F-v), I(F-N[v]) is unimodal.
Here N[v] contains v and all its neighbors.

HEREDITARY(F): I(F[S]) is unimodal for EVERY proper subset S of V.

GLOBAL-MINIMAL(F): F violates ORIGINAL and every forest with fewer vertices is
unimodal. This is a hypothetical premise, not a property established for any
of the diagnostic inputs. GLOBAL-MINIMAL implies HEREDITARY, which implies
LOCAL. The converses are not used. Checking 2|V| deletions proves only LOCAL.

If ORIGINAL is false, the well-ordering of the vertex count gives a
GLOBAL-MINIMAL forest. This forest is nonempty, has no isolated vertex and no
component isomorphic to a single edge. Connectedness is NOT concluded.

## 3. All-vertex decomposition and joint bounds

For v in V use ACTUAL graph counts

    A_v=I(F-v;x), B_v=x I(F-N[v];x), P=I(F;x)=A_v+B_v.

For a nonzero unimodal sequence C, let M(C)=[ell_C,r_C] be its full interval
of maximum positions. Padding by zeros cannot change these positive maxima.
Under LOCAL(F), for nonempty F, define

    u_v=min(r_Av,r_Bv), d_v=max(ell_Av,ell_Bv),
    U=max_v u_v, D=min_v d_v.

The proved finite-sequence statement is

    Delta P_k >= 0 for k<U;  Delta P_k <= 0 for k>=D,
    where Delta P_k=P_(k+1)-P_k, 0<=k<|V|.

D<=U+1 is sufficient for unimodality, including D<=U and D=U+1 separately.
A vertex with dist(M(A_v),M(B_v))<=1 implies this joint condition. The vertices
attaining U and D need not be the same.

The unproved universal auxiliary assertions are:
L: every nonempty forest with LOCAL has such a good vertex;
J: every nonempty forest with LOCAL satisfies D<=U+1.
Both remain UNRESOLVED here. Their versions restricted to HEREDITARY also
remain UNRESOLVED. A minimum counterexample must have D>=U+2 and any strict
descent-followed-by-ascent pair must lie at U<=i<j<D.

## 4. The quantitative structural bridge RSM (UNRESOLVED)

This is one precise sufficient continuation of the same main route, NOT an
assumption of the proved reductions and NOT a claim that it must be true.

Let F be a nonempty forest with no isolated vertices satisfying HEREDITARY(F).
Compute U,D above. For every pair of integers U<=i<j<D, require a leaf ell with
neighbor w for which the following test succeeds. Put

    C=I(F-{ell,w};x), H=I(F-N[w];x),
    X=(1+x)C=A_w, Y=xH=B_w.

Say that an ordering (E,L) of (X,Y) is polarized at i,j when

    Delta E_i<0, Delta E_j<=0,
    Delta L_i>=0, Delta L_j>0.

The successful test is: either neither ordering is polarized, OR, for a
polarized ordering, the following integer expression is nonnegative:

    Q(E,L;i,j) = Delta L_i*(-Delta E_j)
                 - Delta L_j*(-Delta E_i) >= 0.        (RSM)

There is at most one polarized ordering. This statement quantifies over
actual forests and uses no assumption about the signs of Delta P_i,Delta P_j.
Its graph structure is substantive: if T_1,...,T_s are the branches beyond w
other than ell, rooted at the neighbors of w, and R is the polynomial of the
other components, then

    C=R product_t I(T_t), H=R product_t I(T_t-root_t).

Neither the common factor R nor the relation between these actual rooted
branches may be dropped. For example, when E=Y and L=X, the expression is

    (C_(j+1)-C_(j-1))*(H_i-H_(i-1))
      - (C_(i+1)-C_(i-1))*(H_j-H_(j-1)).

RSM asks for a leaf-support split blocking each residual pair, not for all
minors at all indices to be nonnegative. Its unlocalized strengthening is
false even for a seven-vertex star (material.json).

A real valley in a minimum counterexample forces EVERY vertex split, hence
EVERY leaf-support split, to be polarized with Q<0. Thus a proof of RSM would
contradict that valley and complete ORIGINAL. This final implication IS proved.
The missing part is RSM's existence/nonnegativity assertion for actual branch
products in the residual interval. No coverage or induction establishing it is
available. All checked graphs have D<=U+1, so the current graph data give NO
nonvacuous test of RSM when there are two residual indices.

RSM demands an additional quantitative certificate; it is not asserted to be
necessary or equivalent to ORIGINAL. Negative Q does not by itself imply a valley. A unimodal abstract sum with Q<0 is explicitly retained. Failure
of RSM would therefore not by itself refute ORIGINAL; J or a weaker coefficient
argument might still hold. These distinctions prevent a reformulation of the
desired conclusion from being called a proved structural lemma.

## 5. Exact status of the other auxiliary statements

PROVED: decomposition from independent subsets; mode-interval sign bounds;
joint criterion; no isolated/single-edge component in a minimum counterexample;
actual rooted messages and retained common factors; double-count identities;
unique early/late split roles; opposite selected roles at leaf and support;
negative signed minor forced by a valley; RSM would imply ORIGINAL.

REFUTED: under LOCAL, EVERY leaf is a good vertex (tree-11 at leaf 4).
REFUTED: every polarized leaf-support minor at arbitrary indices is nonnegative
(star7; all its proper induced forests were checked).
REFUTED AS AN ABSTRACT SEQUENCE CLAIM: the listed leaf-shape conditions and
H<=C suffice for leaf insertion to preserve unimodality. The witness cannot
be a forest because its first two nonconstant counts would require too many
edges. It is not a refutation of a real-forest theorem.

The historical 25-to-30 control still refutes the relevant over-broad LC
insertion, not unimodality or ORIGINAL. No stronger graph-level assertion is
refuted by presenting only these restricted witnesses.

## 6. Inherited FAMILY and formal boundaries

Inherited baseline: stakeswky/awards at
36467feaa5bd486979077b97ad2bac5a75805986, closure_v5/VERDICT.json.
FAMILY is the exact B59 repeated-mixture E/P theorem for every integer t>=1;
its recorded mathematical status is PROVED_COMPUTER_ASSISTED, its formal status
NOT_ESTABLISHED. This run does not extend B59 or reverify that entire proof.
No FAMILY statement is a dependency of the reductions above.

ORIGINAL_FORMAL is NOT_ESTABLISHED: no top-level Lean source/build/axiom audit.
The fresh executable probe failed with command-not-found, exit 127. Installing
Lean alone would not fill the mathematical RSM gap. No local formal result,
old receipt or repository CI is substituted for ORIGINAL.
