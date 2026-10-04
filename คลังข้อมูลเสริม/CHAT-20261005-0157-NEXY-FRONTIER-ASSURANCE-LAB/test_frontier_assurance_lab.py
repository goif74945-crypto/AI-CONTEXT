
# ===== test_adversarial.py =====
import random
import unittest
from frontier_assurance_lab import Constraint,ConstraintEngine,Plan,ParetoPruner,PerturbationExperiment,HiddenDependencyDetector

class AdversarialDeterminismTests(unittest.TestCase):
    def test_muscle_100_permutations_same_result(self):
        engine=ConstraintEngine({"mode":["safe","fast","audit"]})
        base=[Constraint("a","mode","EQ",("safe",)),Constraint("b","mode","EQ",("fast",)),Constraint("c","mode","DENY",("audit",))]
        expected=engine.solve(base); rng=random.Random(74945)
        for _ in range(100):
            sample=base[:]; rng.shuffle(sample); self.assertEqual(engine.solve(sample),expected)
    def test_parex_100_permutations_same_result(self):
        p=ParetoPruner(); base=[Plan("a",10,8,3,5,1),Plan("b",8,8,4,5,2),Plan("c",7,10,2,8,1),Plan("d",1,1,9,9,9,False)]
        expected=p.prune(base); rng=random.Random(74945)
        for _ in range(100):
            sample=base[:]; rng.shuffle(sample); self.assertEqual(p.prune(sample),expected)
    def test_ghostedge_100_permutations_same_result(self):
        d=HiddenDependencyDetector(min_hits=2,min_ratio_milli=500)
        base=[PerturbationExperiment(f"e{i}","vault",("judge","view"),("judge",) if i%3 else ()) for i in range(12)]
        expected=d.detect(base,{}); rng=random.Random(74945)
        for _ in range(100):
            sample=base[:]; rng.shuffle(sample); self.assertEqual(d.detect(sample,{}),expected)

# ===== test_ghostedge.py =====
from frontier_assurance_lab import PerturbationExperiment, HiddenDependencyDetector
class GhostEdgeTests(unittest.TestCase):
    def test_detects_repeatable_undeclared_edge(self):
        d=HiddenDependencyDetector(min_hits=2,min_ratio_milli=750)
        ex=[PerturbationExperiment("e1","vault",("judge","ui"),("judge",)),PerturbationExperiment("e2","vault",("judge","ui"),("judge",))]
        r=d.detect(ex,{"judge":[]}); self.assertEqual(r["status"],"CANDIDATES_FOUND"); self.assertEqual((r["candidates"][0]["parent"],r["candidates"][0]["child"]),("vault","judge"))
    def test_declared_edge_not_reported(self):
        d=HiddenDependencyDetector(min_hits=1,min_ratio_milli=1); ex=[PerturbationExperiment("e1","vault",("judge",),("judge",))]
        self.assertEqual(d.detect(ex,{"judge":["vault"]})["status"],"CLEAN")
    def test_threshold_rejects_weak_signal(self):
        d=HiddenDependencyDetector(min_hits=2,min_ratio_milli=800)
        ex=[PerturbationExperiment("e1","a",("b",),("b",)),PerturbationExperiment("e2","a",("b",),("b",)),PerturbationExperiment("e3","a",("b",),())]
        self.assertEqual(d.detect(ex,{})["status"],"CLEAN")
    def test_deterministic_order(self):
        d=HiddenDependencyDetector(min_hits=1,min_ratio_milli=1); ex=[PerturbationExperiment("z","a",("b",),("b",)),PerturbationExperiment("a","a",("b",),("b",))]
        self.assertEqual(d.detect(ex,{}),d.detect(reversed(ex),{}))

# ===== test_muscle.py =====
from frontier_assurance_lab import Constraint, ConstraintEngine, FreezeError
class MuscleTests(unittest.TestCase):
    def setUp(self): self.engine=ConstraintEngine({"mode":["safe","fast","audit"]})
    def test_sat(self):
        r=self.engine.solve([Constraint("c1","mode","ALLOW",("safe","audit")),Constraint("c2","mode","NEQ",("audit",))])
        self.assertEqual(r["status"],"SAT"); self.assertEqual(r["final_domains"]["mode"],["safe"])
    def test_exact_minimum_core(self):
        r=self.engine.solve([Constraint("a","mode","EQ",("safe",)),Constraint("b","mode","EQ",("fast",)),Constraint("c","mode","DENY",("audit",))])
        self.assertEqual(r["status"],"UNSAT"); self.assertEqual(r["core_ids"],["a","b"])
    def test_deterministic_input_order(self):
        cs=[Constraint("b","mode","EQ",("fast",)),Constraint("a","mode","EQ",("safe",))]
        self.assertEqual(self.engine.solve(cs),self.engine.solve(reversed(cs)))
    def test_unknown_variable_freezes(self):
        with self.assertRaises(FreezeError): self.engine.solve([Constraint("x","missing","EQ",("v",))])

# ===== test_obsure.py =====
from frontier_assurance_lab import EffectSpec, TelemetryEventSpec, ObservabilityGate
BASE=("trace_id","action_id","effect_id","timestamp")
def events(eid,fields=BASE,reversible=False):
    phases=["INTENT","START","SUCCESS","FAILURE"]+(["COMPENSATION_START","COMPENSATION_RESULT"] if reversible else [])
    return [TelemetryEventSpec(f"{eid}-{p.lower()}",eid,p,tuple(fields)) for p in phases]
