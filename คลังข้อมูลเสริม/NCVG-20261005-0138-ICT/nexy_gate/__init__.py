"""NEXY Companion Verification Gate."""

from .gate import GateDecision, evaluate_bundle
from .canonical import canonical_json_bytes, sha256_hex

__all__ = ["GateDecision", "evaluate_bundle", "canonical_json_bytes", "sha256_hex"]
__version__ = "0.1.0"
