from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ)
ENV["PYTHONPATH"] = str(ROOT / "src")
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)


def run(name: str, cmd: list[str]) -> None:
    p = subprocess.run(cmd, cwd=ROOT, env=ENV, text=True, capture_output=True)
    (EVIDENCE / name).write_text(f"$ {' '.join(cmd)}\nexit={p.returncode}\n\nSTDOUT\n{p.stdout}\nSTDERR\n{p.stderr}", encoding="utf-8")
    if p.returncode != 0:
        raise SystemExit(f"verification failed: {name}")


run("01_compileall.txt", [sys.executable, "-m", "compileall", "-q", "src", "tests", "demo.py"])
run("02_unittest.txt", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
run("03_demo.json.txt", [sys.executable, "demo.py"])
run("03b_static_policy_scan.txt", [sys.executable, "static_policy_scan.py"])

# Deterministic replay: execute demo twice and compare exact bytes.
a = subprocess.check_output([sys.executable, "demo.py"], cwd=ROOT, env=ENV)
b = subprocess.check_output([sys.executable, "demo.py"], cwd=ROOT, env=ENV)
(EVIDENCE / "04_replay_determinism.txt").write_text(
    f"byte_equal={a == b}\nsha256={hashlib.sha256(a).hexdigest()}\nbytes={len(a)}\n", encoding="utf-8"
)
if a != b:
    raise SystemExit("demo replay was not byte-stable")

files = []
for path in sorted(ROOT.rglob("*")):
    if path.is_file() and "__pycache__" not in path.parts and path.name not in {"MANIFEST.sha256", "10_REMOTE_PUBLICATION_RECEIPT.md"}:
        rel = path.relative_to(ROOT).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        files.append((digest, rel))
(ROOT / "MANIFEST.sha256").write_text("".join(f"{d}  {p}\n" for d, p in files), encoding="utf-8")
(EVIDENCE / "05_verification_summary.json").write_text(json.dumps({
    "status": "PASS",
    "concept_count": 20,
    "q_format": "signed checked Q64.64",
    "compileall": "PASS",
    "unit_integration_tests": "PASS",
    "replay_determinism": "PASS",
    "manifest_files": len(files),
}, indent=2, sort_keys=True), encoding="utf-8")
print("PASS")
