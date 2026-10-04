"""Human Control Surface Assurance (HCAS).

HCAS is an advisory, deterministic linter for machine-readable control-surface
manifests. It does not grant authority and does not modify NEXY.AI.
"""

from .model import Finding, Severity, ValidationReport
from .validator import validate_manifest

__all__ = ["Finding", "Severity", "ValidationReport", "validate_manifest"]
__version__ = "0.1.0"
