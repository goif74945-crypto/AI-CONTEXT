from __future__ import annotations

import json
import time

from nexy_intent_guard import evaluate_proposal, semantic_digest


def build_contract(n: int) -> dict:
    requirements = [
        {"id": f"REQ-{i:04d}", "text": f"Synthetic requirement {i}", "kind": "must", "immutable": i < 10}
        for i in range(n)
    ]
    criteria = [
        {
            "id": f"AC-{i:04d}",
            "text": f"Synthetic criterion {i}",
            "minimum_evidence": "unit",
            "requirement_ids": [f"REQ-{i:04d}"],
        }
        for i in range(n)
    ]
    return {
        "schema_version": "0.1",
        "contract_id": f"synthetic-{n}",
        "objective": "Synthetic scalability benchmark; not project truth.",
        "scope": {
            "in_scope": ["bench/**"],
            "out_of_scope": [],
            "protected": [],
            "allowed_repositories": ["synthetic/bench"],
            "protected_repositories": ["*NEXY.AI*"],
        },
        "requirements": requirements,
        "acceptance_criteria": criteria,
        "stop_conditions": ["Freeze on any invariant violation."],
        "unknowns": [],
        "assumptions": [],
    }


def build_proposal(n: int) -> dict:
    return {
        "proposal_id": f"synthetic-proposal-{n}",
        "target_repository": "synthetic/bench",
        "touch_paths": ["bench/output.json"],
        "covered_requirement_ids": [f"REQ-{i:04d}" for i in range(n)],
        "evidence": {f"AC-{i:04d}": "unit" for i in range(n)},
        "resolved_unknowns": [],
        "claims": [],
    }


def main() -> None:
    sizes = (100, 500, 1000)
    observations = []
    for n in sizes:
        contract = build_contract(n)
        proposal = build_proposal(n)
        start = time.perf_counter()
        digest = semantic_digest(contract)
        digest_seconds = time.perf_counter() - start

        start = time.perf_counter()
        report = evaluate_proposal(contract, proposal)
        evaluate_seconds = time.perf_counter() - start

        observations.append({
            "synthetic_requirements": n,
            "decision": report.decision.value,
            "digest_prefix": digest[:16],
            "digest_seconds": digest_seconds,
            "evaluate_seconds": evaluate_seconds,
        })

    print(json.dumps({"note": "Local synthetic observation only; not a performance guarantee.", "results": observations}, indent=2))


if __name__ == "__main__":
    main()
