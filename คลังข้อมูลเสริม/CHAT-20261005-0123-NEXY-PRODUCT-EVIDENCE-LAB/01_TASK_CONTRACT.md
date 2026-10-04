# TASK CONTRACT — NEXY Product Evidence Lab

objective: Build and verify a standalone deterministic product-evidence compiler/evaluator useful to future NEXY product work.
target: คลังข้อมูลเสริม/CHAT-20261005-0123-NEXY-PRODUCT-EVIDENCE-LAB/
authorized_scope:
  - create new files only under the target folder
protected_scope:
  - all existing files outside the target folder
  - all repositories whose name contains NEXY.AI
authority_sources:
  - user request in current conversation
  - AI-CONTEXT/AI-EXECUTION-KERNEL.md
  - projects/NEXY.AI/overview.md
  - projects/NEXY.AI/requirements.md
  - projects/NEXY.AI/architecture.md
preconditions:
  - AI-CONTEXT repository is accessible and writable
  - target folder name is not already present
success_invariants:
  - no protected-scope mutation
  - proposal is explicitly marked AI-PROPOSED
  - deterministic reference code has no network dependency
  - material missing inputs yield validation failure or FREEZE, never guessed defaults
  - experiment output never auto-authorizes release/deploy/ship
  - tests are actually executed before PASS claims
forbidden_actions:
  - modify NEXY.AI repository
  - fabricate evidence
  - use hidden randomness in critical evaluation
  - persist secrets
required_evidence:
  - repository read evidence for authority/context
  - local syntax/static execution
  - executed unit tests
  - post-write repository readback
stop_conditions:
  - any required write would leave authorized scope
  - source authority conflict affecting correctness
  - test failures not repairable within current task
deliverables:
  - architecture and requirements
  - reference Python package
  - unit/adversarial tests
  - example contracts
  - validation report
  - research backlog
  - final audit/resumption state
