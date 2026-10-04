#!/usr/bin/env python3
"""Deterministic Minimal Blocker Core / Freeze Explanation Engine.

AI-PROPOSED EXPERIMENTAL TOOLING for AI-CONTEXT. This module is intentionally
standalone and uses only Python's standard library. It does not import or mutate
NEXY.AI implementation code.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

STATUS_ORDER = {
    "PASS": 0,
    "UNKNOWN": 1,
    "NOT_VERIFIED": 2,
    "BLOCKED": 3,
    "FAIL": 4,
    "CONFLICT": 5,
}
ALLOWED_STATUSES = frozenset(STATUS_ORDER)
EVIDENCE_CLASS_RANK = {
    "E0_PRESENCE": 0,
    "E1_STATIC": 1,
    "E2_UNIT": 2,
    "E3_INTEGRATION": 3,
    "E4_E2E": 4,
    "E5_RUNTIME": 5,
    "E6_DEPLOYMENT": 6,
    "E7_PHYSICAL": 7,
}
ALLOWED_REPAIR_KINDS = frozenset(
    {"EVIDENCE", "IMPLEMENTATION", "AUTHORITY", "DEPENDENCY", "REVIEW", "OTHER"}
)
MAX_DEPTH = 64
MAX_NODES = 10_000
DEFAULT_MAX_REPAIR_SETS = 256


class SpecError(ValueError):
    """Raised when a blocker-core input violates the engine contract."""


@dataclass(frozen=True)
class EvidenceLeaf:
    leaf_id: str
    declared_status: str
    effective_status: str
    required_class: str | None
    observed_class: str | None
    target_revision: str | None
    observed_revision: str | None
    repair_cost: float
    repair_kind: str
    remediation: str | None
    downgrade_reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.leaf_id,
            "declared_status": self.declared_status,
            "effective_status": self.effective_status,
            "required_class": self.required_class,
            "observed_class": self.observed_class,
            "target_revision": self.target_revision,
            "observed_revision": self.observed_revision,
            "repair_cost": self.repair_cost,
            "repair_kind": self.repair_kind,
            "remediation": self.remediation,
            "downgrade_reasons": list(self.downgrade_reasons),
        }


@dataclass
class EvaluationContext:
    evidence: dict[str, EvidenceLeaf]
    max_repair_sets: int
    node_count: int = 0
    truncated: bool = False

    def visit(self, depth: int) -> None:
        if depth > MAX_DEPTH:
            raise SpecError(f"gate depth exceeds {MAX_DEPTH}")
        self.node_count += 1
        if self.node_count > MAX_NODES:
            raise SpecError(f"gate node count exceeds {MAX_NODES}")


def canonical_json(value: Any) -> str:
    """Return stable JSON suitable for deterministic hashing."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require_nonempty_str(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SpecError(f"{path} must be a non-empty string")
    return value.strip()


def _optional_str(value: Any, path: str) -> str | None:
    if value is None:
        return None
    return _require_nonempty_str(value, path)


def _parse_cost(value: Any, path: str) -> float:
    if value is None:
        return 1.0
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SpecError(f"{path} must be a finite non-negative number")
    numeric = float(value)
    if not math.isfinite(numeric) or numeric < 0:
        raise SpecError(f"{path} must be a finite non-negative number")
    return numeric


