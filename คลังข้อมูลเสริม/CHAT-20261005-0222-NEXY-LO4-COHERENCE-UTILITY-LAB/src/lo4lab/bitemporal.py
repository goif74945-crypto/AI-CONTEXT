from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .canonical import fingerprint


class BitemporalError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FactVersion:
    fact_id: str
    subject: str
    attribute: str
    value: Any
    valid_from: int
    valid_until: int | None
    known_at: int
    source_id: str
    authority_rank: int
    supersedes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("fact_id", "subject", "attribute", "source_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise BitemporalError(f"{field_name} must be non-empty")
        if not isinstance(self.valid_from, int) or not isinstance(self.known_at, int):
            raise BitemporalError("timestamps must be integer logical times")
        if self.valid_until is not None:
            if not isinstance(self.valid_until, int):
                raise BitemporalError("valid_until must be int or None")
            if self.valid_until <= self.valid_from:
                raise BitemporalError("valid_until must be greater than valid_from")
        if not isinstance(self.authority_rank, int) or self.authority_rank < 0:
            raise BitemporalError("authority_rank must be a non-negative integer")
        if self.fact_id in self.supersedes:
            raise BitemporalError("a fact cannot supersede itself")
        if len(set(self.supersedes)) != len(self.supersedes):
            raise BitemporalError("duplicate supersedes ids")


@dataclass(frozen=True, slots=True)
class TemporalResolution:
    status: str
    subject: str
    attribute: str
    valid_time: int
    known_time: int
    values: tuple[Any, ...]
    supporting_fact_ids: tuple[str, ...]
    ignored_lower_authority_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]
    report_fingerprint: str


def _validate_ledger(records: tuple[FactVersion, ...]) -> None:
    ids = [record.fact_id for record in records]
    if len(ids) != len(set(ids)):
        raise BitemporalError("duplicate fact_id")
    id_set = set(ids)
    graph = {record.fact_id: tuple(record.supersedes) for record in records}
    for record in records:
        missing = set(record.supersedes) - id_set
        if missing:
            raise BitemporalError(f"unknown superseded fact ids: {sorted(missing)}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise BitemporalError("supersedes graph contains a cycle")
        if node in visited:
            return
        visiting.add(node)
        for parent in graph[node]:
            visit(parent)
        visiting.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node)


def _active(record: FactVersion, *, valid_time: int, known_time: int) -> bool:
    if record.known_at > known_time:
        return False
    if valid_time < record.valid_from:
        return False
    return record.valid_until is None or valid_time < record.valid_until


def resolve_at(
    records: Iterable[FactVersion],
    *,
    subject: str,
    attribute: str,
    valid_time: int,
    known_time: int,
) -> TemporalResolution:
    rows = tuple(sorted(records, key=lambda r: r.fact_id))
    _validate_ledger(rows)
    if not subject.strip() or not attribute.strip():
        raise BitemporalError("subject and attribute must be non-empty")

    candidates = [
        row
        for row in rows
        if row.subject == subject
        and row.attribute == attribute
        and _active(row, valid_time=valid_time, known_time=known_time)
    ]

    if not candidates:
        payload = {
            "status": "UNKNOWN",
            "subject": subject,
            "attribute": attribute,
            "valid_time": valid_time,
            "known_time": known_time,
            "values": [],
            "supporting_fact_ids": [],
            "ignored_lower_authority_ids": [],
            "reason_codes": ["NO_ELIGIBLE_FACT"],
        }
        return TemporalResolution(
            status="UNKNOWN",
            subject=subject,
            attribute=attribute,
            valid_time=valid_time,
            known_time=known_time,
            values=(),
            supporting_fact_ids=(),
            ignored_lower_authority_ids=(),
            reason_codes=("NO_ELIGIBLE_FACT",),
            report_fingerprint=fingerprint(payload),
        )

    superseded: set[str] = set()
    by_id = {row.fact_id: row for row in candidates}

    def mark_ancestors(fact_id: str) -> None:
        row = by_id.get(fact_id)
        if row is None:
            return
        for parent in row.supersedes:
            if parent in by_id and parent not in superseded:
                superseded.add(parent)
                mark_ancestors(parent)

    for row in candidates:
        mark_ancestors(row.fact_id)

    surviving = [row for row in candidates if row.fact_id not in superseded]
    top_rank = max(row.authority_rank for row in surviving)
    top = [row for row in surviving if row.authority_rank == top_rank]
    lower = tuple(sorted(row.fact_id for row in surviving if row.authority_rank < top_rank))

    value_groups: dict[str, list[FactVersion]] = {}
    value_by_fp: dict[str, Any] = {}
    for row in top:
        fp = fingerprint(row.value)
        value_groups.setdefault(fp, []).append(row)
        value_by_fp[fp] = row.value

    sorted_fps = sorted(value_groups)
    status = "PASS" if len(sorted_fps) == 1 else "CONFLICT"
    reasons = ("RESOLVED_SINGLE_VALUE",) if status == "PASS" else ("TOP_AUTHORITY_VALUE_CONFLICT",)
    values = tuple(value_by_fp[fp] for fp in sorted_fps)
    supporters = tuple(sorted(row.fact_id for fp in sorted_fps for row in value_groups[fp]))
    payload = {
        "status": status,
        "subject": subject,
        "attribute": attribute,
        "valid_time": valid_time,
        "known_time": known_time,
        "values": list(values),
        "supporting_fact_ids": list(supporters),
        "ignored_lower_authority_ids": list(lower),
        "reason_codes": list(reasons),
    }
    return TemporalResolution(
        status=status,
        subject=subject,
        attribute=attribute,
        valid_time=valid_time,
        known_time=known_time,
        values=values,
        supporting_fact_ids=supporters,
        ignored_lower_authority_ids=lower,
        reason_codes=reasons,
        report_fingerprint=fingerprint(payload),
    )
