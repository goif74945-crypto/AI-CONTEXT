# CASE 20261009-NEXY-GPT6-SOL-RAILWAY-LOOP-V1
TITLE: Existing Railway test assets versus current-head isolation
CLASS: ENGINEERING_RUNNER_DISCOVERY / PROVENANCE / RELEASE_SECURITY
STATUS: OPEN_FOR_BUILDER
FACT: Railway project NEXY Validation R2 and successful PostgreSQL/Redis service deployments exist, but environment is named production and not ephemeral; current validation source pin is old, two validation services last build FAILED, current Product HEAD differs.
ROOT RISK: Confusing availability of tools/services with authorization to mutate shared data, or with current-head test PASS. Project creation attempt hit free plan provision limit, not a universal absence of all testing routes.
FIX: Builder command must search for existing grants and safe nonproduction isolated resource use, read historical logs as diagnostic, prefer actual current-head test on isolated authorized runner, never replay old results. If one provisioning path blocked, execute other READY source/tests.
VALIDATION: Command review 26/26 structural checks, GitHub readback; no current-head runtime tests in this task.
PREVENTION: source blob+head to exact test receipt, explicit Railway service isolation, separate status for source-only, runtime E2E and release gates.
NEXT: same GPT-6 Sol builder executes COMMANDS/20261009-NEXY-GPT6-SOL-RAILWAY-LOOP-V1.md in active normal chat and submits evidence to independent auditor.
