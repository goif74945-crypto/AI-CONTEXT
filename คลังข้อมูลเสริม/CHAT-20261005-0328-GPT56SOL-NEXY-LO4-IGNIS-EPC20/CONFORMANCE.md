# DESIGN-CODE-TEST CONFORMANCE

- S01 Action Reversibility Preflight: DESIGN invariant -> code handler `_s01` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S02 Queue Wait Fairness Monitor: DESIGN invariant -> code handler `_s02` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S03 Non-Goal Creep Sentinel: DESIGN invariant -> code handler `_s03` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S04 Retry Harm Guard: DESIGN invariant -> code handler `_s04` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S05 Precondition Disclosure Gate: DESIGN invariant -> code handler `_s05` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S06 Session Expiry Transparency Gate: DESIGN invariant -> code handler `_s06` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S07 Session Revocation Completeness Proof: DESIGN invariant -> code handler `_s07` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S08 Structured Error Actionability Gate: DESIGN invariant -> code handler `_s08` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S09 Partial Success Prohibition Gate: DESIGN invariant -> code handler `_s09` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S10 State Disclosure Consistency Gate: DESIGN invariant -> code handler `_s10` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S11 Secret Placeholder Integrity Gate: DESIGN invariant -> code handler `_s11` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S12 Ownership Export Completeness Verifier: DESIGN invariant -> code handler `_s12` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S13 Capability Claim Calibration Gate: DESIGN invariant -> code handler `_s13` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S14 Idempotency Feedback Gate: DESIGN invariant -> code handler `_s14` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S15 Rate-Limit Recovery Contract Auditor: DESIGN invariant -> code handler `_s15` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S16 Audit Correlation Completeness Compiler: DESIGN invariant -> code handler `_s16` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S17 Cancellation Propagation Witness: DESIGN invariant -> code handler `_s17` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S18 Stale-Job User Impact Gate: DESIGN invariant -> code handler `_s18` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S19 Evidence Explanation Loss Auditor: DESIGN invariant -> code handler `_s19` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.
- S20 Canonical Reason Precedence Resolver: DESIGN invariant -> code handler `_s20` -> behavior tests in `tests/test_lo4_epc20.py`; adversarial cross-check where applicable. STATUS=CONFORMANT_LOCAL.

Shared Q64/canonicalization invariants map to `Q64`, `canonical_digest`, and `evaluate`, exercised by numeric, malformed, float-forbidden, key-order and determinism tests.
