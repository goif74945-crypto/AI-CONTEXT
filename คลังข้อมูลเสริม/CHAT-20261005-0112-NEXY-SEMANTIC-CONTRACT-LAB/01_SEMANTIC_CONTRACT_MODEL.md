# Semantic Contract Model

A semantic contract is the machine-checkable boundary between authorized intent and executed or claimed meaning.

## Contract tuple
C = <O,A,S,I,K,R,F,V,E,T>
O objective; A authority; S scope; I inputs; K immutable constraints; R required behavior; F forbidden behavior; V validation; E evidence; T stop conditions.

## Meaning preservation chain
User intent -> normalized contract -> plan -> tool calls -> observed state -> verification evidence -> completion claim.

Every edge can lose meaning. Record explicit mappings.

## Stable IDs
OBJ-### objectives
AUTH-### authority rules
SCOPE-### scope clauses
INV-### invariants
REQ-### required behaviors
FORBID-### forbidden behaviors
VAL-### validation clauses
EVID-### evidence records
STOP-### stop conditions

## Traceability
Every critical action maps to REQ or VAL.
Every critical requirement maps to verification.
Every completion claim maps to evidence.
Orphan action = suspected scope expansion.
Orphan requirement = incomplete work.

## Truth states
PASS = direct verification.
FAIL = contradictory observation.
UNKNOWN = absent information.
BLOCKED = cannot safely proceed.
NOT_APPLICABLE = explicitly outside contract.
UNKNOWN never collapses into PASS.

## Mutation contract
Before a write: resolve exact target, prove scope, inspect pre-state, define post-state, define recovery, execute, read back, compare.

## Completion contract
COMPLETE is legal only when all critical requirements and validations pass, no critical prohibition is violated, required deliverables exist, evidence is readable, and no unresolved critical contradiction remains.
