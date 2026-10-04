# Defect / Failure Log

## F-001 — Expected TDD RED
- Symptom: initial six test files failed with `ERR_MODULE_NOT_FOUND` because implementation did not yet exist.
- Classification: expected RED state, not hidden.
- Evidence: `evidence/01_RED.txt`.
- Correction: implemented shared Q64.64 substrate and five engines.
- Re-verification: full suite PASS.

## F-002 — Concurrent GitHub write conflict
- Symptom: first durable checkpoint write returned HTTP 409 because another chat advanced AI-CONTEXT `main`.
- Root cause: concurrent independent sessions writing the same branch.
- Correction: refreshed branch HEAD and retried only this unique namespace; no force push or sibling overwrite.
- Re-verification: checkpoint create returned commit `917030fa00c2a1b7422b37f57a7b42f39cbbd6a9`; final readback still required after full publication.

## Formula review outcome
The implemented backlog/delay equations were cross-checked against Le Boudec/Thiran tutorial material. Chain composition is explicitly scoped to the fluid rate-latency service-curve abstraction. No silent packetization/general-scheduler claim is made.
