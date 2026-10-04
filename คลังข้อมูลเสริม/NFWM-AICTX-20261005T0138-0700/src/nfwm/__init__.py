"""NEXY Failure Witness Minimizer (NFWM).

AI-proposed external research tooling. This package is not part of NEXY.AI and
must not be treated as canonical NEXY implementation or deployment evidence.
"""

from .analyzer import AnalysisResult, analyze_trace
from .minimize import minimize_violation
from .profile import Profile, load_profile

__all__ = [
    "AnalysisResult",
    "Profile",
    "analyze_trace",
    "load_profile",
    "minimize_violation",
]

__version__ = "0.1.0"
