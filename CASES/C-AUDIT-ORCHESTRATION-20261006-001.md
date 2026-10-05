# CASE C-AUDIT-ORCHESTRATION-20261006-001
## Context
User requires separation of duties: this coordinator creates only the audit-chat instruction. The audit chat performs exhaustive spec-vs-code verification and then generates the downstream builder command from proven findings.
## Proven controls
- Product repository is read-only for the auditor.
- Audit authority is pinned to branch NEXY.ai.
- Full source must be read with streaming coverage.
- 837 normalized rows are source normalization; 773 are current implementation scope.
- Legacy 215 registry is prohibited as current denominator.
- Audit coverage, evidence coverage, and verified completion are separate metrics.
- The builder command is forbidden until the audit final gate.
## Reusable lesson
Do not pre-compose repair work before the audit establishes exact FINDING_ID/REQ_ID evidence, paths, dependencies, and acceptance tests.
## Status
VERIFIED_CASE
