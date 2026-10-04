import random, unittest
from epistemic_integrity import *

class ReferenceTests(unittest.TestCase):
    def test_ecof_pass_cycle_unknown(self):
        e=EpistemicCircularityFirewall()
        self.assertEqual(e.audit([ClaimNode('a',('e:x',)),ClaimNode('b',('c:a',))],{'x'}).status,'PASS')
        self.assertEqual(e.audit([ClaimNode('a',('c:b',)),ClaimNode('b',('c:a',))],set()).status,'FREEZE')
        self.assertEqual(e.audit([ClaimNode('a',('e:missing',))],set()).status,'FREEZE')

    def test_dmag_monotonic_conflict_and_input_validation(self):
        a=DecisionMonotonicityAuditor(); r=MonotonicityRule('risk','NONINCREASING',('FREEZE','REVIEW','RELEASE'))
        good=[DecisionObservation('0',{'risk':0},'RELEASE'),DecisionObservation('1',{'risk':1},'REVIEW'),DecisionObservation('2',{'risk':2},'FREEZE')]
        self.assertEqual(a.audit(good,r).status,'PASS')
        self.assertEqual(a.audit([DecisionObservation('0',{'risk':0},'REVIEW'),DecisionObservation('1',{'risk':1},'RELEASE')],r).status,'FREEZE')
        with self.assertRaises(ValueError): a.audit([DecisionObservation('x',{'risk':float('nan')},'FREEZE')],r)
        with self.assertRaises(ValueError): a.audit([DecisionObservation('x',{'risk':0},'FREEZE'),DecisionObservation('x',{'risk':1},'FREEZE')],r)

    def test_pdza_dead_zones_and_budget(self):
        p=PolicyDeadZoneAnalyzer(100)
        out=p.analyze({'tier':('free','pro'),'risk':(0,1)},[
            PolicyRule('deny',100,{'risk':1},'DENY'),
            PolicyRule('shadow',90,{'tier':'free','risk':1},'DENY'),
            PolicyRule('allow',50,{'tier':'pro'},'ALLOW'),
            PolicyRule('unreachable',1,{'tier':'enterprise'},'ALLOW')],'REVIEW')
        self.assertIn('unreachable',out.unreachable_rules); self.assertIn('shadow',out.shadowed_rules); self.assertIn('allow',out.live_rules)
        self.assertEqual(PolicyDeadZoneAnalyzer(2).analyze({'x':(0,1),'y':(0,1)},[], 'DENY').status,'FREEZE')

    def test_rkm_exact_boundary_reuse(self):
        m=RefutationKnowledgeMemory(); m.add(RefutationEntry('h','s','p','a','cex',('e1',),10))
        self.assertEqual(m.lookup('h','s','p','a',5).status,'REFUTED')
        self.assertEqual(m.lookup('h','s','p2','a',5).reason,'PREMISE_DRIFT')
        self.assertEqual(m.lookup('h','s','p','a2',5).reason,'AUTHORITY_DRIFT')
        self.assertEqual(m.lookup('h','s','p','a',11).reason,'STALE_REFUTATION')

    def test_ace_closure(self):
        a=AssumptionClosureEngine()
        blocked=a.audit({'a':('fact:f','assume:q'),'b':('claim:a',)},{'f'},{'q'},set(),('b',))
        self.assertEqual(blocked.status,'BLOCKED'); self.assertEqual(blocked.assumptions_by_claim['b'],('q',))
        self.assertEqual(a.audit({'a':('fact:f',)},{'f'},set(),set(),('a',)).status,'PASS')

    def test_advisory_gate(self):
        c=EpistemicCircularityFirewall().audit([ClaimNode('c',('e:e',))],{'e'})
        m=DecisionMonotonicityAuditor().audit([DecisionObservation('x',{'risk':0},'RELEASE')],MonotonicityRule('risk','NONINCREASING',('FREEZE','RELEASE')))
        p=PolicyDeadZoneAnalyzer().analyze({'risk':(0,1)},[PolicyRule('deny',10,{'risk':1},'DENY'),PolicyRule('allow',5,{'risk':0},'ALLOW')],'REVIEW')
        a=AssumptionClosureEngine().audit({'c':('fact:f',)},{'f'},set(),set(),('c',))
        r=RefutationKnowledgeMemory().lookup('h','s','p','a',0)
        self.assertEqual(AdvisoryIntegrityGate().evaluate(c,m,p,a,r,{'deny','allow'}).status,'READY')

class DeterminismProperties(unittest.TestCase):
    def test_order_invariance_500_iterations(self):
        rng=random.Random(20261005)
        ecof=EpistemicCircularityFirewall(); claims=[ClaimNode('a',('e:e',)),ClaimNode('b',('c:a',))]; expected=ecof.audit(claims,{'e'})
        for _ in range(100):
            x=list(claims); rng.shuffle(x); self.assertEqual(ecof.audit(x,{'e'}),expected)
        rule=MonotonicityRule('risk','NONINCREASING',('FREEZE','REVIEW','RELEASE')); obs=[DecisionObservation('0',{'risk':0},'RELEASE'),DecisionObservation('1',{'risk':1},'REVIEW'),DecisionObservation('2',{'risk':2},'FREEZE')]; expected2=DecisionMonotonicityAuditor().audit(obs,rule)
        for _ in range(100):
            x=list(obs); rng.shuffle(x); self.assertEqual(DecisionMonotonicityAuditor().audit(x,rule),expected2)
        rules=[PolicyRule('a',10,{'x':0},'ALLOW'),PolicyRule('b',10,{'x':1},'DENY')]; expected3=PolicyDeadZoneAnalyzer().analyze({'x':(0,1)},rules,'REVIEW')
        for _ in range(100):
            x=list(rules); rng.shuffle(x); self.assertEqual(PolicyDeadZoneAnalyzer().analyze({'x':(0,1)},x,'REVIEW'),expected3)
        entries=[RefutationEntry('h','s1','p1','a','c1',('e1',),10),RefutationEntry('h','s2','p2','a','c2',('e2',),10)]
        for _ in range(100):
            x=list(entries); rng.shuffle(x); mem=RefutationKnowledgeMemory(); [mem.add(e) for e in x]; self.assertEqual(mem.lookup('h','s2','p2','a',0).counterexample,'c2')
        pairs=[('a',('fact:f',)),('b',('claim:a','assume:q'))]
        for _ in range(100):
            x=list(pairs); rng.shuffle(x); self.assertEqual(AssumptionClosureEngine().audit(dict(x),{'f'},{'q'},set(),('b',)).assumptions_by_claim['b'],('q',))

if __name__=='__main__': unittest.main(verbosity=2)
