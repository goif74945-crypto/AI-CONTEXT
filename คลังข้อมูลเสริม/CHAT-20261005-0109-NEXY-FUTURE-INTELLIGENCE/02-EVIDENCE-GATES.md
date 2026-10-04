# Evidence Gates

Core rule: a claim is only as strong as the evidence class capable of proving it.

| Claim | Minimum evidence |
|---|---|
| File exists | repository/filesystem read |
| Syntax parses | parser/compiler |
| Unit behavior | executed unit test |
| Integration works | integration test with real boundary or faithful test environment |
| UI renders | browser/runtime inspection |
| User flow works | end-to-end execution |
| Performance target | measured benchmark under stated conditions |
| Security property | threat-specific test/review; never absence-of-errors |
| Deployment works | deployment state + health/runtime probe |
| Data is real | authoritative source provenance |
| No regression | relevant regression suite |
| Requirement complete | requirement-to-evidence coverage = 100% for required items |

## Gate model
G0 Contract: objective, scope, immutable rules, acceptance criteria known.
G1 Preconditions: dependencies and authority resolved.
G2 Build/Artifact: expected artifact exists.
G3 Static validity: syntax/schema/type/static checks.
G4 Behavioral validity: tests execute claimed behavior.
G5 Integration validity: boundaries work together.
G6 Runtime validity: actual runtime state observed.
G7 Regression validity: protected behaviors remain valid.
G8 Evidence closure: every required claim has evidence.
G9 Completion: only now may status be COMPLETE.

## Anti-patterns
- "No error" != correct.
- "Tool said success" != postcondition.
- "Code looks right" != runtime proof.
- "Tests passed" != requirement coverage unless tests map to requirements.
- "Deployed" != healthy.
- "Has citations" != source supports claim.

## Evidence record schema
claim_id; claim; requirement_id; evidence_class; source; observed_at; environment; method; result; limitations; verifier; freshness; artifact_hash_or_ref.

## Negative evidence
Absence of evidence is UNKNOWN, not FAIL, unless the acceptance oracle defines absence as failure.

## Completion invariant
COMPLETE iff every mandatory requirement is PASS and every completion-critical claim has matching evidence. Any UNKNOWN/NOT_VERIFIED critical item prevents COMPLETE.
