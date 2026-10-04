"""Deterministic interaction-contract analysis for NEXY research."""

from .analyzer import analyze_contract
from .model import ValidationError

__all__ = ["analyze_contract", "ValidationError"]
__version__ = "0.1.0"
