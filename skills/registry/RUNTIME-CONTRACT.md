# AI-CONTEXT Skill Registry Runtime Contract

DISCOVER → SELECT → LOAD → COMPOSE → EXECUTE → VERIFY

## DISCOVER
Parse intent, domain, constraints, authority, expected output and validation needs, then query `registry/registry.json`.

## SELECT
Reject authority/scope conflicts, BLOCKED skills, missing dependencies and permission mismatches. Prefer VERIFIED, then MATERIALIZED, then CATALOGED.

## LOAD
Resolve the exact ID, open `load_path`, and locate `locator`. Validate identity before use.

## COMPOSE
Expand dependencies, detect cycles, and build a deterministic DAG. Dependencies execute before dependents.

## EXECUTE
Pass task, current_context, authority, scope, inputs, dependencies, expected_output and validation_requirements. Propagate FAIL/BLOCKED/UNKNOWN.

## VERIFY
Check outcome, scope, dependency completion, validation and evidence. Missing evidence means NOT VERIFIED.

## Stop conditions
Authority conflict; unresolved requirement conflict; missing dependency; cycle; permission violation; integrity failure; unverifiable evidence; critical validation failure; scope expansion.

## Runtime boundary
The Registry routes and identifies Skills. It does not itself grant permissions or execute arbitrary code; an execution backend is required.

## Current branch audit note
The branch `nexy-skill-runtime-canonical-v2` contains a Python execution backend candidate, but the authoritative Master Specification explicitly leaves the concrete Skill runtime/loader implementation UNSPECIFIED. Therefore the branch candidate is NOT VERIFIED as the canonical runtime. No runtime architecture is being invented in this forensic round.
