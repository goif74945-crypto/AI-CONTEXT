from __future__ import annotations
import copy, importlib.util, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'conformance'/'multichannel_equivalence.py'
S=importlib.util.spec_from_file_location('multichannel_equivalence',P); assert S and S.loader
m=importlib.util.module_from_spec(S); sys.modules['multichannel_equivalence']=m; S.loader.exec_module(m)
ROLES=['OWNER','OPERATOR','AUDITOR','SYSTEM','PUBLIC_USER']
CASES=[('INIT','OK'),('READY','OK'),('RUNNING','OK'),('VERIFYING','OK'),('CONSENSUS','OK'),('STABLE','OK'),('STABLE','DEGRADED'),('FREEZE','FREEZE'),('STOP','STOP')]

def b(state,status):
 x={'status':status,'state':state,'request_id':'req','trace_id':'trace','data':{}}
 if state=='STABLE': x['data']={'accepted':True,'releaseable':True,'integrity_hash':'hash'}
 if state=='FREEZE': x['freeze']={'recoverable':True}
 return x

def s(state,status,role):
 x={'displayed_status':status,'displayed_state':state,'headline':state,'summary':'Authoritative state.','result_visible':False,'result':None,'actions':[],'request_id':'req','trace_id':'trace'}
 if state=='STABLE': x.update(result_visible=True,result={'ok':True},headline='Verified result')
 if state=='FREEZE' and role=='OWNER': x['actions']=[{'id':'recover','kind':'MUTATION_REQUEST','requires_backend_authorization':True,'requires_confirmation':True}]
 if state=='READY' and role in {'OWNER','OPERATOR'}: x['actions']=[{'id':'new_directive','kind':'MUTATION_REQUEST','requires_backend_authorization':True}]
 return x

def main():
 clean=inj=caught=0; failures=[]
 for state,status in CASES:
  for role in ROLES:
   base=s(state,status,role); surfaces={k:copy.deepcopy(base) for k in ['visual','aria','mobile','export']}; back=b(state,status)
   if m.audit_channels(back,surfaces,role).conformant: clean+=1
   else: failures.append(('clean',state,status,role))
   mutations=[]
   x=copy.deepcopy(surfaces); x['aria']['trace_id']='wrong'; mutations.append((x,'CHANNEL_TRACE_ID_DIVERGENCE'))
   x=copy.deepcopy(surfaces); x['mobile']['displayed_state']='READY' if state!='READY' else 'RUNNING'; mutations.append((x,'CHANNEL_DISPLAYED_STATE_DIVERGENCE'))
   x=copy.deepcopy(surfaces); x['export']['actions']=[{'id':'foreign','kind':'READ','requires_backend_authorization':True}]; mutations.append((x,'CHANNEL_ACTION_DIVERGENCE'))
   for specimen,expected in mutations:
    inj+=1; got={v.code for v in m.audit_channels(back,specimen,role).cross_channel_violations}
    if expected in got: caught+=1
    else: failures.append((state,status,role,expected,sorted(got)))
 print({'clean_cases':clean,'injected_cross_channel_defects':inj,'caught':caught,'failures':len(failures)})
 if failures:
  print(failures[:20]); return 1
 return 0
if __name__=='__main__': raise SystemExit(main())
