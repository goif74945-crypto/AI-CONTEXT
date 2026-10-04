# Verification Evidence

Environment: Python 3.13.5, isolated local container, no network required by package.

## E1 static
Command: `PYTHONPATH=src python3 -m compileall -q src tests`
Result: PASS. Artifact: `evidence/static-output.txt`.

## E2 unit + negative paths
Command: `PYTHONPATH=src python3 -m unittest discover -s tests -v`
Expected final result after repair: all tests PASS. Artifact: `evidence/unit-test-output.txt`.
Coverage includes Q64 arithmetic, overflow, nonfinite decimal rejection, float rejection, division by zero, each of 20 registered systems, invalid unit domain, zero-cost/zero-weight failures and deterministic tie-break.

## E2 deterministic property sweep
Artifact: `evidence/property-sweep.txt`.
Covers a 17x17x17 Q64 lattice across six bounded composite scorers plus signed arithmetic round-trip cases. Final observed checks are recorded verbatim in artifact.

## E3 standalone integration
`tests/test_integration.py` composes all 20 systems into one representative adapter-neutral flow and proves ranking is unchanged when input-map insertion order is reversed. This is standalone package integration only, not NEXY.AI integration.

## Integrity hashes
`evidence/SHA256SUMS.txt` hashes package source, tests and evidence artifacts. Hashes must be regenerated after every mutation.

## Evidence limits
- NEXY.AI integration: NOT_VERIFIED.
- Production runtime: NOT_VERIFIED.
- Deployment: NOT_VERIFIED.
- Security of a future adapter: NOT_VERIFIED.
- User preference/benefit in real UX research: NOT_VERIFIED.
- Claim that these ideas are globally unique or objectively better than every prior lab: NOT_VERIFIED. This lab provides targeted collision avoidance and stronger composability, not a universal superiority proof.
