# Evidence — CPAC

- Claim: exact purpose/action/resource consent matching and deterministic receipt behavior work as specified in the reference.
- Evidence class: E1 static + E2 unit.
- Environment: Python 3.13.5, local isolated container.
- Unit command: `cd 02_consent_purpose_action_compiler && python3 -m unittest -v test_reference.py`.
- Observed: 5 tests, 5 PASS.
- Negative paths proven: expired grant → ASK; purpose mismatch → ASK; wildcard grant → BLOCK.
- Limitation: legal validity of consent, identity binding, RBAC/LAW composition, UI consent capture and production integration are NOT_VERIFIED.
