# Validation Report — NCMDE Durable Core

Status: PASS
Evidence scope: E0/E1/E2 standalone reference prototype only.
Date: 2026-10-05

## Exact repository identity
Mission branch: chat-20261005-0122-ncmde
Hardened implementation commit before evidence-record update: 60daf248e443075dd6abc774c46b8d5a4dc46693

Verified Git blobs:
- src/ncmde.py = 5407ddcd505469cc34b1736db544413d2c14cc5e
- tests/test_ncmde.py = d2dca11b507391f377be1cba17b440f2725f6275
- fixtures/scenarios.json = 10b21eb2dd40e5f72d6ab9dc732a3fceb59902c3
- schema/mission.schema.json = 06aa7d26f4ba8ed2c55dab324b1b9b8a5578a9c3

The verifier reconstructed Git object SHA-1 for each local execution input using the exact Git blob framing. Result: 4/4 MATCH.

## Static evidence
- python3 -m py_compile src/ncmde.py tests/test_ncmde.py => PASS
- JSON parse for fixture corpus => PASS
- JSON parse for mission schema => PASS
- jsonschema Draft202012Validator + FormatChecker => PASS for 7 mission objects
- jsonschema package observed in verifier environment: 4.26.0

## Unit / behavior evidence
Command:
python3 -m unittest discover -s tests -v

Observed:
Ran 26 tests
OK

Covered paths include:
- exact FILE and TREE write collisions
- protected scope collision
- exclusive resource and authority collision
- PROCEED / COEXIST / DECONFLICT / FREEZE
- expired and completed incumbent handling
- missing domain rejection
- glob and parent traversal rejection
- timezone requirement
- maximum lease policy
- registry/set ordering determinism
- equivalent timezone determinism
- policy-bound hash changes
- mission ID collision
- duplicate registry mission ID rejection
- Unicode controlled-tag normalization
- fixture replay

## Supplemental stress evidence
An external verifier imported the exact committed source blob and executed 1,003 deterministic property checks:
- 500 deterministic disjoint mission pairs => stable identical PROCEED results
- 500 nested TREE write claims => FREEZE with WRITE_SCOPE_COLLISION
- 3 registry-order permutation checks => identical result and decision hash

Result: PASS 1,003 / 1,003.

## Real concurrency-pattern fixture
The fixture modeled the declared metadata pattern observed between two concurrent privacy/context firewall directions:
- decision: DECONFLICT
- overlap: 8961 / 10000
- decision hash: 3fa10df466cf4aa551feeea79325c319b9c08d98963cbe0c3da5c5c71035f899

This is a synthetic normalized fixture informed by the observed sibling mission descriptions. It is not a claim about hidden intent.

## Negative execution history
- Initial local expanded prototype exposed one incorrect moderate-overlap fixture expectation; fixture was corrected instead of weakening the policy threshold.
- Initial durable exact test run passed 25/25 but emitted a ResourceWarning from an unclosed fixture file; test hygiene was corrected.
- Duplicate incumbent mission IDs were identified as an additional registry-integrity invariant and implemented fail-closed.
- Two direct non-force attempts to update main were rejected as non-fast-forward because main moved concurrently. No force update was used.

## Evidence boundary
No E3 integration, E4 end-to-end, E5 operational, E6 deployment, or E7 physical claim is made.