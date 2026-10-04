# Verification Evidence

## Status boundary

This evidence proves the standalone lab source passed static TypeScript validation and executed unit/behavior tests in the local tool environment. It does not prove NEXY integration, deployment, distributed atomicity, external tool behavior, or physical safety.

## Environment

- Session date context: 2026-10-05 (+07:00)
- Node: `v22.16.0`
- TypeScript: `5.8.3`
- Package: `@nexy-labs/side-effect-transaction-planner@0.1.0-proposal`
- Runtime dependencies: none

## Final verification

Command:

```bash
npm run verify
```

Final result after the last source change:

- strict TypeScript typecheck: PASS
- TypeScript build: PASS
- executable tests: **47 passed / 0 failed / 0 skipped**
- evidence class: E1 + E2

## Restore verification

The exact two source archive parts stored under `source/` were concatenated, decoded, SHA-256 checked, extracted into a clean temporary directory, and verified again.

- decoded archive SHA-256: `24749323ac0e6518f00c6071ec1a93a9fd8ab5c4a07d0d365789e927b5fdddf9`
- restored `npm run verify`: **47 passed / 0 failed**
- result: archive fidelity and local reproducibility PASS

## Determinism / capacity observation

Command:

```bash
npm run benchmark
```

Latest local run:

- fixture: 256 independent filesystem mutation actions
- warmups: 5
- measured runs: 50
- stable plan hash across every measured run: yes
- mean: 44.623 ms
- median: 38.308 ms
- p95: 59.936 ms
- min: 27.085 ms
- max: 141.008 ms
- stable plan hash: `10ca7125c9d23e3fe568d4c4ab3cb3dd3ad51a0ba3e40e3de59f5854a9e4dedb`

This is a local microbenchmark only, not a production SLO.

## Failure/recovery history during construction

### F-01 GitHub write race
The first checkpoint write to AI-CONTEXT returned HTTP 409 because another concurrent writer advanced `main`. No force operation was used. Retrying against fresh state succeeded at commit `b6fac7f8bdd500aeea1465f8ba5cb5ecdc3c98e7`.

### F-02 Initial static environment/type issues
The initial strict pass exposed missing local Node type declarations plus strict typing issues in the tests. The local test environment and code were corrected before PASS was claimed.

### F-03 Invalid benchmark fixture
The first ad-hoc benchmark fixture omitted mandatory precondition identity and runtime validation failed. No performance number from that invalid run was retained.

### F-04 First self-review
After an earlier 35-test PASS, review found policy identity needed to bind policy material and later phases needed to recompute plan identity. Those gaps were fixed and tests expanded.

### F-05 Second self-review
After a 42-test PASS, review found five more semantic gaps: hidden resource mutation under `NONE`, non-`NONE` without side-effecting access, preconditions on undeclared resources, rollback effect outside policy, and duplicate set-like policy values. These were fixed and the suite expanded to 47 tests.

## Read-only NEXY evidence

Observed repository: `goif74945-crypto/NEXY.AI-`  
Observed branch: `NEXY.ai`  
Observed head during this task: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

Read-only files inspected included `AGENTS.md`, `package.json`, `packages/phase-f/l1o/l600-support.ts`, its integration test, `packages/queue/dispatch.ts`, and `prisma/schema.prisma`.

No mutation tool was called against the NEXY.AI repository in this task.

## Governing AI-CONTEXT read before mutation

Read included `AI-BOOTSTRAP.md`, `AI-EXECUTION-KERNEL.md`, `INDEX.md`, `WORK-ROUTER.md`, global/behavior/security/verification rules, project workflows, NEXY overview, current source-normalization build matrix, and existing supplemental index/state files.

## Raw evidence preservation

`evidence/EVIDENCE_ARCHIVE.b64` contains the raw verify log, benchmark log, environment record, static audit, source observations, test inventory, and file inventory captured during construction.

Decoded evidence archive SHA-256:

`a0374e2dee6063bfb19291bf9bc87bd3b688ac09ba04edbba8a82d2105faf52a`

## Known evidence gaps

- No E3 real-NEXY adapter/executor integration.
- No E4 end-to-end user/tool flow.
- No E5 durable journal/crash/distributed-lock test.
- No E6 deployment evidence.
- No E7 physical safety evidence.
- Duplicate searches are scoped evidence, not proof that no analogous idea exists anywhere in all history.
