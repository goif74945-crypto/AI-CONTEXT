#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT/src"
python -m compileall -q "$ROOT/src" "$ROOT/tests"
python -m unittest discover -s "$ROOT/tests" -v
python -m nexy_ixlab.cli analyze "$ROOT/examples/high_friction_plan.json" >/dev/null
python -m nexy_ixlab.cli optimize "$ROOT/examples/high_friction_plan.json" >/dev/null
python -m nexy_ixlab.cli compare "$ROOT/examples/high_friction_plan.json" "$ROOT/examples/lower_friction_plan.json" >/dev/null
python -m nexy_ixlab.cli decision "$ROOT/examples/decision_context.json" >/dev/null
printf 'IX-Lab validation PASS\n'
