from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
violations: list[str] = []
for path in sorted((ROOT / "src" / "lo4q64").glob("*.py")):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            violations.append(f"float literal: {path.name}:{node.lineno}={node.value!r}")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name.split('.')[0] for a in node.names] if isinstance(node, ast.Import) else [(node.module or '').split('.')[0]]
            if any(n in {"socket", "requests", "httpx", "urllib"} for n in names):
                violations.append(f"network import: {path.name}:{node.lineno}:{names}")
print(json.dumps({"status": "PASS" if not violations else "FAIL", "violations": violations}, sort_keys=True))
raise SystemExit(1 if violations else 0)
