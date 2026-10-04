# NEXY Side-Effect Transaction Lab

**Status:** `PROPOSAL_BY_AI` / standalone reference implementation  
**Authority:** advisory only; this folder is not canonical NEXY.AI law  
**Storage target:** `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-SIDE-EFFECT-TRANSACTION-LAB`  
**Protected scope:** repositories whose names contain `NEXY.AI` are read-only for this task.

## Why this exists

The observed NEXY.AI code already models side-effect classes, deterministic ordering, idempotency, explicit FREEZE behavior, and protected mutation boundaries. A useful complementary layer is a **whole-plan transaction firewall** that reasons about multiple proposed actions *before* any side effect is committed.

This lab implements that layer without importing or modifying NEXY.AI. It compiles a set of candidate actions into one deterministic plan, proves whether the actions may coexist, checks preconditions immediately before commit, and produces a deterministic compensation order after partial failure.

The intended future value is simple: instead of asking "is each tool call individually legal?", ask the stronger question **"is the complete side-effect plan jointly legal, non-conflicting, precondition-valid, and recoverable?"**

## Core model

```text
candidate actions
      |
      v
policy + structural validation
      |
      v
resource read/write/call effect graph
      |
      +---- conflict / protected scope / missing proof ----> FREEZE
      |
      v
deterministic dependency DAG + execution waves
      |
      v
sealed planHash
      |
      v
read-only preflight observations
      |
      +---- stale/missing/unexpected evidence -------------> FREEZE
      |
      v
COMMIT_READY seal
      |
      v
external executor (NOT implemented here)
      |
  success / partial failure
      |              |
      v              v
   COMPLETE    deterministic compensation plan
```

## Implemented capabilities

- Canonical, domain-separated SHA-256 identity for policies, plans, freeze reasons, and preflight seals.
- Policy sealing so a caller cannot change policy material while retaining the same `policyHash`.
- Deterministic action normalization independent of caller array order.
- Dependency-cycle and unknown-dependency detection.
- Deterministic topological ordering and parallel execution waves.
- Resource conflict detection for unordered operations where either side is side-effecting.
- Explicit side-effect declaration semantics compatible with the observed NEXY `SideEffectClass` names.
- Protected-resource prefix and fragment rules. The default proposal blocks resource IDs containing `/NEXY.AI` and prefixes beginning `repo:NEXY.AI`.
- Per-mutated-resource precondition requirement.
- Exact preflight observation matching with missing, duplicate, unexpected, stale, and hash-mismatch rejection.
- Idempotency requirements for filesystem, network, database, process, and device effect classes.
- Explicit reversibility classes and exact rollback coverage.
- Irreversible actions disabled by default and separately approval-gated when a policy permits them.
- Plan-integrity revalidation before preflight sealing and compensation generation.
- Reverse-topological compensation ordering after partial execution.
- Fail-closed compensation when an irreversible completed action prevents honest rollback.
- Deep-frozen compiled artifacts to reduce accidental in-process mutation.
- Structural NEXY side-effect adapter with **no import from the protected NEXY repository**.
- 47 executable tests, including exhaustive 120-permutation determinism for five independent actions and the 256-action policy boundary.

## Important semantic rule

`AccessMode` values `WRITE`, `CREATE`, `DELETE`, `APPEND`, `EXECUTE`, and `CALL` are treated as side-effecting for planning. A remote GET or other externally observable operation should therefore be represented as `CALL`, not as local `READ`, if it crosses an external boundary. This avoids hiding a network/process/device interaction inside a read-only label.

## What this does not do

This package deliberately does **not** execute tools, call external services, mutate files, acquire distributed locks, perform database transactions, validate real NEXY authority signatures, or deploy anything. It creates and verifies transaction plans. Integration and execution remain separate authority boundaries.

It also does not claim that NEXY.AI currently lacks an equivalent mechanism everywhere. The duplicate search only establishes that the searched AI-CONTEXT terms did not reveal a direct standalone match and that the specific NEXY files inspected expose compatible primitives rather than this exact lab implementation.

## Tested source preservation

The exact tested source package is preserved in:

- `source/SOURCE_ARCHIVE.part00.b64`
- `source/SOURCE_ARCHIVE.part01.b64`

Decoded archive SHA-256:

`24749323ac0e6518f00c6071ec1a93a9fd8ab5c4a07d0d365789e927b5fdddf9`

See `RESTORE_SOURCE.md`. The archive was independently reconstructed in a clean temporary directory and `npm run verify` passed 47/47 after restoration.

## Evidence preservation

Raw verification artifacts are preserved in `evidence/EVIDENCE_ARCHIVE.b64`.

Decoded evidence archive SHA-256:

`a0374e2dee6063bfb19291bf9bc87bd3b688ac09ba04edbba8a82d2105faf52a`

See `EVIDENCE.md` and `RESTORE_EVIDENCE.md`.

## Integration boundary

The proposed integration point is **before any NEXY-controlled side-effect executor**:

1. NEXY or an adapter emits typed candidate actions.
2. The planner compiles them under a sealed transaction policy.
3. `FREEZE` means no side-effect executor may be invoked.
4. For `ALLOW`, a read-only observer supplies current precondition observations.
5. Preflight must return `COMMIT_READY` for the exact `planHash`.
6. A future executor would independently verify the seal and execute deterministic waves.
7. On partial failure, compensation order is generated; compensation itself should be recompiled and preflighted before mutation.

This is a proposal, not a production integration claim.
