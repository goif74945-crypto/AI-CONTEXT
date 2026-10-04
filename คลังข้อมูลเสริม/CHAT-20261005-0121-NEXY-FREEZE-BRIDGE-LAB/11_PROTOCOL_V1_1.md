# Freeze Bridge Protocol v1.1

Classification: **AI-PROPOSED PROTOCOL / REFERENCE IMPLEMENTATION**

## Input contract — FreezeEvent

Required:
- `protocol_version = "1.1"`
- `event_id`
- `reason_code`
- `status`
- `blocking_layer`
- `recovery_owner`
- `authorized_recovery_intents`

Optional/defaulted:
- `disclosure = PUBLIC`
- `locale = en`
- `dependency_recheck_safe = false`
- `missing_inputs = []`
- `evidence_refs = []`
- `context_label = null`

## Status enum

- FROZEN
- BLOCKED
- NOT_VERIFIED
- UNKNOWN
- CONFLICT

## Reason taxonomy

Known reference reasons:
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

Unknown string reasons fail safe to `UNKNOWN_REASON`. Non-string values reject.

## Recovery intents

- PROVIDE_REQUIRED_INPUT
- RESOLVE_AUTHORITY_CONFLICT
- REFRESH_EVIDENCE
- RECHECK_DEPENDENCY
- REQUEST_AUTHORITY_REVIEW
- ESCALATE_OPERATOR
- ADJUST_SCOPE
- ACKNOWLEDGE_STATE

These are semantic intents only. They are not buttons, permissions or operations.

## Intent law

`eligible = authorized_upstream ∩ allowed_by_reason_policy`

Ordering is fixed by `INTENT_PRIORITY` and does not depend on input list ordering.

## Required-input law

`required_inputs` is emitted only for MISSING_REQUIRED_INPUT.

Values are identifiers such as `target_branch`; secret values do not belong in this protocol.

## Disclosure law

PUBLIC / INTERNAL:
- supplied evidence references are deterministically sorted.

RESTRICTED:
- reference implementation keeps only `public:` references.

RESTRICTED + SECURITY_INTEGRITY:
- all evidence references are suppressed.

The prefix convention is a prototype boundary, not a production ACL system.

## Dependency recheck law

Input `dependency_recheck_safe=true` is not sufficient.

Output becomes true only if:
1. the reason policy does not force unsafe;
2. RECHECK_DEPENDENCY survives the intent intersection;
3. the upstream safety flag is true.

UNKNOWN_REASON, security/integrity, authority/policy conflict, illegal state, permission denied and internal invariant force false.

## Localization law

English/Thai wording may change `title` and `summary` only.

Localization must not change:
- status;
- reason;
- intents;
- disclosure;
- required-input identifiers;
- dependency-recheck semantics;
- owner;
- blocking layer.

## Output contract — FreezeExplanation

- protocol_version
- event_id
- status
- reason_code
- title
- summary
- blocking_layer
- recovery_owner
- required_inputs[]
- eligible_recovery_intents[]
- evidence_refs[]
- disclosure
- dependency_recheck_safe
- downstream_ui_authority_required = true
- fingerprint

## Fingerprint

SHA-256 over canonical normalized input + policy version + explanation content.

It is content identity, not a signature and not authorization.

## Determinism

Compiler uses:
- no system clock;
- no randomness;
- no network;
- no model call;
- no filesystem mutation;
- fixed sorting and intent ordering.

## Error behavior

Malformed input:
- library raises `FreezeBridgeError`;
- CLI exits 2 and writes structured FAIL JSON to stderr;
- no partial explanation is emitted.

## Security boundary

The protocol is designed to minimize presentation-layer authority:
- no role;
- no display mode;
- no action execution;
- no secret value requirement;
- no automatic unfreeze;
- no bypass/force token.

A future production integration must replace prototype disclosure prefixes with actual NEXY ACL/data-classification authority.
