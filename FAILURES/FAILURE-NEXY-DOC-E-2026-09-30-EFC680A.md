# FAILURE-NEXY-DOC-E-2026-09-30-EFC680A

FAILURE_ID: FAILURE-NEXY-DOC-E-2026-09-30-EFC680A
status: RESOLVED_EXECUTION_PATH / E11_EXTERNAL_BLOCK_ACTIVE
version: 2

## Historical failed approaches
- GitHub Actions hosted runner: jobs instantiated but executable steps/logs unavailable
- Opera Browser Connector: disconnected during this task
- Remote Desktop Commander: device offline
- Termalin: no enrolled host
- Railway new validation service: Free plan resource limit
- Railway custom Dockerfile snapshot initially searched root Dockerfile
- validation image initially lacked Prisma generation
- validation image initially lacked Rust toolchain
- runtime build:web was SIGKILLed; no unsupported OOM conclusion
- prebuilt BUILD_ID guard initially used wrong path
- E7 campaign initially omitted existsSync import
- E7 fixture initially used non-canonical IDs and failed API schema validation
- stale E10/E12 receipts were rejected by exact-head identity checks

## Successful recovery path
- reused isolated Railway nexy-validation-branch
- validation alias only as provider source pointer
- kept implementation on work/doc-e-exact-head-20260930
- exact-head validation image + real PostgreSQL/Redis/worker/API drills
- E7 production-boundary fixture repaired without weakening schema/auth
- real rollback current -> prior release and restore current
- fresh E10/E12 receipts bound to real deployment IDs
- final exact-head campaign generated one E1-E12 attestation

## Latest exact-head result
- SHA: e82edcd9e6ab1322526499a45ecb72ff9a487e4a
- tree: 5cc36e3b85e775c462c4a2baf6a05abe7150f049
- final campaign deployment: 8d6180ec-1a6e-4fab-9c3d-19da8daf1ba6
- E1-E10 PASS
- E11 BLOCKED_EXTERNAL
- E12 PASS
- evidence_root_sha256: 9fb0c7cf13d920a2dededd4ac90e39d66b7f6716d4c7cb733d700502d3a02465
- attestation_sha256: a8082bc1386cd5cb8f8c62fcf10fdd8a2082b02d13b05578d42f97e6437e5d8a
- release_authorized=false
- deploy_authorized=false

## Unresolved
Only E11 remains unresolved. Missing authorized engineering/security/migration signoff is not a source defect. It must not be bypassed, fabricated, self-signed by AI, or inferred from general user approval.

## Prevention
- always bind receipts to exact tested SHA/tree
- blank/reject stale receipts instead of adapting them
- keep validation diagnostics secret-redacted
- keep application rollback evidence separate from migration rollback evidence
