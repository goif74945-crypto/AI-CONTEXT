#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist
npm run typecheck
npm run build
npm test
npm run stress
bash scripts/static_audit.sh
python3 scripts/crosscheck.py
