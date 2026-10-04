from __future__ import annotations

import json
import sys
from pathlib import Path
from dataclasses import asdict

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from lo4_foundry import (
    ActionCandidate, ArchitectureChoice, Authority, BenefitClaim, ConflictSet,
    ConstraintRef, FutureOption, NoveltyDimension, RegretPolicy,
    choose_minimax_regret, evaluate_surprise_budget, integrate_foundry,
    propose_minimal_relaxation, refute_feature, select_option_preserving_choice,
)

surprise = evaluate_surprise_budget([
    NoveltyDimension("architecture", 2400, 3000),
    NoveltyDimension("ux", 1800, 1500),
])
anti = refute_feature([BenefitClaim("cuts-repeat-work", 7800, 3)], 2800, 1500)
relax = propose_minimal_relaxation(
    [
        ConstraintRef("USER_LAW", Authority.USER_LAW, False, 999999),
        ConstraintRef("LO4_LATENCY_TARGET", Authority.EXPERIMENTAL, True, 3),
    ],
    [ConflictSet("latency-vs-depth", ("LO4_LATENCY_TARGET",))],
)
regret = choose_minimax_regret([
    ActionCandidate("small-reversible-pilot", True, False, True, {"normal": 80, "provider_outage": 65}),
    ActionCandidate("full-cutover", False, False, True, {"normal": 100, "provider_outage": -50}),
], RegretPolicy(max_worst_case_regret=1000))
option = select_option_preserving_choice(
    [FutureOption("local-model", 5000), FutureOption("new-provider", 3000), FutureOption("offline", 2000)],
    [
        ArchitectureChoice("adapter-first", True, ("local-model", "new-provider", "offline"), 1000, 500, 7000),
        ArchitectureChoice("provider-locked", True, ("new-provider",), 7000, 9000, 8000),
    ],
)
final = integrate_foundry(surprise, anti, relax, regret, option)

print(json.dumps({
    "surprise": asdict(surprise),
    "anti_feature": asdict(anti),
    "relaxation": asdict(relax),
    "regret": asdict(regret),
    "option": asdict(option),
    "foundry": asdict(final),
}, ensure_ascii=False, indent=2, default=lambda x: x.value if hasattr(x, "value") else str(x)))
