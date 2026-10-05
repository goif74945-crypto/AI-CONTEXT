# T-8F2D6A15 — SystemEnvelope authority-safe repair design

STATUS: DESIGN_COMPLETE / SOURCE_MUTATION_BLOCKED
REQ_ID: REQ-DOC-C-3-2-SYSTEM-ENVELOPE
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
BASE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96

## FACT

Final DOC-C §3.2 is the active build authority and defines one canonical envelope shape. The current implementation both expands that shape with unsupported top-level members and narrows declared primitive domains without final-DOC-C evidence.

## Minimal repair plan once mutation is unblocked

1. packages/contracts/envelope.ts
   - Retain only canonical §3.2 envelope members.
   - Remove ActorTypeSchema/RoleSchema/BlockingLayerSchema/FreezeReasonSchema/EnvelopeWarningSchema/EnvelopeIntegritySchema from the canonical envelope module unless a separate active authoritative requirement proves they belong elsewhere.
   - Use z.string() for timestamp/request_id/trace_id/correlation_id/version.
   - Use z.number() for optional duration_ms.
   - Make the canonical object exact/strict so unsupported wire members are detected rather than silently promoted as canonical.
   - Keep buildEnvelope output limited to the authoritative keys.

2. packages/contracts/errors.ts
   - Keep ErrorCodeSchema unchanged.
   - For canonical envelope error payload, message and source must follow final DOC-C string domain unless another active DOC-C requirement proves narrower constraints.
   - Keep recoverable boolean unchanged.

3. tests/contract/envelope.test.ts
   - Add an exact-key oracle for canonical output.
   - Add negative tests rejecting unsupported actor/freeze_reason/warnings/integrity wire members.
   - Add positive counterexamples for values allowed by DOC-C but rejected by current narrowing: opaque timestamp/version strings, long IDs, fractional/negative duration numbers, empty error message/source if no separate authoritative constraint exists.
   - Preserve required fields and enumerated status/state/error-code tests.

## Collision/risk assessment

- Search found freezeReason, warnings, and envelope integrity options unused outside envelope.ts.
- ActorTypeSchema and FreezeReasonSchema are not consumed elsewhere. The search hit for RoleSchema in dialog-sandbox is a distinct DialogRoleSchema, not an envelope import.
- ErrorPayloadSchema is consumed by envelope.ts and historical evidence docs only.
- Therefore the expected runtime blast radius is low, but API contract tests must still run because buildEnvelope is widely used.

## Forbidden shortcuts

- Do not keep unsupported members merely because historical evidence docs describe them.
- Do not change DOC-C primitive types to match current implementation convenience.
- Do not weaken ErrorCode/SystemStatus/SystemState enumerations.
- Do not mutate NEXY.ai.
- Do not bypass the V7 worker-branch block by editing NEXY.AI-Test-AI directly.

## Verification commands after legal worker namespace exists

- npx vitest run tests/contract/envelope.test.ts --reporter=verbose
- npm run test:contract
- npm run check:doc-c
- affected API integration tests
- broader M01 contract-lock verification as required by integration wave risk

Every result must bind repository, branch, commit SHA, tree SHA, spec hash, command, runner, result, and exit code.
