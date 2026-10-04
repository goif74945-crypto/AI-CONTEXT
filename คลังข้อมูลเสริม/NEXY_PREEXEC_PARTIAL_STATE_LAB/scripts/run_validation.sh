#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
export PYTHONPATH="$ROOT/src"
python3 -m compileall -q src tests
python3 -m unittest discover -s tests -v
python3 -m nexy_pepsa.cli analyze --plan examples/safe_plan.json --policy examples/policy.json >/tmp/nexy_pepsa_safe_report.json
safe_code=$?
if [ "$safe_code" -ne 0 ]; then
  echo "safe plan did not return READY" >&2
  exit 1
fi
set +e
python3 -m nexy_pepsa.cli analyze --plan examples/unsafe_plan.json --policy examples/policy.json >/tmp/nexy_pepsa_unsafe_report.json
unsafe_code=$?
set -e
if [ "$unsafe_code" -ne 2 ]; then
  echo "unsafe plan did not return FREEZE exit code 2" >&2
  exit 1
fi
python3 - <<'PY'
import json
from pathlib import Path
safe = json.loads(Path('/tmp/nexy_pepsa_safe_report.json').read_text())
unsafe = json.loads(Path('/tmp/nexy_pepsa_unsafe_report.json').read_text())
assert safe['verdict'] == 'READY', safe
assert unsafe['verdict'] == 'FREEZE', unsafe
assert any(item['code'] == 'PROTECTED_RESOURCE_MUTATION' for item in unsafe['findings'])
print('VALIDATION_GATE=PASS')
print('SAFE_VERDICT=' + safe['verdict'])
print('UNSAFE_VERDICT=' + unsafe['verdict'])
print('SAFE_COMBINED_HASH=' + safe['combined_hash'])
print('UNSAFE_COMBINED_HASH=' + unsafe['combined_hash'])
PY
