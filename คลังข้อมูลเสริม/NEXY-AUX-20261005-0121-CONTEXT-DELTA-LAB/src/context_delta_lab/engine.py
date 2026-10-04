from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Iterable

AUTHORITIES = {
    "DOC_B",
    "DOC_C",
    "DOC_D",
    "DOC_E",
    "PROJECT_CONTEXT",
    "AI_PROPOSAL",
}
SCOPES = {
    "CURRENT_GOVERNING_LAW",
    "CURRENT_BUILD",
    "CURRENT_BUILD_SUPPLEMENT",
    "SUPPORTED_PRODUCT_DESIGN",
    "DEPLOYMENT_EVIDENCE",
    "EXCLUDED_CURRENT",
    "DEFERRED_FUTURE",
    "ADVISORY",
}
EVIDENCE_CLASSES = {"E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "NOT_APPLICABLE"}
SEVERITY_SCORE = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}


class ValidationError(ValueError):
    """Semantic input error that must freeze processing."""


@dataclass(frozen=True)
class Change:
    record_id: str
    kind: str
    reasons: tuple[str, ...]
    severity: str
    old: dict[str, Any] | None
    new: dict[str, Any] | None


def _norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require_string(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} must be a non-empty string")
    return value.strip()


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValidationError("each requirement must be an object")
    record_id = _require_string(raw, "id")
    authority = _require_string(raw, "authority")
    scope = _require_string(raw, "scope")
    statement = _norm_text(_require_string(raw, "statement"))
    evidence_class = _require_string(raw, "evidence_class")
    if authority not in AUTHORITIES:
        raise ValidationError(f"{record_id}: unknown authority {authority}")
    if scope not in SCOPES:
        raise ValidationError(f"{record_id}: unknown scope {scope}")
    if evidence_class not in EVIDENCE_CLASSES:
        raise ValidationError(f"{record_id}: unknown evidence_class {evidence_class}")

    depends_on = raw.get("depends_on", [])
    if not isinstance(depends_on, list) or any(not isinstance(x, str) or not x.strip() for x in depends_on):
        raise ValidationError(f"{record_id}: depends_on must be a list of non-empty strings")
    dep_ids = sorted(set(x.strip() for x in depends_on))
    if record_id in dep_ids:
        raise ValidationError(f"{record_id}: self-dependency is forbidden")

    source_hash = raw.get("source_hash")
    if source_hash is not None and (not isinstance(source_hash, str) or not source_hash.strip()):
        raise ValidationError(f"{record_id}: source_hash must be null or a non-empty string")

    metadata = raw.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValidationError(f"{record_id}: metadata must be an object")

    return {
        "id": record_id,
        "authority": authority,
        "scope": scope,
        "statement": statement,
        "evidence_class": evidence_class,
        "depends_on": dep_ids,
        "source_hash": source_hash.strip() if isinstance(source_hash, str) else None,
        "metadata": metadata,
    }


def validate_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(snapshot, dict):
        raise ValidationError("snapshot must be an object")
    snapshot_id = _require_string(snapshot, "snapshot_id")
    source_commit = _require_string(snapshot, "source_commit")
    raw_records = snapshot.get("requirements")
    if not isinstance(raw_records, list):
        raise ValidationError("requirements must be a list")

    records = [normalize_record(item) for item in raw_records]
    by_id: dict[str, dict[str, Any]] = {}
    for rec in records:
        if rec["id"] in by_id:
            raise ValidationError(f"duplicate requirement id: {rec['id']}")
        by_id[rec["id"]] = rec

    for rec in records:
        for dep in rec["depends_on"]:
            if dep not in by_id:
                raise ValidationError(f"{rec['id']}: missing dependency {dep}")

    _assert_acyclic(by_id)
    normalized_records = [by_id[key] for key in sorted(by_id)]
    normalized = {
        "snapshot_id": snapshot_id,
        "source_commit": source_commit,
        "requirements": normalized_records,
    }
    normalized["fingerprint"] = sha256_json(normalized)
    return normalized


