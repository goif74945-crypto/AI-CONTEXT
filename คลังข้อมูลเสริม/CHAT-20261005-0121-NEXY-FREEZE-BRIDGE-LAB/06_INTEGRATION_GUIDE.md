> **HISTORICAL / SUPERSEDED v1.0**
>
> This file records the initial design before the concurrent `NEXY Trust UX Contract Lab` was discovered. Its UI/action-oriented portions are **not current**. The current Freeze Bridge contract is v1.1 and is defined by `README.md`, `10_V1_1_PIVOT_AND_SIBLING_BOUNDARY.md`, and `11_PROTOCOL_V1_1.md`. Historical text is retained for provenance only.

# Future Integration Guide

Classification: **AI-PROPOSED INTEGRATION DESIGN — NOT CURRENT BUILD INSTRUCTION**

## Intended consumer surfaces

A future production equivalent could feed:
- NEXY::PULSE for status/recovery cards;
- NEXY::VIEW for read-only result/freeze explanation;
- NEXY::FRONT for directive correction;
- architect/debug surfaces for evidence links where disclosure allows.

It should **not** sit upstream of Core/Judge authority.

## Recommended boundary

```text
Authoritative subsystem
  produces:
    FreezeEvent
  with:
    already-decided status/reason/actions/disclosure
        |
        v
Freeze Bridge
        |
        v
RecoveryCard DTO
        |
        +--> API serializer
        +--> web card
        +--> terminal/operator UI
        +--> localized text renderer
```

## Required upstream guarantees

Before a real bridge can be trusted:
1. reason code must come from an authoritative source, not from UI inference;
2. authorized_actions must be computed by backend authority;
3. disclosure must be bound to actual ACL/security policy;
4. evidence refs must be opaque and access-controlled at dereference time;
5. event_id must support traceability without exposing secrets.

## Required downstream guarantees

Presentation must:
- display real status, not a fake success/loading state;
- not create buttons for action codes absent from Recovery Card;
- re-authorize action execution server-side even if a button is visible;
- never treat `retryable` as permission by itself;
- preserve event/fingerprint in telemetry if allowed;
- render missing-field identifiers without secret values.

## Suggested API boundary

Conceptual only:

```text
POST /internal/freeze-bridge/compile
Content-Type: application/json

FreezeEvent -> RecoveryCard
```

A production system may instead compile in-process. Network separation is not required by the concept.

## UI pattern

A recovery card should ideally show:
- state badge;
- short title;
- one-sentence reason summary;
- owner/blocked layer;
- exact missing field identifiers when appropriate;
- only legal next actions;
- optional evidence link when disclosure permits.

Avoid:
- generic "Something went wrong";
- fake "Retry" on non-retryable states;
- long internal trace dumps;
- multiple speculative causes;
- therapist-style reassurance;
- UI controls that backend will inevitably reject.

## Telemetry proposal

If later adopted, useful counters may include:
- freeze_reason_total{reason_code};
- recovery_action_rendered_total{action_code};
- recovery_action_selected_total{action_code};
- unknown_reason_total;
- restricted_evidence_suppressed_total;
- invalid_bridge_event_total;
- user_recovery_success_total by reason.

Telemetry must not include secret raw inputs.

## Integration verification ladder

### E1
- type/schema validation;
- contract compile;
- no unauthorized action in static fixtures.

### E2
- reason/action policy tests;
- disclosure tests;
- localization snapshot/semantic tests;
- deterministic fingerprint tests.

### E3
- authoritative producer → bridge → API DTO integration;
- ACL-aware evidence reference behavior;
- backend action re-authorization.

### E4
- user sees frozen UI as frozen;
- buttons match authorized card;
- missing-input correction flow works;
- non-retryable event exposes no retry path.

### E5
- fault injection;
- policy-version mismatch;
- event flood/load behavior;
- telemetry/privacy validation.

### E6
- exact deployed build;
- smoke + rollback;
- current policy/version evidence.

No later evidence class is claimed by this lab.
