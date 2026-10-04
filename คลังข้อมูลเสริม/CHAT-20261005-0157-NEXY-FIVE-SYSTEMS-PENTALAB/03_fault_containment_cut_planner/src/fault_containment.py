from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable


class ContainmentInputError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Component:
    component_id: str
    mandatory: bool = False


@dataclass(frozen=True, slots=True)
class Dependency:
    provider: str
    consumer: str
    mode: str


@dataclass(frozen=True, slots=True)
class ContainmentResult:
    status: str
    quarantined: tuple[str, ...]
    degraded: tuple[str, ...]
    healthy: tuple[str, ...]
    reason_parents: tuple[tuple[str, str | None], ...]
    reason_codes: tuple[str, ...]
    fingerprint: str

    def reason_path(self, component_id: str) -> tuple[str, ...]:
        parents = dict(self.reason_parents)
        if component_id not in parents:
            raise KeyError(component_id)
        path: list[str] = []
        seen: set[str] = set()
        current: str | None = component_id
        while current is not None:
            if current in seen:
                raise RuntimeError("REASON_LINEAGE_CYCLE")
            seen.add(current)
            path.append(current)
            current = parents[current]
        path.reverse()
        return tuple(path)


def _clean(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise ContainmentInputError(f"{field}:NOT_STRING")
    value = value.strip()
    if not value:
        raise ContainmentInputError(f"{field}:EMPTY")
    return value


def plan_containment(
    components: Iterable[Component],
    dependencies: Iterable[Dependency],
    failed_components: Iterable[str],
) -> ContainmentResult:
    comps = sorted(
        (Component(_clean(c.component_id, "component_id"), bool(c.mandatory)) for c in components),
        key=lambda c: c.component_id,
    )
    ids = [c.component_id for c in comps]
    if not ids:
        raise ContainmentInputError("NO_COMPONENTS")
    if len(ids) != len(set(ids)):
        raise ContainmentInputError("DUPLICATE_COMPONENT_ID")
    mandatory = {c.component_id for c in comps if c.mandatory}
    all_ids = set(ids)

    deps: list[Dependency] = []
    for d in dependencies:
        provider = _clean(d.provider, "dependency.provider")
        consumer = _clean(d.consumer, "dependency.consumer")
        mode = _clean(d.mode, "dependency.mode").upper()
        if mode not in {"HARD", "SOFT", "ISOLATED"}:
            raise ContainmentInputError(f"INVALID_MODE:{mode}")
        if provider not in all_ids or consumer not in all_ids:
            raise ContainmentInputError(f"UNKNOWN_COMPONENT_REF:{provider}->{consumer}")
        if provider == consumer:
            raise ContainmentInputError(f"SELF_DEPENDENCY:{provider}")
        deps.append(Dependency(provider, consumer, mode))
    deps.sort(key=lambda d: (d.provider, d.consumer, d.mode))
    if len(deps) != len(set(deps)):
        raise ContainmentInputError("DUPLICATE_DEPENDENCY")

    failed = tuple(sorted({_clean(x, "failed_component") for x in failed_components}))
    unknown_failed = set(failed) - all_ids
    if unknown_failed:
        raise ContainmentInputError(f"UNKNOWN_FAILED_COMPONENT:{sorted(unknown_failed)}")
    if not failed:
        return _finalize("FULL", (), (), tuple(ids), (), (), comps, deps, failed)

    outbound: dict[str, list[Dependency]] = {cid: [] for cid in ids}
    for d in deps:
        outbound[d.provider].append(d)

    quarantined: set[str] = set(failed)
    degraded: set[str] = set()
    parent: dict[str, str | None] = {f: None for f in failed}
    q = deque(failed)
    while q:
        provider = q.popleft()
        for d in outbound[provider]:
            if d.mode == "ISOLATED":
                continue
            if d.mode == "SOFT":
                if d.consumer not in quarantined:
                    degraded.add(d.consumer)
                continue
            if d.consumer not in quarantined:
                quarantined.add(d.consumer)
                degraded.discard(d.consumer)
                parent[d.consumer] = provider
                q.append(d.consumer)

    for d in deps:
        if d.mode == "SOFT" and d.provider in quarantined and d.consumer not in quarantined:
            degraded.add(d.consumer)

    healthy = all_ids - quarantined - degraded
    reason_codes: set[str] = set()
    if quarantined & mandatory:
        status = "FREEZE"
        reason_codes.add("MANDATORY_COMPONENT_QUARANTINED")
    elif degraded or len(quarantined) > len(failed):
        status = "DEGRADED"
        reason_codes.add("CONTAINED_WITH_DEGRADATION")
    else:
        status = "DEGRADED"
        reason_codes.add("LOCAL_FAILURE_CONTAINED")

    reason_parents = tuple(sorted(parent.items()))
    return _finalize(
        status,
        tuple(sorted(quarantined)),
        tuple(sorted(degraded)),
        tuple(sorted(healthy)),
        reason_parents,
        tuple(sorted(reason_codes)),
        comps,
        deps,
        failed,
    )


def _finalize(
    status: str,
    quarantined: tuple[str, ...],
    degraded: tuple[str, ...],
    healthy: tuple[str, ...],
    reason_parents: tuple[tuple[str, str | None], ...],
    reason_codes: tuple[str, ...],
    comps: list[Component],
    deps: list[Dependency],
    failed: tuple[str, ...],
) -> ContainmentResult:
    payload = {
        "status": status,
        "quarantined": quarantined,
        "degraded": degraded,
        "healthy": healthy,
        "reason_parents": reason_parents,
        "reason_codes": reason_codes,
        "input": {
            "components": [(c.component_id, c.mandatory) for c in comps],
            "dependencies": [(d.provider, d.consumer, d.mode) for d in deps],
            "failed": failed,
        },
    }
    fingerprint = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ContainmentResult(status, quarantined, degraded, healthy, reason_parents, reason_codes, fingerprint)
