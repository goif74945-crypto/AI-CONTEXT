"""AI-PROPOSED: integrity validator for requirement/test/evidence manifests."""
from __future__ import annotations

import hashlib
from collections import Counter, deque
from typing import Any, Mapping, Sequence


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_manifest(nodes: Sequence[Mapping[str, Any]], blobs: Mapping[str, str]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    ids = [str(node.get("id", "")) for node in nodes]
    counts = Counter(ids)

    for node_id, count in sorted(counts.items()):
        if not node_id:
            errors.append({"code": "EMPTY_ID", "id": node_id})
        elif count > 1:
            errors.append({"code": "DUPLICATE_ID", "id": node_id, "count": count})

    by_id: dict[str, Mapping[str, Any]] = {}
    for node in nodes:
        node_id = str(node.get("id", ""))
        if node_id and node_id not in by_id:
            by_id[node_id] = node

    for node_id, node in sorted(by_id.items()):
        refs = node.get("refs", [])
        if not isinstance(refs, list):
            errors.append({"code": "INVALID_REFS", "id": node_id})
            continue
        for ref in sorted({str(r) for r in refs}):
            if ref not in by_id:
                errors.append({"code": "MISSING_REF", "id": node_id, "ref": ref})

        expected_hash = node.get("sha256")
        if expected_hash is not None:
            if node_id not in blobs:
                errors.append({"code": "MISSING_BLOB", "id": node_id})
            else:
                actual = _sha256(blobs[node_id])
                if actual != expected_hash:
                    errors.append(
                        {
                            "code": "STALE_HASH",
                            "id": node_id,
                            "expected": str(expected_hash),
                            "actual": actual,
                        }
                    )

    # Detect cycles among resolvable references.
    color: dict[str, int] = {node_id: 0 for node_id in by_id}
    cycles: set[tuple[str, str]] = set()

    def visit(node_id: str) -> None:
        color[node_id] = 1
        refs = by_id[node_id].get("refs", [])
        if isinstance(refs, list):
            for ref in sorted(str(r) for r in refs if str(r) in by_id):
                if color[ref] == 0:
                    visit(ref)
                elif color[ref] == 1:
                    cycles.add((node_id, ref))
        color[node_id] = 2

    for node_id in sorted(by_id):
        if color[node_id] == 0:
            visit(node_id)
    for src, dst in sorted(cycles):
        errors.append({"code": "REFERENCE_CYCLE", "id": src, "ref": dst})

    roots = sorted(node_id for node_id, node in by_id.items() if node.get("kind") == "requirement")
    reachable: set[str] = set(roots)
    queue = deque(roots)
    while queue:
        current = queue.popleft()
        refs = by_id[current].get("refs", [])
        if not isinstance(refs, list):
            continue
        for ref in sorted(str(r) for r in refs):
            if ref in by_id and ref not in reachable:
                reachable.add(ref)
                queue.append(ref)

    orphans = sorted(node_id for node_id in by_id if node_id not in reachable)
    errors.sort(key=lambda e: (e["code"], e.get("id", ""), e.get("ref", "")))

    if not by_id:
        status = "NOT_VERIFIED"
    else:
        status = "FAIL" if errors else ("PARTIAL" if orphans else "PASS")
    return {
        "status": status,
        "node_count": len(by_id),
        "errors": errors,
        "orphans": orphans,
        "reachable": sorted(reachable),
    }
