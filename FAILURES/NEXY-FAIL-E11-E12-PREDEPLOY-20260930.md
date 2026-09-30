# FAILURE — E11/E12 release gate and post-build validation blocker

FAILURE_ID: NEXY-FAIL-E11-E12-PREDEPLOY-20260930
related_task: NEXY-E11-HUMAN-APPROVAL-VALIDATION-20260930
head: d7f824ed7f4b70e5308f3b8bb6a31fbf1ad0a61e
tree: 4cf698ed37f87d68df1c30a3e55bd4bd80a36c5e
severity: S4
version: 1.0.0

## Context
User requested complete Human E11 approval with passing tests according to specification.

## Failed approach
A truthful E11 PASS cannot be minted from the current evidence because E12 exact-head application rollback proof is absent. Two canonical Railway validation deployments also ended FAILED after successful image build.

## Root causes / boundaries
1. E11 is intentionally an external human authorization gate; AI self-approval is forbidden by code/tests.
2. E11 requires rollback_verified=true and monitoring_verified=true.
3. Current exact-head E12 application rollback receipt is not proven.
4. Latest successful exact-head runtime campaign also has E10 externally blocked.
5. Railway deployments ce1bf3c1-f3d3-4170-9a7c-46c3aaa929a2 and 69b0c677-2321-4fa0-9b51-22d9ae6a5cbb failed after image build; available deploy log showed no attributable pre-deploy error detail.
6. Railway diagnostic-agent path was unavailable due provider usage limit.

## Recovery
- Use an explicitly authorized rollback-capable isolated environment to execute and verify application rollback for d7f824ed7f4b70e5308f3b8bb6a31fbf1ad0a61e/4cf698ed37f87d68df1c30a3e55bd4bd80a36c5e.
- Produce provider-backed E12 receipt including rollback execution, health checks, smoke checks, monitoring verification and log link.
- Resolve E10 provider-command evidence.
- Human reviewer(s) then produce evidence-backed engineering/security/migration approval.
- Rerun exact-head DOC-E and require all E1-E12 PASS.

## Prevention
Never mark E11 PASS from user identity alone; approvals are assertions about completed reviews/evidence, not merely actor existence.

status: UNRESOLVED_EXTERNAL
