from nexy_mvk import (
    Case,
    Observation,
    VerificationEngine,
    deterministic_replay,
    evidence_removal_safety,
    irrelevant_context_invariance,
    permission_reduction_monotonicity,
)
from nexy_mvk.report import report_to_dict
import json


def simulated_control_adapter(case: Case) -> Observation:
    has_write = "write" in case.permissions
    has_proof = "proof" in case.evidence
    released = has_proof and bool(case.permissions)
    effects = ("read", "write") if has_write and released else (("read",) if released else ())
    return Observation(
        status="PASS" if released else "FREEZE",
        released=released,
        payload={"decision": "release" if released else "freeze"},
        side_effects=effects,
        evidence=case.evidence,
    )


seed = Case(
    prompt="Execute the verified read/write operation.",
    context={"resource": "demo"},
    permissions=frozenset({"read", "write"}),
    evidence=("proof", "trace"),
)
relations = [
    deterministic_replay(),
    irrelevant_context_invariance(key="irrelevant_note", value="does-not-affect-policy"),
    permission_reduction_monotonicity(remove={"write"}),
    evidence_removal_safety(remove={"proof"}),
]
report = VerificationEngine(simulated_control_adapter).run(seed, relations, run_id="example-integration")
print(json.dumps(report_to_dict(report), sort_keys=True, ensure_ascii=False))
raise SystemExit(0 if report.passed else 1)
