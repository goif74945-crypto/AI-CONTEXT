from __future__ import annotations

import hashlib
import json

from .artifact import ArtifactFile, ConsumerProfile, evaluate as evaluate_artifact
from .capability import Capability, CompositionRequest, compose
from .mastery import MasteryRequest, SkillNode, compile_path
from .outcome import ObjectiveContract, WorkItem, analyze
from .supply_chain import Dependency, TrustPolicy, audit


def build_demo_report() -> dict:
    objective = analyze(
        ObjectiveContract("ship-report", ("correct", "usable"), ("NEXY.AI-",)),
        (
            WorkItem("verify", ("correct",), "lab/verify"),
            WorkItem("package", ("usable",), "lab/package", ("verify",)),
        ),
    )

    capabilities = compose(
        CompositionRequest(frozenset({"text"}), "pdf", frozenset({"internal"}), frozenset({"read", "write-output"}), 5, 8),
        (
            Capability("render-markdown", "AVAILABLE", frozenset({"text"}), frozenset({"markdown"}), frozenset({"internal"}), frozenset({"read"}), 1, 1),
            Capability("render-pdf", "AVAILABLE", frozenset({"markdown"}), frozenset({"pdf"}), frozenset({"internal"}), frozenset({"write-output"}), 1, 2),
        ),
    )

    payload = b"verified artifact\n"
    artifact = evaluate_artifact(
        ConsumerProfile("pdf-consumer", frozenset({"report.pdf"}), frozenset({"application/pdf"}), frozenset({"title"}), frozenset({"SECRET"}), 1024),
        (ArtifactFile("report.pdf", "application/pdf", payload, hashlib.sha256(payload).hexdigest()),),
        {"title": "Report"},
    )

    supply_chain = audit(
        TrustPolicy(frozenset({"internal-registry"}), frozenset({"VERIFIED"}), frozenset({"read"}), frozenset()),
        (Dependency("renderer", "1.2.3", "internal-registry", "a" * 64, True, "VERIFIED", frozenset({"read"}), frozenset()),),
    )

    mastery = compile_path(
        MasteryRequest("operate", frozenset({"basics"}), 5),
        (
            SkillNode("basics", (), "Understand one-output/freeze rule", "Can distinguish PASS from FREEZE"),
            SkillNode("verify", ("basics",), "Inspect evidence status", "Can identify missing evidence"),
            SkillNode("operate", ("verify",), "Run an authorized task", "Completes guided dry run"),
        ),
    )

    return {
        "goal_contribution_graph": objective,
        "verified_capability_composer": capabilities,
        "artifact_consumer_fitness_gate": artifact,
        "supply_chain_trust_gate": supply_chain,
        "mastery_path_compiler": mastery,
    }


def main() -> None:
    print(json.dumps(build_demo_report(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
