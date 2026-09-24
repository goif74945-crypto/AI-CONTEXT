#!/usr/bin/env python3
import subprocess
import sys

raise SystemExit(subprocess.call([
    sys.executable,
    "projects/NEXY.AI/context-router/tools/generate-context-pack.py",
    "--profile", "BUILDER",
    *sys.argv[1:],
]))
