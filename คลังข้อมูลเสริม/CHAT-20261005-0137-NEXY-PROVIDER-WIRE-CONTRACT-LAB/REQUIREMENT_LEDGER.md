# Requirement Ledger

| ID | Requirement | Authority | Implementation | Evidence | Status |
|---|---|---|---|---|---|
| PW-001 | Standalone, no NEXY.AI mutation | User directive | repository placement | final path audit | PASS |
| PW-002 | Deterministic canonical serialization | lab design | `codec.py` | unit tests | PASS |
| PW-003 | Fail closed on invalid sequence/state | NEXY principle + lab design | `state.py`, `boundary.py` | negative tests | PASS |
| PW-004 | Deterministic transcript fingerprint | lab design | `model.py`, `replay.py` | replay test | PASS |
| PW-005 | Tool-call JSON validation | lab design | `state.py` | negative/unit tests | PASS |
| PW-006 | Direction integrity | lab design | `state.py` | negative tests | PASS |
| PW-007 | Refusal/error terminal semantics | lab design | `state.py` | negative tests | PASS |
| PW-008 | Fuzz-like adversarial sequence coverage | user asks repeated test/fix | tests | deterministic randomized tests | PASS |
| PW-009 | Integration guidance without vendor claims | user constraint | `DESIGN.md`, `INTEGRATION_GUIDE.md` | content read-back | PASS |
| PW-010 | Resumable durable context | AI-CONTEXT kernel | `MEMORY_CHECKPOINT.md` | content read-back | PASS |
