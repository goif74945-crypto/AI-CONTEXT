"""NEXY Verification Accelerator Mesh prototypes.

These modules are supplemental, model-agnostic prototypes intended for future
integration evaluation. They do not modify or assert implementation of NEXY.AI.
"""

from .correlated_evidence import EvidenceItem, EvidenceRequirement, EvidenceAssessment, assess_evidence
from .metamorphic import MetamorphicRelation, MetamorphicResult, verify_metamorphic
from .counterexample import MinimizationResult, minimize_sequence
from .assumption_planner import Assumption, Experiment, ExperimentPlan, plan_experiments
from .behavioral_canary import CanaryCase, CanaryBaseline, CanaryResult, record_baseline, verify_canaries

__all__ = [
    "EvidenceItem",
    "EvidenceRequirement",
    "EvidenceAssessment",
    "assess_evidence",
    "MetamorphicRelation",
    "MetamorphicResult",
    "verify_metamorphic",
    "MinimizationResult",
    "minimize_sequence",
    "Assumption",
    "Experiment",
    "ExperimentPlan",
    "plan_experiments",
    "CanaryCase",
    "CanaryBaseline",
    "CanaryResult",
    "record_baseline",
    "verify_canaries",
]
