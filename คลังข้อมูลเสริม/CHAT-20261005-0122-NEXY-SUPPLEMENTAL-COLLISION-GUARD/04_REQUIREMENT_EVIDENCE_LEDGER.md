# Requirement and Evidence Ledger

Status values follow AI-CONTEXT verification law.

| ID | Requirement | Evidence target | Class | Current status |
|---|---|---|---|---|
| R01 | Work exists only in authorized AI-CONTEXT supplemental directory | GitHub target path/read-back | E0 | PENDING_REMOTE |
| R02 | No repository whose name contains `NEXY.AI` is mutated | tool/action history + mutation target audit | E0/action receipt | PASS_SO_FAR |
| R03 | Project responsibility is distinct from inspected sibling workstreams | root-name scan + adjacent workstream memory inspection | E0/read evidence | PASS_BOUNDED |
| R04 | Same inputs produce deterministic ranking/order | `test_result_order_is_deterministic` | E2 | PASS |
| R05 | Exact duplicate reaches `LIKELY_DUPLICATE` | `test_exact_duplicate_is_likely_duplicate` | E2 | PASS |
| R06 | Strong near-duplicate is not automatically exact duplicate | `test_flags_near_duplicate_with_explanation` | E2 | PASS |
| R07 | Orthogonal candidate can remain `DISTINCT` | `test_marks_orthogonal_candidate_distinct` | E2 | PASS |
| R08 | Generated output cannot recursively change fingerprint | `test_generated_directory_does_not_change_project_fingerprint` | E2 | PASS |
| R09 | Relative path is part of fingerprint identity | `test_relative_file_path_changes_content_hash` | E2 | PASS |
| R10 | Missing root fails | `test_missing_root_is_rejected` | E2 | PASS |
| R11 | Blank candidate title fails | `test_blank_candidate_title_is_rejected` | E2 | PASS |
| R12 | Generic-only/no-discriminating candidate fails | unit + CLI negative tests | E2 | PASS |
| R13 | Symlinked file cannot pull outside content into fingerprint | `test_symlinked_file_outside_project_is_not_read` | E2 | PASS |
| R14 | Symlinked project directory is ignored | `test_symlinked_project_directory_is_ignored` | E2 | PASS |
| R15 | CI gate returns nonzero when threshold is met | `test_fail_at_high_overlap_returns_policy_exit_code_2` | E2 | PASS |
| R16 | CI gate permits distinct candidate at same threshold | `test_fail_at_high_overlap_allows_distinct_candidate` | E2 | PASS |
| R17 | Invalid CLI input is cleanly rejected without traceback | `test_cli_rejects_candidate_without_discriminating_terms_without_traceback` | E2 | PASS |
| R18 | Python source/tests compile | `python -m compileall -q src tests` | E1 | PASS |
| R19 | Full current suite executes | unittest discovery + direct-file invocation | E2 | PASS |
| R20 | JSON schema is syntactically valid | JSON parser | E1 | PASS |
| R21 | Immutable payload hash manifest matches persisted files | SHA-256 local + GitHub read-back | E0/integrity | PENDING_REMOTE |
| R22 | No unfinished placeholder markers shipped | static text scan | E1 | PASS |
| R23 | No third-party runtime dependency | import/static inspection | E1 | PASS |

## Evidence interpretation

`PASS_BOUNDED` for R03 means: no same-responsibility project was found in the **inspected current root names and specifically inspected adjacent workstream records**. It is not an exhaustive proof that no semantically equivalent file exists anywhere in the repository.

`PASS_SO_FAR` for R02 becomes a final PASS only after all persistence actions are complete and the mutation receipt confirms every write targeted AI-CONTEXT.
