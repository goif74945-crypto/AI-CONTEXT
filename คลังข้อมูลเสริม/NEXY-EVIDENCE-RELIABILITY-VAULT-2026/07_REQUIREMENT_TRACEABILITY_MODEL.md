# Requirement Traceability Model

## Purpose
Connect the 837-row normalized source matrix to future implementation and evidence without claiming implementation exists.

## Trace tuple
T = {requirement_id, authority_class, source_anchor, build_scope, implementation_refs[], verification_refs[], evidence_refs[], status, revision}

## Status rules
- SOURCE_ONLY: requirement is normalized but implementation not evaluated.
- IMPLEMENTED_NOT_VERIFIED: code reference exists but required behavior evidence absent.
- PARTIAL: some mandatory acceptance conditions proven.
- PASS: all acceptance conditions proven at bound revision/environment.
- FAIL: direct evidence contradicts acceptance condition.
- BLOCKED/CONFLICT/UNKNOWN as defined by kernel.

## Cardinality
One requirement may map to many implementation refs and many evidence refs.
One implementation component may satisfy many requirements.
Never infer completeness from file count or component count.

## Coverage measures
Source coverage = requirements with valid source anchors / authoritative denominator.
Implementation mapping coverage = requirements with implementation refs / in-scope denominator.
Verification coverage = requirements with valid evidence / in-scope denominator.
Release coverage requires mandatory PASS, not merely mapped rows.

## NEXY current denominator
Use the current normalized matrix rules:
- total normalized rows: 837;
- current non-excluded/deferred worksheet: 773;
- deployment evidence rows: 52 are proof obligations, not implementation substitutes;
- legacy 215 and prior 262/518 counts are not interchangeable denominators.

## Change impact
When a requirement changes, invalidate linked acceptance/evidence nodes whose semantics changed. When code changes, invalidate evidence linked to affected implementation nodes. Preserve history rather than overwriting provenance.

## Query examples
- Which CURRENT_BUILD requirements lack implementation mapping?
- Which mapped requirements lack runtime evidence?
- Which PASS statuses are stale for current revision?
- Which deployment evidence obligations remain unmet?
- Which requirements are blocked by authority conflict?
