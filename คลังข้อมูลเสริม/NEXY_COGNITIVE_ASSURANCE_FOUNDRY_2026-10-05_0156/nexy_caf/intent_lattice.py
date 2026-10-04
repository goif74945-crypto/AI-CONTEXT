from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .contracts import Decision, Finding, Verdict, stable_tuple


@dataclass(frozen=True, slots=True)
class IntentContract:
    objective: str
    authorized_scope: tuple[str, ...]
    protected_scope: tuple[str, ...]
    invariants: tuple[str, ...]
    required_evidence: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    authority_sources: tuple[str, ...]


class IntentLatticeCompiler:
    """Compile intent into a deterministic contract and freeze on material gaps.

    The lattice is deliberately conservative: scope overlap, missing objective,
    missing authority, or a required-evidence vacuum cannot silently pass.
    """

    ENGINE = "intent-lattice-compiler"

    @staticmethod
    def _norm(values: Iterable[str]) -> tuple[str, ...]:
        return stable_tuple(tuple(values))

    def compile(
        self,
        *,
        objective: str,
        authorized_scope: Iterable[str],
        protected_scope: Iterable[str],
        invariants: Iterable[str],
        required_evidence: Iterable[str],
        stop_conditions: Iterable[str],
        authority_sources: Iterable[str],
        known_conflicts: Mapping[str, str] | None = None,
    ) -> Decision:
        contract = IntentContract(
            objective=objective.strip(),
            authorized_scope=self._norm(authorized_scope),
            protected_scope=self._norm(protected_scope),
            invariants=self._norm(invariants),
            required_evidence=self._norm(required_evidence),
            stop_conditions=self._norm(stop_conditions),
            authority_sources=self._norm(authority_sources),
        )
        findings: list[Finding] = []

        if not contract.objective:
            findings.append(Finding("INTENT_NO_OBJECTIVE", 100, "Objective is empty."))
        if not contract.authority_sources:
            findings.append(Finding("INTENT_NO_AUTHORITY", 100, "No authority source is declared."))
        if not contract.authorized_scope:
            findings.append(Finding("INTENT_NO_SCOPE", 90, "Authorized scope is empty."))
        if not contract.required_evidence:
            findings.append(Finding("INTENT_NO_EVIDENCE", 85, "Required evidence is undefined."))
        if not contract.stop_conditions:
            findings.append(Finding("INTENT_NO_STOP", 70, "Stop conditions are undefined."))

        overlap = sorted(set(contract.authorized_scope) & set(contract.protected_scope))
        if overlap:
            findings.append(
                Finding(
                    "INTENT_SCOPE_COLLISION",
                    100,
                    "Authorized and protected scope overlap.",
                    tuple(overlap),
                )
            )

        conflicts = known_conflicts or {}
        for key in sorted(conflicts):
            findings.append(
                Finding(
                    "INTENT_AUTHORITY_CONFLICT",
                    100,
                    f"Unresolved authority conflict: {key}",
                    (str(conflicts[key]),),
                )
            )

        hard = any(f.severity >= 85 for f in findings)
        score = max(0, 100 - sum(min(f.severity, 50) for f in findings))
        verdict = Verdict.FREEZE if hard else (Verdict.REVIEW if findings else Verdict.PASS)

        return Decision(
            engine=self.ENGINE,
            verdict=verdict,
            score=score,
            findings=tuple(findings),
            payload={
                "contract": {
                    "objective": contract.objective,
                    "authorized_scope": contract.authorized_scope,
                    "protected_scope": contract.protected_scope,
                    "invariants": contract.invariants,
                    "required_evidence": contract.required_evidence,
                    "stop_conditions": contract.stop_conditions,
                    "authority_sources": contract.authority_sources,
                },
                "conflict_count": len(conflicts),
            },
        )