def _assert_acyclic(by_id: dict[str, dict[str, Any]]) -> None:
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        mark = state.get(node, 0)
        if mark == 2:
            return
        if mark == 1:
            if node in stack:
                start = stack.index(node)
                cycle = stack[start:] + [node]
            else:
                cycle = stack + [node]
            raise ValidationError("dependency cycle: " + " -> ".join(cycle))
        state[node] = 1
        stack.append(node)
        for dep in by_id[node]["depends_on"]:
            visit(dep)
        stack.pop()
        state[node] = 2

    for node in sorted(by_id):
        visit(node)


def _severity(old: dict[str, Any] | None, new: dict[str, Any] | None, reasons: Iterable[str]) -> str:
    reasons = set(reasons)
    rec = new or old or {}
    old_scope = old.get("scope") if old else None
    new_scope = new.get("scope") if new else None
    old_auth = old.get("authority") if old else None
    new_auth = new.get("authority") if new else None

    if new is None and old_scope in {"CURRENT_GOVERNING_LAW", "CURRENT_BUILD", "CURRENT_BUILD_SUPPLEMENT"}:
        return "CRITICAL"
    if "AUTHORITY_CHANGED" in reasons and ({old_auth, new_auth} & {"DOC_B", "DOC_C"}):
        return "CRITICAL"
    if "SCOPE_CHANGED" in reasons and ({old_scope, new_scope} & {"CURRENT_GOVERNING_LAW", "CURRENT_BUILD"}):
        return "CRITICAL"
    if rec.get("scope") in {"CURRENT_GOVERNING_LAW", "CURRENT_BUILD", "CURRENT_BUILD_SUPPLEMENT", "DEPLOYMENT_EVIDENCE"}:
        return "HIGH"
    if rec.get("scope") == "SUPPORTED_PRODUCT_DESIGN":
        return "MEDIUM"
    return "LOW"


def _change_reasons(old: dict[str, Any], new: dict[str, Any]) -> tuple[str, ...]:
    checks = (
        ("STATEMENT_CHANGED", "statement"),
        ("AUTHORITY_CHANGED", "authority"),
        ("SCOPE_CHANGED", "scope"),
        ("EVIDENCE_CLASS_CHANGED", "evidence_class"),
        ("DEPENDENCY_CHANGED", "depends_on"),
        ("SOURCE_HASH_CHANGED", "source_hash"),
        ("METADATA_CHANGED", "metadata"),
    )
    return tuple(label for label, field in checks if old.get(field) != new.get(field))


def _action_for(change: Change) -> str:
    reasons = set(change.reasons)
    if change.kind == "REMOVED":
        return "REVIEW_REMOVAL_AND_INVALIDATE_DEPENDENT_PROOF"
    if reasons & {"AUTHORITY_CHANGED", "SCOPE_CHANGED"}:
        return "REVIEW_AUTHORITY_THEN_REVALIDATE"
    if reasons & {"STATEMENT_CHANGED", "DEPENDENCY_CHANGED", "EVIDENCE_CLASS_CHANGED"}:
        return "REVALIDATE_REQUIREMENT_AND_MATCHING_EVIDENCE"
    return "REVIEW_SOURCE_DRIFT"


