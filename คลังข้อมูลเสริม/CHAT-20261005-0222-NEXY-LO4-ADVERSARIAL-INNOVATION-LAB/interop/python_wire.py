import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lo4lab.aurora import AbstentionCase, AbstentionPolicy, AgentAction, evaluate_abstention
from lo4lab.contract_drift import analyze_contract_drift
from lo4lab.margin import Constraint, Operator, evaluate_constraints
from lo4lab.traceweight import InfluenceGraph, InfluenceNode
from lo4lab.upa import EvidenceValue, TruthState

fixture = json.loads((Path(__file__).with_name("fixture.json")).read_text())

a = fixture["aurora"]
policy = AbstentionPolicy(
    max_unsafe_answer_rate=a["policy"]["max_unsafe_answer_rate"],
    min_reliability_score=a["policy"]["min_reliability_score"],
    max_brier_score=a["policy"]["max_brier_score"],
)
cases = [
    AbstentionCase(
        x["case_id"], x["answerable"], AgentAction(x["action"]),
        x.get("correct"), x.get("confidence"), x.get("risk_weight", 1.0),
    )
    for x in a["cases"]
]
aurora = evaluate_abstention(cases, policy)

margin = evaluate_constraints([
    Constraint(x["name"], x["actual"], Operator(x["operator"]), x["limit"], x["scale"], x["required_margin"])
    for x in fixture["margin"]["constraints"]
])

u = fixture["upa"]
upa = EvidenceValue(TruthState(u["left"]["state"]), tuple(u["left"]["provenance"])).knowledge_join(
    EvidenceValue(TruthState(u["right"]["state"]), tuple(u["right"]["provenance"]))
)

t = fixture["traceweight"]
graph = InfluenceGraph([
    InfluenceNode(x["node_id"], x["parents"], x["is_agent_source"], x["verified"])
    for x in t["nodes"]
])
trace = graph.analyze(t["target"])

d = fixture["contract_drift"]
drift = analyze_contract_drift(d["before"], d["after"])

out = {
    "aurora": {"status": aurora.status, "unsafe_answer_rate": round(aurora.unsafe_answer_rate, 12)},
    "margin": {"release_status": margin.release_status, "minimum_margin": round(float(margin.minimum_margin), 12)},
    "upa": {"state": upa.state.value, "releaseable": upa.releaseable},
    "traceweight": {"status": trace.status, "dominant_source": trace.dominant_source, "dominance_ratio": round(trace.dominance_ratio, 12)},
    "contract_drift": {"status": drift.status, "total_cost": drift.total_cost},
}
print(json.dumps(out, sort_keys=True, separators=(",", ":")))
