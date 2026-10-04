# Failure Taxonomy and FREEZE Semantics
Status: PROPOSAL grounded in NEXY project philosophy

## Why taxonomy matters
“error” is too coarse. Recovery depends on whether the problem is input, authority, evidence, determinism, dependency, security, resource or implementation failure.

## Classes
F01 INPUT_INVALID — malformed/unsupported input
F02 AUTHORITY_AMBIGUOUS — no unique governing rule
F03 AUTHORITY_CONFLICT — governing rules conflict
F04 EVIDENCE_MISSING — required proof absent
F05 EVIDENCE_STALE — proof targets wrong dependency/source
F06 EVIDENCE_CONTRADICTORY — proofs disagree
F07 DETERMINISM_VIOLATION — equivalent inputs produce illegal divergence
F08 BOUNDARY_VIOLATION — module/capability/authority boundary crossed
F09 DEPENDENCY_FAILURE — required service/tool unavailable
F10 SECURITY_POLICY — action denied by security policy
F11 RESOURCE_LIMIT — bounded resource exceeded
F12 IMPLEMENTATION_DEFECT — invariant violated by code
F13 EXTERNAL_UNTRUSTED — external claim cannot be validated
F14 PARTIAL_COMPLETION — subset succeeded but objective remains unmet
F15 UNKNOWN — cannot classify safely

## Outcome vocabulary
PASS — acceptance criteria proven
FAIL — deterministic known failure
FREEZE — continuing could create an invalid/unsafe claim or action
BLOCKED — external prerequisite unavailable
NOT_VERIFIED — output exists but proof is insufficient

## Critical rule
Do not collapse FREEZE into FAIL.
FAIL can be a verified expected outcome.
FREEZE means authority/safety/correctness does not permit selecting a legal output.

## Recovery matrix
- INPUT_INVALID -> reject with exact diagnostic
- AUTHORITY_* -> resolve authoritative source; otherwise FREEZE
- EVIDENCE_* -> regenerate/reverify; never handwave
- DETERMINISM -> isolate nondeterministic input/state and rerun
- BOUNDARY -> deny action and inspect architecture
- DEPENDENCY -> BLOCKED or deterministic fallback only if specified
- SECURITY -> deny and record reason
- RESOURCE -> bounded failure; no silent truncation if completeness required
- IMPLEMENTATION -> fix smallest root cause, regression test
- UNKNOWN -> FREEZE

## Anti-patterns
- catching every exception and returning success
- fallback values that look authoritative
- silently skipping unavailable checks
- changing requirements to fit implementation
- “best effort” release claims
