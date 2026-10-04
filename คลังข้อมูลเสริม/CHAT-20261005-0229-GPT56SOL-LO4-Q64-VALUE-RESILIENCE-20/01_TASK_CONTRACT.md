# Task Contract

## Objective
Create twenty novel Lo4 systems that can integrate with NEXY.AI later without mutating any NEXY.AI repository, implement them with Q64.64 decision arithmetic, execute real tests, and retain design/code/test/evidence together.

## Authorized scope
- Create files only under this new folder in `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม`.
- Read NEXY.AI context for compatibility and authority boundaries.

## Protected scope
- Any repository whose name contains `NEXY.AI` is read-only.
- Canon, DOC-B/C/D/E and current implementation state are not modified.

## Success invariants
1. Exactly 20 unique concept IDs.
2. All quantitative engine inputs and outputs use integer-backed Q64.64.
3. No Python float is accepted by Q64 constructors or used in engine formulas.
4. Missing/extra/out-of-domain input fails closed.
5. Q64 overflow and divide-by-zero fail explicitly.
6. Low-confidence result freezes.
7. Canonical serialization is key-order independent and deterministic.
8. Unit, adversarial boundary, integration, compile and replay tests pass locally.
9. Evidence files and manifest are persisted beside code.
10. No claim of Canon promotion or NEXY.AI production integration is made.

## Evidence class
Local isolated runtime evidence proves this package executes under the local Python runtime only. It does not prove NEXY.AI repository integration or deployment behavior.
