from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_provenance_taint import ProvenanceEngine, ReleasePolicy, SourceSpec, TransformContract  # noqa: E402


def main() -> None:
    engine = ProvenanceEngine()
    artifact = engine.source(
        "root",
        SourceSpec(
            origin_id="bench:root",
            source_kind="bench",
            authority_rank=100,
            assurance_tags=frozenset({"verified"}),
            epoch=0,
        ),
    )
    contract = TransformContract(
        contract_id="bench-step",
        preserved_assurances=frozenset({"verified"}),
    )
    policy = ReleasePolicy(
        policy_id="bench-policy",
        min_authority_rank=1,
        required_assurances=frozenset({"verified"}),
        forbidden_taints=frozenset(),
    )

    transforms = 20_000
    start = time.perf_counter()
    for i in range(transforms):
        artifact = engine.derive(str(i), [artifact], contract, epoch=i + 1)
    transform_seconds = time.perf_counter() - start

    decisions = 50_000
    start = time.perf_counter()
    for _ in range(decisions):
        decision = engine.release_decision(artifact, policy, current_epoch=transforms)
        if not decision.allowed:
            raise RuntimeError(decision)
    decision_seconds = time.perf_counter() - start

    print(f"transforms={transforms}")
    print(f"transform_seconds={transform_seconds:.6f}")
    print(f"transforms_per_second={transforms / transform_seconds:.2f}")
    print(f"decisions={decisions}")
    print(f"decision_seconds={decision_seconds:.6f}")
    print(f"decisions_per_second={decisions / decision_seconds:.2f}")
    print(f"final_artifact_id={artifact.artifact_id}")


if __name__ == "__main__":
    main()
