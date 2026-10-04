> **HISTORICAL / SUPERSEDED v1.0**
>
> This file records the initial design before the concurrent `NEXY Trust UX Contract Lab` was discovered. Its UI/action-oriented portions are **not current**. The current Freeze Bridge contract is v1.1 and is defined by `README.md`, `10_V1_1_PIVOT_AND_SIBLING_BOUNDARY.md`, and `11_PROTOCOL_V1_1.md`. Historical text is retained for provenance only.

# Security / Misuse Threat Model

Classification: **AI-PROPOSED THREAT MODEL**

## Assets

The bridge may handle:
- event identity;
- status/reason category;
- blocking-layer label;
- missing-field names;
- evidence references;
- action authorization set;
- recovery ownership metadata.

The bridge must not require secret values.

## Trust boundaries

```text
Upstream authoritative runtime
      |
      | structured event (untrusted until validated)
      v
Freeze Bridge
      |
      | filtered recovery card
      v
Presentation / user surface
```

Even though the event comes from an upstream system, the bridge validates its shape. Repository rules explicitly treat external/model/generated content as untrusted unless authority promotes it.

## Threats and controls

### T1 — Action injection
**Threat:** attacker inserts a visually convincing but unauthorized action.

**Control:**
- actions must be known enum values;
- output = upstream authorized set ∩ reason policy set;
- unknown action values reject the event;
- no FORCE/BYPASS action exists.

### T2 — Markup/prompt injection in free text
**Threat:** context label or other free text manipulates downstream UI/model behavior.

**Control:**
- context_label is validated but intentionally not reflected into Recovery Card output;
- protocol favors identifiers/enums over arbitrary prose;
- control characters rejected.

### T3 — Evidence reference leakage
**Threat:** security freeze exposes sensitive incident/path references.

**Control:**
- explicit disclosure class;
- RESTRICTED filtering;
- RESTRICTED + SECURITY_INTEGRITY suppresses all references.

### T4 — False retry
**Threat:** bridge tells user to retry a freeze class that must remain contained.

**Control:**
- force_non_retryable policy;
- retry requires both policy permission and effective RETRY_AFTER_DEPENDENCY authorization.

### T5 — Cause invention
**Threat:** new/unknown reason gets mapped to a plausible but wrong known reason.

**Control:**
- UNKNOWN_REASON fallback;
- generic wording;
- no cause inference.

### T6 — Localization authority drift
**Threat:** Thai and English copy imply different legal capabilities.

**Control:**
- machine action codes and policy are shared;
- localization changes labels only;
- translation cannot expand action set.

### T7 — Fingerprint confusion
**Threat:** output fingerprint is treated as cryptographic authorization.

**Control:**
- docs explicitly state fingerprint is not a signature;
- fingerprint is only deterministic content identity.

### T8 — Denial by oversized payload
**Threat:** huge lists/strings cause expensive processing.

**Control:**
- hard length/item bounds;
- linear bounded processing;
- no recursion;
- no network.

### T9 — State mutation through bridge
**Threat:** presentation layer becomes a hidden mutator.

**Control:**
- stateless reference design;
- no persistence;
- no callback/network/action execution;
- output only contains action descriptors.

### T10 — Stale policy
**Threat:** production system changes reason/auth semantics while bridge policy remains old.

**Control:**
- protocol and policy versions;
- adoption requires exact-version integration evidence;
- unknown reason fails safe.

## Security non-claims

This lab has **not** proven:
- production auth isolation;
- browser/UI XSS safety;
- server/API authorization;
- real incident ACL behavior;
- sandbox containment;
- deployment security.

Those require E3–E6 evidence in the actual target architecture.

## Data minimization rule

Prefer:
- field identifiers, not field values;
- opaque evidence references, not raw logs;
- machine codes, not arbitrary prose;
- smallest action set required.

Never place credentials, private keys, API tokens, passwords or recovery secrets into freeze events.
