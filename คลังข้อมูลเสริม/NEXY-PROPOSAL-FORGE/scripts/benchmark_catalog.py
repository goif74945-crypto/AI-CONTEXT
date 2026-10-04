from __future__ import annotations

import json
import time

from nexy_proposal_forge.canon import canonical_json
from nexy_proposal_forge.engine import evaluate_proposal
from nexy_proposal_forge.models import Proposal


def make_proposal(index: int) -> Proposal:
    return Proposal.from_dict(
        {
            "proposal_id": f"BENCH-{index:04d}",
            "version": "0.0.0",
            "status": "AI_PROPOSED_CONCEPT",
            "title": f"Synthetic benchmark proposal {index}",
            "summary": "Synthetic deterministic benchmark fixture.",
            "problem": f"Synthetic benchmark problem domain {index} for catalog scaling.",
            "intended_users": ["benchmark"],
            "user_outcomes": [f"Measure catalog comparison path {index}"],
            "proposed_capabilities": [f"Capability {index}", f"Capability group {index % 17}"],
            "integration_surfaces": [f"surface-{index % 23}"],
            "non_goals": ["represent real NEXY requirements"],
            "risks": ["synthetic data cannot establish production performance"],
            "assumptions": [],
            "authority_references": ["synthetic-benchmark-only"],
            "evidence": [
                {
                    "ref_id": f"AUTH-{index}",
                    "role": "AUTHORITY",
                    "truth_class": "SOURCE_FACT",
                    "claim": "Synthetic benchmark fixture authority marker.",
                    "locator": "synthetic",
                },
                {
                    "ref_id": f"DUP-{index}",
                    "role": "DUPLICATE_CHECK",
                    "truth_class": "REPO_FACT",
                    "claim": "Synthetic benchmark duplicate-check marker.",
                    "locator": "synthetic",
                },
            ],
            "authority_conflicts": [],
        }
    )


def main() -> None:
    catalog = tuple(make_proposal(index) for index in range(837))
    candidate = Proposal.from_dict(
        {
            **make_proposal(9_999).to_dict(),
            "proposal_id": "BENCH-CANDIDATE",
            "title": "Distinct benchmark candidate",
        }
    )

    start = time.perf_counter_ns()
    first = evaluate_proposal(candidate, catalog)
    elapsed_ns = time.perf_counter_ns() - start
    second = evaluate_proposal(candidate, catalog)

    payload = {
        "catalog_size": len(catalog),
        "elapsed_ns_observation": elapsed_ns,
        "deterministic_repeat": canonical_json(first.to_dict()) == canonical_json(second.to_dict()),
        "recommendation": first.recommendation,
        "top_overlap_count": len(first.top_overlaps),
        "note": "Local synthetic observation only; not a production SLA or NEXY runtime claim.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
