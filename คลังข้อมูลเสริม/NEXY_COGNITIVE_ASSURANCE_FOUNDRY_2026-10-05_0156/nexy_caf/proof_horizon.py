from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .contracts import Decision, Finding, Verdict, stable_tuple


@dataclass(frozen=True, slots=True)
class ProofNode:
    proof_id: str
    depends_on: tuple[str, ...]
    evidence_class: str
    freshness_budget: int
    age: int

    def __post_init__(self) -> None:
        if not self.proof_id.strip():
            raise ValueError("proof_id must not be empty")
        if self.freshness_budget < 0 or self.age < 0:
            raise ValueError("freshness_budget and age must be >= 0")


class ProofHorizonScheduler:
    """Invalidate evidence transitively when a dependency drifts or gets stale."""

    ENGINE = "proof-horizon-scheduler"

    def schedule(
        self,
        proofs: Iterable[ProofNode],
        *,
        changed_dependencies: Iterable[str] = (),
        critical_evidence_classes: Iterable[str] = ("E4", "E5", "E6", "E7"),
    ) -> Decision:
        supplied = tuple(proofs)
        ids = [p.proof_id for p in supplied]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate proof_id")
        nodes = {p.proof_id: p for p in supplied}
        ordered = sorted(supplied, key=lambda p: p.proof_id)

        changed = set(stable_tuple(tuple(changed_dependencies)))
        critical = set(stable_tuple(tuple(critical_evidence_classes)))
        invalid: set[str] = set()
        reasons: dict[str, set[str]] = {p.proof_id: set() for p in ordered}
        findings: list[Finding] = []

        for p in ordered:
            missing = sorted(d for d in p.depends_on if d.startswith("proof:") and d[6:] not in nodes)
            if missing:
                invalid.add(p.proof_id)
                reasons[p.proof_id].update(f"missing:{x}" for x in missing)
            if p.age > p.freshness_budget:
                invalid.add(p.proof_id)
                reasons[p.proof_id].add("stale")
            direct = sorted(set(p.depends_on) & changed)
            if direct:
                invalid.add(p.proof_id)
                reasons[p.proof_id].update(f"changed:{x}" for x in direct)

        progressed = True
        while progressed:
            progressed = False
            for p in ordered:
                upstream_invalid = {
                    d[6:] for d in p.depends_on if d.startswith("proof:") and d[6:] in invalid
                }
                if upstream_invalid and p.proof_id not in invalid:
                    invalid.add(p.proof_id)
                    reasons[p.proof_id].update(f"upstream:{x}" for x in sorted(upstream_invalid))
                    progressed = True

        plan = []
        for p in ordered:
            if p.proof_id in invalid:
                priority = 100 if p.evidence_class in critical else 60
                plan.append((priority, p.proof_id, tuple(sorted(reasons[p.proof_id]))))
        plan.sort(key=lambda x: (-x[0], x[1]))

        if plan:
            findings.append(
                Finding(
                    "PROOF_REVALIDATION_REQUIRED",
                    90 if any(x[0] == 100 for x in plan) else 70,
                    "One or more proof nodes crossed their proof horizon.",
                    tuple(x[1] for x in plan),
                )
            )

        verdict = Verdict.FREEZE if any(x[0] == 100 for x in plan) else (Verdict.REVIEW if plan else Verdict.PASS)
        score = max(0, 100 - min(100, len(plan) * 15))
        return Decision(
            engine=self.ENGINE,
            verdict=verdict,
            score=score,
            findings=tuple(findings),
            payload={
                "changed_dependencies": tuple(sorted(changed)),
                "revalidation_plan": tuple(plan),
                "valid_proof_count": len(ordered) - len(invalid),
                "invalid_proof_count": len(invalid),
            },
        )
