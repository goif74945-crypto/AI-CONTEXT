# OXC Reference Architecture

Classification: **EXPERIMENTAL / AI-PROPOSED**

## 1. Trust boundary

OXC receives a sanitized `CoreSnapshot`. The caller remains responsible for deriving that snapshot from authoritative backend state.

OXC treats every field as untrusted input at the contract boundary and validates supported values.

The proposal deliberately avoids querying databases, sessions, providers or environment variables. This keeps compiler output a pure function of explicit input.

## 2. Input domains

### CoreSnapshot

Contains:

- schema version;
- system state;
- truth status;
- current role;
- current mode;
- blocking reasons;
- backend-described actions.

### ActionDescriptor

Each action declares:

- stable id and label;
- action kind;
- `backendAllowed`;
- explicit allowed roles;
- explicit allowed system states;
- whether VERIFIED truth is required;
- risk;
- reversibility;
- minimum friction;
- denied-action visibility policy.

Important design choice: OXC does not derive backend authorization from role hierarchy. The backend supplies `backendAllowed`, and the presentation compiler may only narrow further.

### PreferenceEnvelope

Contains presentation-only choices:

- detail;
- density;
- language;
- motion;
- friendly tone.

No preference field is permitted in the action-eligibility path.

## 3. Compiler stages

### Stage A — Contract normalization

Rejects:

- unsupported enums;
- malformed objects;
- duplicate action ids;
- empty role/state allow-lists;
- empty required strings.

Failure mode: `OxcContractError`, code `INVALID_INPUT`.

### Stage B — Authority narrowing

An action accumulates deterministic denial reasons:

- `BACKEND_DENIED`
- `ROLE_DENIED`
- `STATE_DENIED`
- `VIEW_MODE_READ_ONLY`
- `SYSTEM_STOPPED`
- `SYSTEM_FROZEN`
- `VERIFIED_TRUTH_REQUIRED`

Any denial prevents ENABLED state.

Visibility policy may map denial to DISABLED or HIDDEN, but never to ENABLED.

### Stage C — Friction compilation

Friction is monotonic. OXC chooses the maximum requirement across:

- descriptor minimum;
- risk;
- reversibility;
- recovery floor.

Ordering:

```text
NONE < ACK < CONFIRM < DOUBLE_CONFIRM
```

Current proposal mapping:

- LOW → NONE
- MEDIUM → ACK
- HIGH → CONFIRM
- CRITICAL → DOUBLE_CONFIRM
- REVERSIBLE → NONE
- REVERSIBLE_WITH_COST → CONFIRM
- IRREVERSIBLE → DOUBLE_CONFIRM
- RECOVERY → at least CONFIRM

This mapping is proposal policy, not NEXY canon.

### Stage D — Truth banner

Priority:

1. FREEZE
2. STOP
3. truth CONFLICT
4. truth BLOCKED
5. UNKNOWN
6. NOT_VERIFIED
7. PARTIAL
8. VERIFIED

FREEZE and STOP are mandatory surface signals.

### Stage E — Progressive disclosure

User preference selects a normal detail target:

- COMPACT → MINIMAL
- BALANCED → STANDARD
- DEEP → DIAGNOSTIC

Critical conditions may raise the minimum disclosure level. They never lower it.

Current proposal forces DIAGNOSTIC for:

- FREEZE;
- STOP;
- CONFLICT;
- BLOCKED;
- any enabled DOUBLE_CONFIRM action.

UNKNOWN/NOT_VERIFIED force at least STANDARD.

### Stage F — SurfacePlan

Output contains:

- system pulse;
- truth status;
- truth banner;
- disclosure level;
- mandatory signals;
- action plans;
- copied presentation preferences;
- declared invariants.

## 4. Determinism

The compiler core intentionally contains no:

- clock reads;
- random values;
- network;
- filesystem;
- database;
- process execution;
- environment lookup;
- hidden model call.

Identical validated input therefore has no designed nondeterministic source.

## 5. State ownership

OXC owns no durable state.

Caller owns:
- authoritative Core state;
- permission state;
- risk/action metadata;
- preference lifecycle.

Renderer owns:
- visual rendering only.

OXC owns:
- deterministic compilation from the explicit snapshot into a surface plan.

## 6. Evolution law

Future versions should use explicit schema versions.

Breaking interpretation changes require a new schema version or an explicit compatibility adapter. Unknown versions must fail closed.
