# Phase 11: global third-minor theorem

## Statement and status

For every finite simple undirected unweighted forest `F`, if `p_k(F)` counts
independent `k`-sets, then

`p_3(F)^2 >= p_2(F) p_4(F)`.

This is a scoped theorem for the original forest problem. It does not prove
unimodality of every forest and does not close Erdős #993. Together with the
previous `k=1,2` bounds, any failure of the stronger `PREFIX_BETA` conjecture
must occur at `k>=4`.

## Evidence

`PROOF.md` gives a written proof for every order `n>=12`. Orders `1..11` are
covered by `src/check_l3.py`, which enumerates every unlabelled forest as a
multiset of NetworkX 3.6.1 non-isomorphic free-tree representatives. It checks
1,347 forests built from 436 tree types. Every complete independence
polynomial is computed twice: rooted-tree DP plus component convolution, and
literal vertex-subset enumeration. The two methods agree on 10,342 coefficient
entries. The closed formulas for `p_2,p_3,p_4` are checked against the literal
counts and every `L_3` is nonnegative.

Environment actually run: Python 3.13.5, NetworkX 3.6.1.

Observed hashes:

- `src/check_l3.py`: `678e36608a0c6d41c9c59ff71d14cf294f88615ac91ca2696373845dfb4697c5`
- `certificates/L3_SMALL_FORESTS.json`: `1e05be6f3beb95d377e96d330a9592e930431a5e86596944c578b11cfdd0a39a`
- generated record stream: `dc0c85dc6e13e9f1be5e334084992bddc95c3a1ca654c8613377fd13a6616d65`

Reproduce:

```bash
python3 src/check_l3.py
sha256sum src/check_l3.py certificates/L3_SMALL_FORESTS.json
```

## Review boundary

Same-model review checked the inclusion-exclusion formula for `p_4`, the sign
of the dropped `+p_2 t` term, the monotonicity step in `s`, the comparison in
`m`, and the complete finite base. No Lean build or axiom audit was run. This
is not independent external peer review. No global novelty or prize claim is
made.

## Remaining gap

`PREFIX_BETA` is still unproved for `k>=4`. The Phase-9/10 whole-forest
availability-variance barrier, `J_H`, and `RSM` also remain unresolved. A
negative later log-concavity minor would still need a complete-sequence valley
check before it could count as an Erdős #993 counterexample.
