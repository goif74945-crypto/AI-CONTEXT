# NEXY.AI Governance Intelligence

## Purpose
Resolve **authority, scope, supersession, and contradiction** before AI builds/audits NEXY.

Files:
- `authority-graph.json` — what source has authority over what question/domain.
- `scope-registry.json` — CURRENT/FUTURE/DEFERRED/EXCLUDED/HISTORICAL semantics and promotion rules.
- `supersession-graph.json` — claim-level + requirement-level replacement edges.
- `conflicts.jsonl` — contradictions/distinctions with explicit resolution state.
- `validation-report.md` — structural checks.

## Non-negotiable rule
Do not resolve every disagreement with a single linear precedence list.

First determine:
1. domain;
2. scope;
3. question type (normative build vs implementation vs runtime vs deploy vs physical);
4. then apply authority/supersession.

## Core project hierarchy
- DOC-B: System Law.
- DOC-C: current build obligation.
- DOC-D: product design subordinate to B/C.
- DOC-E: deployment proof/approval.
- future Constitutional/Game/Robotics sources: domain authority only in their future scope unless promoted.
- repository/runtime/physical evidence: descriptive truth used to prove compliance; not normative replacement for spec.

## Claim-level supersession
Never say “new document supersedes old document” unless the source actually does so wholesale.
Prefer:
`old claim → SUPERSEDED_BY → new claim`.

This preserves valid unaffected content from older documents.
