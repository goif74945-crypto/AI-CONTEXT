from __future__ import annotations

import itertools
import json
from pathlib import Path

from ncif.engine import evaluate_consensus
from ncif.models import ConsensusPolicy


def evidence(root_ids: tuple[str, ...]) -> list[dict]:
    return [
        {
            "evidence_id": rid,
            "kind": "runtime",
            "source_identity": f"source:{rid}",
            "parents": [],
            "correlation_keys": [],
        }
        for rid in root_ids
    ]


def vote(actor: str, root_id: str, key: str | None) -> dict:
    return {
        "actor_id": actor,
        "stance": "SUPPORT",
        "evidence_ids": [root_id],
        "correlation_keys": [] if key is None else [key],
    }


def main() -> int:
    roots = ("r0", "r1", "r2")
    correlation_options = (None, "shared:a", "shared:b")
    checked = 0
    failures: list[dict] = []

    for root_assignment in itertools.product(roots, repeat=4):
        for key_assignment in itertools.product(correlation_options, repeat=4):
            votes = [vote(f"actor-{i}", root_assignment[i], key_assignment[i]) for i in range(4)]
            data = {"claim_id": "bounded-audit", "evidence": evidence(roots), "votes": votes}
            result = evaluate_consensus(data, ConsensusPolicy(min_support_groups=1))
            checked += 1

            if not (1 <= result.support_group_count <= 4):
                failures.append({"type": "GROUP_COUNT_RANGE", "roots": root_assignment, "keys": key_assignment})
                continue

            reversed_result = evaluate_consensus(
                {"claim_id": "bounded-audit", "evidence": list(reversed(evidence(roots))), "votes": list(reversed(votes))},
                ConsensusPolicy(min_support_groups=1),
            )
            if result.to_dict() != reversed_result.to_dict():
                failures.append({"type": "ORDER_INVARIANCE", "roots": root_assignment, "keys": key_assignment})

            clone_votes = votes + [vote("clone", root_assignment[0], key_assignment[0])]
            clone_result = evaluate_consensus(
                {"claim_id": "bounded-audit", "evidence": evidence(roots), "votes": clone_votes},
                ConsensusPolicy(min_support_groups=1),
            )
            if clone_result.support_group_count != result.support_group_count:
                failures.append({"type": "CLONE_INFLATION", "roots": root_assignment, "keys": key_assignment})

    report = {
        "audit": "NCIF_BOUNDED_CORRELATION_MATRIX",
        "checked_cases": checked,
        "assertion_failures": len(failures),
        "status": "PASS" if not failures else "FAIL",
        "failure_examples": failures[:20],
        "limitations": [
            "Bounded deterministic matrix, not exhaustive over arbitrary graph size.",
            "Tests structural independence declarations, not truth of external evidence itself.",
        ],
    }
    out = Path(__file__).resolve().parents[1] / "evidence" / "bounded-audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
