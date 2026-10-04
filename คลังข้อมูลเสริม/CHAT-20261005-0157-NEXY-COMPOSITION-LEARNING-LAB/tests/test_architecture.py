from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path


class ArchitectureBoundaryTests(unittest.TestCase):
    def test_runtime_package_imports_only_stdlib_or_local_modules(self) -> None:
        src = Path(__file__).resolve().parents[1] / "src" / "nexy_aux"
        stdlib = set(sys.stdlib_module_names)
        violations: list[tuple[str, str]] = []
        for path in sorted(src.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root not in stdlib and root != "nexy_aux":
                            violations.append((path.name, alias.name))
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    root = node.module.split(".", 1)[0]
                    if root not in stdlib and root != "nexy_aux":
                        violations.append((path.name, node.module))
        self.assertEqual(violations, [])

    def test_core_modules_do_not_import_network_or_process_execution(self) -> None:
        src = Path(__file__).resolve().parents[1] / "src" / "nexy_aux"
        forbidden_roots = {"socket", "subprocess", "requests", "httpx", "urllib", "ftplib", "paramiko"}
        violations: list[tuple[str, str]] = []
        for path in sorted(src.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                names: list[str] = []
                if isinstance(node, ast.Import):
                    names.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    names.append(node.module)
                for name in names:
                    if name.split(".", 1)[0] in forbidden_roots:
                        violations.append((path.name, name))
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
