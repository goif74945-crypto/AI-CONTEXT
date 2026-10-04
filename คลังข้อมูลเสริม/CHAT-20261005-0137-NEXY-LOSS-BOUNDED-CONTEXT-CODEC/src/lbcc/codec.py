from __future__ import annotations

from fractions import Fraction
from typing import Iterable, Mapping

from .model import (
    PPM,
    SCHEMA_VERSION,
    CodecMetrics,
    CodecPolicy,
    CodecResult,
    CodecStatus,
    ContextAtom,
    ContextBundle,
    ContextCapsule,
    DroppedRef,
    TruthClass,
)
from .security import scan_sensitive
from .serialization import canonical_json_bytes, sha256_hex

_TRUTH_WEIGHT: dict[TruthClass, int] = {
    TruthClass.SOURCE_FACT: 800_000,
    TruthClass.REPO_FACT: 780_000,
    TruthClass.RUNTIME_FACT: 850_000,
    TruthClass.EXTERNAL_FACT: 700_000,
    TruthClass.INFERENCE: 350_000,
    TruthClass.ASSUMPTION: 250_000,
    TruthClass.UNKNOWN: 760_000,
    TruthClass.CONFLICT: 900_000,
    TruthClass.NOT_VERIFIED: 650_000,
}


def importance(atom: ContextAtom) -> int:
    score = _TRUTH_WEIGHT[atom.truth_class]
    score += atom.authority_rank * 1_000
    score += min(len(atom.evidence), 4) * 10_000
    score += min(len(atom.provenance), 4) * 5_000
    return min(score, 1_000_000)


def is_protected(atom: ContextAtom, policy: CodecPolicy) -> bool:
    if atom.immutable:
        return True
    if atom.authority_rank >= policy.protected_authority_rank:
        return True
    return policy.protect_unknown_conflict and atom.truth_class in {
        TruthClass.UNKNOWN,
        TruthClass.CONFLICT,
    }


def _source_bundle_view(bundle: ContextBundle) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_id": bundle.bundle_id,
        "atoms": tuple(sorted(bundle.atoms, key=lambda a: a.atom_id)),
    }


def _atom_ref(atom: ContextAtom) -> DroppedRef:
    return DroppedRef(
        atom_id=atom.atom_id,
        atom_sha256=sha256_hex(atom),
        importance=importance(atom),
    )


def _ledger_root(ledger: Iterable[DroppedRef]) -> str:
    return sha256_hex(tuple(sorted(ledger, key=lambda x: x.atom_id)))


def _loss_ppm(dropped_importance: int, total_importance: int) -> int:
    if total_importance == 0:
        return 0
    return (dropped_importance * PPM + total_importance - 1) // total_importance


def _make_capsule(
    bundle: ContextBundle,
    retained: Iterable[ContextAtom],
    ledger: tuple[DroppedRef, ...],
    total_importance: int,
) -> ContextCapsule:
    retained_tuple = tuple(sorted(retained, key=lambda a: a.atom_id))
    dropped_importance = sum(x.importance for x in ledger)
    return ContextCapsule(
        schema_version=SCHEMA_VERSION,
        bundle_id=bundle.bundle_id,
        source_commitment_sha256=sha256_hex(_source_bundle_view(bundle)),
        retained_atoms=retained_tuple,
        dropped_count=len(ledger),
        dropped_commitment_sha256=_ledger_root(ledger),
        total_importance=total_importance,
        dropped_importance=dropped_importance,
        loss_ppm=_loss_ppm(dropped_importance, total_importance),
    )


def _metrics(bundle: ContextBundle, capsule: ContextCapsule | None, ledger: tuple[DroppedRef, ...]) -> CodecMetrics:
    total_importance = sum(importance(a) for a in bundle.atoms)
    dropped_importance = sum(x.importance for x in ledger)
    return CodecMetrics(
        source_atoms=len(bundle.atoms),
        retained_atoms=len(capsule.retained_atoms) if capsule else 0,
        dropped_atoms=len(ledger),
        capsule_bytes=len(canonical_json_bytes(capsule)) if capsule else 0,
        total_importance=total_importance,
        dropped_importance=dropped_importance,
        loss_ppm=_loss_ppm(dropped_importance, total_importance),
    )


def _capsule_size_from_parts(
    *,
    bundle_id: str,
    source_commitment_sha256: str,
    retained_atom_byte_lengths: Iterable[int],
    dropped_count: int,
    total_importance: int,
    dropped_importance: int,
) -> int:
    """Compute exact canonical capsule size without serializing retained atoms repeatedly.

    The dropped commitment is represented by a 64-byte placeholder because every SHA-256
    hex digest has identical serialized length. This makes the size exact while allowing
    the real ledger/root to be computed once after selection.
    """
    lengths = tuple(retained_atom_byte_lengths)
    skeleton = {
        "schema_version": SCHEMA_VERSION,
        "bundle_id": bundle_id,
        "source_commitment_sha256": source_commitment_sha256,
        "retained_atoms": [],
        "dropped_count": dropped_count,
        "dropped_commitment_sha256": "0" * 64,
        "total_importance": total_importance,
        "dropped_importance": dropped_importance,
        "loss_ppm": _loss_ppm(dropped_importance, total_importance),
    }
    base = len(canonical_json_bytes(skeleton))
    if not lengths:
        return base
    return base + sum(lengths) + len(lengths) - 1


