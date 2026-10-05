# RECERT Collision-Safe Path Integrity — Design

**Classification: AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION**

## Verified gap

The original experimental RECERT flattens nested mappings into dot-delimited
paths. A literal key such as `"a.b"` aliases the nested path represented by
`{"a": {"b": ...}}`. Fresh reproduction showed the original certifier returning
`CERTIFIED` when the nested value changed from `1` to `2` because the literal
key overwrote the same flattened path.

This continuation deepens RECERT; it does not add a sixth mission concept.

## Objective

Provide an independent, fail-closed recovery comparison using canonical JSON
Pointer paths:

- escape `~` as `~0` and `/` as `~1`;
- reject non-canonical or invalid pointer escapes;
- reject non-string mapping keys and cyclic state graphs;
- preserve type-sensitive equality (`true` is not integer `1`);
- restrict `NONDECREASING` to integers excluding booleans;
- apply ignored prefixes only at path-segment boundaries;
- forbid root-wide ignore and policy rules hidden by an ignore prefix;
- emit deterministic sorted mismatches and a SHA-256 result hash.

## Contracts

- `PointerRecoveryPolicy`: JSON Pointer modes and ignored subtrees.
- `PointerRecoveryCertifier`: collision-safe state flattening and comparison.
- `RecertPathIntegrityAssurance`: conservative integration adapter that requires
  both original RECERT and collision-safe RECERT to certify. Disagreement
  freezes and is surfaced explicitly.

Supported modes remain `EXACT`, `NONDECREASING`, `PRESENT`, `ABSENT`, and
`ANY`. Unspecified paths default to `EXACT`.

## Non-duplication boundary

Repository inspection found reusable JSON Pointer techniques in other isolated
labs and many recovery-proof proposals, but no prior artifact that detects the
confirmed dotted-path alias in this mission's RECERT and binds a collision-safe
replacement check to RECERT output. This artifact owns only that narrow
recovery-state identity gap.

## Failure semantics

Invalid policy/state input raises `FreezeError`. Semantic mismatch returns
`FREEZE`. The implementation never rewrites state, guesses a path, relaxes a
mode, or treats legacy certification as sufficient after a disagreement.

## Limits

- This compares bounded in-memory mapping snapshots, not live stores.
- Snapshot authenticity, capture atomicity, and authority provenance are not
  proven.
- Arrays remain leaf values, matching the original RECERT mapping-focused
  contract.
- No production, deployment, canonical-adoption, or NEXY.AI integration claim
  is made.
