# D9 external formal verification interface v1

Run: 20260921T161307Z_round9_external_formal_audit.
ORIGINAL=NOT_CLOSED. D8 two-leaf results are preserved; no new leaf theorem is claimed.
External source: junwei-lu/Erdos_993_Tree_Independent_Set_Unimodality,
commit b2a1d3ede8aef259b1de6e319e7fd6cb56481ac1.
This is an audit interface, not a completed Lean verification certificate.

## D9-EXT-v1: evidence contract

The target declarations are ErdosProblem993.main_fin and
ErdosProblem993.unimodal_of_isAcyclic. Their existential threshold precedes
all finite graph quantifiers. They do NOT assert all-order unimodality.
The paper v1 upper bound is 17*alpha/25; Central.lean proves a statement
with upper bound 64*alpha/95. Both exceed 2*alpha/3, but are not identical.
main_fin chooses max 1000 N1 with N1 obtained from central: 1000 is not N0.

Basic.lean imports the entire Mathlib aggregation. The manifest pins mathlib
5e932f97dd25535344f80f9dd8da3aab83df0fe6 and eight additional packages;
Lean is pinned to v4.29.1. The manifest package name StatLean differs from
lakefile.toml's ErdosProblem993. This is recorded, not declared a proof error.

At release, shell calls to lake build and lake env lean
ErdosProblem993/AxiomCheck.lean both exit 127: Lake is absent. The official
toolchain download and dependency transport also fail DNS. No Lean source
was elaborated, no transitive axiom output was obtained, and no BUILD_PASS
or AXIOM_PASS is claimed. GitHub connector source reading does work.
The audit continues with explicit import and selected analytic-body review.

## D9-MIDDLE-v1: conditional project interface, written arithmetic proof

For positive integers n,M,alpha with M<=n and n<=2*alpha, let
h=floor(M*(n-1)/(4*M-2))+1 and beta=ceil(alpha*(n-1)/(n+alpha)).
If h<=k and j=k+1<beta, then ceil(n/5)<=j<=floor(64*alpha/95).
For an actual forest meeting the unknown central threshold, central therefore
supplies p_(j-1)*p_(j+1)<p_j^2. If p_j<=p_(j-1), then p_(j+1)<p_j.
No HEREDITARY assumption, positive current loss, or division by loss is used.
A plateau is covered. This consequence remains conditional on the external
theorem; it neither calculates N0 nor proves a special leaf/root exists.

Use signed integer or real coefficients in the identity
 a*(b-c)=(b*b-a*c)+b*(a-b).
Natural-number truncated subtraction cannot replace signed subtraction.
The exact weaker criterion is b*b-a*c>=b*(b-a), not necessarily nonnegative LC.

## What A may reuse now

The source-level threshold chain is main_fin -> central -> mean_lc ->
curvature_limit -> compact standardized characteristic-function convergence,
Gaussian domination and variance bounds. Curvature uses
stdCharFn_tendsto_gaussian, not uniform_clt's later CDF statement; the latter
is separately derived from the former using Esseen smoothing.
Full proof-term dependencies still require a real build and qualified
#print axioms. README output and grep results are not execution evidence.
Later findings, scripts and verdicts will be separate files; this v1 is immutable.
Publication does not assert any peer has read it.
