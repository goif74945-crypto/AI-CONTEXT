# C5 — Specification Mutation Sentinel (SMS)

**Classification:** PROPOSAL / standalone prototype

## Problem
A validator can remain green while never proving it rejects forbidden states. Happy-path tests establish acceptance, not enforcement. SMS generates one controlled illegal variant per constraint and checks that the validator rejects it.

## Prototype constraint operators
- exact equality;
- minimum integer;
- maximum integer;
- membership in an allowed tuple;
- non-empty value.

## Contract
1. Validate baseline against all constraints.
2. Refuse mutation testing if baseline is invalid.
3. Generate deterministic illegal mutations sorted by constraint ID.
4. Require the validator to return an actual boolean.
5. Run it on every mutated spec.
6. Report killed mutations and survivors.
7. PASS only when no illegal mutation survives.

## Critical invariant
Mutation generation is not arbitrary fuzzing. Each mutation is traceable to one constraint and expected to violate that constraint.

## Failure model
Invalid baseline, duplicate/malformed constraint, or non-boolean validator -> explicit error. Weak validator accepting an invalid mutation -> survivor / FAIL.

## Integration proposal
Use against NEXY policy/spec validators, compiler gates, configuration validators, or release checks. SMS belongs in test/assurance context, not production policy mutation.

## Tests
Strict validator kills all; weak validator produces survivors; invalid baseline; missing field; duplicate constraint; non-boolean validator; stress check that every synthesized mutation violates its target constraint.

## Trade-offs
Strength: proves guardrails reject known illegal classes.  
Risk: mutation operators define the tested attack surface.  
Mitigation: evolve operators from incidents/failures and preserve survivors as regression cases.
