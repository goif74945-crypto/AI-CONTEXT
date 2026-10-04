from __future__ import annotations

import hashlib
import pathlib
import py_compile
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src" / "nexy_lo4_pentaforge"


def main() -> int:
    for path in sorted(SRC.glob("*.py")):
        py_compile.compile(str(path), doraise=True)
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(proc.stdout, end="")
    print("SHA256")
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and "evidence" not in p.parts and "__pycache__" not in p.parts):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
