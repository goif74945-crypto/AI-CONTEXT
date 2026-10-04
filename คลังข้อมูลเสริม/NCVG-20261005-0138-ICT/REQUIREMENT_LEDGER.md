# NCVG v0.1 Requirement Ledger

| ID | Requirement | Evidence target | Status |
|---|---|---|---|
| R-001 | Valid complete bundle returns ALLOW | test_valid_bundle_allows | PASS |
| R-002 | Missing evidence returns FREEZE | test_missing_evidence_freezes | PASS |
| R-003 | Wrong evidence class returns FREEZE | test_wrong_evidence_class_freezes | PASS |
| R-004 | Duplicate evidence IDs return FREEZE | test_duplicate_evidence_id_freezes | PASS |
| R-005 | Non-PASS mandatory requirement returns FREEZE | test_mandatory_requirement_non_pass_freezes | PASS |
| R-006 | Non-PASS execution record returns FREEZE | test_execution_non_pass_freezes | PASS |
| R-007 | Forbidden repository mutation returns FREEZE | test_forbidden_repository_mutation_freezes | PASS |
| R-008 | Protected target mutation returns FREEZE | test_protected_target_pattern_freezes | PASS |
| R-009 | Stale/wrong commit evidence returns FREEZE | test_expected_commit_rejects_stale_evidence | PASS |
| R-010 | Matching expected commit can be admitted | test_expected_commit_accepts_matching_evidence | PASS |
| R-011 | Canonical hash stable across mapping order | test_hash_is_stable_across_mapping_order | PASS |
| R-012 | Evidence content change changes hash | test_hash_changes_when_evidence_changes | PASS |
| R-013 | Duplicate requirement IDs return FREEZE | test_duplicate_requirement_id_freezes | PASS |
| R-014 | Empty requirement set returns FREEZE | test_no_requirements_freezes | PASS |
| R-015 | Optional gaps warn but may ALLOW | test_optional_failure_warns_but_allows | PASS |
| R-016 | Policy can reject warnings | test_policy_can_disallow_warnings | PASS |
| R-017 | Non-JSON API input freezes without raising | test_non_json_api_input_freezes_instead_of_raising | PASS |
| R-018 | CLI exit codes stable | test_cli_validate_exit_codes | PASS |
| R-019 | Invalid JSON returns 64 + FREEZE | test_invalid_json_is_input_error | PASS |
| R-020 | Manifest command deterministic | test_manifest_command_is_deterministic | PASS |
| R-021 | 500 deterministic random JSON inputs never crash | test_random_json_inputs_never_raise | PASS |

These statuses prove local companion behavior only, not NEXY.AI runtime integration.
