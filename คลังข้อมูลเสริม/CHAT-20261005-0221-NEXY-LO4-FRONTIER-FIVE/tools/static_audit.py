from __future__ import annotations

from pathlib import Path
import ast
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EXTS = {".py", ".md", ".toml", ".json", ".txt"}
SECRET_PATTERNS = {
    "openai_key": re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}

py_files = sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "tests").rglob("*.py")) + sorted((ROOT / "tools").rglob("*.py"))
for path in py_files:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

hits = []
manifest = {}
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.suffix not in SOURCE_EXTS:
        continue
    rel_parts = path.relative_to(ROOT).parts
    if any(part in {"build", "dist", "__pycache__"} or part.endswith(".egg-info") for part in rel_parts):
        continue
    if rel_parts and rel_parts[0] == "evidence":
        continue
    data = path.read_bytes()
    rel = path.relative_to(ROOT).as_posix()
    manifest[rel] = hashlib.sha256(data).hexdigest()
    text = data.decode("utf-8", errors="ignore")
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            hits.append({"path": rel, "pattern": name})

result = {
    "status": "PASS" if not hits else "FAIL",
    "python_ast_files": len(py_files),
    "manifest_files": len(manifest),
    "secret_hits": hits,
}
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
(ROOT / "evidence" / "sha256-manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
if hits:
    raise SystemExit(1)
