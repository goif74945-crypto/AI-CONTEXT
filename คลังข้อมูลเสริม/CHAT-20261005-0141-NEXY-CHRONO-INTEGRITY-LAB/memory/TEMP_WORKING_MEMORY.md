# Temporary Working Memory / Resumption Checkpoint

## Workstream
`CHAT-20261005-0141-NEXY-CHRONO-INTEGRITY-LAB`

## Mission
Create a novel supplemental NEXY-compatible chrono/deadline integrity primitive while never modifying a repository whose name contains `NEXY.AI`.

## Final verified state
- standalone implementation exists in AI-CONTEXT;
- compile/static validation PASS;
- 42/42 tests PASS after final exact-set normalization;
- deterministic demo PASS;
- executable Git blobs on main match the final local tested bytes;
- README/evidence/execution state published;
- PR #42 merged successfully;
- no NEXY.AI repository mutation occurred.

## Concept boundary
Do not merge these responsibilities:
- Temporal Truth = proposition validity/admissibility;
- Delegation Lease = bounded execution authority;
- Chrono Integrity = clock continuity + elapsed deadline semantics.

## Locked semantics
- monotonic elapsed drives activation/expiration;
- wall time is a cross-check, not TTL authority;
- `elapsed >= timeout => EXPIRED`;
- clock-ID mismatch, epoch mismatch, monotonic rollback, or excessive wall/monotonic divergence => `FREEZE`;
- child budget may only narrow parent remaining budget;
- strict canonical serialization rejects unknown/missing/type-invalid fields;
- this is an AI-proposed, non-canonical supplemental design.

## Evidence anchors
- source blob `33477fe7af548b45a120b8f3db68e533783ef33c`
- tests blob `b831cde8a85f583668e29a5d9fe66d761bc3ddc4`
- pyproject blob `a3438cb2f2a74659de5e5fbeca1418c7921b3996`
- demo blob `b62687e762a7c62076ff7029935064455da57b8e`
- finalization merge `4884f096cb56d56b2a65ec08b39441bcdb31d6d8`

## Safe resume
Read README, EXECUTION_STATE, and evidence first. Do not re-open the design as canonical NEXY scope. Any actual NEXY integration requires a new explicit authorization and new E3/E4/E5 verification.

## Remaining research only
- restart continuity;
- trusted/multi-node time;
- platform suspend/resume and VM snapshot semantics;
- temporal chaos qualification;
- concrete adapters for future authorized NEXY subsystems.

These remain proposals, not current implementation.
