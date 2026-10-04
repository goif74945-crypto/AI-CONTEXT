import itertools,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from critical_path_scheduler import ScheduleInputError,WorkItem,schedule_work

class CriticalPathSchedulerTests(unittest.TestCase):
 def test_dependencies_and_resource_capacity(self):
  tasks=[WorkItem("design",5,"agent",produces_evidence=1),WorkItem("implement",10,"agent",("design",),1),WorkItem("unit",7,"test",("implement",),2,1),WorkItem("audit",3,"agent",("unit",),2,2)]
  r=schedule_work(tasks,{"agent":2,"test":1}); self.assertEqual(r.status,"PLAN_READY"); b={s.task_id:s for s in r.schedule}
  self.assertGreaterEqual(b["implement"].start_ms,b["design"].end_ms); self.assertGreaterEqual(b["unit"].start_ms,b["implement"].end_ms); self.assertGreaterEqual(b["audit"].start_ms,b["unit"].end_ms)
 def test_critical_path_priority_for_same_ready_time(self):
  r=schedule_work([WorkItem("short",2,"agent"),WorkItem("long",5,"agent"),WorkItem("long_tail",10,"test",("long",))],{"agent":1,"test":1}); b={s.task_id:s for s in r.schedule}
  self.assertEqual(b["long"].start_ms,0); self.assertGreaterEqual(b["short"].start_ms,b["long"].end_ms)
 def test_parallel_slots_overlap_independent_work(self):
  r=schedule_work([WorkItem("a",10,"agent"),WorkItem("b",10,"agent")],{"agent":2}); self.assertEqual(r.makespan_ms,10); self.assertEqual({s.start_ms for s in r.schedule},{0})
 def test_future_ready_high_priority_task_does_not_create_artificial_idle(self):
  r=schedule_work([WorkItem("remote_gate",100,"remote"),WorkItem("future_critical",10,"agent",("remote_gate",)),WorkItem("local_now",50,"agent")],{"remote":1,"agent":1}); b={s.task_id:s for s in r.schedule}
  self.assertEqual((b["local_now"].start_ms,b["local_now"].end_ms,b["future_critical"].start_ms,r.makespan_ms),(0,50,100,110))
 def test_planned_evidence_gap_freezes(self):
  r=schedule_work([WorkItem("producer",1,"agent",produces_evidence=1),WorkItem("consumer",1,"agent",("producer",),requires_dependency_evidence=2)],{"agent":1}); self.assertEqual(r.status,"FREEZE"); self.assertIn("PLANNED_EVIDENCE_GAP",r.reason_codes)
 def test_cycle_rejected(self):
  with self.assertRaises(ScheduleInputError): schedule_work([WorkItem("a",1,"agent",("b",)),WorkItem("b",1,"agent",("a",))],{"agent":1})
 def test_permutation_invariant_fingerprint(self):
  tasks=[WorkItem("a",3,"agent"),WorkItem("b",4,"agent"),WorkItem("c",5,"test",("a","b"))]; self.assertEqual(len({schedule_work(p,{"agent":2,"test":1}).fingerprint for p in itertools.permutations(tasks)}),1)
 def test_missing_capacity_rejected(self):
  with self.assertRaises(ScheduleInputError): schedule_work([WorkItem("a",1,"gpu")],{"agent":1})
if __name__=="__main__": unittest.main()
