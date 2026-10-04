# Architecture — NEXY Shadow Execution Guard

Status: AI-PROPOSED / EXPERIMENTAL / ADVISORY ONLY
Reference engine version target: 0.1.0

## 1. Boundary

The engine consumes only declared data and produces only a preview artifact.

It does not:
- open repositories;
- call network services;
- execute shell commands;
- call external tools;
- mutate databases;
- mutate files outside its own optional output file.

The engine trusts neither the truthfulness nor completeness of the upstream snapshot. It validates structure and applies deterministic rules to what it was given.

## 2. Canonical resource identity

A resource is:

```json
{"namespace":"repo:owner/name","key":"relative/path.txt"}
```

Rules:
- `namespace` is a non-empty logical domain identifier.
- `key` is a normalized POSIX-style relative key.
- absolute keys, empty keys, `.`, `..`, backslashes, NUL/control characters and repeated slash ambiguity are rejected.
- resource identity is the tuple `(namespace, key)`.

No symlink resolution is claimed. A real adapter must canonicalize physical targets before mapping them into this model.

## 3. Scope selectors

Selectors have exact namespace matching and either:
- `exact` key match; or
- `prefix` match on path-segment boundaries.

Protected selectors override authorized selectors.

A touched resource is legal only when:
1. it matches at least one authorized selector; and
2. it matches no protected selector.

For move, both source and destination must be legal.

## 4. Supported modeled operations

v0.1:
- `create`
- `update`
- `delete`
- `move`
- `opaque`

`opaque` always freezes with `UNMODELED_EFFECT`.

Every operation has a stable unique ID. Write operations carry inline UTF-8 content. Update/delete/move may declare `expect.exists` and/or `expect.sha256`.

## 5. Two-phase evaluation

### Phase A — static plan audit

Inspect every declared operation without changing simulated state:
- schema/semantic validity;
- operation ID uniqueness;
- resource normalization;
- scope authorization/protection;
- operation count and payload budget;
- opaque effects.

Any static violation yields `FREEZE` before modeled mutation begins.

### Phase B — sequential shadow simulation

If Phase A is clean:
- copy the supplied snapshot into an in-memory state map;
- process operations in declared order;
- verify each precondition against current simulated state;
- apply the modeled effect;
- stop on the first dynamic violation.

This preserves ordered semantics and avoids pretending later operations are meaningful after an earlier step became illegal.

## 6. Snapshot semantics

Snapshot entries may include:
- `sha256`
- optional inline `content`

If content is present, its hash must match the declared SHA-256.

If content is absent, the engine may still verify a hash precondition, but cannot manufacture restore bytes.

Duplicate resource identities are invalid.

## 7. Reversibility policy

Default: `require_reversible = true`.

After successful simulation, compare initial and final state. For every resource that would need restoration:
- if initial content is available, emit a concrete restore action;
- if initial content is unavailable, rollback is incomplete.

When `require_reversible=true`, incomplete rollback converts the preview to `FREEZE` with `ROLLBACK_INCOMPLETE`.

This is stronger than claiming “we can probably recover.” Civilization has tried that strategy often enough.

## 8. Predicted diff and blast radius

Successful simulation emits:
- created resources;
- updated resources;
- deleted resources;
- moved resources as operation history plus state diff;
- namespaces touched;
- total operations;
- write bytes;
- destructive operation count;
- rollback completeness.

## 9. Deterministic certificate

The result body is serialized as canonical JSON:
- UTF-8;
- sorted object keys;
- compact separators;
- deterministic list ordering where input order is not semantically meaningful.

Operation order is semantically meaningful and preserved.

`certificate_sha256` is SHA-256 over the canonical result body excluding that field.

No wall-clock timestamp is injected into the certificate body.

## 10. Decisions and errors

Valid result decisions:
- `PREVIEW_PASS`
- `FREEZE`

Malformed/unsupported input is an input error, not a FREEZE result.

CLI exit contract:
- 0 = PREVIEW_PASS
- 2 = valid FREEZE
- 64 = invalid input / I/O

## 11. Security properties

- standard library only;
- no input execution;
- no shell/network behavior;
- strict resource normalization;
- bounded operations and payload bytes;
- protected scope wins;
- opaque side effects fail closed;
- no secret requirement.

## 12. Integration shape if promoted later

Potential adapter chain:

`NEXY candidate action → provider/tool adapter → canonical effect plan → Shadow Execution Guard → preview certificate → JUDGE/human policy gate → real executor`

Promotion would require exact-head integration tests, real adapter conformance tests, abuse tests, concurrency semantics, symlink/physical-path hardening for filesystem adapters, and operational evidence.

Current integration status: NOT_VERIFIED / NOT_IMPLEMENTED BY THIS LAB.
