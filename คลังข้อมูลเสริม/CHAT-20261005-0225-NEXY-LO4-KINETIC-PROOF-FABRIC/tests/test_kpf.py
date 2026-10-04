import ast, inspect, itertools, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import kinetic_proof_fabric as k

Q=k.Q; q=k.q

def S(name,val,unc='0.1',trust='0.9',age='0',max_age='1'):
    return k.Sensor(name,q(val),q(unc),q(trust),q(age),q(max_age))

def H(x='0'): return k.Hazard(q(x),q(x),q(x))

def hp(decay='1',cap='10'): return k.HazardPolicy(H(decay),H(cap))

def env(**kw):
    d=dict(speed_limit=q('10'),force_limit=q('10'),acceleration_limit=q('10'),max_deceleration=q('5'),reaction_time=q('0.1'),boundary_min=q('-100'),boundary_max=q('100'),margin=q('1'))
    d.update(kw); return k.Envelope(**d)

class FixedTests(unittest.TestCase):
    def test_int_roundtrip(self): self.assertEqual(Q.i(-7).raw, -7*k.SCALE)
    def test_decimal_exact_prefix(self): self.assertEqual(Q.s('1.5').raw, k.SCALE+k.SCALE//2)
    def test_float_forbidden(self):
        with self.assertRaises(TypeError): q(1.25)
    def test_bool_forbidden(self):
        with self.assertRaises(TypeError): q(True)
    def test_div_zero(self):
        with self.assertRaises(ZeroDivisionError): _=q(1)/q(0)
    def test_overflow(self):
        with self.assertRaises(k.QOverflow): Q(k.MAX_RAW)+Q(1)
    def test_negative_mul(self): self.assertEqual((q('-2')*q('3')).raw,q('-6').raw)
    def test_trunc_toward_zero(self): self.assertEqual((q('-1')/q('3')).raw,-(k.SCALE//3))
    def test_no_float_literal_in_decision_source(self):
        tree=ast.parse(inspect.getsource(k))
        floats=[n for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,float)]
        self.assertEqual(floats,[])

class PSTLTests(unittest.TestCase):
    def setUp(self): self.p=k.PSTL(q('0.5'),q('0.6'),2)
    def test_consensus(self):
        r=self.p.fuse([S('a','5'),S('b','5.05'),S('c','20')]); self.assertEqual(r.decision,'PASS'); self.assertEqual(r.sources,('a','b'))
    def test_stale_excluded(self):
        r=self.p.fuse([S('a','5'),S('b','5',age='2'),S('c','5')]); self.assertEqual(r.decision,'PASS'); self.assertIn('STALE:b',r.reasons)
    def test_low_trust_excluded(self):
        r=self.p.fuse([S('a','5'),S('b','5',trust='0.1'),S('c','5')]); self.assertEqual(r.decision,'PASS')
    def test_duplicate_freeze(self): self.assertEqual(self.p.fuse([S('a','1'),S('a','1')]).decision,'FREEZE')
    def test_quorum_freeze(self): self.assertEqual(self.p.fuse([S('a','1'),S('b','10')]).decision,'FREEZE')
    def test_order_independent(self):
        xs=[S('a','5'),S('b','5.05'),S('c','20')]
        sigs={(self.p.fuse(p).decision,self.p.fuse(p).value.raw if self.p.fuse(p).value else None,self.p.fuse(p).sources) for p in itertools.permutations(xs)}
        self.assertEqual(len(sigs),1)
    def test_large_fanin(self):
        xs=[S(f'g{i}','7',unc='0.2') for i in range(200)]+[S(f'o{i}',str(50+i)) for i in range(10)]
        r=self.p.fuse(xs); self.assertEqual(r.decision,'PASS'); self.assertEqual(len(r.sources),200)

class WMDSTests(unittest.TestCase):
    def test_pass(self): self.assertEqual(k.WMDS(q('1'),q('2')).evaluate({'x':q('1')},{'x':q('1.4')},{'x':q('1')}).decision,'PASS')
    def test_soft_exact_is_caution(self): self.assertEqual(k.WMDS(q('1'),q('2')).evaluate({'x':q('0')},{'x':q('1')},{'x':q('1')}).decision,'CAUTION')
    def test_hard_exact_is_freeze(self): self.assertEqual(k.WMDS(q('1'),q('2')).evaluate({'x':q('0')},{'x':q('2')},{'x':q('1')}).decision,'FREEZE')
    def test_missing_axis(self): self.assertEqual(k.WMDS(q('1'),q('2')).evaluate({'x':q('0')},{},{'x':q('1')}).decision,'FREEZE')
    def test_bad_thresholds(self):
        with self.assertRaises(k.QError): k.WMDS(q('2'),q('2'))

class AEPETests(unittest.TestCase):
    def setUp(self): self.a=k.AEPE()
    def test_pass(self): self.assertEqual(self.a.prove(k.KState(q('0'),q('1')),k.Actuation(q('1'),q('1'),q('1'),q('10')),env()).decision,'PASS')
    def test_speed_limit(self): self.assertIn('SPEED_LIMIT',self.a.prove(k.KState(q('0'),q('0')),k.Actuation(q('11'),q('1'),q('2'),q('100')),env()).reasons)
    def test_force_limit(self): self.assertIn('FORCE_LIMIT',self.a.prove(k.KState(q('0'),q('0')),k.Actuation(q('1'),q('11'),q('1'),q('100')),env()).reasons)
    def test_boundary(self): self.assertIn('BOUNDARY',self.a.prove(k.KState(q('99'),q('0')),k.Actuation(q('2'),q('1'),q('1'),q('100')),env()).reasons)
    def test_current_speed_used_for_braking_regression(self):
        r=self.a.prove(k.KState(q('0'),q('9')),k.Actuation(q('1'),q('1'),q('1'),q('3')),env(acceleration_limit=q('20')))
        self.assertIn('INSUFFICIENT_STOPPING_CLEARANCE',r.reasons)
    def test_stopping_monotonic_current_speed(self):
        ds=[]
        for v in range(1,9): ds.append(self.a.prove(k.KState(q('0'),q(v)),k.Actuation(q('1'),q('0'),q('1'),q('100')),env(acceleration_limit=q('20'))).stopping_distance.raw)
        self.assertEqual(ds,sorted(ds))

class CHITests(unittest.TestCase):
    def test_pass_commit(self):
        r=k.CHI().step(H('1'),H('1'),hp()); self.assertEqual(r.decision,'PASS'); self.assertEqual(r.committed,r.proposed)
    def test_freeze_transactional(self):
        c=H('9'); r=k.CHI().step(c,H('2'),hp()); self.assertEqual(r.decision,'FREEZE'); self.assertEqual(r.committed,c)
    def test_accumulation_catches_sequence(self):
        chi=k.CHI(); cur=H('0'); pol=hp(decay='1',cap='3')
        for _ in range(3):
            r=chi.step(cur,H('1'),pol); self.assertEqual(r.decision,'PASS'); cur=r.committed
        r=chi.step(cur,H('1'),pol); self.assertEqual(r.decision,'FREEZE'); self.assertEqual(r.committed,cur)
    def test_bad_decay(self):
        with self.assertRaises(k.QError): k.CHI().step(H(),H(),k.HazardPolicy(H('1.1'),H('10')))

class RHPVTests(unittest.TestCase):
    def setUp(self): self.r=k.RHPV(); self.h='0'*64
    def test_safe_pass(self):
        s=k.HState(1,0,False,self.h); c=k.Command('SAFE','ACTUATE',1,1,q('1'),q('2'),self.h); self.assertEqual(self.r.evaluate(s,c,q('1')).decision,'PASS')
    def test_replay_freeze(self):
        s=k.HState(1,2,False,self.h); c=k.Command('SAFE','ACTUATE',1,2,q('1'),q('2'),self.h); self.assertEqual(self.r.evaluate(s,c,q('1')).decision,'FREEZE')
    def test_expired_freeze(self):
        s=k.HState(1,0,False,self.h); c=k.Command('SAFE','ACTUATE',1,1,q('0'),q('1'),self.h); self.assertEqual(self.r.evaluate(s,c,q('2')).decision,'FREEZE')
    def test_reflex_latches(self):
        s=k.HState(1,0,False,self.h); c=k.Command('REFLEX','STOP',1,1,q('1'),q('2'),self.h); rr=self.r.evaluate(s,c,q('1')); self.assertTrue(rr.state.reflex_latched)
    def test_latch_blocks_safe(self):
        s=k.HState(1,1,True,self.h); c=k.Command('SAFE','ACTUATE',1,2,q('1'),q('2'),self.h); self.assertIn('REFLEX_LATCH_ACTIVE',self.r.evaluate(s,c,q('1')).reasons)
    def test_state_hash_binding(self):
        s=k.HState(1,0,False,self.h); c=k.Command('SAFE','ACTUATE',1,1,q('1'),q('2'),'f'*64); self.assertIn('STATE_BINDING_MISMATCH',self.r.evaluate(s,c,q('1')).reasons)
    def test_reset_advances_exactly_one(self):
        s=k.HState(1,1,True,self.h); self.assertFalse(self.r.reset(s,2,'f'*64).reflex_latched)
        with self.assertRaises(ValueError): self.r.reset(s,3,'f'*64)

class PipelineTests(unittest.TestCase):
    def base(self):
        pstl=k.PSTL(q('0.5'),q('0.6'),2); w=k.WMDS(q('1'),q('2')); fabric=k.KineticProofFabric(pstl,w)
        ps=[S('p1','0'),S('p2','0')]; vs=[S('v1','1'),S('v2','1')]
        ph=pstl.fuse(ps).value; vh=pstl.fuse(vs).value; hs=k.HState(1,0,False,k.state_hash(ph,vh))
        kw=dict(position_samples=ps,velocity_samples=vs,predicted_position=q('0'),predicted_velocity=q('1'),position_tolerance=q('1'),velocity_tolerance=q('1'),request=k.Actuation(q('1'),q('1'),q('1'),q('10')),envelope=env(),current_hazard=H('0'),impulse=H('1'),hazard_policy=hp(),handoff=hs,epoch=1,sequence=1,now=q('1'),lease_until=q('2'))
        return fabric,kw
    def test_complete_pass(self): f,x=self.base(); self.assertEqual(f.evaluate(**x).decision,'PASS')
    def test_sensor_conflict_freezes(self): f,x=self.base(); x['position_samples']=[S('a','0'),S('b','20')]; self.assertEqual(f.evaluate(**x).decision,'FREEZE')
    def test_model_divergence_freezes(self): f,x=self.base(); x['predicted_velocity']=q('10'); self.assertEqual(f.evaluate(**x).decision,'FREEZE')
    def test_envelope_freezes(self): f,x=self.base(); x['request']=k.Actuation(q('11'),q('1'),q('2'),q('100')); self.assertEqual(f.evaluate(**x).decision,'FREEZE')
    def test_hazard_freeze_does_not_commit(self): f,x=self.base(); x['current_hazard']=H('9'); x['impulse']=H('2'); r=f.evaluate(**x); self.assertEqual(r.decision,'FREEZE'); self.assertEqual(r.hazard,H('9'))
    def test_stale_handoff_freezes(self): f,x=self.base(); x['handoff']=k.HState(1,0,False,'f'*64); self.assertEqual(f.evaluate(**x).decision,'FREEZE')

if __name__=='__main__': unittest.main()
