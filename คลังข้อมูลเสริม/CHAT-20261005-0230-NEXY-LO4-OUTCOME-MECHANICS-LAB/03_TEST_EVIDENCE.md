# Test and Evidence

Environment used for standalone verification:
- Node.js v22.16.0
- TypeScript 5.8.3 available in sandbox
- runtime dependencies: none
- provider/network calls: none

E1 static:
- clean strict TypeScript compile PASS
- exactOptionalPropertyTypes, noUncheckedIndexedAccess, noImplicitOverride, noImplicitReturns enabled
- scan for Math., parseFloat(, Number( under src/: no matches

E2 unit/negative/stress:
- final Node test runner result: 29 tests, 29 pass, 0 fail, 0 skipped, 0 todo
- Q64 decimal parsing/arithmetic/overflow/divide-by-zero/canonical serialization
- one executed behavior test for each of 20 engines
- invalid constraint/completion-domain negative paths
- ranking replay 100 times over 200 candidates
- robust lower-bound selection over 500 candidates
- residual-work evaluation over 1,000 requirements

Local E3 integration:
GoalDistance -> EvidenceValueOfInformation -> OpportunityCost -> CostOfDelay -> ResidualWorkMass -> NexyLo4Envelope
Observed deterministic output; canonical=false; invalid input becomes FREEZE.

Failure/fix:
Initial full run compiled but produced 27/29 pass. Two assertions exposed decimal presentation truncation (0.199999 and 0.099999). Q64.toDecimal was repaired to deterministic half-even rounding, then full clean verification produced 29/29 pass.

Evidence boundary:
This proves the standalone tested bundle only. Exact NEXY TypeScript 6.0.3 integration, runtime, deployment, Canon promotion, and global superiority over every prior design remain NOT_VERIFIED.
