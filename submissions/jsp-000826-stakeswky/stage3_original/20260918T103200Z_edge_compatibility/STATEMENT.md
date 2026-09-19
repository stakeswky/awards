# Phase 3: exact statements and status

**ORIGINAL: NOT_CLOSED. Structural progress: NO_STRUCTURAL_ADVANCE.**
The new edge restrictions below are necessary conditions, not a proof that a
counterexample is impossible. There is no legal ORIGINAL counterexample.

## 1. Original statement and conventions
For every finite undirected simple unweighted forest F=(V,E), let a_k count
independent subsets of V of cardinality k. Set P=I(F;x)=sum(a_k x^k), including
a_0=1 and all coefficients through |V|; pad outside that range with zero.
The assertion is that there is an m with a_0<=...<=a_m>=...>=a_|V|.
Empty forests, disconnected forests, isolated vertices and peak plateaus are
allowed. A refutation requires one such F and 0<=i<j<|V| with
Delta P_i<0<Delta P_j, where Delta P_k=P_(k+1)-P_k.

LOCAL means all F-v and F-N[v] are unimodal. HEREDITARY means all proper induced
F[S], S strictly contained in V, are unimodal. GLOBAL-MINIMAL means F is
nonunimodal and every forest of smaller order is unimodal. Only
GLOBAL-MINIMAL => HEREDITARY => LOCAL is used. The computations do not prove
global minimality, and no graph examined here is nonunimodal.

For every vertex v set A_v=I(F-v), B_v=x I(F-N[v]). Under LOCAL their full mode
intervals are [ell_A,r_A], [ell_B,r_B]. Set

    U=max_v min(r_Av,r_Bv), D=min_v max(ell_Av,ell_Bv).

These extrema are used only for nonempty forests satisfying LOCAL. The
inherited sign bounds are Delta P_k>=0 for k<U and Delta P_k<=0 for k>=D;
D<=U+1 implies unimodality. A hypothetical globally least counterexample has
no isolated vertex or K2 component, and its valley must satisfy U<=i<j<D.
None of those inherited reductions is counted as Phase-3 progress.

## 2. Candidate sufficient claims: both UNRESOLVED
**J_H.** Every nonempty unweighted simple forest with no isolated vertices or
K2 components and satisfying HEREDITARY has D<=U+1. This is the primary first
unproved bridge, not a proved theorem or an experimentally verified universal
claim. Its implication to ORIGINAL uses the inherited minimality reductions.

**RSM (unchanged Stage-2 quantifiers).** For every nonempty forest with no
isolated vertices and satisfying HEREDITARY, and for every U<=i<j<D, there is a
leaf l with support w such that, putting C=I(F-{l,w}), H=I(F-N[w]),
X=(1+x)C and Y=xH, either neither ordering (E,L) of (X,Y) satisfies

    Delta E_i<0, Delta E_j<=0, Delta L_i>=0, Delta L_j>0,

or the polarized ordering satisfies

    Q=Delta L_i*(-Delta E_j)-Delta L_j*(-Delta E_i)>=0.

There is no added K2 exclusion in RSM. The leaf may depend on i,j. To refute
RSM every leaf must fail at the same residual pair, with all premises proved.
No such graph or pair was obtained. A single bad leaf, an off-residual Q<0,
or failure of J_H would not be an ORIGINAL refutation.

## 3. Scoped propositions established in this run
E1: Actual-edge and cut-edge identities, with the common disconnected factor
retained, and coefficientwise endpoint-removal injections.
E2: Under LOCAL and D>=U+2, every vertex split has one entire mode interval
ending at or before U and the other beginning at or after D. Selected leaf
and support roles are opposite. This necessary band restriction is not a
contradiction on a tree.
E3: Under HEREDITARY and an actual valley, the same-role and mixed-role edge
slope restrictions of PROOF_ATTEMPT section 3 hold. No incompatibility of all
these restrictions on a forest is proved.
H1: The rooted-signature recurrence in HEREDITARY_COVERAGE.md covers all induced
subsets exactly, with multiplicities. It is a finite verification method, not
a proof that all forests or all hereditary candidates have the joint bound.
H2: The specific 23-vertex tree in certificates/bad_leaf_hereditary.json is
HEREDITARY and has a leaf whose conditional mode intervals have distance 2.
Thus the stronger assertion 'every leaf is good under HEREDITARY, even with
no isolated or K2 component' is REFUTED. The graph is unimodal, vertex 0 is
good, and U=D=8. Neither J_H nor existential good-vertex existence is refuted.

## 4. Evidence and dependency boundaries
The 60-record diagnostic batch contains four inherited controls and 56 new
records, not a claim of 56 globally new isomorphism types. All 60 satisfy LOCAL;
seven have complete HEREDITARY verification and 53 remain UNKNOWN for that
premise. All have D-U<=1. Residual graphs, residual pairs and eligible
nonvacuous RSM tests are all **0**. The additional five tiny regression graphs
are not included in that batch count.

ORIGINAL_FORMAL is NOT_ESTABLISHED: no complete target source, build or axiom
audit. The environment is NOT_PROBED this run, since no full mathematical
candidate exists. FAMILY is inherited unchanged from
36467feaa5bd486979077b97ad2bac5a75805986: PROVED_COMPUTER_ASSISTED mathematically,
NOT_ESTABLISHED formally, with no fresh full FAMILY replay in this run.
The observed recovery HEAD was 5169aa045816af5a87f5cf17341592ecb3ec8139.
