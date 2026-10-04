from __future__ import annotations

import argparse
import json
import sys

from .compiler import compile_experiment
from .errors import ExperimentValidationError
from .io import load_json, proposal_from_dict
from .serialization import contract_hash, pretty_contract_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="npel")
    sub = parser.add_subparsers(dest="command", required=True)
    compile_cmd = sub.add_parser("compile", help="compile an experiment proposal JSON")
    compile_cmd.add_argument("proposal")
    args = parser.parse_args(argv)

    if args.command == "compile":
        try:
            proposal = proposal_from_dict(load_json(args.proposal))
            contract = compile_experiment(proposal)
        except (KeyError, TypeError, ValueError, ExperimentValidationError) as exc:
            print(json.dumps({"status": "FREEZE", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
            return 2
        print(pretty_contract_json(contract))
        print(json.dumps({"contract_hash": contract_hash(contract)}, ensure_ascii=False))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
