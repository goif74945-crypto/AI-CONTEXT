# 07 — NEXY INTEGRATION MAP

**Important:** integration points below are proposals, not implementation facts.

## Canonical concepts observed in AI-CONTEXT

- CIRL resolves intent and constraints.
- USER LAW preserves user authority.
- NEXY::DIALOG is a conversational/sandbox surface.
- NEXY::GUARD is a protective interaction layer.
- NEXY::VIEW renders trusted results.
- freeze is a first-class control state.
- UI must not redefine core authority.
- complexity should remain behind a small user-facing surface.

## Proposed placement

```text
User / DIALOG input
        ↓
[HICF: continuity + clarification control]   (AI-PROPOSED)
        ↓
CIRL / intent-resolution path
        ↓
LAW / CORE / downstream canonical control layers
```

HICF should not adjudicate policy beyond its own interaction contract. A future implementation could supply:

- canonicalized intent state to CIRL;
- clarification reason codes to DIALOG;
- continuity fingerprint to Vault/task checkpoints;
- authority-break events to freeze handling;
- friction metrics to UX telemetry;
- scoped preference candidates to an explicit memory/personalization governance path.

## Compatibility requirements

1. No bypass of User Law.
2. No bypass of safety/freeze requirements.
3. No UI-owned policy mutation.
4. No provider/model-specific semantics in the user contract.
5. No durable memory write without the project’s required authority/provenance path.
6. Deterministic gate result for equivalent canonical input.
7. Existing CIRL remains authoritative unless a future canonical spec explicitly changes it.
