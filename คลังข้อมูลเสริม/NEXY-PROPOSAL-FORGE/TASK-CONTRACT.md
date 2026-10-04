# Task Contract — NEXY Proposal Forge

## Objective
Create a new, useful, non-duplicative supplemental system for NEXY.AI future ideation inside AI-CONTEXT without modifying the NEXY.AI implementation repository.

## Authority sources
1. Current user directive.
2. AI-CONTEXT execution kernel and project context.
3. NEXY.AI authority boundary and current source-normalization matrix.
4. Read-only current NEXY.AI repository observations.

## Authorized scope
- Create and update files only under `คลังข้อมูลเสริม/NEXY-PROPOSAL-FORGE/**` in `goif74945-crypto/AI-CONTEXT`.
- Run local verification against the exact files intended for persistence.

## Protected scope
- Every path in `goif74945-crypto/NEXY.AI-` is read-only.
- Existing AI-CONTEXT files outside the project directory are not to be modified by this execution.

## Immutable requirements
- Every generated idea must be labeled as an AI proposal, never canonical truth.
- The system must never silently promote a proposal into NEXY requirements.
- The system must fail closed on missing required evidence/authority metadata.
- Duplicate/near-duplicate detection must be deterministic.
- Evaluation must be deterministic for identical inputs.
- Output must preserve FACT / INFERENCE / ASSUMPTION / UNKNOWN separation.
- No network calls, hidden model calls, secrets, or mutable external dependencies are required to run the core evaluator.
- NEXY.AI repository must not be mutated.

## Deliverables
- Architecture/specification.
- Machine-readable proposal schema.
- Deterministic Python implementation.
- CLI.
- Example candidate inputs.
- Automated tests.
- Verification/evidence record.
- Durable resumption state.

## Acceptance criteria
- All automated tests pass.
- Repeated evaluation of identical input is byte-for-byte deterministic after canonical JSON serialization.
- Missing authority/evidence fields cannot yield an ADMIT recommendation.
- Exact duplicate cannot yield an ADMIT recommendation.
- High-overlap candidate cannot be silently treated as novel.
- Proposal output explicitly states that it is advisory and non-authoritative.
- All persisted project files can be re-read from GitHub after commit.

## Forbidden actions
- Modify, branch, merge, rename, delete, commit, or push anything in NEXY.AI.
- Claim implementation/deployment readiness for NEXY.AI.
- Treat the 215 historical registry as the current denominator.
- Invent source facts not established by evidence.

## Stop conditions
Freeze mutation if target repository identity changes, protected scope would be touched, current authority conflicts materially, or exact files cannot be verified after persistence.
