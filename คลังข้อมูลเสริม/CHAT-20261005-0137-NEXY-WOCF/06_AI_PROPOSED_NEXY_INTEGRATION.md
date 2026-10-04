# AI-Proposed NEXY Integration Concept

**Status: EXPERIMENTAL / AI-PROPOSED. Not current NEXY law or implementation.**

## Proposed placement
A future orchestrator could place WOCF between task decomposition and workstream creation:

```text
USER / CORE INTENT
      -> task decomposition
      -> proposed workstream manifests
      -> WOCF preflight
      -> atomic reservation layer
      -> worker/agent execution
```

## Integration invariants
- WOCF may narrow admission, never broaden user authority.
- `ALLOW` does not mean code is correct, safe, verified, or deployable.
- `FREEZE` should expose concrete collision evidence, not hidden model reasoning.
- A stale catalog version invalidates an earlier admission result.
- Human/operator override, if ever supported, must be an explicit higher-authority action with its own audit record. This prototype contains no override path.

## Potential user benefit
For large NEXY projects with many parallel agents/chats, users should see fewer duplicate research branches, fewer accidental write collisions, clearer ownership of new work, and less manual policing of who is touching what.

## Promotion requirements
Before any canonical adoption:
1. define a real workstream registry and atomic reservation contract;
2. validate false-positive/false-negative rates on historical project data;
3. integrate with actual scheduler/orchestrator in a sandbox;
4. execute concurrency/race tests;
5. document override authority and audit semantics;
6. obtain explicit project-authority approval.
