# Failure Witness Distiller — Evidence

**Local status:** PASS

## Executed proof

- E2: `failure_witness_distiller.test_engine` — 4 focused unit/negative tests.
- E2 adversarial: exact failure signature is preserved rather than merely a boolean failure state.
- E3 lab integration: BPPL strict parse → FWD reduction → BPPL canonical serialization/reparse.
- Determinism replay: full 33-test suite passed with `PYTHONHASHSEED=1` and `777`; result bodies were byte-identical.

## Claims proven

The executed tests establish source-failure precondition enforcement, deterministic reduction on the fixtures, exact signature preservation, smaller witness production on the representative case, and unstable-oracle detection.

## Evidence boundary

These results prove the standalone reference implementation in this lab at E1/E2 and the stated lab-level E3 interactions. They do **not** prove integration into NEXY.AI, production performance, deployment readiness, or authority promotion.
