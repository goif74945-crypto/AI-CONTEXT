from __future__ import annotations

import compileall
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> int:
    if not compileall.compile_dir(SRC, quiet=1, force=True):
        print("STATIC_COMPILE: FAIL")
        return 2
    print("STATIC_COMPILE: PASS")

    env = {**__import__("os").environ, "PYTHONPATH": str(SRC)}
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-p", "test_*.py", "-v"],
        cwd=ROOT,
        env=env,
        text=True,
    )
    if proc.returncode != 0:
        print("UNIT_AND_INTEGRATION: FAIL")
        return proc.returncode
    print("UNIT_AND_INTEGRATION: PASS")

    probe_outputs = []
    for seed in ("1", "2", "777"):
        probe_env = {**env, "PYTHONHASHSEED": seed}
        probe = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "determinism_probe.py")],
            cwd=ROOT,
            env=probe_env,
            text=True,
            capture_output=True,
            check=True,
        )
        probe_outputs.append(probe.stdout.strip())
    if len(set(probe_outputs)) != 1:
        print("DETERMINISM_PROBE: FAIL")
        for seed, output in zip(("1", "2", "777"), probe_outputs):
            print(seed, output)
        return 3
    print("DETERMINISM_PROBE: PASS (PYTHONHASHSEED=1,2,777 identical)")

    tracked = sorted([*SRC.rglob("*.py"), *(ROOT / "tests").rglob("*.py"), ROOT / "pyproject.toml", *(ROOT / "scripts").rglob("*.py")])
    manifest = {
        "format": 1,
        "files": [
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "git_blob_sha1": git_blob_sha(path),
                "bytes": path.stat().st_size,
            }
            for path in tracked
        ],
    }
    (ROOT / "IMPLEMENTATION_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"MANIFEST: PASS ({len(tracked)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
