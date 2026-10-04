# Architecture — NEXY Freeze Bridge

Classification: **AI-PROPOSED SYSTEM DESIGN**

## 1. Architectural position

```text
NEXY Core / Judge / Policy / Runtime
        |
        | already-decided Freeze Event
        v
+-----------------------------+
|  FREEZE BRIDGE              |
|  1. Validate                |
|  2. Normalize               |
|  3. Apply disclosure law    |
|  4. Intersect safe actions  |
|  5. Localize presentation   |
|  6. Fingerprint output      |
+-----------------------------+
        |
        | Recovery Card
        v
NEXY::PULSE / VIEW / FRONT / operator surface
```

The bridge is downstream from authority and upstream from presentation.

## 2. Authority invariant

`BridgeAuthority ⊂ UpstreamAuthority`

The bridge can only **remove** actions or redact information. It cannot add authority.

For each emitted action `a`:

`a ∈ UpstreamAuthorizedActions ∩ ReasonPolicyAllowedActions`

If either side excludes an action, the bridge excludes it.

## 3. Main modules

### model.py
Owns:
- enums;
- input normalization;
- validation bounds;
- immutable dataclasses;
- output serialization.

### policy.py
Owns:
- reason-to-message mapping;
- per-reason allowed action set;
- non-retryable overrides;
- evidence suppression flags;
- language text;
- canonical action ordering.

### compiler.py
Owns:
- action intersection;
- disclosure filtering;
- effective retryability;
- needed-input exposure;
- deterministic card assembly;
- fingerprint generation.

### cli.py
Owns:
- JSON input/output shell;
- error exit code;
- no business authority.

## 4. Data flow

```text
raw mapping
  ↓ strict normalization
FreezeEvent (immutable)
  ↓ reason policy lookup
  ↓ authorized-action intersection
  ↓ disclosure filter
  ↓ deterministic sort/order
RecoveryCard
  ↓ canonical fingerprint
JSON/user surface
```

## 5. Determinism strategy

Deterministic output depends on:
- fixed protocol version;
- fixed policy version;
- normalized enums;
- sorted missing-input IDs;
- sorted evidence references when visible;
- fixed action priority;
- canonical JSON encoding for fingerprint;
- no system clock;
- no RNG;
- no network;
- no model call.

The output fingerprint binds:
- normalized event fields;
- policy version;
- generated card fields.

## 6. State model

Freeze Bridge itself is deliberately stateless.

```text
RECEIVE → VALIDATE → NORMALIZE → FILTER → COMPILE → EMIT
              |                         |
              +-------- FAIL -----------+
```

No write-back or auto-retry exists inside the engine.

## 7. Recovery ownership

`recovery_owner` is informational routing, not permission:
- USER
- OPERATOR
- SYSTEM
- EXTERNAL_DEPENDENCY
- NONE

A surface can display the owner but must still use upstream authorization for actionable controls.

## 8. Disclosure boundary

Classes:
- PUBLIC
- INTERNAL
- RESTRICTED

Reference behavior:
- PUBLIC: sorted supplied evidence refs may be shown.
- INTERNAL: supplied refs may be shown to an internal surface.
- RESTRICTED: only `public:` refs survive by default.
- RESTRICTED + SECURITY_INTEGRITY: all evidence refs are suppressed.

This is only a conservative reference policy. Any future production integration must map to the actual NEXY security/disclosure model.

## 9. Failure semantics

Invalid contract:
- reject;
- CLI exit code 2;
- structured FAIL error on stderr;
- never emit a partially valid Recovery Card.

Unknown future reason:
- map to `UNKNOWN_REASON`;
- do not infer cause;
- force non-retryable;
- only emit pre-authorized actions allowed by unknown policy.

## 10. Performance shape

The engine is CPU-only, in-memory and O(n) in the number of supplied lists. Hard list bounds prevent unbounded per-event processing in the reference contract.

Current local benchmark is recorded separately and must not be interpreted as a production guarantee.

## 11. Non-authority of human language

Localized title/summary/action labels are presentation strings only.

They do not:
- decide status;
- change allowed action codes;
- alter retryability;
- mutate state;
- resolve conflicts;
- grant permission.

## 12. Evolution law

Protocol and policy are versioned separately:
- protocol `1.0`;
- policy `freeze-bridge-policy/1.0`.

Breaking contract changes require a new protocol version and explicit migration/adoption work. Wording-only changes may still require snapshot/UI review because language can affect user understanding even when machine behavior is unchanged.
