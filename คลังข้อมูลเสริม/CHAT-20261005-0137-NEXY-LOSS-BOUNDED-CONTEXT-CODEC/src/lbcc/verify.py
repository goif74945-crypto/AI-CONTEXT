from __future__ import annotations

from dataclasses import dataclass

from .codec import _ledger_root, _loss_ppm, _source_bundle_view, importance
from .model import SCHEMA_VERSION, CodecMetrics, CodecPolicy, CodecResult, CodecStatus, ContextBundle, DroppedRef
from .serialization import canonical_json_bytes, sha256_hex


@dataclass(frozen=True, slots=True)
class VerificationReport:
    passed: bool
    failures: tuple[str, ...]


def verify_against_source(bundle: ContextBundle, result: CodecResult, policy: CodecPolicy) -> VerificationReport:
    failures: list[str] = []
    if result.schema_version != SCHEMA_VERSION:
        failures.append("unsupported result schema_version")
    if result.status != CodecStatus.PASS or result.capsule is None:
        failures.append("result is not PASS with a capsule")
        return VerificationReport(False, tuple(failures))

    capsule = result.capsule
    if capsule.schema_version != SCHEMA_VERSION:
        failures.append("unsupported capsule schema_version")
    if capsule.bundle_id != bundle.bundle_id:
        failures.append("bundle_id mismatch")
    if capsule.source_commitment_sha256 != sha256_hex(_source_bundle_view(bundle)):
        failures.append("source commitment mismatch")
    if len(canonical_json_bytes(capsule)) > policy.max_capsule_bytes:
        failures.append("capsule exceeds policy byte budget")
    if capsule.loss_ppm > policy.max_loss_ppm:
        failures.append("capsule exceeds policy loss budget")

    source_by_id = {a.atom_id: a for a in bundle.atoms}
    retained_ids: set[str] = set()
    for atom in capsule.retained_atoms:
        if atom.atom_id in retained_ids:
            failures.append(f"duplicate retained atom: {atom.atom_id}")
            continue
        retained_ids.add(atom.atom_id)
        source_atom = source_by_id.get(atom.atom_id)
        if source_atom is None:
            failures.append(f"retained atom absent from source: {atom.atom_id}")
        elif source_atom != atom:
            failures.append(f"retained atom mismatch: {atom.atom_id}")

    expected_ledger = tuple(
        sorted(
            (
                DroppedRef(a.atom_id, sha256_hex(a), importance(a))
                for a in bundle.atoms
                if a.atom_id not in retained_ids
            ),
            key=lambda x: x.atom_id,
        )
    )
    if result.loss_ledger != expected_ledger:
        failures.append("loss ledger does not match omitted source atoms")
    if _ledger_root(result.loss_ledger) != capsule.dropped_commitment_sha256:
        failures.append("dropped commitment mismatch")
    if capsule.dropped_count != len(result.loss_ledger):
        failures.append("dropped_count mismatch")

    expected_total = sum(importance(a) for a in bundle.atoms)
    expected_dropped = sum(x.importance for x in result.loss_ledger)
    if capsule.total_importance != expected_total:
        failures.append("total_importance mismatch")
    if capsule.dropped_importance != expected_dropped:
        failures.append("dropped_importance mismatch")

    expected_metrics = CodecMetrics(
        source_atoms=len(bundle.atoms),
        retained_atoms=len(capsule.retained_atoms),
        dropped_atoms=len(result.loss_ledger),
        capsule_bytes=len(canonical_json_bytes(capsule)),
        total_importance=expected_total,
        dropped_importance=expected_dropped,
        loss_ppm=_loss_ppm(expected_dropped, expected_total),
    )
    if result.metrics != expected_metrics:
        failures.append("result metrics mismatch")

    return VerificationReport(not failures, tuple(failures))
