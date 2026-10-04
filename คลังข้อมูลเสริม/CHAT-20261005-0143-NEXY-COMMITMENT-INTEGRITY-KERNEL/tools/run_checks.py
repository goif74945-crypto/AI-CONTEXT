from __future__ import annotations

import compileall
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    print("[1/4] compileall")
    if not compileall.compile_dir(ROOT / "src", quiet=1):
        return 1
    if not compileall.compile_dir(ROOT / "tests", quiet=1):
        return 1

    print("[2/4] JSON fixtures parse")
    for p in sorted((ROOT / "fixtures").glob("*.json")) + sorted((ROOT / "examples").glob("*.json")) + sorted((ROOT / "schemas").glob("*.json")):
        with p.open("r", encoding="utf-8") as f:
            json.load(f)
        print(f"  parsed {p.relative_to(ROOT)}")

    print("[3/4] unit tests")
    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    cp = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"], env=env, text=True)
    if cp.returncode:
        return cp.returncode

    print("[4/4] adversarial corpus")
    cp = subprocess.run([sys.executable, str(ROOT / "tools" / "run_corpus.py")], env=env, text=True)
    return cp.returncode


if __name__ == "__main__":
    raise SystemExit(main())
