#!/usr/bin/env python3
"""Regression and rejection tests for the threshold refinement."""
import unittest
from fractions import Fraction
from itertools import product as tuples
from threshold_certificate import integer_bounds, rational_bound, check_t, require
from branch_study import palette, bounds, branch, graph, product, add, packed, valley, lc
from audit_study import checker, unimodal
from continued_probe import cases


class ThresholdTests(unittest.TestCase):
    def test_independent_bound_formulas(self):
        for t in range(1,13):
            d,n=integer_bounds(t,4*t+2)
            for k in range(1,len(n)):
                self.assertEqual(Fraction(n[k],d),rational_bound(t,k))

    def test_retains_old_three_terms(self):
        for t in (3,10,45,47,70):
            for k in range(1,80):
                old=Fraction(3*t,4)+Fraction((k-1)*(t-1),64)+Fraction((k-1)*(k-2)*(t-1)*(t-2),4608*t)
                self.assertGreaterEqual(rational_bound(t,k),old)

    def test_boundary_failures_are_not_hidden(self):
        self.assertEqual(check_t(44)['failed_indices']['LC'],list(range(34,50)))
        self.assertFalse(check_t(45)['failed_indices']['LC'])
        self.assertEqual(check_t(46)['failed_indices']['corridor_square'],[40,41])
        self.assertTrue(all(not v for v in check_t(47)['failed_indices'].values()))

    def test_palette_and_infinite_tail(self):
        self.assertEqual(len(palette()),21)
        for p in bounds():
            self.assertEqual(len(p),25)
            self.assertTrue(all(v>0 for _,v in p))

    def test_case_scope(self):
        seq=list(cases());self.assertEqual(len(seq),134)
        pal={tuple([s]*d) for d,s in palette()}
        for kind,_,arms,_ in seq[:128]:
            self.assertEqual(kind,'outside-palette')
            self.assertTrue(any(tuple(a) not in pal for a in arms))
        self.assertEqual([r[1] for r in seq[-6:]],[44,45,46,47,69,70])

    def test_known_log_concavity_failure_not_unimodality(self):
        arms=[[1]*3,[1]*4,[1]*4]
        original=graph(arms);p=[-1]+[v-1 for v in original[2:]]
        formula=add(product(branch(a)[1] for a in arms),[0]+product(branch(a)[0] for a in arms))
        actual=packed(p)[0];rec,_=checker(p)
        self.assertEqual(formula,actual);self.assertEqual(tuple(actual),rec((1<<len(p))-1))
        self.assertEqual(actual[-3:],[2979,51,1])
        self.assertFalse(lc(actual));self.assertIsNone(valley(actual))

    def test_invalid_inputs(self):
        for p in ([],[-1,2],[-1,-1],[-1,1],[-1,False]):
            with self.assertRaises(ValueError):checker(p)
        for t in (0,-1,True):
            with self.assertRaises(ValueError):integer_bounds(t,5)
        with self.assertRaises(ValueError):require(False,'reject modified certificate')

    def test_valleys_include_platforms(self):
        for n in range(1,7):
            for a in tuples(range(3),repeat=n):
                self.assertEqual(valley(a) is None,unimodal(a))
        self.assertIsNotNone(valley([3,2,2,4]))


if __name__=='__main__':
    unittest.main(verbosity=2)
