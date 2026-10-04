> **HISTORICAL / SUPERSEDED v1.0**
>
> This file records the initial design before the concurrent `NEXY Trust UX Contract Lab` was discovered. Its UI/action-oriented portions are **not current**. The current Freeze Bridge contract is v1.1 and is defined by `README.md`, `10_V1_1_PIVOT_AND_SIBLING_BOUNDARY.md`, and `11_PROTOCOL_V1_1.md`. Historical text is retained for provenance only.

# Protocol Specification v1.0

Classification: **AI-PROPOSED PROTOCOL**

## 1. Input: Freeze Event

Required core fields:

| Field | Meaning |
|---|---|
| protocol_version | Must be `1.0` |
| event_id | Stable opaque event identifier |
| reason_code | Machine reason category |
| status | FROZEN/BLOCKED/NOT_VERIFIED/UNKNOWN/CONFLICT |
| blocking_layer | Non-secret logical layer identifier |
| recovery_owner | USER/OPERATOR/SYSTEM/EXTERNAL_DEPENDENCY/NONE |
| authorized_actions | Actions authorized upstream |

Optional/defaulted fields:
- disclosure: PUBLIC
- locale: en
- retryable: false
- missing_inputs: []
- evidence_refs: []
- context_label: null

## 2. Reason codes

Reference v1 codes:
- MISSING_REQUIRED_INPUT
- AUTHORITY_CONFLICT
- POLICY_CONFLICT
- INSUFFICIENT_EVIDENCE
- DEPENDENCY_UNAVAILABLE
- SECURITY_INTEGRITY
- INVALID_STATE_TRANSITION
- STALE_EVIDENCE
- PERMISSION_DENIED
- INTERNAL_INVARIANT
- UNKNOWN_REASON

Unknown string values intentionally normalize to `UNKNOWN_REASON`.

This behavior differs from other enums because future reason expansion should fail safe without causing the presentation bridge itself to fabricate a specific classification.

## 3. Action codes

- PROVIDE_MISSING_INPUT
- REVIEW_CONFLICT
- RETRY_AFTER_DEPENDENCY
- OPEN_EVIDENCE
- REQUEST_AUTHORITY_REVIEW
- CONTACT_OPERATOR
- ACKNOWLEDGE
- CHANGE_SCOPE
- WAIT_FOR_SYSTEM

There is deliberately no FORCE, BYPASS, AUTO_UNFREEZE or arbitrary override action.

## 4. Effective action law

```text
EffectiveActions =
  StablePriorityOrder(
    AuthorizedActions ∩ ReasonPolicyAllowedActions
  )
```

Localization has no effect on this set.

## 5. Retry law

`retryable=true` in the input is only a candidate signal.

Effective retryability becomes true only when:
1. reason policy does not force non-retryable;
2. RETRY_AFTER_DEPENDENCY is an effective action;
3. upstream retryable flag is true.

Authority/policy/security/internal-invariant/unknown classes can force non-retryable.

## 6. Missing inputs

Only emitted for `MISSING_REQUIRED_INPUT`.

The reference protocol treats values as **field identifiers**, not secret values. Example:
- `target_branch`
- `expected_head`

Do not place passwords, tokens, private keys or secret values in this list.

## 7. Evidence references

Evidence refs are opaque references, not raw evidence payloads.

Reference prefixes used by this prototype:
- `public:`
- `internal:`
- `secret:`

Restricted events filter references conservatively. A production system would need a canonical disclosure/ACL binding rather than relying on string prefixes.

## 8. Output: Recovery Card

Fields:
- protocol_version
- event_id
- status
- reason_code
- title
- summary
- blocking_layer
- recovery_owner
- needed
- actions[]
- evidence_refs
- disclosure
- retryable
- fingerprint

## 9. Fingerprint

SHA-256 over canonical JSON containing:
- policy version;
- normalized event;
- card content excluding the fingerprint field itself.

Purpose:
- detect accidental presentation-policy drift;
- bind a rendered recovery card to its normalized input/policy;
- support deterministic snapshots.

It is **not** a signature and provides no authenticity by itself.

## 10. Validation bounds

Reference implementation hard bounds:
- event_id ≤ 128 chars;
- blocking_layer ≤ 96;
- context_label ≤ 160;
- missing_inputs ≤ 24 items, each ≤ 96;
- evidence_refs ≤ 24 items, each ≤ 160;
- authorized_actions ≤ supported action count.

Forbidden control characters are rejected from human-provided string fields.

## 11. Error contract

Invalid input:
- no Recovery Card;
- `FreezeBridgeError` in library use;
- CLI returns exit code 2;
- stderr emits JSON with `status: FAIL`.

## 12. Compatibility boundary

This protocol is not current NEXY build authority. Before adoption:
- map real NEXY enums/reason taxonomy;
- map real authorization model;
- map real disclosure model;
- map DOC-C/D support;
- execute integration/UI/security tests;
- bind exact-version evidence.
