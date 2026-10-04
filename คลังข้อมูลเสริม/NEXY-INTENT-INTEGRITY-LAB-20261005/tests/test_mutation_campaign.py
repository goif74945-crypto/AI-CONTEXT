from __future__ import annotations

import copy
import json
import random
import unittest
from pathlib import Path

from nexy_intent_guard import GuardDecision, compare_contracts, evaluate_proposal

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class UnauthorizedContractMutationCampaign(unittest.TestCase):
    """Deterministic mutation campaign for common intent-drift classes."""

    def test_200_semantic_mutations_never_pass_without_exact_approval(self) -> None:
        base = load("base_contract.json")
        mutation_kinds = (
            "objective",
            "requirement_text",
            "criterion_text",
            "criterion_evidence",
            "scope_add",
            "out_scope_remove",
            "protected_repo_remove",
            "stop_remove",
            "unknown_add",
            "assumption_add",
        )

        for seed in range(200):
            rng = random.Random(seed)
            candidate = copy.deepcopy(base)
            kind = mutation_kinds[seed % len(mutation_kinds)]

            if kind == "objective":
                candidate["objective"] += f" mutation-{seed}"
            elif kind == "requirement_text":
                req = rng.choice(candidate["requirements"])
                req["text"] += f" mutation-{seed}"
            elif kind == "criterion_text":
                criterion = rng.choice(candidate["acceptance_criteria"])
                criterion["text"] += f" mutation-{seed}"
            elif kind == "criterion_evidence":
                criterion = rng.choice(candidate["acceptance_criteria"])
                criterion["minimum_evidence"] = "deployment"
            elif kind == "scope_add":
                candidate["scope"]["in_scope"].append(f"extra-{seed}/**")
            elif kind == "out_scope_remove":
                candidate["scope"]["out_of_scope"] = []
            elif kind == "protected_repo_remove":
                candidate["scope"]["protected_repositories"] = []
            elif kind == "stop_remove":
                candidate["stop_conditions"] = candidate["stop_conditions"][1:]
            elif kind == "unknown_add":
                candidate["unknowns"].append(f"Synthetic unknown {seed}")
            elif kind == "assumption_add":
                candidate["assumptions"].append(f"Synthetic assumption {seed}")
            else:  # pragma: no cover
                raise AssertionError(kind)

            report = compare_contracts(base, candidate)
            self.assertEqual(
                report.decision,
                GuardDecision.FREEZE,
                f"seed={seed} kind={kind} unexpectedly escaped freeze: {report.to_dict()}",
            )
            self.assertTrue(report.change_ids, f"seed={seed} kind={kind} produced no change IDs")


class ProposalMutationCampaign(unittest.TestCase):
    def test_150_invalid_execution_proposals_never_pass(self) -> None:
        contract = load("base_contract.json")
        base = load("passing_proposal.json")
        mutation_kinds = (
            "protected_repo",
            "foreign_repo",
            "protected_path",
            "outside_path",
            "missing_req",
            "weak_evidence",
        )

        for seed in range(150):
            proposal = copy.deepcopy(base)
            kind = mutation_kinds[seed % len(mutation_kinds)]

            if kind == "protected_repo":
                proposal["target_repository"] = f"goif74945-crypto/NEXY.AI-{seed}"
            elif kind == "foreign_repo":
                proposal["target_repository"] = f"goif74945-crypto/FOREIGN-{seed}"
            elif kind == "protected_path":
                proposal["touch_paths"] = [f"NEXY.AI/src/{seed}.ts"]
            elif kind == "outside_path":
                proposal["touch_paths"] = [f"unapproved/{seed}.txt"]
            elif kind == "missing_req":
                proposal["covered_requirement_ids"] = ["REQ-001", "REQ-002"]
            elif kind == "weak_evidence":
                proposal["evidence"]["AC-002"] = "static"
            else:  # pragma: no cover
                raise AssertionError(kind)

            report = evaluate_proposal(contract, proposal)
            self.assertEqual(
                report.decision,
                GuardDecision.FREEZE,
                f"seed={seed} kind={kind} unexpectedly escaped freeze: {report.to_dict()}",
            )


if __name__ == "__main__":
    unittest.main()
