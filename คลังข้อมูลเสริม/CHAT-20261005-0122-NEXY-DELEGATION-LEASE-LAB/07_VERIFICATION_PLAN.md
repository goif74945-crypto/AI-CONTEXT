# 07 — Verification Plan

| Claim | Required evidence |
|---|---|
| package parses/imports | E1 |
| exact policy behavior | E2 |
| child cannot escalate in tested cases | E2 |
| schema files are valid JSON | E1 syntax parse |
| full JSON Schema 2020-12 conformance | E1 real schema validator, not yet run |
| NEXY auth/RBAC integration safe | E3 |
| authorize/freeze/re-authorize UX works | E4 |
| revocation/concurrency safe | E5 |
| deployed target safe | E6 |

## Executed local commands
```bash
cd reference
PYTHONPATH=src python -m compileall -q src tests examples
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python examples/demo.py
```
Schemas were syntax-parsed with stdlib `json.loads`.

## Covered negative paths
Plan drift; resource/verb/effect violations; missing high-impact gate; expiry; not-yet-active; revocation; action/cost exhaustion; policy mismatch; invalid index; frozen-decision commit rejection; child escalation; novel wildcard rejection; destination drift; journal tamper; malformed fields; deterministic repeatability.

## Future proof work
Property tests over scope lattices; lifecycle/revocation model checking; concurrent reservation tests; resource canonicalizer fuzzing; signature forgery/rotation; stale-worker revocation; crash between decision/effect; replay receipts; cross-project confusion; UI/backend desynchronization.

Do not infer integrated PASS from the standalone suite.
