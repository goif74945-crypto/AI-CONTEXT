from __future__ import annotations

from dataclasses import dataclass
import unicodedata
from typing import Iterable


def _norm(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().casefold()
    if not normalized:
        raise ValueError("names and aliases must be non-empty")
    return normalized


@dataclass(frozen=True)
class SymbolContract:
    namespace: str
    canonical_name: str
    semantic_id: str
    kind: str
    domain: str
    unit: str | None
    authority: str
    lifecycle: str
    aliases: tuple[str, ...] = ()

    def signature(self) -> tuple[str, str, str | None, str, str]:
        return (self.kind, self.domain, self.unit, self.authority, self.lifecycle)

    def labels(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys((_norm(self.canonical_name), *(_norm(a) for a in self.aliases))))


@dataclass(frozen=True)
class Collision:
    severity: str
    collision_type: str
    label: str
    left: str
    right: str
    reason: str


class SemanticNamespaceCollisionGuard:
    """Detects name/alias reuse that would make cross-layer contracts semantically ambiguous."""

    @staticmethod
    def analyze(contracts: Iterable[SymbolContract]) -> tuple[Collision, ...]:
        items = tuple(contracts)
        seen_identity: dict[str, SymbolContract] = {}
        label_index: dict[str, list[SymbolContract]] = {}
        collisions: list[Collision] = []

        for item in items:
            if not item.semantic_id.strip():
                raise ValueError("semantic_id must be non-empty")
            prior = seen_identity.get(item.semantic_id)
            if prior is not None and prior.signature() != item.signature():
                collisions.append(Collision(
                    "CRITICAL",
                    "IDENTITY_DRIFT",
                    item.semantic_id,
                    f"{prior.namespace}:{prior.canonical_name}",
                    f"{item.namespace}:{item.canonical_name}",
                    "same semantic_id has incompatible contract signature",
                ))
            else:
                seen_identity[item.semantic_id] = item
            for label in item.labels():
                label_index.setdefault(label, []).append(item)

        for label, bound in label_index.items():
            for i, left in enumerate(bound):
                for right in bound[i + 1 :]:
                    same_identity = left.semantic_id == right.semantic_id
                    same_signature = left.signature() == right.signature()
                    if same_identity and same_signature:
                        continue
                    collision_type = "NAMESPACE_COLLISION" if not same_identity else "IDENTITY_DRIFT"
                    severity = "HIGH" if not same_identity else "CRITICAL"
                    collisions.append(Collision(
                        severity,
                        collision_type,
                        label,
                        f"{left.namespace}:{left.canonical_name}",
                        f"{right.namespace}:{right.canonical_name}",
                        "same normalized label resolves to incompatible semantics",
                    ))

        dedup = {
            (c.severity, c.collision_type, c.label, c.left, c.right, c.reason): c
            for c in collisions
        }
        return tuple(sorted(dedup.values(), key=lambda c: (c.severity, c.collision_type, c.label, c.left, c.right)))
