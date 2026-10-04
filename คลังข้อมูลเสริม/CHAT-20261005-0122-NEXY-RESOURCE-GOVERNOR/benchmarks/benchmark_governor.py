from __future__ import annotations

import argparse
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import AgentProfile, DataClass, ResourceGovernor, RiskTier, TaskProfile  # noqa: E402


def agent(index: int, role: str) -> AgentProfile:
    return AgentProfile(
        agent_id=f"{role}-{index:04d}",
        provider_domain=f"provider-{index % 17}",
        roles=frozenset({role}),
        capabilities=frozenset({"code"}),
        clearance=DataClass.RESTRICTED,
        max_context_tokens=200_000,
        input_cost_microunits_per_1k=100 + index % 23,
        output_cost_microunits_per_1k=200 + index % 31,
        estimated_latency_ms=50 + index % 101,
        quality_bps=8000 + index % 1500,
        max_evidence_class=7,
    )


def benchmark(size: int, repeats: int) -> dict[str, float | int | str]:
    task = TaskProfile(
        task_id=f"benchmark-{size}",
        required_capabilities=frozenset({"code"}),
        data_class=DataClass.INTERNAL,
        risk_tier=RiskTier.HIGH,
        required_evidence_class=3,
        worker_input_tokens=4000,
        worker_output_tokens=2000,
        verifier_input_tokens=2500,
        verifier_output_tokens=800,
        max_total_tokens=20_000,
        max_cost_microunits=100_000,
        max_latency_ms=10_000,
    )
    agents = [agent(i, "worker") for i in range(size)] + [agent(i, "verifier") for i in range(size)]
    governor = ResourceGovernor()
    samples_ms: list[float] = []
    decision = None
    for _ in range(repeats):
        started = time.perf_counter()
        decision = governor.plan(task, agents)
        samples_ms.append((time.perf_counter() - started) * 1000)
    assert decision is not None
    return {
        "workers": size,
        "verifiers": size,
        "pairs": size * size,
        "repeats": repeats,
        "decision": decision.decision,
        "median_ms": statistics.median(samples_ms),
        "min_ms": min(samples_ms),
        "max_ms": max(samples_ms),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic deterministic NPRG reference benchmark")
    parser.add_argument("--sizes", nargs="+", type=int, default=[50, 100, 250, 500])
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    if args.repeats <= 0 or any(size <= 0 for size in args.sizes):
        parser.error("sizes and repeats must be positive")
    for size in args.sizes:
        result = benchmark(size, args.repeats)
        print(
            "workers={workers} verifiers={verifiers} pairs={pairs} repeats={repeats} "
            "decision={decision} median_ms={median_ms:.3f} min_ms={min_ms:.3f} max_ms={max_ms:.3f}".format(
                **result
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
