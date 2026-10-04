import unittest
from lo4_epc20 import I128_MAX, Q64, SYSTEM_IDS, NumericFault, canonical_digest, evaluate
H="a"*64; H2="b"*64

class Lo4FinalTests(unittest.TestCase):
    def ok(self,s,p):
        d=evaluate(s,p); self.assertEqual(d.status,"PASS",(s,d)); return d
    def no(self,s,p,r=None):
        d=evaluate(s,p); self.assertEqual(d.status,"FREEZE",(s,d));
        if r:self.assertEqual(d.reason,r)
        return d
    def test_numeric_law(self):
        self.assertEqual(Q64.from_ratio(1,2).raw,1<<63)
        self.assertEqual(Q64.from_ratio(1,2).serialize(),f"q64:{1<<63}")
        with self.assertRaises(NumericFault):Q64.from_ratio(1,0)
        with self.assertRaises(NumericFault):Q64.from_raw(I128_MAX+1)
        with self.assertRaises(NumericFault):Q64.from_raw(I128_MAX).mul(Q64.from_int(2))
    def test_all_systems(self):
        self.assertEqual(len(SYSTEM_IDS),20); self.assertEqual(len(set(SYSTEM_IDS)),20)
    def test_s01(self):
        self.ok("S01",{"destructive":True,"reversible":True,"rollback_proof":H}); self.no("S01",{"destructive":True,"reversible":False,"rollback_proof":""},"IRREVERSIBLE_ACTION")
    def test_s02(self):
        t=Q64.from_ratio(1,2).raw; self.ok("S02",{"wait_ticks":{"a":5,"b":10},"min_fairness_q64":t}); self.no("S02",{"wait_ticks":{"a":1,"b":10},"min_fairness_q64":t},"QUEUE_FAIRNESS_LOW")
        for high in range(2,30):
            low=(high+1)//2; self.ok("S02",{"wait_ticks":{"a":low,"b":high},"min_fairness_q64":t}); self.no("S02",{"wait_ticks":{"a":low-1,"b":high},"min_fairness_q64":t})
    def test_s03(self):
        self.ok("S03",{"requested_features":["audit"],"excluded_features":["blockchain"]}); self.no("S03",{"requested_features":["blockchain"],"excluded_features":["blockchain"]},"NON_GOAL_CREEP")
    def test_s04(self):
        self.ok("S04",{"attempt":2,"retry_budget":3,"side_effect_free":False,"idempotency_proven":True,"prior_effect_unknown":True}); self.no("S04",{"attempt":2,"retry_budget":3,"side_effect_free":False,"idempotency_proven":False,"prior_effect_unknown":True},"AMBIGUOUS_RETRY_HARM"); self.no("S04",{"attempt":4,"max_attempts":3,"side_effect_free":True,"idempotency_proven":False,"prior_effect":"NONE"},"RETRY_BUDGET_EXCEEDED")
    def test_s05(self):
        self.ok("S05",{"preconditions":[{"id":"p","satisfied":True,"disclosed":True}]}); self.no("S05",{"preconditions":[{"id":"p","satisfied":True,"disclosed":False}]},"PRECONDITION_HIDDEN")
    def test_s06(self):
        self.ok("S06",{"current_tick":5,"warning_tick":8,"expiry_tick":10,"user_warned":False}); self.no("S06",{"current_tick":8,"warning_tick":8,"expiry_tick":10,"user_warned":False},"EXPIRY_NOT_DISCLOSED"); self.no("S06",{"current_tick":10,"warning_tick":8,"expiry_tick":10,"user_warned":True},"SESSION_EXPIRED")
    def test_s07(self):
        self.ok("S07",{"revocation_requested":True,"active_handles":["a","b"],"revoked_handles":["a","b"]}); self.no("S07",{"revocation_requested":True,"active_handles":["a","b"],"revoked_handles":["a"]},"REVOCATION_INCOMPLETE")
    def test_s08(self):
        p={"code":"E","blocking_layer":"LAW","recoverable":True,"remediation":"refresh evidence"}; self.assertEqual(self.ok("S08",p).metrics["actionability_q64"],Q64.ONE.serialize()); p["remediation"]=""; self.no("S08",p,"ERROR_NOT_ACTIONABLE")
    def test_s09(self):
        self.ok("S09",{"component_statuses":["PASS","PASS"],"reported_status":"PASS"}); self.no("S09",{"component_statuses":["PASS","FREEZE"],"reported_status":"OK"},"PARTIAL_SUCCESS_MISREPORTED")
    def test_s10(self):
        self.ok("S10",{"internal_state":"FREEZE","visible_state":"FREEZE"}); self.no("S10",{"internal_state":"FREEZE","visible_state":"STABLE"},"STATE_DISCLOSURE_MISMATCH")
    def test_s11(self):
        self.ok("S11",{"server_only":True,"config":{"OPENAI_API_KEY":"INJECT_AT_RUNTIME"}}); self.no("S11",{"server_only":True,"config":{"OPENAI_API_KEY":"sk-live-secret"}},"SECRET_LITERAL_PRESENT")
    def test_s12(self):
        self.ok("S12",{"owned_ids":["a","b"],"exported_ids":["a"],"excluded":{"b":"user_deleted"}}); self.no("S12",{"owned_ids":["a","b"],"exported_ids":["a"],"excluded":{}},"OWNERSHIP_EXPORT_INCOMPLETE")
    def test_s13(self):
        self.assertEqual(self.ok("S13",{"declared":["audit"],"verified":["audit","vault"]}).metrics["claim_coverage_q64"],Q64.ONE.serialize()); self.no("S13",{"declared":["audit","voice"],"verified":["audit"]},"UNVERIFIED_CAPABILITY_CLAIM")
    def test_s14(self):
        p={"duplicate":True,"key":"k","original_intent_hash":H,"replay_intent_hash":H,"original_result_hash":H2,"replay_result_hash":H2,"user_feedback":"REPLAYED"}; self.ok("S14",p); p["replay_intent_hash"]=H2; self.no("S14",p,"IDEMPOTENCY_INTENT_CONFLICT")
    def test_s15(self):
        self.ok("S15",{"limited":True,"current_tick":10,"retry_after_ticks":5,"unlock_tick":15,"user_disclosed":True}); self.no("S15",{"limited":True,"current_tick":10,"retry_after_ticks":5,"unlock_tick":14,"user_disclosed":True},"RATE_LIMIT_RECOVERY_INCONSISTENT")
    def test_s16(self):
        ev=[{"sequence":1,"request_id":"r","trace_id":"t","correlation_id":"c","event":"A"},{"sequence":2,"request_id":"r","trace_id":"t","correlation_id":"c","event":"B"}]; self.ok("S16",{"events":ev}); ev[1]["sequence"]=1; self.no("S16",{"events":ev},"AUDIT_SEQUENCE_INVALID")
    def test_s17(self):
        self.ok("S17",{"cancel_requested":True,"components":{"queue":"CANCELLED","worker":"STOPPED"},"side_effects_after_cancel":[]}); self.no("S17",{"cancel_requested":True,"components":{"queue":"CANCELLED","worker":"STOPPED"},"side_effect_after_cancel":True},"POST_CANCEL_SIDE_EFFECT")
    def test_s18(self):
        self.ok("S18",{"stale":True,"expired":True,"user_status":"EXPIRED","side_effect_after_expiry":False}); self.no("S18",{"stale":True,"expired":True,"user_status":"","side_effect_after_expiry":False},"STALE_JOB_UNDISCLOSED")
    def test_s19(self):
        self.assertEqual(self.ok("S19",{"required_evidence":[H,H2],"explained_evidence":[H2,H]}).metrics["coverage_q64"],Q64.ONE.serialize()); self.no("S19",{"required_evidence":[H,H2],"explained_evidence":[H]},"EVIDENCE_EXPLANATION_LOSS"); self.no("S19",{"required_evidence":[H],"explained_evidence":[H,H2]},"EVIDENCE_EXPLANATION_INVENTED")
    def test_s20(self):
        a=self.ok("S20",{"reasons":["TIMEOUT","SECURITY_BREACH","EVIDENCE_MISSING"]}); b=self.ok("S20",{"reasons":["EVIDENCE_MISSING","TIMEOUT","SECURITY_BREACH"]}); self.assertEqual(a.selected_reason,"SECURITY_BREACH"); self.assertEqual(a.evidence_root,b.evidence_root); self.no("S20",{"reasons":["TIMEOUT","MAGIC"]},"UNKNOWN_REASON")
    def test_fail_closed(self):
        for sid in SYSTEM_IDS:
            self.assertEqual(evaluate(sid,{"bad":object()}).status,"FREEZE")
            self.assertEqual(evaluate(sid,{"value":0.1}).reason,"BINARY_FLOAT_FORBIDDEN")
    def test_key_order_determinism(self):
        a=evaluate("S03",{"requested_features":["audit"],"excluded_features":["blockchain"]}); b=evaluate("S03",{"excluded_features":["blockchain"],"requested_features":["audit"]}); self.assertEqual(a.evidence_root,b.evidence_root); self.assertEqual(canonical_digest(a.to_dict()),canonical_digest(b.to_dict()))
if __name__=="__main__":unittest.main()
