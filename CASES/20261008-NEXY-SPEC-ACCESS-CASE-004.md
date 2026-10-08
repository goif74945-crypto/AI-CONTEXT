# CASE — NEXY Specification Access and Authority Reconciliation

CASE_ID: 20261008-NEXY-SPEC-ACCESS-CASE-004
TASK_ID: 20261008-NEXY-CODEX-NEXT-COMMAND-004
CATEGORY: AUTHORITY / EVIDENCE / BLOCKER_SCOPE
STATUS: RESOLVED_FOR_VERIFIED_EXTRACTS_ONLY

OBSERVATION:
The preceding Codex execution classified AUTH-01, AUTH-02, AUTH-03, SCOPE-01 as SPEC_SOURCE_ACCESS_BLOCKED because it could not access the original design DOCX. A separate authenticated audit environment has the uploaded DOCX bytes and a matching required SHA256.

EVIDENCE:
Original DOCX SHA256:
b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

Verified extracts:
EVIDENCE/20261008-NEXY-SPEC-AUTHORITY-RESOLUTION-004.md

IMPACT:
A blanket source-access block prevents row-specific authority classification despite verifiable extracts. However the extracts cannot establish every normative requirement throughout the full DOCX.

RULING:
For the four rows, use their exact available source locators and audit current source individually. Do not automatically mark them VERIFIED. Any missing normatively relevant passage remains blocked locally.

PREVENTION:
Record spec digest, exact paragraph locators, source-to-row bindings, and known scope limits in AI-CONTEXT.

LIMITS:
This is not deployment approval or proof of implementation compliance.

FINAL_STATUS: CLOSED_AS_CONTROL_HANDBACK.
