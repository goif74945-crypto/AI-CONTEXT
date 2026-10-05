# BLOCK-FSM-BOOTSTRAP-AUTHORITY-GAP-001

## Scope
Local block only: final DOC-C FSM error-edge parity + bootstrap dependency-failure handling. Independent missions remain runnable.

## Problem
The final DOC-C matrix after `FINAL VERDICT` explicitly contains `error -> FREEZE` rows for `RUNNING` and `VERIFYING`, while the earlier vNEXT.1 section contains a broader `ANY except STOP + error -> FREEZE` rule. Temporal authority makes the later final matrix the build authority where the two conflict.

At `NEXY.AI-Test-AI@608426cb30398b1f3461866f7079d2a435c96b96`, Rust follows the final matrix but TypeScript still implements the broader historical rule. Bootstrap currently depends on the broader TypeScript `INIT + error -> FREEZE` edge.

## Expected
1. One final-DOC-C transition semantics across TS and Rust.
2. Bootstrap failure remains fail-closed.
3. No unsupported FSM evidence is fabricated.
4. No implicit recovery path is introduced.
5. Exact-SHA executed tests must prove the repair before VERIFIED.

## Actual
- TS: `error -> FREEZE` from INIT/READY/RUNNING/VERIFYING/CONSENSUS/STABLE/FREEZE.
- Rust: `error -> FREEZE` only from RUNNING/VERIFYING.
- Bootstrap: on tick/dependency failure, calls `transitionSystemState("error","CORE", ...)` while state can be INIT.
- Current Test-AI SHA has no associated workflow run, so there is no fresh execution oracle.

## Primary evidence
- Spec SHA: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- FINAL VERDICT: non-empty paragraphs 8297-8305.
- Final DOC-C executable matrix: paragraphs 8811-8910.
- Final log/incident law: paragraphs 8952-8957.
- Superseded conflicting vNEXT.1 transition table: paragraphs 7447-7504.

## Attempts / history inspected
1. Confirmed current TS/Rust parity split at exact integration SHA.
2. Traced prior repair chain:
   - `67252bb...`: process-local `quarantineSystemStateForBootstrapFailure()`.
   - `533748e...`: bootstrap switched from CORE error transition to quarantine.
   - `f105f226...`, `9ebc954...`, `fffa702...`, `cae6a99...`: coverage wiring.
   - `81e680d...`, `025deb70...`, `608426cb...`: reverted as pending authority-safe repair.
3. Rejected piecemeal TS narrowing because it breaks current bootstrap fail-closed state semantics.
4. Rejected blindly restoring the prior quarantine because it changes runtime state outside the canonical transition path and was explicitly reverted as not yet authority-safe.

## Alternative paths
- Design an explicit pre-admission quarantine with provable restart/recovery semantics and evidence rules.
- Add a dedicated authoritative bootstrap-failure transition only if primary Spec is amended; current build authority does not provide one.
- Preserve the broad TS edge temporarily only as an acknowledged mismatch, never as VERIFIED final-DOC-C parity.

## Dependency graph
`FINAL DOC-C FSM authority -> TS/Rust parity -> bootstrap failure design -> contract tests -> integration validation`

## Unblock condition
A design must be demonstrated that simultaneously:
- obeys final DOC-C legal transition authority,
- fails closed on bootstrap dependency/tick failure,
- cannot silently recover on restart,
- preserves incident/audit truth when persistence is available,
- and can be tested at an exact candidate SHA.

## Chats consulted
No peer conclusion was trusted as authority. Git history and primary Spec were inspected directly.

## Status
TRUE_BLOCK for this semantic mutation scope only. Project-wide work is NOT blocked.
