# Formalization status: NOT_ESTABLISHED; top-level build NOT_RUN

The attempted toolchain pin is `leanprover/lean4:v4.31.0`, an official release.
The executable was not present. Both an actual version probe and a compilation
probe failed to launch. One bounded download attempt failed with curl exit 6
(DNS resolution). Exact commands and errors are in `logs/lean-probe.json`.
There is no installed-toolchain hash to report and no fresh top-level axiom list.

`Probe.lean` is explicitly only an environment test. It did not run. It is not
an approximation of the FAMILY theorem. No `sorry`, custom target axiom, or
partial arithmetic lemma is presented as a completed top-level formal proof.
No old `.olean`, historical log, repository CI or earlier theorem is credited.

Even an available Lean binary would not by itself finish this work: the new
complete mathematical argument has not been translated into Lean sources.
The missing formal obligations are the actual graph/count identities, the
finite-order ULC convolution theorem, certificate checker soundness and full
coverage, the mixed-contribution and ratio lemmas, the infinite-tail argument,
and their composition into FAMILY-LC and FAMILY with the exact B59 quantifiers.
The intended public graph interface is the standard finite `SimpleGraph`
semantics with ordinary `Nat` and finite-subset cardinalities. No custom natural
number or modified independent-set meaning is introduced by this package.

ORIGINAL has neither a complete mathematical proof nor a formal proof here.

Official validation guidance consulted:
https://lean-lang.org/doc/reference/latest/ValidatingProofs/
Proof elaboration, exact statement correspondence, transitive axiom reporting,
and fresh-source checking are separate obligations; none is inferred from a
Python pass or from source hashes. The attempted pin's release page is
https://github.com/leanprover/lean4/releases/tag/v4.31.0 .
