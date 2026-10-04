# Regression Matrix

The v0.1 executable suite covers the following control failures:

| Failure class | Expected control response | Test |
|---|---|---|
| Missing mandatory evidence | BLOCK | `test_missing_evidence_blocks_completion` |
| Protected target mutation | BLOCK + critical finding | `test_protected_scope_is_critical` |
| Unknown action scope | critical finding | `test_unknown_scope_is_unauthorized` |
| Re-asking a resolved directive | clarification-debt finding | `test_resolved_directive_reclarification_is_flagged` |
| Action based on assumption | assumption-pressure finding | `test_action_assumption_is_visible` |
| Explicit directive conflict | BLOCK | `test_explicit_conflict_blocks` |
| PASS without evidence reference | penalize + flag | `test_pass_without_reference_is_not_accepted_as_clean` |
| Duplicate directive identity | validation error | `test_duplicate_directive_rejected` |
| Repeated execution same input | identical report | `test_deterministic_report` |
| Batch mixed health | aggregate pass/block | `test_batch_aggregates_pass_and_block` |
| Canonical identity under object key reorder | same SHA-256 | `test_canonical_hash_ignores_dict_key_order` |
| Empty batch | validation error | `test_empty_batch_rejected` |

## Missing future tests
These are intentionally not claimed as implemented:
- semantic extraction accuracy from natural-language chats;
- freshness invalidation tied to external repository commits;
- wildcard/hierarchical scope matching;
- adversarial Unicode normalization policy;
- cryptographic signing of evidence bundles;
- runtime integration with NEXY.