def _normalize_evidence(raw: Mapping[str, Any], target_revision: str | None) -> dict[str, EvidenceLeaf]:
    if not isinstance(raw, Mapping) or not raw:
        raise SpecError("evidence must be a non-empty object")

    normalized: dict[str, EvidenceLeaf] = {}
    for raw_id in sorted(raw):
        leaf_id = _require_nonempty_str(raw_id, "evidence key")
        item = raw[raw_id]
        if not isinstance(item, Mapping):
            raise SpecError(f"evidence.{leaf_id} must be an object")

        declared = _require_nonempty_str(item.get("status"), f"evidence.{leaf_id}.status").upper()
        if declared not in ALLOWED_STATUSES:
            raise SpecError(
                f"evidence.{leaf_id}.status must be one of {sorted(ALLOWED_STATUSES)}, got {declared!r}"
            )

        required_class = _optional_str(item.get("required_class"), f"evidence.{leaf_id}.required_class")
        observed_class = _optional_str(item.get("observed_class"), f"evidence.{leaf_id}.observed_class")
        if required_class is not None and required_class not in EVIDENCE_CLASS_RANK:
            raise SpecError(f"evidence.{leaf_id}.required_class is invalid: {required_class!r}")
        if observed_class is not None and observed_class not in EVIDENCE_CLASS_RANK:
            raise SpecError(f"evidence.{leaf_id}.observed_class is invalid: {observed_class!r}")

        leaf_target_revision = _optional_str(
            item.get("target_revision", target_revision), f"evidence.{leaf_id}.target_revision"
        )
        observed_revision = _optional_str(
            item.get("observed_revision"), f"evidence.{leaf_id}.observed_revision"
        )
        repair_kind = _require_nonempty_str(
            item.get("repair_kind", "EVIDENCE"), f"evidence.{leaf_id}.repair_kind"
        ).upper()
        if repair_kind not in ALLOWED_REPAIR_KINDS:
            raise SpecError(
                f"evidence.{leaf_id}.repair_kind must be one of {sorted(ALLOWED_REPAIR_KINDS)}"
            )
        remediation = _optional_str(item.get("remediation"), f"evidence.{leaf_id}.remediation")
        repair_cost = _parse_cost(item.get("repair_cost"), f"evidence.{leaf_id}.repair_cost")

        effective = declared
        reasons: list[str] = []
        if declared == "PASS":
            if required_class is not None:
                if observed_class is None:
                    effective = "NOT_VERIFIED"
                    reasons.append("MISSING_OBSERVED_EVIDENCE_CLASS")
                elif EVIDENCE_CLASS_RANK[observed_class] < EVIDENCE_CLASS_RANK[required_class]:
                    effective = "NOT_VERIFIED"
                    reasons.append("INSUFFICIENT_EVIDENCE_CLASS")
            if leaf_target_revision is not None:
                if observed_revision is None:
                    effective = "NOT_VERIFIED"
                    reasons.append("MISSING_OBSERVED_REVISION")
                elif observed_revision != leaf_target_revision:
                    effective = "NOT_VERIFIED"
                    reasons.append("STALE_OR_WRONG_REVISION")

        normalized[leaf_id] = EvidenceLeaf(
            leaf_id=leaf_id,
            declared_status=declared,
            effective_status=effective,
            required_class=required_class,
            observed_class=observed_class,
            target_revision=leaf_target_revision,
            observed_revision=observed_revision,
            repair_cost=repair_cost,
            repair_kind=repair_kind,
            remediation=remediation,
            downgrade_reasons=tuple(reasons),
        )
    return normalized


def _aggregate_status(statuses: Iterable[str]) -> str:
    values = list(statuses)
    if not values:
        return "UNKNOWN"
    return max(values, key=lambda status: STATUS_ORDER[status])


def _normalize_sets(
    candidates: Iterable[frozenset[str]], max_repair_sets: int
) -> tuple[list[frozenset[str]], bool]:
    """Deduplicate and keep inclusion-minimal repair sets deterministically."""
    unique = sorted(set(candidates), key=lambda s: (len(s), tuple(sorted(s))))
    minimal: list[frozenset[str]] = []
    truncated = False
    for candidate in unique:
        if any(existing.issubset(candidate) for existing in minimal):
            continue
        minimal.append(candidate)
        if len(minimal) >= max_repair_sets:
            truncated = len(unique) > len(minimal)
            break
    return minimal, truncated


def _combine_repair_families(
    families: Sequence[Sequence[frozenset[str]]], max_repair_sets: int
) -> tuple[list[frozenset[str]], bool]:
    if not families:
        return [frozenset()], False
    acc: list[frozenset[str]] = [frozenset()]
    truncated_any = False
    for family in families:
        if not family:
            return [], truncated_any
        generated = (left | right for left in acc for right in family)
        acc, truncated = _normalize_sets(generated, max_repair_sets)
        truncated_any = truncated_any or truncated
    return acc, truncated_any


def _validate_node_shape(node: Mapping[str, Any], path: str) -> str:
    operators = [key for key in ("leaf", "all_of", "any_of", "at_least") if key in node]
    if len(operators) != 1:
        raise SpecError(f"{path} must contain exactly one gate operator")
    extra = set(node) - set(operators) - {"label"}
    if extra:
        raise SpecError(f"{path} has unsupported keys: {sorted(extra)}")
    return operators[0]


