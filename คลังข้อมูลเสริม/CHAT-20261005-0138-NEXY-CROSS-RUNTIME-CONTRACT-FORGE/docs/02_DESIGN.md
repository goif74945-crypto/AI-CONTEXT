# System Design

## 1. Problem statement

Cross-language systems can implement the same conceptual contract in multiple files and runtimes. Review discipline can reduce divergence, but it cannot make manual duplication deterministic. If a TypeScript transition table changes while a Rust mirror does not, both files can still compile and their local tests can still pass while the overall system contract has drifted.

This forge moves shared contract semantics into a small, strict, language-neutral intermediate representation and treats generated runtime views as derived artifacts.

## 2. Non-goals

- It does not infer truth from source code.
- It does not decide which NEXY document is authoritative.
- It does not rewrite NEXY source.
- It does not make deployment or runtime-correctness claims.
- It does not replace runtime-specific behavior that cannot be represented in the manifest.

## 3. Architecture

### 3.1 `src/canonicalize.mjs`

Responsibilities:

- reject non-JSON-safe values;
- reject dangerous prototype-related keys recursively;
- canonicalize arrays/objects that are already semantically ordered by upstream normalization;
- produce stable canonical JSON;
- produce SHA-256 digests.

Security boundary: arbitrary parsed JSON is treated as untrusted data.

### 3.2 `src/validate-manifest.mjs`

Responsibilities:

- strict allow-list of keys at every schema level;
- schema version and identifier validation;
- input resource limits;
- enum uniqueness and wire-value uniqueness;
- reference integrity between state machines and enum definitions;
- actor membership validation;
- terminal-state invariants;
- actor-aware transition determinism;
- canonical sort of semantically set-like collections;
- provenance normalization;
- semantic and full-manifest fingerprints.

Decision-key invariant:

```text
(from state, event, actor) -> exactly one (to state, sorted guards)
```

A duplicate decision key with different output/guards is `NON_DETERMINISTIC_TRANSITION`; an exact duplicate is `DUPLICATE_TRANSITION`. Both fail closed.

### 3.3 `src/compiler.mjs`

One validated normalized object drives every output:

- normalized manifest;
- TypeScript source;
- Rust source;
- runtime snapshot;
- conformance fixtures;
- compile evidence.

No generator independently reinterprets the raw input.

### 3.4 TypeScript target

Generated TypeScript provides:

- readonly enum-like constant objects;
- union types derived from those constants;
- immutable transition table;
- actor/guard-aware transition lookup;
- explicit denial result when transition, actor, or guard requirements fail.

A discovered generator defect initially widened frozen actor arrays to `readonly string[]`; the compiler was repaired to emit `as const`, and a strict `tsc` regression test was added.

### 3.5 Rust target

Generated Rust is intentionally conservative:

- `#![no_std]`;
- no `Vec`, `String`, heap allocation, or serde requirement;
- enums with stable wire-string conversion;
- static slices for authorized actors and guards;
- deterministic transition lookup;
- guard callback represented as a function pointer.

This maximizes portability to a constrained core, but it also means richer payload/schema contracts would require future IR extensions rather than silently inventing runtime semantics.

### 3.6 `src/audit.mjs`

The auditor builds the expected canonical runtime snapshot from the manifest and recursively compares it with an observed snapshot.

Diff classes:

- `TYPE_MISMATCH`
- `UNEXPECTED_VALUE`
- `MISSING_VALUE`
- `UNEXPECTED_KEY`
- `MISSING_KEY`
- `VALUE_MISMATCH`

Any diff yields `FAIL`.

### 3.7 `src/cli.mjs`

Commands:

- `validate`: validate and report fingerprints;
- `compile`: emit all deterministic artifacts;
- `snapshot`: print expected runtime snapshot;
- `audit`: compare observed runtime snapshot and return exit 2 on drift.

## 4. Data and provenance model

The manifest separates semantic contract data from provenance. The forge computes:

- `semanticFingerprint`: hash of normalized semantic identity/contract version/enums/state machines, excluding provenance;
- `manifestFingerprint`: hash of the full normalized manifest including provenance.

This distinction permits source-observation metadata to change without falsely claiming a semantic contract change, while still allowing the complete artifact to be sealed separately.

## 5. Determinism model

Determinism is enforced by:

1. schema validation before generation;
2. canonical ordering for enum definitions, members, machines, terminal states, transitions, actors, guards, and provenance paths where ordering carries no semantics;
3. canonical JSON serialization;
4. one normalized object shared by all generators;
5. byte-for-byte repeated-build regression tests;
6. semantic fingerprints included in generated outputs.

## 6. Threat model

### Inputs considered hostile

- arbitrary JSON;
- malformed nested values;
- prototype-pollution keys;
- code-injection-shaped identifiers/wire values;
- huge input intended to exhaust resources;
- duplicate/ambiguous transition definitions;
- unexpected schema fields.

### Controls

- recursive JSON safety check;
- plain-object checks;
- dangerous-key rejection;
- regex-restricted identifiers/wire strings;
- explicit key allow-lists;
- bounded manifest bytes/counts;
- no `eval`, dynamic import, shell generation, or template execution from user values;
- JSON escaping and controlled language emitters.

## 7. Failure model

Validation errors are explicit structured failures and stop compilation. The compiler never drops invalid entries to “make progress.” The auditor treats extra as well as missing values as drift. CLI error codes distinguish ordinary validation/operation errors from detected drift and usage errors.

## 8. Evolution law

`schemaVersion` owns the forge IR syntax. A future incompatible manifest-format change must increment it. `contractVersion` belongs to each contract. Existing schema version 1 validators must reject unknown fields rather than guessing their meaning.

Proposed future extensions must be additive only when old readers can reject them safely or when a new schema version is introduced.

## 9. Trade-offs

### Benefits

- one semantic source for multiple runtime views;
- stable fingerprints and machine-comparable snapshots;
- explicit drift evidence;
- deterministic generation;
- better review surface than manually comparing parallel implementations.

### Costs

- introduces a compiler/IR that itself must be trusted and tested;
- cannot represent arbitrary runtime-specific behavior without expanding the IR;
- generated source can be less idiomatic than hand-written code;
- adoption requires an explicit authority decision about which contracts are safe to generate;
- Rust compilation still needs the Rust toolchain in the target verification environment.

## 10. Integration boundary

The forge is deliberately standalone. Future NEXY integration, if authorized, should begin with a read-only comparison mode. Only after the current DOC-C authority and exact NEXY HEAD are reconciled should any contract be nominated for generation. See `05_INTEGRATION_PROPOSAL_ONLY.md`.
