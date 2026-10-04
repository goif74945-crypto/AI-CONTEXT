from __future__ import annotations

import json
import random
import time

from aeul.comet import OverlapEvidence
from aeul.portfolio import PortfolioCandidate, PortfolioPolicy, compose_portfolio
from aeul.q64 import Q64
from aeul.regret import ProposalCandidate, RegretPolicy, UtilityInterval, select_proposal

q = Q64.from_ratio


def main() -> None:
    rng = random.Random(202610050224)
    start = time.perf_counter()
    regret_policy = RegretPolicy({"quality": q(3, 4), "speed": q(1, 4)}, {"quality": q(1, 4)}, q(3, 4))
    regret_select = 0
    for case in range(10000):
        candidates = []
        for j in range(4):
            qlo = rng.randrange(25, 91); qhi = rng.randrange(qlo, 101)
            slo = rng.randrange(0, 91); shi = rng.randrange(slo, 101)
            candidates.append(ProposalCandidate(
                f"r{case}:{j}",
                {"quality": UtilityInterval(q(qlo, 100), q(qhi, 100)), "speed": UtilityInterval(q(slo, 100), q(shi, 100))},
            ))
        if select_proposal(candidates, regret_policy).status == "SELECT":
            regret_select += 1

    portfolio_select = 0
    for case in range(3000):
        items = []
        evidence = []
        for j in range(6):
            items.append(PortfolioCandidate(
                f"p{case}:{j}", q(rng.randrange(30, 91), 100), q(rng.randrange(5, 31), 100),
                q(rng.randrange(5, 26), 100), frozenset({"d" + str(j % 3)})
            ))
        for a in range(6):
            for b in range(a + 1, 6):
                evidence.append(OverlapEvidence(items[a].candidate_id, items[b].candidate_id, q(rng.randrange(0, 51), 100), f"e:{a}:{b}"))
        result = compose_portfolio(
            items, overlap_evidence=evidence,
            policy=PortfolioPolicy(q(4, 5), q(3, 5), 3, 2, q(1, 1))
        )
        if result.status == "SELECT":
            portfolio_select += 1

    print(json.dumps({
        "status": "PASS",
        "seed": 202610050224,
        "regret_cases": 10000,
        "regret_select": regret_select,
        "portfolio_cases": 3000,
        "portfolio_select": portfolio_select,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
