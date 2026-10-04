# Proposed NEXY Integration Boundary

**STATUS: AI_PROPOSAL_ONLY — NOT AUTHORIZED FOR NEXY.AI IMPLEMENTATION**

## Goal

Allow NEXY operators/auditors to reduce a failing trace into a compact reproducer without giving the minimizer any authority over canonical NEXY state.

## Proposed data flow

```text
NEXY OBS / incident export
       |
       | sanitized, read-only trace artifact
       v
NFWM external process
       |
       +--> analysis.json
       +--> witness.json
       +--> witness verification result
       |
       v
human/auditor review
       |
       +--> optional regression fixture in an authorized future workflow
```

## Required integration locks before any future adoption

1. NEXY exports data; NFWM receives no credentials capable of mutation.
2. Export schema/version is explicit and runtime-validated.
3. Source commit/build/environment identifiers accompany the trace.
4. Witness import, if ever allowed, is treated as untrusted evidence input.
5. NFWM PASS never means NEXY deployment PASS.
6. Failure witnesses cannot trigger automatic production mutation.
7. Sensitive log fields must be redacted by an authorized policy before external export.
8. Integration must receive its own E3/E4-level verification where relevant.

## Compatibility mapping

| NEXY context concept | NFWM use |
|---|---|
| System state FSM | profile transition set |
| FREEZE blocks release | release-after-freeze invariant |
| Freeze incident linkage | incident-id invariant |
| idempotency | duplicate-run invariant |
| trace/request IDs | witness correlation fields |
| evidence discipline | canonical witness + replay verifier |
| no hidden repair | NFWM reports/minimizes; never patches input |

## Non-goals

- no automatic incident recovery;
- no quorum/judge replacement;
- no LAW enforcement replacement;
- no Vault mutation;
- no auth/session handling;
- no production deployment decision.
