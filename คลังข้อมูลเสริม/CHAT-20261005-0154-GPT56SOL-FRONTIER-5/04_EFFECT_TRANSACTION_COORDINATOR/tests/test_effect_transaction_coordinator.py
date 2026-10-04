import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from effect_transaction_coordinator import *

class TestETC(unittest.TestCase):
    def test_happy_path(self):
        xs=[Action("a","k1",True,{},{}),Action("b","k2",False,{},None,"approval:1")]
        r=execute_plan(xs,lambda a:True,lambda a:True)
        self.assertEqual(r["status"],"PASS")
    def test_failure_compensates_reverse(self):
        xs=[Action("a","k1",True,{},{}),Action("b","k2",True,{},{}),Action("c","k3",True,{},{})]
        order=[]
        r=execute_plan(xs,lambda a:a.action_id!="c",lambda a:order.append(a.action_id) is None or True)
        self.assertEqual(r["status"],"ROLLBACK_COMPLETE"); self.assertEqual(order,["b","a"])
    def test_irreversible_without_approval_freezes_before_commit(self):
        calls=[]; xs=[Action("delete","k",False)]
        r=execute_plan(xs,lambda a:calls.append(a.action_id) or True,lambda a:True)
        self.assertEqual(r["status"],"FREEZE"); self.assertEqual(calls,[])
    def test_uncompensated_residue_freezes(self):
        xs=[Action("a","k1",True,{},{}),Action("b","k2",True,{},{})]
        r=execute_plan(xs,lambda a:a.action_id!="b",lambda a:False)
        self.assertEqual(r["status"],"FREEZE"); self.assertEqual(r["residual_effects"],["a"])

    def test_duplicate_idempotency_rejected(self):
        xs=[Action("a","k",True,{},{}),Action("b","k",True,{},{})]
        with self.assertRaises(ValueError): execute_plan(xs,lambda a:True,lambda a:True)

    def test_reversible_without_compensation_freezes_prepare(self):
        calls=[]; xs=[Action("a","k",True,{},None)]
        r=execute_plan(xs,lambda a:calls.append(a.action_id) or True,lambda a:True)
        self.assertEqual(r["status"],"FREEZE"); self.assertEqual(calls,[])

if __name__=='__main__': unittest.main()
