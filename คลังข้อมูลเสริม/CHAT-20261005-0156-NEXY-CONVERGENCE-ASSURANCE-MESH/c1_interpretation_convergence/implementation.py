from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from shared import GateResult, canonical_json, sha256_hex


@dataclass(frozen=True)
class Interpretation:
    interpretation_id: str
    variables: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not self.interpretation_id.strip():
            raise ValueError("interpretation_id must be non-empty")


@dataclass(frozen=True)
class DecisionSignature:
    action: str
    target: str
    scope: tuple[str, ...]
    effects: tuple[str, ...]
    authority_epoch: str

    def __post_init__(self) -> None:
        if not self.action.strip() or not self.target.strip() or not self.authority_epoch.strip():
            raise ValueError("action, target, and authority_epoch must be non-empty")

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "target": self.target,
            "scope": sorted(set(self.scope)),
            "effects": sorted(set(self.effects)),
            "authority_epoch": self.authority_epoch,
        }


DecisionEvaluator = Callable[[Interpretation], DecisionSignature]


def _divergent_fields(signatures: Iterable[DecisionSignature]) -> tuple[str, ...]:
    payloads = [s.canonical_payload() for s in signatures]
    fields = ("action", "target", "scope", "effects", "authority_epoch")
    return tuple(
        field
        for field in fields
        if len({canonical_json(payload[field]) for payload in payloads}) > 1
    )


def evaluate_convergence(
    interpretations: Iterable[Interpretation],
    evaluator: DecisionEvaluator,
) -> GateResult:
    ordered = sorted(tuple(interpretations), key=lambda item: item.interpretation_id)
    if not ordered:
        return GateResult("FREEZE", "NO_INTERPRETATIONS", {"interpretation_count": 0})

    ids = [item.interpretation_id for item in ordered]
    if len(set(ids)) != len(ids):
        return GateResult("FREEZE", "DUPLICATE_INTERPRETATION_ID", {"ids": ids})

    evaluated: list[tuple[Interpretation, DecisionSignature, str]] = []
    for interpretation in ordered:
        try:
            signature = evaluator(interpretation)
            fingerprint = sha256_hex(signature.canonical_payload())
        except Exception as exc:  # fail closed across caller-supplied evaluators
            return GateResult(
                "FREEZE",
                "EVALUATOR_FAILURE",
                {
                    "interpretation_id": interpretation.interpretation_id,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
        evaluated.append((interpretation, signature, fingerprint))

    fingerprints = {fingerprint for _, _, fingerprint in evaluated}
    witness = [
        {
            "interpretation_id": interpretation.interpretation_id,
            "signature_hash": fingerprint,
            "signature": signature.canonical_payload(),
        }
        for interpretation, signature, fingerprint in evaluated
    ]

    if len(fingerprints) == 1:
        signature = evaluated[0][1]
        return GateResult(
            "RELEASE",
            "ALL_ADMISSIBLE_INTERPRETATIONS_CONVERGE",
            {
                "decision_signature": signature.canonical_payload(),
                "decision_hash": evaluated[0][2],
                "interpretation_count": len(evaluated),
                "witness": witness,
            },
        )

    return GateResult(
        "FREEZE",
        "DECISION_RELEVANT_AMBIGUITY",
        {
            "divergent_fields": _divergent_fields(item[1] for item in evaluated),
            "distinct_decision_count": len(fingerprints),
            "witness": witness,
        },
    )
