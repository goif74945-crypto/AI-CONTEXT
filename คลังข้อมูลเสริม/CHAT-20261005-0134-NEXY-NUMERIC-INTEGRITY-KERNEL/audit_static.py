from __future__ import annotations
import ast
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "nnik"
FORBIDDEN_IMPORT_ROOTS = {"socket","requests","urllib","http","ftplib","telnetlib","paramiko","subprocess","multiprocessing","ctypes"}
FORBIDDEN_CALLS = {"eval","exec","compile","__import__"}

def run() -> int:
    findings = []
    files = sorted(PACKAGE.glob("*.py"))
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    if root in FORBIDDEN_IMPORT_ROOTS:
                        findings.append({"file":path.name,"line":node.lineno,"kind":"forbidden_import","value":alias.name})
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0]
                if root in FORBIDDEN_IMPORT_ROOTS:
                    findings.append({"file":path.name,"line":node.lineno,"kind":"forbidden_import","value":node.module})
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                findings.append({"file":path.name,"line":node.lineno,"kind":"forbidden_call","value":node.func.id})
            elif isinstance(node, ast.Constant) and isinstance(node.value, float):
                findings.append({"file":path.name,"line":node.lineno,"kind":"binary_float_literal","value":repr(node.value)})
    result = {"files_scanned":[p.name for p in files],"findings":findings,"pass":not findings}
    (ROOT/"evidence"/"static_audit.json").write_text(json.dumps(result,indent=2)+"
",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return 0 if result["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(run())
