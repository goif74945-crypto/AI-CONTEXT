# OXC Integration Guide

Classification: **EXPERIMENTAL / AI-PROPOSED / NOT IMPLEMENTED IN NEXY**

This file describes a possible future integration path only.

## Proposed placement

```text
NEXY authoritative state / permission service
              ↓
      sanitized CoreSnapshot
              ↓
        OXC compiler
              ↓
         SurfacePlan
              ↓
     web/mobile renderer
              ↓
 user requests an action
              ↓
  SERVER RE-AUTHORIZATION
              ↓
 Core execution / rejection
```

Critical invariant: the server re-authorizes. OXC never substitutes for backend policy.

## Suggested adoption phases

### Phase 0 — contract-only experiment

- keep OXC outside NEXY source;
- review input/output schema against current DOC-C/D authority;
- resolve role mismatch such as current backend SYSTEM role versus reference VIEWER;
- decide whether action-risk metadata is canonical or merely UI hint.

### Phase 1 — shadow compilation

- run OXC beside existing UI policy;
- do not control rendering;
- compare OXC plan against actual UI;
- collect mismatches;
- no production authority change.

### Phase 2 — read-only surfaces

Use OXC only for:
- status/truth banner;
- diagnostic disclosure;
- read/inspect actions.

Backend behavior unchanged.

### Phase 3 — controlled action surfaces

Only after E3/E4 tests:
- render disabled/hidden/enabled states from plan;
- keep backend re-authorization;
- test race/freeze/version changes between render and click.

### Phase 4 — preference envelope

Enable explicit presentation preferences after proving:
- authorization projection remains invariant;
- no security-critical content can be hidden;
- browser/local persistence obeys privacy law.

## Required contract additions before serious integration

Reference v1 intentionally omits fields that a production design likely needs:

- snapshot version / state revision;
- project/tenant scope;
- action version;
- authorization decision id or provenance reference;
- reason codes owned by backend;
- localization message key rather than free-form authoritative label;
- expiry/freshness policy;
- optional accessibility requirements.

These omissions are deliberate because current evidence does not authorize inventing exact NEXY schemas.

## Compatibility notes

- DOC-D records OWNER/OPERATOR/AUDITOR/SYSTEM, while this reference uses VIEWER as a human-facing read-only role. This mismatch must be resolved by current project authority before integration.
- Reference friction mapping is a proposal, not current NEXY law.
- Current project release status remains BLOCKED/NOT VERIFIED in AI-CONTEXT and is unrelated to this experiment.

## Rollback

Because OXC should be a presentation compiler, adoption should retain a feature-gated path back to the current renderer policy during experimentation.

Rollback must never bypass backend enforcement.

## Acceptance evidence for promotion

Minimum suggested classes:

- E1: type/schema/static validation;
- E2: policy unit/metamorphic tests;
- E3: integration against real permission/state APIs;
- E4: browser flows covering FREEZE, role denial, dangerous action confirmation and preference invariance;
- security abuse tests for stale/tampered plans.

No production-ready claim before those are current-revision evidence.
