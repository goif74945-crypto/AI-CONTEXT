from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .codec import compact
from .io import bundle_from_dict, result_from_dict
from .model import CodecPolicy, CodecStatus
from .serialization import canonical_json_text
from .verify import verify_against_source


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _policy(args: argparse.Namespace) -> CodecPolicy:
    return CodecPolicy(
        max_capsule_bytes=args.max_bytes,
        max_loss_ppm=args.max_loss_ppm,
        protected_authority_rank=args.protected_authority_rank,
        allow_sensitive=args.allow_sensitive,
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lbcc")
    sub = p.add_subparsers(dest="command", required=True)

    def common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--max-bytes", type=int, required=True)
        sp.add_argument("--max-loss-ppm", type=int, default=0)
        sp.add_argument("--protected-authority-rank", type=int, default=95)
        sp.add_argument("--allow-sensitive", action="store_true")

    c = sub.add_parser("compact")
    c.add_argument("bundle")
    common(c)

    v = sub.add_parser("verify")
    v.add_argument("bundle")
    v.add_argument("result")
    common(v)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        bundle = bundle_from_dict(_load_json(args.bundle))
        policy = _policy(args)
        if args.command == "compact":
            result = compact(bundle, policy)
            print(canonical_json_text(result))
            return 0 if result.status == CodecStatus.PASS else 2
        result = result_from_dict(_load_json(args.result))
        report = verify_against_source(bundle, result, policy)
        print(canonical_json_text(report))
        return 0 if report.passed else 3
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 64


if __name__ == "__main__":
    raise SystemExit(main())
