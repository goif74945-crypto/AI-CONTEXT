# Evidence — Kinetic Proof Fabric

Work code: CHAT-20261005-0225-NEXY-LO4-KINETIC-PROOF-FABRIC
Evidence scope: isolated software reference implementation only.

## Development lineage
1. Initial modular implementation compiled and passed 52 tests.
2. Manual architecture audit found a real AEPE defect: braking distance used target speed alone.
3. A regression test reproduced the defect as FAIL.
4. Formula repaired to use max(abs(current_velocity), abs(target_velocity)).
5. Targeted regression passed.
6. Expanded modular property/stress suite reached 62/62 PASS.
7. PSTL was optimized from O(n^2) candidate scanning to O(n log n) weighted endpoint sweep and regression suite remained PASS.
8. A first consolidated publish bundle failed due an import/package-layout regression and was not published as PASS.
9. Packaging was corrected and consolidated bundle passed.
10. Final compact release candidate matching the files intended for durable publication was rerun cleanly.

## Final release-candidate evidence
Static command: PYTHONPATH=src python -m py_compile src/kinetic_proof_fabric.py tests/test_kpf.py
Observed: PASS, exit code 0.

Test command: PYTHONPATH=src python -m unittest discover -s tests -v
Observed: PASS, 44 tests, 0.012 s in local sandbox.
Coverage includes Q64.64 arithmetic/overflow/input rejection, PSTL consensus/freshness/trust/order/stress, WMDS thresholds/missing axes, AEPE limits/braking regression/monotonicity, CHI transactionality, RHPV lease/replay/latch/hash/reset, and six composed pipeline cases.

## Exact local SHA-256 before publication
src/kinetic_proof_fabric.py = 452cd5b48078fa86377526dc2667f193ecd47872712ad8de01c56b36af362029
tests/test_kpf.py = d00ea59483d0fc11d32b7248f1d148d85ae4efd03958061811bcf630ce412d16
test log = 2e97f2def20b80cd9f640138e3c76cdef25af0c18192a57a61dd3b62935a4f72

## Evidence classes
E1 static: PASS locally.
E2 unit/regression/property: PASS locally.
E3 isolated software integration: PASS locally.
E5 target runtime/operational: NOT_VERIFIED.
E6 deployment: NOT_VERIFIED.
E7 physical/HIL: NOT_VERIFIED.

## Not proven
NEXY runtime integration, ROS2/MCU interoperability, target-hardware WCET, sensor accuracy, actuator braking physics, watchdog independence, power/thermal/mechanical behavior, emergency-stop hardware, production deployment, certification, or Canon promotion.