class ObsureTests(unittest.TestCase):
    def setUp(self): self.g=ObservabilityGate()
    def test_low_complete_passes(self): self.assertEqual(self.g.evaluate([EffectSpec("cache","LOW",False)],events("cache"))["status"],"PASS")
    def test_missing_phase_freezes(self): self.assertEqual(self.g.evaluate([EffectSpec("send","LOW",False)],events("send")[:-1])["status"],"FREEZE")
    def test_high_requires_provenance_fields(self):
        r=self.g.evaluate([EffectSpec("delete","HIGH",True)],events("delete",reversible=True)); fields=set()
        [fields.update(g.get("fields",[])) for g in r["gaps"]]; self.assertEqual(fields,{"authority_ref","evidence_ref"})
    def test_critical_complete_passes(self):
        f=BASE+("authority_ref","evidence_ref","state_digest"); self.assertEqual(self.g.evaluate([EffectSpec("deploy","CRITICAL",True)],events("deploy",f,True))["status"],"PASS")

# ===== test_parex.py =====
from frontier_assurance_lab import Plan, ParetoPruner
class ParexTests(unittest.TestCase):
    def setUp(self): self.p=ParetoPruner()
    def test_prunes_dominated(self):
        a=Plan("a",10,9,3,4,2); b=Plan("b",8,8,5,4,3); r=self.p.prune([b,a])
        self.assertEqual(r["frontier"],["a"]); self.assertEqual(r["pruned"]["b"]["reason"],"PARETO_DOMINATED")
    def test_keeps_tradeoff_frontier(self):
        a=Plan("cheap",6,6,1,3,2); b=Plan("strong",10,10,5,5,1)
        self.assertEqual(self.p.prune([a,b])["frontier"],["cheap","strong"])
    def test_hard_ineligible_removed(self):
        r=self.p.prune([Plan("x",100,100,0,0,0,False)])
        self.assertEqual(r["status"],"FREEZE")
    def test_equal_not_arbitrarily_tiebroken(self):
        a=Plan("a",1,1,1,1,1); b=Plan("b",1,1,1,1,1)
        self.assertEqual(self.p.prune([b,a])["frontier"],["a","b"])

# ===== test_pipeline.py =====
from frontier_assurance_lab import Constraint,Plan,PerturbationExperiment,RecoveryPolicy,EffectSpec,TelemetryEventSpec,FrontierAssurancePipeline
BASE=("trace_id","action_id","effect_id","timestamp")
class PipelineTests(unittest.TestCase):
    def telemetry(self): return [TelemetryEventSpec(f"write-{p.lower()}","write",p,BASE) for p in ("INTENT","START","SUCCESS","FAILURE")]
    def base(self): return dict(constraints=[Constraint("c1","mode","EQ",("safe",))],plans=[Plan("safe",10,10,3,4,1),Plan("worse",5,5,8,8,3)],experiments=[PerturbationExperiment("e1","vault",("judge",),()),PerturbationExperiment("e2","vault",("judge",),())],declared_dependencies={"judge":[]},before_state={"law":{"epoch":7}},after_state={"law":{"epoch":7}},recovery_policy=RecoveryPolicy(),effects=[EffectSpec("write","LOW",False)],telemetry=self.telemetry())
    def test_ready_uses_all_five(self):
        r=FrontierAssurancePipeline({"mode":["safe","fast"]}).assess(**self.base()); self.assertEqual(r["status"],"READY"); self.assertEqual(r["parex"]["frontier"],["safe"])
    def test_unsat_freezes(self):
        kw=self.base(); kw["constraints"]=[Constraint("a","mode","EQ",("safe",)),Constraint("b","mode","EQ",("fast",))]
        r=FrontierAssurancePipeline({"mode":["safe","fast"]}).assess(**kw); self.assertIn("UNSAT_CONSTRAINTS",r["reasons"])
    def test_hidden_dependency_freezes(self):
        kw=self.base(); kw["experiments"]=[PerturbationExperiment("e1","vault",("judge",),("judge",)),PerturbationExperiment("e2","vault",("judge",),("judge",))]
        r=FrontierAssurancePipeline({"mode":["safe","fast"]}).assess(**kw); self.assertIn("UNDECLARED_DEPENDENCY",r["reasons"])

# ===== test_recert.py =====
from frontier_assurance_lab import RecoveryPolicy, RecoveryCertifier
class ReCertTests(unittest.TestCase):
    def setUp(self): self.c=RecoveryCertifier()
    def test_exact_recovery(self): self.assertEqual(self.c.certify({"job":{"state":"ready"}},{"job":{"state":"ready"}},RecoveryPolicy())["status"],"CERTIFIED")
    def test_nondecreasing_counter(self):
        p=RecoveryPolicy(modes={"metrics.retries":"NONDECREASING"}); self.assertEqual(self.c.certify({"metrics":{"retries":2}},{"metrics":{"retries":3}},p)["status"],"CERTIFIED")
    def test_detects_semantic_mismatch(self):
        r=self.c.certify({"law":{"epoch":4}},{"law":{"epoch":3}},RecoveryPolicy()); self.assertEqual(r["status"],"FREEZE"); self.assertEqual(r["mismatches"][0]["path"],"law.epoch")
    def test_ignored_ephemeral_prefix(self):
        p=RecoveryPolicy(ignore_prefixes=("runtime.temp",)); self.assertEqual(self.c.certify({"runtime":{"temp":{"pid":1}},"x":1},{"runtime":{"temp":{"pid":9}},"x":1},p)["status"],"CERTIFIED")
