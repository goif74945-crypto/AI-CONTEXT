import ast
from pathlib import Path
import unittest


class StaticGuardTests(unittest.TestCase):
    def test_reference_core_has_no_dangerous_runtime_imports_or_eval(self):
        root = Path(__file__).resolve().parents[1] / "src" / "frontierfive"
        banned_modules = {"subprocess", "socket", "requests", "urllib", "httpx", "os"}
        banned_calls = {"eval", "exec", "compile", "__import__"}
        violations = []
        for path in sorted(root.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split(".")[0] in banned_modules:
                            violations.append(f"{path.name}:import:{alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.split(".")[0] in banned_modules:
                        violations.append(f"{path.name}:from:{node.module}")
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in banned_calls:
                    violations.append(f"{path.name}:call:{node.func.id}")
        self.assertEqual(violations, [])
