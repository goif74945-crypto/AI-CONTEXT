# NEXY Independent Assurance Five-Pack

**Execution ID:** `CHAT-20261005-0153-NEXY-INDEPENDENT-ASSURANCE-FIVEPACK`  
**Status:** AI-proposed concepts with a standalone reference implementation.  
**Not current NEXY law, not integrated NEXY runtime code, not deployment evidence.**

This package explores five orthogonal controls selected after scanning the existing `AI-CONTEXT/คลังข้อมูลเสริม` work for direct conceptual collisions. The goal is to strengthen NEXY-compatible assurance without modifying any repository whose name contains `NEXY.AI`.

## The five mechanisms

1. **IAQ — Independence-Aware Quorum**: prevents correlated agents from manufacturing confidence by counting independent failure domains rather than raw votes.
2. **ECG — Evidence Contamination Guard**: detects circular verification where an oracle is derived from the target, shares an untrusted root, or has cyclic lineage.
3. **RAAS — Risk-Adaptive Assurance Scheduler**: routes actions to stronger evidence/control gates as blast radius, irreversibility and production risk rise.
4. **CTR — Capability Tombstone Registry**: prevents retired capabilities from reappearing through stale caches/snapshots while retaining append-only history.
5. **AIG — Attention Integrity Governor**: suppresses/coalesces repetitive low-value alerts without hiding a materially changed critical state.

## Files

- `TASK_CONTRACT.md` — authority, scope and acceptance contract.
- `DESIGN.md` — architecture, invariants, failure semantics and NEXY compatibility for all five ideas.
- `nexy_assurance_fivepack.py` — standalone Python 3.13 reference implementation.
- `test_nexy_assurance_fivepack.py` — pytest suite covering positive, negative, determinism and cross-system flow.
- `EVIDENCE.md` — TDD/verification record and evidence boundaries.
- `FINAL_TEST.txt` — exact final test output for the persisted bundle.
- `STATIC.txt` — exact static compilation result.
- `00_MISSION_STATE.md` — resumable execution state.
- `FINAL_AUDIT.md` — acceptance audit.
- `MANIFEST.sha256` — SHA-256 manifest for the persisted artifact set (excluding itself).

## Integration boundary

These mechanisms are deliberately implemented as a provider-agnostic standalone package. An actual NEXY integration would require an explicit promotion decision, interface mapping to the exact NEXY implementation HEAD, tests at the required evidence class, and DOC-C/DOC-E compliance. This package makes no claim that those later gates have occurred.

## Latest verified continuation

The AIG reference now treats escalation from any noncritical severity to `CRITICAL` as material before duplicate suppression. A parameterized regression test covers `LOW`, `MEDIUM` and `HIGH` escalation while the existing exact-CRITICAL-duplicate behavior remains covered. The exact standalone bundle passes 35 tests and static compilation in the recorded environment.
