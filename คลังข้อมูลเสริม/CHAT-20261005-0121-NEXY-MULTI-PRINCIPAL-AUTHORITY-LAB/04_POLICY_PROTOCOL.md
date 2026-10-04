# MPAL Policy / Request / Approval Protocol v0.1

Status: `EXPERIMENTAL_REFERENCE_PROTOCOL`

## Policy
Top-level:
- `policy_id`: stable identifier.
- `version`: positive integer.
- `principals`: known principals with roles/domains/active state.
- `rules`: exact `(domain, action)` authorization rules.

Principal:
- `principal_id`
- `roles[]`
- `domains[]`
- `active: bool`

Rule:
- `rule_id`
- `domain`
- `action`
- `requester_roles[]`
- `approval_groups[]`
- `veto_roles[]`
- `deny_mode`
- `requester_may_approve`
- `min_distinct_approvers`

Approval group:
- `group_id`
- `eligible_roles[]`
- `threshold >= 1`

Supported denial modes:
- `ANY_ELIGIBLE_DENY`
- `VETO_ROLES_ONLY`

## Request
- `request_id`
- `requester_id`
- `domain`
- `action`
- `target_id`
- `payload_sha256`
- `policy_version`

The payload hash binds authority to an exact action payload without requiring MPAL to interpret payload contents.

## Approval receipt
- `principal_id`
- `decision: APPROVE | DENY`
- `group_id`
- `request_sha256`
- `policy_version`
- `valid_from_tick`
- `valid_until_tick`

## Evaluation order
1. Validate policy.
2. Validate request.
3. Require request policy version == policy version.
4. Resolve requester identity.
5. Enforce requester active/domain/rule/role permissions.
6. Check requester-specific quorum satisfiability.
7. Validate approval receipts.
8. Enforce request-hash and policy-version binding.
9. Reject contradictory receipts.
10. Ignore inactive/not-yet-valid/expired/self-forbidden receipts.
11. Apply deny/veto semantics.
12. Count distinct group approvals.
13. Enforce overall distinct-principal minimum.
14. Return deterministic decision.

## Duplicate law
Identical duplicate receipts from one principal are ignored after the first. Different receipts from one principal in the same evaluation set produce `FREEZE`.

## No fallback law
- No matching action rule => `DENY`.
- No hidden default approver group.
- No role hierarchy inferred from role names.
- No model may synthesize an approval.
- No stale policy approval is silently migrated.

## Example deployment rule
The fixture requires 1 Security approval + 2 Owner/Operator approvals + 3 distinct approvers, forbids requester self-approval, and permits Owner/Security veto.

The fixture is an engineering example, not an organizational recommendation.
