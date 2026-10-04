"""AI-proposed deterministic bounded interleaving verifier."""

from .engine import static_conflicts, verify_plan
from .model import ModelError, parse_plan

__all__ = ["ModelError", "parse_plan", "static_conflicts", "verify_plan"]
__version__ = "0.1.0"
