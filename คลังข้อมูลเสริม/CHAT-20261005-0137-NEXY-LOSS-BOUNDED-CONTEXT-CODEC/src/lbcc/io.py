from __future__ import annotations

from typing import Any

from .model import (
    SCHEMA_VERSION,
    CodecMetrics,
    CodecResult,
    CodecStatus,
    ContextAtom,
    ContextBundle,
    ContextCapsule,
    DroppedRef,
    TruthClass,
)

_ATOM_KEYS = {
    "atom_id", "text", "truth_class", "authority_rank", "provenance", "evidence",
    "immutable", "tags", "valid_from", "valid_to", "metadata"
}


def _reject_unknown(data: dict[str, Any], allowed: set[str], where: str) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ValueError(f"unknown field(s) in {where}: {', '.join(unknown)}")


def atom_from_dict(data: dict[str, Any]) -> ContextAtom:
    _reject_unknown(data, _ATOM_KEYS, "atom")
    return ContextAtom(
        atom_id=str(data["atom_id"]),
        text=str(data["text"]),
        truth_class=TruthClass(data["truth_class"]),
        authority_rank=int(data.get("authority_rank", 0)),
        provenance=tuple(data.get("provenance", ())),
        evidence=tuple(data.get("evidence", ())),
        immutable=bool(data.get("immutable", False)),
        tags=tuple(data.get("tags", ())),
        valid_from=data.get("valid_from"),
        valid_to=data.get("valid_to"),
        metadata=dict(data.get("metadata", {})),
    )


def bundle_from_dict(data: dict[str, Any]) -> ContextBundle:
    _reject_unknown(data, {"bundle_id", "atoms"}, "bundle")
    return ContextBundle(
        bundle_id=str(data["bundle_id"]),
        atoms=tuple(atom_from_dict(x) for x in data["atoms"]),
    )


def result_from_dict(data: dict[str, Any]) -> CodecResult:
    _reject_unknown(data, {"schema_version", "status", "reason", "capsule", "loss_ledger", "metrics"}, "result")
    if data["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported schema_version: {data['schema_version']}")
    capsule_data = data.get("capsule")
    capsule = None
    if capsule_data is not None:
        _reject_unknown(
            capsule_data,
            {
                "schema_version", "bundle_id", "source_commitment_sha256", "retained_atoms",
                "dropped_count", "dropped_commitment_sha256", "total_importance",
                "dropped_importance", "loss_ppm"
            },
            "capsule",
        )
        capsule = ContextCapsule(
            schema_version=capsule_data["schema_version"],
            bundle_id=capsule_data["bundle_id"],
            source_commitment_sha256=capsule_data["source_commitment_sha256"],
            retained_atoms=tuple(atom_from_dict(x) for x in capsule_data["retained_atoms"]),
            dropped_count=int(capsule_data["dropped_count"]),
            dropped_commitment_sha256=capsule_data["dropped_commitment_sha256"],
            total_importance=int(capsule_data["total_importance"]),
            dropped_importance=int(capsule_data["dropped_importance"]),
            loss_ppm=int(capsule_data["loss_ppm"]),
        )
    ledger_items = []
    for x in data.get("loss_ledger", []):
        _reject_unknown(x, {"atom_id", "atom_sha256", "importance"}, "loss_ledger entry")
        ledger_items.append(DroppedRef(str(x["atom_id"]), str(x["atom_sha256"]), int(x["importance"])))
    ledger = tuple(ledger_items)
    m = data["metrics"]
    _reject_unknown(
        m,
        {"source_atoms", "retained_atoms", "dropped_atoms", "capsule_bytes", "total_importance", "dropped_importance", "loss_ppm"},
        "metrics",
    )
    metrics = CodecMetrics(
        source_atoms=int(m["source_atoms"]), retained_atoms=int(m["retained_atoms"]),
        dropped_atoms=int(m["dropped_atoms"]), capsule_bytes=int(m["capsule_bytes"]),
        total_importance=int(m["total_importance"]), dropped_importance=int(m["dropped_importance"]),
        loss_ppm=int(m["loss_ppm"]),
    )
    return CodecResult(
        schema_version=data["schema_version"],
        status=CodecStatus(data["status"]),
        reason=data.get("reason"), capsule=capsule, loss_ledger=ledger, metrics=metrics,
    )
