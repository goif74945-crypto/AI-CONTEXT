from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "src" / "nexy_outcome"
BANNED_IMPORT_ROOTS = {
    "asyncio",
    "http",
    "os",
    "pathlib",
    "random",
    "requests",
    "secrets",
    "socket",
    "subprocess",
    "time",
    "urllib",
}

findings: list[dict[str, str]] = []
files = sorted(CORE.glob("*.py"))
for path in files:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        for name in names:
            root = name.split(".", 1)[0]
            # CLI is allowed stdin/stdout via sys; json/hashlib/math are deterministic library dependencies.
            if root in BANNED_IMPORT_ROOTS:
                findings.append({"file": str(path.relative_to(ROOT)), "import": name})

result = {
    "status": "PASS" if not findings else "FAIL",
    "checked_python_files": [str(p.relative_to(ROOT)) for p in files],
    "banned_import_roots": sorted(BANNED_IMPORT_ROOTS),
    "findings": findings,
    "note": "AST import audit of reference core; this is static evidence only, not a sandbox/runtime proof.",
}
print(json.dumps(result, sort_keys=True))
raise SystemExit(0 if not findings else 1)
