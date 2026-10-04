from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_provenance_taint import (  # noqa: E402
    ProvenanceEngine,
    ReleasePolicy,
    SourceSpec,
    Taint,
    decision_to_record,
)


def main() -> None:
    engine = ProvenanceEngine()
    policy = ReleasePolicy(
        policy_id="demo-release",
        min_authority_rank=50,
        required_assurances=frozenset({"verified", "schema:valid"}),
        forbidden_taints=frozenset(Taint),
        max_age_epochs=5,
    )

    candidate = engine.source(
        "candidate answer",
        SourceSpec(
            origin_id="model:candidate-1",
            source_kind="model-candidate",
            authority_rank=60,
            epoch=100,
        ),
    )
    before = engine.release_decision(candidate, policy, current_epoch=100)

    receipt = engine.issue_verification(
        candidate,
        verifier_id="trusted-verifier-boundary",
        added_assurances={"verified", "schema:valid"},
        cleared_taints={Taint.UNVERIFIED},
        issued_epoch=100,
        expires_epoch=105,
    )
    verified = engine.apply_verification(candidate, receipt, current_epoch=100)
    after = engine.release_decision(verified, policy, current_epoch=100)

    print(json.dumps({"before": decision_to_record(before), "after": decision_to_record(after)}, indent=2))


if __name__ == "__main__":
    main()
