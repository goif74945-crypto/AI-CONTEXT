#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
files=(
  "$ROOT/shared/q64.ts" "$ROOT/shared/contracts.ts" "$ROOT/shared/calculus.ts"
  "$ROOT/01_FLOWGUARD_64/src.ts" "$ROOT/02_QUEUEBOUND_64/src.ts" "$ROOT/03_DEADLINE_64/src.ts"
  "$ROOT/04_CHAIN_64/src.ts" "$ROOT/05_SHAPER_64/src.ts"
)
if grep -nE '(^|[^A-Za-z0-9_])[0-9]+\.[0-9]+([^A-Za-z0-9_]|$)|Math\.|parseFloat\(|Number\(' "${files[@]}"; then
  echo 'FAIL: forbidden floating-point construct found in quantitative decision modules'
  exit 1
fi
if grep -nE '\beval\(|new Function\(|child_process|fetch\(|https?://' "${files[@]}"; then
  echo 'FAIL: forbidden dynamic/network primitive found in quantitative decision modules'
  exit 1
fi
echo 'PASS: quantitative decision modules contain no floating-point literal/API and no dynamic/network primitive'
