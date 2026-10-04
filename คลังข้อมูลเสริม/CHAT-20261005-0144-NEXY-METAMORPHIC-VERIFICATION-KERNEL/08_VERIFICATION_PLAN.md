# Verification Plan

## E1 static
- `python -m compileall -q src tests`
- package installation/import smoke.

## E2 unit
- canonicalization determinism and strict rejection;
- immutable defensive copies;
- engine success/failure/error classification;
- each relation positive and negative paths;
- CLI input validation.

## Local integration proof
Install the package from the project directory, run the generated console script against `examples/fixture.json`, then run a multi-relation harness with a deterministic simulated control adapter.

## Negative control
Run a deliberately drifting adapter under deterministic replay and verify MVK returns FAIL. This proves the harness is not merely capable of producing PASS.

## NEXY integration boundary
No real NEXY adapter execution is authorized in this task because NEXY.AI is protected from mutation and no exact authorized test endpoint/revision is part of this scope. Record NEXY integration as `NOT_VERIFIED`, not PASS.
