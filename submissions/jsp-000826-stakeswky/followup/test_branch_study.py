#!/usr/bin/env python3
"""Small controls for the public, exact study (not a proof of the conjecture)."""
import itertools,json,subprocess,sys,tempfile,unittest
from pathlib import Path
import branch_study as b
import audit_study as a

class StudyTests(unittest.TestCase):
    def test_known_tree14(self):
        p=[-1,0,1,2,2,2,0,6,6,6,0,10,10,10]
        expected=[1,14,78,230,411,489,400,225,84,19,2]
        rec,_=a.checker(p)
        self.assertEqual(list(rec((1<<14)-1)),expected)
        self.assertEqual(b.packed(p)[0],expected)
        self.assertIsNone(b.valley(expected))

    def test_all_plateau_sequences(self):
        count=0
        for n in range(1,9):
            for seq in itertools.product(range(3),repeat=n):
                self.assertEqual(b.valley(seq) is None,a.unimodal(seq));count+=1
        self.assertEqual(count,9840)
        self.assertEqual(b.valley([1,4,3,3,4,1]),[1,3])

    def test_small_direct_subsets(self):
        for arms in [[[1]],[[2]],[[1,1]],[[2],[1]],[[1,2],[1]]]:
            p=b.graph(arms);n=len(p);expected=[0]*(n+1)
            av=[[0]*(n+1) for _ in p];bv=[[0]*(n+1) for _ in p]
            for mask in range(1<<n):
                if any(mask>>i&1 and mask>>p[i]&1 for i in range(1,n)):continue
                k=mask.bit_count();expected[k]+=1
                for v in range(n):(bv if mask>>v&1 else av)[v][k]+=1
            while len(expected)>1 and expected[-1]==0:expected.pop()
            self.assertEqual(b.packed(p)[0],expected)
            for v,(x,y) in enumerate(b.splits(p)):
                self.assertEqual(x+[0]*(n+1-len(x)),av[v]);self.assertEqual(y+[0]*(n+1-len(y)),bv[v])

    def test_palette_and_symbolic_bounds(self):
        self.assertEqual(len(b.palette()),21)
        self.assertEqual([len(x) for x in b.bounds()],[25,25])
        self.assertTrue(all(v>0 for terms in b.bounds() for _,v in terms))

    def test_invalid_parents(self):
        for p in [[],[-1,1],[-1,-1],[-1,2,1],[-1,3,0]]:
            with self.assertRaises((AssertionError,ValueError)):b.packed(p)
            with self.assertRaises((AssertionError,ValueError)):a.checker(p)

    def test_canonical_reroot(self):
        p=b.graph([[1,2],[3],[1,1]])
        adj=[[] for _ in p]
        for v in range(1,len(p)):adj[v].append(p[v]);adj[p[v]].append(v)
        for root in range(len(p)):
            ids={root:0};order=[root];parents=[-1]
            for v in order:
                for w in reversed(adj[v]):
                    if w not in ids:ids[w]=len(order);order.append(w);parents.append(ids[v])
            self.assertEqual(b.canonical(p),b.canonical(parents))

    def test_corrupt_count_rejected(self):
        row=b.evaluate('palette-small',[[3],[4]],1);row['coefficients'][2]+=1
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'bad.jsonl').write_text(json.dumps(row)+'\n')
            with self.assertRaises(AssertionError):a.main(p/'bad.jsonl',p/'out.json',1)
            self.assertFalse((p/'out.json').exists())

    def test_optimized_mode_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'not-created'
            run=subprocess.run([sys.executable,'-O',str(Path(b.__file__)),'--out',str(out)],capture_output=True)
            self.assertNotEqual(run.returncode,0);self.assertFalse(out.exists())

if __name__=='__main__':unittest.main(verbosity=2)
