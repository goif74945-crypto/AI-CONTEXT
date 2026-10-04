# Task Contract — NEXY Shadow Execution Guard

Status: LOCKED FOR THIS MISSION
Classification: EXPERIMENTAL / AI-PROPOSED / ADVISORY-ONLY

## Objective

Create a standalone, deterministic pre-execution simulator that can evaluate a declared mutation plan against a supplied snapshot and scope policy before any real side effect occurs.

The tool must help a NEXY-like orchestrator answer:

> “If I execute exactly this declared plan against exactly this supplied snapshot, are all modeled effects within authorized scope, outside protected scope, consistent with preconditions, and recoverable under the selected reversibility policy?”

It must never execute the real plan.

## Required outputs

- Design and product-value documentation.
- Machine-readable plan/result schemas.
- Python reference implementation with no third-party runtime dependency.
- CLI.
- Unit/adversarial/CLI tests.
- RED→GREEN evidence for the implementation cycle.
- Validation runner.
- Integration proposal that does not mutate NEXY.AI.
- Clearly labeled AI-proposed future ideas.
- Final audit and resumable execution state.

## Inputs

A shadow plan containing:
- a supplied logical resource snapshot;
- explicit authorized/protected scope selectors;
- an ordered operation list;
- operation preconditions;
- payloads for modeled writes;
- execution limits;
- reversibility policy.

## Immutable requirements

R1. Real external side effects are forbidden.
R2. Protected scope overrides authorized scope.
R3. Unmodeled/opaque effects freeze; they are never assumed safe.
R4. Resource keys must be normalized and traversal/control-character forms rejected.
R5. Ordered operations are simulated against evolving simulated state.
R6. Preconditions are checked against the state immediately before that operation.
R7. The tool must distinguish malformed input from a valid plan that freezes.
R8. Output must be deterministic for identical semantic input.
R9. No wall-clock data may enter the deterministic certificate body.
R10. Rollback feasibility must be explicit; missing restore bytes cannot be called reversible.
R11. A result is advisory only and cannot authorize a NEXY mutation.
R12. No NEXY.AI repository is modified.
R13. Unknown policy/operation semantics must fail closed.
R14. Static scope violations must be discoverable before modeled mutation starts.
R15. Evidence claims must remain limited to the standalone lab and the local test environment.

## Acceptance criteria

- All in-scope tests pass from a clean local invocation.
- Python bytecode compilation succeeds.
- CLI returns separate exit codes for preview pass, valid freeze, and invalid input.
- Adversarial tests cover traversal, stale preconditions, protected scope, unauthorized scope, opaque effects, destructive rollback gaps, duplicate IDs/resources, and limits.
- Determinism is tested.
- Persistence is verified by GitHub read-after-write after publication.
- Final audit lists all known limitations without claiming integration/deployment evidence.

## Required evidence

- E1: Python compile + schema JSON parse.
- E2: executed unit/adversarial suite.
- E3-like local component proof: CLI invokes parser/engine/result serialization end-to-end inside the local sandbox.
- Persistence proof: GitHub read-after-write on representative published artifacts.

## Stop / freeze conditions

Freeze mission mutation if:
- target repository identity changes;
- write would escape the authorized folder;
- target path unexpectedly exists before create;
- permission becomes insufficient;
- a required behavior cannot be tested;
- a secret/credential would need to be persisted;
- completing the lab would require modifying a NEXY.AI repository.

## Non-goals

- Real tool execution.
- Production deployment.
- Full provider-specific tool semantics.
- Filesystem symlink resolution.
- Database transaction simulation.
- Network-call replay.
- Canonical promotion into NEXY requirements.
