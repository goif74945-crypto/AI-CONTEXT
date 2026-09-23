# Evidence Registry Validation

## Target
- repo: `goif74945-crypto/NEXY.AI-`
- branch: `codex/spec-audit-20260919-78df350`
- current HEAD: `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`

## DOC-E source pack
- declared source revision: `9eaeec9b830471907f2f1f19ca5d76371caf22cb`
- relation to current HEAD: **STALE_FOR_CURRENT_HEAD**

## Current E1–E12 status
- PASS: **0**
- BLOCKED: **12**
- exact-current-HEAD proofs: **0**

This is deliberate. The current evidence pack itself states that hosted Actions jobs terminated before executable steps were exposed and E11 lacks authorized external signoff.

### Namespace inconsistency observed
`docs/evidence/current/README.md` names campaign revision `db52f9f...`, while the aggregated DOC-E pack names `9eaeec9b830471907f2f1f19ca5d76371caf22cb`. Neither equals current HEAD `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`.

This is recorded as evidence freshness/namespace drift, not silently reconciled.

## Verdict
**Current HEAD remains NOT VERIFIED / NON-DEPLOYABLE from DOC-E evidence.**
