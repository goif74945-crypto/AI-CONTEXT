"""Dependency-free verification runner for the NEXY PCF lab."""

from __future__ import annotations

import compileall
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TEST_KEY = b"verification-only-key-32-bytes-minimum"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    summary = {
        "compile": False,
        "json_files": 0,
        "allow_fixture": False,
        "freeze_fixture": False,
        "secret_leak_check": False,
        "unit_tests": False,
    }

    if not compileall.compile_dir(str(SRC), quiet=1):
        print(json.dumps(summary, sort_keys=True))
        return 1
    summary["compile"] = True

    for folder in (ROOT / "schemas", ROOT / "fixtures"):
        for path in sorted(folder.glob("*.json")):
            load_json(path)
            summary["json_files"] += 1

    sys.path.insert(0, str(SRC))
    from nexy_pcf.compiler import compile_context

    policy = load_json(ROOT / "fixtures" / "policy.json")
    destination = load_json(ROOT / "fixtures" / "provider-alpha.json")
    allow_env = load_json(ROOT / "fixtures" / "envelope-allow.json")
    freeze_env = load_json(ROOT / "fixtures" / "envelope-freeze-secret.json")

    allow = compile_context(allow_env, destination, policy, receipt_key=TEST_KEY)
    if allow.get("decision") != "ALLOW":
        print(json.dumps(summary, sort_keys=True))
        return 1
    summary["allow_fixture"] = True

    freeze = compile_context(freeze_env, destination, policy, receipt_key=TEST_KEY)
    if freeze.get("decision") != "FREEZE":
        print(json.dumps(summary, sort_keys=True))
        return 1
    summary["freeze_fixture"] = True

    if "TOP-SECRET-FIXTURE-VALUE" in json.dumps(freeze, sort_keys=True):
        print(json.dumps(summary, sort_keys=True))
        return 1
    summary["secret_leak_check"] = True

    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        print(completed.stdout)
        print(json.dumps(summary, sort_keys=True))
        return completed.returncode
    summary["unit_tests"] = True
    print(completed.stdout)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
