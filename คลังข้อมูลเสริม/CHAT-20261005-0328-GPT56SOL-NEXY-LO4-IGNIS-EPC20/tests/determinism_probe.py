from lo4_epc20 import Q64, SYSTEM_IDS, canonical_digest, evaluate
H='a'*64; H2='b'*64
cases={
'S01':{'destructive':True,'reversible':True,'rollback_proof':H},
'S02':{'wait_ticks':{'b':10,'a':5},'min_fairness_q64':Q64.from_ratio(1,2).raw},
'S03':{'excluded_features':['blockchain'],'requested_features':['audit']},
'S04':{'attempt':2,'retry_budget':3,'side_effect_free':False,'idempotency_proven':True,'prior_effect_unknown':True},
'S05':{'preconditions':[{'id':'p','satisfied':True,'disclosed':True}]},
'S06':{'current_tick':5,'warning_tick':8,'expiry_tick':10,'user_warned':False},
'S07':{'revocation_requested':True,'active_handles':['a','b'],'revoked_handles':['b','a']},
'S08':{'code':'E','blocking_layer':'LAW','recoverable':True,'remediation':'refresh evidence'},
'S09':{'component_statuses':['PASS','PASS'],'reported_status':'PASS'},
'S10':{'internal_state':'FREEZE','visible_state':'FREEZE'},
'S11':{'server_only':True,'config':{'OPENAI_API_KEY':'INJECT_AT_RUNTIME'}},
'S12':{'owned_ids':['a','b'],'exported_ids':['a'],'excluded':{'b':'deleted'}},
'S13':{'declared':['audit'],'verified':['vault','audit']},
'S14':{'duplicate':True,'key':'k','original_intent_hash':H,'replay_intent_hash':H,'original_result_hash':H2,'replay_result_hash':H2,'user_feedback':'REPLAYED'},
'S15':{'limited':True,'current_tick':10,'retry_after_ticks':5,'unlock_tick':15,'user_disclosed':True},
'S16':{'events':[{'sequence':1,'request_id':'r','trace_id':'t','correlation_id':'c'},{'sequence':2,'request_id':'r','trace_id':'t','correlation_id':'c'}]},
'S17':{'cancel_requested':True,'components':{'worker':'STOPPED','queue':'CANCELLED'},'side_effects_after_cancel':[]},
'S18':{'stale':True,'expired':True,'user_status':'EXPIRED','side_effect_after_expiry':False},
'S19':{'required_evidence':[H2,H],'explained_evidence':[H,H2]},
'S20':{'reasons':['TIMEOUT','EVIDENCE_MISSING','SECURITY_BREACH']}}
print(canonical_digest([evaluate(s,cases[s]).to_dict() for s in SYSTEM_IDS]))