class DeltaEngine:
    def compare(self, base: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
        old = validate_snapshot(base)
        new = validate_snapshot(current)
        old_map = {r["id"]: r for r in old["requirements"]}
        new_map = {r["id"]: r for r in new["requirements"]}

        changes: list[Change] = []
        all_ids = sorted(set(old_map) | set(new_map))
        for record_id in all_ids:
            before = old_map.get(record_id)
            after = new_map.get(record_id)
            if before is None:
                reasons = ("ADDED",)
                changes.append(Change(record_id, "ADDED", reasons, _severity(None, after, reasons), None, after))
            elif after is None:
                reasons = ("REMOVED",)
                changes.append(Change(record_id, "REMOVED", reasons, _severity(before, None, reasons), before, None))
            else:
                reasons = _change_reasons(before, after)
                if reasons:
                    changes.append(Change(record_id, "MODIFIED", reasons, _severity(before, after, reasons), before, after))

        direct = {c.record_id: c for c in changes}
        reverse = self._reverse_dependencies(old_map, new_map)
        impacted = self._propagate(direct, reverse)

        queue = []
        for record_id in sorted(impacted, key=lambda rid: (-SEVERITY_SCORE[impacted[rid]["severity"]], 0 if rid in direct else 1, rid)):
            item = impacted[record_id]
            change = direct.get(record_id)
            current_rec = new_map.get(record_id)
            old_rec = old_map.get(record_id)
            evidence = (current_rec or old_rec or {}).get("evidence_class", "NOT_APPLICABLE")
            queue.append({
                "record_id": record_id,
                "severity": item["severity"],
                "impact": "DIRECT" if change else "TRANSITIVE",
                "reasons": list(change.reasons) if change else ["DEPENDENCY_IMPACT"],
                "via": item["via"],
                "required_action": _action_for(change) if change else "REVALIDATE_DEPENDENT_REQUIREMENT",
                "required_evidence_class": evidence,
                "status": "NOT_VERIFIED",
            })

        report_core = {
            "format_version": "0.1.0",
            "base": {"snapshot_id": old["snapshot_id"], "source_commit": old["source_commit"], "fingerprint": old["fingerprint"]},
            "current": {"snapshot_id": new["snapshot_id"], "source_commit": new["source_commit"], "fingerprint": new["fingerprint"]},
            "summary": {
                "change_count": len(changes),
                "impacted_count": len(impacted),
                "critical_count": sum(1 for q in queue if q["severity"] == "CRITICAL"),
                "high_count": sum(1 for q in queue if q["severity"] == "HIGH"),
            },
            "changes": [self._serialize_change(c) for c in sorted(changes, key=lambda c: c.record_id)],
            "revalidation_queue": queue,
            "truth_boundary": "REPORT_IS_ADVISORY; IMPLEMENTATION_AND_RUNTIME_REMAIN_NOT_VERIFIED",
        }
        report_core["report_fingerprint"] = sha256_json(report_core)
        return report_core

    @staticmethod
    def _serialize_change(change: Change) -> dict[str, Any]:
        return {
            "record_id": change.record_id,
            "kind": change.kind,
            "reasons": list(change.reasons),
            "severity": change.severity,
            "old": change.old,
            "new": change.new,
        }

    @staticmethod
    def _reverse_dependencies(old_map: dict[str, dict[str, Any]], new_map: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
        reverse: dict[str, set[str]] = {}
        for record_map in (old_map, new_map):
            for record_id, record in record_map.items():
                reverse.setdefault(record_id, set())
                for dep in record["depends_on"]:
                    reverse.setdefault(dep, set()).add(record_id)
        return reverse

    @staticmethod
    def _propagate(direct: dict[str, Change], reverse: dict[str, set[str]]) -> dict[str, dict[str, Any]]:
        impacted: dict[str, dict[str, Any]] = {
            record_id: {"severity": change.severity, "via": []}
            for record_id, change in sorted(direct.items())
        }

        # Traverse independently from each direct change. A per-root seen set
        # guarantees termination even when the union of old/new dependency
        # graphs contains a cycle caused by an edge reversal across snapshots.
        for root_id, change in sorted(direct.items()):
            frontier = [root_id]
            seen = {root_id}
            while frontier:
                parent = frontier.pop(0)
                for child in sorted(reverse.get(parent, ())):
                    if child in seen:
                        continue
                    seen.add(child)
                    entry = impacted.setdefault(child, {"severity": change.severity, "via": []})
                    if SEVERITY_SCORE[change.severity] > SEVERITY_SCORE[entry["severity"]]:
                        entry["severity"] = change.severity
                    if parent not in entry["via"]:
                        entry["via"].append(parent)
                        entry["via"].sort()
                    frontier.append(child)
        return impacted
