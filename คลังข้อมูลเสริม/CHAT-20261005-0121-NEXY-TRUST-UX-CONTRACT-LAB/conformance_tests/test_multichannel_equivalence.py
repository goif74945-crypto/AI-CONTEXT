from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'conformance'/'multichannel_equivalence.py'
SPEC=importlib.util.spec_from_file_location('multichannel_equivalence',PATH)
assert SPEC and SPEC.loader
m=importlib.util.module_from_spec(SPEC)
sys.modules['multichannel_equivalence']=m
SPEC.loader.exec_module(m)


def backend(state='READY',status='OK'):
    b={'status':status,'state':state,'request_id':'req','trace_id':'trace','data':{}}
    if state=='STABLE': b['data']={'accepted':True,'releaseable':True,'integrity_hash':'hash'}
    if state=='FREEZE': b['freeze']={'recoverable':True}
    return b


def surface(state='READY',status='OK',role='OPERATOR'):
    s={'displayed_status':status,'displayed_state':state,'headline':state,'summary':'Authoritative state.','result_visible':False,'result':None,'actions':[],'request_id':'req','trace_id':'trace'}
    if state=='STABLE': s.update(result_visible=True,result={'ok':True},headline='Verified result')
    if state=='FREEZE' and role=='OWNER': s['actions']=[{'id':'recover','kind':'MUTATION_REQUEST','requires_backend_authorization':True,'requires_confirmation':True}]
    if state=='READY' and role in {'OWNER','OPERATOR'}: s['actions']=[{'id':'new_directive','kind':'MUTATION_REQUEST','requires_backend_authorization':True}]
    return s


def channels(state='READY',status='OK',role='OPERATOR'):
    x=surface(state,status,role)
    return {k:copy.deepcopy(x) for k in ['visual','aria','mobile','export']}


def xcodes(report): return {v.code for v in report.cross_channel_violations}


class MultiChannelTests(unittest.TestCase):
    def test_four_identical_channels_pass(self):
        self.assertTrue(m.audit_channels(backend(),channels(), 'OPERATOR').conformant)

    def test_state_divergence_detected(self):
        c=channels(); c['aria']['displayed_state']='RUNNING'
        r=m.audit_channels(backend(),c,'OPERATOR')
        self.assertIn('CHANNEL_DISPLAYED_STATE_DIVERGENCE',xcodes(r))

    def test_status_divergence_detected(self):
        c=channels(); c['mobile']['displayed_status']='DEGRADED'
        self.assertIn('CHANNEL_DISPLAYED_STATUS_DIVERGENCE',xcodes(m.audit_channels(backend(),c,'OPERATOR')))

    def test_result_visibility_divergence_detected(self):
        c=channels(); c['export']['result_visible']=True; c['export']['result']={'x':1}
        self.assertIn('CHANNEL_RESULT_VISIBLE_DIVERGENCE',xcodes(m.audit_channels(backend(),c,'OPERATOR')))

    def test_request_identity_divergence_detected(self):
        c=channels(); c['aria']['request_id']='other'
        self.assertIn('CHANNEL_REQUEST_ID_DIVERGENCE',xcodes(m.audit_channels(backend(),c,'OPERATOR')))

    def test_trace_identity_divergence_detected(self):
        c=channels(); c['aria']['trace_id']='other'
        self.assertIn('CHANNEL_TRACE_ID_DIVERGENCE',xcodes(m.audit_channels(backend(),c,'OPERATOR')))

    def test_action_divergence_detected(self):
        c=channels(); c['mobile']['actions']=[]
        self.assertIn('CHANNEL_ACTION_DIVERGENCE',xcodes(m.audit_channels(backend(),c,'OPERATOR')))

    def test_individual_channel_violation_fails_whole_report(self):
        b=backend('FREEZE','FREEZE'); c=channels('FREEZE','FREEZE','OWNER'); c['aria']['headline']='Successful'
        r=m.audit_channels(b,c,'OWNER')
        self.assertFalse(r.conformant)
        self.assertIn('FREEZE_SUCCESS_COPY',{v['code'] for v in r.per_channel_reports['aria']['violations']})

    def test_freeze_owner_channels_can_pass(self):
        self.assertTrue(m.audit_channels(backend('FREEZE','FREEZE'),channels('FREEZE','FREEZE','OWNER'),'OWNER').conformant)

    def test_stable_channels_can_pass(self):
        self.assertTrue(m.audit_channels(backend('STABLE'),channels('STABLE'),'OPERATOR').conformant)

    def test_stop_channels_can_pass(self):
        self.assertTrue(m.audit_channels(backend('STOP','STOP'),channels('STOP','STOP'),'OWNER').conformant)

    def test_empty_channels_fail_closed(self):
        with self.assertRaises(Exception): m.audit_channels(backend(),{},'OPERATOR')

    def test_deterministic_certificate(self):
        a=m.audit_channels(backend(),channels(),'OPERATOR')
        b=m.audit_channels(backend(),channels(),'OPERATOR')
        self.assertEqual(a.to_dict(),b.to_dict())

    def test_certificate_changes_on_channel_drift(self):
        a=m.audit_channels(backend(),channels(),'OPERATOR')
        c=channels(); c['aria']['trace_id']='other'
        b=m.audit_channels(backend(),c,'OPERATOR')
        self.assertNotEqual(a.certificate_fingerprint,b.certificate_fingerprint)

    def test_action_order_does_not_create_false_divergence(self):
        c=channels('FREEZE','FREEZE','OWNER')
        extra={'id':'view_trace','kind':'READ','requires_backend_authorization':True}
        for name in c: c[name]['actions'].append(copy.deepcopy(extra))
        c['aria']['actions']=list(reversed(c['aria']['actions']))
        self.assertTrue(m.audit_channels(backend('FREEZE','FREEZE'),c,'OWNER').conformant)


if __name__=='__main__': unittest.main(verbosity=2)
