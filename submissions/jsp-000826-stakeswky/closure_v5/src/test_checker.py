#!/usr/bin/env python3
"""Checker regressions, not a replacement for the quantified proof certificates."""
import unittest
from fractions import Fraction as F
from itertools import combinations
from verify_envelope import primary_test,replay_test,lower_primary,lower_replay
from verify_blocks import packed_mul,palette_replay,lc_margins,ulc_margins
from verify_graphs import validate,counter,brute,valley
from polynomials import B,mul

class CheckerTests(unittest.TestCase):
    def test_square_root_elimination_at_rational_squares(self):
        for p in range(6):
            for q in range(1,6):
                for rn in range(1,21):
                    r=F(rn,10);actual=max(F(0),1-F(p,q))**2<=r
                    for test in (primary_test,replay_test):
                        self.assertEqual(test(p*p,q*q,rn,10,1,1),actual)
    def test_squaring_negative_left_side(self):
        for test in (primary_test,replay_test):
            self.assertTrue(test(0,1,2,1,1,1))
            self.assertFalse(test(0,1,999,1000,1,1))
            self.assertTrue(test(1,4,1,4,1,1))
            self.assertFalse(test(1,4,249,1000,1,1))
    def test_lower_rational_algorithms(self):
        for t in range(4,8):
            for S in range(3*t,17*t+1):
                d=min(3*t,(S+2*t)//5,18*t-S)
                for j in range(1,S+2):
                    self.assertEqual(F(*lower_primary(t,S,d,j)),F(*lower_replay(t,S,d,j)))
    def test_palette(self):self.assertEqual(set(B),set(palette_replay()))
    def test_packed_products(self):
        for a in ([1],[1,0,3],[7,9,2],[1,1,1,1]):
            for b in ([1,5],[8,0,9],[1]*13):self.assertEqual(mul(a,b),packed_mul(a,b))
    def test_bad_LC_and_ULC_detected(self):
        self.assertLess(min(lc_margins([1,4,1,4])),0)
        self.assertLess(min(ulc_margins([1,1,1],2)),0)
    def test_plateaus_and_valleys(self):
        self.assertEqual(valley([1,4,4,3,3,4]),[2,4])
        self.assertIsNone(valley([1,4,4,3,3,0,0]))
    def test_invalid_graphs_rejected(self):
        for n,e in [(1,[(0,0)]),(2,[(0,1),(1,0)]),(3,[(0,1),(1,2),(2,0)]),(1,[(0,1)])]:
            with self.assertRaises(ValueError):validate(n,e)
    def test_all_forests_on_at_most_five_labeled_vertices(self):
        checked=0;by_n=[]
        for n in range(6):
            at_n=0
            pairs=list(combinations(range(n),2))
            for mask in range(1<<len(pairs)):
                edges=[e for i,e in enumerate(pairs) if mask>>i&1]
                try:validate(n,edges)
                except ValueError:continue
                adj,rec,dp=counter(n,edges);allv=(1<<n)-1
                self.assertEqual(list(rec(allv)),dp(allv));self.assertEqual(brute(n,edges),dp(allv))
                checked+=1;at_n+=1
            by_n.append(at_n)
        self.assertEqual(by_n,[1,1,2,7,38,291])
        self.assertEqual(checked,340)

if __name__=='__main__':unittest.main(verbosity=2)
