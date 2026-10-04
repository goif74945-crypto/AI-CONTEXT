# Verification Evidence Report

- execution: `CHAT-20261005-0155-NEXY-EDGE-CONTRACTS-QUINTET-SOL`
- environment: `Python 3.13.5`
- network required: no
- third-party runtime dependencies: none

## E1 static
Command: `PYTHONPATH=src python -m compileall -q src tests`

Observed: **PASS**. Python source and tests compiled without syntax errors.

## E2 unit / negative / composition
Command: `PYTHONPATH=src python -m unittest discover -s tests -v`

Observed: **PASS — 27/27 tests**.

Coverage includes:
- approval plan tamper, expiry, directive epoch drift, scope escalation, mutation budget and signature failure;
- evidence closure optimality, prerequisite cycle, impossible closure and state-limit fail-closed behavior;
- safe adapter exact mapping, alias mapping, incompatible types, ambiguity and critical-field drift;
- correlated-witness false consensus, independent subset selection and target mismatch;
- policy monotonicity pass/violation/mixed-direction cases;
- cross-module safe pipeline composition;
- deterministic verdict fingerprint repeatability;
- AST static guard against network/subprocess/eval-style execution in reference core.

Raw output: `evidence/test-output.txt`.

## Evidence boundary
This proves E1/E2 properties of this standalone reference package only. It does **not** prove NEXY.AI integration, production authentication/key management, provider registry truth, deployment, performance at production scale, or user adoption.
