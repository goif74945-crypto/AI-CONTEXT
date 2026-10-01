FAILURE_ID: FAIL-NEXY-SANDBOX-TEST-IMPORT-80FB8FB0
TASK_ID: NEXY-FULL-AUDIT-80fb8fb0-20261002
context: current canonical HEAD test source
failed_approach: current commit contains corrupted dependency token
cause: import specifier is "viteหำดำst" instead of "vitest"
recovery: exact one-line repair then exact-head rerun on the repaired SHA
boundary: defect is in test source; no production runtime source change is proven by this commit
prevention: dependency/import resolution check before accepting HEAD
status: ACTIVE_BLOCKER
