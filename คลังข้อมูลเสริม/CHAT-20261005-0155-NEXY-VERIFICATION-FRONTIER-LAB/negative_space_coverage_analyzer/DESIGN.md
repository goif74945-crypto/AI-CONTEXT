# Negative-Space Coverage Analyzer (NSCA) — Design

Status: **AI-PROPOSED / EXPERIMENTAL / NON-CANONICAL**

## Objective
Detect requirements whose intended behavior is defined by what the system **must refuse, deny, or freeze on**, but whose linked evidence contains only happy-path or otherwise insufficient tests.

## Problem
Traceability systems often count “a test references this requirement” as coverage. That can be dangerously wrong for negative obligations. A test proving a legal request succeeds does not prove an illegal request is denied.

## Inputs and outputs
- `Requirement(requirement_id, obligation, text)`.
- `Evidence(evidence_id, requirement_ids, polarity, status, evidence_class)`.
- `CoverageReport` with per-requirement findings and aggregate negative-space ratio.

Recognized negative obligations in v0.1: `FORBID`, `FREEZE_ON`, `DENY`, `MUST_NOT`.

## Invariants
1. Only explicit negative-polarity evidence can cover a negative obligation.
2. Evidence must be PASS and belong to the configured accepted evidence-class set.
3. Happy-path PASS evidence is reported separately as potentially misleading coverage.
4. Failed or too-weak negative evidence is reported but does not qualify.
5. Positive obligations are outside this analyzer's denominator.

Default accepted classes are E2–E7 because a behavioral prohibition normally needs executed behavior evidence. The caller may override that set explicitly when a specific claim legally accepts another class.

## Failure model
Duplicate IDs, invalid polarity, or empty accepted-class policy fail with `ValueError`. Unknown requirement IDs referenced by evidence are indexed but cannot create phantom requirements in the report.

## NEXY integration proposal
NSCA can consume a requirement/evidence trace export, identify negative-space debt, and hand those gaps to a planner such as VPO. It MUST NOT itself mark the overall project PASS or redefine which obligations are current authority.

## Evidence plan
E2 tests cover positive-evidence false coverage, qualifying negative E2 behavior, failed/static evidence rejection, positive-obligation exclusion, explicit evidence-class override, and duplicate evidence IDs. E3 lab integration turns an NSCA gap into a VPO proof-planning claim.

## Known limitations
- Obligation classification is explicit string metadata, not natural-language interpretation.
- It does not prove test quality beyond polarity/status/class metadata.
- It does not currently model freshness, exact commit binding, or environment identity; those belong to upstream evidence records.
