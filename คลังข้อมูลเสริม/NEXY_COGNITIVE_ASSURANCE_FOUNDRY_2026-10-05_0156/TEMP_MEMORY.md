# Temporary Execution Memory / Resumption Point

Session identifier: `PROJECT-CONVERSATION-2026-10-05T01:56+07:00`
Internal ChatGPT chat ID: `UNKNOWN_NOT_EXPOSED_BY_AVAILABLE_TOOLS`

## Scope lock
- WRITE: only `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/<this-work-folder>/`
- READ: AI-CONTEXT context as required
- FORBIDDEN WRITE: any repository whose name contains `NEXY.AI`

## Current design
Five engines: ILC, CAG, CDL, PHS, HTBG. Shared deterministic Decision/Finding contract. Suite combines decisions with FREEZE dominance.

## Verification required before completion
1. Python compileall.
2. Unit/negative-path tests.
3. Determinism checks included in unit tests.
4. Re-read committed files from AI-CONTEXT.
5. Record commit SHA and executed output in EVIDENCE.md.

## Known non-goals
- No production deployment.
- No NEXY.AI source integration.
- No claim these proposals are canonical requirements.
- No use of hidden/private NEXY internals beyond AI-CONTEXT project context.
