# C3 — Evidence Portability Compiler (EPC)

> **AI_PROPOSED_CONCEPT / NON-CANONICAL**

## Objective
Decide whether evidence collected in one context can legally support the same claim in another context, without treating old proof as universally reusable.

## Decision states
- `PORTABLE`: every supplied context dimension is governed and no invalid/reverify condition is triggered.
- `REVERIFY`: artifact/claim may be related, but one or more policy dimensions or freshness rules require new proof.
- `INVALID`: evidence cannot support the target claim/context.
- `FREEZE`: required portability information/policy is missing or incoherent.

## Policy rules per dimension
- `MUST_EQUAL`: any change invalidates portability.
- `REVERIFY_IF_DIFFERENT`: change requires fresh verification.
- `CAN_DIFFER`: difference is explicitly authorized by portability policy.

## Fail-closed coverage rule
The union of source and target context dimensions must be governed by policy. Omitting `code_sha`, `runtime`, `provider`, `schema`, `region`, or another supplied dimension cannot silently turn changed evidence into `PORTABLE`.

## Evidence-class law
Evidence class is matched exactly against target-accepted classes. The prototype deliberately refuses simplistic numeric substitution such as “E5 is higher than E2 therefore it proves E2,” because evidence classes prove different propositions.

## Time law
- expired exactly at the expiry instant => `REVERIFY`;
- evaluation earlier than collection => `INVALID/TEMPORAL_INCONSISTENCY`;
- missing required evaluation time => `FREEZE`.

## Why NEXY could benefit
NEXY depends on exact-revision evidence and provider-independent workers. EPC can serve as a gate before reusing test proof across code, runtime, provider, policy, schema, or environment changes.

## Code / tests
- Code: `src/nexy_aux/portability.py`
- Tests: `tests/test_portability.py`, `tests/test_properties.py`, `tests/test_hardening.py`
