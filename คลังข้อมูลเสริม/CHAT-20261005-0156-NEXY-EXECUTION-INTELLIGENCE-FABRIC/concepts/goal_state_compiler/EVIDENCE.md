# Goal-State Compiler — Evidence

- Implementation: `engine.py`
- Tests: `test_engine.py`
- Evidence class: E1 compile + E2 unit behavior.
- Verified behaviors: order-independent contract identity, PASS path, missing fact → NOT_VERIFIED, forbidden effect → FREEZE, tampered contract rejection.
- Fresh suite result before persistence: included in root `evidence/LOCAL-VERIFY.json` after final verification.
- Deployment/live NEXY integration: NOT_VERIFIED.
