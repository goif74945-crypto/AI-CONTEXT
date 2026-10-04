# NECC Test & Verification Evidence — Published Summary

## Scope of proof
This evidence proves the standalone NECC research prototype at the frozen local bytes packed into the published bundle. It does **not** prove NEXY integration, production deployment, provider behavior, distributed durability, or cryptographic non-repudiation.

## TDD/remediation history
1. RED: implementation imports absent.
2. GREEN: 35 tests.
3. RED: R0 mutation + timezone-equivalent identity regressions.
4. Repair exposed ledger timestamp hash mismatch: 36 PASS / 1 FAIL.
5. Repair: 37 PASS.
6. RED: wire/CLI absent.
7. Repair: 44 PASS.
8. RED: metadata immutability/source-qualified snapshot defects.
9. Repair: 48 PASS.
10. RED: exact-expiry + non-finite metadata error contract.
11. Repair: 55 PASS.
12. RED: non-string metadata mapping key.
13. Repair: 56 PASS.

## Final local verification
Timestamp: `2026-10-05T01:54:20+07:00`
Runtime: Python `3.13.5`

- `python -m compileall -q -f src tests` -> PASS
- `PYTHONPATH=src python -m unittest discover -s tests -v` -> 56 / 56 PASS
- repeated CLI compilation + byte comparison -> PASS
- wheel build -> PASS
- clean venv wheel install/import -> PASS
- installed-wheel CLI == source CLI -> PASS

Deterministic example contract:
`necc:v1:62ebfc3fb96286cb8e6027314cd01f6720efbf419f5da559f366791e6ba93517`

Final wheel SHA-256:
`b670649dbb6e3851c46eabe162552001f4f1b853e498e4e95041f27132dc6440`

## Publication integrity
Encoded exact-tree path:
`bundle/necc_project_bundle.tar.gz.base64`

Readback Git blob SHA-1:
`5a8bd4b4bb11606cff33b3992345218eb273a397`

Decoded archive SHA-256 expected from the frozen local bundle:
`dd514ccf27f9302c286e62a4d5a185210add0a92f8b7b606a859c497e8067a6d`

Readback text length: 39,432.
Readback content equality against staged exact base64: PASS.
