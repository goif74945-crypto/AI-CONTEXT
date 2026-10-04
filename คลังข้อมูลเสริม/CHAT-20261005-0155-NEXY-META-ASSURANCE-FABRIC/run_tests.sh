#!/usr/bin/env sh
set -eu
PYTHONPATH="${PYTHONPATH:-}:src" python3 -m compileall -q src tests
PYTHONPATH="${PYTHONPATH:-}:src" python3 -m unittest discover -s tests -p 'test_*.py' -v
