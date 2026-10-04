# Specification Compiler for Agentic Engineering

## Purpose
Convert natural-language project requirements into an executable intermediate representation (IR) before implementation begins. The goal is not prettier documentation. The goal is to prevent silent requirement loss.

## Core IR
Each requirement becomes a record:
- RID: stable requirement identifier
- authority: user/spec/project/official-doc/tool-result/inference
- modality: MUST | MUST_NOT | SHOULD | MAY
- scope: component, file, route, API, workflow, or global
- trigger: when the requirement applies
- behavior: observable required behavior
- evidence: how compliance can be demonstrated
- dependencies: prerequisite RIDs
- conflicts: incompatible RIDs
- failure_policy: expected behavior when impossible
- mutability: immutable | controlled | provisional
- status: unimplemented | partial | implemented | verified | blocked

## Compilation pipeline
1. Parse statements without weakening modal verbs.
2. Split compound requirements only when semantics remain identical.
3. Resolve pronouns and implicit subjects from authoritative context.
4. Normalize duplicate statements while preserving provenance.
5. Build dependency and conflict graphs.
6. Reject unresolved contradictions on critical paths.
7. Emit implementation obligations and verification obligations separately.
8. Freeze immutable RIDs before mutation begins.

## Anti-loss rule
No implementation task may exist without one or more parent RIDs. No RID may be declared complete without evidence. This creates bidirectional traceability:
Requirement -> Work -> Artifact -> Test -> Evidence -> Requirement.

## Example
Input: "Search must never fabricate a vehicle when upstream data is missing."
IR:
RID: DATA-SEARCH-017
modality: MUST_NOT
trigger: upstream record absent
behavior: synthesize vehicle result
expected: fail explicitly with typed absence
evidence: negative test + response fixture
mutability: immutable

## Compiler failures
- Ambiguous authority
- Contradictory MUST clauses
- Missing acceptance evidence
- Unbounded scope
- Undefined term affecting behavior
- Requirement whose success cannot be observed

A compiler failure is a design event, not permission to guess.
