# Audit of the adaptive nested-hub root-moment claim

Date: 2026-09-24.

## Question audited

The parallel package `parallel/window_claude/20260924T084900Z_root_moment_certificates/` reports two large finite root-moment certificates and labels the polylogarithmic root-moment bound as refuted. This audit checks the logical scope of that conclusion and independently recomputes the two fixed examples.

For a rooted tree at hard-core activity `lambda`, the quantity under discussion is

`M = q_root (1-q_root) delta_root^2`,

with the level recursion used in the parallel package.

## Independent recomputation

`verify_fixed_examples.py` is a separate direct high-precision Decimal implementation of the displayed recurrence. It uses the fixed child-count sequences of the two certified examples and exact integer arithmetic for the tree order.

It reproduces:

- `lambda=1`: `n = 444037630851675841201`, `M = 5.254278481224044...e6`, and `M/(ln n)^2 = 2324.610177...`;
- `lambda=3`: `n = 66560531541929765724627215360023888876848541589025718947221636445187811`, `M = 4.562449622767539...e41`, `M/(ln n)^2 = 1.715597512220218...e37`, and `log M/log n = 0.5882138651...`.

This corroborates the numerical values of the two fixed trees. It is not interval arithmetic and does not independently certify the outward-rounding implementation used by the parallel package.

## Logical correction

Two finite examples cannot refute the existence of a universal constant `C` in a statement such as

`M <= C (log n)^2`

for every tree in the relevant activity range. They only give lower bounds on any such constant. In particular, the two examples show that a uniform constant covering them must be at least about `1.7156e37` if `lambda=3` is included.

Likewise, finite examples do not prove that `M/(log n)^d` is unbounded for any fixed `d`, and they do not prove an asymptotic exponent. The preceding `WINDOW_LC_PROGRESS.md` explicitly describes the claimed exponent equality as numerical to about three decimals. That numerical slope evidence is useful, but it is not an analytic infinite-family lower bound.

Therefore the status `REFUTED_WITH_RIGOROUS_CERTIFICATES` for the existence of any polylogarithmic root-moment bound is too strong on the evidence currently stored in the repository.

## Correct status

The defensible conclusion from the audited material is:

1. the two explicit finite trees have very large root moments, and the fixed values are independently corroborated here;
2. they rule out small or moderate universal constants in a quadratic-log bound over the tested activity range;
3. they provide strong evidence for polynomial growth and for sharpness of the FLNYZ Holder exponent;
4. an analytic infinite family proving unbounded `M/(log n)^d` is still needed before declaring every polylogarithmic bound impossible.

This correction does not affect the original Erdős #993 status: `ORIGINAL = NOT_CLOSED`. It also does not produce a non-unimodal forest.

## Reproduction boundary

Run:

```bash
python3 verify_fixed_examples.py
```

The script uses only the Python standard library. No Lean build or axiom audit was run in this stage. The review is same-project review, not independent external peer review.
