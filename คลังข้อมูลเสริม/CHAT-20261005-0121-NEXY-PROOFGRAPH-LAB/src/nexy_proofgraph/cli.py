from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .documents import load_documents
from .graph import extract_link_edges, impact_closure
from .lockfile import build_lock, dump_lock, load_lock, verify_lock
from .model import Severity
from .policy import load_policy
from .rules import run_rules


def _json(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _scan(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    policy = load_policy(Path(args.policy))
    documents = load_documents(root, max_bytes=policy.scan_max_bytes)
    findings = run_rules(documents, policy)
    threshold = Severity.parse(args.fail_on)
    counts = {name: 0 for name in Severity.__members__}
    for finding in findings:
        counts[finding.severity.name] += 1
    payload = {
        "schema": "nexy-proofgraph/scan-result",
        "documents": len(documents),
        "findings": [f.to_dict() for f in findings],
        "counts": counts,
        "fail_on": threshold.name,
        "ok": not any(f.severity >= threshold for f in findings),
    }
    if args.format == "json":
        print(_json(payload))
    else:
        print(f"documents={payload['documents']} ok={payload['ok']} counts={counts}")
        for f in findings:
            loc = f"{f.path}:{f.line}" if f.line else f.path
            print(f"{f.severity.name:<8} {f.rule_id} {loc} {f.message}")
    return 0 if payload["ok"] else 1


def _graph(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    policy = load_policy(Path(args.policy))
    documents = load_documents(root, max_bytes=policy.scan_max_bytes)
    edges = extract_link_edges(documents)
    payload = {
        "schema": "nexy-proofgraph/link-graph",
        "nodes": [{"path": d.path, "sha256": d.sha256, "size": d.size, "kind": d.kind} for d in documents],
        "edges": [e.to_dict() for e in edges],
    }
    rendered = _json(payload) + "\n"
    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


def _impact(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    policy = load_policy(Path(args.policy))
    documents = load_documents(root, max_bytes=policy.scan_max_bytes)
    edges = extract_link_edges(documents)
    impacted = impact_closure(edges, args.changed, max_depth=args.max_depth)
    print(_json({"schema": "nexy-proofgraph/impact", "changed": args.changed, "impact": impacted}))
    return 0


def _lock(args: argparse.Namespace) -> int:
    lock = build_lock(Path(args.root), args.paths)
    dump_lock(lock, Path(args.out))
    print(_json({"ok": True, "out": args.out, "files": len(lock["files"])}))
    return 0


def _verify_lock(args: argparse.Namespace) -> int:
    result = verify_lock(Path(args.root), load_lock(Path(args.lock)))
    print(_json(result))
    return 0 if result["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nexy-proofgraph", description="Deterministic AI-CONTEXT integrity and impact analyzer")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="scan context files against deterministic rules")
    scan.add_argument("root")
    scan.add_argument("--policy", required=True)
    scan.add_argument("--format", choices=("text", "json"), default="text")
    scan.add_argument("--fail-on", choices=("INFO", "WARNING", "ERROR", "CRITICAL"), default="ERROR")
    scan.set_defaults(func=_scan)

    graph = sub.add_parser("graph", help="emit a local Markdown-reference graph")
    graph.add_argument("root")
    graph.add_argument("--policy", required=True)
    graph.add_argument("--out")
    graph.set_defaults(func=_graph)

    impact = sub.add_parser("impact", help="compute reverse-reference impact closure")
    impact.add_argument("root")
    impact.add_argument("--policy", required=True)
    impact.add_argument("--changed", nargs="+", required=True)
    impact.add_argument("--max-depth", type=int, default=32)
    impact.set_defaults(func=_impact)

    lock = sub.add_parser("lock", help="create deterministic SHA-256 truth-lock manifest")
    lock.add_argument("root")
    lock.add_argument("--paths", nargs="+", required=True)
    lock.add_argument("--out", required=True)
    lock.set_defaults(func=_lock)

    verify = sub.add_parser("verify-lock", help="verify a truth-lock manifest against current files")
    verify.add_argument("root")
    verify.add_argument("--lock", required=True)
    verify.set_defaults(func=_verify_lock)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
