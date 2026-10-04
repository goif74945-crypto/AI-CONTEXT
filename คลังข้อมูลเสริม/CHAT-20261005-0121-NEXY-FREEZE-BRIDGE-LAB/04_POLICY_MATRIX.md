# Policy Matrix

Classification: **AI-PROPOSED REFERENCE POLICY**

This matrix constrains presentation/recovery behavior only. It does not redefine NEXY Core law.

## Reason policy

| Reason | Retry forced off | Primary user meaning | Allowed action codes |
|---|---:|---|---|
| MISSING_REQUIRED_INPUT | No | Required input is absent; do not guess | PROVIDE_MISSING_INPUT, CHANGE_SCOPE, ACKNOWLEDGE |
| AUTHORITY_CONFLICT | Yes | Credible authorities conflict | REVIEW_CONFLICT, OPEN_EVIDENCE, REQUEST_AUTHORITY_REVIEW, ACKNOWLEDGE |
| POLICY_CONFLICT | Yes | Requested action conflicts with active policy | REVIEW_CONFLICT, REQUEST_AUTHORITY_REVIEW, CHANGE_SCOPE, ACKNOWLEDGE |
| INSUFFICIENT_EVIDENCE | No | Proof is not strong/current enough | PROVIDE_MISSING_INPUT, OPEN_EVIDENCE, CHANGE_SCOPE, ACKNOWLEDGE |
| DEPENDENCY_UNAVAILABLE | No | Required dependency is unavailable | RETRY_AFTER_DEPENDENCY, WAIT_FOR_SYSTEM, CHANGE_SCOPE, ACKNOWLEDGE |
| SECURITY_INTEGRITY | Yes | Security/integrity containment | CONTACT_OPERATOR, ACKNOWLEDGE |
| INVALID_STATE_TRANSITION | Yes | Requested transition is illegal from current state | OPEN_EVIDENCE, REQUEST_AUTHORITY_REVIEW, ACKNOWLEDGE |
| STALE_EVIDENCE | No | Existing proof does not bind current target | OPEN_EVIDENCE, RETRY_AFTER_DEPENDENCY, ACKNOWLEDGE |
| PERMISSION_DENIED | Yes | Current authority cannot perform action | REQUEST_AUTHORITY_REVIEW, CONTACT_OPERATOR, ACKNOWLEDGE |
| INTERNAL_INVARIANT | Yes | Internal invariant violated | OPEN_EVIDENCE, CONTACT_OPERATOR, ACKNOWLEDGE |
| UNKNOWN_REASON | Yes | Cause cannot be classified safely | CONTACT_OPERATOR, ACKNOWLEDGE |

## Canonical action ordering

The reference engine emits only effective actions and orders them deterministically:

1. PROVIDE_MISSING_INPUT
2. REVIEW_CONFLICT
3. OPEN_EVIDENCE
4. REQUEST_AUTHORITY_REVIEW
5. RETRY_AFTER_DEPENDENCY
6. WAIT_FOR_SYSTEM
7. CHANGE_SCOPE
8. CONTACT_OPERATOR
9. ACKNOWLEDGE

Input action order is never treated as authority or priority.

## Disclosure policy

### PUBLIC
Supplied evidence references may be shown after deterministic sorting.

### INTERNAL
Supplied evidence references may be shown to a surface already authorized for INTERNAL data.

### RESTRICTED
Only references explicitly marked `public:` survive the reference filter.

### RESTRICTED + SECURITY_INTEGRITY
All evidence references are suppressed.

## Unknown-reason law

Unknown future reason strings are deliberately not rejected as a specific cause and not auto-mapped to a "nearest" known reason.

They become:
- reason_code = UNKNOWN_REASON;
- retryable = false;
- generic explanation;
- only upstream-authorized CONTACT_OPERATOR/ACKNOWLEDGE actions that are allowed by unknown policy.

This preserves uncertainty rather than replacing it with a convenient story.

## Action-law examples

### Example A
Input authorized:
`[PROVIDE_MISSING_INPUT, CONTACT_OPERATOR, CHANGE_SCOPE]`

Reason:
`MISSING_REQUIRED_INPUT`

Output:
`[PROVIDE_MISSING_INPUT, CHANGE_SCOPE]`

CONTACT_OPERATOR is dropped because the reason policy does not allow it in this reference profile.

### Example B
Input:
- reason = SECURITY_INTEGRITY
- retryable = true
- authorized includes RETRY_AFTER_DEPENDENCY

Output:
- retryable = false
- RETRY_AFTER_DEPENDENCY absent

The presentation bridge cannot weaken containment.

## Policy self-check

The included self-check enumerates:
- 11 reason codes;
- 2 locales;
- 3 disclosure classes;
- 5 statuses.

Total: **330 cases**.

For every generated case it verifies:
- deterministic repeat output;
- emitted actions are a subset of reason policy;
- restricted security cases leak no evidence references;
- restricted security cases are non-retryable;
- unknown-reason cases are non-retryable.

Observed in this execution: **330/330 PASS**.