def compact(bundle: ContextBundle, policy: CodecPolicy) -> CodecResult:
    findings = scan_sensitive(bundle)
    atom_importance = {a.atom_id: importance(a) for a in bundle.atoms}
    atom_byte_length = {a.atom_id: len(canonical_json_bytes(a)) for a in bundle.atoms}
    total_importance = sum(atom_importance.values())
    if findings and not policy.allow_sensitive:
        reason = "sensitive content detected: " + ", ".join(
            f"{f.atom_id}:{f.kind}" for f in findings
        )
        return CodecResult(
            schema_version=SCHEMA_VERSION,
            status=CodecStatus.FREEZE,
            reason=reason,
            capsule=None,
            loss_ledger=(),
            metrics=CodecMetrics(
                source_atoms=len(bundle.atoms),
                retained_atoms=0,
                dropped_atoms=0,
                capsule_bytes=0,
                total_importance=total_importance,
                dropped_importance=0,
                loss_ppm=0,
            ),
        )

    protected = [a for a in bundle.atoms if is_protected(a, policy)]
    optional = [a for a in bundle.atoms if not is_protected(a, policy)]
    retained = list(protected)
    retained_ids = {a.atom_id for a in protected}
    retained_importance = sum(atom_importance[a.atom_id] for a in retained)
    retained_byte_lengths = [atom_byte_length[a.atom_id] for a in retained]
    source_commitment = sha256_hex(_source_bundle_view(bundle))

    protected_size = _capsule_size_from_parts(
        bundle_id=bundle.bundle_id,
        source_commitment_sha256=source_commitment,
        retained_atom_byte_lengths=retained_byte_lengths,
        dropped_count=len(bundle.atoms) - len(retained),
        total_importance=total_importance,
        dropped_importance=total_importance - retained_importance,
    )
    if protected_size > policy.max_capsule_bytes:
        initial_ledger = tuple(
            sorted((_atom_ref(a) for a in bundle.atoms if a.atom_id not in retained_ids), key=lambda x: x.atom_id)
        )
        return CodecResult(
            schema_version=SCHEMA_VERSION,
            status=CodecStatus.FREEZE,
            reason="protected atoms exceed max_capsule_bytes",
            capsule=None,
            loss_ledger=initial_ledger,
            metrics=_metrics(bundle, None, initial_ledger),
        )

    ranked = sorted(
        optional,
        key=lambda a: (
            -Fraction(atom_importance[a.atom_id], max(1, atom_byte_length[a.atom_id])),
            -atom_importance[a.atom_id],
            a.atom_id,
        ),
    )

    for atom in ranked:
        candidate_importance = retained_importance + atom_importance[atom.atom_id]
        candidate_lengths = (*retained_byte_lengths, atom_byte_length[atom.atom_id])
        candidate_size = _capsule_size_from_parts(
            bundle_id=bundle.bundle_id,
            source_commitment_sha256=source_commitment,
            retained_atom_byte_lengths=candidate_lengths,
            dropped_count=len(bundle.atoms) - len(retained) - 1,
            total_importance=total_importance,
            dropped_importance=total_importance - candidate_importance,
        )
        if candidate_size <= policy.max_capsule_bytes:
            retained.append(atom)
            retained_ids.add(atom.atom_id)
            retained_importance = candidate_importance
            retained_byte_lengths.append(atom_byte_length[atom.atom_id])

    final_ledger = tuple(
        sorted((_atom_ref(a) for a in bundle.atoms if a.atom_id not in retained_ids), key=lambda x: x.atom_id)
    )
    final_capsule = _make_capsule(bundle, retained, final_ledger, total_importance)
    final_size = len(canonical_json_bytes(final_capsule))
    if final_size > policy.max_capsule_bytes:
        return CodecResult(
            schema_version=SCHEMA_VERSION,
            status=CodecStatus.FREEZE,
            reason="internal size-accounting invariant violated",
            capsule=None,
            loss_ledger=final_ledger,
            metrics=_metrics(bundle, None, final_ledger),
        )
    if final_capsule.loss_ppm > policy.max_loss_ppm:
        return CodecResult(
            schema_version=SCHEMA_VERSION,
            status=CodecStatus.FREEZE,
            reason=(
                f"loss budget exceeded: observed={final_capsule.loss_ppm}ppm "
                f"allowed={policy.max_loss_ppm}ppm"
            ),
            capsule=None,
            loss_ledger=final_ledger,
            metrics=_metrics(bundle, None, final_ledger),
        )

    return CodecResult(
        schema_version=SCHEMA_VERSION,
        status=CodecStatus.PASS,
        reason=None,
        capsule=final_capsule,
        loss_ledger=final_ledger,
        metrics=_metrics(bundle, final_capsule, final_ledger),
    )


def rehydrate(
    capsule: ContextCapsule,
    loss_ledger: tuple[DroppedRef, ...],
    atom_store: Mapping[str, ContextAtom],
) -> ContextBundle:
    if capsule.schema_version != SCHEMA_VERSION:
        raise ValueError(f"unsupported schema_version: {capsule.schema_version}")
    if _ledger_root(loss_ledger) != capsule.dropped_commitment_sha256:
        raise ValueError("loss ledger commitment mismatch")
    retained = {a.atom_id: a for a in capsule.retained_atoms}
    if len(retained) != len(capsule.retained_atoms):
        raise ValueError("duplicate retained atom IDs")
    restored = dict(retained)
    for ref in loss_ledger:
        atom = atom_store.get(ref.atom_id)
        if atom is None:
            raise ValueError(f"missing dropped atom in store: {ref.atom_id}")
        if sha256_hex(atom) != ref.atom_sha256:
            raise ValueError(f"atom hash mismatch: {ref.atom_id}")
        restored[ref.atom_id] = atom
    bundle = ContextBundle(bundle_id=capsule.bundle_id, atoms=tuple(restored.values()))
    if sha256_hex(_source_bundle_view(bundle)) != capsule.source_commitment_sha256:
        raise ValueError("rehydrated source commitment mismatch")
    return bundle
