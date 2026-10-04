# ECPC-20 Verification and Failure Audit

## Final isolated verification
- TypeScript E1 typecheck: PASS.
- Strict hardening: PASS with noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch, noImplicitOverride, noPropertyAccessFromIndexSignature.
- Build: PASS.
- Source scan: PASS; exactly 20 concept modules.
- Final E2 node:test suite: **62/62 PASS**.
- Fresh sealed-archive extraction: typecheck PASS, strict hardening PASS, build PASS, **62/62 PASS**, source scan PASS.
- Transport reconstruction: PASS.
- NEXY repository mutations: **0**.
- Canon promotion: NOT_PERFORMED.
- NEXY runtime integration: NOT_VERIFIED.
- Deployment: NOT_VERIFIED.

## Stress / property checks included
- Q64 add/sub inversion: 20,000.
- Q64 multiply identity: 20,000.
- Q64 monotonic ratio: 5,000.
- canonical insertion variants: 5,000.
- multilingual schema rotations: 5,000.
- schema permutation determinism: 1,000.
- integrated compiler replay: 1,000.
- Merkle repeat: 1,000.
- EPC ledger deterministic rebuild: 2,000.
- upgrade-planner repeat: 1,000.

## Evidence identities
- E2 TAP SHA-256: `9c3f41739ea3ae263cb8d9f15fe72c0b64f10cbd7ea4dd079819a2c985f1c99e`
- Integrated proof report SHA-256: `624c6a743c424f19f77f708109f6e55e6906b58f9a47b037fd040f7182d83501`
- Tested-source manifest SHA-256: `1e615976b8ec5a9d4cdd9d089d9dbba1fd697ed05d35d72dd45f20b2b70ae826`
- Sealed archive SHA-256: `ef83a3ca988a4177b15f8a61910305bef7a5465a31d04f64aa5245ab1e9905be`

## Preserved RED / audit failures

### RED-001 — missing Node ambient type definitions
Initial `tsc --noEmit` failed with TS2688 because the execution environment lacked project-local `@types/node`.
Repair: remove ambient package dependency and add narrow declarations for exactly `node:crypto`, `node:test`, `node:assert/strict`.
Reverification: PASS.

### RED-002 — canonical encoder non-terminal path
Compiler found a function that lacked a terminal return/throw.
Repair: explicit fail-closed `NON_CANONICAL_UNREACHABLE` throw.
Reverification: PASS.

### AUDIT-003 — locale-dependent comparator after initial green suite
Static audit found `localeCompare()` in canonical ordering paths, an environment-sensitive input.
Repair: replace with explicit code-unit relational comparator and add Thai + composed/decomposed Unicode tests.
Reverification: no `localeCompare` in source; full suite PASS.

### RED-004 — evidence harness exited after E1
First seal command accidentally exited the parent shell from a brace group, so only the first evidence file existed.
Repair: fail-fast harness rewritten without parent-shell exit; evidence directory recreated; entire capture rerun.
Reverification: complete E1/E2 evidence set exists.

## Source-scan assertions
- concept-module-count=20
- no locale/time/random/Math/Number-constructor authoritative decision source
- no decimal/exponent numeric literal in `src`
- no TypeScript suppression or TODO/FIXME/HACK in `src`
- canonical ordering locale-independent

## Boundary
This evidence proves the isolated tested package bytes only. It is not evidence of NEXY runtime/deployment/Canon acceptance.
