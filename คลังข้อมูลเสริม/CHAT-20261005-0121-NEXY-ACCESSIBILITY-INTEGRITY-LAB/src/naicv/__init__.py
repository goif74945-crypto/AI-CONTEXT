"""NEXY Accessibility Integrity Contract + Validator (AI proposal)."""

from .validator import validate_surface
from .model import load_surface, ValidationReport, Finding

__all__ = ["validate_surface", "load_surface", "ValidationReport", "Finding"]
__version__ = "0.1.0"
