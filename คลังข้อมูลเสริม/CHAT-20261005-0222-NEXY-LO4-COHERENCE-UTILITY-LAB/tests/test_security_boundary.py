from __future__ import annotations

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "src" / "lo4lab"
FORBIDDEN_IMPORT_ROOTS = {
    "subprocess", "socket", "requests", "urllib", "http", "ftplib", "telnetlib",
    "paramiko", "asyncssh", "httpx", "aiohttp",
}
FORBIDDEN_CALL_NAMES = {"eval", "exec"}
FORBIDDEN_ATTR_CALLS = {
    ("os", "system"), ("os", "popen"), ("os", "getenv"),
    ("subprocess", "run"), ("subprocess", "Popen"), ("subprocess", "call"),
}


def dotted_name(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Name):
        return (node.id,)
    if isinstance(node, ast.Attribute):
        return (*dotted_name(node.value), node.attr)
    return ()


class TestSecurityBoundary(unittest.TestCase):
    def test_reference_core_has_no_network_subprocess_or_dynamic_execution_imports(self):
        violations: list[str] = []
        for path in sorted(ROOT.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split(".")[0] in FORBIDDEN_IMPORT_ROOTS:
                            violations.append(f"{path.name}:{node.lineno}:import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    root = (node.module or "").split(".")[0]
                    if root in FORBIDDEN_IMPORT_ROOTS:
                        violations.append(f"{path.name}:{node.lineno}:from {node.module}")
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALL_NAMES:
                        violations.append(f"{path.name}:{node.lineno}:call {node.func.id}")
                    dotted = dotted_name(node.func)
                    if len(dotted) >= 2 and (dotted[-2], dotted[-1]) in FORBIDDEN_ATTR_CALLS:
                        violations.append(f"{path.name}:{node.lineno}:call {'.'.join(dotted)}")
        self.assertEqual(violations, [], "Forbidden execution/network boundary violations: " + repr(violations))

    def test_reference_core_does_not_read_environment(self):
        violations: list[str] = []
        for path in sorted(ROOT.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute) and dotted_name(node)[-2:] == ("os", "environ"):
                    violations.append(f"{path.name}:{node.lineno}:os.environ")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
