# TASK-DOC-C-DIRECTIVE-CONTENT-TYPE-422-001

STATUS: BLOCKED_TEST_INFRA
OWNER_CHAT: C-SOL-20261006-0215-0700-DIRECTIVE-422
PRODUCT_REPO: goif74945-crypto/NEXY.AI-
BASE_BRANCH: NEXY.AI-Test-AI
BASE_SHA: aec9afaa77213c37b223b7594b92eb81c7862f9a
WORKER_BRANCH: work/C-SOL-20261006-0215-0700-directive-422
AUTHORITATIVE_SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

## Requirement
FINAL DOC-C §4.2 POST /api/directives error matrix binds SCHEMA_VIOLATION to HTTP 422.

## Proven gap
The non-JSON Content-Type validation path emits canonical error.code=SCHEMA_VIOLATION but uses HTTP 415 instead of the route-contract HTTP 422.

## Mutation scope
- packages/api/directives.ts
- tests/integration/directives/create.spec.ts

## Stop conditions
Change only the Content-Type schema-failure status to 422, add a regression test, attempt executable validation, and integrate only with valid test evidence.


## Current evidence
- Worker head after temporary validation-workflow cleanup: 1fca8d92a0f8b9d746a345b885ef688a7bdf103c
- Draft PR: #85
- Net product diff: directives.ts 1 status-line change; create.spec.ts adds one regression test.
- Real validation attempt: workflow run 37362378212 / job 111939815849.
- Result: GitHub Actions completed failure before any workflow step executed; job steps were null.
- Target still returned HTTP 415 + SCHEMA_VIOLATION immediately before PR creation.
- Integration remains fail-closed pending executable test evidence.
