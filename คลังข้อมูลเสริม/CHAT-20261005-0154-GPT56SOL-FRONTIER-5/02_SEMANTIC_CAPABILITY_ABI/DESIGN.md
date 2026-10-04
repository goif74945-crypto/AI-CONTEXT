# Semantic Capability ABI Compiler (SCAC) — Design

## Problem
Provider adapters often agree on names but disagree on semantics. `search`, `tool_call`, or `json_output` can have incompatible guarantees even when APIs connect successfully.

## Objective
Compile a provider declaration against a provider-neutral capability ABI. Binding succeeds only when version, schema hashes, determinism level and evidence floor satisfy the contract.

## Invariants
- Exact major ABI compatibility is required.
- Required capability cannot disappear silently.
- Provider evidence class must meet or exceed contract floor.
- Determinism guarantees cannot be weaker than the contract.
- The binding-plan digest is canonical and reproducible.

## Output
PASS with immutable binding plan, or FREEZE with deterministic reasons.
