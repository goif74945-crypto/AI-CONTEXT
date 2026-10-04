# OXC Contracts and State Model

Classification: **EXPERIMENTAL / AI-PROPOSED**

## Contract philosophy

The renderer should not reconstruct policy from scattered booleans and visual conditions.

Instead:

```text
authoritative snapshot → OXC → explicit surface plan → renderer
```

This reduces policy drift between components.

## System states accepted by reference v1

`INIT | READY | RUNNING | VERIFYING | CONSENSUS | STABLE | FREEZE | STOP`

These names are taken from current NEXY product context. Their full backend semantics remain owned by NEXY, not OXC.

## Truth statuses accepted by reference v1

`VERIFIED | PARTIAL | UNKNOWN | CONFLICT | NOT_VERIFIED | BLOCKED`

OXC uses these only for display/eligibility constraints declared by the action descriptor.

## Roles accepted by reference v1

`OWNER | OPERATOR | AUDITOR | VIEWER`

OXC intentionally has no role inheritance.

If a future backend adds a role, v1 rejects it until the contract is updated. This is safer than interpreting `SUPERADMIN`, `SYSTEM`, or any unknown string as “probably more privileged.”

## Action kinds

- READ
- INSPECT
- EXPORT
- MUTATE
- RECOVERY

## Eligibility equation

For an action to be ENABLED, all required gates must hold:

```text
backendAllowed
AND role ∈ allowedRoles
AND systemState ∈ allowedSystemStates
AND mode permits action kind
AND system hard-state rule permits action kind
AND (requiresVerifiedTruth → truthStatus == VERIFIED)
```

There is no preference term in this equation.

## Visibility

Denied action:

- `SHOW_DISABLED` → DISABLED
- `HIDE_WHEN_DENIED` → HIDDEN

Visibility does not change executability.

## Friction lattice

```text
NONE
  ↓
ACK
  ↓
CONFIRM
  ↓
DOUBLE_CONFIRM
```

Compilation is monotonic: the highest applicable level wins.

A future implementation should not allow presentation preference to reduce compiled friction.

## Surface-plan invariants

Reference output declares:

- PRESENTATION_CANNOT_CHANGE_TRUTH
- PRESENTATION_CANNOT_GRANT_AUTHORITY
- BACKEND_DENIAL_FAILS_CLOSED
- FREEZE_AND_STOP_ARE_MANDATORY_SIGNALS
- PREFERENCES_ARE_PRESENTATION_ONLY
- IDENTICAL_INPUTS_PRODUCE_IDENTICAL_OUTPUTS

These strings are documentation signals, not proof by themselves. Tests provide the executed evidence for selected invariants.

## Preference lifecycle recommendation

Preferred integration pattern:

- session-scoped by default;
- explicit user choice;
- no inferred mood or personality authority;
- durable storage only if the user explicitly opts in and project privacy rules permit it;
- preference deletion does not alter authoritative task history.

## Renderer rule

A renderer may choose layout components, but it must not silently drop `mandatorySignals` or reinterpret action state.

If a renderer cannot represent the plan faithfully, it should fail closed rather than invent a “best effort” control.