def _evaluate_node(node: Any, ctx: EvaluationContext, path: str = "gate", depth: int = 0) -> dict[str, Any]:
    ctx.visit(depth)
    if not isinstance(node, Mapping):
        raise SpecError(f"{path} must be an object")
    operator = _validate_node_shape(node, path)
    label = _optional_str(node.get("label"), f"{path}.label")

    if operator == "leaf":
        leaf_id = _require_nonempty_str(node["leaf"], f"{path}.leaf")
        if leaf_id not in ctx.evidence:
            raise SpecError(f"{path}.leaf references unknown evidence id {leaf_id!r}")
        leaf = ctx.evidence[leaf_id]
        repairs = [frozenset()] if leaf.effective_status == "PASS" else [frozenset({leaf_id})]
        return {
            "operator": "leaf",
            "label": label,
            "leaf_id": leaf_id,
            "status": leaf.effective_status,
            "repair_sets": repairs,
            "children": [],
        }

    if operator in {"all_of", "any_of"}:
        children_raw = node[operator]
        if not isinstance(children_raw, list) or not children_raw:
            raise SpecError(f"{path}.{operator} must be a non-empty array")
        children = [
            _evaluate_node(child, ctx, f"{path}.{operator}[{index}]", depth + 1)
            for index, child in enumerate(children_raw)
        ]
        child_statuses = [child["status"] for child in children]

        if operator == "all_of":
            status = "PASS" if all(s == "PASS" for s in child_statuses) else _aggregate_status(
                s for s in child_statuses if s != "PASS"
            )
            repair_sets, truncated = _combine_repair_families(
                [child["repair_sets"] for child in children], ctx.max_repair_sets
            )
        else:
            if any(s == "PASS" for s in child_statuses):
                status = "PASS"
            elif all(s == "FAIL" for s in child_statuses):
                status = "FAIL"
            else:
                # A failed alternative does not make an OR gate fail when another
                # alternative is merely unresolved. Classify from still-viable paths.
                status = _aggregate_status(s for s in child_statuses if s != "FAIL")
            repair_sets, truncated = _normalize_sets(
                itertools.chain.from_iterable(child["repair_sets"] for child in children),
                ctx.max_repair_sets,
            )
        ctx.truncated = ctx.truncated or truncated
        return {
            "operator": operator,
            "label": label,
            "status": status,
            "repair_sets": repair_sets,
            "children": children,
        }

    raw = node["at_least"]
    if not isinstance(raw, Mapping):
        raise SpecError(f"{path}.at_least must be an object")
    if set(raw) != {"k", "of"}:
        raise SpecError(f"{path}.at_least must contain exactly 'k' and 'of'")
    k = raw["k"]
    children_raw = raw["of"]
    if isinstance(k, bool) or not isinstance(k, int):
        raise SpecError(f"{path}.at_least.k must be an integer")
    if not isinstance(children_raw, list) or not children_raw:
        raise SpecError(f"{path}.at_least.of must be a non-empty array")
    if k < 1 or k > len(children_raw):
        raise SpecError(f"{path}.at_least.k must be between 1 and {len(children_raw)}")

    children = [
        _evaluate_node(child, ctx, f"{path}.at_least.of[{index}]", depth + 1)
        for index, child in enumerate(children_raw)
    ]
    pass_count = sum(child["status"] == "PASS" for child in children)
    fail_count = sum(child["status"] == "FAIL" for child in children)
    if pass_count >= k:
        status = "PASS"
    elif len(children) - fail_count < k:
        # Too many alternatives are already known FAIL for the threshold to be
        # satisfied without repairing at least one hard failure.
        status = "FAIL"
    else:
        viable_unresolved = [
            child["status"] for child in children if child["status"] not in {"PASS", "FAIL"}
        ]
        status = _aggregate_status(viable_unresolved)

    candidates: list[frozenset[str]] = []
    truncated = False
    for indices in itertools.combinations(range(len(children)), k):
        families = [children[index]["repair_sets"] for index in indices]
        combined, local_truncated = _combine_repair_families(families, ctx.max_repair_sets)
        candidates.extend(combined)
        truncated = truncated or local_truncated
        if len(candidates) > ctx.max_repair_sets * 16:
            # Bound candidate explosion before minimization. Deterministic because
            # combinations and child families are deterministically ordered.
            candidates = candidates[: ctx.max_repair_sets * 16]
            truncated = True
            break
    repair_sets, norm_truncated = _normalize_sets(candidates, ctx.max_repair_sets)
    ctx.truncated = ctx.truncated or truncated or norm_truncated
    return {
        "operator": "at_least",
        "label": label,
        "status": status,
        "required": k,
        "pass_count": pass_count,
        "repair_sets": repair_sets,
        "children": children,
    }


def _strip_internal(node: Mapping[str, Any]) -> dict[str, Any]:
    result = {key: value for key, value in node.items() if key not in {"repair_sets", "children"}}
    children = node.get("children", [])
    if children:
        result["children"] = [_strip_internal(child) for child in children]
    return result


def _set_cost(repair_set: Iterable[str], evidence: Mapping[str, EvidenceLeaf]) -> float:
    return sum(evidence[item].repair_cost for item in repair_set)


def _repair_record(repair_set: frozenset[str], evidence: Mapping[str, EvidenceLeaf]) -> dict[str, Any]:
    ids = sorted(repair_set)
    return {
        "evidence_ids": ids,
        "total_cost": _set_cost(ids, evidence),
        "actions": [
            {
                "id": item,
                "repair_kind": evidence[item].repair_kind,
                "remediation": evidence[item].remediation,
                "effective_status": evidence[item].effective_status,
            }
            for item in ids
        ],
    }


