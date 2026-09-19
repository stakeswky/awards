# Proof audit for the component-order-30 reduction

## 1. Disjoint components give convolution

If a forest is the disjoint union F=F_1 sqcup ... sqcup F_r, an independent set in F is uniquely a choice of one independent set in each component. Hence

    I(F;x) = product_q I(F_q;x),

and the coefficient sequence is the repeated convolution of the component sequences. This is a direct bijection.

Every coefficient from size 0 through the independence number is positive: take any maximum independent set and any subset of it. Thus the support of an independence sequence is an interval.

## 2. Separate log-concave and non-log-concave components

Assume every component has at most 30 vertices and accept the pinned external tree census. Every component sequence is unimodal. Split the components into L, whose independence sequences are log-concave, and M, whose sequences are not log-concave.

By Hoggar's convolution theorem, the product polynomial for all components in L has a log-concave coefficient sequence. Therefore, if the product for M is unimodal, Keilson--Gerber strong unimodality shows that multiplying by the log-concave L-product preserves unimodality.

It remains only to prove that every multiset product from the finite bank S of the 149 non-log-concave component sequences is unimodal.

## 3. Finite-basis closure lemma

For a multiset Q from S, write p(Q) for its product sequence. Define H_r to be the size-r multisets Q for which p(Q) is non-log-concave and every deletion of one distinct multiset occurrence gives an element of H_(r-1). At level 1, H_1=S.

The pinned computation gives:

- every size-2 multiset product is unimodal;
- |H_2|=97;
- every size-3 candidate obtained by extending H_2 is unimodal;
- every size-3 candidate whose every distinct deletion lies in H_2 is log-concave, so H_3 is empty.

Suppose a multiset product from S is non-unimodal and choose a counterexample multiset Q of least size. Every nonempty proper submultiset has a unimodal product by minimality.

If a nonempty proper submultiset A had a log-concave product, let B=Q\A. The product p(B) is unimodal by minimality. Keilson--Gerber would make p(A)*p(B)=p(Q) unimodal, a contradiction. Therefore every nonempty proper submultiset of Q has a non-log-concave product.

Size 1 is impossible because each member of S is unimodal. Size 2 is impossible by the complete pair check. Size 3 is impossible by the complete triple-candidate check.

If |Q|>=4, take any 3-element submultiset T of Q. It is proper, so its product is unimodal and non-log-concave. Every 2-element deletion from T is also a proper submultiset of Q, hence has a non-log-concave product and belongs to H_2. Thus T lies in H_3. But the pinned computation has H_3 empty, a contradiction.

Hence every multiset product from S is unimodal. Repeated components cause no gap: all objects above are multisets, not sets, and the deletion condition is applied to distinct multiset values exactly as in the pinned closure program.

## 4. Forest corollary

The product for M is unimodal by Section 3. The product for L is log-concave by Hoggar. Keilson--Gerber therefore makes their convolution unimodal. Empty L or empty M is harmless: the identity sequence (1) is log-concave and unimodal.

Thus every forest all of whose components have order at most 30 has a unimodal independent-set sequence. Consequently any counterexample to Erdős #993 must contain a tree component of order at least 31.

## 5. What this does not prove

The argument depends on the pinned external tree census and closure computation plus the two classical convolution theorems. This run does not recompute the large census. It does not show that every tree on at least 31 vertices is unimodal. It does not prove the current `J_H` or `RSM` bridge, and it does not close ORIGINAL.
