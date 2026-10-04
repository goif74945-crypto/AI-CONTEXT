# Resume Capsule

- mission_id: `CHAT-20261005-0121-NEXY-PRIVACY-CONTEXT-FIREWALL`
- repository: `goif74945-crypto/AI-CONTEXT`
- folder: `คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-PRIVACY-CONTEXT-FIREWALL`
- proposal class: `AI_PROPOSED_SUPPLEMENTAL_CONCEPT`
- protected scope: every repository whose name contains `NEXY.AI`; every AI-CONTEXT path outside this mission folder

## Resume sequence

1. Read `00_EXECUTION_STATE.md`.
2. Read `01_TASK_CONTRACT.md`.
3. Read `10_COMPLETION_CERTIFICATE.md` and `09_VERIFICATION_EVIDENCE.md`.
4. Re-resolve current AI-CONTEXT branch HEAD.
5. Re-run `scripts/verify.py` and `scripts/fuzz_verify.py` before changing any verified code.
6. If code/policy contracts change, invalidate affected E1/E2 evidence and reopen the relevant acceptance criteria.
7. Never promote the design to canonical NEXY law without explicit authority.

## Current implementation boundary

The implementation is a standalone Python reference. A future integration must place it before provider/tool egress, and must not use a downstream verifier as a substitute for pre-egress admission control.

## Known follow-on work if explicitly authorized later

- real NEXY adapter integration;
- provider profile lifecycle/attestation;
- KMS/HSM-backed receipt keys;
- deletion/revocation propagation evidence;
- real observability integration;
- E3/E4/E5 tests;
- legal/privacy review if a jurisdiction-specific claim is required.
