import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from scoped_authority_lease import *

class TestSALE(unittest.TestCase):
    def lease(self): return Lease("user","agent","drive.write",("project/*",),("create","update"),100,200,3)
    def test_authorized(self):
        l=self.lease(); self.assertEqual(authorize(l,now=150,subject="agent",capability="drive.write",resource="project/a",action="create",uses=0)["status"],"PASS")
    def test_expired_freezes(self):
        l=self.lease(); self.assertEqual(authorize(l,now=200,subject="agent",capability="drive.write",resource="project/a",action="create",uses=0)["status"],"FREEZE")
    def test_usage_exhaustion_freezes(self):
        l=self.lease(); self.assertEqual(authorize(l,now=150,subject="agent",capability="drive.write",resource="project/a",action="create",uses=3)["status"],"FREEZE")
    def test_child_cannot_escalate(self):
        p=self.lease(); c=Lease("agent","sub","drive.write",("project/*",),("create","delete"),120,190,2,p.lease_id())
        self.assertEqual(validate_child(p,c)["status"],"FREEZE")
    def test_child_narrowing_passes(self):
        p=self.lease(); c=Lease("agent","sub","drive.write",("project/a",),("create",),120,190,2,p.lease_id())
        self.assertEqual(validate_child(p,c)["status"],"PASS")

    def test_revoked_freezes(self):
        l=self.lease(); self.assertEqual(authorize(l,now=150,subject="agent",capability="drive.write",resource="project/a",action="create",uses=0,revoked_ids={l.lease_id()})["status"],"FREEZE")

    def test_resource_escape_freezes(self):
        l=self.lease(); self.assertEqual(authorize(l,now=150,subject="agent",capability="drive.write",resource="other/a",action="create",uses=0)["status"],"FREEZE")

    def test_child_expiry_escalation_freezes(self):
        p=self.lease(); c=Lease("agent","sub","drive.write",("project/a",),("create",),120,210,2,p.lease_id())
        self.assertEqual(validate_child(p,c)["status"],"FREEZE")

if __name__=='__main__': unittest.main()
