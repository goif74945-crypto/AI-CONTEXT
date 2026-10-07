# Ledger — NEXY VS Code and Railway Diagnostic

LEDGER_ID: LEDGER-20261007-NEXY-RAILWAY-DIAGNOSTIC-005
TASK_ID: 20261007-NEXY-RAILWAY-DIAGNOSTIC-005
TIMESTAMP_UTC: 2026-10-07T16:19:21Z
PARENT_AI_CONTEXT_HEAD: 8b9e258b2356ed7d07ecea66cc48a5e2bf4d1c40
CHECKPOINT_COMMIT: 81198f65ea58d62899087abf74912e582f49b235

| Seq | Action | Evidence | Result |
|---:|---|---|---|
| 1 | Read locked command and current capability evidence | AI-CONTEXT/8b9e258b2356ed7d07ecea66cc48a5e2bf4d1c40 | Read; exact-head fail-closed rules apply |
| 2 | Open GitHub VS Code target | Repo Code Bridge open_vscode | URL returned for NEXY.ai at 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43; no desktop process |
| 3 | Initialize Wix context | WixREADME | Plugin context read; no Wix mutation |
| 4 | Inventory Railway | Railway NEXY Validation R2 | Existing services found; no staged changes |
| 5 | Read Railway failed deployments/logs | deployments a4e4f0a2 and e06fbfc7 | Historical failures found; neither exact-head |
| 6 | Decide whether to redeploy | Locked gateway rule | Do not use Railway as CI bypass while dispatch is denied |
| 7 | Persist diagnostic records | AI-CONTEXT/main | Committed without force at 81198f65ea58d62899087abf74912e582f49b235; read-back completed at that revision |

## Ruling

Ruling: retain Railway findings as stale root-cause leads, not current proof — the cost if wrong is delayed diagnosis; promoting stale failures could patch the wrong source and violate exact-head evidence.

## Gate

- Product HEAD exact: YES
- Railway exact-head proof: NO
- Product source changed: NO
- New Railway deployment: NO
- CI dispatch capability: NO
- PASS_100: NO
- Status: BLOCKED_WITH_RESUME
