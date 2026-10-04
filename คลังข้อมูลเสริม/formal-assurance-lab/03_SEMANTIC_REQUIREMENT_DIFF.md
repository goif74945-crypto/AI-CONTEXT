# Semantic Requirement Diff

Status: PROPOSAL

## Problem
Line diffs detect text changes. Verification systems need to detect obligation changes.

## Canonical requirement record
R = {
 id,
 authority_class,
 scope_class,
 actor,
 action,
 object,
 modality,
 conditions,
 thresholds,
 units,
 exceptions,
 forbidden_behavior,
 evidence_class,
 source_anchor,
 version,
 supersedes
}

## Modality
Recommended normalized values:
MUST
MUST_NOT
SHOULD
SHOULD_NOT
MAY
INFORMATIONAL

Modality extraction is never enough by itself; authority_class remains separate.

## Change classes
SD01 AUTHORITY_CHANGE
SD02 SCOPE_CHANGE
SD03 MODALITY_STRENGTHEN
SD04 MODALITY_WEAKEN
SD05 ACTOR_CHANGE
SD06 ACTION_CHANGE
SD07 OBJECT_CHANGE
SD08 CONDITION_CHANGE
SD09 THRESHOLD_CHANGE
SD10 UNIT_CHANGE
SD11 EXCEPTION_CHANGE
SD12 FORBIDDEN_BEHAVIOR_CHANGE
SD13 EVIDENCE_REQUIREMENT_CHANGE
SD14 SOURCE_ANCHOR_CHANGE
SD15 SPLIT
SD16 MERGE
SD17 DEPRECATE
SD18 ADD
SD19 REMOVE
SD20 AMBIGUITY_CHANGE

## Impact levels
P0: can alter legal/illegal side effects, authority, security, release decision.
P1: can alter behavior or acceptance.
P2: changes evidence/test obligations without intended product behavior change.
P3: editorial/clarifying with no normalized semantic change.

Impact must be proven from normalized fields, not guessed from line count.

## Example
Old: "System should reject stale evidence."
New: "System must reject evidence whose source identity differs from the target release."
Potential diff:
- modality strengthened SHOULD -> MUST
- condition clarified
- object narrowed/defined
- likely P1/P0 depending on release authority

## Required output
For each changed requirement:
- old normalized record
- new normalized record
- semantic change classes
- affected dependencies
- proofs invalidated
- migration action
- unresolved ambiguity

## Anti-false-positive tests
- whitespace/reflow only -> no semantic change
- equivalent unit conversion with exact equality -> no threshold change
- renamed heading without changed source identity semantics -> editorial
- reordered clauses with same logic -> no semantic change

## Anti-false-negative tests
- 5 min -> 10 min must be caught
- <=5 -> <5 must be caught
- user -> admin must be caught
- may -> must must be caught
- "except X" added must be caught
- evidence E3 -> E4 must be caught
- current -> future/deferred scope must be caught

## NEXY relevance
FACT_PROJECT: the current normalized source matrix already distinguishes authority/scope and has 837 rows. A future semantic diff system should operate on explicit normalized records rather than revive deprecated registry counts.
