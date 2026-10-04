"""NEXY Shadow Assurance Lab prototype.

Advisory, standalone tooling. It does not execute candidate actions and is not
part of the NEXY.AI implementation repository.
"""

from .comparator import compare_pair
from .gate import evaluate_datasets
from .models import DecisionRecord, EvidenceRef, Finding, GateReport

__all__ = [
    "DecisionRecord",
    "EvidenceRef",
    "Finding",
    "GateReport",
    "compare_pair",
    "evaluate_datasets",
]
