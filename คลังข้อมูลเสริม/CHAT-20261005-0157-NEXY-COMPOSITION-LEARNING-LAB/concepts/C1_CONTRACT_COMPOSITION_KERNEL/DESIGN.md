# C1 — Contract Composition Kernel (CCK)

> **AI_PROPOSED_CONCEPT / NON-CANONICAL**

## Objective
Detect whether a set of independently described components can compose without unmet assumptions or contradictory guarantees.

## Input contract
Each component provides:
- `id`: stable unique string;
- `assumptions`: required literals;
- `guarantees`: literals established if admitted.

A literal is an opaque fact string. A leading `!` denotes the exact opposite literal. The prototype intentionally does not invent implication rules or semantic equivalences.

## Algorithm
1. Validate initial facts and component-local guarantees for direct contradictions.
2. Repeatedly find all pending components whose assumptions are a subset of current facts.
3. Admit ready components in deterministic lexical id order.
4. Before adding guarantees, freeze if any guarantee contradicts an existing fact.
5. If no pending component can be admitted, freeze with exact missing and contradicted assumptions.
6. Emit the admitted waves, final facts, status, reason, and deterministic fingerprint.

## Failure semantics
- `CONTRADICTORY_INITIAL_FACTS`
- `SELF_CONTRADICTORY_GUARANTEE`
- `UNSATISFIED_ASSUMPTIONS`
- `CONTRADICTORY_GUARANTEE`
- malformed input -> explicit validation exception

## Why NEXY could benefit
A component may be individually valid while an assembled execution graph is invalid. CCK provides a deterministic preflight layer for checking explicit assume/guarantee interfaces before a plan is allowed to execute.

## Limits
This is propositional literal closure, not SAT/SMT/theorem proving. A future production version would need a typed contract language, authority binding, provenance, and mapping to actual NEXY component identities.

## Code / tests
- Code: `src/nexy_aux/composition.py`
- Shared canonicalization: `src/nexy_aux/canonical.py`
- Tests: `tests/test_composition.py`, `tests/test_properties.py`, `tests/test_hardening.py`
