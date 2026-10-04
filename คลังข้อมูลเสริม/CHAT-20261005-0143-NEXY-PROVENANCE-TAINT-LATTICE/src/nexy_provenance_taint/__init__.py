"""Reference kernel for deterministic provenance/authority taint propagation.

AI-PROPOSED CONCEPT: this package is an experimental compatibility-oriented lab.
It is not canonical NEXY.AI law and is not integrated into the NEXY.AI runtime.
"""

from .core import ProvenanceEngine
from .wire import artifact_from_record, artifact_to_record, decision_to_record, receipt_from_record, receipt_to_record
from .model import (
    Artifact,
    ReleaseDecision,
    ReleasePolicy,
    SourceSpec,
    Taint,
    TransformContract,
    VerificationReceipt,
)

__all__ = [
    "Artifact",
    "ProvenanceEngine",
    "ReleaseDecision",
    "ReleasePolicy",
    "SourceSpec",
    "Taint",
    "TransformContract",
    "VerificationReceipt",
    "artifact_from_record",
    "artifact_to_record",
    "decision_to_record",
    "receipt_from_record",
    "receipt_to_record",
]
