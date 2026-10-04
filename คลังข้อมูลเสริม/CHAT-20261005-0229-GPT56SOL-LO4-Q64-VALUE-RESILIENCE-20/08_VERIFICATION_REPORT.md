# Verification Report

## Local runtime evidence
- `python -m compileall -q src tests demo.py`: PASS.
- `python -m unittest discover -s tests -v`: PASS, 20 tests.
- Boundary/adversarial matrix: 200 sampled boundary combinations × 20 concepts inside the unit suite: PASS.
- Canonical key-order independence: PASS.
- Missing/extra/out-of-domain fail-closed tests: PASS.
- Float-constructor rejection: PASS.
- Overflow and divide-by-zero guards: PASS.
- Static AST policy scan for float literals/network imports in runtime package: PASS, zero violations.
- Demo repeated twice: byte-identical, SHA-256 `76e44d92020b63149831d39726b8be90ac4e391d5e2b647126ea49bb72aab981`.

## Evidence boundary
These results prove the standalone package under the local Python runtime used for this execution. They do **not** prove integration with the NEXY.AI implementation repository, production deployment, or Canon promotion.
