from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .engine import ConformanceEngine
from .errors import ConformanceError
from .model import CaseContract, Observation, ProviderManifest, Status


def _load_json(path: str) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _emit(payload: Any) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, sort_keys=True, indent=2)
    sys.stdout.write("\n")


def _verify(args: argparse.Namespace) -> int:
    manifest = ProviderManifest.from_dict(_load_json(args.manifest))
    case = CaseContract.from_dict(_load_json(args.case))
    observations = [Observation.from_dict(_load_json(path)) for path in args.observation]
    report = ConformanceEngine().verify(manifest, case, observations)
    _emit(report.to_dict())
    return 0 if report.status is Status.PASS else 2


def _compare(args: argparse.Namespace) -> int:
    case = CaseContract.from_dict(_load_json(args.case))
    groups: dict[str, list[Observation]] = {}
    for path in args.observation:
        observation = Observation.from_dict(_load_json(path))
        groups.setdefault(observation.provider_ref, []).append(observation)
    status, findings = ConformanceEngine().compare_reports(case, groups)
    _emit({"case_id": case.case_id, "status": status.value, "findings": [f.to_dict() for f in findings]})
    return 0 if status is Status.PASS else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nexy-model-conformance")
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="verify observations for one provider manifest")
    verify.add_argument("--manifest", required=True)
    verify.add_argument("--case", required=True)
    verify.add_argument("--observation", action="append", required=True)
    verify.set_defaults(func=_verify)

    compare = sub.add_parser("compare", help="compare stable paths across providers")
    compare.add_argument("--case", required=True)
    compare.add_argument("--observation", action="append", required=True)
    compare.set_defaults(func=_compare)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ConformanceError, OSError, json.JSONDecodeError) as exc:
        _emit({"status": "FAIL", "error": type(exc).__name__, "message": str(exc)})
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
