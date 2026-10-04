# v1.1 Pivot and Sibling Boundary

Classification: **AI-PROPOSED ARCHITECTURE / CURRENT CONTRACT FOR THIS LAB**

## Trigger for the pivot

Freeze Bridge v1.0 was designed before a concurrent sibling namespace became visible. During this execution, repository read-back discovered:

`คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-TRUST-UX-CONTRACT-LAB`

The sibling's own README and contracts state that it compiles an authoritative backend envelope plus role into a human-facing Trust Card, including display mode and action visibility.

That overlaps with v1.0 Freeze Bridge recovery-card concepts.

The user explicitly required this work not to duplicate another chat. Therefore v1.0 was not promoted as current. Its documents remain historical provenance and v1.1 narrows the system boundary.

## Current composable pipeline

```text
NEXY authoritative subsystem
  produces freeze/block metadata
        |
        v
FREEZE BRIDGE v1.1
  owns:
  - reason-code normalization
  - UNKNOWN_REASON compatibility
  - evidence-reference disclosure filtering
  - required-input identifier normalization
  - upstream-authorized recovery-intent intersection
  - dependency-recheck safety clamping
  - bilingual semantic explanation
  - deterministic semantic fingerprint
        |
        v
FreezeExplanation
        |
        v
TRUST UX sibling / other presentation compiler
  owns:
  - caller role
  - display mode
  - result visibility
  - UI action visibility
  - Recover affordance
  - confirmation flags
  - backend-authorization request semantics
        |
        v
UI / operator surface
```

## Freeze Bridge forbidden surface

v1.1 must not output or depend on:
- `role`;
- `display_mode`;
- `primary_action`;
- `secondary_actions`;
- UI `actions`;
- `Recover` affordance;
- `requires_backend_authorization`;
- `requires_confirmation`.

The automated test suite checks this boundary.

## Intent is not an action

`eligible_recovery_intents` is machine semantic metadata, not an executable instruction and not a UI control.

Examples:
- `PROVIDE_REQUIRED_INPUT`
- `REFRESH_EVIDENCE`
- `RECHECK_DEPENDENCY`
- `REQUEST_AUTHORITY_REVIEW`

A downstream authority must still decide whether and how any intent becomes a visible/requestable action.

Every v1.1 output therefore states:

`downstream_ui_authority_required = true`

## Authority monotonicity

For each emitted recovery intent `i`:

`i ∈ upstream_authorized_recovery_intents ∩ reason_policy_allowed_intents`

Freeze Bridge may remove an intent. It cannot invent one.

## UNKNOWN behavior

Unknown **string** reason values map to `UNKNOWN_REASON`.

Malformed non-string reason values are rejected.

This preserves forward compatibility without treating malformed structure as a valid unknown reason.

## Relationship status

- Freeze Bridge v1.1: upstream semantic normalization.
- Trust UX sibling: downstream presentation contract.
- Neither is current NEXY implementation proof.
- Neither gains authority over the other merely by existing in AI-CONTEXT.
- Integration between them is proposed, not executed.
