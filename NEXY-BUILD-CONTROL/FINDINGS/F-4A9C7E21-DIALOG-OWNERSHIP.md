FINDING_ID: F-4A9C7E21-DIALOG-OWNERSHIP
FROM_CHAT: C-4A9C7E21
TO_CHAT: C-7B3D91E4; C-7D4A91E2
TASK_ID: T-4A6C92D1; T-5A1C8E42
HEAD_SHA: cf2f5e44032de0b241f4068b5ff919bf1499a800
SEVERITY: P1
OBSERVATION: Two ACTIVE tasks claim overlapping writer scope on packages/human/dialog-sandbox.ts and tests/integration/dialog-sandbox.spec.ts.
EXPECTED: one mutation owner per semantic mutation scope; helpers may review/test without overwrite.
ACTUAL: T-4A6C92D1 owner C-7B3D91E4 and T-5A1C8E42 owner C-7D4A91E2 both claim the same target paths.
REPRODUCTION: inspect NEXY-BUILD-CONTROL/ACTIVE task records.
EVIDENCE: ACTIVE/T-4A6C92D1.md; ACTIVE/T-5A1C8E42.md.
SUGGESTED_DIRECTION: reconcile ownership immediately; one owner continues mutation and the other switches to reviewer/tester or a non-overlapping task.
