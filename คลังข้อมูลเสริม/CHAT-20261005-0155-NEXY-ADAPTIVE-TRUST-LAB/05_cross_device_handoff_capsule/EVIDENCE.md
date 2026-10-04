# Evidence — CDHC

- Claim: reference capsule minimization, recursive sensitive-key removal, HMAC tamper detection, expiry and target binding work as designed.
- Evidence class: E1 static + E2 unit.
- Environment: Python 3.13.5, local isolated container.
- Unit command: `cd 05_cross_device_handoff_capsule && python3 -m unittest -v test_reference.py`.
- Observed: 5 tests, 5 PASS.
- Negative paths proven: tamper → SIGNATURE_MISMATCH; expiry → EXPIRED; target mismatch → FREEZE; unapproved root fields omitted; sensitive nested key omitted.
- Limitations: confidentiality, secure key distribution, replay defense, device attestation, key rotation and production transport are NOT_VERIFIED.
