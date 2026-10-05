# TASK-DOC-C-FREEZE-RECOVER-423-CODE-001

STATUS: IN_PROGRESS
OWNER_CHAT: C-SOL-20261006-0208-0700-FREEZE-423
PRODUCT_REPO: goif74945-crypto/NEXY.AI-
BASE_BRANCH: NEXY.AI-Test-AI
BASE_SHA: 235de26be580929855044a0f3c0d92cc131a527d
WORKER_BRANCH: work/C-SOL-20261006-0208-0700-freeze-423-code
AUTHORITATIVE_SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

## Requirement
FINAL DOC-C §4.2 POST /api/freeze/recover errors:
- 403 FORBIDDEN
- 409 FREEZE_RECOVERY_DENIED
- 423 SYSTEM_IN_FREEZE

## Proven gap
Current handler returns HTTP 423 with error.code=FREEZE_RECOVERY_DENIED in two state-inconsistency paths:
1. new recovery requested while current runtime state is not FREEZE
2. durable system state changes before recovery transaction commits

These are contractually 423 SYSTEM_IN_FREEZE paths, while 409 remains FREEZE_RECOVERY_DENIED.

## Mutation scope
- packages/api/directives.ts
- tests/integration/freeze/recover.spec.ts

## Stop conditions
Canonicalize only the two 423 codes, preserve denial audit events and 409 behavior, add regression assertions, attempt real validation, and integrate only with executable test evidence.
