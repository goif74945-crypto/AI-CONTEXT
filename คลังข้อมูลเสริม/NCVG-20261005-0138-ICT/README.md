# NCVG — NEXY Companion Verification Gate

> **Status:** AI-PROPOSED COMPANION PROJECT. This is not canonical NEXY.AI law and is not implementation proof for NEXY.AI.

NCVG is a standalone, model-agnostic, fail-closed semantic verifier for NEXY-compatible execution evidence. It lives outside any repository whose name contains `NEXY.AI` and can be integrated through JSON/stdin/stdout without modifying NEXY.AI itself.

## Why it exists
AI-CONTEXT already defines Task Contracts, Requirement Ledgers, Evidence Records, Execution Records, evidence classes, and a strict rule that design/implementation/runtime/deployment truth must not be conflated. JSON Schema validates shape, but cross-record semantic consistency still needs an admission gate.

NCVG fills that gap by checking whether a claimed PASS is actually supported by the bundle supplied to the gate.

## Decision model
`bundle -> canonicalize -> semantic checks -> requirement/evidence admission -> mutation-boundary checks -> ALLOW | FREEZE`

## Implemented checks
- mandatory requirements need real PASS evidence;
- evidence classes are explicitly admitted per requirement;
- stale/wrong-commit evidence may be rejected;
- duplicate IDs are rejected;
- protected/forbidden mutation targets freeze;
- execution record must be PASS;
- malformed API inputs freeze;
- canonical JSON SHA-256 is deterministic.

## Run
```bash
python -m nexy_gate validate examples/pass_bundle.json
python -m nexy_gate validate examples/freeze_bundle.json
python -m nexy_gate manifest examples/pass_bundle.json
python -m unittest discover -v
```

Exit codes: `0` ALLOW/success, `2` FREEZE, `64` malformed/read input.

NCVG never executes mutations. It is not authorization, deployment proof, cryptographic identity, or evidence that current NEXY.AI already integrates it.
