# NEXY Lo4 Reality Five

**Classification:** `Lo4_AI_PROPOSAL_ONLY` / experimental / not Canon / not deployed.

Execution code: `CHAT-20261005-0224-NEXY-LO4-REALITY-FIVE`

This lab explores five underrepresented real-world integration problems around NEXY: operator attention, data-placement constraints, accessibility-preserving representations, human interruption policy, and finite verification compute. It deliberately does not duplicate the adjacent 02:21 Lo4 proposals (CAWT, EDEL, CCF, SIMF, DRCDO).

## Why this set is different

Most adjacent supplemental work is assurance-centric. This set targets the boundary where a verified AI control system meets actual users, providers, regions, accessibility modes, approvals, and finite compute. The goal is not more internal cleverness for its own sake. The goal is to preserve NEXY principles while reducing avoidable friction and making future integration more operationally realistic.

## Systems

1. **OAC — Operator Attention Compiler**: guarantees safety/blocker/authority/irreversible notices cannot be hidden by an attention budget, then deterministically packs optional information.
2. **JCPP — Jurisdictional Compute Placement Planner**: filters provider/region choices through explicit data-placement contracts before any cost/latency/reliability optimization.
3. **SAEM — Semantic Accessibility Equivalence Mirror**: verifies that accessible/compact/low-bandwidth representations preserve decision-critical semantic atoms.
4. **HIG — Human Intervention Governor**: deterministically decides AUTO_PROCEED vs ASK_USER vs REQUIRE_APPROVAL vs FREEZE from explicit authority, risk, uncertainty, reversibility, and side-effect contracts.
5. **VIBA — Verification Investment Budget Allocator**: funds mandatory evidence first, then computes an exact Pareto frontier over optional verification tiers to maximize stated expected risk reduction within a finite budget.

## Numeric law

All policy scores, normalized metrics, budgets, costs, thresholds, coverage and risk-reduction values in the reference implementation use signed **Q64.64** fixed-point arithmetic backed by a signed 128-bit raw range. The contract path accepts integer/ratio/decimal-string construction and intentionally avoids binary floating-point.

## Fail-closed boundaries

- JCPP returns `FREEZE` when no placement satisfies hard constraints.
- HIG returns `FREEZE` for invalid authority, prohibited actions, or risk at/above the configured freeze threshold.
- SAEM fails when required semantic atoms are missing or changed.
- VIBA returns `FREEZE` if mandatory baseline verification cannot fit the budget.
- OAC never drops mandatory safety/blocker/authority/irreversible notices; if they exceed attention budget it reports `ATTENTION_OVERFLOW` rather than hiding them.

## Verification summary

Local evidence in this bundle:
- Python compile: PASS.
- 28 unit/integration/regression tests: PASS.
- Stress verification: PASS for 20k notices, 10k placements, 50k semantic atoms, and 40 obligations × 6 VIBA tiers.
- reverse-order digest determinism: PASS.
- test suite under four `PYTHONHASHSEED` values: PASS.
- a real VIBA tie-break defect was found by stress testing, fixed, and locked with a regression test before publication.

These results are isolated reference evidence, not production SLA or current NEXY.AI implementation proof.

## Run locally

```bash
python verify.py
python stress_verify.py
```

## Integration boundary

Future integration should be adapter-based. NEXY authoritative policy/config/state supplies contracts and thresholds. These Lo4 systems may propose/compile/verify derived structures but do not become LAW/JUDGE/CORE authority and may not self-promote. Integration must be revalidated against the exact NEXY implementation commit and environment.

## Modular implementation
The executable reference implementation is published as the `reality_five/` package with one module per concept plus `core.py` and `pipeline.py`. `lo4_reality_five.py` is a compatibility facade. Tests are split under `tests/` by subsystem so failures localize cleanly.
