#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
cat bundle/bundle.part*.b64 | base64 -d > lo4_verified_skill_foundry.tar.gz
echo "66b1876dd724af961282fe19373283b75979de75f133036e70c0f578e82a7a22  lo4_verified_skill_foundry.tar.gz" | sha256sum -c -
tar -xzf lo4_verified_skill_foundry.tar.gz
cd lo4_verified_skill_foundry
sha256sum -c MANIFEST.sha256
python static_guard.py
python verify.py
python stress_verify.py
