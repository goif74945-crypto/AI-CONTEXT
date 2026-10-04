from __future__ import annotations

from collections import defaultdict
from typing import Any
from urllib.parse import urlparse

from .canonical import canonical_json


def _artifact_key(pkg: dict[str, str]) -> tuple[str, str, str]:
    return (pkg["version"], pkg["source"], pkg["integrity"])


def _source_origin(source: str) -> str:
    parsed = urlparse(source)
    if parsed.scheme and parsed.hostname:
        try:
            port = parsed.port
        except ValueError:
            port = None
        authority = parsed.hostname.lower()
        if port is not None:
            authority = f"{authority}:{port}"
        return f"{parsed.scheme.lower()}://{authority}"
    return source

def _logical_key(pkg: dict[str, str]) -> tuple[str, str]:
    return (pkg["ecosystem"], pkg["name"])


def _event(event_type: str, ecosystem: str, name: str, before: dict[str, str] | None, after: dict[str, str] | None) -> dict[str, Any]:
    return {"type": event_type, "ecosystem": ecosystem, "name": name, "before": before, "after": after}


def diff_snapshots(baseline: dict[str, Any], candidate: dict[str, Any]) -> list[dict[str, Any]]:
    left: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    right: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for pkg in baseline.get("packages", []):
        left[_logical_key(pkg)].append(pkg)
    for pkg in candidate.get("packages", []):
        right[_logical_key(pkg)].append(pkg)

    events: list[dict[str, Any]] = []
    for key in sorted(set(left) | set(right)):
        ecosystem, name = key
        before = sorted(left.get(key, []), key=_artifact_key)
        after = sorted(right.get(key, []), key=_artifact_key)
        if not before:
            events.extend(_event("ADDITION", ecosystem, name, None, pkg) for pkg in after)
            continue
        if not after:
            events.extend(_event("REMOVAL", ecosystem, name, pkg, None) for pkg in before)
            continue
        if len(before) == 1 and len(after) == 1:
            b, a = before[0], after[0]
            if _artifact_key(b) == _artifact_key(a):
                continue
            if b["version"] != a["version"]:
                events.append(_event("VERSION_CHANGE", ecosystem, name, b, a))
                if _source_origin(b["source"]) != _source_origin(a["source"]):
                    events.append(_event("SOURCE_CHANGE", ecosystem, name, b, a))
            elif b["source"] != a["source"]:
                events.append(_event("SOURCE_CHANGE", ecosystem, name, b, a))
            elif b["integrity"] != a["integrity"]:
                events.append(_event("INTEGRITY_CHANGE", ecosystem, name, b, a))
            continue

        before_map = {_artifact_key(pkg): pkg for pkg in before}
        after_map = {_artifact_key(pkg): pkg for pkg in after}
        for artifact in sorted(set(before_map) - set(after_map)):
            events.append(_event("REMOVAL", ecosystem, name, before_map[artifact], None))
        for artifact in sorted(set(after_map) - set(before_map)):
            events.append(_event("ADDITION", ecosystem, name, None, after_map[artifact]))

    events.sort(key=lambda e: (e["ecosystem"], e["name"], e["type"], canonical_json(e["before"]), canonical_json(e["after"])))
    return events
