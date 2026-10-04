from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .canonical import canonical_json
from .simulator import SimulationEvent, simulate
from .validator import validate_manifest


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _parse_quorum(value: str | None) -> bool | None:
    if value is None or value == "unknown":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nexy-adapter-cert")
    sub = parser.add_subparsers(dest="command", required=True)

    validate_cmd = sub.add_parser("validate", help="Validate an AgentAdapter manifest")
    validate_cmd.add_argument("manifest")

    sim_cmd = sub.add_parser("simulate", help="Simulate canonical adapter outcome semantics")
    sim_cmd.add_argument("manifest")
    sim_cmd.add_argument("--event", required=True, choices=[e.value for e in SimulationEvent])
    sim_cmd.add_argument("--quorum-possible", choices=["true", "false", "unknown"], default="unknown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = _load(args.manifest)

    if args.command == "validate":
        report = validate_manifest(manifest)
        print(canonical_json(report.to_dict()))
        return 0 if report.status == "PASS" else 2

    report = simulate(
        manifest,
        args.event,
        quorum_possible_after_exclusion=_parse_quorum(args.quorum_possible),
    )
    print(canonical_json(report.to_dict()))
    return 0 if report.status == "PASS" else 2
