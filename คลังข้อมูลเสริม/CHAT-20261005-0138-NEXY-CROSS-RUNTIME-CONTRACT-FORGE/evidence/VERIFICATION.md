# Verification Record

## Target

Standalone local project:

`CHAT-20261005-0138-NEXY-CROSS-RUNTIME-CONTRACT-FORGE`

NEXY compatibility fixture source commit:

`goif74945-crypto/NEXY.AI-@9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43` (read-only observation only).

## Environment

See `environment.txt`.

Observed:

- Node `v22.16.0`
- npm `10.9.2`
- TypeScript compiler `5.8.3`
- `rustc`: NOT_INSTALLED
- `cargo`: NOT_INSTALLED

## Gate V1: Node syntax/static parse

Evidence class: E1.

Command pattern:

```bash
for f in src/*.mjs tests/*.mjs; do node --check "$f"; done
```

Observed: `NODE_CHECK=PASS`.

Artifact: `node-check-output.txt`.

## Gate V2: automated behavior tests

Evidence class: E2, with CLI-oriented integration coverage inside the suite.

Command:

```bash
npm test
```

Observed:

- tests: 22
- pass: 22
- fail: 0
- cancelled: 0
- skipped: 0
- todo: 0

Artifact: `test-output.txt`.

Negative paths include:

- duplicate enum/member semantics;
- unknown referenced states/events/actors;
- actor-aware nondeterminism;
- exact duplicate transitions;
- terminal outbound transitions;
- prototype-pollution keys;
- injection-shaped wire values;
- runtime snapshot missing/unexpected data;
- invalid CLI manifest behavior.

## Gate V3: real generated TypeScript strict compilation

Evidence class: E1.

Command:

```bash
tsc --noEmit --target ES2022 --module Node16 --moduleResolution Node16 \
  --strict --exactOptionalPropertyTypes --noUncheckedIndexedAccess \
  generated/contract.generated.ts
```

Observed: PASS.

Artifact: `tsc-output.txt`.

### Failure-repair evidence

An earlier run failed with TS2322 because generated frozen actor arrays widened to `readonly string[]`. The generator was corrected to retain literal tuple types with `as const`. A regression test invoking `tsc` was added. The subsequent command passed and the full test suite passed 22/22.

## Gate V4: deterministic independent compilation

Evidence class: E3 for the compiler pipeline.

Procedure:

1. compile the same manifest into `/tmp/nexy-forge-a`;
2. independently compile it into `/tmp/nexy-forge-b`;
3. recursively diff both output directories.

Observed: no differences, `DETERMINISM_DIFF=PASS`.

Artifacts:

- `determinism-compile-a.json`
- `determinism-compile-b.json`
- `determinism-diff.txt`

## Gate V5: snapshot self-audit

Evidence class: E3.

Input: emitted `generated/contract.snapshot.json`.

Observed: `AUDIT_SELF=PASS`.

Artifacts:

- `audit-pass-summary.json`
- `audit-pass-output.txt`

## Gate V6: injected semantic drift must fail closed

Evidence class: E3 negative-path proof.

Procedure:

- copy emitted snapshot;
- remove the `OWNER` actor from `$.enums.vnext_actor`;
- run CLI `audit` against the modified snapshot.

Expected: audit FAIL and process exit code 2.

Observed:

- report status: `FAIL`;
- process exit: `2`;
- path-level diffs include the shifted/missing actor entries under `$.enums.vnext_actor`.

This is a PASS for the **negative-path requirement** that real drift must be rejected.

Artifacts:

- `audit-drift-summary.json`
- `audit-drift-exit-code.txt`
- `audit-drift-stderr.txt`

## Gate V7: coverage observation

Command:

```bash
node --test --experimental-test-coverage tests/*.test.mjs
```

Observed aggregate:

- line: 96.29%
- branch: 81.05%
- functions: 97.96%

Artifact: `coverage-output.txt`.

No minimum coverage threshold was defined by the task, so these percentages are observation evidence, not a standalone release claim.

## Gate V8: generated Rust compile

Required evidence for claim “generated Rust compiles”: E1 Rust compiler evidence.

Observed environment: no `rustc`, no `cargo`.

Status: **NOT_VERIFIED**.

What is proven instead:

- source generation completes;
- unit tests assert `#![no_std]` and absence of allocation-oriented `Vec`/`String`/`std` patterns intended to be excluded;
- deterministic generation produces the same Rust bytes across repeated builds.

These facts do not substitute for a real Rust compiler result.

## Final local verdict

Standalone implementation: **PASS** for all locally executable acceptance gates.  
Generated Rust compilation claim: **NOT_VERIFIED**.  
NEXY.AI production integration: **NOT PERFORMED / OUT OF SCOPE**.
