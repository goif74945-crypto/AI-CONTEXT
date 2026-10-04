from __future__ import annotations

import json
from pathlib import Path

from ncif.engine import evaluate_consensus
from ncif.models import ConsensusPolicy


def deep_lineage_case(depth: int) -> dict:
    evidence = []
    for i in range(depth):
        evidence_id = f"n{i:05d}"
        parents = [] if i == depth - 1 else [f"n{i+1:05d}"]
        evidence.append(
            {
                "evidence_id": evidence_id,
                "kind": "runtime" if not parents else "derived",
                "source_identity": "deep-root" if not parents else f"derived:{i}",
                "parents": parents,
                "correlation_keys": [],
            }
        )
    return {
        "claim_id": "stress-deep-lineage",
        "evidence": evidence,
        "votes": [{"actor_id": "actor", "stance": "SUPPORT", "evidence_ids": ["n00000"], "correlation_keys": []}],
    }


def wide_case(root_count: int, clone_factor: int) -> dict:
    evidence = [
        {
            "evidence_id": f"r{i}",
            "kind": "runtime",
            "source_identity": f"source:{i}",
            "parents": [],
            "correlation_keys": [],
        }
        for i in range(root_count)
    ]
    votes = []
    for i in range(root_count):
        for j in range(clone_factor):
            votes.append(
                {
                    "actor_id": f"actor-{i}-{j}",
                    "stance": "SUPPORT",
                    "evidence_ids": [f"r{i}"],
                    "correlation_keys": [],
                }
            )
    return {"claim_id": "stress-wide", "evidence": evidence, "votes": votes}


def main() -> int:
    failures: list[str] = []
    deep = evaluate_consensus(deep_lineage_case(5000), ConsensusPolicy(min_support_groups=1))
    if deep.decision != "CONSENSUS_CANDIDATE" or deep.support_groups[0].root_evidence_ids != ("n04999",):
        failures.append("deep-lineage")

    wide = evaluate_consensus(wide_case(500, 10), ConsensusPolicy(min_support_groups=500))
    if wide.decision != "CONSENSUS_CANDIDATE" or wide.support_group_count != 500:
        failures.append("wide-clone-collapse")

    report = {
        "audit": "NCIF_STRESS_AUDIT",
        "status": "PASS" if not failures else "FAIL",
        "deep_lineage_nodes": 5000,
        "wide_unique_roots": 500,
        "wide_votes": 5000,
        "observed_wide_support_groups": wide.support_group_count,
        "failures": failures,
        "limitations": [
            "Local structural stress only; no production latency/SLO claim.",
            "Does not prove correctness for unbounded graph sizes or hostile memory exhaustion.",
        ],
    }
    path = Path(__file__).resolve().parents[1] / "evidence" / "stress-audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
