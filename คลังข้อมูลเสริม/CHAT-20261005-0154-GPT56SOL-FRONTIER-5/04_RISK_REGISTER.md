# Risk Register

| ID | Risk | Current mitigation | Status |
|---|---|---|---|
| R1 | Structural drift misses semantic value drift | Probe catalog may include status/shape only in reference implementation; production probes should add domain-specific assertions | OPEN |
| R2 | ABI schema hash equality is too rigid for backward-compatible evolution | Future version negotiation rules required | OPEN |
| R3 | Taint verification could be abused if evidence IDs are not authenticated | Production verifier must bind evidence cryptographically | OPEN |
| R4 | Compensation cannot undo every real-world side effect | ETC reports residue and FREEZE rather than claiming atomicity | MITIGATED |
| R5 | Authority lease content hash is not an authentication signature | Design explicitly blocks production use without signed issuance | MITIGATED |
| R6 | No live NEXY integration test | Integration remains NOT_VERIFIED | OPEN |
