# TASK CONTRACT — NEXY Privacy Context Firewall

## Identity
- mission_id: CHAT-20261005-0121-NEXY-PRIVACY-CONTEXT-FIREWALL
- deliverable_type: AI-proposed supplemental engineering lab
- authority_class: proposal, not canonical NEXY requirement
- target_store: AI-CONTEXT/คลังข้อมูลเสริม/<mission_id>/

## OBJECTIVE
Create and verify a standalone deterministic privacy-context compiler that can serve as a future integration reference for NEXY. It must reduce context exposure before external AI/provider/tool calls and must fail closed when privacy policy is incomplete or violated.

## REQUIRED OUTPUT
1. Architecture and threat model.
2. Explicit policy/data contracts.
3. Executable Python reference implementation with no third-party runtime dependencies.
4. JSON schemas and example fixtures.
5. Unit and negative-path tests.
6. Deterministic CLI.
7. Verification record and final audit.
8. Durable execution state/resume capsule.

## INPUTS
- User directive in this conversation.
- AI-CONTEXT execution law and verification law.
- NEXY project overview and current normalized authority boundary.
- Official NIST Privacy Framework material and OWASP LLM02 Sensitive Information Disclosure as external research context only.

## IMMUTABLE REQUIREMENTS
- Do not modify NEXY.AI repositories.
- Do not silently promote this design into canonical NEXY law.
- Unknown data classification, missing purpose, or missing destination policy must not silently pass.
- Minimum necessary fields only.
- Secret values must not appear in generated audit explanations/receipts.
- Same normalized input + policy must produce the same decision structure and receipt hash.
- Verification claims require matching evidence.

## CORE MODEL
A request consists of:
- task purpose;
- destination/provider/tool identity;
- context fields;
- each field's classification, source, purposes, retention hint, and egress constraints;
- destination profile;
- policy version.

The compiler emits exactly one of:
- ALLOW with a minimized payload, retention leases, decisions, and a deterministic receipt; or
- FREEZE with explicit violation codes and no payload.

## INITIAL CLASSIFICATION SET
- PUBLIC
- INTERNAL
- PERSONAL
- SENSITIVE
- SECRET
- CREDENTIAL

Classification is policy metadata, not automatic detection. Automatic detection may be proposed later but cannot be treated as authoritative without evidence.

## ACCEPTANCE CRITERIA
AC01 unknown classification => FREEZE.
AC02 empty/unknown task purpose => FREEZE.
AC03 unknown destination => FREEZE.
AC04 fields not required for the stated purpose are removed.
AC05 destination max classification is enforced.
AC06 field-level egress deny is enforced.
AC07 SECRET/CREDENTIAL are denied from external egress by default.
AC08 allowed retained fields receive bounded retention leases.
AC09 audit output contains field IDs/paths and reasons, not denied raw values.
AC10 deterministic canonicalization produces stable receipt hashes.
AC11 malformed envelopes fail with typed errors/freeze, never implicit allow.
AC12 CLI returns machine-readable JSON.
AC13 tests cover positive, negative, deterministic, privacy-leak, and edge cases.
AC14 all persisted artifacts are read back after write.
AC15 final status cannot be COMPLETE until tests and read-back verification pass.

## EVIDENCE REQUIREMENTS
- E0: persisted file presence/read-back.
- E1: Python compile/import + JSON schema parse + deterministic serialization checks.
- E2: executed unit tests covering AC01–AC13.
- No claim of E3/E4/E5/E6 because this lab is not integrated or deployed.

## FORBIDDEN BEHAVIOR
- Guessing missing privacy metadata.
- Logging denied raw values.
- Treating a provider name as trusted without an explicit profile.
- Expanding to legal advice/compliance certification.
- Editing unrelated AI-CONTEXT files.
- Editing or testing the NEXY.AI implementation repository.

## FAILURE CONDITIONS
- Any acceptance criterion lacks evidence.
- Test suite has failures/errors.
- Persisted content differs from verified local content.
- Protected-scope mutation occurs.
- Proposal/canonical boundary becomes ambiguous.

## STOP CONDITIONS
Stop with BLOCKED/FREEZE rather than improvising if the required repository becomes inaccessible, writes cannot be read back, or verification cannot bind to the persisted content.

## EXTERNAL RESEARCH NOTE
As of 2026-10-05, NIST presents Privacy Framework 1.1 as an Initial Public Draft / update effort rather than final binding law, and OWASP's 2025 LLM Top 10 identifies Sensitive Information Disclosure as LLM02. These references motivate risk controls but do not define NEXY requirements.
