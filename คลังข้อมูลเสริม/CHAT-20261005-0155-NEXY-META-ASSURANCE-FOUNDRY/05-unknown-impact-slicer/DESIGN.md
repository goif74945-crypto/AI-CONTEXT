# Design — Unknown Impact Slicer (UIS)

Classification: `AI_PROPOSED_CONCEPT / REFERENCE_IMPLEMENTATION`

## Problem
"Unknown exists" is not the same as "unknown can change the legal result." Freezing on every unresolved field burdens the user, while guessing is unacceptable. A deterministic system can sometimes prove that an unknown is irrelevant to the current outcome.

## Exact finite model
UIS consumes:
- finite variables with explicit domains;
- currently known bindings;
- declarative rules mapping partial conditions to output labels;
- a default output;
- an explicit enumeration limit.

No expression evaluator or model inference is used.

For every completion of the unknown variables, UIS computes the legal output. Conflicting simultaneously matching rules with different outputs are a contract conflict and freeze.

## Result classes
- `STABLE`: every legal completion produces the same output. Unknowns remain unknown, but they are proven non-material to this decision surface.
- `MATERIAL_UNKNOWNS`: multiple outputs are reachable. UIS identifies each unknown variable for which changing only that variable can change output while all other unknown assignments are held fixed.
- `FREEZE`: malformed/conflicting rule system or bounded enumeration limit exceeded.

## Important boundary
UIS does not answer unknowns and does not decide whether the system is allowed to execute. It only proves impact/non-impact over the declared finite model. A downstream clarification optimizer can ask only about material unknowns.

## Integration proposal
Potential upstream companion to ambiguity handling: `detect unknowns -> UIS materiality proof -> ask only material unknowns -> CORE/JUDGE`. This can reduce unnecessary clarification without weakening zero-guess behavior.
