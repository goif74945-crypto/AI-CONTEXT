# Evidence — MCAE

- Claim: reference arbitration behavior matches DESIGN invariants covered by tests.
- Evidence class: E1 static + E2 unit.
- Environment: Python 3.13.5, local isolated container.
- Static evidence: root `evidence/STATIC_COMPILE.txt` → PASS.
- Unit command: `cd 01_multimodal_claim_arbitration && python3 -m unittest -v test_reference.py`.
- Observed: 5 tests, 5 PASS.
- Negative paths proven: top-tier contradiction → CONFLICT; invalid confidence → FREEZE; weak margin → FREEZE; same-source repetition cannot manufacture consensus.
- Limitations: modality extraction, semantic normalization, real sensor/model quality, NEXY integration, deployment and production behavior are NOT_VERIFIED.
