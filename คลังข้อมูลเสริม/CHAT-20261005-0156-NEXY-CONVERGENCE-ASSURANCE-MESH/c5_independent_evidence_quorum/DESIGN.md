# C5 — Independent Evidence Quorum Engine (IEQE)

Status: `AI_PROPOSED_CONCEPT`

## Objective
Prevent a claim from appearing well-proven merely because multiple evidence records share the same producer, runner, upstream evidence, or common failure domain.

## Inputs
Each `EvidenceRecord` declares:
- claim ID;
- evidence class;
- producer;
- explicit failure domains;
- `derived_from` evidence IDs.

A `QuorumNeed` declares minimum evidence class and required number of independent witnesses.

## Independence rule
For every candidate evidence record, IEQE recursively expands its ancestry. Two selected witnesses are independent only if their expanded closures have:
- no shared evidence IDs;
- no shared producers;
- no shared failure domains.

Dependency cycles or missing ancestor IDs block evaluation as an invalid evidence graph.

## Invariants
1. Lower evidence class is never eligible.
2. Distinct filenames are not treated as independence.
3. Derived evidence inherits all parent producer/failure-domain dependencies.
4. Common-mode overlap freezes.
5. Selection is deterministic by sorted evidence ID and exact combinations.

## NEXY value
Raises assurance against self-confirming/circular verification and common-mode tool/CI/model failures, especially when a final judge receives many superficially different proofs.
