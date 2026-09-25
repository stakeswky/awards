# Internal review

Review type: SAME_MODEL_SELF_REVIEW with exact finite checks; not external peer review.

1. The component allocation law uses the actual product coefficients and conditions on the exact sizes selected in every component. No external factor is cancelled.
2. Total variance is decomposed with the between-allocation term Var_a(m_a). Dropping it would make the argument invalid; both displayed decompositions retain it.
3. The forest identity eta=mu-Ec uses c(empty)=0 and is valid componentwise.
4. C1 is clearly labelled a candidate. The implication C1 => plateau-safe BARRIER is proved, but no converse or theorem status is claimed.
5. A failure of C1 is not called an ORIGINAL counterexample. The descent history and beta position remain separate.
6. The minimal-component theorem assumes vertex-minimal ORIGINAL failure. It does not infer that an arbitrary counterexample has only non-LC components; one first passes to a vertex-minimal induced counterexample.
7. The strong-unimodality convolution fact is used only for an LC component times a unimodal complementary forest. No claim that unimodal times unimodal is unimodal is made.
8. The C1 census is finite evidence. The mathematical decompositions do not depend on it.
9. No Lean build or axiom audit was run. Repository CI is not mathematical verification.
10. The previous A package could not be safely reconstructed byte-for-byte through the available repository-write interface from the large local-only patch, so it was not partially published. Window B's commit is preserved.
