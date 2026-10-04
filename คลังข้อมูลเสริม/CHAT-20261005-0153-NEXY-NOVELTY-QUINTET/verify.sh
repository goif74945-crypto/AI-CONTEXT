#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
for d in "$ROOT"/0[1-5]_*; do
  echo "== $(basename "$d") =="
  (cd "$d" && python -m unittest -v test_src.py)
done
(cd "$ROOT" && python -m unittest -v test_integration.py)
python -m compileall -q "$ROOT"
echo "VERIFICATION_PASS"
