# Failure Witness Distiller (FWD) — Design

Status: **AI-PROPOSED / EXPERIMENTAL / NON-CANONICAL**

## Objective
Reduce a JSON-like failing input to a smaller reproducible witness while preserving the **exact same failure signature**. The intended use is debugging deterministic FREEZE/deny/error behavior without handing future engineers a huge request whose relevant cause is buried in noise.

## Authority and scope
FWD is advisory infrastructure outside the NEXY authority-bearing core. It may explain or minimize a failure already produced by an authoritative oracle. It MUST NOT decide whether an action is authorized, change the signature, or turn a failure into a release.

## Inputs and outputs
Input: JSON-like Python value plus an oracle `value -> failure signature | None`.
Output: `DistillationResult` containing the original signature, minimized witness, ordered reduction steps, and before/after node counts.

## Invariants
1. The source MUST already fail; otherwise FWD rejects the request.
2. Every accepted reduction MUST reproduce the exact original signature.
3. Candidate ordering is deterministic.
4. Final witness is rechecked to detect unstable/stateful oracles.
5. A result is a locally minimized witness, not a theorem of global minimality.

## Algorithm
FWD walks mappings in sorted-key order and lists by index. It repeatedly proposes strictly simpler neighbors by deleting container members or simplifying primitive values. The first candidate that preserves the exact signature is accepted, then the search restarts. Termination is bounded by `max_steps`.

This greedy strategy intentionally prefers reproducibility and auditability over globally optimal delta debugging. A future implementation may add hierarchical ddmin or parallel partitions, but only if deterministic tie-breaking remains explicit.

## Failure model
- Non-failing source: `ValueError`.
- Oracle instability detected on final re-check: `RuntimeError`.
- Step budget exhausted: `RuntimeError`.
- Oracle exception: propagated, because hiding an oracle failure would invent evidence.

## NEXY integration proposal
A future adapter could consume a frozen request/evidence capsule, call the existing authoritative verifier as the oracle, and emit a diagnostic witness linked to the original proof identity. The witness must remain **diagnostic only** and cannot inherit authorization from the source object.

## Evidence plan
E2 unit tests cover deterministic minimization, signature preservation, non-failing input rejection, and unstable-oracle detection. E3 lab integration verifies a strict boundary payload can be minimized and then round-trip through canonical serialization.

## Known limitations
- Greedy local minimum only.
- Assumes a deterministic and side-effect-free oracle for meaningful output.
- JSON-like structures only in this reference prototype.
- Runtime cost can be high when oracle evaluation is expensive.
