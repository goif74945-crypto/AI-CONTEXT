from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def main() -> None:
    ick = load("ick_smoke", "01-invariant-conservation-kernel/src/ick.py")
    mfwr = load("mfwr_smoke", "02-minimal-failure-witness-reducer/src/mfwr.py")
    esc = load("esc_smoke", "03-epistemic-saturation-controller/src/esc.py")
    eecp = load("eecp_smoke", "04-exact-evidence-cut-planner/src/eecp.py")
    uis = load("uis_smoke", "05-unknown-impact-slicer/src/uis.py")

    before = ick.Snapshot.build(authority_level=1, evidence_level=1, constraints=["law"], capabilities=["read"])
    after = ick.Snapshot.build(authority_level=1, evidence_level=1, constraints=["law"], capabilities=["read"])
    assert ick.evaluate_transition(before, after).status == "PASS"

    reduced = mfwr.reduce_failure(["noise", "boom", "tail"], lambda xs: "boom" in xs)
    assert reduced.witness == ("boom",)

    rounds = [
        esc.Round.build(round_id="r1", contributions=[esc.Contribution.build(agent_id="a1", independence_domain="p", claim_ids=["C"])]),
        esc.Round.build(round_id="r2", contributions=[esc.Contribution.build(agent_id="a2", independence_domain="p", claim_ids=["C"])]),
    ]
    assert esc.analyze_rounds(rounds, patience=1, min_rounds=2).status == "SATURATED"

    graph = eecp.EvidenceGraph([eecp.Evidence("E", 1), eecp.Claim("C", "OR", ("E",))])
    assert graph.plan_acquisition("C").required_new_evidence == ("E",)

    model = uis.ImpactModel([uis.Variable.build("x", [0, 1])], [], default_output="SAME")
    assert model.analyze().status == "STABLE"

    print("INTEGRATION_SMOKE_PASS: 5/5 modules imported and representative contracts executed")


if __name__ == "__main__":
    main()
