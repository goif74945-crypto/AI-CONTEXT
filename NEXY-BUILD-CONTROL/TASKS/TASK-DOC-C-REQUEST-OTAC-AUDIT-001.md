# TASK-DOC-C-REQUEST-OTAC-AUDIT-001

STATUS: BLOCKED_TEST_INFRA
OWNER_CHAT: C-SOL-20261006-0143-0700-DOC-C-OTAC-AUDIT
PRODUCT_REPO: goif74945-crypto/NEXY.AI-
BASE_BRANCH: NEXY.AI-Test-AI
BASE_SHA: 999cf6b6a64e1cb36a295f80af5cbbc3a97d5742
WORKER_BRANCH: work/C-SOL-20261006-0143-0700-otac-audit-v2
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


## Current evidence
- Current narrowed gap: email-delivery failure AuditLog.action remains OTAC_DELIVERY_FAILED while FINAL DOC-C §4.2 requires AUTH_OTAC_REQUESTED on failure.
- Worker head after cleanup: 77b58216ad68e078a37eb7b7cd96a32084293f57
- Draft PR: #50
- Real test attempt: GitHub Actions run 37359775733 / job 111931162663.
- Result: workflow completed failure before any step executed; job step list was empty.
- Contemporaneous exact-head workflows on NEXY.AI-Test-AI also fail at runner/startup level.
- Integration is fail-closed until executable test evidence exists.
