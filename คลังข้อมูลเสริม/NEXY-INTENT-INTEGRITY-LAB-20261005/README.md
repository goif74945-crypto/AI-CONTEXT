# NEXY Intent Integrity & Change Guard Lab

**Status:** AI-PROPOSED CONCEPT / RESEARCH PROTOTYPE / ADVISORY ONLY  
**Authority:** This directory is supplemental research inside `AI-CONTEXT`; it is **not** a current NEXY.AI requirement, implementation claim, or deployment claim.  
**Protected boundary:** No repository whose name contains `NEXY.AI` is modified by this work.

## Why this exists

Long AI workflows can fail without an obvious crash. The system may gradually reinterpret the objective, silently drop a hard requirement, expand scope, weaken evidence, or transform an assumption into an asserted fact. The output can look polished while no longer matching what the human authorized.

This lab explores a deterministic guardrail for that failure class. It treats user intent as a versioned contract with a stable semantic digest, then checks proposed work and contract revisions against explicit scope, mandatory requirements, evidence classes, truth classes, and exact approvals.

The aim is not to replace NEXY::CORE, NEXY::LAW, NEXY::JUDGE, or any current project component. The aim is to provide a future-useful research artifact that could inform an eventual intent-preservation mechanism if the authoritative NEXY specification ever adopts such a design.

## Research hypothesis

A multi-agent control system can reduce silent semantic drift if every execution phase carries a small, canonical intent contract and every mutation must prove one of two conditions:

1. it preserves the contract exactly enough to satisfy deterministic invariants; or
2. it is covered by an explicit, exact authorization for the specific semantic change.

Otherwise the guard returns `FREEZE` rather than trying to infer permission.

## Prototype capabilities

- Canonical JSON normalization with Unicode NFC and deterministic ordering.
- SHA-256 semantic digest for reproducible contract identity.
- Repository-identity allow/protect boundaries plus path enforcement with `in_scope`, `out_of_scope`, and `protected` patterns.
- Mandatory requirement coverage checking.
- Evidence-strength floor per acceptance criterion.
- Truth-class checks that reject obvious assumption-to-fact escalation.
- Detection of `NOT_VERIFIED` completion claims.
- Contract-to-contract drift detection.
- Exact change authorization envelopes rather than blanket approval.
- Deterministic CLI output and standard-library-only Python implementation.
- Unit and invariant tests, including randomized ordering checks.

## Non-goals

This prototype does **not** claim to:

- infer intent from unrestricted natural language;
- prove two arbitrary texts are semantically equivalent;
- enforce policy inside the actual NEXY runtime;
- replace authorization, authentication, or cryptographic identity;
- prove human consent merely because an approval JSON file exists;
- provide production-grade glob isolation or OS sandboxing;
- establish that current NEXY.AI implements any of this.

## Structure

- `docs/01_CONCEPT_SPEC.md` — problem, objectives, invariants, and decisions.
- `docs/02_ARCHITECTURE.md` — proposed data flow and component model.
- `docs/03_FAILURE_SECURITY_MODEL.md` — attack/failure analysis.
- `docs/04_FUTURE_INTEGRATION_IDEAS.md` — strictly non-authoritative integration concepts.
- `schemas/` — machine-readable research schemas.
- `src/nexy_intent_guard/` — deterministic prototype implementation.
- `tests/` — unit/invariant tests and fixtures.
- `00_EXECUTION_STATE.md` — resumable checkpoint for this work.
- `VERIFICATION.md` — executed evidence and limitations.
- `CHAT_PROVENANCE.md` — session provenance and chat-ID status.

## Local verification

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m nexy_intent_guard.cli digest tests/fixtures/base_contract.json
PYTHONPATH=src python -m nexy_intent_guard.cli check-proposal \
  tests/fixtures/base_contract.json \
  tests/fixtures/passing_proposal.json
```

Expected result: the unit suite passes; compileall exits `0`; the passing proposal returns `PASS`.

## Design principle

**Authorization must be narrower than ambiguity.**

When the system cannot prove that a proposed action is inside the user's authorized semantic boundary, the default result is not creative interpretation. It is a visible freeze with evidence explaining why.
