# Design

## Authority model
1. Current user directive: create useful NEXY-compatible work in AI-CONTEXT only; never write NEXY.AI.
2. AI-CONTEXT execution kernel/rules.
3. NEXY DOC-B identity/law and DOC-C vNEXT build spec.
4. This lab's proposal rules, clearly labeled `PROPOSED_GUARD`.

## Architecture

```text
candidate manifest
      |
      v
+-------------------+
| deterministic     |
| static validator  |
+-------------------+
      | PASS
      v
+-------------------+
| failure-semantics |
| replay simulator  |
+-------------------+
      |
      v
canonical report + digests
```

## Invariants
- Adapter is a worker, never NEXY authority.
- No direct release.
- No direct SWARM/adapter -> VAULT mutation.
- No automatic retry by default.
- Unknown quorum state never becomes optimistic continuation.
- Valid result continues to cross-verification; it never becomes direct release.
- Reports are deterministic for semantically identical JSON key ordering.
- The tool has zero third-party runtime dependencies.

## Failure semantics implemented
| Event | Condition | Lab action | Basis |
|---|---|---|---|
| valid result | manifest PASS | CONTINUE_TO_CROSS_VERIFY | DOC-C locked pipeline |
| invalid result schema | any valid adapter | FREEZE | AGENT_SCHEMA_INVALID + error->FREEZE |
| timeout | critical | FREEZE | critical timeout freezes |
| timeout | noncritical, quorum survives | EXCLUDE_AGENT_AND_CONTINUE | DOC-C noncritical timeout rule |
| timeout | noncritical, quorum fails | FREEZE | quorum/release cannot pass |
| timeout | noncritical, quorum unknown | FREEZE | zero-guess rule |
| provider failure | valid adapter | FREEZE | DEPENDENCY_FAILURE + error->FREEZE |

## Security boundary
The lab never needs provider secrets. Its manifest contains only a declaration that secrets are runtime injected and not persisted. Real secret-handling claims require runtime evidence elsewhere.

## Determinism
Canonical JSON uses sorted keys, UTF-8, fixed separators and SHA-256. Issue ordering is stable by `(code, path, message)`.
