from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .common import ContractError, fingerprint


def _parse_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ContractError("timestamp must be string")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"invalid timestamp: {value!r}") from exc
    if dt.tzinfo is None:
        raise ContractError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


def plan_revalidation(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ContractError("payload must be object")
    now = _parse_time(payload.get("now"))
    current_versions = payload.get("current_versions", {})
    artifacts = payload.get("artifacts")
    if not isinstance(current_versions, dict):
        raise ContractError("current_versions must be object")
    if not isinstance(artifacts, list) or not artifacts:
        raise ContractError("artifacts must be non-empty list")
    if len(artifacts) > 5000:
        raise ContractError("artifact count exceeds 5000")
    by_id: dict[str, dict[str, Any]] = {}
    for art in artifacts:
        if not isinstance(art, dict):
            raise ContractError("artifact must be object")
        aid = art.get("id")
        if not isinstance(aid, str) or not aid:
            raise ContractError("artifact.id must be non-empty string")
        if aid in by_id:
            raise ContractError(f"duplicate artifact id: {aid}")
        by_id[aid] = art

    stale: dict[str, set[str]] = {aid: set() for aid in by_id}
    for aid, art in sorted(by_id.items()):
        observed = _parse_time(art.get("observed_at"))
        max_age = art.get("max_age_seconds")
        if not isinstance(max_age, int) or max_age < 0:
            raise ContractError("max_age_seconds must be non-negative int")
        if observed > now:
            stale[aid].add("OBSERVED_IN_FUTURE")
        elif (now - observed).total_seconds() > max_age:
            stale[aid].add("TTL_EXPIRED")
        captured = art.get("captured_versions", {})
        if not isinstance(captured, dict):
            raise ContractError("captured_versions must be object")
        for dep, version in sorted(captured.items()):
            if dep not in current_versions:
                stale[aid].add(f"UNKNOWN_CURRENT_VERSION:{dep}")
            elif current_versions[dep] != version:
                stale[aid].add(f"VERSION_CHANGED:{dep}")

    # Evidence dependencies form a DAG where an artifact may rely on another evidence artifact.
    graph: dict[str, list[str]] = {}
    reverse: dict[str, list[str]] = {aid: [] for aid in by_id}
    for aid, art in sorted(by_id.items()):
        deps = art.get("depends_on_artifacts", [])
        if not isinstance(deps, list) or not all(isinstance(x, str) for x in deps):
            raise ContractError("depends_on_artifacts must be list[str]")
        for dep in deps:
            if dep not in by_id:
                raise ContractError(f"unknown evidence artifact dependency: {dep}")
            reverse[dep].append(aid)
        graph[aid] = sorted(deps)

    state: dict[str, int] = {}
    order: list[str] = []
    def visit(node: str) -> None:
        mark = state.get(node, 0)
        if mark == 1:
            raise ContractError("artifact dependency cycle")
        if mark == 2:
            return
        state[node] = 1
        for dep in graph[node]:
            visit(dep)
        state[node] = 2
        order.append(node)
    for aid in sorted(by_id):
        visit(aid)

    for aid in order:
        for dep in graph[aid]:
            if stale[dep]:
                stale[aid].add(f"UPSTREAM_STALE:{dep}")

    revalidate = [aid for aid in order if stale[aid]]
    return {
        "status": "PASS" if not revalidate else "FREEZE",
        "reason_codes": [] if not revalidate else ["STALE_EVIDENCE_REQUIRES_REVALIDATION"],
        "input_hash": fingerprint(payload),
        "stale": {aid: sorted(reasons) for aid, reasons in sorted(stale.items()) if reasons},
        "revalidation_order": revalidate,
        "fresh_artifacts": sorted(aid for aid in by_id if not stale[aid]),
    }
