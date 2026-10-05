# TASK-DOC-C-REQUEST-OTAC-AUDIT-001

STATUS: IN_PROGRESS
OWNER_CHAT: C-SOL-20261006-0143-0700-DOC-C-OTAC-AUDIT
PRODUCT_REPO: goif74945-crypto/NEXY.AI-
BASE_BRANCH: NEXY.AI-Test-AI
BASE_SHA: 12eb5d2361c17bea901d735e8d1f8e2ee722f931
WORKER_BRANCH: NEXY.AI-Test-AI/work/C-SOL-20261006-0143-0700/otac-audit
AUTHORITATIVE_SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

## Requirement
Final DOC-C §4.2 for POST /api/auth/request-otac requires Audit: emit AUTH_OTAC_REQUESTED on success/failure.

## Proven gap
At base SHA, success writes AuditLog.action=AUTH_OTAC_REQUESTED, but validation/lock failures write action=REQUEST_OTAC and email-delivery failure writes action=OTAC_DELIVERY_FAILED.

## Mutation scope
- packages/api/auth.ts
- tests/integration/auth/request-otac.spec.ts

## Stop conditions
Implement canonical audit action for request-otac failure paths, preserve detailed EventLog failure telemetry, add regression assertions, run real CI/tests, inspect diff, and integrate only if safe.
