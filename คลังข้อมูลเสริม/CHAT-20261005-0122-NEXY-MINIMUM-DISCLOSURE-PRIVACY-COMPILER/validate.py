from __future__ import annotations

import hashlib
import json
import pathlib
import py_compile
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    py_files = sorted(ROOT.rglob("*.py"))
    for path in py_files:
        py_compile.compile(str(path), doraise=True)

    json_files = sorted(ROOT.rglob("*.json"))
    parsed = {str(path.relative_to(ROOT)): json.loads(path.read_text(encoding="utf-8")) for path in json_files}
    fixture = ROOT / "fixtures" / "adversarial_cases.json"
    data = parsed[str(fixture.relative_to(ROOT))]
    assert isinstance(data, list) and len(data) >= 8
    assert len({x["id"] for x in data}) == len(data)

    env = {"PYTHONPATH": str(ROOT / "src")}
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    print(proc.stdout)
    print(proc.stderr, file=sys.stderr)
    if proc.returncode != 0:
        return proc.returncode

    manifest = {
        "python_files": {str(p.relative_to(ROOT)): sha256(p) for p in py_files},
        "json_files": {str(p.relative_to(ROOT)): sha256(p) for p in json_files},
        "tests_returncode": proc.returncode,
    }
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
