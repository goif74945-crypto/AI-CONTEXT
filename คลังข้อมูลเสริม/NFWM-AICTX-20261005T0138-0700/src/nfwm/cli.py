from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analyzer import analyze_trace
from .canonical import canonical_json_bytes, sha256_canonical
from .errors import NFWMError
from .io import load_trace, write_canonical_json
from .minimize import minimize_violation, witness_is_one_minimal
from .profile import load_profile


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nfwm")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="analyze a trace and optionally minimize violations")
    analyze.add_argument("trace")
    analyze.add_argument("--profile", required=True)
    analyze.add_argument("--output")
    analyze.add_argument("--minimize", action="store_true")

    verify = sub.add_parser("verify-witness", help="verify a witness file against a profile")
    verify.add_argument("witness")
    verify.add_argument("--profile", required=True)
    return parser


def _emit(value: object, output: str | None) -> None:
    if output:
        write_canonical_json(output, value)
    else:
        sys.stdout.buffer.write(canonical_json_bytes(value) + b"\n")


def _run_analyze(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    trace = load_trace(args.trace)
    analysis = analyze_trace(trace, profile)
    result: dict[str, object] = {
        "schema_version": "nfwm.analysis.v1",
        "profile_id": profile.profile_id,
        "profile_status": profile.profile_status,
        "trace_hash": sha256_canonical(trace.to_raw()),
        **analysis.to_raw(),
    }
    if args.minimize and analysis.violations:
        witnesses = []
        for code in sorted({v.code for v in analysis.violations}):
            witness = minimize_violation(trace.events, profile, code)
            witnesses.append(witness.to_raw())
        result["witnesses"] = witnesses
    _emit(result, args.output)
    return 0 if analysis.passed else 2


def _run_verify(args: argparse.Namespace) -> int:
    profile = load_profile(args.profile)
    with Path(args.witness).open("r", encoding="utf-8") as f:
        raw = json.load(f)
    if raw.get("schema_version") != "nfwm.witness.v1":
        raise NFWMError("witness schema_version must equal 'nfwm.witness.v1'")
    events_raw = raw.get("events")
    if not isinstance(events_raw, list):
        raise NFWMError("witness.events must be an array")
    # Reuse strict Trace validation for event shape.
    from .model import Trace
    trace = Trace.from_raw({"schema_version": "nfwm.trace.v1", "events": events_raw})
    code = raw.get("violation_code")
    if not isinstance(code, str) or not code:
        raise NFWMError("witness.violation_code must be a non-empty string")
    expected_hash = raw.get("witness_hash")
    actual_hash = sha256_canonical([e.to_raw() for e in trace.events])
    hash_ok = expected_hash == actual_hash
    minimized = minimize_violation(trace.events, profile, code)
    one_minimal = witness_is_one_minimal(minimized, profile)
    same_event_count = len(minimized.witness_events) == len(trace.events)
    passed = bool(hash_ok and one_minimal and same_event_count)
    out = {
        "schema_version": "nfwm.witness-verification.v1",
        "status": "PASS" if passed else "FAIL",
        "hash_ok": hash_ok,
        "one_minimal": one_minimal,
        "same_event_count_after_reminimize": same_event_count,
        "witness_hash": actual_hash,
        "violation_code": code,
    }
    sys.stdout.buffer.write(canonical_json_bytes(out) + b"\n")
    return 0 if passed else 3


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "analyze":
            return _run_analyze(args)
        if args.command == "verify-witness":
            return _run_verify(args)
        raise AssertionError("unreachable command")
    except (NFWMError, ValueError, OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"NFWM_ERROR: {exc}\n")
        return 64


if __name__ == "__main__":
    raise SystemExit(main())
