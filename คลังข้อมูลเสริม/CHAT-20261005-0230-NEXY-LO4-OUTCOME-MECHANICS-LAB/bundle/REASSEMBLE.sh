#!/usr/bin/env bash
set -euo pipefail
cat part-*.b64 | base64 -d > outcome-mechanics-source.tar.gz
printf '%s  %s\n' '99d61fc903013f1c99d09719fbbcbd62b7a5bda6bff2a208034d3db6a500bac7' 'outcome-mechanics-source.tar.gz' | sha256sum -c -
tar -xzf outcome-mechanics-source.tar.gz
