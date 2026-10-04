# NEXY Outcome Closure Mesh — Architecture

Status: AI_PROPOSED / NON_GOVERNING

## System purpose
NOCM is an isolated reference layer for proving **outcome closure**, not merely activity completion. It composes five deterministic modules without giving any module authority to execute NEXY directives or promote itself into NEXY law.

```
Blocking UNKNOWNs
      │
      ▼
Reversible Probe Planner ──safe probe plan only──▶ new evidence
      │
      ▼
Outcome Closure Engine ──CLOSED/OPEN/FREEZE──▶ Progress Truth Ledger
      │                                              │
      └──────────────────────────────────────────────┘
                         │
                         ▼
                Benefit Regression Judge
                         │
                         ▼
                Adoption Readiness Firewall
                         │
                         ▼
             READY_FOR_HUMAN_REVIEW / HOLD / FREEZE
```

## Design principles
- Deterministic normalization and stable ordering.
- Fail closed on malformed identities, authority deficits, unsafe effects, contradictions, or protected mutation.
- Exact integer accounting for progress and probe costs.
- No probabilistic guess is required by the reference implementation.
- Fingerprints are deterministic identity fingerprints, explicitly **not cryptographic security hashes**.
- Human adoption remains external authority.

## Concept 1 — Outcome Closure Engine
Input: contract containing required predicates, forbidden predicates, and minimum evidence per required predicate; observations with status and evidence IDs.

Output: `CLOSED`, `OPEN`, or `FREEZE`, plus explicit required gaps, evidence deficits, unresolved forbidden conditions, triggered forbidden conditions, reasons, and fingerprint.

Critical behavior:
- `CLOSED` requires every required predicate to be `SATISFIED` with enough evidence.
- A forbidden predicate must be explicitly shown absent (`VIOLATED`) with evidence before closure.
- A satisfied forbidden predicate or malformed contract causes `FREEZE`.
- UNKNOWN never silently becomes safe.

Trade-off: conservative closure can delay completion, but it prevents the much more expensive failure mode of declaring success while a forbidden condition is unresolved.

## Concept 2 — Progress Truth Ledger
Input: stable obligation IDs with `PASS | FAIL | PENDING | BLOCKED | UNKNOWN`.

Output: `COMPLETE | INCOMPLETE | BLOCKED | NOT_VERIFIED | FREEZE`, a factual pass ratio in basis points, status partitions, and a completion-claim boolean.

Critical behavior:
- Only all-PASS permits a completion claim.
- UNKNOWN yields NOT_VERIFIED.
- BLOCKED outranks PENDING.
- Duplicate IDs freeze instead of double-counting work.
- Empty work is not treated as 100% complete.

Trade-off: the pass ratio is intentionally not a forecast of remaining time. It is a truth-preserving count, less glamorous and much harder to lie with.

## Concept 3 — Reversible Probe Planner
Input: blocking unknowns, candidate probes, probe effect class, integer cost, required authority, optional rollback, available authorities, optional cost budget.

Output: `READY | PROBE | BLOCKED | FREEZE`, minimum-cost safe cover, rejected probes, coverage witness, and fingerprint.

Critical behavior:
- Irreversible probes are always rejected.
- Reversible writes require rollback text and sufficient authority.
- OWNER satisfies OPERATOR-level authority; OPERATOR does not satisfy OWNER.
- Exact bounded search minimizes total cost, then probe count, then canonical ID tuple.
- Search is capped at 24 safe relevant candidates; exceeding the bound returns BLOCKED instead of pretending exact optimization completed.
- Planner emits a plan only. It does not execute effects.

Trade-off: bounded exact search can BLOCK large candidate sets rather than use a heuristic. This deliberately preserves the meaning of “minimum” and lets a future production implementation replace the search algorithm without changing semantics.

## Concept 4 — Benefit Regression Judge
Input: declared value axes, direction (`HIGHER`/`LOWER`), critical flag, minimum improvement, maximum tolerated regression, baseline observations, candidate observations.

Output: `BENEFICIAL | REJECT | INCONCLUSIVE | FREEZE`, improved/regressed/missing axes and normalized deltas.

Critical behavior:
- Missing observations are INCONCLUSIVE.
- At least one declared improvement is required.
- Regression beyond tolerance on a critical axis rejects the candidate.
- Invalid threshold contracts freeze.
- Noncritical regressions remain visible and can coexist with BENEFICIAL if a real declared improvement exists; downstream human review owns the trade-off decision.

Trade-off: this is not statistics. It is suitable for exact, already-observed metrics and explicit engineering acceptance deltas, while Product Evidence Lab remains the better fit for uncertain experimental inference.

## Concept 5 — Adoption Readiness Firewall
Input: collision status, compatibility checks, required/present evidence classes, rollback state, protected-scope mutation flag, and upstream outcome/progress/benefit verdicts.

Output: `READY_FOR_HUMAN_REVIEW | HOLD | FREEZE`, reasons and missing evidence classes.

Critical behavior:
- `automaticApproval` is a literal false in the output type and implementation.
- Protected-scope mutation freezes.
- Explicit compatibility failure freezes; compatibility UNKNOWN holds.
- Unresolved collision, missing evidence, unverified rollback, open outcome, incomplete progress, or non-beneficial result holds.
- No state maps to automatic adoption.

Trade-off: this adds friction before adoption. The point is that adoption of an AI-generated subsystem should have friction exactly where evidence, compatibility, rollback, or human authority is incomplete.

## Composition invariant
No upstream success can erase a downstream blocker. A passing Benefit Regression result cannot override an OPEN outcome. A complete Progress ledger cannot override protected mutation. A safe Probe plan cannot itself turn an UNKNOWN into verified evidence. The mesh composes by conjunction, not by averaging confidence.
