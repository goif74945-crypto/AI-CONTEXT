# Build / Promotion Order

**Status:** PROPOSAL — not current NEXY implementation scope.

A safe future adoption order is:

1. **BPPL adapter** at an isolated ingress/preflight boundary, because its contract is narrow and independently testable.
2. **NSCA** in offline CI/reporting mode to expose missing negative-path evidence without changing runtime behavior.
3. **VPO** in recommendation-only mode, comparing its proposed portfolios with existing verification plans before allowing automated scheduling.
4. **CMAE** in isolated verification/eval jobs only, with mutant artifacts forbidden from production state.
5. **FWD** on already-frozen failures, initially as diagnostic evidence generation only.

Each promotion step needs: current authoritative schema mapping, exact-head tests, negative-path tests, regression proof, performance/resource bounds, and explicit authority. A later step must not be used to retroactively justify an earlier unverified integration.
