#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
out="$here/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz"
cat "$here"/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz.part00 \
    "$here"/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz.part01 \
    "$here"/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz.part02 \
    "$here"/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz.part03 > "$out"
echo "5b5511bd3139039fdb1c0b96717e4abfe5d22ce7bf24957556c535fd3ce5b6c1  $out" | sha256sum -c -
printf 'PASS: %s\n' "$out"
