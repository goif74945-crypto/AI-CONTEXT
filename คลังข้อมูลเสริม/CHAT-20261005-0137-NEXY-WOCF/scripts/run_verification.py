from __future__ import annotations

import json
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    checks: list[dict[str, object]] = []

    py_files = [ROOT / "src" / "wocf.py", ROOT / "tests" / "test_wocf.py", ROOT / "scripts" / "run_verification.py"]
    try:
        for path in py_files:
            py_compile.compile(str(path), doraise=True)
        checks.append({"gate": "E1-python-compile", "status": "PASS", "files": [str(p.relative_to(ROOT)) for p in py_files]})
    except Exception as exc:  # pragma: no cover - verifier failure reporting
        checks.append({"gate": "E1-python-compile", "status": "FAIL", "error": repr(exc)})
        print(json.dumps({"status": "FAIL", "checks": checks}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1

    json_files = sorted((ROOT / "fixtures").glob("*.json")) + sorted((ROOT / "schema").glob("*.json"))
    try:
        for path in json_files:
            json.loads(path.read_text(encoding="utf-8"))
        checks.append({"gate": "E1-json-parse", "status": "PASS", "files": [str(p.relative_to(ROOT)) for p in json_files]})
    except Exception as exc:  # pragma: no cover
        checks.append({"gate": "E1-json-parse", "status": "FAIL", "error": repr(exc)})
        print(json.dumps({"status": "FAIL", "checks": checks}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1

    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "tests.test_wocf"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    checks.append(
        {
            "gate": "E2-unit-adversarial",
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    )

    allow = subprocess.run(
        [
            sys.executable,
            str(ROOT / "src" / "wocf.py"),
            "evaluate",
            "--proposal",
            str(ROOT / "fixtures" / "proposal-allow.json"),
            "--catalog",
            str(ROOT / "fixtures" / "catalog.json"),
            "--policy",
            str(ROOT / "fixtures" / "policy.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    allow_payload = json.loads(allow.stdout)
    allow_pass = allow.returncode == 0 and allow_payload.get("decision") in {"ALLOW", "WARN"}
    checks.append(
        {
            "gate": "E2-cli-allow-scenario",
            "status": "PASS" if allow_pass else "FAIL",
            "returncode": allow.returncode,
            "decision": allow_payload.get("decision"),
        }
    )

    freeze = subprocess.run(
        [
            sys.executable,
            str(ROOT / "src" / "wocf.py"),
            "evaluate",
            "--proposal",
            str(ROOT / "fixtures" / "proposal-freeze.json"),
            "--catalog",
            str(ROOT / "fixtures" / "catalog.json"),
            "--policy",
            str(ROOT / "fixtures" / "policy.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    freeze_payload = json.loads(freeze.stdout)
    freeze_pass = freeze.returncode == 2 and freeze_payload.get("decision") == "FREEZE"
    checks.append(
        {
            "gate": "E2-cli-freeze-scenario",
            "status": "PASS" if freeze_pass else "FAIL",
            "returncode": freeze.returncode,
            "decision": freeze_payload.get("decision"),
            "finding_codes": [item.get("code") for item in freeze_payload.get("findings", [])],
        }
    )

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    print(json.dumps({"status": status, "checks": checks}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
