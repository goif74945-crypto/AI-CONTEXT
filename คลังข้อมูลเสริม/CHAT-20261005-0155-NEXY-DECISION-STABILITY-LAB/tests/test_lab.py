from __future__ import annotations
from pathlib import Path
import itertools, random, sys, unittest

sys.path.insert(0,str(Path(__file__).parent.parent/"code"))
from core import Decision, DuplicateEvidenceError, Evidence, Kind, StabilityError, canonicalize, fingerprint
import mono, iris, edge, mde, suite
from damp import Guard, Observation

def atom(eid,kind,tags=()):
    return Evidence(eid,kind,f"claim:{eid}",{"score":1},"test",tags)

def oracle(items):
    support=sum(x.kind is Kind.SUPPORT for x in items)
    block=sum(x.kind is Kind.BLOCK for x in items)
    if block>=2: return Decision.REJECT
    if block==1: return Decision.FREEZE
    return Decision.RELEASE if support>=2 else Decision.FREEZE

class CoreTests(unittest.TestCase):
    def test_fingerprint_order_invariant(self):
        a=[atom("a",Kind.SUPPORT),atom("b",Kind.BLOCK)]
        self.assertEqual(fingerprint(a),fingerprint(reversed(a)))
    def test_canonical_duplicate_equivalent_tag_order(self):
        a=atom("x",Kind.SUPPORT,("a","b")); b=atom("x",Kind.SUPPORT,("b","a"))
        self.assertEqual(len(canonicalize([a,b])),1)
    def test_conflicting_duplicate_rejected(self):
        with self.assertRaises(DuplicateEvidenceError):
            canonicalize([atom("x",Kind.SUPPORT),atom("x",Kind.BLOCK)])
    def test_nan_rejected(self):
        with self.assertRaises(StabilityError):
            Evidence("x",Kind.CONTEXT,"x",float("nan"),"test")

class MonoTests(unittest.TestCase):
    def test_valid_monotone_oracle(self):
        r=mono.verify([atom("s1",Kind.SUPPORT)],[atom("s2",Kind.SUPPORT),atom("b",Kind.BLOCK)],oracle)
        self.assertTrue(r["passed"])
    def test_broken_support_regression_detected(self):
        def broken(items):
            n=sum(x.kind is Kind.SUPPORT for x in items)
            return Decision.RELEASE if n==1 else Decision.FREEZE
        r=mono.verify([atom("s1",Kind.SUPPORT)],[atom("s2",Kind.SUPPORT)],broken)
        self.assertFalse(r["passed"])

class IrisTests(unittest.TestCase):
    def test_noise_and_order_invariant(self):
        r=iris.scan([atom("a",Kind.SUPPORT),atom("b",Kind.SUPPORT)],[atom("c",Kind.CONTEXT)],oracle)
        self.assertTrue(r["passed"])
    def test_non_context_noise_rejected(self):
        with self.assertRaises(ValueError):
            iris.scan([], [atom("x",Kind.BLOCK)], oracle)
    def test_order_sensitive_oracle_detected(self):
        def broken(items):
            return Decision.RELEASE if items and items[0].evidence_id=="a" else Decision.FREEZE
        r=iris.scan([atom("a",Kind.SUPPORT),atom("b",Kind.SUPPORT)],[],broken)
        self.assertFalse(r["passed"])

class EdgeTests(unittest.TestCase):
    def test_distance_one_boundary(self):
        base=[atom("s1",Kind.SUPPORT),atom("s2",Kind.SUPPORT)]
        r=edge.map_boundary(base,[*base,atom("b1",Kind.BLOCK)],oracle)
        self.assertEqual(r["minimum_distance"],1)
    def test_budget_truncation_explicit(self):
        base=[atom(f"s{i}",Kind.SUPPORT) for i in range(4)]
        r=edge.map_boundary(base,base,oracle,max_evaluations=1)
        self.assertTrue(r["truncated"])
    def test_input_order_deterministic(self):
        base=[atom("s1",Kind.SUPPORT),atom("s2",Kind.SUPPORT)]
        world=[*base,atom("b1",Kind.BLOCK),atom("s3",Kind.SUPPORT)]
        self.assertEqual(edge.map_boundary(base,world,oracle),edge.map_boundary(list(reversed(base)),list(reversed(world)),oracle))

