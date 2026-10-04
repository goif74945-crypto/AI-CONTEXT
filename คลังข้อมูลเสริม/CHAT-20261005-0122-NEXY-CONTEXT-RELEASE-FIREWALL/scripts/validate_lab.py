from __future__ import annotations

import ast
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []
    py_files = sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "tests").rglob("*.py")) + [pathlib.Path(__file__)]
    for path in py_files:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"syntax:{path.relative_to(ROOT)}:{exc}")

    for json_path in sorted(ROOT.rglob("*.json")):
        try:
            json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"json:{json_path.relative_to(ROOT)}:{exc}")

    fixture_path = ROOT / "fixtures" / "adversarial_cases.json"
    try:
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        if data.get("schema_version") != "1.0":
            errors.append("fixture schema_version must be 1.0")
        cases = data.get("cases")
        if not isinstance(cases, list) or len(cases) < 12:
            errors.append("fixture must contain at least 12 adversarial cases")
        else:
            ids = [case.get("id") for case in cases]
            if len(ids) != len(set(ids)):
                errors.append("fixture IDs must be unique")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"fixture:{exc}")

    required = [
        "00_SESSION_MEMORY.md",
        "01_TASK_CONTRACT.md",
        "02_ARCHITECTURE.md",
        "03_PRIVACY_CONTRACT.md",
        "04_ADOPTION_AND_RESEARCH.md",
        "README.md",
        "src/nexy_crf/engine.py",
        "tests/test_firewall.py",
        "fixtures/adversarial_cases.json",
    ]
    for relative in required:
        if not (ROOT / relative).exists():
            errors.append(f"missing:{relative}")

    if errors:
        print("VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALIDATION: PASS ({len(py_files)} Python files parsed; {len(data['cases'])} adversarial cases checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
