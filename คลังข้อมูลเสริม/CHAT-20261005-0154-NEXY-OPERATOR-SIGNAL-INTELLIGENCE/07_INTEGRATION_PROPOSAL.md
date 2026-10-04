# Proposed NEXY Integration

Status: AI proposal / NOT_VERIFIED in NEXY production.

## Suggested boundary
- NEXY core remains authoritative for task state, laws, evidence, freeze, and actions.
- An adapter emits a minimal `OperatorSignal` envelope after those authoritative decisions.
- This lab only determines operator-facing salience/delivery/compression and digest/debt structure.

## Candidate composition
- `NEXY::PULSE` -> progress and system-state signals -> Salience/Interruption/Milestone modules.
- `NEXY::JUDGE` -> completion/freeze evidence state -> non-suppressible operator signal.
- `NEXY::GUARD` -> security/safety signal -> CRITICAL/NOW + acknowledgement debt.
- `NEXY::VIEW` -> Outcome Delta result -> concise final "what changed" surface.

## Adoption gates
Before real adoption:
1. define canonical adapter schema from current NEXY source law;
2. map all legal event/evidence states explicitly;
3. run integration tests against exact NEXY revision;
4. test accessibility/localization transport separately;
5. load/fault-test event bursts;
6. prove no required alert can be lost by persistence/transport layers.

No adoption gate is claimed complete here.
