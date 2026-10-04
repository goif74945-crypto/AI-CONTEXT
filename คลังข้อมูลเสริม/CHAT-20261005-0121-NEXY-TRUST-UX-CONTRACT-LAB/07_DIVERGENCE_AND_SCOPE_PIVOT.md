# Divergence and Scope Pivot Record

Status: **EXECUTED / PROVENANCE RECORD**

## Trigger

After this lab's initial Trust Card compiler had already been designed, implemented and partially persisted, the repository advanced concurrently and a sibling project appeared at:

`คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-FREEZE-BRIDGE-LAB`

Read-only inspection established material overlap. The sibling project already implements a deterministic presentation/control-boundary compiler from freeze events to human recovery cards, including policy intersection, disclosure handling, retry law, localization, schemas, tests and self-checks.

## Decision

Do **not** claim the initial Trust Card work is a unique contribution.
Do **not** delete or rewrite it, because it is valid provenance and was already persisted additively.
Do **not** modify the sibling project.

Instead pivot this session's primary contribution to a different system boundary:

**Truth Surface Conformance Model Checker**

The new component consumes:

`authoritative backend truth + rendered surface manifest + role`

and emits:

`deterministic conformance report + invariant violations + certificate fingerprint`

It verifies presentation behavior rather than generating recovery guidance.

## Non-overlap boundary

Freeze Bridge:
- generates a safe recovery card from an already-decided freeze event;
- filters actions/evidence;
- localizes recovery guidance.

Truth Surface Checker:
- audits an already-rendered surface;
- detects state/status lies, result leaks, illegal CTA visibility, identity mismatches, missing release proof and semantic success/retry leakage;
- is suitable as a CI/adversarial gate against any renderer, not just a freeze bridge.

## Status of earlier files in this lab

The following remain **AI-PROPOSED exploratory artifacts** and must not be treated as the session's distinct primary deliverable:
- `03_TRUST_UX_CONTRACT.md`
- `04_FREEZE_COMMUNICATION_PROTOCOL.md`
- `05_ACTION_VISIBILITY_AND_AUTHORITY.md`
- `reference_impl/trustux.py`
- `tests/test_trustux.py`

They are retained to preserve execution history and test evidence.

The distinct primary deliverable is now:
- `08_TRUTH_SURFACE_CONFORMANCE_SPEC.md`
- `conformance/truth_surface_checker.py`
- `conformance_tests/test_truth_surface_checker.py`
- `tools/exhaustive_conformance_selfcheck.py`
- `corpus/truth_surface_scenarios.jsonl`
- `invariants/truth-surface-invariants.json`
- `09_ADVERSARIAL_MODEL_CHECK_REPORT.md`

## Authority

This pivot is additive advisory work only. It does not promote either lab into current NEXY build scope.
