from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = ["frontier5.py", "test_frontier5.py", "README.md", "00_SESSION_MEMORY.md", "evidence/VERIFICATION.md"]


def main() -> int:
    compile_run = subprocess.run(
        [sys.executable, "-m", "py_compile", str(ROOT / "frontier5.py"), str(ROOT / "test_frontier5.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    test_run = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_frontier5.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    hashes = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in FILES
        if (ROOT / name).exists()
    }
    result = {
        "status": "PASS" if compile_run.returncode == 0 and test_run.returncode == 0 else "FAIL",
        "compile_returncode": compile_run.returncode,
        "test_returncode": test_run.returncode,
        "hashes": hashes,
        "test_stdout": test_run.stdout,
        "test_stderr": test_run.stderr,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
