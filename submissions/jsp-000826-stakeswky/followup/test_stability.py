#!/usr/bin/env python3
"""Finite regressions; these do not replace the general stability proof."""
import unittest
from itertools import product,combinations_with_replacement
from fractions import Fraction as F
from math import comb
from stability_certificate import build_certificate,direct_five,five_polynomial,evaluate,shift
from small_palette_study import formulas,audit_graph,recursive_ids,cases
from branch_study import lc,valley
from audit_study import unimodal,checker


class StabilityTests(unittest.TestCase):
    def test_quartic_certificate(self):
        c=build_certificate()
        self.assertEqual(c['finite_positive_indices'],41)
        self.assertEqual(c['positive_tail_coefficients'],5)
        self.assertTrue(all(r['numerator']>0 for r in c['finite_rows']))

    def test_five_term_monotonicity_regression(self):
        for k in range(1,81):
            previous=direct_five(24,k)
            for t in range(25,35):
                now=direct_five(t,k)
                self.assertGreaterEqual(now,previous)
                previous=now

    def test_stability_lemma_finite_grid(self):
        checked=0
        triples=list(product(range(6),repeat=3))
        for k in range(1,6):
            for a,c,d in triples:
                if k*c*c < (k+1)*a*d:continue
                for b,e,f in triples:
                    if b*f>e*e or k*b>a or k*f>d:continue
                    self.assertLessEqual((a+b)*(d+f),(c+e)**2)
                    checked+=1
        self.assertGreater(checked,0)
        print('stability-grid valid premise instances:',checked)

    def test_assumptions_cannot_be_dropped(self):
        # Dominance and strong LC alone are insufficient without LC of b.
        a,c,d,b,e,f,k=100,105,100,10,1,10,10
        self.assertGreaterEqual(k*c*c,(k+1)*a*d)
        self.assertTrue(k*b<=a and k*f<=d)
        self.assertGreater((a+b)*(d+f),(c+e)**2)
        self.assertGreater(b*f,e*e)
        # Ordinary LC alone is insufficient in place of factorial LC of z.
        self.assertTrue(lc([10,10,10]) and lc([1,0,0]))
        self.assertFalse(lc([11,10,10]))

    def test_all_small_generators_agree(self):
        for t in range(1,5):
            left=list(recursive_ids(t))
            right=[list(x) for x in combinations_with_replacement(range(21),t)]
            self.assertEqual(left,right)
            self.assertEqual(len(left),comb(20+t,t))

    def test_three_counting_routes(self):
        for arms in ([[3]],[[5]*3],[[4],[5,5]],[[3],[17],[5]*3,[8,8]]):
            for leaf in (True,False):
                p,c,pairs=formulas(arms,leaf)
                _,w,U,D=audit_graph(p,c,pairs)
                self.assertFalse(w)
                self.assertIsNone(valley(c))

    def test_bad_counts_rejected(self):
        p,c,pairs=formulas([[3],[4]],True)
        c=c[:];c[2]+=1
        with self.assertRaises(ValueError):audit_graph(p,c,pairs)

    def test_bad_graph_rejected(self):
        for p in ([],[-1,2,1],[-1,1],[-1,0,8],[-1,False]):
            with self.assertRaises(ValueError):checker(p)

    def test_known_non_lc_is_not_a_counterexample(self):
        p,c,pairs=formulas([[1]*3,[1]*4,[1]*4],False)
        self.assertEqual(len(p),26)
        self.assertEqual(c[-3:],[2979,51,1])
        self.assertFalse(lc(c))
        self.assertIsNone(valley(c))
        audit_graph(p,c,pairs)

    def test_plateaus_and_zero_shift(self):
        for c in product(range(3),repeat=6):
            self.assertEqual(valley(c) is None,unimodal(c))
            self.assertEqual(valley([0]+list(c)) is None,unimodal([0]+list(c)))

    def test_certificate_is_not_a_t23_claim(self):
        self.assertLess(direct_five(23,42),43)
        c,d=five_polynomial(24)
        for k in (43,100,10000):
            self.assertEqual(evaluate(c,k),evaluate(shift(c,43),k-43))
            self.assertGreater(evaluate(c,k),0)

    def test_complete_frozen_case_count(self):
        rows=list(cases())
        self.assertEqual(len(rows),12909)
        self.assertEqual(sum(r[0]=='palette-complete' for r in rows),12649)
        self.assertEqual(sum(r[0]=='outside-palette-probe' for r in rows),256)
        self.assertEqual(sum(r[0].endswith('control') for r in rows),4)


if __name__=='__main__':
    unittest.main(verbosity=2)