def evaluate_spec(spec: Mapping[str, Any], max_repair_sets: int = DEFAULT_MAX_REPAIR_SETS) -> dict[str, Any]:
    """Evaluate a gate and emit a deterministic freeze/pass certificate."""
    if not isinstance(spec, Mapping):
        raise SpecError("input must be a JSON object")
    if max_repair_sets < 1 or max_repair_sets > 4096:
        raise SpecError("max_repair_sets must be between 1 and 4096")

    schema_version = _require_nonempty_str(spec.get("schema_version"), "schema_version")
    if schema_version != "1.0":
        raise SpecError(f"unsupported schema_version {schema_version!r}; expected '1.0'")
    certificate_id = _require_nonempty_str(spec.get("certificate_id"), "certificate_id")

    target = spec.get("target")
    if not isinstance(target, Mapping):
        raise SpecError("target must be an object")
    target_name = _require_nonempty_str(target.get("name"), "target.name")
    target_revision = _optional_str(target.get("revision"), "target.revision")

    allowed_top_level = {"schema_version", "certificate_id", "target", "evidence", "gate", "metadata"}
    extra = set(spec) - allowed_top_level
    if extra:
        raise SpecError(f"unsupported top-level keys: {sorted(extra)}")
    metadata = spec.get("metadata", {})
    if not isinstance(metadata, Mapping):
        raise SpecError("metadata must be an object when provided")

    evidence = _normalize_evidence(spec.get("evidence"), target_revision)
    ctx = EvaluationContext(evidence=evidence, max_repair_sets=max_repair_sets)
    evaluated = _evaluate_node(spec.get("gate"), ctx)
    repair_sets = evaluated["repair_sets"]

    repair_records = [_repair_record(repair_set, evidence) for repair_set in repair_sets]
    repair_records.sort(
        key=lambda record: (
            record["total_cost"],
            len(record["evidence_ids"]),
            tuple(record["evidence_ids"]),
        )
    )
    nonempty_repairs = [record for record in repair_records if record["evidence_ids"]]
    recommended = nonempty_repairs[0] if nonempty_repairs else None

    unsatisfied = [leaf.as_dict() for leaf in evidence.values() if leaf.effective_status != "PASS"]
    status_summary = {name: 0 for name in sorted(ALLOWED_STATUSES)}
    for leaf in evidence.values():
        status_summary[leaf.effective_status] += 1
    status = evaluated["status"]
    payload = {
        "schema_version": "1.0",
        "certificate_id": certificate_id,
        "engine": {
            "name": "nexy-minimal-blocker-core",
            "version": "0.1.0",
            "semantics": "AI-PROPOSED / EXPERIMENTAL / ADVISORY ONLY",
            "hash_scope": "canonical certificate body excluding certificate_sha256",
        },
        "target": {"name": target_name, "revision": target_revision},
        "status": status,
        "decision": "ALLOW" if status == "PASS" else "FREEZE",
        "status_summary": status_summary,
        "unsatisfied_evidence": unsatisfied,
        "minimal_repair_sets": repair_records,
        "recommended_repair_set": recommended,
        "primary_blocker_core": (recommended["evidence_ids"] if recommended is not None else []),
        "recommendation_guarantee": (
            "PARTIAL_DUE_TO_REPAIR_SET_TRUNCATION"
            if ctx.truncated
            else "LOWEST_DECLARED_COST_AMONG_ALL_INCLUSION_MINIMAL_REPAIR_SETS"
        ),
        "explanation_tree": _strip_internal(evaluated),
        "evaluation": {
            "node_count": ctx.node_count,
            "repair_set_limit": max_repair_sets,
            "repair_sets_truncated": ctx.truncated,
        },
        "metadata": dict(metadata),
    }
    payload["certificate_sha256"] = sha256_json(payload)
    return payload


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path | None, value: Any, pretty: bool) -> None:
    text = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        if pretty
        else canonical_json(value) + "\n"
    )
    if path is None:
        sys.stdout.write(text)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute deterministic minimal blocker cores and freeze certificates."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input gate specification JSON")
    parser.add_argument("--output", type=Path, help="Output certificate JSON; defaults to stdout")
    parser.add_argument(
        "--max-repair-sets",
        type=int,
        default=DEFAULT_MAX_REPAIR_SETS,
        help=f"Maximum inclusion-minimal repair sets to retain (default {DEFAULT_MAX_REPAIR_SETS})",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        spec = load_json(args.input)
        certificate = evaluate_spec(spec, max_repair_sets=args.max_repair_sets)
        write_json(args.output, certificate, pretty=args.pretty)
    except (OSError, json.JSONDecodeError, SpecError) as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        return 64
    return 0 if certificate["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
