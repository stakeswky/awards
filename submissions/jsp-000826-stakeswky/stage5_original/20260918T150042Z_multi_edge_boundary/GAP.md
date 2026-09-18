# First unproved connection: unchanged

**NOT_CLOSED / NO_STRUCTURAL_ADVANCE.**

## Direct route and exact missing implication
Suppose F is a finite simple unweighted forest which is a counterexample
minimal first by vertex count, then by edge count. It satisfies HEREDITARY,
LOCAL, and unimodality of every F-S for nonempty S subset E. It has no isolated
or K2 component, and is not assumed connected. For an actual valley write
Delta P_i=-s<0<Delta P_j=t, U<=i<j<D.

The proved defect formulas yield Q_S=sum_{empty!=A subset S} defect[A], with
all shared defect polynomials coming from THIS same F. Minimality requires
Delta Q_S(i)>=s OR Delta Q_S(j)<=-t for every nonempty S.

The first missing implication is an actual-forest argument ruling out this
valley together with all those constraints. One sufficient conclusion is a
nonempty S with Delta Q_S(i)<s and Delta Q_S(j)>-t. No construction or universal
inequality proving that conclusion is established. The proof of the defect
partition, the exact star squares, and the root-profile recursion do not
supply it. This is not presented as a proved lemma.

The additional unknown in the rooted version is a shape condition on ALL
internal joint profiles, valid at the leaf and preserved by every actual
child recursion and external completion, that excludes the valley. The
lossless counting state alone does not constitute that condition.

## Old domain, excluded part, remaining domain
Old domain: every real minimum-counterexample residual configuration, with
all internal vertices, true rooted branch polynomials and any other components.
Newly excluded nonempty part of that actual domain: NONE established.
Remaining domain: UNCHANGED.

The cut-mode witness has U=D=8, outside that domain. The equal-message pair
also has no residual pair, and its tested completions have equal U,D. These
show why two unlocalized shortcuts are insufficient; they do not reduce the
original residual domain. Adding more necessary identities is not GAP_REDUCED.

## Alternative sufficient routes remain unresolved
J_H keeps the nonempty/isolate-free/K2-free HEREDITARY premises and conclusion
D<=U+1. The inherited RSM keeps the nonempty/isolate-free HEREDITARY premises,
its pair-dependent existential leaf, and no added K2 exclusion. For a leaf
l with support w put C=I(F-{l,w}), X=(1+x)C, Y=xI(F-N[w]). At every residual
pair some leaf must either admit no polarized ordering (E,L), or satisfy
Delta L_i*(-Delta E_j)-Delta L_j*(-Delta E_i)>=0 for its polarized ordering.
Polarization means Delta E_i<0, Delta E_j<=0, Delta L_i>=0, Delta L_j>0.
Both candidate universal assertions are UNRESOLVED. No valid J_H or RSM
refutation was obtained. Their conditional implications remain inherited,
not converted into a full proof by finite tests.

## Nonvacuous evidence
Final discovery has 122 accepted nonisomorphic forests within this run,
maximum order 53 and maximum D-U=1. Fixed materials and boundary completions
also have no residual pairs. Across these computations:
residual graphs=0; residual pairs=0; eligible nonvacuous RSM tests=0.
The primary original-problem contradiction has not been exercised on an
actual hard graph. This is finite absence, not a theorem of absence.
