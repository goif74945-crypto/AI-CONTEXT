# NCVG Integration Contract

> **AI proposal. Integration with NEXY.AI is NOT VERIFIED.**

## Recommended placement
`NEXY orchestration -> evidence bundle -> NCVG -> ALLOW/FREEZE -> higher-authority judge`

NCVG should remain outside the NEXY.AI repository boundary. It verifies bundle consistency while final authority remains with the higher-authority NEXY judge/law layer.

## Bundle v1.0
Required top-level fields:
- `bundle_version`
- `task_contract`
- `requirement_ledger`
- `evidence`
- `execution_record`
- `policy`

## Policy
- `acceptable_evidence_classes`: exact admitted classes per requirement
- `expected_commit`: exact commit binding or null
- `protected_target_patterns`: protected mutation patterns
- `forbidden_mutation_repository_name_fragments`: repository fragments forbidden for mutation
- `allow_warnings`: whether warning-only bundles can ALLOW

## Output
```json
{
  "decision": "ALLOW|FREEZE",
  "status": "PASS|FAIL",
  "bundle_sha256": "...",
  "verified_requirements": ["REQ-..."],
  "total_mandatory_requirements": 2,
  "findings": []
}
```

Exit codes: `0` ALLOW/success, `2` semantic FREEZE, `64` malformed/unreadable input.

## Integration acceptance criteria
Do not claim NEXY integration until exact adapter mapping, schema validation, negative FREEZE propagation, exact-commit binding, higher-authority judge behavior, User Law non-bypass, and target runtime/deployment evidence are all demonstrated.
