from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .canon import canonical_json, sha256_fingerprint
from .collision import compare_work_manifests
from .engine import evaluate_proposal
from .io import load_catalog, load_proposal, load_work_manifest, load_work_manifest_catalog
from .models import ProposalValidationError


def _print_json(data: object) -> None:
    sys.stdout.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nexy-proposal-forge",
        description="Deterministic evaluator for AI-proposed NEXY feature candidates.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a proposal capsule")
    validate.add_argument("proposal", type=Path)

    fingerprint = sub.add_parser("fingerprint", help="print the canonical SHA-256 proposal fingerprint")
    fingerprint.add_argument("proposal", type=Path)

    canonical = sub.add_parser("canonical", help="print canonical JSON")
    canonical.add_argument("proposal", type=Path)

    evaluate = sub.add_parser("evaluate", help="evaluate a proposal against an optional catalog")
    evaluate.add_argument("proposal", type=Path)
    evaluate.add_argument("--catalog", type=Path, default=None)

    collide = sub.add_parser("collide", help="compare one active work manifest against a manifest catalog")
    collide.add_argument("manifest", type=Path)
    collide.add_argument("--catalog", type=Path, required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "collide":
            manifest = load_work_manifest(args.manifest)
            catalog = load_work_manifest_catalog(args.catalog)
            _print_json(compare_work_manifests(manifest, catalog).to_dict())
            return 0

        proposal = load_proposal(args.proposal)
        if args.command == "validate":
            _print_json({"proposal_id": proposal.proposal_id, "status": "PASS"})
            return 0
        if args.command == "fingerprint":
            sys.stdout.write(sha256_fingerprint(proposal.to_dict()) + "\n")
            return 0
        if args.command == "canonical":
            sys.stdout.write(canonical_json(proposal.to_dict()) + "\n")
            return 0
        if args.command == "evaluate":
            catalog = load_catalog(args.catalog)
            _print_json(evaluate_proposal(proposal, catalog).to_dict())
            return 0
        parser.error(f"unknown command {args.command!r}")
    except (OSError, json.JSONDecodeError, ProposalValidationError, TypeError, ValueError) as exc:
        if isinstance(exc, ProposalValidationError):
            payload = {"status": "FAIL", "errors": list(exc.errors)}
        else:
            payload = {"status": "FAIL", "errors": [str(exc)]}
        _print_json(payload)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
