# Task Contract

- objective: Design, implement and test five new high-value standalone systems compatible in principle with NEXY.AI while never modifying the NEXY.AI repository.
- target: `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0155-NEXY-FIVE-FORGE/`
- authority_sources:
  1. current user directive;
  2. AI-CONTEXT `AI-EXECUTION-KERNEL.md`;
  3. AI-CONTEXT NEXY.AI project overview/current normalized matrix;
  4. AI-CONTEXT global security/verification rules.
- authorized_scope: create new files only under the target supplemental folder.
- protected_scope: every repository whose name contains `NEXY.AI`; all existing files outside the new folder.
- success_invariants:
  - five distinct ideas exist;
  - each has design, code and tests;
  - tests are actually executed in a sandbox;
  - evidence records distinguish design/prototype/runtime/integration truth classes;
  - no secrets or credentials are committed;
  - no NEXY.AI implementation repository is changed.
- required_evidence: E1 syntax/static importability and E2 unit behavior for standalone prototypes; E3+ NEXY integration is explicitly NOT VERIFIED.
- forbidden_actions: modify/delete/rename any NEXY.AI repository content; claim NEXY integration or deployment without evidence.
- stop_conditions: target ambiguity, write authorization loss, collision that invalidates novelty, or failing tests that cannot be repaired safely.
- deliverables: README, temporary memory, five design specs, five Python implementations, aggregate tests, integration notes, evidence report and final audit.
