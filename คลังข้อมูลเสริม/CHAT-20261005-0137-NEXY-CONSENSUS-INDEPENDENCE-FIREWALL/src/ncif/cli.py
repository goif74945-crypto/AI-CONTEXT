from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import evaluate_consensus
from .models import ConsensusPolicy, ContractError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate evidence-lineage independence for a consensus claim.")
    parser.add_argument("input", type=Path, help="JSON file containing claim_id, evidence, and votes")
    parser.add_argument("--min-support-groups", type=int, default=2)
    parser.add_argument("--max-opposition-groups", type=int, default=0)
    parser.add_argument("--require-single-root-resilience", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        policy = ConsensusPolicy(
            min_support_groups=args.min_support_groups,
            max_opposition_groups=args.max_opposition_groups,
            require_single_root_resilience=args.require_single_root_resilience,
        )
        result = evaluate_consensus(raw, policy)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(json.dumps({"decision": "CONTRACT_ERROR", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 3

    print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result.decision == "CONSENSUS_CANDIDATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
