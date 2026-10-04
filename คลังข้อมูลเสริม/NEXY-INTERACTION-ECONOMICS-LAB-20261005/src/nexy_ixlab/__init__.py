"""NEXY Interaction Economics Lab.

AI-proposed research implementation. This package is not a current NEXY spec.
"""

from .compare import ComparisonVerdict, PlanComparison, compare_plans
from .model import InteractionBudget, InteractionPlan, InteractionStep, StepKind
from .optimizer import OptimizationResult, optimize_plan
from .planner import Action, DecisionContext, DecisionResult, decide_action
from .scorer import PlanAssessment, assess_plan

__all__ = [
    "Action",
    "ComparisonVerdict",
    "DecisionContext",
    "DecisionResult",
    "InteractionBudget",
    "InteractionPlan",
    "InteractionStep",
    "OptimizationResult",
    "PlanComparison",
    "PlanAssessment",
    "StepKind",
    "assess_plan",
    "compare_plans",
    "decide_action",
    "optimize_plan",
]
