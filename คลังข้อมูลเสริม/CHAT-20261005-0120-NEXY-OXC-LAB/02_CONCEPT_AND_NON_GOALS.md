# OXC Concept and Non-Goals

Classification: **EXPERIMENTAL / AI-PROPOSED**

## Source-grounded motivation

Relevant NEXY context inspected before design:

- `projects/NEXY.AI/requirements.md`
- `projects/NEXY.AI/deep/human-control-surface.md`
- `projects/NEXY.AI/deep/doc-d-product-design.md`
- `projects/NEXY.AI/status.md`
- `projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`
- global AI-CONTEXT execution/security/verification/memory rules

Observed design constraints include:

- human-facing adaptation belongs to presentation and cannot alter Core truth/authority;
- UI must reflect real state;
- frozen state must look frozen;
- visible does not imply editable or executable;
- dangerous operations require explicit controlled paths;
- product UX should be minimal, information-dense without confusion, and hide deep complexity until needed;
- NEXY is a control environment rather than a generic chat transcript manager.

## Proposed product hypothesis

A deterministic compiler between authoritative state and UI rendering can make strict control semantics easier to use while reducing the chance that UX code accidentally invents authority.

Conceptual flow:

```text
AUTHORITATIVE CORE SNAPSHOT
        +
PRESENTATION-ONLY PREFERENCES
        ↓
CONTRACT VALIDATION
        ↓
AUTHORITY NARROWING
        ↓
TRUTH SIGNAL COMPILATION
        ↓
RISK / FRICTION COMPILATION
        ↓
PROGRESSIVE DISCLOSURE
        ↓
SURFACE PLAN
        ↓
UI RENDERER
```

OXC output is not a command and not an authorization token. It is a deterministic rendering contract.

## Intended benefits

- lower cognitive load for ordinary operators;
- fewer UI paths that silently diverge from backend truth;
- explicit blocked/disabled reasons;
- safer irreversible/dangerous-action UX;
- easier testability of “preference cannot change authority”;
- model/provider independence because the compiler is ordinary deterministic code;
- clean path for multilingual/style adaptation without teaching presentation code to infer permissions.

## Non-goals

OXC does **not**:

- decide whether an action is legally authorized in the backend;
- override LAW/CORE/JUDGE;
- change release thresholds;
- infer missing user intent;
- infer emotional state;
- use mood to change truth;
- profile the user persistently;
- select external AI providers;
- execute tools;
- own durable project state;
- become a hidden retry/fallback system;
- replace backend permission checks;
- claim production readiness.

## Promotion boundary

This proposal should remain EXPERIMENTAL until NEXY project authority explicitly promotes it and integration tests prove that a real UI/backend boundary preserves the same invariants.

Repeated discussion, popularity or model confidence is not promotion evidence.