class MdeTests(unittest.TestCase):
    def test_release_minimum_two_supports(self):
        base=[atom("s1",Kind.SUPPORT),atom("s2",Kind.SUPPORT),atom("s3",Kind.SUPPORT),atom("c",Kind.CONTEXT)]
        self.assertEqual(mde.extract(base,oracle)["minimum_size"],2)
    def test_empty_subset_can_reproduce_freeze(self):
        self.assertEqual(mde.extract([atom("c",Kind.CONTEXT)],oracle)["minimum_size"],0)

class DampTests(unittest.TestCase):
    def test_promotion_dwell(self):
        g=Guard(promotion_dwell=2)
        self.assertIs(g.observe(Observation(1,Decision.RELEASE,"x"))["public"],Decision.FREEZE)
        self.assertIs(g.observe(Observation(2,Decision.RELEASE,"x"))["public"],Decision.RELEASE)
    def test_fingerprint_change_resets(self):
        g=Guard(promotion_dwell=2)
        g.observe(Observation(1,Decision.RELEASE,"a"))
        r=g.observe(Observation(2,Decision.RELEASE,"b"))
        self.assertEqual((r["public"],r["pending_count"]),(Decision.FREEZE,1))
    def test_safety_regression_immediate(self):
        g=Guard(initial=Decision.RELEASE,promotion_dwell=99)
        r=g.observe(Observation(1,Decision.FREEZE,"x"))
        self.assertEqual((r["public"],r["reason"]),(Decision.FREEZE,"safety_regression_immediate"))
    def test_replay_rejected(self):
        g=Guard(); g.observe(Observation(5,Decision.FREEZE,"x"))
        with self.assertRaises(StabilityError): g.observe(Observation(5,Decision.FREEZE,"x"))

class IntegrationTests(unittest.TestCase):
    def test_five_system_pipeline(self):
        base=[atom("s1",Kind.SUPPORT),atom("s2",Kind.SUPPORT)]
        s3=atom("s3",Kind.SUPPORT); b1=atom("b1",Kind.BLOCK)
        r=suite.run(oracle,baseline=base,monotonic_candidates=[s3,b1],
            irrelevant_context=[atom("noise",Kind.CONTEXT)],universe=[*base,s3,b1],
            temporal_evidence=[[atom("s1",Kind.SUPPORT)],base,[*base,s3],[*base,s3],[b1]],promotion_dwell=2)
        self.assertTrue(r["passed"])
        self.assertEqual(r["edge"]["minimum_distance"],1)
        self.assertEqual(r["mde"]["minimum_size"],2)
        self.assertEqual([x["public"] for x in r["temporal"]][-2:],[Decision.RELEASE,Decision.FREEZE])
    def test_all_four_atom_permutations_same_fingerprint(self):
        items=[atom("a",Kind.SUPPORT),atom("b",Kind.BLOCK),atom("c",Kind.CONTEXT),atom("d",Kind.SUPPORT)]
        expected=fingerprint(items)
        for p in itertools.permutations(items): self.assertEqual(fingerprint(p),expected)
    def test_random_monotonicity_100_cases(self):
        rng=random.Random(202610050155)
        for case in range(100):
            base=[atom(f"{case}:s:{i}",Kind.SUPPORT) for i in range(rng.randrange(4))]
            base += [atom(f"{case}:b:{i}",Kind.BLOCK) for i in range(rng.randrange(3))]
            r=mono.verify(base,[atom(f"{case}:sx",Kind.SUPPORT),atom(f"{case}:bx",Kind.BLOCK)],oracle,max_group_size=1)
            self.assertTrue(r["passed"])

if __name__=="__main__": unittest.main()
