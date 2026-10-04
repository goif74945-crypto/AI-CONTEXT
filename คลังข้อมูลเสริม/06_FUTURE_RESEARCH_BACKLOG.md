# Future Research Backlog — High-Leverage, Non-Source Work
Status: PROPOSAL

These tasks are intentionally suitable for AI-CONTEXT and do not require editing NEXY.AI source.

## P0
### R1 Authority Graph Extractor
Research schema for mapping specs -> invariants -> implementation -> tests -> evidence.
Deliverable: machine-readable graph format + orphan detection rules.

### R2 Evidence Closure Auditor
Define algorithm that answers: “Which release claims still lack a valid proof path?”
Key property: dependency-aware invalidation.

### R3 Context Poisoning Corpus
Build adversarial documents/issues/web snippets that attempt authority escalation, memory persistence, stale-spec resurrection and tool misuse.

### R4 FREEZE Conformance Suite
Catalog scenarios where an agent must refuse to select an output because uniqueness/authority/evidence is missing.

## P1
### R5 Determinism Threat Model
Inventory hidden nondeterminism: locale, timezone, filesystem order, network, clocks, randomness, concurrency, dependency resolution, compiler/runtime versions, floating behavior, caches.

### R6 Semantic Requirement Diff
Research diffing that detects normative changes such as MUST/SHALL/NEVER, thresholds, scope and authority rather than line changes only.

### R7 Proof-Carrying Context
Each retrieved chunk carries provenance and verification metadata; generated conclusions cite dependency graph nodes.

### R8 Negative Capability Registry
Represent what each subsystem/agent explicitly cannot do. Use it to prevent accidental capability creep.

## P2
### R9 Failure Knowledge Base
Normalize historical failures into trigger/root-cause/fix/regression-test/affected-invariant records.

### R10 Counterfactual Release Testing
Ask: if one proof, dependency, permission, or source identity were wrong, would the release process still incorrectly pass?

### R11 Agent Blast-Radius Model
Quantify maximum damage per capability grant and workflow stage.

### R12 Long-Horizon Drift Tests
Repeated multi-step agent runs to detect instruction dilution, scope creep and memory poisoning over time.

## Research quality gate
A backlog item becomes recommended architecture only after:
- project relevance demonstrated
- assumptions explicit
- threat/failure model included
- measurable acceptance criteria defined
- evidence source identified
- conflicts with authoritative NEXY rules checked
