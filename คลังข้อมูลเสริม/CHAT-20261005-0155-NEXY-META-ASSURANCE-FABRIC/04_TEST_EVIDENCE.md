# Test Evidence

## Evidence E1-A — Python static compile
Environment observed during final aligned development run: Python 3.13.5.

Command:
```bash
PYTHONPATH=src python3 -m compileall -q src tests
```

Observed result: exit status 0.

Claim supported: source and tests parse/compile in the observed Python environment.  
Limitation: does not prove behavior or package installation metadata.

## Evidence E1-B — forbidden-import AST audit
Core modules were parsed with Python `ast` and imports were inspected against the forbidden core-I/O set:

`os, sys, subprocess, socket, requests, urllib, http, random, time, datetime, pathlib, sqlite3, multiprocessing, threading, asyncio`

Observed result: `FORBIDDEN_IMPORT_VIOLATIONS []`.

Claim supported: the inspected core source has no imports from the declared hidden-I/O/nondeterminism set.  
Limitation: static import absence alone is not a full sandbox/security proof.

## Evidence E2-A — unit + deterministic stress tests
Command:
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Observed final result after source alignment:
```text
Ran 31 tests in 0.004s
OK
```

Coverage highlights:
- MVS: relation PASS, relation FAIL, malformed relation, 451-case affine grid.
- CLL: legal transfer, undeclared mint, external delta, missing key, multi-step sequence, transfer grid.
- MPWE: minimum weighted cover, tie stability, uncovered requirement, malformed evidence, brute-force optimality cross-check.
- BFK: canonical key/scenario ordering, semantic diff, duplicate IDs, float rejection, 24 scenario permutations.
- SMS: all mutations killed by strict validator, survivors under weak validator, invalid baseline, duplicate constraints, missing field, non-boolean validator, per-mutation target violation.

## Remediation evidence
Earlier suite: 30/30 PASS. Logical independent fail-closed review found that SMS accepted truthy non-boolean validator outputs. The code was changed to require `bool` exactly and a regression test was added. Final aligned suite: 31/31 PASS.

## Evidence limits
- These are standalone local prototype tests, not NEXY.AI integration tests.
- No browser, service, database, network, deployment, load, fault-injection, or production evidence exists.
- GitHub persistence evidence is recorded in the completion record after final read-back.
