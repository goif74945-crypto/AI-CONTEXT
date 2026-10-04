"""NEXY Consensus Independence Firewall reference implementation.

AI-PROPOSED / NON-GOVERNING. This package evaluates evidence-lineage
independence and cannot grant NEXY authority or final verification.
"""

from .engine import evaluate_consensus
from .models import ConsensusPolicy, ConsensusResult, ContractError

__all__ = ["ConsensusPolicy", "ConsensusResult", "ContractError", "evaluate_consensus"]
__version__ = "0.1.0"
