from __future__ import annotations

import platform
import time

from lo4lab.aurora import AbstentionCase, AbstentionPolicy, AgentAction, evaluate_abstention
from lo4lab.contract_drift import analyze_contract_drift
from lo4lab.margin import Constraint, Operator, evaluate_constraints
from lo4lab.traceweight import InfluenceGraph, InfluenceNode
from lo4lab.upa import EvidenceValue, TruthState


def bench(name, iterations, fn):
    start = time.perf_counter()
    for _ in range(iterations):
        fn()
    elapsed = time.perf_counter() - start
    print(f"{name}: iterations={iterations} elapsed_s={elapsed:.6f} ops_per_s={iterations/elapsed:.2f}")


cases = [
    AbstentionCase("a", True, AgentAction.ANSWER, True, 0.99),
    AbstentionCase("b", False, AgentAction.ABSTAIN),
    AbstentionCase("c", True, AgentAction.ANSWER, True, 0.95),
]
policy = AbstentionPolicy(max_unsafe_answer_rate=0.0, min_reliability_score=0.99)
constraints = [
    Constraint("risk", "0.01", Operator.LE, "0.1", scale="1", required_margin="0.05"),
    Constraint("confidence", "0.98", Operator.GE, "0.9", scale="1", required_margin="0.05"),
]
graph = InfluenceGraph([
    InfluenceNode("a", {}, True, True),
    InfluenceNode("b", {}, True, True),
    InfluenceNode("c", {}, True, True),
    InfluenceNode("merge", {"a": 1, "b": 1, "c": 1}),
    InfluenceNode("final", {"merge": 1}),
])
base = {
    "authorized_scope": ["read", "prototype"],
    "success_invariants": ["safe", "tests"],
    "forbidden_actions": ["write-nexy"],
    "assumptions": [],
    "required_evidence": ["e2", "readback"],
}
t = EvidenceValue(TruthState.TRUE, ("a",))
u = EvidenceValue(TruthState.UNKNOWN, ("b",))

print("environment:", platform.python_version(), platform.platform())
bench("AURORA", 30000, lambda: evaluate_abstention(cases, policy))
bench("MARGIN", 50000, lambda: evaluate_constraints(constraints))
bench("UPA", 250000, lambda: t.logical_and(u).knowledge_join(t).negate())
bench("TRACEWEIGHT", 20000, lambda: graph.analyze("final"))
bench("CONTRACT_DRIFT", 50000, lambda: analyze_contract_drift(base, base))
