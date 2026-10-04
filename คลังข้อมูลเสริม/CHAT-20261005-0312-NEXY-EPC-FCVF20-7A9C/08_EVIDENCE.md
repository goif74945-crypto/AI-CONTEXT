# FCVF-20 Verification Evidence

## Evidence boundary

This record proves the standalone FCVF-20 reference package on the exact local bytes represented by `MANIFEST.sha256` after publication. It does **not** prove that NEXY currently imports, deploys, or executes FCVF.

## E1 — Static verification: PASS

Environment: Python 3.13.5. `python -m compileall -q src tests` completed with exit code 0. An AST scan across every production module in `src/epc_fcvf` found **0 binary-float literals**. Captured outputs: `evidence/compileall.txt` and `evidence/float_scan.txt`.

## E2 — Unit / negative / property verification: PASS

`python -m unittest discover -s tests -v` executed **38 tests**, all PASS. The suite covers checked Q64.64 arithmetic, overflow/division-by-zero, float rejection, vote field materialization, KEEP/CUT lifetime rights, DEFER rights preservation, WIP/insufficient CUT rejection, missing critical evidence, immutable verdict history, append-only revisions, semantic duplicate witnesses, deterministic permutation equivalence, non-destructive CUT receipts, evidence monotonicity, authority non-interference, weak-rule detection, exact 20-system registry cardinality, and canonical serialization.

Captured output: `evidence/unittest.txt`.

## E3 — Modeled integration / exhaustive verification: PASS in bounded modeled scope

The depth-6 exhaustive run used a deterministic alphabet containing three status transitions, four critical evidence attachments, two KEEP attempts, two CUT attempts, DEFER, promotion attack, Core mutation attack, and Canon override attack.

Observed depth-6 report:
- unique reachable canonical states: **222**
- transitions examined: **2,430**
- accepted transitions: **1,306**
- blocked transitions: **1,124**
- unsafe states: **0**
- stable state-set digest: `1ffd8836145d15612222b80f9aaec95ac79dce8acce2374a2d4b00ef24dc64f8`

A separate depth-5 run executed twice and produced identical reports/digests. This verifies deterministic exploration for the tested model.

## Constitutional regression proof: PASS

A deliberately weakened constitution with `max_keep=2` produced a real unsafe state. The regression differential found a counterexample and the reducer shrank it to a 6-event 1-minimal trace. The independent invariant layer reported `LVBA` and `PWCV` failures. This demonstrates that the checker is capable of failing on the defect it claims to guard rather than simply mirroring the transition code.

Separate weak models that permit auto-promotion, external Core mutation, or Canon override are accepted only by the intentionally weakened transition configuration and then rejected by independent constitutional checkers (`PNCG`, `ANIC`, `CNOP`, and/or `PWCV`). Evidence: `evidence/constitutional_attack_matrix.json`.

## End-to-end reference flow: PASS

`python -m epc_fcvf.cli` executed evidence attachment -> READY -> KEEP -> all-20-system evaluation. Result:
- accepted = true
- findings_pass = true
- systems = 20
- vote_count = 1
- Q64.64 evidence coverage raw = `18446744073709551616` (1.0)
- canonical state hash = `04a12d6a8d0a3f9ac251e0d5b3fd1782debf50312cf9b3b271ffcbc459b1a4f5`

Captured output: `evidence/cli.json`.

## Spec/code grounding

The authoritative source bytes were materialized from connected Google Drive and independently identified as Microsoft Word OOXML. SHA-256 exactly matched AI-CONTEXT's canonical source identity: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.

Relevant source evidence includes the constitutional authority split stating that AGENT proposes, SWARM debates, VERIFY validates evidence, CORE decides, and the Human/auxiliary layer cannot modify Core state, influence decisions, bypass verification, or escalate privilege. The source also specifies Q64.64/fixed128 authoritative math.

Read-only NEXY implementation evidence at `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43` confirms current ownership separation and Q64.64 implementation constraints, including `packages/core/vnext-state-matrix.ts`, `packages/intelligence/trinity.ts`, `packages/phase-f/sovereign/canon-seal.ts`, and `core-kernel/src/engine/fixed128_math.rs`.

## Claim limits

PASS applies to the standalone protocol verifier and bounded model described above. NEXY runtime integration, production behavior, distributed concurrency, database durability, deployment and physical-world behavior are **NOT_VERIFIED** by this package.
