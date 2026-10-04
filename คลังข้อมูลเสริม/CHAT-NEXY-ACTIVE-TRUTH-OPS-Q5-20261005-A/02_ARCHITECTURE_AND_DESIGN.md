# Architecture and Design

Classification: AI_PROPOSED / EXPERIMENTAL / NOT_CANON

## Global invariants
G1. Explicit authority outranks model proposal.
G2. UNKNOWN cannot be silently promoted to FACT.
G3. Deterministic selection uses exact canonical ordering and SHA-256 fingerprints.
G4. Core functions are pure with no hidden external I/O.
G5. Bounded exact-search planners reject inputs above their declared search bound rather than silently switch to an unverified heuristic.
G6. Plans and candidates do not execute mutations.
G7. Evidence class matching is exact; a numerically higher class does not automatically substitute for a different required class.

## AEAP — Active Evidence Acquisition Planner
Objective:
Choose a deterministic evidence collection plan from explicit evidence needs and a finite probe catalog.

Inputs:
- evidence needs with id, required evidence class and blocking/optional status;
- probes with produced evidence, explicit dependencies, cost, latency, risk, enabled/destructive properties;
- explicit planner bounds/policy.

Required behavior:
- exact bounded subset search, maximum 20 candidate probes;
- all blocking needs must be covered;
- optional evidence value is optimized only after mandatory coverage;
- dependencies must be present and cycle-free;
- return selected probes, dependency-safe deterministic topological execution order, per-need coverage witness and fingerprint.

Optimization:
mandatory coverage -> optional value -> lower risk -> lower cost -> lower latency -> fewer probes -> canonical ID tie break.

Forbidden:
executing probes, generating evidence, claiming a need is satisfied without a declared producer.

Failure:
malformed input, dependency cycle, structural impossibility or bound violation returns fail-closed result/error rather than an invented plan.

## RCTC — Runtime Contract Telemetry Compiler
Objective:
Compile a finite approved invariant plus declared event schema into a deterministic pure monitor.

Supported predicate forms:
FIELD_PRESENT, EQUALS, ENUM, NUMERIC_RANGE.

Required behavior:
- authority.status must equal APPROVED;
- referenced fields must exist in the declared schema where required;
- compile to canonical monitor contract with deterministic fingerprint;
- pure evaluator returns PASS, VIOLATION or BLOCKED;
- no alarm emission, state mutation or external I/O.

Authority barrier:
Candidate or discovered invariants cannot self-promote. IDW output requires an external authorized promotion before RCTC compilation is legal.

## IDW — Invariant Discovery Workbench
Objective:
Mine bounded accepted/rejected trace examples for candidate invariants without granting them authority.

Input model:
trace ID, accepted/rejected label, scalar JSON primitive observations.

Candidate families:
FIELD_PRESENT, CONSTANT, ENUM, NUMERIC_RANGE, FIELDS_EQUAL.

Required behavior:
- runtime validator rejects nested/non-primitive observation values;
- maximum 64 fields, enum cardinality maximum 32;
- candidate must hold across accepted support and have at least one rejected counterexample;
- output exact supportTraceIds and counterexampleTraceIds;
- all output authority is CANDIDATE_ONLY;
- deterministic canonical candidate ordering/fingerprint.

Forbidden:
probabilistic confidence fabrication, auto-promotion to rule, direct mutation of RCTC authority.

## CDPP — Causal Diagnostic Probe Planner
Objective:
Select explicit probes that discriminate a finite set of declared causal hypotheses.

Inputs:
hypothesis IDs and probe catalog whose outcome prediction for each hypothesis is explicitly supplied by the caller.

Required behavior:
- never infer missing hypotheses or predictions;
- exact bounded subset search, maximum 20 probes;
- every hypothesis pair must have at least one selected probe with different declared outcome predictions;
- return unresolved pairs when complete discrimination is structurally or budget impossible;
- return per-pair discrimination witnesses and deterministic fingerprint.

Optimization:
lower risk -> lower cost -> fewer probes -> canonical ID tie break.

Forbidden:
executing probes, claiming a root cause, treating correlation as causation.

## CRG — Contract Retirement Gate
Objective:
Prevent unsafe contract/interface retirement.

Required gates:
- consumer inventory complete;
- no consumer state UNKNOWN;
- no active consumers;
- declared no-use window complete with zero observed calls;
- usage evidence fresh;
- replacement parity PROVEN and evidence fresh;
- rollback documented, tested and evidence fresh;
- explicit retirement authority approved and fresh.

Decision states:
FREEZE = epistemic insufficiency such as incomplete/unknown/stale evidence.
HOLD = known facts show retirement conditions are not yet met.
RETIRE_CANDIDATE = all gates pass.

Output:
reason codes, blocking consumers, per-gate PASS/HOLD/FREEZE checks and fingerprint.

Forbidden:
deleting or modifying any contract, automatically authorizing retirement.

## Cross-system composition
IDW -> external authority review/promotion -> RCTC -> pure monitoring.
RCTC violation can be represented through a NEXY-compatible advisory adapter.
AEAP may plan evidence collection needed by verification workflows.
CDPP may plan diagnostic experiments from already-declared hypotheses.
CRG may consume externally verified usage/replacement/rollback/authority facts.

No arrow grants execution authority by itself.
