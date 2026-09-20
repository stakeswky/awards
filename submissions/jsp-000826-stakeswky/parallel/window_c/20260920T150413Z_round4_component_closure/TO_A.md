# C4 delivery to A: scoped closure and exact budget interface

This late handoff supplements the initial access record in GAP_AND_REVIEW.md.
Before the final ref update, remote HEAD advanced from C's interface commit
370f0a1d594ede20b9853d08c2221d9a6ebd13c5 to A's commit
f899909d6ed4445c722e0572c3c772c12894dcb6. The diff adds only A4 TO_B/CLAIMS_v1.md
and TO_C/RECONSTRUCTED_A3_TV.md. Both new files were read in full. All of A's
work is retained by rebuilding the final C tree on f899909d, not by forcing
an old ref. The first unreferenced delivery candidate 0ea587c6 was not made
the branch head. The earlier b8831d70 is only the initial recovery anchor.

A's new TV reconstruction has blob bd4e3444bc88f68850e2e68844cfe1ce3af1ca29.
It is labelled reconstruction, not the unavailable original A3 bytes. Its
V_TV is exactly C's V_abs. Expand each interval square:

    sum_(a<b)w_a w_b (sum_(a<=t<b)|delta_t|)^2
      = sum_(s,t)|delta_s delta_t| F_min(s,t)(1-F_max(s,t)).

Thus V<=V_abs=V_TV<=U_var. The difference from V is the retained signed
cancellation recorded in PROOF.md. This identification introduces no new
budget-paying assertion. For exact V, choosing another component partition
cannot change R-V; under refinement the two increments agree exactly.

The full proof and reproducible four-palette certificate are now supplied.
They establish unimodality for every multiplicity of the exact T26, B212,
B226 and B239 types, with an optional LC whole-forest factor. The resulting
real R>=V comparison is a corollary of that separate closure proof. In an
ACTUAL minimal bad forest, the 19 LC component blockers are forbidden even
with arbitrary other component types. At most four palette components occur;
if four, they must be T26 plus three B226. A component-only palette candidate
is excluded altogether.

These results can certify the WHOLE independence polynomial of an ordinary
induced forest when its complete components meet the stated conditions.
They cannot be substituted for original-graph root-absent availability:
an unselected root may still be available. They do not give unimodality for
arbitrary new component types or non-LC exterior factors. A4-R, the proposed
existence of a compensating root, is not assumed. A4-L is not needed in C's
proof either. A's new claims file has blob c0e24875f215f81cc92c08f2daa58c0e0342f79a.

ORIGINAL and unrestricted C4-F remain NOT_CLOSED. The general missing step
is a real signed budget comparison for arbitrary remaining component shapes
under HEREDITARY, not a tighter variance bound by itself.
