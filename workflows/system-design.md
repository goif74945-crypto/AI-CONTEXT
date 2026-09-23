# WORKFLOW — SYSTEM DESIGN

## Goal
Convert intent into an implementable, testable architecture.

## Pipeline
`INTENT → REQUIREMENTS → INVARIANTS → BOUNDARIES → DATA/STATE → FAILURE → SECURITY → INTERFACES → TEST MODEL → BUILD ORDER`

## Design contract
Define:
- purpose/non-goals;
- actors/authority;
- functional requirements;
- nonfunctional requirements;
- invariants;
- modules and ownership;
- interfaces/contracts;
- data model and provenance;
- state machines;
- concurrency/order semantics;
- failure/recovery;
- security/trust boundaries;
- observability;
- version/evolution law;
- evidence/acceptance tests.

## Rules
- every state mutation has an owner;
- every external boundary validates input;
- every durable object has provenance/identity;
- every failure has a defined state/behavior;
- every requirement maps to a test/evidence path;
- avoid architecture that depends on hidden model behavior.

## Deliverables
At minimum:
1. architecture map;
2. contracts;
3. invariants;
4. failure model;
5. requirement ledger;
6. build order;
7. verification plan.
