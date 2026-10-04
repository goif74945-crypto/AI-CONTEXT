from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .common import Verdict, canonical_hash


@dataclass(frozen=True)
class ArtifactFile:
    name: str
    media_type: str
    content: bytes
    declared_sha256: str
    classification: str = "INTERNAL"


@dataclass(frozen=True)
class ConsumerProfile:
    profile_id: str
    required_files: frozenset[str]
    allowed_media_types: frozenset[str]
    required_metadata: frozenset[str]
    forbidden_classifications: frozenset[str]
    max_total_bytes: int
    require_hash_match: bool = True


def evaluate(profile: ConsumerProfile, files: tuple[ArtifactFile, ...], metadata: dict[str, str]) -> dict:
    if not profile.profile_id.strip() or profile.max_total_bytes < 0:
        return {"verdict": Verdict.FREEZE.value, "reason_codes": ["INVALID_CONSUMER_PROFILE"]}

    names = [f.name for f in files]
    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    missing_files = sorted(profile.required_files - set(names))
    unsupported_media = sorted(f.name for f in files if f.media_type not in profile.allowed_media_types)
    forbidden_classification = sorted(f.name for f in files if f.classification in profile.forbidden_classifications)
    missing_metadata = sorted(profile.required_metadata - set(metadata))
    empty_metadata = sorted(key for key in profile.required_metadata if key in metadata and not str(metadata[key]).strip())
    total_bytes = sum(len(f.content) for f in files)
    oversize = total_bytes > profile.max_total_bytes
    hash_mismatches = sorted(
        f.name
        for f in files
        if profile.require_hash_match and hashlib.sha256(f.content).hexdigest() != f.declared_sha256.lower()
    )

    reasons: list[str] = []
    if duplicate_names:
        reasons.append("DUPLICATE_FILE_NAME")
    if missing_files:
        reasons.append("MISSING_REQUIRED_FILE")
    if unsupported_media:
        reasons.append("UNSUPPORTED_MEDIA_TYPE")
    if forbidden_classification:
        reasons.append("FORBIDDEN_CLASSIFICATION")
    if missing_metadata or empty_metadata:
        reasons.append("MISSING_REQUIRED_METADATA")
    if oversize:
        reasons.append("PACKAGE_TOO_LARGE")
    if hash_mismatches:
        reasons.append("CONTENT_HASH_MISMATCH")

    file_fingerprints = [
        {
            "name": f.name,
            "media_type": f.media_type,
            "classification": f.classification,
            "actual_sha256": hashlib.sha256(f.content).hexdigest(),
            "bytes": len(f.content),
        }
        for f in sorted(files, key=lambda x: x.name)
    ]
    result = {
        "verdict": Verdict.FREEZE.value if reasons else Verdict.PASS.value,
        "reason_codes": sorted(reasons),
        "total_bytes": total_bytes,
        "duplicate_names": duplicate_names,
        "missing_files": missing_files,
        "unsupported_media": unsupported_media,
        "forbidden_classification": forbidden_classification,
        "missing_metadata": sorted(set(missing_metadata + empty_metadata)),
        "hash_mismatches": hash_mismatches,
        "file_fingerprints": file_fingerprints,
    }
    result["fingerprint"] = canonical_hash({"profile": profile, "metadata": metadata, "result": result})
    return result
