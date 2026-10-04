# Remediation History

## RH-001 — Adversarial noise-chain property test
- Observed: 40 PASS / 1 FAIL after adding property tests.
- Failure: expected `E_SECRET_EGRESS`, received early `MISSING_ARTIFACT`.
- Root cause: test generator inserted dependent noise steps in reverse topological order.
- Repair: generate noise chain in dependency order before target steps.
- Verification: property test passed; full suite became 41/41 PASS.
- Classification: TEST_HARNESS_DEFECT, not product defect.

## RH-002 — Hardening gaps intentionally exposed
Ten tests were added before implementation change. They correctly failed for:
- non-finite canonical numbers;
- ungoverned portability dimension;
- exact expiry boundary;
- evaluation before collection;
- nondeterministic failure oracle;
- conflicting equalities;
- exists/not-exists correction conflict;
- malformed `supersedes`;
- duplicate tool output names;
- missing fingerprints on early terminal results.

Repairs implemented the stricter contracts rather than weakening assertions.

## RH-003 — Recursive fingerprint helper regression
- Observed: focused hardening suite raised `RecursionError` in C1 `_finish()`.
- Root cause: scripted text replacement replaced the helper's own two-line body, turning it into self-recursion.
- Repair: restore helper to set SHA-256 then return the result.
- Verification: hardening suite 10/10 PASS.
- Classification: IMPLEMENTATION_REGRESSION introduced during hardening, detected before final regression.

## RH-004 — Property test stale after stricter C3 contract
- Observed: full suite 50 PASS / 1 FAIL.
- Root cause: legacy property test specified a policy only for `runtime`, while evidence/target records also contained `code` and `region`; new C3 law correctly freezes ungoverned dimensions.
- Repair: update test input to explicitly govern all three dimensions (`code=MUST_EQUAL`, `runtime=<tested rule>`, `region=CAN_DIFFER`).
- Verification: focused property test PASS; full suite 51/51 PASS.
- Classification: TEST_EXPECTATION_STALE_AFTER_INTENTIONAL_CONTRACT_HARDENING.
