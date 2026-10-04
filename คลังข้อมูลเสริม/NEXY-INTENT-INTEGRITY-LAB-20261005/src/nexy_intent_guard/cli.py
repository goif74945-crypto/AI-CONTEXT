from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .core import ContractError, evaluate_proposal, semantic_digest, validate_contract_shape
from .transition import compare_contracts


def _load(path: str) -> Any:
    p = Path(path)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContractError(f"Invalid JSON in {path}: {exc}") from exc


def _emit(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nexy-intent-guard")
    sub = parser.add_subparsers(dest="command", required=True)

    digest = sub.add_parser("digest", help="Validate and hash an intent contract")
    digest.add_argument("contract")

    proposal = sub.add_parser("check-proposal", help="Check an execution proposal against a contract")
    proposal.add_argument("contract")
    proposal.add_argument("proposal")

    transition = sub.add_parser("check-transition", help="Detect semantic drift between contract versions")
    transition.add_argument("base")
    transition.add_argument("candidate")
    transition.add_argument("--approval", default=None)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "digest":
            contract = _load(args.contract)
            validate_contract_shape(contract)
            _emit({"contract_digest": semantic_digest(contract), "status": "PASS"})
            return 0

        if args.command == "check-proposal":
            report = evaluate_proposal(_load(args.contract), _load(args.proposal))
            _emit(report.to_dict())
            return 0 if report.decision.value == "PASS" else 2

        if args.command == "check-transition":
            approval = _load(args.approval) if args.approval else None
            report = compare_contracts(_load(args.base), _load(args.candidate), approval)
            _emit(report.to_dict())
            return 0 if report.decision.value == "PASS" else (2 if report.decision.value == "FREEZE" else 1)

    except ContractError as exc:
        _emit({"status": "INVALID_INPUT", "error": str(exc)})
        return 64

    parser.error("unreachable command")
    return 64


if __name__ == "__main__":
    sys.exit(main())
