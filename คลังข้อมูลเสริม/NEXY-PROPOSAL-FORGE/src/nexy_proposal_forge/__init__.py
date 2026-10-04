"""NEXY Proposal Forge.

This package evaluates AI-proposed feature candidates. It does not authorize,
promote, or implement NEXY.AI requirements.
"""

from .engine import EvaluationResult, evaluate_proposal
from .models import Proposal, ProposalValidationError

__all__ = [
    "EvaluationResult",
    "Proposal",
    "ProposalValidationError",
    "evaluate_proposal",
]

__version__ = "0.1.0"
