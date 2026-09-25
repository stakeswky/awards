# External dependency audit: arXiv:2609.20961v1

Run 20260921T123043Z_round8_misalignment_strip. This is a reading and interface
review, NOT independent external peer review or a fresh formal build.

## Identified source and status

Authors: Ethan X. Fang, Junwei Lu, Eran Nevo, Yuan Yao, Hailun Zheng.
Title: Unimodality of Independence Polynomials for Sufficiently Large Forests.
Version: arXiv:2609.20961v1, submitted2026-09-17 18:16:42 UTC,18 pages.
Official full text: https://arxiv.org/html/2609.20961v1
Official version metadata: https://arxiv.org/abs/2609.20961
The official HTML identifies a CC BY4.0 license. The source was read through
web tools; no claim is made that original TeX/PDF bytes were downloaded or
hashed. This is a newly located EXTERNAL result, not project-authored research.

## Exact use in C8

Only its Theorem1.2 is a necessary external mathematical dependency of
C8-LARGE-PAY: uniform strict log-concavity for every sufficiently large
n-vertex forest at n/5<=j<=17alpha(F)/25. Theorem1.1 separately states
unimodality above an absolute order threshold. Section9 explicitly leaves
the all-order conjecture open. Neither theorem supplies a numeric threshold.
We do not claim that n438, the old n6280 control, or any other explicit graph
is known to lie above that threshold.

The new C8 application proves its own project-middle range inclusion and
its own exact strip/budget lower bound, in PROOF.md Sections5.3--5.4.
No statement about modal/max/envelope surrogate gates follows from this use.

## What was actually checked in reading

The proof path was read in the official HTML, including Sections4--8 and
final remarks. At the interfaces, the following points were checked:

* Root conditioning uses actual descendant subtrees, not arbitrary arrays;
  the constants controlling conditional first/second moments are uniform
  over graph shapes, allowing high degree.
* The normal approximation is uniform over forests and the fixed fugacity
  interval. Its proof has separate conditional mean and variance errors.
* An all-frequency bound, not the CLT alone, supplies integrable domination
  for the Fourier second difference. The sign limit is strictly positive.
* The fugacity mean bracket contains the stated coefficient interval. This
  random-size mean is not the project's one-vertex-extension mean mu_k.
* The patching uses the actual full-graph tail. No component-LC assumption
  enters the external statement. The constant N is existential throughout.

The explicit conditional Fourier calculation in C8 explains the dependency
boundary; C8 does not claim to re-prove every probabilistic lemma in the paper.
A few display-level slips (for example the missing square on i_k in the
introductory proof sketch) were read against the exact Theorem1.2 and its
positive second-difference argument, not elevated into different theorems.
No contradiction in the specific theorem interface used by C8 was identified.
This limited review does not amount to an independent certification of every
line or of the authors' claimed formalization.

## Formal source access

The paper links
https://github.com/junwei-lu/Erdos_993_Tree_Independent_Set_Unimodality .
The connected GitHub contents read returned404. No source was obtained from
that repository; no Lean build, target theorem check, or axiom audit was run.
The paper's statement that a formalization exists is not a C8 execution receipt.

## Relation to earlier project facts

The older beta boundary comes from Basit--Galvin,
https://arxiv.org/html/2006.12562v2 , Theorem1.3. It is inherited, not novel.
Previous finite-family and P4 results stay valid at their original explicit
scopes. The new preprint adds an all-shape asymptotic dependency, not an
explicit finite cutoff or an all-size solution. No prize, novelty, priority,
organizer acceptance, or repository catalog change is requested.
