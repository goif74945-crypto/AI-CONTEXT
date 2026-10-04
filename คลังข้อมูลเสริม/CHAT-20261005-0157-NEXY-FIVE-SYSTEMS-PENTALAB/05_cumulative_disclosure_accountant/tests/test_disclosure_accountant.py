import itertools,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from disclosure_accountant import DisclosureEvent,DisclosureInputError,DisclosureItem,DisclosurePolicy,LedgerState,evaluate_disclosure

class DisclosureAccountantTests(unittest.TestCase):
 def catalog(self): return [DisclosureItem("email","identity",2,"identity"),DisclosureItem("phone","identity",2,"identity"),DisclosureItem("city","location",2,"location"),DisclosureItem("street","location",4,"location"),DisclosureItem("pref","behavior",1,"behavior")]
 def policy(self): return DisclosurePolicy(10,(("identity",4),("location",5)),8000)
 def test_individually_safe_events_can_fail_cumulatively(self):
  r1=evaluate_disclosure(self.catalog(),LedgerState(),DisclosureEvent("e1","model-A","task",("city",)),self.policy()); self.assertEqual(r1.status,"ALLOW")
  r2=evaluate_disclosure(self.catalog(),r1.next_state,DisclosureEvent("e2","model-A","task",("street",)),self.policy()); self.assertEqual(r2.status,"FREEZE"); self.assertIn("CATEGORY_BUDGET_EXCEEDED:location",r2.reason_codes); self.assertEqual(r2.next_state,r1.next_state)
 def test_duplicate_item_does_not_consume_budget_twice(self):
  r1=evaluate_disclosure(self.catalog(),LedgerState(),DisclosureEvent("e1","A","p",("email",)),self.policy()); r2=evaluate_disclosure(self.catalog(),r1.next_state,DisclosureEvent("e2","A","p",("email",)),self.policy()); self.assertEqual(r2.projected_audience_points,2); self.assertEqual(r2.newly_disclosed_items,())
 def test_audiences_are_isolated(self):
  r1=evaluate_disclosure(self.catalog(),LedgerState(),DisclosureEvent("e1","A","p",("email","phone")),self.policy()); r2=evaluate_disclosure(self.catalog(),r1.next_state,DisclosureEvent("e2","B","p",("email","phone")),self.policy()); self.assertNotEqual(r2.status,"FREEZE"); self.assertEqual(r2.projected_audience_points,4)
 def test_near_limit_requires_review(self):
  policy=DisclosurePolicy(10,(("identity",10),("location",10)),7000); r=evaluate_disclosure(self.catalog(),LedgerState(),DisclosureEvent("e1","A","p",("email","phone","city","pref")),policy); self.assertEqual(r.status,"REVIEW"); self.assertIn("CUMULATIVE_BUDGET_NEAR_LIMIT",r.reason_codes)
 def test_review_is_preflight_and_does_not_mutate_ledger(self):
  policy=DisclosurePolicy(10,(("identity",10),("location",10)),7000); state=LedgerState(); r=evaluate_disclosure(self.catalog(),state,DisclosureEvent("e1","A","p",("email","phone","city","pref")),policy); self.assertEqual(r.status,"REVIEW"); self.assertEqual(r.next_state,state); self.assertNotIn("e1",r.next_state.accepted_events)
 def test_linkability_concentration_blocks(self):
  policy=DisclosurePolicy(10,(("identity",10),("location",10)),9000); r=evaluate_disclosure(self.catalog(),LedgerState(),DisclosureEvent("e1","A","p",("city","street")),policy); self.assertEqual(r.status,"FREEZE"); self.assertIn("LINKABILITY_CONCENTRATION:location",r.reason_codes)
 def test_catalog_order_does_not_change_receipt(self):
  catalog=self.catalog(); receipts=set()
  for p in itertools.permutations(catalog[:3]): receipts.add(evaluate_disclosure(list(p)+catalog[3:],LedgerState(),DisclosureEvent("e","A","p",("email","city")),self.policy()).receipt_hash)
  self.assertEqual(len(receipts),1)
 def test_event_replay_rejected(self):
  r=evaluate_disclosure(self.catalog(),LedgerState(),DisclosureEvent("e","A","p",("pref",)),self.policy())
  with self.assertRaises(DisclosureInputError): evaluate_disclosure(self.catalog(),r.next_state,DisclosureEvent("e","A","p",("city",)),self.policy())
if __name__=="__main__": unittest.main()
