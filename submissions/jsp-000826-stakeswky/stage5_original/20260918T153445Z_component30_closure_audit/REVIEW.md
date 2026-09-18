# Review

Review type: **SAME_MODEL_AUDIT_OF_PINNED_EXTERNAL_RESULT**.

This review is separate from the external finding's reported independent reproduction. The present run did not independently rerun the heavy census.

## Checks

1. **Graph-to-product semantics.** For a disjoint union, the independence polynomial is the product of component polynomials by a direct bijection.
2. **Interval support.** If a graph has an independent set of maximum size alpha, every size 0,...,alpha occurs by taking subsets. Independence sequences therefore satisfy the interval-support condition used by strong unimodality.
3. **Normalization.** Keilson--Gerber is commonly stated for probability sequences. Dividing positive finite sequences by their total masses does not change log-concavity or unimodality, and convolution changes only by a positive scalar. The application is valid.
4. **Repeated components.** The pinned closure code uses sorted index tuples with repetition, so pair and triple coverage is multiset coverage.
5. **Minimal-counterexample induction.** If a proper factor is log-concave and the complementary factor is unimodal, strong unimodality contradicts minimal non-unimodality. Therefore every proper nonempty factor of a minimal counterexample must be non-log-concave. Empty H_3 then excludes every size at least four because each 3-submultiset would belong to H_3.
6. **Arithmetic transcript.** The fresh local checker verifies the published counts: 2+19+7+121=149; C(150,2)=11,175 pair multisets; 11,078+97=11,175; 111+10,712=10,823; and 11,175+10,823=21,998.
7. **External evidence boundary.** The pinned external log states 149 non-log-concave but unimodal trees, 11,175 unimodal pair products, 97 non-log-concave pairs, 10,823 unimodal triple candidates and empty H_3. These are not relabeled as fresh computations here.
8. **Independent review boundary.** The SciNet finding reports a 2026-08-04 disjoint reproduction of the headline counts and Lane-A closure. It also records a stale session-specific path in `build_qsets.py` that can interrupt one clean-clone verification path. That is retained as a reproducibility note; it is not silently called fixed by this repository.
9. **ORIGINAL boundary.** The conclusion is only that a counterexample must contain a component with at least 31 vertices. `J_H`, `RSM`, the all-real-forest residual incompatibility, and the unrestricted conjecture remain unresolved.
10. **Formal boundary.** No Lean source, build, or axiom audit is run in this stage. `ORIGINAL_FORMAL=NOT_ESTABLISHED`.

## Verdict

The component-order-30 reduction is mathematically sound **conditional on the pinned external census/closure certificates and the two cited classical convolution theorems**. It is a real scoped reduction of the possible counterexample domain. It is not a proof of Erdős #993.
